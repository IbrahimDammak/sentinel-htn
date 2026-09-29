# SENTINEL-HTN — module contract

Every module codes against this file. Change it only by agreement. Shared constants: `sentinel/__init__.py`
(`CHANNELS`, `RISK_SIGN`, `SLOW_CONTEXT`, `ACUTE_CONTEXT`, `QUALITY`, `CUFF`, `DAILY_COLUMNS`,
`PEOPLE_COLUMNS`, `STATES`, `HTN_SBP`, `HTN_DBP`).

**Dependencies: numpy, pandas, scipy, matplotlib only.** There is no scikit-learn, pytest or statsmodels:
- logistic regression → `scipy.optimize.minimize`
- calibration → Platt scaling via the same logistic fit
- AUROC → rank formula

Python 3.10. Style: plain functions, no classes unless needed, no speculative options, short docstrings.

## Data

### `daily` DataFrame — one row per person-day (long format)
| column | type | meaning |
|---|---|---|
| pid | str | person id |
| day | int | days since enrolment (0..end_day) |
| month | int 1–12 | calendar month (season) |
| night_rhr, night_rmssd, still_hr, steps, sleep_dur, sleep_reg | float, NaN = missing | `CHANNELS` |
| ambient_temp | float °C | outdoor temperature (slow context) |
| menses | float 0/1, NaN if N/A | menstrual phase flag (slow context) |
| exercise_min, alcohol, illness | float | acute context (vigorous min previous evening; 0/1; 0/1) |
| firmware | int | device firmware version; a change forces re-baseline |
| sqi | float 0–1 | fraction of the night with good PPG signal |
| rhythm_irregular | int 0/1 | irregular-rhythm gate (AF-like) — the only rhythm use |
| sbp, dbp | float, NaN except cuff days | home cuff (HBPM) readings, day mean |

### `people` DataFrame — one row per person
`pid, age, sex ('F'/'M'), bmi, skin_ita (ITA° skin tone), converter (bool), t_ref (float day of clinical
reference or NaN), onset (float day true drift began — SYNTHETIC ONLY, never a model input), end_day (int)`.

`t_ref` is the day of the first of two consecutive HBPM occasions whose mean is ≥130 systolic or ≥80 diastolic.

## Stage APIs

### data.py
- `make_cohort(n_people=600, days=540, seed=0, converter_rate=0.35) -> (daily, people)`
- `load_csv(daily_path, people_path) -> (daily, people)`: validates the required columns. Missing optional
  columns are filled (context → 0, menses → NaN, firmware → 0, rhythm_irregular → 0, sqi → 1.0).
- `perturb(daily, kind, level, seed=0, channel=None, people=None) -> daily`. `kind` is one of:
  - `'mcar'`: blank a `level` fraction of channel values
  - `'noise'`: add Gaussian noise of `level`×the channel SD
  - `'drop_channel'`: `channel` all NaN
  - `'mnar'`: extra missingness `level`, weighted toward low `skin_ita`; needs `people`
  - `'sensor_fail'`: sqi=0 on 14-day blocks covering a `level` fraction of days

### learn.py — LEARN (RQ1 personal baseline, RQ4 context)
- `quality_gate(daily, sqi_min=0.6, exercise_max=45) -> daily`: adds bool `valid` (sqi ≥ sqi_min,
  rhythm_irregular == 0, and ≥1 channel present). Channel values on invalid days become NaN. On acute-context days
  (exercise_min > exercise_max, alcohol == 1 or illness == 1), `night_rhr`, `night_rmssd` and `still_hr` become NaN,
  and int `ctx_masked` = 1 is set.
- `fit_context(daily) -> ctx`: dict channel → OLS coefs on [1, ambient_temp, sin(2πm/12), cos(2πm/12),
  menses(NaN→0)], fitted on pooled training days.
- `apply_context(daily, ctx) -> daily`: adds `<ch>_adj` = value minus the context effect, excluding the intercept.
- `fit_prior(daily, warmup_days=56) -> prior`: dict channel → {'mu0', 'tau' (between-person SD of person means),
  'sigma' (pooled within-person SD)}, from each training person's first `warmup_days` of `<ch>_adj`.
- `personal_baseline(daily, prior, warmup_valid=28, personal=True) -> resid`. Rows are pid, day, and
  `<ch>_z` for each channel. Each z is RISK_SIGN × (x_adj − m_i) / sqrt(sigma² + v_i), clipped to ±6.
  - m_i, v_i: normal–normal posterior of the person mean from their first `warmup_valid` valid observations,
    shrunk to mu0 with tau.
  - `personal=False` ablation: m_i = mu0, v_i = tau².
  - Also returns `valid`, `ctx_masked`, and bool `baseline_ready` (False during warm-up).
  - A firmware change restarts the warm-up.

### detect.py — DETECT (RQ2 persistence, RQ4)
- `weekly(resid) -> wk`: rows pid, week (= day // 7). Adds:
  - `<ch>_w`: mean z, NaN if fewer than 3 non-NaN days
  - `n_valid`: valid days in the week
  - `evaluable`: n_valid ≥ 4 and baseline_ready for most of the week
  - `dev`: joint deviation, the mean of available `<ch>_w`
  - `ctx_masked`: sum for the week
- `cusum(wk, k=0.25, h=3.0) -> wk`: adds `cusum`, a one-sided upper CUSUM of `dev` per person. Non-evaluable
  weeks carry the previous value forward.
- `persistence(wk, thr=0.5, m=4, n=6) -> wk`: adds
  - `n_eval`: evaluable weeks among the last n
  - `n_exceed`: evaluable weeks with dev > thr among the last n
  - `persist`: n_exceed ≥ m
  - `episodes`: cumulative count of False→True transitions of persist
  - Missing weeks are "not evaluable", never negative.
- `tune_threshold(wk, people, budget=0.5, grid=None) -> thr`: the smallest dev threshold whose persist episodes per
  NON-converter person-year are ≤ budget.

### predict.py — PREDICT (RQ3 risk trajectory)
- `make_landmarks(wk, daily, people, horizon_weeks=26) -> lm`: one row per pid-week with baseline ready, up to
  (excluding) the t_ref week. Columns:
  - identity and label: pid, week, `y` (1 if t_ref ∈ (7·week, 7·(week+horizon)])
  - level: age, sex_m, bmi, cuff_sbp_last, cuff_dbp_last, cuff_days_since, rhr_level (mean `night_rhr_adj` over
    the last 28 days)
  - change: dev, dev_slope12 (OLS slope of dev over the last 12 weeks), cusum, n_exceed, n_eval, persist
  - quality: valid_days_30
  - NaN handling: impute a training median plus a missing indicator; do it inside `fit`, not here.
- `FEATURE_SETS`: dict 'full' / 'level_only' / 'cuff_only' / 'change_only' → column lists. The nulls
  'level_only' and 'cuff_only' are mandatory comparators.
- `fit(lm_fit, lm_cal, cols, l2=1.0, n_boot=20, seed=0) -> model`: penalised logistic regression on standardised
  columns, bootstrapped by person for an uncertainty band, with Platt calibration fitted on `lm_cal` (isotonic tied scores at few events).
- `predict(model, lm) -> lm` with added `p`, `p_lo`, `p_hi` (calibrated; bootstrap 10th/90th percentiles).

### warn.py — WARN (RQ6 three states, evidence)
- `decide(pred, thr_p, min_valid_30=15) -> dec`: adds `state` ∈ STATES.
  - POOR_QUALITY if valid_days_30 < min_valid_30
  - WARNING if p_lo ≥ thr_p and persist
  - otherwise INSUFFICIENT
- `tune_warning(pred, people, budget=0.5, grid=None) -> thr_p`: the smallest thr_p whose WARNING episodes per
  non-converter person-year are ≤ budget.
- `first_warnings(dec) -> DataFrame`: pid, first_warning_week, first_warning_day (NaN if never).
- `ledger(dec, wk, pid, week) -> dict`: the evidence behind one decision, for the report. Keys:
  - state, p, p_lo, p_hi
  - weeks_exceeded (n_exceed/n_eval), episodes, dev_slope12
  - channel_contrib ({ch: mean `<ch>_w` over the last 6 weeks})
  - valid_days_30, ctx_masked_6w, month

### evaluate.py — metrics A–F
- `metrics(dec, people, horizon_weeks=26) -> dict`:
  - A — auroc, auprc (landmark p vs y)
  - B — per converter, lead_days = t_ref − first_warning_day (warnings before t_ref only); sens_lead_0/30/90/180
    and median_lead. An abstention counts as a miss.
  - C — alarms_per_nonconv_py, warning_precision (warned persons converting ≤ horizon after the first warning)
  - D — brier, ece (10 bins)
  - F — aurc (risk–coverage over the confidence p_hi−p_lo), abstention_rate (share of non-WARNING weeks that are
    POOR_QUALITY)
- `by_group(dec, people, col, bins) -> DataFrame`: metrics per group, e.g. skin_ita terciles (E8 fairness).

### run.py — CLI
- `python run.py --synthetic [--n 600 --days 540 --seed 0] --out results/`, or
  `python run.py --daily d.csv --people p.csv --out results/`
- Subject-grouped split: 60% fit / 20% calibration / 20% test.
- `pipeline(daily, people, split, cfg) -> (dec_test, wk_test, models, thresholds)`. `cfg` toggles: `personal`,
  `context`, feature set.
- Runs:
  - the main model
  - ablations: level_only, cuff_only, change_only, no personalisation, no context
  - robustness (E): mcar 0.3/0.6, noise 1.0, drop night_rmssd, mnar 0.4, sensor_fail 0.3
  - fairness by skin_ita tercile
- Writes `results/metrics.json`, `results/report.md` (tables plus one example evidence ledger) and figures
  (calibration curve, lead-time histogram, risk–coverage).

### tests/test_pipeline.py
Plain asserts, runnable with `python tests/test_pipeline.py` on a small cohort (n=150, days=360). It checks that:
- the states are ⊂ STATES and STATES contains no 'STABLE'
- `onset` never appears in any feature set
- AUROC > 0.6 on synthetic data
- abstention rises under mcar 0.6
- the metrics keys exist

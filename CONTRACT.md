# SENTINEL-HTN — module contract

Every module codes against this file. Change it only by agreement. Shared constants: `sentinel/__init__.py`
(`CHANNELS`, `PULSE`, `RISK_SIGN`, `EVIDENCE`, `SLOW_CONTEXT`, `ACUTE_CONTEXT`, `QUALITY`, `CUFF`, `DAILY_COLUMNS`,
`PEOPLE_COLUMNS`, `STATES`, `HTN_SBP`, `HTN_DBP`) and `channels(df, suffix='')` = `CHANNELS` + the `PULSE` channels
with any non-NaN value in `df[c + suffix]`. Every per-channel loop (quality gate, context, prior, baseline, weights,
weekly deviation, perturbations) iterates `channels(...)`, so absent or all-NaN pulse columns leave every stage
exactly as without them.

**Dependencies: numpy, pandas, scipy, matplotlib only** for the core package and `run.py`. The optional
`sentinel/pulse.py` (PPG embeddings) also needs torch (CPU), pyPPG, dotmap and openpyxl, imported inside its
functions; scikit-learn appears only in its PaPaGei reproduction and self-check. Nothing else imports it. In the core:
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
| pulse_htn | float, OPTIONAL (absent or NaN = no pulse data) | `PULSE`: nightly median PaPaGei-S hypertension-head logit (sentinel/pulse.py). RISK_SIGN +1, EVIDENCE 0.5. (An embedding-drift channel, pulse_drift, was removed after the audit: non-directional — it rises with any change, including a BP fall — and near-zero simulated signal.) |

### `people` DataFrame — one row per person
`pid, age, sex ('F'/'M'), bmi, skin_ita (ITA° skin tone), converter (bool), t_ref (float day of clinical
reference or NaN), onset (float day true drift began — SYNTHETIC ONLY, never a model input), end_day (int)`.

`t_ref` is the day of the first of two consecutive HBPM occasions whose mean is ≥130 systolic or ≥80 diastolic.

## Stage APIs

### data.py
- `make_cohort(n_people=600, days=540, seed=0, converter_rate=0.35, effect=1.0, pulse_coupling=PULSE_COUPLING)
  -> (daily, people)`; daily has `DAILY_COLUMNS + PULSE`. The pulse column comes from a separate generator
  `default_rng((seed, 1))` drawn after everything else, so every other column is bit-identical to the cohort without
  them. Pulse simulation is scale-free, in units of the night-to-night SD. PPG-BP (results/ppg_bp/metrics.json
  `simulator_inputs`, final head's scale) supplies only between-person and clip-to-clip quantities: clip-level ICC
  0.52 and an age-adjusted BETWEEN-person slope of 0.0099 within-clip SD per mmHg (final head; results/ppg_bp/metrics.json). **Assumptions** (marked
  `# assumption:` in data.py):
  - night-to-night SD = the clip-to-clip SD (1 unit); night-to-night variability was NOT measured, and no sqrt(n) gain
    is assumed from the nightly median; AR(1) rho 0.3; between-person SD sqrt(ICC / (1 - ICC)) = 1.04 units;
  - within-person coupling `pulse_coupling` (night SD per mmHg of latent SBP, drift + season), default
    `PULSE_COUPLING` = 0.0092 ≈ the between-person slope (0.0099; 0.0092 is an earlier estimate, bracketed by the sweep), which the audit treats as an UPPER bound (between-person
    differences include structural vascular ageing). 0 = the pulse channels carry no BP signal. run.py
    `--pulse-coupling`; results/pulse/coupling_sweep.md compares 0, 0.0092 and 0.0184;
  - pulse is missing whenever the core channels are, plus 10% of worn nights (no clean clip); no acute-context or
    skin-tone effect beyond that shared missingness.
- `load_csv(daily_path, people_path) -> (daily, people)`: validates the required columns. Missing optional
  columns are filled (context → 0, menses → NaN, firmware → 0, rhythm_irregular → 0, sqi → 1.0).
- `perturb(daily, kind, level, seed=0, channel=None, people=None) -> daily`. `kind` is one of:
  - `'mcar'`: blank a `level` fraction of channel values (`channels(daily)`: pulse included when present)
  - `'noise'`: add Gaussian noise of `level`×the channel SD
  - `'drop_channel'`: `channel` (a name or a list, e.g. `PULSE`) all NaN
  - `'mnar'`: extra missingness `level`, weighted toward low `skin_ita`; needs `people`
  - `'sensor_fail'`: sqi=0 on 14-day blocks covering a `level` fraction of days

### learn.py — LEARN (RQ1 personal baseline, RQ4 context)
- `quality_gate(daily, sqi_min=0.6, exercise_max=45) -> daily`: adds bool `valid` (sqi ≥ sqi_min,
  rhythm_irregular == 0, and ≥1 channel present). Channel values on invalid days become NaN. On acute-context days
  (exercise_min > exercise_max, alcohol == 1 or illness == 1), `night_rhr`, `night_rmssd`, `still_hr` and
  `pulse_htn` become NaN, and int `ctx_masked` = 1 is set.
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
- `channel_weights(wk, evidence) -> {ch: weight}`: label-free reliability (1 / variance of the weekly channel mean z on evaluable weeks) times the literature prior `EVIDENCE` (sentinel/__init__.py). Never fitted to labels. A channel without a usable variance gets weight 0, never NaN; `weekly` treats a channel missing from `weights` as 0.
- `weekly(resid, weights=None) -> wk`: rows pid, week (= day // 7); `dev` is the weighted mean of available channels (equal if None). Adds:
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
- `make_landmarks(wk, daily, people, horizon_weeks=26, trend_r=None) -> lm` (trend_r = Kalman observation variance measured on the training split): one row per pid-week with baseline ready, up to
  (excluding) the t_ref week. Columns:
  - identity and label: pid, week, `y` (1 if t_ref ∈ (7·week, 7·(week+horizon)])
  - level: age, sex_m, bmi, cuff_sbp_last, cuff_dbp_last, cuff_days_since, rhr_level (mean `night_rhr_adj` over
    the last 28 days)
  - change: dev, dev_slope12 (OLS slope of dev over the last 12 weeks), cusum, n_exceed, n_eval, persist, trend
    and trend_z (causal Kalman local-linear-trend slope of dev per week, and slope / posterior SD)
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
- `prompts(dec, refractory=REFRACTORY_WEEKS) -> bool Series`: WARNING episode starts that become prompts when a start
  within `refractory` (26) weeks of the person's previous prompt is suppressed. 26 weeks = the prediction horizon
  (chosen to equal the 26-week prediction horizon; not the panel's rule, which was 13 weeks after a normal cuff series). A burden metric only: states, first warnings (asserted in `metrics`), the
  tuned thresholds and the operating curve's chance floor all use the unsuppressed episodes.
- `ledger(dec, wk, pid, week) -> dict`: the evidence behind one decision, for the report. Keys:
  - state, p, p_lo, p_hi
  - weeks_exceeded (n_exceed/n_eval), episodes, dev_slope12
  - channel_contrib ({ch: mean `<ch>_w` over the last 6 weeks})
  - valid_days_30, ctx_masked_6w, month

### evaluate.py — metrics A–F
- `metrics(dec, people, horizon_weeks=26, cal=None) -> dict`:
  - A — auroc, auprc (landmark p vs y); with `cal` (calibration-set predictions, `models['pred_cal']`):
    sens_spec92 = landmark-level sensitivity at p > thr_spec92, where thr_spec92 is the 0.92 quantile (method
    'higher') of p over the CALIBRATION people's y=0 weeks (never chosen on test), and spec_spec92_test = the test
    specificity actually reached; NaN without `cal`
  - B — per converter, lead_days = t_ref − first_warning_day (warnings before t_ref only); sens_lead_0/30/90/180
    and median_lead. An abstention counts as a miss.
  - C — alarms_per_nonconv_py, warning_precision (warned persons converting ≤ horizon after the first warning);
    person-level at the WARNING operating point: TP = converter warned before t_ref, FN = converter not warned
    (abstention = miss), FP = non-converter ever warned, TN = never warned; specificity = TN/(TN+FP),
    f1 = 2TP/(2TP+FP+FN), both CUMULATIVE over follow-up (`followup_median_days`); ppv_person = TP/(TP+FP) at the
    cohort's conversion rate; lr_pos = sens_lead_0 / FP share
  - C, false prompts over time (non-converters; day 0 = first landmark week, after the warm-up):
    false_prompt_6mo / false_prompt_12mo = Kaplan–Meier probability of ≥1 prompt by 6 / 12 months (`km_incidence`,
    censored at the last landmark week); false_prompts_per_nonconv; alarms_per_nonconv_py divides by calendar time
    (end_day + 1, warm-up included), alarms_per_nonconv_monitored_py by landmark weeks only;
    prompts_per_nonconv_py_r26 = alarms_per_nonconv_py after `warn.prompts` (26-week refractory period)
  - B, simulator only (people.onset; NaN on real data): sens_post_onset_30/90 = sens_lead_30/90 with a first warning
    before the drift onset counted as a miss; n_pre_onset_first_warnings
  - D — brier, ece (10 bins)
  - F — aurc (risk–coverage over the confidence p_hi−p_lo), abstention_rate (share of non-WARNING weeks that are
    POOR_QUALITY)
- `by_group(dec, people, col, bins, cal=None) -> DataFrame`: metrics per group, e.g. skin_ita or age terciles.

### run.py — CLI
- `python run.py --synthetic [--n 600 --days 540 --seed 0] --out results/`, or
  `python run.py --daily d.csv --people p.csv --out results/`
- Subject-grouped split: 60% fit / 20% calibration / 20% test.
- `pipeline(daily, people, split, cfg) -> (dec_test, wk_test, models, thresholds)`. `cfg` toggles: `personal`,
  `context`, feature set, `weights`, `pulse` (False, the default, drops the PULSE columns).
- **Pulse channels are OFF by default** (`BASE['pulse'] = False`): unvalidated channels have to earn their way in. The
  pulse channels have only cross-sectional, between-person evidence (PPG-BP, fingertip PPG at rest, one cuff
  reading); their within-person coupling and night-to-night noise are assumptions. So the main model, and the
  paper's, is the model without them (identical to results/weighted), and `with_pulse` is reported next to it as a
  variant whose gain is conditional on the assumed coupling.
- Runs:
  - the main model
  - ablations: level_only, cuff_only, change_only, no personalisation, no context, equal_weights,
    reliability_only, with_pulse (main + pulse_htn)
  - robustness (E): mcar 0.3/0.6, noise 1.0, drop night_rmssd, mnar 0.4, sensor_fail 0.3; plus
    with_pulse_drop_pulse (the with_pulse model with its pulse channels removed at test time only)
  - fairness by skin_ita tercile; the same metrics by age tercile (model behaviour: age has no causal role in
    the simulator)
  - operating curve: per warning budget (0.25/0.5/1/2 per non-converter person-year, re-tuned on calibration people)
    Se0/Se30/Se90, realised alarms and precision for full, level_only, cuff_only, with_pulse, plus the chance floor
    (random warnings at the UNSUPPRESSED budget rate)
  - `--pulse-coupling X`: synthetic cohort with assumed within-person pulse coupling X (stored in metrics.json)
  - `--lifesnaps`: the transfer model is trained without the pulse columns (LifeSnaps has none)
  - `--summary DIR [--ref DIR]`: DIR/summary.md, mean ± SD over DIR/seed*/metrics.json: main vs with_pulse at
    matched alarm rates (with_pulse's Se read off its operating curve at main's realised test alarm rate), false prompts
    over time, suppression burden, pre-onset warnings; with --ref, every value shared with ref's metrics.json must be
    identical
  - `--sweep DIR... --out OUT`: OUT/coupling_sweep.md, with_pulse vs main per coupling (one run root per coupling),
    at own operating points and at matched alarm rates
- Writes `results/metrics.json`, `results/report.md` (tables plus one example evidence ledger) and figures
  (calibration curve, lead-time histogram, risk–coverage).

### tests/test_pipeline.py
Plain asserts, runnable with `python tests/test_pipeline.py` on a small cohort (n=150, days=360). It checks that:
- the states are ⊂ STATES and STATES contains no 'STABLE'
- `onset` never appears in any feature set
- AUROC > 0.6 on synthetic data
- abstention rises under mcar 0.6
- the metrics keys exist
- the default run has no pulse channel; with pulse on it gets a weight; an all-NaN pulse column with pulse on
  gives exactly the default decisions

### pulse.py — optional PPG embeddings (torch; not imported by the core)
- PPG-BP experiment (`python -m sentinel.pulse`): PaPaGei reproduction; repeated-CV demographics vs embeddings for
  labels named by definition (`LABELS`: sbp120 = SBP ≥ 120 on one cuff reading, stage12_vs_normal = SBP ≥ 140 vs
  < 120, and the EXPLORATORY sbp130_dbp80 added after the audit); the gain c − a with a Nadeau–Bengio corrected CI
  and an age×sex-stratified permutation test (repeat percentiles are split variability only); age bands; noise
  decomposition (fold scales and the final head's scale, `simulator_inputs`); head → results/ppg_bp/{summary.md,
  metrics.json, head.npz}. head.npz stores `label` and `domain` (fingertip PPG at rest, not validated on wrist PPG
  at night).
- `pulse_channels(nights, fs, model, head) -> pulse_htn` per night for one person; `nights` = list of lists of raw
  clean clips (≤ 10 s). `night_htn` = median head logit of the night's clips (NaN without clips).

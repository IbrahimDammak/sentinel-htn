# AI engineer panel note: RQ3 early detection (branch `rq3-trend`)

## What changed

| File | Function | Change |
|---|---|---|
| `sentinel/predict.py` | `local_trend` (new) | Causal Kalman filter with a local linear trend (level + slope per week), vectorised over people, run on the weekly `dev`. Weeks that are not evaluable get a prediction step only. Returns the filtered slope and its posterior SD. |
| `sentinel/predict.py` | `make_landmarks`, `CHANGE` | New features `trend` (slope) and `trend_z` (slope / SD), used in `full` and `change_only` only. The nulls are unchanged. |
| `run.py` | `pipeline` | Keeps the calibration predictions (`models['pred_cal']`). |
| `run.py` | `operating_curve` (new), `figures`, `write_report`, `main` | Operating curve, `lead_vs_budget.png`, and a table in `report.md`. |
| `tests/test_pipeline.py` | — | No-leakage assert: changing weeks > t leaves the trend at weeks ≤ t unchanged. |
| `CONTRACT.md`, `README.md` | — | Document the new columns and the figure. |

The filter constants are fixed, not tuned on outcomes:
- observation SD 0.2 (measured: 0.21 among fit-split non-converters)
- level noise 0.03 per week, slope noise 0.003 per week
- prior slope SD 0.01

`dev` at week w uses only days ≤ 7w+6, and `onset` is in no feature set. The outputs are in `results/rq3_trend/seed{0,1,2}/`. The baseline files `results/seed*` and `summary_3seeds.md` are unchanged; a re-run of the old feature set reproduces them exactly.

## Results (n=1,200, seeds 0–2, mean ± SD)

| run | AUROC | AUPRC | Se@0 | Se@30 | **Se@90** | Se@180 | alarms/nc-py | precision |
|---|---|---|---|---|---|---|---|---|
| full, before | 0.638±0.041 | 0.132±0.018 | 0.489±0.101 | 0.334±0.074 | **0.203±0.052** | 0.135±0.048 | 0.463±0.020 | 0.182±0.052 |
| **full, after** | **0.648±0.029** | **0.150±0.022** | **0.590±0.090** | **0.483±0.078** | **0.190±0.017** | 0.068±0.038 | 0.493±0.023 | **0.211±0.046** |
| change_only, before | 0.630±0.042 | 0.121±0.019 | 0.464±0.115 | 0.325±0.107 | 0.133±0.072 | 0.059±0.044 | 0.496±0.062 | 0.218±0.069 |
| change_only, after | 0.643±0.029 | 0.145±0.025 | 0.573±0.062 | 0.489±0.051 | 0.157±0.054 | 0.052±0.039 | 0.488±0.023 | 0.220±0.038 |
| level_only | 0.578±0.025 | 0.083±0.003 | 0.419±0.023 | 0.303±0.048 | 0.219±0.051 | 0.167±0.036 | 0.372±0.069 | 0.153±0.022 |
| cuff_only | 0.561±0.022 | 0.080±0.010 | 0.432±0.103 | 0.294±0.078 | 0.205±0.048 | 0.143±0.034 | 0.441±0.080 | 0.143±0.024 |

### Early-warning operating curve (Se@90, realised test alarms per non-converter person-year in brackets)

For each budget, `thr_p` is re-tuned on the calibration people. **Chance** is warnings at random times at the budget rate, between baseline-ready and t_ref − 90 d.

| budget | full, before | full, after | level_only | cuff_only | chance |
|---|---|---|---|---|---|
| 0.25 | 0.119 (0.22) | 0.105 (0.28) | 0.160 (0.20) | 0.154 (0.24) | 0.132 |
| 0.5 | 0.203 (0.46) | 0.190 (0.49) | 0.219 (0.37) | 0.205 (0.44) | 0.244 |
| 1 | 0.319 (0.98) | 0.325 (0.99) | 0.343 (0.94) | 0.363 (0.98) | 0.420 |
| 2 | 0.410 (1.29) | 0.410 (1.29) | 0.410 (1.29) | 0.410 (1.29) | 0.644 |

At budget 2 all models coincide. The persistence watch tier caps warnings at about 1.3 per person-year, so `thr_p` reaches 0 and the rule is persistence only.

## Did RQ3 improve?

**Not at 90 days.** Se@90 is 0.190 ± 0.017, against 0.203 before, 0.219 for level_only and 0.205 for cuff_only. These differences are within seed noise, and the ranking is the same at every budget.

Closer to the diagnosis, the trend helps clearly:
- Se@30 rises from 0.334 to 0.483, above both nulls (about 0.30).
- Se@0 rises from 0.489 to 0.590.
- AUPRC is up 14% and precision up 16%, still within the 0.5 alarm budget.

Se@180 halves because the warnings now move toward the real drift. Risk-adaptive persistence (b) was not added, since (a) did not help at 90 days.

Two reasons explain the 90-day result:
1. **Label timing.** In the synthetic generator (seed 0), the median gap from drift onset to t_ref is 121 days. At 90–120 days before t_ref, the mean converter `dev` is 0.10, against a weekly noise SD of 0.21. For most converters there is almost no signal 90 days out.
2. **Se@90 rewards untimely alarms.** At every budget, the random-timing floor is above all three models. Any first warning ≥ 90 days early counts, even one long before the drift began. The small "wins" of level_only and cuff_only are diffuse static-risk alarms, not early detection.

## Mapping to strap-only data (CONTRACT.md columns)

| Source | Columns |
|---|---|
| **Wrist strap (PPG + accelerometer)** | `night_rhr`, `night_rmssd`, `still_hr`, `steps`, `sleep_dur`, `sleep_reg`, `exercise_min`, `sqi`, `rhythm_irregular`, `firmware`, `day` |
| **Phone** | `month`, `ambient_temp` (location → weather), `alcohol`, `illness`, `menses` (self-report or cycle app); `age`, `sex`, `bmi`, `skin_ita` (onboarding) |
| **Home cuff** | `sbp`, `dbp`: the labels (`t_ref`) and the `cuff_*` level features |

All change features and `rhr_level` come from the strap alone. With the trend features, the strap-only `change_only` model almost matches `full`: AUROC 0.643 vs 0.648. The cuff is still needed for labels, and the phone supplies context.

## Next best improvement

1. **Fix the yardstick.** Report Se@90 as skill above the chance floor, plus a timely window: the first warning falls 90–182 days before t_ref.
2. **Raise the signal-to-noise ratio.** Run `local_trend` on each channel's weekly z so the model can weight night_rhr and night_rmssd. Train a lead-shifted label, t_ref ∈ (t+90, t+182] days.
3. **Validate on real data.** Real drift takes years, not 120–200 days.

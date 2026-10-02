# SENTINEL-HTN

Personalised, uncertainty-aware early warning of emerging hypertension from wearable (AIoT) data.

## The problem

The BioVance challenge (IEEE EMBS Tunisia) asks whether longitudinal multimodal wearable data can show a person
drifting from their own baseline toward hypertension **before clinical detection**. The signals are noisy, individual,
context-dependent and often missing, and an early but unreliable warning is not useful. So the system must:

`X(1:t) -> personal baseline -> change -> trajectory -> early warning`

and report a risk estimate, an early-warning time, its uncertainty, the evidence behind it and a data-quality
assessment. The clinical reference `t_ref` is the first of two consecutive home-cuff (HBPM) occasions averaging
>= 130 systolic or >= 80 diastolic.

## Pipeline

| Stage | File | Research question | What it does |
|---|---|---|---|
| Learn | `sentinel/learn.py` | RQ1 personalisation, RQ4 context | quality gate; regress out slow context (temperature, season, menses); mask acute context (exercise, alcohol, illness); shrinkage baseline per person, restarted on a firmware change |
| Detect | `sentinel/detect.py` | RQ2 temporal reasoning, RQ4 | weekly joint deviation, CUSUM, persistence rule (m of last n weeks); missing weeks are "not evaluable", never negative |
| Predict | `sentinel/predict.py` | RQ3 early detection | landmark-week logistic risk of conversion within 26 weeks, bootstrap uncertainty band, Platt calibration; null comparators (`level_only`, `cuff_only`) |
| Warn | `sentinel/warn.py` | RQ6 uncertainty, evidence | three-state decision with abstention; two tiers — persistence "watch" tier (2 episodes/person-year) confirmed by the risk gate tuned to 0.5 alarms/non-converter person-year; per-decision evidence ledger |
| Evaluate | `sentinel/evaluate.py`, `run.py` | RQ5 reliability | metrics A-F, ablations, robustness (missingness, noise, dropped channel, sensor failure), fairness by skin tone |

`sentinel/data.py` holds the synthetic cohort, the CSV loader and the perturbations. The interfaces are fixed in `CONTRACT.md`.

## Run

```
pip install -r requirements.txt
python run.py --synthetic --quick --out results_quick      # ~15 s smoke run (too few converters for stable metrics)
python run.py --synthetic --out results                     # default: 600 people, 540 days
python run.py --synthetic --n 1200 --seed 0 --out results/seed0   # the setting behind results/summary_3seeds.md (seeds 0-2)
python run.py --daily daily.csv --people people.csv --out results   # organiser data (schema in CONTRACT.md)
python run.py --lifesnaps rais_anonymized/csv_rais_anonymized/daily_fitbit_sema_df_unprocessed.csv --n 1200 --out results/lifesnaps
#   real-world transfer test on LifeSnaps (71 people, 4 months, Fitbit; kaggle datasets download -d skywescar/lifesnaps-fitbit-dataset):
#   no BP labels, so it reports real coverage, abstention and false-alarm rates next to synthetic non-converters
python tests/test_pipeline.py                               # end-to-end test (400 people, ~10 s)
python -m sentinel.evaluate                                 # metric self-check against hand-computed values
```

Current synthetic results (3 seeds, 1,200 people each): `results/summary_3seeds.md`; per-seed reports, figures and an
example evidence ledger in `results/seed*/`.

Options: `--n`, `--days`, `--seed`, `--quick` (n=150, days=360, 5 bootstrap resamples). The split is subject-grouped
60/20/20 (fit / calibration / test), stratified by converter. Every model, threshold and calibrator is fitted on clean
fit/calibration people; robustness runs perturb only the test people's data.

## Outputs (in `--out`)

- `metrics.json`: main model, ablations, robustness, fairness, thresholds and an example ledger
- `report.md`: tables for metrics A-F, ablations with deltas vs the full model, robustness, fairness by skin_ita tercile, and one evidence ledger for a warned converter
- `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png` (sensitivity at >= 90 d lead vs warning budget for full, level_only, cuff_only)

Metrics: A predictive (AUROC, AUPRC), B early detection (lead time, sensitivity at 0/30/90/180 days lead),
C false-alarm burden (alarms per non-converter person-year, warning precision), D calibration (Brier, ECE),
E robustness, F uncertainty quality (AURC, abstention rate).

## The three states

| State | Meaning |
|---|---|
| `WARNING` | sufficient evidence: the calibrated risk lower bound clears the threshold **and** the deviation is persistent |
| `INSUFFICIENT` | no reliable conclusion; keep monitoring |
| `POOR_QUALITY` | too few valid days in the last 30; any warning is suppressed |

There is no "stable" state: absence of a warning is not a claim of health.

## Repository layout

| Path | Contents |
|---|---|
| `sentinel/` | the four pipeline stages, data generator/loader, metrics |
| `run.py`, `tests/` | CLI and end-to-end test |
| `CONTRACT.md` | data schema and module APIs (use it to plug in the organiser dataset) |
| `results/` | synthetic results: `summary_3seeds.md`, per-seed reports and figures |
| `debate/` | the evidence base behind the design: challenge brief, six expert position papers, cross-critiques, defences, citation audits and the chair's verdict (`debate/verdict/verdict.md`) |

## Limitations

- **Synthetic data.** All results come from a simulated cohort until the organiser dataset arrives. Effect sizes, missingness and the label process are assumptions, so numbers show relative behaviour (ablations, robustness), not clinical performance. The quick cohort has very few test converters and its metrics are noisy.
- **EM sensing is an optional pilot tier and is not in this code.** The pipeline uses only PPG-derived heart rate, HRV, activity, sleep and context channels.
- **No mmHg output.** The system estimates the risk of conversion, not a blood-pressure value. Home-cuff readings serve only as labels and as a level feature.
- **Not a diagnostic.** It is a research prototype for early-warning; a warning means "get a proper cuff measurement", not a diagnosis.

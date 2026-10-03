# Juror 4 (ML, health time series): SENTINEL-HTN

## 1. Deliverable compliance
- **Paper:** all 10 sections present; about 5 pages, which is borderline, and not compiled. The author block is a TODO (`main.tex:13`).
- **Slides:** missing.
- **Repo:** GitHub `main` lacks the paper and trend model.

## 2. Verification log
- **Test:** `python tests/test_pipeline.py` passed in about 5 s (AUROC 0.616).
- **Numbers vs `results/rq3_trend/seed*/metrics.json`:** all of these match.
  - AUROC 0.648, AUPRC 0.150;
  - Se30 0.483;
  - alarms 0.493/py;
  - ECE 0.006;
  - chance Se90 0.244;
  - 77/131 converters warned;
  - noise alarms 0.991/py.
- **Caveat on the SDs:** they are population SDs (ddof=0). The sample SD for AUROC is 0.035, not 0.029.
- **Re-run:** seed 0 reproduces exactly.
- **Fresh seeds 3–5** (scratch script, no repo edits):
  - AUROC 0.646, which replicates.
  - Se30 **0.418** against the reported 0.483. It stays above chance (0.300); without the trend it is 0.290.
  - Se90 0.179, still below chance (0.241).
  - My personal cuff-trajectory null stays at chance (AUROC 0.54–0.59).

**Leakage hunt: no code-level leakage.** The split is by subject (`run.py:32`). Context, prior and thresholds are fitted on fit/cal only (`run.py:72-84`). Landmarks stop before the t_ref week (`predict.py:51`), the cuff lookup is backward-only (`predict.py:65`), perturbations touch test data only (`run.py:90`), and the Kalman causality test is at `tests/test_pipeline.py:25`.

**Evaluation flaws found:**
1. **Circular simulator.** The model encodes the generator's structure exactly:
   - The 45-min exercise mask (`learn.py:10`) matches the generator's `ex > 45` effect (`data.py:48,56`).
   - The covariates are linear in temperature, season and menses (`learn.py:21`), exactly like the generator (`data.py:41-43,56`).
   - The firmware step (`data.py:53`) is exactly what the warm-up restart handles (`learn.py:73`).
   - Every channel carries the assumed risk sign (`data.py:8` vs `__init__.py:8`).

   So RQ1 and RQ4 gains partly hold by construction.
2. **Test-set reuse.** The trend features were developed and reported on the same seeds 0–2. On fresh seeds the Se30 gain shrinks by about 25%.
3. **Se30 chance floor not reproducible.** The code computes the floor only at L=90 (`run.py:110`), so the 0.301 in the paper appears nowhere in the repo. I get 0.295 on seed 0 with the same formula at L=30.
4. **Calibration overstated.**
   - The Brier skill score is only 0.03–0.05.
   - 85% of risks are below 0.1, so the equal-width-bin ECE (`evaluate.py:33`) is trivially small.
   - AURC ranks by band width (`evaluate.py:41`), which tracks low p. It is not evidence about uncertainty.
   - Se180 halved with the trend (0.135 to 0.068) and is not reported.

## 3. Scores

| RQ | Score | Evidence |
|---|---|---|
| RQ1 Personalization | 7 | Shrinkage baseline; without it AUPRC falls from 0.150 to 0.114, but the simulator guarantees the gain. |
| RQ2 Temporal | 7 | CUSUM, 4-of-6 persistence with missing weeks treated as neutral, and a causal Kalman trend with a unit test. No BOCPD or learned comparator. |
| RQ3 Early detection | 5 | Se30 beats the random-alarm floor, including on fresh seeds (0.42 vs 0.30). Nothing beats chance at 90 d; precision 0.21. |
| RQ4 Context | 5 | Tested only against the confounders it was built to match; no misspecification test. |
| RQ5 Reliability | 6 | Five test-only perturbations plus fairness terciles. Noise doubles alarms and abstention is 4× higher in the darkest tercile; both reported, neither fixed. |
| RQ6 Uncertainty | 5 | Abstention is a valid-day count (`warn.py:9`) and the band is a parameter bootstrap. At 60% MCAR, AUROC is 0.583 while abstention only moves from 0.11 to 0.14. |
| **Total** | **35/60** | |

## 4. Strengths and weaknesses

**Strengths**
1. A random-alarm chance floor, and an admission that no model beats chance at 90 days.
2. Leakage-clean, exactly reproducible, with a causality unit test.
3. Event-level metrics: abstention counts as a miss, and alarms are per non-converter person-year.

**Weaknesses**
1. All evidence comes from a self-made simulator that mirrors the model, so it is circular.
2. The only model is a single L2 logistic regression, with no GBM, GRU-D/mTAN or wearable foundation-model comparator.
3. Calibration and uncertainty rest on uninformative metrics.

## 5. Q&A questions
1. Your mask threshold is the simulator's exercise threshold. How do AUPRC and alarms change with a 30-minute threshold, a nonlinear temperature effect, or unmodelled sleep apnoea?
2. The trend was designed and scored on seeds 0–2, and on my fresh seeds Se30 is 0.42. Which number goes in the paper?
3. With a Brier skill score of about 0.04, why call calibration "good"? And does band width predict error once you condition on p?

## 6. Predicted placement
**Top-3.** It is the most self-critical evaluation a student team is likely to show, which fits the brief. AUROC 0.65 on synthetic data will look weak beside transformer entries, and the missing slides and unpushed repo cost points. It could win only with complete deliverables and a solid defence of the simulator.

## 7. Must-fix items
1. Produce the slide deck, push `rq3-trend` and the paper to `main`, and fill in the authors.
2. Report fresh seeds 3–5 and sample SDs, and add L=30 to the chance-floor code.
3. Run a simulator misspecification stress test: a different exercise threshold, a nonlinear temperature effect, and one unmodelled confounder.
4. Replace the ECE claim with the Brier skill score and a calibration slope, and report Se180.
5. Add a GBM or GRU-D comparator, or justify its absence.

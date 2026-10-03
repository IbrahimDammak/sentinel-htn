# PPG-BP: frozen PaPaGei-S embeddings vs demographics for cuff SBP level (real data, cross-sectional)

Data: PPG-BP (Liang 2018, CC0): 219 hospital participants in China; ONE seated upper-arm cuff reading and three 2.1-s fingertip PPG clips each. Antihypertensive treatment is NOT recorded (a treated, controlled hypertensive counts as < 120); the cohort includes 38 people with diabetes, 20 with cerebral infarction and 25 with cerebrovascular disease, so the embeddings may encode a vascular-disease or vascular-age phenotype that chronological-age adjustment does not remove. Embeddings: PaPaGei-S (frozen), the authors' preprocessing; subject = mean of the 3 clip embeddings. This tests whether pulse shape carries information about BP level BETWEEN people; tracking of BP change WITHIN a person is not tested.

Labels (by definition): **sbp120** = SBP >= 120 mmHg on a single cuff reading (PPG-BP non-'Normal'; PaPaGei's label); **stage12_vs_normal** = Stage 1-2 vs Normal (middle band excluded) = SBP >= 140 vs < 120 mmHg; extreme-groups design, so AUROC is inflated by spectrum bias (not a screening-population figure); **sbp130_dbp80** = EXPLORATORY: SBP >= 130 or DBP >= 80 mmHg (ACC/AHA 2025 stage 1 = the t_ref threshold); added after the audit, NOT pre-specified.

## 1. Reproduction of PaPaGei's benchmark (their split, recipe and sklearn probe)

Train 123, test = their test + val 82 (52 positive); label sbp120; AUROC [500-bootstrap 95% CI].

| probe input | AUROC [95% CI] | GridSearchCV choice |
|---|---|---|
| PaPaGei-S embeddings | 0.694 [0.549, 0.808] | {'C': 0.1, 'max_iter': 100, 'penalty': 'l2', 'solver': 'lbfgs'} |
| demographics (age, sex, BMI), same probe | 0.794 [0.685, 0.887] | {'C': 1, 'max_iter': 100, 'penalty': 'l2', 'solver': 'lbfgs'} |

Paired bootstrap difference embeddings - demographics: -0.100 [-0.256, +0.057]. Sensitivity of the embedding AUROC to C (shown only; never used for a choice): C=0.01: 0.731, C=0.1: 0.694, C=1: 0.665, C=10: 0.655, C=100: 0.658. Consistent with the authors' own Table 15 (PaPaGei, ICLR 2025, Appendix E: demographics 0.77 [0.65-0.88], PaPaGei-S 0.77 [0.68-0.87], PaPaGei-S + demographics 0.80): age alone reaches the published embedding figure, and our embedding estimate lies within the published CI.

## 2. Repeated stratified 5-fold subject-level CV (20 repeats, seeds 0-19)

a: demographics, b: embeddings, c: demographics + embeddings. A repeat's AUROC is the mean over its 5 outer folds; cells show the mean over repeats [2.5-97.5 percentiles over repeats = **split-to-split variability, not a confidence interval**: the repeats reuse the same people]. Uncertainty of the gain c - a: Nadeau-Bengio corrected resampled t-test on the fold-level differences (n_test/n_train = 0.25), and a permutation test that shuffles the embeddings within age-decile x sex strata (100 permutations, 3 CV repeats each). Standardisation on training folds only; no PCA; demographics L2 = 1.0 fixed a priori; embedding-block L2 by inner stratified 5-fold CV on the training fold only (grid 10^-1..10^4); logistic fit sentinel.predict._logit_fit.

| label | n (pos) | a | b | c | c - a (split variability) | c - a: corrected 95% CI, p | stratified permutation p |
|---|---|---|---|---|---|---|---|
| sbp120 | 219 (139) | 0.702 [0.686, 0.718] | 0.701 [0.668, 0.728] | 0.749 [0.720, 0.780] | 0.047 [0.019, 0.074] | +0.047 [-0.010, +0.104], p = 0.108 | 0.010 (null mean -0.007, max +0.009) |
| stage12_vs_normal | 134 (54) | 0.767 [0.749, 0.787] | 0.727 [0.671, 0.774] | 0.812 [0.790, 0.845] | 0.045 [0.012, 0.072] | +0.045 [-0.015, +0.106], p = 0.142 | 0.010 (null mean -0.006, max +0.039) |
| sbp130_dbp80 | 219 (100) | 0.686 [0.675, 0.693] | 0.715 [0.670, 0.754] | 0.760 [0.727, 0.784] | 0.073 [0.043, 0.102] | +0.073 [+0.018, +0.128], p = 0.009 | not run |

Reading: the permutation test asks whether the embeddings carry information beyond age and sex in THIS sample; the corrected CI asks how precisely the gain would carry to a new sample. Where the corrected CI includes 0 the gain is **suggestive**, not established. sbp130_dbp80 is EXPLORATORY (added after the audit, not pre-specified). stage12_vs_normal excludes the middle band, so its AUROCs are inflated by spectrum bias.

## 3. Gain by age band (sbp120; post hoc, descriptive, SMALL SAMPLES)

AUROC of the repeat-mean out-of-fold logit within each band (fold heads differ in scale; no CI).

| age band | n (pos) | age only | a | b | c |
|---|---|---|---|---|---|
| <50 | 56 (23) | 0.794 | 0.816 | 0.623 | 0.748 |
| 50-64 | 91 (58) | 0.551 | 0.549 | 0.729 | 0.738 |
| >=65 | 72 (58) | 0.549 | 0.464 | 0.612 | 0.585 |
| 30-65 (target ages) | 128 (80) | 0.569 | 0.605 | 0.668 | 0.725 |

## 4. Noise decomposition of the clip-level head score

Model b, label sbp120; out-of-fold logits of each held-out subject's 3 single clips, computed within each outer fold and averaged over folds; mean over repeats [split variability]. **What this measures:** between-person spread and clip-to-clip noise of clips taken seconds apart (each 2.1-s clip is zero-padded to 10 s). **What it does not measure:** night-to-night variability, and how the score moves when one person's BP changes. The slope is a between-person, cross-sectional slope (it partly reflects structural vascular ageing); the raw slope contains age and is never used.

| quantity | fold-tuned heads (scales differ, L2 31..10^4) | final head's scale (fixed L2) |
|---|---|---|
| between_sd | 0.743 [0.580, 0.940] | 0.552 [0.519, 0.579] |
| within_sd | 0.747 [0.544, 1.030] | 0.522 [0.502, 0.548] |
| icc | 0.496 [0.441, 0.532] | 0.522 [0.501, 0.542] |
| slope_per_mmHg | 0.013 [0.009, 0.016] | 0.010 [0.009, 0.011] |
| slope_per_mmHg_age_adj | 0.006 [0.004, 0.008] | 0.005 [0.004, 0.006] |
| slope_per_mmHg_in_within_sd | 0.019 [0.015, 0.022] | 0.020 [0.018, 0.023] |
| slope_per_mmHg_age_adj_in_within_sd | 0.009 [0.007, 0.012] | 0.010 [0.008, 0.013] |

Scale-free simulator inputs (final head's scale): clip-level ICC 0.522; age-adjusted between-person slope 0.0099 within-clip SD per mmHg. between-person and clip-to-clip quantities only: the within-person coupling and night-to-night noise used in the simulator are ASSUMPTIONS.

Final head (results/ppg_bp/head.npz): model b, label sbp120, all 219 subjects, L2 = 1000 (5-fold CV on all subjects). Domain: PPG-BP: transmissive fingertip PPG at rest (seated, hospital cohort in China), 2.1-s clips; NOT validated on wrist reflectance PPG at night.

Runtime 1099 s. Command: `.venv/Scripts/python.exe -m sentinel.pulse` (embeddings cached in data/ppg_bp/embeddings.npz).

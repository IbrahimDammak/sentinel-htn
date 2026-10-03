# PULSE Step 1 audit: clinical and biostatistical review

**Reviewer role:** consultant cardiologist and hypertension specialist (ESC/ESH), with clinical-research and biostatistics training.
**Date:** 2026-10-03.
**Scope (Step 1 only):** `sentinel/pulse.py` lines 1–316 and 397–end (unchanged since the snapshot), and `results/ppg_bp/{summary.md, metrics.json, head.npz}` (md5 unchanged during the audit).
**Not audited:** the nightly-channel code appended to `pulse.py` (lines 317–396) and the concurrent Step-2 edits to `data.py`, `detect.py`, `__init__.py`, `evaluate.py`, `learn.py`, `warn.py`, `run.py` and the tests. `evaluate.auroc` and `predict._logit_fit` are unchanged.
**How it was checked:** every number below was re-run on a snapshot of `sentinel/` from the scratch scripts `scratchpad/audit/a1…a7*.py`. Nothing in the repository was modified except this file.

## Verdict

The engineering is sound, and the headline numbers reproduce exactly:
- The embedding recipe matches the PaPaGei authors' recipe bit for bit.
- Cross-validation is at subject level, with no leakage.
- The 20-repeat CV and the noise decomposition reproduce to every digit.
- An independent sklearn implementation on different splits agrees.

The coder also deserves credit for reporting that age alone reaches the published PaPaGei-S benchmark (0.77). The authors' own appendix says the same thing (Table 15: age+sex 0.77, PaPaGei-S 0.77).

**What I accept clinically.** The data support a modest, cross-sectional, between-person association: pulse-shape embeddings add about 0.05 AUROC over age, sex and BMI.
- Shuffling the embeddings within age×sex strata destroys this gain (permutation p = 0.01).
- It survives adjustment for HR, non-linear age and comorbidity.

**What I do not accept yet:**
- **The uncertainty is mislabelled.** The quoted interval [0.019, 0.074] shows split-to-split variability only. A resampling-corrected 95% CI is about [−0.01, +0.10] (p ≈ 0.11).
- **The primary label is not hypertension.** It is SBP ≥ 120 on a single reading.
- **Nothing here measures within-person behaviour.** Step 1 says nothing about how the score moves when one person's BP rises, or about night-to-night noise. Using the cross-sectional slope and the seconds-apart clip SD as Step-2 simulator couplings would make any pulse-channel benefit circular.

**Overall:** fit for purpose as a cross-sectional feasibility and credibility check; not yet fit as evidence for within-person tracking. There are 3 MUST-FIX items, all about wording and design rather than code bugs.

## Findings

### MUST-FIX

**M1. The headline uncertainty is split variability, not a confidence interval.**

`summary.md` table, `metrics.json` `diff_c_minus_a`: "+0.047 [0.019, 0.074], share(c−a>0) 1.00". The summary's own footnote says this is "not a sampling CI". But the Step-1 report, and anything copied from it, will read it as one. Repeats reuse the same 219 people, so 20/20 agreement is expected even with no true effect. Re-analysis of the coder's exact folds:

| contrast | mean | Nadeau–Bengio corrected 95% CI, p | subject bootstrap of pooled OOF scores (scores held fixed, so optimistic) | permutation within age-decile×sex strata (100 perms) |
|---|---|---|---|---|
| primary, c − a | +0.047 | [−0.010, +0.104], p = 0.11 | [−0.004, +0.099] | p = 0.010 (null mean −0.007, max +0.009) |
| strict, c − a | +0.045 | [−0.015, +0.106], p = 0.14 | [−0.019, +0.113] | p = 0.010 (null max +0.039) |

The two tests answer different questions:
- The permutation test asks whether the association is real in this sample. It is: the gain is not an artefact of the extra tuned block (shuffled or Gaussian embeddings give −0.014 to +0.013).
- The corrected test asks how precisely the gain would carry to a new sample. Not precisely: the CI includes 0.

**Fix:**
- Report the gain with the corrected CI and the stratified-permutation p.
- Rename "[2.5–97.5 pct over repeats]" to "split variability". Never write "20/20" or "1.00" next to the increment.
- Reference: Nadeau & Bengio, *Mach Learn* 2003;52:239–281 ([link](https://link.springer.com/article/10.1023/A:1024068626366)). Code: `nb_corrected` in `scratchpad/audit/common.py`.

**M2. The "primary" label is SBP ≥ 120 on one reading, not hypertension.**

Evidence from `a6_labels.py` and the crosstab in this audit:
- **SBP alone defines the class.** PPG-BP's `Hypertension` class equals JNC7 SBP bands in 219/219 people. Under the JNC7 SBP/DBP "or" rule, 4 people would change class.
- **Primary positive means "elevated or hypertension".** Primary == (SBP ≥ 120) is True for every subject. In ESC 2024 terms this is "elevated BP or hypertension", not hypertension ([ESC 2024](https://academic.oup.com/eurheartj/article/45/38/3912/7741010): non-elevated <120/70, elevated 120–139/70–89, hypertension ≥140/90 office).
- **The "Normal" class mixes categories.** 19 of the 80 "Normal" people have DBP 70–82, which ESC 2024 calls elevated.
- **Many "prehypertension" cases are stage 1 hypertension.** 43 of the 85 meet ACC/AHA 2025 stage 1 (≥130/80; [Jones 2025](https://www.ahajournals.org/doi/10.1161/HYP.0000000000000249)).
- **BP was measured once.** It was a single Omron HEM-7201 upper-arm reading taken alongside the PPG ([Liang 2018](https://pmc.ncbi.nlm.nih.gov/articles/PMC5827692/)). 50/219 people (23%) are within ±5 mmHg of the 120 cut-off, so label noise is large.
- **Treatment status is unknown.** Antihypertensive treatment is not recorded, and the cohort is from a hospital. A treated hypertensive with controlled BP is labelled "Normal" but has a hypertensive vascular phenotype.

**Fix:**
- Name the labels by threshold everywhere: summary title, `head.npz` `label`, paper. Use "SBP ≥ 120 vs < 120 (single seated reading)" and "SBP ≥ 140 vs < 120, 120–139 excluded".
- Add the label that matches the team's own reference, ≥130/80 computed from the raw SBP/DBP. I ran it exploratorily (`a6_labels.py`, coder's CV): demographics 0.686, embeddings 0.715, both 0.760, c − a +0.073, NB-corrected CI [+0.018, +0.128], p = 0.009. Pre-specify it before quoting it.
- Also report continuous outcomes. Ridge CV R² for SBP was 0.197 with demographics and 0.278 with demographics + embeddings. For DBP it was 0.027 and 0.084.

**M3. Step 1 measures nothing within a person, so the Step-2 couplings must be assumptions, not "taken from this experiment".**

These outputs (`noise()`, lines 170–189) are all between-person or clip-to-clip:
- **The slope is between-person.** The 0.006 logit/mmHg slope is an age-adjusted, cross-sectional regression across people. Between-person PPG differences with BP largely reflect structural arterial stiffness and vascular ageing, which change over years, not 26 weeks ([Charlton 2022, AJP-Heart 322:H493](https://doi.org/10.1152/ajpheart.00392.2021)).
- **The head score mostly tracks age.** Its out-of-fold correlation is r = 0.49 with age and 0.33 with SBP (`a3_stats.py`).
- **The clip SD is not night-to-night variability.** The "within-person SD 0.747" compares 2.1-s fingertip clips taken seconds apart. Each clip is about 263 samples zero-padded to 1250 (79% zeros). That says nothing about night-to-night variability on a wrist.
- **Cuffless methods track within-person change poorly.** The 2025 AHA statement reports poor tracking of within-person BP change and recommends against using cuffless devices for diagnosis or management ([Cohen, *Hypertension* 83(3):e00254](https://pmc.ncbi.nlm.nih.gov/articles/PMC13335599/); [Mukkamala 2025, *Hypertension* 82:957](https://www.ahajournals.org/doi/10.1161/HYPERTENSIONAHA.125.24822)).

**Fix:** see the Step-2 guidance below. In short:
- State β_within as an assumption and run a grid that includes 0.
- Do not derive nightly noise as clip SD/√n.
- Show that the pipeline at β = 0 neither gains AUROC or lead time nor raises the alarm rate.

### SHOULD-FIX

**S1. Absolute noise numbers mix heads on different scales.**

The fold L2 penalties range from 31 to 10⁴ (`metrics.json` `l2_chosen`). On the final head's scale (L2 = 1000, out-of-fold, `a7`) the values are:
- between SD 0.55, within SD 0.52, ICC 0.52;
- slope 0.010 logit/mmHg, or 0.0048 age-adjusted.

The reported values are 0.743 / 0.747 / 0.496 and 0.013 / 0.006. **Fix:** feed the simulator scale-free quantities: ICC ≈ 0.50, and an age-adjusted slope of ≈ 0.009–0.010 within-clip SD per mmHg. Alternatively, recompute at L2 = 1000.

**S2. The strict label is an extreme-groups design.**

Excluding the 120–139 band inflates AUROC (spectrum bias), so 0.81 is not a screening-population figure. **Fix:** say so next to the number.

**S3. Report the robustness checks I ran; they help the team.**

| comparator | c − a gain (coder's CV) |
|---|---|
| demographics + HR | +0.051 |
| + age², age×sex | +0.059 |
| + diabetes, cerebral infarction, cerebrovascular disease | +0.044 |
| same contrasts, strict label | +0.050, +0.065, +0.051 |
| independent sklearn re-implementation, different splits | +0.043 (primary), +0.062 (strict) |

Notes on these checks:
- Adding HR or comorbidities did not improve the demographic model.
- **Age strata (post hoc, descriptive):**
  - Ages 30–65 (n = 128), the team's target: a 0.60 → c 0.70.
  - Ages 50–64, where age carries no information: embeddings alone 0.72 vs demographics 0.54.
  - Ages < 50 (n = 56): adding embeddings lowered AUROC (0.82 → 0.75).

  The gain is heterogeneous and small-sample.

**S4. `head.npz` metadata overstates portability.**

Lines 260–261 store `score='logit; apply to single-clip PaPaGei-S embeddings'`. The head comes from:
- transmissive fingertip PPG (660/905 nm, SEP9AF-2), seated, in a Chinese hospital cohort;
- 2.1-s clips selected by skewness-SQI;
- the label SBP ≥ 120.

Wrist reflectance PPG at night differs in site, wavelength, contact pressure and posture. **Fix:** store the domain and label in the file and in the docstring, and state that it is not validated on wrist PPG.

**S5. Frame the reproduction with the authors' own table.**

PaPaGei, ICLR 2025, Appendix E, Table 15, p. 28 ([arXiv 2410.20542](https://arxiv.org/abs/2410.20542)), hypertension row: Demo (age, sex) 0.77 [0.65–0.88]; PaPaGei-S 0.77 [0.68–0.87]; PaPaGei-S + Demo 0.80 [0.70–0.89]. I checked the column mapping from the PDF word coordinates.

The coder's "age alone 0.774" therefore reproduces the authors' own demographic baseline, which validates the split, the test set (test + val, 82 people) and the probe.

The 0.694 vs 0.77 gap for the embeddings is not significant (each CI contains the other estimate). It is plausibly the instability of choosing C by 4-fold accuracy on 123 people: the per-C AUROC ranges from 0.655 to 0.731. GPU vs CPU numerics may also play a part. **Fix:** write "consistent with the authors' Table 15", and do not present it as a discovery against them.

**S6. Confounders that cannot be removed here should be stated.**

- The cohort is a hospital population: 20 cerebral infarction, 25 cerebrovascular disease, 38 diabetes.
- Treatment status is unknown.
- The embeddings may encode a vascular-disease or "history of hypertension" phenotype rather than current BP. Chronological-age adjustment does not remove vascular age.

### NOTE (verified correct)

- **N1. Embedding recipe.** An independent re-implementation from the authors' notebook cell 9 (z-score → pyPPG Chebyshev 0.5–12 Hz → resample_poly 1/8 → centre-pad to 1250) matches the cache exactly on 24 clips (max |Δ| = 0.0). pyPPG is 1.0.41, as pinned by the authors. Weights load strictly; output index 0. Self-check passes in 4.9 s.
- **N2. CV hygiene.** Rows are subjects, and the 3 clip embeddings are averaged before splitting, so no clip leakage is possible. Standardisation (`fit_head`, line 122) and L2 tuning (`tune_l2`, lines 134–145) use training rows only, with distinct inner seeds. Label mapping is correct: 80/139 primary and 80/54 strict, with 85 excluded.
- **N3. Mean-of-fold vs pooled AUROC.** Pooled out-of-fold AUROC is about 0.005 lower for every model, and c − a is identical (+0.047). The choice is immaterial; keep mean-of-folds and state it.
- **N4. ICC.** The one-way random-effects estimator is correct for balanced k = 3, and the self-check recovers simulated components. The value is single-clip ICC; a 3-clip mean has reliability ≈ 0.75 (Spearman–Brown).
- **N5. Slopes.** These are OLS of the person-mean out-of-fold score on SBP, and on SBP + age. A pooled check gives 0.006, or 0.008 when also adjusting for HR, BMI and sex. A single cuff reading attenuates the slope slightly (regression dilution).
- **N6. Reproduction code.** `reproduce()` faithfully copies the authors' probe: GridSearchCV(cv = 4, accuracy), the same grid with failing l1+lbfgs fits, and 500 bootstraps. Convergence warnings are suppressed; this does not affect conclusions.

## Reproduced vs reported numbers

| quantity | reported | reproduced by the auditor |
|---|---|---|
| self-check | OK, ~5 s | OK, 4.9 s |
| PaPaGei-S, authors' split + probe | 0.694 [0.549–0.808] | 0.694 [0.549, 0.808] |
| demographics, same probe | 0.794 | 0.794 [0.685, 0.887] |
| age alone, same probe | 0.774 | 0.774 [0.665, 0.869] (raw-age rank AUROC also 0.774) |
| published PaPaGei-S / Demo | 0.77 [0.68–0.87] | 0.77 [0.68–0.87] / 0.77 [0.65–0.88] (paper Table 15) |
| CV primary: a / b / c | .702 / .701 / .749 | identical (per-repeat max abs diff 0.0) |
| CV primary: c − a | +0.047 [0.019, 0.074] | +0.047; corrected CI [−0.010, +0.104], p = 0.11; permutation p = 0.01 |
| CV strict: a / b / c | .767 / .727 / .812 | identical |
| CV strict: c − a | +0.045 [0.012, 0.072] | +0.045; corrected CI [−0.015, +0.106], p = 0.14; permutation p = 0.01 |
| independent sklearn CV (other splits): primary / strict | — | a .701/.762, b .704/.734, c .744/.824 |
| between SD / within SD / ICC | 0.743 / 0.747 / 0.496 | identical; at final-head L2 = 1000: 0.55 / 0.52 / 0.52 |
| slope, raw / age-adjusted (logit/mmHg) | 0.013 / 0.006 | identical; at L2 = 1000: 0.010 / 0.0048 |
| final head L2 | 1000 | 1000 |

## Claim wording

**Permitted in the paper (1–3 sentences):**

> "In PPG-BP (219 hospital participants in China; one seated upper-arm cuff reading and three 2.1-s fingertip PPG clips each; treatment status unrecorded), embeddings from a frozen PPG foundation model (PaPaGei-S) alone discriminated SBP ≥ 120 from < 120 mmHg no better than age, sex and BMI (cross-validated AUROC 0.70 vs 0.70). The published benchmark for this task (0.77) is matched by age alone on the authors' split. Added to age, sex and BMI, the embeddings raised AUROC from 0.70 to 0.75 (+0.05; resampling-corrected 95% CI −0.01 to +0.10; within age-and-sex-stratum permutation p = 0.01). This suggests that pulse shape carries some between-person information about BP level beyond these demographics; tracking of BP change within a person was not tested."

**Forbidden:**
- "PPG shape / the pulse channel detects or predicts hypertension." The label is SBP ≥ 120, and the association is cross-sectional.
- "Validated on real data" for the pulse channels or for SENTINEL's discrimination.
- "+0.047 [0.019, 0.074]" presented as a CI, "significant in 20/20 repeats", or any p-value derived from the repeats.
- "Within-person coupling of 0.006 logit/mmHg measured", or "night-to-night noise / ICC measured on real data".
- Any mmHg estimate or BP value from the head.
- "PaPaGei's result does not reproduce." It is within CI and consistent with the authors' Table 15.
- Generalisation to wrist PPG, nocturnal recordings, untreated community adults or Tunisian wearers.

## Step-2 guidance (simulator coupling and evaluation)

1. **Direction and size of within-person coupling.**
   - **Direction:** physiology predicts a positive sign. Higher pressure stiffens the artery, the reflected wave arrives earlier and the dicrotic notch and diastolic peak are blunted. So rising BP should push the head score up.
   - **Size:** small and person-specific. It is confounded by HR, vasomotor tone (skin temperature, sleep stage), posture and strap contact pressure.
   - **Upper bound:** the between-person slope includes structural vascular ageing, which does not change in 26 weeks, so it is an upper bound for within-person coupling. The defensible range is β_within ∈ {0, 0.5, 1} × the age-adjusted between-person slope (≈ 0.010 within-clip SD per mmHg), with β = 0 as the null. Never use the raw slope (0.013), because it contains age.
2. **Noise.**
   - Do not set nightly noise to clip SD/√(clips per night). That ignores night-to-night physiological variation and would make the channel look far more informative than it is.
   - Assume the night-to-night SD of the nightly median is at least the between-person SD (ICC across nights ≤ 0.5). Add AR(1) autocorrelation, as was done for LifeSnaps, plus occasional step changes (strap repositioning, firmware), and run a sensitivity grid.
3. **The drift channel (`pulse_drift`) has no empirical BP coupling at all.**
   - It is label-free and unsigned, so it fires on any change.
   - Count it in the alarm budget, and test it against simulated non-BP shifts (repositioning, season, weight change). Persistence and context should absorb these.
   - Its PCA basis comes from fingertip PPG-BP clips.
4. **Mandatory analyses.** Run:
   - full vs full minus pulse channels;
   - full with pulse at β = 0, which must not improve AUROC or Se30 and must not raise alarms per non-converter person-year;
   - the β grid, reported as a curve.

   Any reported gain must be labelled "conditional on an assumed coupling".
5. **What Step 2 may claim.** "The pipeline can ingest two real-model-derived pulse channels. Its alarm budget holds when they carry no signal, and it benefits only if the within-person coupling is at least X." It must not claim earlier detection from PPG morphology.
6. **Data that could replace assumptions later:**
   - **Aurora-BP** (Mieloszyk et al., *IEEE JBHI* 2022;26:2864): wrist PPG with ambulatory cuff readings, giving within-day, within-person change; access by request ([repo](https://github.com/microsoft/aurorabp-sample-data)).
   - The organisers' longitudinal data.

## RQ1–RQ6 scorecard (effect of Step-1 evidence on the team's score)

| RQ | effect | why / what to do |
|---|---|---|
| RQ1 personal baseline | slight + | Between-person score variance is about equal to clip noise (ICC ≈ 0.5), so population thresholds on a PPG score would be poor. This supports per-person baselining. Say no more than that. |
| RQ2 persistent change | neutral (risk if misused) | No within-person data. Simulated pulse drift must not be presented as evidence of detecting persistent change. |
| RQ3 early detection / lead time | **risk** | If Se30 or lead time improves only through pulse channels with assumed β, judges will see circularity. Report the β = 0 and β-grid results, and keep the paper's existing "about a month over chance" claim unchanged. |
| RQ4 context | neutral / slight risk | The head score tracks age (r = 0.49) and sex (−0.19). Wrist PPG morphology is strongly context-dependent (temperature, posture, contact pressure, HR). Pulse channels need the same context regression and masking as the other channels. |
| RQ5 reliability (noisy / missing) | slight + | This is a real-data component check: exact reproduction, permutation controls, an honest null against demographics. Clip-level ICC is a lower-level reliability number; do not stretch it to nights. |
| RQ6 uncertainty and abstention | + if M1 fixed, − if not | Reporting corrected CIs and stating "suggestive, CI includes 0" is exactly the credibility judges reward. Presenting split variability as a CI would cost points. |

**Net:** Step 1 is a credibility asset under the judges' criterion (the most credible scientific approach), provided M1–M3 are applied. It is not an accuracy asset.

## Sources (verified 2026-10-03)

- **PaPaGei.** Pillai A, Spathis D, Kawsar F, Malekzadeh M. ICLR 2025. Table 4 and Appendix E Table 15. https://arxiv.org/abs/2410.20542
- **PPG-BP.** Liang Y, Chen Z, Liu G, Elgendi M. *Sci Data* 2018;5:180020. https://pmc.ncbi.nlm.nih.gov/articles/PMC5827692/
- **ESC 2024 guidelines.** McEvoy JW et al. *Eur Heart J* 2024;45:3912–4018. https://academic.oup.com/eurheartj/article/45/38/3912/7741010
- **AHA/ACC 2025 guideline.** Jones DW et al. https://www.ahajournals.org/doi/10.1161/HYP.0000000000000249
- **AHA cuffless-device statement.** Cohen JB et al. *Hypertension* 83(3):e00254. https://pmc.ncbi.nlm.nih.gov/articles/PMC13335599/
- **Cuffless BP review.** Mukkamala R et al. *Hypertension* 2025;82(6):957–970. https://www.ahajournals.org/doi/10.1161/HYPERTENSIONAHA.125.24822
- **ESH cuffless validation.** Stergiou GS et al. *J Hypertens* 2023;41:2074–2087 (already `stergiou2023` in the paper).
- **Limits of PPG-based BP.** Mehta S et al. *Sci Rep* 2024;14:18318. https://www.nature.com/articles/s41598-024-68862-1
- **PPG-BP benchmark.** González S et al. *Sci Data* 2023;10:149. https://pmc.ncbi.nlm.nih.gov/articles/PMC10030661/
- **PPG and vascular age.** Charlton PH et al. *AJP-Heart* 2022;322:H493–H522. https://doi.org/10.1152/ajpheart.00392.2021
- **Aurora-BP.** Mieloszyk R et al. *IEEE JBHI* 2022;26(7):2864–2875. https://github.com/microsoft/aurorabp-sample-data
- **Corrected resampled t-test.** Nadeau C, Bengio Y. *Mach Learn* 2003;52:239–281. https://link.springer.com/article/10.1023/A:1024068626366

Audit scripts (scratch, not in the repo): `a1_embed_repro.py`, `a2_cv.py`, `a3_stats.py`, `a4_perm_noise.py`, `a5_sklearn_cv.py`, `a6_labels.py`, `a7_fixed_l2_noise.py`, and `common.py`, which imports a snapshot of `sentinel/` with the repo's data paths.

---

# Steps 2–3 audit: pulse channels in the pipeline, the simulator and new metrics

**Scope:**
- Step-2 code: `sentinel/__init__.py` (`channels`), the `learn.py` / `detect.py` / `warn.py` diffs, the `data.py` pulse simulator, the `pulse.py` nightly section (lines 317–396), and the `run.py` additions.
- Step-3 code: `sentinel/evaluate.py`.
- Results: `results/pulse/*` and `results/pulse_lifesnaps/*`.

**Snapshot:** the code was snapshotted at the start of this audit (`scratchpad/audit/snap2`, md5 in `hashes_s2.txt`). That snapshot produced `results/pulse` (02:30–02:33).

**Changed under me:** afterwards `data.py` and `pulse.py` changed. The changes are the coder's M1–M3 fixes: a scale-free simulator (`_PULSE_ICC` 0.52, `PULSE_COUPLING` 0.0092 "UPPER bound", a `pulse_coupling=` argument) and renamed labels. I did not chase them; they are to be verified at the end, as agreed.

**Scripts:** `b1_rng_isolation.py`, `b2_invariant_spec.py`, `b3_drift_real_vs_sim.py`, `b4_burden.py`.

## Verdict (Steps 2–3)

**The plumbing is correct and the claimed invariants hold:**
- The core simulator columns are identical to HEAD.
- `no_pulse` reproduces `results/weighted`, and the LifeSnaps output is byte-identical.
- All-NaN pulse columns give exactly the no-pulse decisions.
- The nightly maths is causal.

**What the pulse channels actually did.** Even at the upper-bound coupling, they did not help. AUROC fell by 0.007, and the share of converters warned before t_ref fell from 0.48 to 0.42. The lower alarm rate and higher "specificity" come from a different operating point, not from better separation. Reporting only those two numbers would mislead.

**Two simulator problems:**
- `pulse_drift` is a near-zero-signal, non-directional and non-personalised channel. It still gets 13–14% of the weight.
- The simulator's drift is not what the code computes.

**What the Step-3 metrics show.** They are correctly implemented and expose an important clinical fact: over about 16 months, 34% of non-converters get at least one false prompt, and a prompt raises the odds of conversion only about 1.4-fold (LR+ 1.4). That is honest and worth reporting, but in time-explicit units and never beside Apple's 92.3%.

**Overall:** 2 MUST-FIX, both about framing.

## Findings (Steps 2–3)

### MUST-FIX

**M4. The pulse vs no-pulse comparison reports only the metrics that moved favourably; the "gain" is an operating-point shift that costs sensitivity.**

Evidence: `results/pulse/seed*/metrics.json`, `main` vs `ablations.no_pulse`, reproduced to ≤1e-14 by `b2`.

| metric | pulse | no pulse |
|---|---|---|
| AUROC | 0.614 | 0.621 |
| warned before t_ref (Se0) | 0.424 | 0.481 (lower with pulse in all 3 seeds) |
| Se30 | 0.281 | 0.322 |
| per-week sensitivity at 92% per-week specificity | 0.172 | 0.191 |
| alarms per non-converter person-year | 0.354 | 0.405 |
| person-level specificity | 0.699 | 0.658 |

The two arms use separately tuned thresholds (seed 0: persistence threshold 0.10 vs 0.15), so they sit at different points of the curve.

`summary.md`'s "Pulse effect" table hides this. `KEY` lacks `sens_lead_0/30`, and the table shows `sens_lead_90` +0.016, which reads as a gain.

**Fix:**
- Compare arms at a matched realised alarm rate: put `no_pulse`, and every coupling arm of the sweep, into the `operating_curve` fits.
- Add `sens_lead_0` and `sens_lead_30` to `KEY`.
- State the result in words: "no improvement".

**M5. "Person-level specificity 0.66–0.70" and `sens_spec92` invite a false comparison with Apple's 92.3%.**

- **The metric is cumulative.** `evaluate.metrics` counts a non-converter as a false positive if ever warned over the whole follow-up. Median monitoring is 497 days (`b4`).
- **The same data in time-explicit units (default no-pulse system, 3 seeds):**
  - cumulative incidence of a first false prompt: 10% at 6 months, 23% at 12 months, 34% by the end;
  - 1.76 prompts per falsely prompted person;
  - person-level sensitivity 0.48 against a false-positive share of 0.34, so LR+ 1.4 and LR− 0.79;
  - person-level PPV 0.22 at the test-set conversion rate of 17%.
- **`sens_spec92` is a different kind of number.** It is per landmark week, it uses `p` rather than `p_lo`, and it ignores the persistence gate, so it is not the system's operating point.
- **Apple's figure measures something else.** Apple's 41.2% / 92.3% is a per-person classification of *prevalent, undiagnosed* hypertension over one 30-day window (validation n = 2,229, twice-daily home BP reference; [Apple 2025](https://www.apple.com/health/pdf/Hypertension_Notifications_Validation_Paper_September_2025.pdf)).
- **The closest same-unit figure is still not comparable.** Per 4-week window, 3.0% of non-converter windows contain a new prompt (4.1% contain any WARNING week). That is still a different task (incident vs prevalent) on a simulated population.

**Fix:**
- Rename `specificity` to "non-converters never prompted during follow-up (median 16 months)" and report it with:
  - the cumulative-incidence curve;
  - prompts per person;
  - LR+;
  - PPV together with the prevalence it depends on.
- Rename `sens_spec92` to "per-week sensitivity at 92% per-week specificity".
- Never place either number next to Apple's. If Apple is cited, cite it as a different task.

### SHOULD-FIX

**S7. `pulse_drift` should not enter the risk score as specified.**

- **No evidence base.** `EVIDENCE['pulse_drift'] = 0.5` (`__init__.py`), but no literature, and not PPG-BP either, links a label-free embedding distance to BP. The file's own rule is that EVIDENCE is a literature prior.
- **Reliability weighting rewards it anyway.** It gets 13–14% of total weight, more than `pulse_htn` (9%; `summary.md` weights). Yet in the simulator it carries almost no BP signal: a 17 mmHg rise shifts one of 8 unit axes by about 0.14 SD, which raises the expected distance by about 0.003 against a nightly SD of about 0.69.
- **It is non-directional but scored as risk.** A BP fall (new treatment, weight loss), strap repositioning or season all raise it, yet `RISK_SIGN` is +1. The evidence ledger then shows it as risk evidence.
- **It is not personalised.** Its own warm-up (the first 28 nights with clips) consumes the pipeline's warm-up window. In 83% of simulated people the personal baseline sees zero drift values (`b3`), so its z-score uses the population prior.

**Fix:** set its weight in `dev` to 0 and keep it as a ledger flag, "pulse shape changed, direction unknown", or as a re-baseline/quality trigger. If it is kept in the score, give it a second warm-up after its reference.

**S8. The simulator's drift is not what `night_drift` computes.**

`data._pulse` draws the distance from true unit-variance, stationary AR(1) axes, with no estimated mean or covariance. I ran the real `night_drift` on equivalent stationary 8-dim input (`b3`):

| | real `night_drift` | simulator |
|---|---|---|
| mean distance | 2.98 | 2.74 |
| between-person SD of person means | 0.17 | 0.04 (4× smaller) |

The person-specific offsets are persistent, and S7's missing personal baseline will not remove them. A slow embedding wander (random walk 0.02 SD per night per axis) also raises everyone's mean distance from 2.99 to 3.13 within a year.

**Fix:**
- Simulate low-dim embeddings and pass them through `night_drift` itself.
- Add a non-stationary null: slow wander, plus step changes at strap and firmware events.
- Reset the drift reference at firmware changes, and build it only from quality-gated, non-acute nights. Today the real reference can include alcohol and illness nights.

**S9. The simulator omits the main non-BP drivers of PPG morphology, so pulse looks cleaner and more independent than it is.**

- **Heart rate.** PaPaGei-S embeddings predict average HR to an MAE of 3.47 bpm (paper Table 15, verified). Yet simulated pulse noise is independent of `night_rhr` noise, so pulse counts as independent evidence when part of it would double-count heart rate.
- **Vasomotor tone, contact pressure, posture and sleep stage.** None of these affect the simulated pulse (`data.py`: "no acute-context or skin-tone effects"). As a result, blanking pulse on acute nights, about 35% of nights here, can only lose information in the simulation, even though in reality it removes real confounding. The simulation cannot show that the masking helps.
- **Missingness.** Clips go missing at 10% MCAR, independent of SQI and skin tone. Morphology-grade clips are more SQI- and skin-tone-sensitive than HR, so the skin-tone abstention gap would widen.

**Fix:**
- Correlate pulse noise with `night_rhr` and temperature.
- Make clip availability depend on SQI and ITA, or list these as optimistic omissions in CONTRACT.md.

**S10. The TP definition and exposure windows need stating.**

- **Pre-onset warnings count as hits.** A TP is any warning before t_ref, including one before the simulated onset: 1–2 of about 20 TPs per seed without pulse, and 6 of 21 with pulse in seed 0. In simulation, report "first warning before onset" as a sanity column.
- **The two groups are watched for different lengths of time.** Converters are followed until t_ref, non-converters for 540 days. Show first-warning cumulative incidence for both groups on a common time axis.
- **The alarm denominator includes warm-up.** `alarms_per_nonconv_py` divides by calendar time (`end_day+1`), although no warning is possible during warm-up. Per monitored year the rate is about 0.44 rather than 0.41 (pre-existing). State the denominator.

**S11. Read the age-tercile table as model behaviour, not physiology.**

In the simulator age has no causal role: `_person` draws it last and independently, and corr(age, converter) on test is −0.05. Yet alarm rates rise across age terciles (0.21 / 0.37 / 0.49 in the pulse run). The fitted age coefficient is +0.04 to +0.10 per SD in all three seeds, and the threshold amplifies it.

**Fix:** label the table "model behaviour". In real data age legitimately raises pre-test probability, so older wearers will get more prompts; that should be disclosed.

### NOTE (verified correct)

- **N7. RNG isolation.** `daily` (core columns) and `people` from the current simulator equal those from HEAD 8471b58 for seeds 0–2 (n = 1200, 540 days): `DataFrame.equals` is True (`b1`).
- **N8. Invariants.**
  - The `no_pulse` main metrics reproduce `results/weighted` main, and pulse main reproduces `results/pulse` main, on every key. Differences are ≤1.4e-15 relative (float summation under single-threaded BLAS); the coder's stored files compare exactly.
  - `results/pulse_lifesnaps/real_world.{json,md}` are byte-identical to `lifesnaps_weighted` (`cmp`).
- **N9. Plumbing.**
  - `channels()` is used consistently in quality gate, context, prior, baseline, weights, weekly and perturb.
  - A NaN variance gives weight 0, and an unknown channel weighs 0 in `weekly`.
  - The all-NaN-equals-dropped property is asserted in `tests/test_pipeline.py`.
  - `drop_pulse` at test time degrades gracefully (AUROC 0.621).
- **N10. Nightly maths.**
  - `night_htn` is the median of clip logits.
  - `night_drift` takes its reference from the first 28 nights with clips. Editing later nights leaves earlier outputs unchanged (`b3`).
  - Ledoit–Wolf matches sklearn. `python -m sentinel.pulse --selfcheck` reports OK, including the nightly check (7.5 s).
- **N11. Acute-night blanking.** Blanking pulse on acute nights is physiologically appropriate: alcohol vasodilation, late vigorous exercise and febrile illness all alter nocturnal vascular tone and HR. It is consistent with the core night channels.
- **N12. Step-3 metrics.** They match their docstrings, and the hand-computed self-check passes (`python -m sentinel.evaluate`). `sens_at_spec` takes its threshold from calibration y=0 weeks only (0.92 'higher' quantile); the specificity reached on test was 0.919–0.942.

## Reproduced vs reported numbers (Steps 2–3; snapshot code, 3 seeds)

| quantity | coder's report | auditor |
|---|---|---|
| RNG isolation | bit-identical | identical to HEAD, seeds 0–2 |
| `no_pulse` = `results/weighted` main | all keys identical | identical to ≤1.4e-15 |
| LifeSnaps output | byte-identical | byte-identical |
| AUROC, pulse vs no pulse | 0.614 ± 0.024 vs 0.621 ± 0.014 | same |
| alarms / non-converter person-year | 0.354 vs 0.405 | same (0.430/0.305/0.328 vs 0.446/0.378/0.392) |
| person-level specificity | 0.699 vs 0.658 | same |
| Se0, pulse vs no pulse | not reported | 0.424 vs 0.481 |
| Se30, pulse vs no pulse | not reported | 0.281 vs 0.322 |
| `sens_spec92`; test specificity reached | 0.172; 0.931 | 0.172 (no pulse 0.191); 0.919–0.942 |
| non-converters with ≥1 false prompt | 30–35% over ~1.5 y | 34% over a median 497 monitored days; 10% at 6 mo, 23% at 12 mo |
| prompts per falsely prompted person | — | 1.76 |
| person sensitivity / false-positive share / LR+ | — | 0.48 / 0.34 / 1.4 |
| new false prompt per 4-week window | — | 3.0% of non-converter windows |
| self-checks | OK | evaluate OK; pulse + nightly OK |

## Clinical safety and alarm burden

**What the numbers mean (default system, simulated).** Per 1,000 non-converting wearers:
- about 100 have a first false prompt by 6 months, about 230 by 12 months and about 340 by 16 months;
- about 400 confirmatory home-BP weeks are triggered per year, including repeats.

The positive predictive value depends on prevalence. It is 22% at the simulated 17% conversion rate. With the same sensitivity and false-positive share, it would be 13.5% at 10% conversion and 6.9% at 5% (arithmetic only, not an epidemiological estimate).

**Harms.** A false prompt asks for one week of guideline-concordant home BP readings ([ESC 2024](https://academic.oup.com/eurheartj/article/45/38/3912/7741010)); it never leads to treatment. The real harms are:
- repeat prompts and alarm fatigue;
- anxiety;
- above all, false reassurance: 52% of converters are never prompted before t_ref.

**Is it acceptable?**
- **Yes, as a "measure your BP at home" prompt in a research pilot,** provided the wording is neutral, repeats are suppressed, and routine screening continues unchanged.
- **No, as a "hypertension notification".** LR+ 1.4 is too weak to tell anyone that they are likely developing hypertension.

**Levers, none of which retunes on test:**
1. **Apply the panel's pre-specified repeat suppression** (`panel/cardiologist.md` §2: "suppress repeats for 3 months after a normal cuff series") as a fixed rule. On the same test decisions:

   | suppression after a prompt | prompts per non-converter person-year | prompts per falsely prompted person |
   |---|---|---|
   | none | 0.405 | 1.76 |
   | 13 weeks | 0.283 | 1.23 |
   | 26 weeks | 0.254 | 1.10 |

   By construction, this leaves the share ever prompted, the first-warning sensitivity and the lead time unchanged. Implement it in `warn.py` and report both versions.
2. **Re-anchor the personal baseline after a normal home-BP confirmation.** This uses the confirmation as information; evaluate it on the fit and calibration people.
3. **Do not expect a lower budget to buy efficiency.** At budget 0.25 the realised alarm rate is 0.19, with Se90 0.08 against 0.13 for chance (`results/weighted` operating curve). Person-level discrimination is the bottleneck, not the threshold.
4. **Report against the pragmatic comparator.** An annual home-BP week for everyone costs 1 week per person-year and gives near-complete detection with up to 12 months' delay. SENTINEL triggers about 0.3–0.4 weeks per person-year in non-converters and prompts 48% of converters before t_ref.

## Claim wording (Steps 2–3)

**Permitted, Step 3** (numbers from the default no-pulse system):

> "At the warning operating point (thresholds tuned on calibration people to 0.5 prompts per non-converter person-year; 0.41 realised on test), 34% of simulated non-converters (32–39% across seeds) received at least one false prompt during a median 16 months of monitoring (10% by 6 months, 23% by 12 months), with 1.8 prompts per falsely prompted person, while 48% of converters were prompted before the reference date (positive likelihood ratio 1.4). Each prompt asks for one week of home blood-pressure readings. These simulated figures are not comparable with the per-person specificity of commercial hypertension-notification features, which classify prevalent hypertension over a single 30-day window."

**Permitted, Step 2** (update the numbers after the coupling sweep):

> "Two pulse-wave channels derived from a frozen PPG foundation model, simulated with PPG-BP-derived noise and a within-person coupling set at the cross-sectional slope (an upper bound), did not improve discrimination or early detection (AUROC 0.614 vs 0.621; converters prompted before the reference 42% vs 48%). Their lower alarm rate reflected a different operating point, not better separation."

**Forbidden:**
- "Pulse channels reduce false alarms" or "improve specificity".
- Unqualified "specificity 0.70".
- `sens_spec92` written as "92% specificity", or placed next to Apple's 41.2% / 92.3%.
- "Sensitivity 19% at 92% specificity" without "per week".
- "`pulse_drift` detects BP-related vascular change".
- F1 quoted without its prevalence (17% conversion over about 16 months).
- Any pulse-on result presented without the β = 0 arm.

## RQ1–RQ6 scorecard, updated with Steps 2–3

| RQ | Step 1 | Steps 2–3 | why / what to do |
|---|---|---|---|
| RQ1 personal baseline | slight + | neutral (− if pulse is shown) | `pulse_drift` gets no personal baseline in 83% of people (S7). The core channels are unchanged. |
| RQ2 persistent change | neutral | neutral | Pulse adds no persistent-change evidence; with pulse, Se0 and Se30 drop. |
| RQ3 early detection | risk | + if M4 is fixed, − if not | "A foundation-model channel did not help even at the upper-bound coupling" is a credible negative. Selectively quoting specificity and alarms would be seen through. |
| RQ4 context | neutral / slight risk | neutral | Acute-night blanking and context regression are consistent, but the simulator lacks non-BP confounders of morphology (S9), so the benefit is untested. |
| RQ5 reliability | slight + | + | Graceful degradation with `drop_pulse`, the all-NaN invariance and the LifeSnaps invariance were all verified. |
| RQ6 uncertainty, abstention, evidence | + if M1 is fixed | + if M5 is fixed; − for the ledger until S7 | Time-explicit false-prompt reporting with LR+ and PPV is exactly the clinical honesty judges reward. The ledger currently presents a non-directional channel as risk evidence. |

**Net:** Steps 2–3 are engineering-sound and add credibility, provided they are framed as a negative result for pulse plus a frank false-prompt burden. Framed as "pulse improves specificity" or "92% specificity", they would cost points.

**Additional source:** Apple Inc., *Hypertension Notification Feature validation paper*, September 2025 (sensitivity 41.2% [37.2–45.3], specificity 92.3% [90.6–93.7], 30-day window, n = 2,229 undiagnosed adults; figures confirmed via secondary reports, because the PDF exceeded the fetch limit). https://www.apple.com/health/pdf/Hypertension_Notifications_Validation_Paper_September_2025.pdf

---

# Final verification (after the coders' fixes)

**Date:** 2026-10-03. **Method:** read-only re-runs on the current working tree. Scratch scripts `b5_final.py` (invariants, coupling isolation, independent re-computation of the burden and pre-onset metrics on the current code, seeds 0–2), `b6_latent.py`, `b7_chance_onset.py`; output in `scratchpad/audit/out/b5.log`. The with_pulse arms were not re-run; their matched-rate numbers were recomputed from the stored operating curves.

**Self-checks:** `python tests/test_pipeline.py` OK (8.8 s); `python -m sentinel.evaluate` OK; `python -m sentinel.warn` OK; `.venv python -m sentinel.pulse --selfcheck` OK, including the nightly check (6.8 s).

**Reproduced exactly (45/45 values, |Δ| < 1e-9, current code vs stored `results/pulse/seed*/metrics.json` main):**
- KM false prompt by 6 / 12 months: 0.095 / 0.228. My own KM agrees, and so does the crude proportion, because follow-up is near-uniform (minimum 441 days).
- Never prompted: 0.658, over a median of 504 days.
- Prompts per non-converter: 0.599.
- Alarm rate: 0.405 per calendar person-year, 0.437 per monitored person-year.
- With the 26-week refractory: 0.254, using my own `episodes()` from b4. First warnings were unchanged for every person.
- LR+ 1.41; PPV 0.228.
- Se0 / Se30 / Se90: 0.481 / 0.322 / 0.161.
- Post-onset Se30 / Se90: 0.281 / 0.120.
- Pre-onset first warnings: 2 / 1 / 2.

## Item status

| item | status | evidence |
|---|---|---|
| M1 CI / permutation / wording | VERIFIED | `summary.md` and `metrics.json`: NB-corrected +0.047 [−0.010, +0.104], p = 0.108; stratified permutation p = 0.0099 (100 perms); percentiles relabelled "split-to-split variability, not a confidence interval"; "suggestive". |
| M2 labels by definition | VERIFIED | `sbp120`, `stage12_vs_normal` (spectrum-bias note) and `sbp130_dbp80` (EXPLORATORY, post-audit) in the summary, `metrics.json` and `head.npz` `label`; treatment unrecorded; comorbidities and vascular-phenotype caveat. Continuous-outcome R² was not added (optional). |
| M3 coupling an assumption, grid with 0 | VERIFIED | `--pulse-coupling`. Arms differ only in pulse_htn: core columns, NaN pattern and noise are identical, and the 2× shift is exactly 2 × the 1× shift (b5). No √n noise gain. At β = 0: AUROC −0.003 (0/3 seeds), alarms −0.010. |
| M4 matched-rate comparison | VERIFIED | My recomputation from the stored curves matches `summary.md` to 3 dp (budget 0.5: Se0 .481 vs .453, Se30 .322 vs .313, Se90 .161 vs .165). `KEY` has Se0/Se30. "No improvement" in words. See N-2 on the label "pre-specified". |
| M5 time-explicit burden, no Apple | VERIFIED | KM 6/12 mo, cumulative "specificity" defined, prompts per person, PPV with prevalence, LR+. No Apple mention in the results or README. `sens_spec92` is captioned per week. The paper intro cites Apple only as background, which is acceptable. |
| S1 scale-free inputs | PARTIAL | ICC 0.522 and slope 0.0099 (final head) are reported, but `data.PULSE_COUPLING` and CONTRACT.md say 0.0092 (N-3). |
| S2 spectrum bias | VERIFIED | Stated next to `stage12_vs_normal`. |
| S3 robustness checks in repo | NOT DONE | Optional. HR, age² and comorbidity contrasts exist only in this audit. |
| S4 `head.npz` domain | VERIFIED | `label`, `domain` ("NOT validated on wrist reflectance PPG at night") and `score` (between-person only) are stored. |
| S5 Table 15 framing | VERIFIED | "Consistent with the authors' own Table 15". |
| S6 confounders | VERIFIED | Hospital cohort, 38 / 20 / 25 comorbid, treatment unrecorded. |
| S7 pulse_drift | VERIFIED | Removed from `__init__`, `data`, `pulse` and `run`; only explanatory comments remain. |
| S8 drift simulator | VERIFIED (moot) | The channel was removed. |
| S9 HR-correlated noise, quality- and skin-tone-dependent clips | NOT DONE | CONTRACT lists "no acute-context or skin-tone effect" as an assumption, but neither HR coupling nor the word "optimistic" appears. |
| S10 TP definition / exposure | PARTIAL | Done: the pre-onset column and both denominators. Not done: a common-time-axis incidence curve for converters vs non-converters. |
| S11 age-tercile caption | VERIFIED | "model behaviour by age; age has no causal role in the simulator". Not done: the real-world disclosure that older wearers will get more prompts. |
| Default-off invariant | VERIFIED | Seeds 0–2: 340/340 values shared with `results/weighted` identical. Coupling-0 and 2× mains are identical to the default. LifeSnaps `real_world.{json,md}` byte-identical. |
| Suppression is burden-only; chance floor unaffected | VERIFIED | `operating_curve` chance = 1 − exp(−budget × exposure). It never calls `prompts()` and is identical across weighted, pulse and both coupling arms. `metrics()` asserts that first warnings are unchanged. |

## New issues (ranked)

**N-1 (fix before the paper): the 26-week refractory is not the panel's pre-specified rule.**
- `panel/cardiologist.md` line 23 specifies "suppress repeats for 3 months after a normal cuff series", that is, 13 weeks.
- `warn.py` (comment), `summary.md` and `report.md` instead call the 26-week period "pre-specified by the clinical panel".
- 26 weeks was chosen after my audit table showed both values: 13 weeks → 0.283, 26 weeks → 0.254 prompts per non-converter person-year, on identical decisions.

Fix: either make 13 weeks the reported rule and 26 weeks a variant, or keep 26 weeks but drop "pre-specified by the panel" and write "26 weeks (one prediction horizon), chosen after the audit; the panel's 13-week rule gives 0.28".

**N-2 (wording): "pre-specified rule" for the no-improvement verdict.**
- I cannot verify the timing. The rule was written after the own-operating-point results were known (this audit, M4).
- The rule (3/3 seeds × 3 metrics) is strict enough that most modest true gains would also read "no improvement".
- The negative conclusion should rest on the effect sizes: matched-rate differences −0.028, −0.009 and +0.004, with seed SDs of about 0.03 and about 42 test converters per seed.

Fix: in the paper, say "decision rule" without "pre-specified", or omit it and give the numbers.

**N-3 (consistency): the coupling default does not match the measured slope.**
- `PULSE_COUPLING` = 0.0092, and CONTRACT.md calls this "the age-adjusted between-person slope".
- `results/ppg_bp/metrics.json simulator_inputs.coupling_sd_per_mmHg` = 0.0099.

The effect on conclusions is nil, because the 2× arm (0.0184) brackets it. Fix: cite 0.0099 as the slope and 0.0092 as the "≈ slope" default, or set the default to 0.0099.

**N-4 (minor): "age alone reaches the published embedding figure" is not backed by a stored number.**
The 0.774 value was dropped from `metrics.json`. In the paper, quote the stored demographics value (0.79) or the authors' Table 15.

**N-5 (note: a zero-coupling pulse channel is not harmless).**
At β = 0, with_pulse lowered Se0 by 0.047 (own operating point) and 0.045 (matched rate), in 3/3 seeds. Pure noise with 11% weight dilutes the core channels. This supports default-off. Do not describe the β = 0 arm as "no effect".

**N-6 (simulator disclosure, optional): some label non-converters are latent drifters.**
- 19% of simulated label non-converters (37 of 199 per seed on test) are latent drifters that were not cuff-confirmed within follow-up.
- 67% of them were prompted, against 27% of people with no latent drift.
- So about 37% of "falsely" prompted people carry a real, unconfirmed simulated rise.

The label-based burden remains the primary, correct figure. This is simulator-only and must not be used to shrink the headline.

**N-7 (pre-onset analysis, optional and post hoc): the right chance floor.**
`sens_post_onset_*` must not be compared with the unrestricted chance floor (0.254 / 0.204). Under the same rule (a random first warning before onset = miss), random warnings at the model's realised rate give 0.093 (30 d) and 0.047 (90 d). The model (0.281 / 0.120) is above this floor in every seed. This is auditor-computed (b7); add it to the repo before quoting. The paper's primary 90-day verdict (0.161 vs 0.204, not above chance) stands.

## Paper-ready claims (approved wording)

**(a) PPG-BP, real labels, cross-sectional:**
> "In PPG-BP (219 hospital participants in China; one seated upper-arm cuff reading and three 2.1-s fingertip PPG clips each; antihypertensive treatment not recorded), embeddings from a frozen PPG foundation model (PaPaGei-S) alone discriminated SBP ≥ 120 from < 120 mmHg no better than age, sex and BMI (cross-validated AUROC 0.70 vs 0.70). On the authors' split, the embeddings reached 0.69 [0.55–0.81] against 0.79 for age, sex and BMI, consistent with the authors' own appendix (0.77 for each). Added to age, sex and BMI, the embeddings raised AUROC from 0.70 to 0.75 (+0.05; resampling-corrected 95% CI −0.01 to +0.10, p = 0.11; permutation within age-decile × sex strata, p = 0.01). Pulse shape may thus carry some between-person information about BP level beyond demographics; the gain is suggestive rather than established, and tracking of within-person BP change was not tested."

Optional, only with both qualifiers: "In an exploratory post hoc analysis against ≥130/80 mmHg, the gain was +0.07 (corrected 95% CI +0.02 to +0.13)."

**(b) Pulse-channel extension, simulated:**
> "An optional nightly pulse channel (median head logit of clean night clips) was simulated with an assumed within-person BP coupling: zero, the cross-sectional between-person slope (an upper bound), and twice that. At the upper-bound coupling and matched alarm rates (0.41 prompts per non-converter person-year), it did not improve early detection (warned before the reference date 0.45 vs 0.48; Se30 0.31 vs 0.32; Se90 0.165 vs 0.161; AUROC 0.619 vs 0.621; three seeds, about 42 test converters each). With zero coupling, the added channel lowered the share of converters warned by 0.05 in every seed; at twice the upper bound, matched-rate Se30 rose by only 0.02 ± 0.02. The channel is therefore off by default."

**(c) False-prompt burden and suppression, simulated:**
> "At the operating point (thresholds tuned on calibration people to 0.5 prompts per non-converter person-year; 0.41 realised on test per calendar year, 0.44 per monitored year), the Kaplan–Meier probability that a non-converter had received at least one false prompt was 0.10 at 6 months and 0.23 at 12 months; over a median 504 monitored days, 34% were prompted at least once (0.60 prompts per non-converter). 48% of converters were prompted before the reference date (positive likelihood ratio 1.4; person-level PPV 0.23 at the simulated 17% conversion rate, lower at lower prevalence). Each prompt asks for one week of home BP readings. A 26-week refractory period after each prompt (one prediction horizon), which leaves every first warning unchanged, would lower the burden from 0.41 to 0.25 prompts per non-converter person-year."

If the panel's 13-week rule is added to the repo, append: "(0.28 with the panel's 13-week rule)".

**(d) Pre-onset sensitivity analysis, simulated:**
> "Because the simulator knows when each drift began, we also scored converters first warned before the simulated drift onset as misses (5 of 125 test converters over three seeds, warned 27–103 days before onset): Se30 fell from 0.32 to 0.28 and Se90 from 0.16 to 0.12."

Optional, only after N-7 is in the repo: "Scored the same way, random warnings at the model's alarm rate reach 0.09 and 0.05."

## Forbidden phrasings (in addition to the earlier lists)

- "pre-specified by the clinical panel" for the 26-week refractory (N-1). Also "suppression reduces false alarms or false positives": the share of non-converters ever prompted is unchanged at 34%; only repeats fall.
- "pre-specified decision rule" for the pulse verdict, unless timing evidence is shown (N-2).
- "the pulse channel has no effect at zero coupling" (N-5). Also "pulse improves Se30 at 2× coupling" quoted at its own operating point (+0.040 with alarms +0.036, 3/3 seeds), which is an operating-point shift.
- "0.0092 = the measured slope" or "coupling measured": the slope is between-person (0.0099), and the coupling is assumed.
- `sbp130_dbp80` (p = 0.009) presented as primary or without "exploratory, post hoc". Also the 30–65 age band (0.61 → 0.73) quoted as the target-population gain.
- `sens_post_onset_*` compared with the unrestricted chance floor in either direction. Also "beats chance at 90 days" based on the onset-restricted floor alone. Also any "detects drift before onset" reading of the 5 pre-onset warnings.
- "specificity 0.66 / 0.67", or "never prompted" without "cumulative over a median 504 days". Also any juxtaposition with Apple's 92.3%.
- "Validated on real data" for the pulse channel; "detects or predicts hypertension from PPG shape"; "+0.047 [0.019, 0.074]" as a CI; "20/20 repeats".

## Updated verdict

M1–M5 are verified. All burden, matched-rate and pre-onset numbers reproduce exactly from the current code, and the default-off and LifeSnaps invariants hold. One wording error must be fixed before the paper: N-1, the refractory attribution. N-2 and N-3 are small consistency and wording fixes. Remaining open items: S3 (optional), S9 (simulator realism, disclose it) and S10 (the common-time-axis curve). None blocks the approved claims above.

# Juror 2: clinical expert (cardiology, CHU)
Team SENTINEL-HTN, local branch `rq3-trend`.

## 1. Deliverable compliance
- **Paper:** all sections present; about 5 IEEE pages, at the limit (not compiled). The author line is still a TODO.
- **Slides:** missing.
- **Repo:** the code runs, but `paper/` and `panel/` are untracked, and `main` has neither the paper nor the trend features.

## 2. Verification log
1. `python tests/test_pipeline.py` passes in ~10 s (AUROC 0.616).
2. Table I "Full" vs `results/rq3_trend/seed*/metrics.json`: the means match (AUROC 0.648 from 0.679/0.609/0.655; AUPRC 0.150; Se30 0.483; Se90 0.190; alarms 0.493; precision 0.211; ECE 0.006). The ± values are population SD (sample SD: AUROC ±0.035, Se30 ±0.096).
3. "Beat both baselines in every seed" is true. "77/131 converters warned" is correct (29+21+27 of 41+43+47).
4. The 90-day chance floor (0.244) and the operating-curve figures (0.325 vs 0.420 at 1/py) are correct. **The 30-day floor (0.301), the headline RQ3 comparison, is produced by no committed code**: `run.py:111` computes the floor only at 90 d. My estimate (~0.30) agrees.
5. Fairness and robustness figures are correct: dark-tercile abstention 0.231, noise alarms 0.99, and MNAR/sensor-failure abstention 0.334/0.522.
6. "Full w/o trend" comes from the earlier pipeline (`results/seed*`, different θp), not from an ablation in the same run.
7. The SCD reframing arithmetic holds. ~38/100,000/yr is ≈1×10⁻⁶ per person-day, so at 99.9% specificity the PPV is ≤0.1%.
8. In `sentinel/data.py::_person`, age, sex and BMI don't depend on conversion, and baseline SBP is capped at 123 for everyone. By design, static risk carries **no signal**.
9. The endpoint (`__init__.py:31`) is home BP ≥130/80. ESC 2024 sets home hypertension at ≥135/85.

## 3. Scores
| RQ | /10 | Evidence |
|---|---|---|
| RQ1 Personalization | 8 | Shrinkage baseline, firmware restart; removal drops AUPRC 0.150→0.114, partly by construction |
| RQ2 Temporal | 8 | CUSUM, 4-of-6 persistence, missing weeks not evaluable, causal Kalman trend with a unit test for causality |
| RQ3 Early detection | 5 | Se30 0.48 vs 0.30 chance, reported honestly. But 90 days is at chance, drift is compressed to 120–200 d, the comparators are straw men (#8), the floor can't be reproduced and there's no usual-care comparator |
| RQ4 Context | 6 | Temperature, season and menses are regressed out, and acute context is masked (AUPRC 0.111 without it). But the simulator injects exactly these confounders, and Ramadan, beta-blockers and OSA aren't modelled |
| RQ5 Reliability | 7 | Six perturbations on test data only, reported honestly. Noise, the commonest real PPG failure, doubles alarms to 0.99/py; abstention is 4× higher in dark skin |
| RQ6 Uncertainty | 8 | No "stable" state, and a warning needs both p_lo and persistence. ECE 0.006 (flattered by the low base rate). Abstention counts as a miss and rises as data degrade |
| **Total** | **42/60** | |

## 4. Clinical strengths and weaknesses
**Strengths**
1. **A sound reframing.** The SCD PPV argument is correct, hypertension is the modifiable upstream target, and the system displays no mmHg value, which follows the ESH position.
2. **A safe, actionable output.** A warning leads to 7 days of home readings with a validated upper-arm cuff, so a false alarm costs a week of readings, not a drug. Having no "stable" state prevents false reassurance.
3. **Honesty.** The paper reports the chance floor, the 90-day null result, the skin-tone inequity and the noise failure.

**Weaknesses**
1. **Circular evidence.** The couplings (+0.15 bpm/mmHg, and −40 steps/mmHg, which reverses the causal direction) are assumed and then "discovered". Static risk is switched off, so "both baselines stayed at chance" (abstract) is an artifact of the simulator.
2. **Endpoint and intended use.** A home threshold of 130/80 is below ESC 2024, the guideline Tunisian practice follows. The panel's exclusions (beta-blockers, ivabradine, AF, pregnancy) and Ramadan are missing from the paper.
3. **Clinical burden.** AUROC is 0.65, 4 in 5 warnings are false, and noise pushes this to about one cuff series per healthy wearer per year. 41% of converters are never warned. Cuff lending through CSBs is written as fact, but it is only a proposal.

## 5. Q&A questions
1. Your simulator gives age, BMI and baseline BP no link to conversion. Can you show the strap beating a Framingham-type score plus an annual cuff check, which is what a Tunisian GP actually has?
2. How many converters remain at the ESC home threshold of ≥135/85? And what should a CSB doctor do with a home mean of 132/82?
3. Who absorbs about one warning per healthy wearer per year under real noise, and what happens to someone on a beta-blocker, in AF, or fasting during Ramadan?

## 6. Placement: **Top-3**
Against transformers showing AUROC above 0.9 on leaky data, this is the most credible approach (the brief's criterion) and the safest for patients. It won't win: the data are synthetic only, discrimination is weak, the comparator is a straw man and there are no slides. If there's still no deck at the pitch, I'd place it as a Finalist.

## 7. Must-fix before final submission
1. Deliver the slide deck (≤15 slides), push the paper and trend code to `main`, and fill in the authors.
2. Either drop "baselines stayed at chance", or give the simulator realistic static risk and rerun.
3. Report results at the ESC home threshold of ≥135/85 (or rename the endpoint) and align the pathway with it.
4. Put the exclusions, the red-flag screen (SAMU 190) and Ramadan into the intended-use paragraph.
5. Commit the code for the Se30 chance floor, and report sample SD.

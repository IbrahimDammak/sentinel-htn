# Juror 1 (Chair): SENTINEL-HTN

I judged the local `rq3-trend` state.

## 1. Deliverable compliance
- **Paper:** IEEEtran format with all ten required sections. About 3,100 words, 22 references, one `figure*`, two figures and a table put it at an estimated **4.5–5 pages**. It is uncompiled, so the limit is unverified. The author block still reads `TODO`.
- **Slides:** **none**. A required deliverable is missing.
- **Repo:** `origin/main` has only the initial commit, with no trend code and no paper. Locally, `paper/` is *untracked*. The README points to the pre-trend `summary_3seeds.md`, so the paper's link cannot reproduce Table I.

## 2. Verification log
- `python tests/test_pipeline.py` **passed** (exit 0, AUROC 0.616), and so did `python -m sentinel.evaluate`.
- A rerun of seed 0 was **bit-identical** to `rq3_trend/seed0/metrics.json`.

| Paper claim | metrics.json (seeds 0/1/2) | Verdict |
|---|---|---|
| AUROC .648±.029 | .679/.609/.655 | Match |
| AUPRC .150, Se30 .483, Se90 .190, chance Se90 .244 | main, operating_curve | Match |
| Alarms .493, precision .211, ECE .006 | main | Match |
| 77/131 warned, lead 64±4 d | sens_lead_0 | Match |
| Noise alarms .99; dark-tercile abstention .231 | robustness, fairness | Match |
| **Chance Se30 .301** | absent: `run.py` computes chance only at 90 d | **Untraceable** (I re-derived .295) |
| "w/o trend" row | `results/seed*/`, an earlier run | Partial |

- The "±SD" values are population SDs (ddof=0) over n=3. Sample SDs are about 20% larger (Se30 ±.096). This is not disclosed.
- **Extra probes (seed 0):**
  - Prevalence is 6.2%, and 88% of predictions are p<0.1.
  - The **Brier skill score is 0.046** against a constant predictor.
  - Band width correlates with p at r=0.91. Ordering by width gives AURC .0345, against **.0354 ordering by p alone**.

## 3. Scores

| RQ | /10 | Evidence |
|---|---|---|
| RQ1 Personalization | 7 | The shrinkage baseline works: without it, AUPRC drops .150→.114 and Se30 .483→.315. But the baseline is frozen after 28 days, and the simulator was designed so between-person spread exceeds the effect. |
| RQ2 Temporal | 8 | CUSUM, 4-of-6 persistence with neutral missing weeks, and a causal Kalman trend (unit-tested). The trend lifts Se30 .334→.483. |
| RQ3 Early detection | 6 | The model beats an honest chance floor at 30 d (.483 vs .301), and the team admits failure at 90 d (.190 vs .244). The gain is only about a month on a compressed drift, and the 30-day floor cannot be reproduced. |
| RQ4 Context | 6 | Removing context drops AUPRC to .111, but this is circular: the simulator's season (`data.py:41-43`) has exactly the form the model regresses out. No unmodelled confounder is tested. |
| RQ5 Reliability | 6 | Six perturbations plus a fairness split. But noise doubles the alarm rate, MCAR-30% raises it .49→.66 (unmentioned), and at MCAR-60% abstention barely moves (.112→.143). |
| RQ6 Uncertainty | 5 | The three-state design is good. But the band adds nothing beyond p, abstention is only a valid-day count, and an ECE of .006 means little at 6% prevalence. |
| **Total** | **38/60** | |

## 4. Strengths
1. The evaluation design is rare for students: null comparators, a chance floor at the same budget, alarms per person-year, and abstention counted as a miss.
2. Negative results are reported honestly (the 90-day failure, noise, skin-tone inequity).
3. It is reproducible: about 1,300 lines of code, a hand-checked metric test and a bit-exact rerun.

## 5. Weaknesses
1. Everything is synthetic, and the simulator encodes the method's own assumptions, so the RQ1 and RQ4 ablations partly validate the simulator.
2. The uncertainty is largely cosmetic: the band tracks p, and the calibration claims say little (Brier skill score 0.046).
3. There are no slides, the paper is not in git, and the headline chance Se30 cannot be traced to any code.

## 6. Hard questions
1. "Your band correlates with p at r=0.91, and ordering by p gives the same AURC. What does your uncertainty add?"
2. "Non-converters' final 26 weeks are labelled 0 (`make_landmarks`), yet half of the simulated drifters (35%) never reach the label (17%). How does this censoring bias your AUROC and your false-alarm count?"
3. "Your simulator generates season exactly as your model removes it. Show us one confounder your model does not know about."

## 7. Placement
**Top-3 if the deck and repo are fixed; Finalist as it stands.** This is the most credible methodology I would expect among 10–20 student teams, and it matches the brief's emphasis on credibility. But an AUROC of 0.65 looks weak beside transformer entries, and the compliance gaps would lose it any close tie.

## 8. Must-fix (ordered)
1. Build the ≤15-slide deck, commit `paper/` and the trend code, push to `main`, and update the README.
2. Add the chance-floor Se30 to `run.py`, commit a script that generates Table I, and make "w/o trend" an in-run ablation.
3. Use ddof=1 or bootstrap CIs, and add a paired test of Se30 against chance.
4. Report the Brier skill score and the AURC obtained by ordering on p. Either make the band respond to data quality or tone down the RQ6 claims.
5. Compile the paper to confirm it fits in 5 pages, fill in the author block, and drop landmarks whose horizon runs past the end of follow-up.

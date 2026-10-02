# Juror 3 (industry: MedTech/AIoT CTO): SENTINEL-HTN

## 1. Deliverable compliance
- **Paper:** IEEEtran source with all 10 required sections and 23 references. About 3,050 body words, 3 figures and 1 table put it at roughly 5 pages, the limit; I could not compile it. The author line is still a TODO, and the state labels overflow their boxes in the architecture figure.
- **Slides:** missing.
- **Repo:** the pushed `main` is only the initial commit, and `paper/` and two panel files are untracked. The URL printed in the paper does not reproduce the paper.

## 2. Verification log
- `python tests/test_pipeline.py`: **PASS in 3.6 s** (AUROC 0.616). The six module self-checks (`python -m sentinel.*`) are all OK.
- `run.py --synthetic --n 1200 --seed 0` into my scratchpad: **35.7 s**. The resulting `metrics.json` is **identical** to the committed `results/rq3_trend/seed0`.
- **Paper spot-check:** AUROC .648, AUPRC .150, Se30 .483, alarms .493 and precision .211 all match seeds 0–2.
  - The reported SDs are population SDs; the sample SDs are about 20% larger.
  - The chance Se30 of 0.301 appears in no results file.
- **git:** on `rq3-trend`, 2 commits; `main` is 1 commit behind; 4 untracked paths.

## 3. Scores
| RQ | /10 | Evidence |
|---|---|---|
| RQ1 | 8 | Shrinkage baseline (Eq. 1), re-baselined on firmware change. Removing it drops AUPRC from .150 to .114 and Se30 from .483 to .315. |
| RQ2 | 8 | CUSUM, a 4-of-6 persistence rule and a causal Kalman trend. A test asserts causality. The ledger omits the Kalman trend the paper says it contains. |
| RQ3 | 5 | Se30 is .483 vs .301 by chance, with a median lead of 64 d. At 90 d it is *below* chance (.190 vs .244). |
| RQ4 | 7 | The no-context ablation drops AUPRC to .111, but the confounders are the team's own simulated ones, and alcohol, illness and menses are self-reported. |
| RQ5 | 6 | Missing-data and sensor-failure cases are absorbed by abstention. Noise doubles alarms (0.99/py) and 30% missingness raises them to 0.66. The darkest skin tercile abstains 0.23 of the time. |
| RQ6 | 8 | Three states, warnings gated on p_lo, and abstention counted as a miss; ECE .006. The band rests on only 20 bootstraps. |
| **Total** | **42/60** | |

## 4. Strengths and weaknesses
**Strengths**
1. **Engineering quality:** about 1,170 lines using NumPy, pandas and SciPy only. It has leakage guards (`onset` is asserted out of the features, and a test checks for future cuff reads) and reproduces bit for bit.
2. **Honest evaluation:** null comparators, a random-alarm chance floor, an alarm budget, and a published 90-day negative result.
3. **The right product shape:** no BP number, a locked model, and a warning that leads to a 7-day home-cuff series and then a GP visit. This mirrors Apple K250507, the only cleared precedent.

**Weaknesses**
1. **Circular evidence:** `data.py` builds in a coupling of +0.15 bpm per mmHg, and the model then finds it. There is not one real night of data.
2. **Nothing physical:** the "single wrist strap" is a desk design with estimated power only, and its front end (MAX86176) is listed as discontinued.
3. **No differentiation or regulatory story:** Apple already ships a cleared notification on hardware people own. SENTINEL has 0.21 precision and requires a new device. There is no intended use and no MDR class (Rule 11 would make it Class IIa or higher, with IEC 62304 and ISO 14971).

## 5. Q&A
1. Your simulator builds in +0.15 bpm per mmHg. What real-data result would falsify SENTINEL, and when will you run it?
2. If `load_csv` accepts any wearable export, why build a strap instead of software for Fitbit, Samsung or Apple Health data?
3. At 0.21 precision, how many cuff series and GP visits does one true warning cost, and who pays for them in Tunisia?

## 6. Placement: **Top-3 (likely 2nd–3rd)**
It fits the brief's "credible, not most accurate" test better than a typical transformer entry. It loses the top spot because it has no deck, no demo, only synthetic data and an AUROC of 0.65 that ML-heavy teams will beat on paper. **If there is no deck on the day, it drops to Finalist.** Fund: not yet. Hire: yes.

## 7. Must-fix (ordered)
1. **A 15-slide deck.** Suggested content:
   - the problem, and why the system outputs no BP number;
   - the one-strap user journey and the three states;
   - the pipeline;
   - the chance-floor result, with "90 d = chance" stated as a finding;
   - skin tone and robustness;
   - a comparison with Apple;
   - cost and regulatory path;
   - limitations;
   - the ask.
2. **A live demo.** Run `run.py` on a fresh seed (36 s) and show one timeline going from baseline to drift to WARNING, with its ledger, plus one POOR_QUALITY suppression. Ideally, add a few real nights via `load_csv`.
3. **Make the repo match the paper:** commit `paper/` and the panels, merge into `main`, and tag the submission.
4. **Fix the paper:**
   - add the authors;
   - compile it and confirm it fits 5 pages;
   - report sample SDs;
   - save the chance Se30 to `metrics.json`;
   - put the Kalman trend in the ledger.
5. **Add an intended-use and MDR/IEC 62304 paragraph,** with a three-row comparison against Apple.

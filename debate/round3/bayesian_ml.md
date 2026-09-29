# Round 3 — Defence and final position: THE BAYESIAN (BayesTrack-HTN v3)

Scarce resource: incident-hypertension events with dense pre-onset data. `[bayesian_ml-n]` are my references. No new research this round.

## 1. Rebuttal

**clinician / device_engineer / ppg_scientist: "STABLE is unsafe, a fourth state, false reassurance."** Conceded. The challenge defines three states and 58.8% of undiagnosed cases get no alert at the cleared operating point (a modelled figure: [bayesian_ml-5] is a NHANES model of manufacturer sensitivity/specificity). STABLE is removed. Output: SUFFICIENT-warning, INSUFFICIENT, POOR-QUALITY. Absence of a warning is never displayed as reassurance.

**clinician: "Bias, not noise: proxies attenuate change; add a shrinkage-toward-calibration term."** Conceded, and the audit agrees that my sentence that proxy variance grows with calibration distance overstates [bayesian_ml-25] (Walzel: n=37, one watch, a mean difference at one threshold). Attenuation is the documented failure: 1.8 of 7.4 mmHg registered [device_engineer-14] and -1.0 of -19.7 mmHg (n=3) [clinician-13]. The model gains a per-channel gain term with a prior below 1, and no channel is assumed unbiased.

**clinician: "Synthetic onsets are circular for RQ3."** Accepted. Injected-onset data give only delay-versus-magnitude curves for a detector, never a headline lead time. Real-event lead time is the headline; synthetic results go to a robustness appendix.

**clinician: "[bayesian_ml-6] is n=1."** Yes: WEAK, honestly tagged, not prospective.

**em_engineer: "C13 ignores physiologist-28 and PS-19."** Conceded. "Wearable SCD prediction rests on single-case evidence" was too broad. A 14-day single-lead ECG predicted near-term sustained VA (external AUROC 0.948, PPV about 9–10% in a referred population) and accelerometry reached 0.74 in ICD patients. F2 is out of scope here, not infeasible.

**em_engineer / device_engineer / physiologist / ppg_scientist / clinician: A0 is a strawman; no cuff-only or level-only null.** Fully conceded. A0 is now a strong pooled level model (frozen encoder score plus demographics, re-scored per landmark), and a cuff-only hazard (intermittent cuff BP, slope, demographics) is added. In Aurora the calibration cuff plus time of day beat every waveform model (the audit says my "not for within-person change" carve-out was unsupported, and I removed it). Mandatory ablations: A0 level-only, A0' cuff-only, A_full. If the subject-bootstrap CI of the gain includes zero, RQ1 personalisation is dropped from the paper.

**em_engineer: "Prostate PSA analogy versus in-domain ΔC of 0.008–0.019."** The in-domain number wins, and I say so. The PSA landmark result (0.743 to 0.800) is a single trial, SEs 0.018 each, no test: an analogy only. NightSignal supports the design pattern, not months-scale detection.

**em_engineer / physiologist: "POOR-QUALITY fires when a key channel is missing, so missed spot-checks become misses."** Fixed: no EM or spot-check channel is "key"; POOR-QUALITY is per observation and per week and uses channel-level q-weights. Skipped spot-checks are modelled as MNAR. Pre-registered A8 effect: Se(90 d) 40% to 55% needs about 85 converters. I will state that this is unattainable on the likely data, so A8 is a power analysis for the future pilot, not a pass/fail.

**physiologist: "Rest-equivalent pools states; z̃ is the generic sympathetic signature; C12 uses between-person associations."** All three conceded. Sleep and daytime stillness become separate channels (I adopt the physiologist's split). The error SD reduction of 15–20% in the calibration posture supports this. RHR up, HRV down and PAT down agree on "something changed", not on vascular change. C12 is downgraded: steps and sleep are "associated with" incident HTN (All of Us), not shown as within-person predictors. My 60-minute post-exercise rule is an assumption with no cited support; I mark it a tunable parameter.

**physiologist / ppg_scientist: season in the hazard; NPV threshold; right-censoring.** Season and ambient temperature enter as covariates. Because STABLE is gone, the NPV threshold question is moot. Censoring: non-converter warnings within W days of end of follow-up are censored (my own round-2 correction of E2).

**ppg_scientist: "ACI needs labels; C1 transfers method, not SNR."** Both correct. ACI's guarantee is long-run and assumes feedback each step, which sparse cuff labels weaken, so ACI is optional. NightSignal fired on RHR ≥4 bpm over 2 nights, a bigger and faster signal than pre-hypertensive drift.

**ppg_scientist: events per predictor for the landmark hazard.** A penalised discrete-time logistic layer with at most a handful of pre-specified features; fewer than about 10 events per predictor triggers a fallback to the level model plus threshold on the change statistic. I do not have a validated rule of thumb from the corpus, so this is my design choice.

**device_engineer: conformal with few positives.** Conceded (round 2). Split conformal needs at least 9 positives per stratum at α=0.1, and 19 at 0.05.

## 2. Audit response

- **L45 "persistence gating matters empirically" (ref 1):** replaced by "consistent with". Alavi did not ablate 2-night gating; the 72%/69% comparison is a Fitbit subset.
- **L19 (ref 25):** "exactly the regime where hypertension emerges" withdrawn. **L53:** variance-growth is a design hypothesis, not a finding.
- **L150 (ref 23):** carve-out removed. **L114:** ABPM only in the 483-person ambulatory arm.
- **L104 (ref 18):** "a related Apple foundation model", not the cleared feature's encoder.
- **L21 (ref 24):** "ESH suggests tests as applicable."
- **L55 (refs 26, 27):** "associated with".
- **L9 (ref 5):** PPV 69.1%/NPV 79.0% are modelled.
- **L61 (ref 4):** 15 usable days is a study-inclusion rule, not shown as a device gate.
- **PREPRINT tags** added for refs 12, 15 (and 8, 9, 16–20 already).
- **Ref 3 (Mitratza):** orphan; either cite for the 20–88% range or delete. I delete it.
- **Ref 28 Cossu:** ALS/MS patients, Garmin, a Bayesian smoother, WEAK. **Ref 29:** analogy, single prostate RCT. **Ref 19 LSM-2:** label is self-reported HTN, not incident.

## 3. PROTOTYPE CARD (v3), BayesTrack-HTN

- **Target:** emerging HTN warning plus timestamp; no mmHg; no acute stream.
- **State model:** hierarchical multivariate local-level model, Student-t, quality-weighted (q-weights), per-channel attenuation gain, season and temperature covariates, sleep and daytime as separate channels; baseline ≥28 valid nights.
- **Detection:** CUSUM/BOCPD on residuals; at most three pre-registered persistence rules; thresholds set on non-converters only (Neyman–Pearson).
- **Risk layer:** penalised discrete-time landmark hazard on pooled level plus deviation features; isotonic calibration; conformal optional.
- **Output:** three states; evidence ledger.
- **Evaluation:** subject-grouped forward-chaining; abstention counts as a miss; alarms per non-converter person-year; censoring-aware precision; delay distributions; no point-adjust; scheduled HBPM to avoid verification bias; AURGC alongside AUROC.
- **Ablations:** level-only, cuff-only, no-context, per-channel, ITA-stratified MNAR stress.

## 4. Final ranking

| Option | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 | RQ6 | Ev | Eng | Stu | Justification |
|---|---|---|---|---|---|---|---|---|---|---|
| CONFIRM-HTN | 5 | 6 | 7 | 5 | 5 | 6 | 6 | 7 | 8 | Strong t_ref and action loop; no formal uncertainty. |
| EM-ANCHOR | 6 | 6 | 5 | 6 | 7 | 6 | 3 | 5 | 4 | EM unscoreable, though modality-optional design is useful. |
| TRACE-PPG | 7 | 6 | 6 | 6 | 8 | 6 | 7 | 8 | 8 | Most testable; conformal layer flawed. |
| NOCTURNE | 7 | 8 | 6 | 8 | 6 | 6 | 5 | 6 | 6 | Best context; axis counting flawed. |
| BayesTrack-HTN (mine) | 8 | 8 | 6 | 6 | 8 | 8 | 5 | 6 | 5 | I mark RQ3, RQ6 and Ev down: conformal weak, event count small, and no in-domain evidence that change beats level. |
| BioVance-Edge | 5 | 5 | 6 | 5 | 7 | 6 | 5 | 8 | 4 | Solid failure budgets; thin modelling. |
| F2 as stated | 2 | 2 | 1 | 2 | 3 | 3 | 3 | 2 | 2 | Event labels absent; base rate hostile. |

## 5. Recommendation

- Use a joint state-space posterior on PPG+IMU features, level plus deviation, with a per-channel attenuation gain.
- Tune every threshold on non-converters, evaluate only on converters.
- Three states; no STABLE; abstention is a miss.
- Report Se at 0/30/90/180 days with label-interval width, and censoring-aware precision.
- Mandatory nulls: level-only and cuff-only.
- Fairness: coverage and abstention by skin tone, age, BMI under MNAR.
- Conformal only when positive counts allow; otherwise posterior plus isotonic.
- Any EM channel enters only as an optional q-weighted input with a pre-registered power analysis.

**Verdict on the user's idea.** F2 as stated cannot be evaluated on this challenge: there are no acute-event labels, the alarm budget per person is a different problem, and EM channels probably do not exist in the data. Its architecture (personal baseline, change detection, calibrated abstention) is the right frame for it; the state-space engine would transfer, but acute prediction needs referred-population data and different metrics.

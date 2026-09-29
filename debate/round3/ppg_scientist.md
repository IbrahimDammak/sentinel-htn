# Round 3 — Defence and final position: THE PPG SCIENTIST (TRACE-PPG v3)

`[PS-n]` are my references; others use their own IDs. No new research this round.

## 1. Rebuttal

**clinician / em_engineer / physiologist / bayesian_ml / device_engineer: "C11 overstates [PS-3]."** Five critics, one answer: conceded and narrowed. PS-3 compared ECG embeddings *instead of* PPG (0.769 vs 0.819) on self-reported, cross-sectional labels, with different participant counts (141,207 PPG against 106,643 ECG) and different sampling density. There is no PPG+ECG or PAT arm, and the embedding might partly learn treatment (a hypothesis). The audit adds that the gain over demographics is only 0.05 and that the authors are Apple's. C11 now reads: "ECG-only did not beat PPG-only on prevalent self-reported labels; no test of ECG added to PPG." It is graded WEAK for D1. It is not evidence that PPG beats ECG on emerging disease, and ECG representations do predict incident HTN (AIRE-HTN C 0.70) [physiologist-20].

**clinician / physiologist: "How do you show the score detects disease, not treatment?"** By design, not by assertion: exclude or stratify treated participants, and validate on incident labels in untreated people. This is unresolved until the data are checked, so I mark it as a risk.

**clinician / physiologist: C14 selective; sleep RMSSD is in TRACE.** Conceded. HELIUS was null for SDNN/RMSSD [PS-28], while positive results come from a 232,587-person cohort (10-s ECG) and ELSA-Brasil. HRV is "contested". It stays as one input in a joint model and is not a lead claim.

**clinician / device_engineer: "Persistence uses up lead time; earliest warning at about day 90."** Accepted, and I already moved to weekly aggregates with a ≥4-of-6 rule (about 28 days), keeping 30-day windows only for the coverage gate. Se(90 d) after persistence is unknown, and I will not claim a number. It is the primary output of the ablation.

**clinician: "Which threshold is primary; E3 as a number?"** The organisers' label; otherwise 30-day HBPM mean ≥130/80 for comparability with [PS-1], with ESC ≥135/85 as sensitivity. Budget: at most 0.5 alerts per non-converter person-year (shared with the clinician; a proposal).

**em_engineer: "C4 applied to ECG only."** Fair. Aurora's failed models included PPG alone, and the drug-effect miss was optical [PS-10; n=3]. Aurora is negative for absolute and next-day BP, not proven negative for within-person change. Burden of proof stays on EM, but PPG-only tracking is unproven too.

**em_engineer: "C7 contradicted by physiologist-28."** Conceded. My accelerometer AUROC 0.74 [PS-19] was not the best evidence. F2 fails here on scoring and base rate, not on absence of science. Also PS-20 "proven" is corrected below.

**em_engineer: skin-tone fairness hole (abstention counts as a miss).** Valid. Participants at ITA <10° were 36% of the sample but 50–85% of missing data [PS-22], so abstention becomes tone-linked sensitivity loss. My fallback: report valid-days-per-30 and sensitivity by ITA group, test MNAR, and use EM only as an *optional* fallback whose independence from pigmentation I have not shown. The audit also fixes my reassurance: Fitzpatrick RR 1.11 [0.84, 1.47] means a roughly 16% lower sensitivity cannot be excluded.

**physiologist: morphology transfer; PS-27 is finger, not wrist.** Conceded (UK Biobank PulseTrace PCA2). Wrist night-to-night morphology repeatability is unshown, so morphology is an exploratory channel.

**physiologist: PS-25 as evidence for the RQ4 problem.** Yes. The 1.15 alert-days per person came from non-COVID triggers (stress, alcohol, travel), against 3.42 for COVID. It supports context handling more than a benign false-alarm rate.

**bayesian_ml: Mondrian conformal is vacuous with few positives (9 needed at α=0.1).** Conceded. Conformal becomes optional; the main uncertainty is the hierarchical posterior plus isotonic calibration. Under 9 positive calibration subjects the output is INSUFFICIENT.

**bayesian_ml: All of Us lead time includes care-seeking time; access.** Both real. Incident HTN there is EHR-diagnosed, so lead time is partly clinic-visit gap; I report it with visit frequency as a covariate. Registered-tier access within the challenge window is unverified.

**device_engineer: raw PPG platform access; hardware.** Morphology and PaPaGei need raw PPG. Whether a commodity watch exposes it is a platform question I cannot answer from the corpus. If only aggregates ship, encoders cannot be tested and I revert to aggregate features.

**device_engineer: the card undercuts the MVP with a custom unit.** I agree: software-only is the MVP; hardware needs a metric that moves.

**bayesian_ml: right-censoring of precision; NPV for STABLE.** Accepted. Non-converter warnings near end of follow-up are censored, and there is no STABLE state.

## 2. Audit response

- **PS-20 "proven":** withdrawn. Restated: appropriate-intervention incidence 3% (2–3), I² 88.9%, single-arm, no comparator.
- **PS-1 "M6 validated at regulatory level":** withdrawn. The clearance covers prevalent-HTN notification only (sens 41.2% [37.2–45.3], spec 92.3%); nothing on lead time or trajectory. STRONG stands only for "cleared", not effectiveness. Add INDUSTRY-CLAIM (sponsor data).
- **PS-9 Mieloszyk:** removed as support for "no better than baseline" (tonometry beat baselines). Keep PS-8 only.
- **PS-16/17:** MODERATE plus INDUSTRY-CLAIM; sensitivity 69.3% (n=135) is from induced or simulated pulselessness.
- **PS-6:** 13.9/8.5 is in-distribution; external was 10.0–18.6 SBP.
- **PS-21:** "no significant bias" is underpowered (four studies, n=176).
- **PS-3:** INDUSTRY-CLAIM; self-reported label.
- **PS-33:** Samsung's 87.7% specificity missed its acceptance criterion; PS-32/33 show a wrist OSA feature exists, not that radar adds nothing.
- **PS-15 Aktiia:** clearance confirmed (2 Jul 2025, DXN); calibration interval and age range unverifiable, and clinician-11 says monthly. I drop the 24-h claim.
- **PS-27:** HR 2.88 is from full text, not the abstract; finger PPG.

## 3. PROTOTYPE CARD (v3), TRACE-PPG

- **Target:** emerging HTN warning from PPG+IMU on a commodity watch; no mmHg; no acute claim.
- **Data:** All of Us Fitbit+EHR (482 incident cases; access unverified) for development; challenge data if it ships.
- **Engine:** frozen PPG encoder score (level arm) plus weekly-aggregate change pipeline (main-sleep window, context-residualised), joint posterior; missing weeks are "not evaluable".
- **Persistence:** ≥4 of 6 weeks; 30-day windows only for the coverage gate.
- **Uncertainty:** posterior plus isotonic calibration; conformal optional; three states.
- **Fairness:** ITA-stratified valid-day coverage, MNAR stress tests.
- **Ablations:** level-only vs change vs both at matched alarms; three-arm ECG ablation (ECG only if arm 3 beats arm 2).
- **Regulatory:** software-only, locked model with per-user state, Class IIa intent.

## 4. Final ranking

| Option | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 | RQ6 | Ev | Eng | Stu | Justification |
|---|---|---|---|---|---|---|---|---|---|---|
| CONFIRM-HTN | 5 | 6 | 7 | 5 | 5 | 6 | 6 | 7 | 8 | Best labels and action loop; little modelling. |
| EM-ANCHOR | 6 | 6 | 5 | 6 | 7 | 6 | 3 | 5 | 4 | Honest but EM cannot be scored on the data. |
| TRACE-PPG (mine) | 7 | 6 | 5 | 6 | 7 | 6 | 6 | 8 | 8 | Testable and deployable; I cut RQ3/Ev because latency, treatment confounding and level-vs-change are open. |
| NOCTURNE | 7 | 8 | 6 | 8 | 6 | 6 | 5 | 6 | 6 | Best RQ2/RQ4; night data and season unproven. |
| BayesTrack-HTN | 8 | 8 | 7 | 6 | 8 | 9 | 6 | 6 | 5 | Best metrics; conformal weak with few events. |
| BioVance-Edge | 5 | 5 | 6 | 5 | 7 | 6 | 5 | 8 | 4 | Real power and regulatory numbers; hardware scope. |
| F2 as stated | 2 | 2 | 1 | 2 | 3 | 3 | 3 | 2 | 2 | Base-rate and scoring mismatch. |

## 5. Recommendation

- Software-only PPG+IMU notifier; all evaluation on features that exist.
- Hybrid: frozen encoder level score plus weekly change pipeline, with the ablation deciding how much personalisation adds.
- Weekly k-of-n persistence at least one menstrual cycle; season covariate.
- Report coverage and abstention by ITA group.
- Abstention counts as a miss; alarms per non-converter person-year; censoring-aware precision.
- Check treated versus untreated before trusting any encoder score.
- ECG only through the three-arm ablation.
- No acute stream; irregular rhythm makes windows ineligible (rhythm-aware SQI).

**Verdict on the user's idea.** F2 is not empty science: a 14-day ECG predicted near-term VA (external AUROC 0.948) and a case report showed a prodrome. But it fails this challenge. No acute labels exist to score RQ3, base rates in unselected people give PPV of about 0.1%, and EM cannot be tested on likely PPG-derived data. I would reinstate an acute channel only if an unselected prospective cohort showed PPV ≥10% at about one false alarm per 20 user-years.

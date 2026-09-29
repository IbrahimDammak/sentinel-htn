# Round 3 — Defence and final position: THE PHYSIOLOGIST (NOCTURNE v3)

`[physiologist-n]` are my references; `[PS-n]` = ppg_scientist. No new research this round.

## 1. Rebuttal

**clinician: "Nocturnal BP prognosis is borrowed for HR/HRV; what links wearable night HR/HRV to hypertension?"** Conceded as posed. Night-time SBP was the most informative BP measure [clinician-18], and [physiologist-10] is an expert consensus on nocturnal BP, not a study of HR/HRV. My night-window choice for HR/HRV rests on two weaker legs: wearables track night RHR/HRV against ECG (CCC 0.97–0.99), and night removes daytime context noise. The first is Oura-only, N=13, with Polar HRV at 0.82; the second is reasoning. PHY-9 stays a hypothesis, and the night-vs-all-day ablation decides. Bayes' data point cuts against me: removing night data cost only about 5% F1 in [bayesian_ml-19] (PREPRINT).

**clinician / bayesian_ml / device_engineer: "Slow confounders (season, weight, detraining, firmware, new drugs) pass through a 4-of-6 rule."** Conceded, and I withdrew "persistence exceeds every known transient". Timescale separation handles alcohol (days), infection (about 3 days) and the menstrual cycle, not season. Ambulatory BP rose 0.61 mmHg per 1 °C fall [physiologist-24] (concurrent-day, hypertensive panel), so a 10 °C swing is roughly 6 mmHg, the size of the drift (linearity assumed). Answer to "which model term": ambient temperature and season as explicit covariates in the state-space model, weight and step change as tagged covariates, device/firmware change as a forced re-baseline, and warnings reported with the calendar month of the warning and of t_ref. In the first year with no seasonal history, the model is honest: seasonal component unidentified, so the warning tier is capped at "watch".

**clinician / bayesian_ml: "≥4 of 6 weeks and ≥2 coherent axes may kill sensitivity; simulate it."** I cannot simulate without data, and I will not fake a number. Bayes' calculation shows that k-of-n false-alarm rates cannot be read from the rule when exceedances are autocorrelated, and independence gives P(≥4/6) of about 0.0013 at p=0.10. Both cut sensitivity as well as false alarms. I accept the fix: replace axis counting with a joint posterior, and treat k-of-n as one of at most three pre-registered rules tuned on non-converters.

**em_engineer / ppg_scientist / bayesian_ml: "Coherent is not independent; PEP inside PAT is sympathetic."** Conceded. "≥2 coherent axes" can be one sympathetic shift counted twice. Confounders are multimodal, so agreement shows something changed, not that the vascular system did. My specificity bet is now stated as a hypothesis: HR-adjusted vascular timing, since transients move it less. But em_engineer is right that a wrist gives PAT, not PTT, and HR explains little PEP variance at rest (R² 0.06) [physiologist-13]. Without an ICG or SCG reference this channel cannot be separated, so it is pilot-only.

**em_engineer: "Radar is the better-evidenced sensor for axis 3 (OSA)."** Conceded for evidence quality: AHI ICC 0.965 (N=200, with oximetry) and 85%/88% without SpO2 (N=141). But I hold the line on cost and deployability: wrist accelerometer and SpO2 OSA features are already authorised [PS-32, PS-33] (with Samsung's specificity missing its acceptance criterion), and radar fails a wearable power budget. Radar is a bedside phase-2 option for charging nights and non-wearers, never for BP. My "wrist SpO2 dips" was unresearched and stays flagged.

**ppg_scientist: missing weeks, test-retest.** A missing week is "not evaluable", never negative; too few evaluable weeks gives INSUFFICIENT. Night-time test-retest of wrist-PPG d/a is not in my corpus, so I cannot answer, and PHY-4 is downgraded.

**device_engineer: power budget assumes 25 fps; morphology and PAT need faster sampling.** Correct in principle; I lack a recomputed figure. The audit adds that the device paper's own table omits neural-network inference (47.65 mJ per inference at once a minute is about 215 µA). I ask that the budget be recomputed for a sleep-window morphology burst, and I accept that a one-week-battery watch that must charge overnight would delete my night window. That is a real design conflict for a Class II device.

**device_engineer / clinician: the vascular axis needs overnight ECG+PPG (PSG); spot-check PAT noise is unquantified.** Accepted. [physiologist-15] is a 65-event CVD outcome in a polysomnography cohort, not a wearable design.

**clinician / bayesian_ml: PHY-5 STRONG; personal-only design misses people at high-normal BP.** PHY-5 is MODERATE. I added a population level term and frozen encoder score in v2, and it stays.

**ppg_scientist: PS-25 reframed.** Agreed, and it supports RQ4 rather than benign false alarms.

## 2. Audit response

- **PHY-5 and PHY-10:** STRONG to MODERATE (steps/sleep cohorts are about 6–7k self-selected, EHR-linked; the AIRE-HTN C-index is 0.70, retrospective).
- **Ref 29:** "diagnose ACS" withdrawn. Restated: separated ACS from healthy controls, N=71, spectrum-biased.
- **Ref 22:** "temperature" removed; the study used HR and steps only.
- **Ref 25:** the CCC 0.97–0.98 (RHR) and 0.97–0.99 (HRV) figures are for the best device, Oura, N=13; Polar 0.86/0.82 and Whoop 0.91/0.94.
- **Ref 18:** INDUSTRY-CLAIM; 1,863 analysed, not 2,229. **Ref 19:** entry was corrupted; correct it to Apple 510(k) K250507 (cleared 11 Sep 2025).
- **Ref 15:** 65 events, CVD (not HTN), older MESA sleep cohort.
- **Ref 4:** d/a HR 2.84 is one cohort of 902 men with 124 cases; the b/a index was null (omitted earlier).
- **Ref 1:** 10-s clinic ECG, not wearable; "within-person" is a change-score association only. **Ref 2:** CI 1.01–1.12 borderline, elderly only. **Ref 11:** weight is not wearable physiology. **Ref 28:** "already referred" unverified. **Ref 12:** uncited, removed.

## 3. PROTOTYPE CARD (v3), NOCTURNE

- **Target:** emerging HTN trajectory; no mmHg; no acute claim.
- **Windows:** main-sleep window as primary, with daytime stillness as a separate channel (not pooled); morning spot-check optional.
- **Sensors:** wrist PPG, IMU and skin temperature; weekly cuff; ECG optional for rhythm gate only.
- **Model:** night-anchored, context-residualised change plus a population level term and frozen encoder score; joint posterior; season, ambient temperature, weight and steps as covariates.
- **Persistence:** ≥4 of 6 weeks (one menstrual cycle) as floor; 2 of 3 months as sensitivity; year-one seasonal cap at "watch".
- **Ablations:** night vs all-day; with vs without residualisation; level-only; cuff-only.
- **Output:** three states with confounder tags, "explained by context" ledger.

## 4. Final ranking

| Option | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 | RQ6 | Ev | Eng | Stu | Justification |
|---|---|---|---|---|---|---|---|---|---|---|
| CONFIRM-HTN | 5 | 6 | 7 | 5 | 5 | 6 | 6 | 7 | 8 | Right reference point; little context modelling. |
| EM-ANCHOR | 6 | 6 | 5 | 6 | 7 | 6 | 3 | 5 | 4 | PEP confound unresolved without ICG/SCG. |
| TRACE-PPG | 7 | 6 | 6 | 6 | 8 | 6 | 7 | 8 | 8 | Best data fit and deployment. |
| NOCTURNE (mine) | 7 | 8 | 5 | 8 | 6 | 6 | 5 | 5 | 6 | Strong RQ2/RQ4; I cut RQ3, Ev and Eng: latency (8–12 weeks minimum), season, and battery-charge conflict. |
| BayesTrack-HTN | 8 | 8 | 7 | 6 | 8 | 9 | 6 | 6 | 5 | Strongest formal container; context is thin ("rest-equivalent" pools states). |
| BioVance-Edge | 5 | 5 | 6 | 5 | 7 | 6 | 5 | 8 | 4 | Real numbers but power table incomplete. |
| F2 as stated | 2 | 2 | 1 | 3 | 3 | 3 | 3 | 2 | 2 | Context question matters (exertion, ischaemia) but no HTN mapping. |

## 5. Recommendation

- Build software-only PPG+IMU (+skin temperature) with a hybrid level plus change engine.
- Measure at the main-sleep window, and keep daytime stillness as a separate channel.
- Model season, temperature, weight and steps explicitly; cap year-one warnings at "watch".
- Use a joint posterior, not axis counting.
- Treat wrist vascular timing as a pilot hypothesis needing an ICG/SCG reference.
- Run night-vs-all-day, level-only and cuff-only ablations.
- Never count a missing week as negative.
- No acute stream; rhythm is a gate.

**Verdict on the user's idea.** Physiologically, acute cardiac events and emerging hypertension are different time scales and mechanisms: hypertension is slow vascular and autonomic drift measured over weeks to months; sudden arrest is a rare, abrupt event on a possibly silent substrate. EM signals (ECG) are the right physiology for rhythm, but the challenge asks for a slow-drift model and gives no event labels. A referred-population VA predictor exists (external AUROC 0.948), so F2 is real science but the wrong target for these RQs.

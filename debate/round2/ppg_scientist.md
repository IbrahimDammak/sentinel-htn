# Round 2 — Cross-critique: THE PPG SCIENTIST (`ppg_scientist`)

Conventions:
- [PS-n] refers to my references: the round-1 list in `round1/ppg_scientist.md`, plus PS-30 to PS-33 added below.
- Other debaters' references are cited by their own IDs.
- "My arithmetic" marks numbers I derived from the cited inputs.

## 1. Cross-critique

### 1.1 clinician (CONFIRM-HTN)

**Steelman.** The strongest argument against F2 in round 1 is the clinician's base-rate arithmetic (C9). SCD runs at 36.8–39.7 per 100,000 per year [clinician-31], so even a daily predictor with 99.9% specificity has a PPV of about 0.1%. The clinician is also the only debater who defined `t_ref` operationally, and who tied the minimum lead time (≥3 months) to the guideline lifestyle windows [clinician-2, clinician-5]. I adopt both.

**Attack.**
- *C5 contradicts the card.* The clinician cites "no compelling evidence" that PAT adds accuracy beyond calibration [clinician-11] and calls Aurora "clear-cut negative" [clinician-12]. CONFIRM-HTN still keeps "PAT at rest/sleep".
  - A watch cannot record ECG during sleep, because Lead I needs the opposite finger on the watch [PS-18].
  - Every patch study cited in round 1 lasted ≤14 days [em_engineer-21, physiologist-28].
- *C11 is overstated.* [clinician-23] predicts CVD, not incident hypertension. Its own increment is small: adding the BP trajectory to baseline BP raised the C-index by only 0.0084–0.0192. So level dominates slope even when the trajectory is measured by cuff (§2). The HRV evidence is mixed: positive in [clinician-24], null after adjustment in [PS-28].
- *Lead time depends on the threshold.* The same warning earns more lead time against ESC home ≥135/85 than against AHA ≥130/80, because the higher threshold is crossed later. Making ESC primary therefore inflates RQ3 relative to the only regulatory benchmark, which used ≥130/80 [PS-1].

**Questions.**
1. Does sleep PAT come from a watch or from a patch? Given your own C5, what evidence says it adds anything to a PPG trajectory?
2. If the organisers supply no label, which threshold is primary?
3. What is the E3 budget as a number, in alerts per non-converter person-year?

**Reference use.** The 32.2% in [clinician-34] measures AF recurrence on a *later* patch. It says nothing about alert accuracy, and concurrent PPV was 98.2%.

### 1.2 em_engineer (EM-ANCHOR)

**Steelman.** This is the most honest champion paper. It corrects itself on radar BP, capacitive ECG and skin tone, keeps every modality optional, and pre-registers a kill criterion. Its best idea is that change detection needs within-person *precision*, not accuracy, so a repeatable but inaccurate PAT (ICC >0.7 [em_engineer-11]) could still be useful. The finding that PRV ≠ HRV is also real: SDNN differed by 8.50 ms in cardiovascular patients [em_engineer-29].

**Attack.**
- *C8: repeatable because unresponsive.* The ICC >0.7 comes from the same study in which the device missed the mental-stress BP responses, with calibrated MAE of 10.1–12.9 mmHg [em_engineer-11]. That is the anchoring pattern of PTT devices: 7.4 mmHg of change by cuff vs 1.8 mmHg by device [PS-11]. Change detection needs responsiveness relative to noise, and no cited study measures that over weeks.
- *The signal is the size of the confound (my arithmetic).* Individual PAT–SBP slopes range from −2,946 to −470.64 mmHg/s [em_engineer-24], so a 10 mmHg SBP drift moves PAT by 3.4–21 ms. Mental stress shortens PEP by 14.5 ms [physiologist-13]. In a 2-minute spot-check, months of drift and one stressful morning look alike.
- *The r of −0.82 in C8* [em_engineer-25] comes from BP swings induced in the lab. In the same study, the sign of the PAT–DBP correlation flipped between exercise types.
- *C7 is labelled STRONG* but rests on carotid–femoral **PWV** [em_engineer-27] (RR 1.09, "considerable heterogeneity"). PAT includes PEP and is not PWV, so C7 is MODERATE and is not evidence for PAT.
- *Agreement is double-counted.* PAT↓, nocturnal HR↑ and ECG-HRV↓ share sympathetic drive. PEP–HR coupling is weak at rest (R² 0.06) and strong under physical stress (0.65) [physiologist-13]. In imperfectly controlled windows, one sympathetic shift can count two or three times.

**Questions.**
1. What are PAT's minimum detectable change and standardised response mean over weeks, from a 2-minute spot-check?
2. What is the kill criterion as a margin: which ΔSe(90 d) or ΔAUPRC, with what CI, on which dataset?
3. The spot-check bundles two interventions, a standardised rest ritual and an ECG channel. Will you run the ablation with a PPG-only spot-check performed in the same ritual?

**Reference use.** [em_engineer-11] supports repeatability but refutes responsiveness. [em_engineer-27] measures PWV, not PAT.

### 1.3 physiologist (NOCTURNE)

**Steelman.** Timescale separation is the best RQ4 idea of round 1. Confounders last from days (alcohol [physiologist-23], infection [physiologist-22]) up to a menstrual cycle [physiologist-21], so a real trajectory must outlast all of them. Night anchoring mirrors how cleared devices already gate their input: they analyse only when the user is still [PS-16, PS-18]. The falsifiable ablations (all-day vs night; with vs without residualisation) are exactly what a jury should see.

**Attack.**
- *Coherent is not the same as independent.* PAT on the vascular axis carries PEP, which follows the same sympathetic tone as the autonomic axis (§1.2). "≥2 coherent axes" can therefore be one cause counted twice.
- *PHY-4 and PHY-9 come from the finger, not the wrist.* d/a was measured by finger PPG at a check-up [physiologist-4]. The CCC of 0.97–0.99 came from an Oura ring in 13 people, and Polar's HRV reached only 0.82 [physiologist-25]. No cited study shows wrist second-derivative features during free-living sleep. I share this limit (§4).
- *PHY-5 is labelled STRONG,* but it rests on between-person associations in a cohort that is 84% white and 73% female [PS-26]. MODERATE.

**Questions.**
1. Mean missingness is 49% [bayesian_ml-19]. In the "≥4 of 6" rule, is a missing week counted as negative, skipped, or a reason to abstain?
2. Which pairs of axes have independent errors?
3. What is the night-time test–retest reliability of wrist-PPG d/a?

**Reference use.** [physiologist-15] supports a CVD outcome (65 events, PSG setting), not incident hypertension.

### 1.4 bayesian_ml (BayesTrack-HTN)

**Steelman.** The strongest contribution of round 1 is this evaluation harness, and I adopt it wholesale:
- event-level lead time, with abstentions counted as misses;
- no point-adjust [bayesian_ml-13];
- alarm budgets per person-time;
- a leakage audit before trusting any result far above 41.2/92.3, since emerging hypertension is a *harder* task than prevalent hypertension.

**Attack.**
- *STABLE is a fourth state, and it reads as reassurance.* The challenge defines three states. At the regulatory operating point, a missing notification carries LR− 0.64 and NPV 79.0% [PS-2].
- *C1 transfers the method but not the SNR.* NightSignal fired on RHR rises of ≥4 bpm over 2 nights [bayesian_ml-1]. For incident hypertension, the RHR association is HR 1.06 per 10 bpm, measured between persons [physiologist-2].
- *ACI needs labels.* ACI's guarantee holds over the long run [bayesian_ml-8]. With weekly cuff labels, no individual reaches that long run within 6–12 months.

**Questions.**
1. What NPV must STABLE reach before it is displayed?
2. Warnings in non-converters count as false alarms, yet conversion can happen after follow-up ends. How do you correct precision for this right-censoring?
3. How many events per predictor does the landmark hazard need, and what is the fallback if there are too few?

**Reference use.** [bayesian_ml-29] and [bayesian_ml-11] are correctly flagged as analogies.

### 1.5 device_engineer (BioVance-Edge)

**Steelman.**
- Intended use sets the class: hypertension-risk software is MDR Class IIa, SCA monitoring is IIb/III, and the WCD is Class III via PMA [device_engineer-16, device_engineer-8].
- Wrist radar fails the power budget (690–1290 mW [device_engineer-17]). Cleared radar monitors measure only HR/RR, and only in clinical settings [device_engineer-4, -5, -6].
- The failure modes are quantified: 16% of users lacked ≥15 usable days, and wear time was 77.4% [device_engineer-1, -25].
- A locked model with per-user state is the right regulatory answer.

**Attack.**
- *The preferred card undercuts the MVP.* A software-only product needs no hardware testing [device_engineer-1]. The custom wrist unit with electrodes "may change the predicate", and the paper predicts no RQ metric that would move to justify it.
- *Radar's OSA role (DE-C13) is already done on the wrist, with FDA authorisation* (STRONG, regulatory):
  - Apple's accelerometer-only feature: sensitivity 66.3% and specificity 98.5% for AHI ≥15, with 1,499 enrolled [PS-32].
  - Samsung's wrist-PPG SpO2 feature: 82.7% / 87.7% [PS-33].
  - Sleepiz radar without SpO2, for comparison: 85% / 88% [device_engineer-29].
- *Adherence: I withdraw my own assumption.* Four-week adherence was good in motivated AF patients (MODERATE):
  - median 83.3% for three 1-minute ECGs a day, though full-protocol days were only 16 of 27 [PS-30];
  - 75.0% of patients missed no day of twice-daily thumb ECG [PS-31].

  Adherence over months in asymptomatic users remains unevidenced.

**Questions.**
1. Which RQ metric moves, and by how much, to justify a hardware file?
2. What spot-check adherence do you assume at month 6?
3. What does radar add over [PS-32, PS-33]?

**Reference use.** [device_engineer-26] (post-stroke adults ≥50 y, 14 days) is generalised to hypertension notifications.

## 2. Red-teaming the consensus

**Against the shared architecture.** All six papers put personal-baseline change detection at the core. Yet the best-validated hypertension signals are *level* classifiers with no personal baseline:
- HTNF: one 30-day window with a linear head [PS-1];
- AIRE-HTN: C-index 0.70 [physiologist-20];
- PPG embeddings: AUROC 0.819 [PS-3].

The only cuff-measured trajectory evidence adds 0.0084–0.0192 to the C-index over level [clinician-23]. One PubMed query this session found no 2021–2026 study of within-person wearable trajectories before incident hypertension (WEAK; absence of evidence).

A personal baseline also anchors at disease. By my arithmetic, the NHANES PPV and NPV in [clinician-16] imply that ≈29–30% of undiagnosed US adults already meet ≥130/80, and only 59% of hypertensive women and 49% of hypertensive men are diagnosed [clinician-22]. "Early detection" is therefore largely detection of *prevalent* undiagnosed hypertension, which is a level problem.

**Where personalisation should still win.** HTNF's false positives cluster in the same people. Most notified non-hypertensives were notified in month one, and new notifications fell month over month [PS-1]. Long-term specificity stayed at 86.4% across six windows. If that figure is per-person cumulative, independent windows would have given 61.8% (0.923⁶). A change detector does not flag a person who is atypical but stable.

**Falsifier.** Pre-register three arms at a fixed alarm budget:
- (a) population level: features or embedding plus a linear head per window, no baseline;
- (b) change pipeline;
- (c) level + change.

If (a) matches (c) on Se(90 d) and AUPRC (Δ CI includes 0), and (b) fails in people with elevated BP at enrolment, then the consensus core is wrong and personalisation is only an add-on.

**Against the rejection of F2.** Single-lead ambulatory ECG *does* predict near-term VT. In a retrospective study, the first 24 h of a 14-day recording predicted sustained VT over the next 13 days, with external AUROC 0.948 [physiologist-28]. A single wearable case also showed change-points 4–6 months before SCD [bayesian_ml-6]. F2 is therefore not empty science; it fails *here*, on scoring and on base rate:
- PPV is ≈9–10% in a monitored population [physiologist-28];
- PPV is ≈0.1% for a daily predictor in the general population [clinician-31].

I would reinstate an acute channel if an unselected prospective cohort showed PPV ≥10% at ≤1 false alarm per ~20 user-years, the loss-of-pulse bar [PS-17].

## 3. Positions on D1–D6

| | Position |
|---|---|
| D1 | PPG+IMU is the core. ECG enters only through a 3-arm ablation: passive PPG / PPG spot-check in the same seated ritual / PPG+ECG spot-check. ECG is kept only if arm 3 beats arm 2 by a pre-set margin. Today the PAT signal is the size of the PEP confound (§1.2). |
| D2 | No, for the challenge: radar cannot be tested, it senses mechanical motion as PPG does [physiologist-31], and it has no hypertension-onset data. Its OSA role is covered by authorised wrist features [PS-32, PS-33]. It is a product option only for people who do not wear a watch at night. |
| D3 | No acute model and no second alarm stream. F3 becomes a **rhythm-aware SQI**: irregular rhythm or ectopy makes HRV and morphology windows ineligible (RQ5). Referral goes through already-cleared platform features [clinician-34, PS-16]. |
| D4 | Change detection first, on weekly aggregates, plus the level arm (§2). A thin calibrated risk layer; a hazard model only if event counts allow. k-of-n is tuned to the alarm budget, with n·Δt ≥ one menstrual cycle. Missing weeks are "not evaluable"; too few evaluable weeks → INSUFFICIENT. |
| D5 | The organisers' label first. Otherwise, a 30-day HBPM mean ≥130/80 is primary (comparable to [PS-1]), with ESC ≥135/85 as a pre-registered sensitivity analysis. Report Se(90 d), Se(180 d) and a censoring-aware precision. |
| D6 | Assume PPG-derived features and no ECG. PAT can be tested only cross-sectionally (Aurora-BP, 24 h [PS-9]); radar cannot be tested at all. No EM lead-time claim is possible within the challenge. |

## 4. Concessions

1. **C7 is partly withdrawn.** I claimed the best prediction evidence was accelerometer-based (AUROC 0.74 [PS-19]); that was wrong, because I missed [physiologist-28]. The "unselected people" clause still stands. My rejection of F2 now rests on scoring and base rate, not on an absence of evidence.
2. **C14 is weakened.** The link from HRV to incident hypertension is mixed, not null: positive in [clinician-24] and [physiologist-1] (N=232,587), null after adjustment in [PS-28].
3. **C11 is narrowed.** Its labels were self-reported and cross-sectional, in one cohort, and ECG representations *do* predict incident hypertension [physiologist-20]. C11 is not evidence that PPG beats ECG.
4. **C13 is narrowed (verified).** [PS-27] used UK Biobank waveforms from a PulseTrace PCA2 clinic device, standardised to 100 samples, not free-living wrist PPG.
5. **The persistence rule changes.** "≥2 of 3 thirty-day windows" imposes at least 60 days of latency, against at least 28 days for a 4-of-6 weekly rule. That loses a month against a ≥90-day target. I move to weekly aggregates and keep 30-day windows only for the coverage gate.
6. **C4 gets a narrower scope.** Aurora is negative for absolute and next-day BP, not for within-person change. Anchoring failures also affect PPG devices [PS-10, bayesian_ml-25]. The burden of proof stays on EM.
7. **Adherence.** At 4 weeks, the evidence does not support my implicit claim that spot-checks will not be done [PS-30, PS-31].

## 5. Updated position: TRACE-PPG v2

TRACE-PPG v2 is PPG+IMU notification software on a commodity watch, plus a validated home cuff. It never outputs a BP number. Merged in from the other papers:
- **physiologist:** the main-sleep window, confounder tags, and the night-vs-all-day and no-residualisation ablations;
- **bayesian_ml:** the quality-weighted local-level baseline and the full evaluation harness;
- **clinician:** `t_ref`, sticky warnings, and a nocturnal/masked flag that routes to ABPM;
- **device_engineer:** a locked model with per-user state, edge SQI, and the Class IIa path;
- **em_engineer:** the kill criterion, run as the D1 3-arm ablation.

New in v2: the level arm, weekly k-of-n persistence, and the rhythm-aware SQI. ECG remains an ablation arm, not a component.

## References (new in round 2)

[ppg_scientist-30] van der Velden RMJ et al. "Mobile health adherence for the detection of recurrent recent-onset atrial fibrillation." Heart, 2023;109(1):26–33 (online 2022-12-13). DOI:10.1136/heartjnl-2022-321346 | PMID:36322782 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=36322782&rettype=abstract&retmode=text — Type: RCT sub-analysis (RACE 7 ACWAS, NCT02248753) — Key numbers: 335 recent-onset AF patients after an ED visit (median age 67, 58% male), asked to record a 1-min handheld ECG three times daily for 4 weeks; median adherence 83.3% (IQR 29.9%); median monitoring days 27/27, median full monitoring days 16/27; 85.7% used the device consistently ≥1×/day; older age and a previous paroxysm associated with adherence — Verified: PubMed abstract.

[ppg_scientist-31] Andersen EL et al. "Feasibility of Patient-Managed ECG Recordings to Detect the Time of Atrial Fibrillation Recurrence after Electrical Cardioversion: Results from the PRE-ELECTRIC Study." Cardiology, 2023;148(4):347–352. DOI:10.1159/000530304 | PMID:37040720 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=37040720&rettype=abstract&retmode=text — Type: prospective cohort (observational, single centre) — Key numbers: 200 enrolled, 164 cardioverted; thumb ECG twice daily and on symptoms for 28 days; 123 (75.0%) had no missing recording days, 97.0% ≤3 missing days; 37.3% with recurrence were unaware of it — Verified: PubMed abstract.

[ppg_scientist-32] Apple Inc. "Sleep Apnea Notification Feature (SANF) — 510(k) Summary K240929." FDA CDRH, 2024 (decision 2024-09-13; product code QZW; predicate DEN230041). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf24/K240929.pdf ; https://api.fda.gov/device/510k.json — Type: regulatory — Key numbers: software-only; Apple Watch accelerometer "breathing disturbances" in consecutive 30-day windows; prospective study, 1,499 enrolled (559 AHI <5, 362 mild, 216 moderate, 201 severe, 161 missing HSAT reference); Nox T3s HSAT reference; sensitivity 66.3% [62.2, 70.3] for AHI ≥15; specificity 98.5% [98.0, 99.0] for AHI <15; no false notifications at AHI <5 — Verified: full PDF text extracted with pypdf.

[ppg_scientist-33] Samsung Electronics. "Sleep Apnea Feature — De Novo decision summary DEN230041." FDA CDRH, 2024 (decision 2024-02-06 per openFDA; received 2023-05-31; Class II, product code QZW). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/reviews/DEN230041.pdf ; https://api.fda.gov/device/510k.json — Type: regulatory — Key numbers: OTC; wrist PPG-derived SpO2 plus actigraphy; on-demand assessment requiring two nights within 10 days; eAHI threshold 15/h; 620 enrolled, 47 did not complete; sensitivity 82.7% (167/202) [76.7, 87.6]; specificity 87.7% (235/268) [83.1, 91.4], which did not pass its pre-set acceptance criterion — Verified: full PDF text extracted with pypdf.

*Verification notes on existing references used in new ways this round:* [PS-1] was re-read this session (K250507 PDF, pypdf). It confirms "PPV (prevalence of 31.4%)", long-term specificity of 86.4% over "six discrete non-overlapping 30-day evaluation windows" (N=187), and that "the majority of participants without hypertension who received a notification did so in the first month" with new notifications decreasing month over month. The summary does not define whether 86.4% is per-person cumulative, so the 61.8% comparison in §2 is conditional. [PS-27] was re-read (PMC full text via E-utilities, PMC12630966), which confirmed UK Biobank field 4205 and the PulseTrace PCA2 device. [physiologist-28] was re-read (PubMed abstract, PMID 40157386): retrospective; 247,254 fourteen-day recordings; the first 24 h predicted sustained VT in the subsequent 13 days; external n=20,497.

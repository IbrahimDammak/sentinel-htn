# Round 2 — Cross-critique: THE CLINICIAN (`clinician`)

Other debaters' sources are cited by their own IDs ([PS-n] = ppg_scientist-n), and claim IDs come from their round-1 tables. "My arithmetic" marks numbers I derived. New sources are [clinician-35] to [clinician-39].

## 1. Cross-critique

### 1.1 em_engineer (EM-ANCHOR)

**Steelman.** This was the most honest advocacy of round 1. He kept a ledger of the evidence *against* EM (C9, C10, C13), made a narrow claim (repeatable timing features, not BP) and pre-registered an ablation with a kill criterion. He is also right that PRV is not HRV in clinical populations: PPG underestimated SDNN by 8.50 ms in cardiovascular patients [em_engineer-29].

**Attack.**
- *C8 treats repeatability as validity.* The PAT–SBP r of −0.82 comes from acute exercise-induced BP changes, and the PAT–DBP correlation changed sign with the type of exercise [em_engineer-25]. The ICC >0.7 comes from a system whose calibrated MAE was 10.1–12.9 mmHg and which missed mental-stress responses [em_engineer-11]. A feature that stays stable while BP moves reads as "no drift", which is the worst possible failure for RQ3. In ambulatory data, models using PAT did no better than the calibration cuff plus time of day (N=1,125) [clinician-12, PS-8].
- *C6 matters less for change than for level.* A constant PRV–HRV bias cancels out in D_i(t) = X_i(t) − B_i. Only a bias that varies over time does harm, and its main clinical source is new ectopy or AF. That is a reason to keep ECG for rhythm (D3), not for PAT.
- *The kill criterion cannot be run for lead time.* No paper identified a dataset that combines longitudinal ECG+PPG with incident-hypertension labels. PulseDB is ICU/surgical data [em_engineer-37], and Aurora-BP spans 24 h [PS-9].

**Questions.** (1) On which dataset will the lead-time kill criterion be run? (2) A twice-daily seated spot-check asks the same of the user as home BP monitoring. Given Aurora, why spend that time on PAT rather than a validated cuff? (3) What action follows a PVC-burden flag, and for whom?

**Reference use.** [em_engineer-21] validated PVC burden on a *3-day continuous patch*, not on 2 × 2 min/day, so it does not support C5 as applied. [em_engineer-27] measured PWV, but wrist PAT includes PEP, which halves under physical stress [physiologist-13].

### 1.2 ppg_scientist (TRACE-PPG)

**Steelman.** TRACE-PPG fits the data the jury will supply. It rests on the only cleared system with this purpose [PS-1], and it names the one dataset in which lead time to incident hypertension can be measured (All of Us, 482 incident cases) [PS-26]. Treating skin tone as a *missingness* problem [PS-22] is the right fairness test. New evidence supports him: in a 12-month smartwatch cohort, PPG-derived HRV and activity data, with no ECG, raised AUC from 0.54 to 0.67 [clinician-35].

**Attack.**
- *C11 overstates what the comparison shows for D1.* The 0.819 vs 0.769 comparison uses self-reported hypertension, i.e. *known* and often treated disease [PS-3], so the embedding may learn drug signatures (my inference). ECG embeddings did no better than demographics + HR (0.769 vs 0.770), which shows they add nothing over a baseline, not that PPG beats ECG on emerging disease.
- *C14 is selective.* HELIUS found no association for SDNN or RMSSD [PS-28], but a 232,587-person cohort found HR 1.58 for the lowest vs highest RMSSD quintile [physiologist-1]. The honest summary is "contested".
- *Persistence uses up lead time.* The rule "≥2 of 3 30-day windows" needs about 60 days of drift if windows do not overlap. For a warning to count at 90 days, drift must therefore be visible ≥150 days before t_ref.

**Questions.** (1) How will you show that the PPG-HTN score detects disease rather than treatment? (2) What Se(90 d) is left after the persistence rule? (3) Which TRACE-PPG features can be computed from All of Us Fitbit exports?

**Reference use.** [PS-3] is a cross-sectional study with self-reported labels, yet it is used as evidence that ECG adds nothing to trajectories.

### 1.3 physiologist (NOCTURNE)

**Steelman.** Timescale separation is the best idea of round 1. An alert must outlast every known transient: alcohol (days) [physiologist-23], infection (~3 days) [physiologist-22] and the menstrual cycle [physiologist-21]. Anchoring on the night is also the most clinically aligned choice: night-time SBP was the most informative BP measure for mortality [clinician-18], and office-masked nocturnal hypertension carried HR 1.72 [clinician-21].

**Attack.**
- *The prognostic value of nocturnal BP is borrowed for HR/HRV.* PHY-9 shows that wearables match ECG for nocturnal HR/HRV (N=13) [physiologist-25]. It does not show that they reveal nocturnal hypertension. For nocturnal *BP* the evidence is mixed:
  - A wristband underestimated the nocturnal dip by 14.2 mmHg [clinician-13].
  - Calibrated arm-PPG (N=50) and ring (N=35) devices tracked awake–asleep change with r ≈0.74–0.75, but with limits of agreement near ±10–13 mmHg and a dipping-category κ of 0.58 [clinician-37, clinician-38].
  - The 2025 ESH position paper keeps ABPM as the reference and says wearables "require further validation" [clinician-39].
  
  So there is triage-grade evidence for BP estimates and none for HR/HRV.
- *Requiring several conditions at once may kill sensitivity.* A warning needs ≥4 of 6 weeks per axis *and* ≥2 coherent axes, while per-axis HRs are only 1.06–1.6. No cited study shows the axes moving together before onset.
- *Seasonality.* Ambulatory BP rose 0.61 mmHg per 1 °C fall in temperature [physiologist-24]. A 10 °C seasonal swing therefore gives about 6 mmHg (my arithmetic, assuming linearity; the data are from hypertensives), which is the size of the drift being sought.

**Questions.** (1) What individual-level evidence links wearable nocturnal HR/HRV to nocturnal or incident hypertension? (2) Simulate the sensitivity of the 4-of-6 × 2-axis rule. (3) How will a seasonal rise be told apart from a trajectory during the first year?

**Reference use.** [physiologist-10], a consensus on nocturnal BP, is used to justify night windows for HR/HRV features it does not study.

### 1.4 bayesian_ml (BayesTrack-HTN)

**Steelman.** This is the best evaluation design in the debate, and every team should adopt it:
- lead time is measured per event, and abstention counts as a miss;
- alarm budgets are set per person-time (HTNF specificity was 92.3% per window but 86.4% over six windows [bayesian_ml-4]);
- point-adjust scoring is excluded [bayesian_ml-13];
- measurement density is reported, because T_i depends on when BP happened to be measured.

**Attack.**
- *The model treats as noise what the evidence shows is bias.* In BayesTrack, proxy variance grows with distance from calibration [bayesian_ml-25]. The documented failure, however, is *attenuation*: a PTT device registered 1.8 mmHg of a 7.4 mmHg change from calibration to the 24 h mean [PS-11], and a PPG wristband registered −1.0 of a −19.7 mmHg drug effect (n=3) [clinician-13]. A proxy treated as unbiased but noisier will report "stable" with confidence. The model needs a shrinkage-toward-calibration term.
- *"STABLE" is unsafe as a user message.* At the precedent's operating point, 58.8% of undiagnosed cases get no alert [bayesian_ml-5], and the FDA summary states that the absence of a notification does not mean the absence of hypertension [clinician-15].
- *Synthetic onsets are circular for RQ3*, because the designer chooses the shape of the drift.

**Questions.** (1) How does BayesTrack avoid "stable" when the proxy is anchored to its calibration? (2) Will users ever see "STABLE"? (3) Will lead time on synthetic onsets be kept out of the headline results?

**Reference use.** [bayesian_ml-6] is n=1, with change points found after a known death. It cannot support prospective detection.

### 1.5 device_engineer (BioVance-Edge)

**Steelman.** He shows that intended use sets the regulatory class. Under the MDR, monitoring vital parameters where there is immediate danger is Class IIb, informing decisions that may cause death is Class III, and analysing physiology to prevent illness is Class IIa [device_engineer-16]. The wearable cardioverter-defibrillator is Class III via PMA [device_engineer-8]. This is the strongest case that an acute channel is not "cheap". His ledger of field failures also belongs in every card: 16% of HTNF participants lacked ≥15 usable days [device_engineer-1], and wear-time was 77.4% at 12 months [device_engineer-25].

**Attack.**
- *PAT contradicts DE-C7.* He rejects M7 because calibrated PTT under-tracks change [device_engineer-14], yet spot-check PAT is his core EM feature. Aurora tested PAT features directly and found no gain [PS-8].
- *The radar precedent is misapplied.* C200 and C300 are cleared for clinical settings and give no alarms [device_engineer-5, -6]. They are not a precedent for home use.
- *Missed spot-checks are informative.* They push the least engaged users into permanent abstention.

**Questions.** (1) What evidence shows that raw PAT tracks drift over months? (2) What spot-check completion do you expect at 6 months, and how does the evaluation handle the rest? (3) Without ECG in the organisers' data, what does the week-6 demo add to the score?

**Reference use.** [device_engineer-26] studied post-stroke patients aged ≥50 receiving AF alerts, so it is population-specific, as is my own [clinician-33].

## 2. Red-teaming the consensus

**Against the shared architecture.** Every validated hypertension predictor cited in this debate is *level-based*: HTNF [clinician-15], AIRE-HTN (C 0.70) [physiologist-20] and PPG-age (HR 2.88) [PS-27]. So are the two prospective wearable studies of incident hypertension I found this round:
- a 30-day mean of smartwatch features (N=230, 28 events; AUC 0.67, 95% CI 0.57–0.76) [clinician-35];
- a baseline nomogram from watch-cuff ABPM and HBPM in people with high-normal BP (validation C-index 0.917) [clinician-36].

No debater retrieved a study in which wearable personal-baseline change detection predicts incident hypertension. Our analogues come from infection [PS-25] and prostate cancer [bayesian_ml-29], and adding a BP trajectory to baseline BP raised the C-index by only 0.0084–0.0192 [clinician-23]. A personal baseline is also blind by construction to hypertension that is already present at enrolment (D_i ≈ 0), and that pool is large: 41% of hypertensive women and 51% of hypertensive men were undiagnosed [clinician-22]. Because lead time is scored against *clinical detection*, a level model that finds prevalent undiagnosed hypertension in month 1 may out-score any drift detector.

**Against rejecting F2.** The rejection depends on the population. In a referred population, 14-day single-lead ECG predicted near-term sustained VA with an external AUROC of 0.948 [physiologist-28]. F2 is the wrong target for unselected screening in this challenge, but it is not wrong as science.

**Falsification test.** Pre-register a *strong* level model (demographics + PPG-HTN score + mean nocturnal HR). Then test whether adding change features raises event-level Se(90 d) at a matched false-alarm budget per person-year, with subject-bootstrap CIs and cases prevalent at enrolment reported separately. If the CI of the gain includes zero, personalisation is decoration and the paper must say so.

## 3. Positions on D1–D6

- **D1 (sensor set).** PPG + IMU as the core, with the cuff as the anchor. The best short-term prediction I found came from cuff BP measured by a watch-format sphygmomanometer [clinician-36]. ECG belongs in the design for rhythm confirmation and as a quality/context flag, because AF makes PRV and pulse morphology uninterpretable (clinical reasoning). PAT stays an ablation arm.
- **D2 (bedside radar).** Radar senses skin displacement [physiologist-31], so it is no closer to the hypertension mechanism than PPG. Its clinical case is sleep-breathing context. Nocturnal hypertension clusters with OSA [clinician-39], and a radar screener reached 85% sensitivity and 88% specificity without SpO2 [device_engineer-29]. Wrist SpO2 approximates this. Radar is phase-2 research only.
- **D3 (acute channel).** No user-facing acute alarms, because of the class jump [device_engineer-16] and the costs in care utilisation and anxiety [clinician-32, clinician-33]. Rhythm irregularity should be used as an *internal* RQ4/RQ5 flag.
- **D4 (formulation).** Change detection triggers the warning, and a calibrated landmark logistic model estimates the risk. A full hazard model is under-powered at ~2–5%/yr incidence. Persistence should be ≥4–6 weeks, longer than one menstrual cycle, tuned on the curve of Se(90 d) against false alarms. Season should be a covariate.
- **D5 (reference point).** Score against the organisers' label, but also report lead time under AHA (≥130/80) and ESC (home ≥135/85, office ≥140/90) [clinician-1, clinician-4]. Each should require two qualifying occasions, and measurement density should be reported. Labels differ across studies: [clinician-35] used office ≥140/90 or the start of drug treatment. Meaningful lead time is ≥90 days, an inference from guideline lifestyle windows [clinician-2, clinician-5].
- **D6 (data reality).** Only the PPG, HRV, activity and sleep components can be tested; PAT, ECG-derived HRV, radar and IPG cannot, and the paper should say so. One EM test can be run now, on the ambulatory arm of Aurora-BP: does PAT add to PPG in tracking the night-time dip measured by ABPM? That would still not be evidence about lead time.

## 4. Concessions

1. **Withdrawn: "emerging hypertension is base-rate-friendly."** The PPV of 70.9% was measured at a 31.4% prevalence of *existing* hypertension [clinician-15]. In the cohorts cited this round, incidence runs at ~2–5% per year:
   - 40,268/232,587 over 3.8 y [physiologist-1];
   - 482/6,042 over 4.0 y [PS-26];
   - 124/902 over ≤4 y [physiologist-4].

   By my arithmetic, at a 1–2.5% six-month incidence a warning with 50% sensitivity and 92.3% specificity has a PPV of about 6–14%. Among people with high-normal BP, 21.8% converted within 6 months [clinician-36], and there the same warning reaches about 64%. So *who is monitored* decides what the warning is worth. Confirmed elevated BP is also actionable under ESC 2024 [clinician-2].
2. **Weakened: C11.** The HRV evidence is contested (null in [PS-28]; positive in [physiologist-1] and [clinician-35]), and a trajectory adds little over the level [clinician-23].
3. **Withdrawn: "PAT at rest/sleep" from a watch.** Watch ECG is recorded only on demand [PS-18].
4. **Downgraded: my "nocturnal/masked pattern → ABPM" flag**, now a triage hypothesis. Small studies of calibrated cuffless devices support it [clinician-37, clinician-38]; the HR/HRV evidence does not.
5. **Replaced: my E3 target.** Specificity ≥92% per 30-day window gives way to false alarms per person-year [bayesian_ml-4].

## 5. Updated position: CONFIRM-HTN v2

- **Two lanes, one confirmation loop.**
  - Lane A (level) promotes bayesian_ml's cross-sectional channel: a PPG-HTN score plus demographics finds *existing* undiagnosed hypertension in month 1.
  - Lane B (change) uses night-anchored, context-residualised personal baselines with persistence that outlasts known transients. It is aimed first at people with elevated or high-normal BP, where base rates support a warning.
  - Both lanes end in a 7-day home-cuff series.
- **Output.** Three states, with no user-facing "stable" and never a value in mmHg. "No alert" does not mean "no hypertension".
- **Merged from others:** physiologist's night windows, confounder tags and ablations; bayesian_ml's event-level harness; ppg_scientist's PPG-only core, missingness tests and All of Us data; device_engineer's Class IIa intended use and locked model; em_engineer's pre-registered ablation, wherever it can be tested.

## 6. Round-2 claims

| ID | Claim | Refs | Strength |
|---|---|---|---|
| R2-C1 | A 50%/92.3% warning has a six-month PPV of ≈6–14% at general incidence and ≈64% in high-normal BP | physiologist-1, physiologist-4, PS-26, clinician-36 | MODERATE inputs; derived |
| R2-C2 | Cuffless proxies attenuate BP change | PS-11, clinician-13 | MODERATE |
| R2-C3 | PAT features added no ambulatory BP information beyond the calibration cuff | clinician-12, PS-8 | STRONG (N=1,125; one sponsor) |
| R2-C4 | The prospective wearable predictors of incident HTN found here are level-based; none uses personal change detection | clinician-35, clinician-36, clinician-23 | WEAK–MODERATE (small/single cohorts; absence of evidence) |
| R2-C5 | Calibrated cuffless devices track awake–asleep BP change only moderately; ABPM remains the reference | clinician-37, clinician-38, clinician-39, clinician-13 | WEAK (N=35–50) + guideline |
| R2-C6 | An acute channel raises the regulatory class | device_engineer-16, device_engineer-8 | STRONG (regulatory) |

## 7. References (new this round; all others cited by round-1 IDs)

[clinician-35] Ceyhun ESA, Ceyhun G. "Smartwatch-derived exercise metrics as predictors of early hypertension: a prospective observational study." BMC Cardiovascular Disorders, 2026;26:693. DOI:10.1186/s12872-026-06073-4 | PMID:42252402 | PMCID:PMC13471549 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42252402&rettype=abstract&retmode=text ; https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=13471549&rettype=xml — Type: prospective cohort (single centre, Türkiye) — Key numbers: 230 normotensive adults (office <140/90), aged 30–60, 12-month follow-up; 84.3% Apple Watch Series 9; predictors = mean of the first 30 days of valid data (PPG-derived resting RMSSD, resting HR, MVPA); outcome = office SBP ≥140 and/or DBP ≥90 (mean of last two readings at 12 months) or start of antihypertensive therapy; 28 (12.2%) incident cases; MVPA OR 0.85 per 10 min/day (0.76–0.94); BMI OR 1.12 (1.04–1.21); resting HR OR 1.04 (0.98–1.10, NS); baseline SBP OR 1.14 per 5 mmHg; HRV reported as "OR 0.88 per 5 ms decrease (0.81–0.96)", which contradicts the paper's stated direction (lower HRV = higher risk), so I do not rely on it; AUC 0.54 clinical-only vs 0.67 (0.57–0.76) smartwatch+clinical, out-of-fold cross-validation, no external validation. — Verified: PubMed abstract + PMC full-text XML; Crossref metadata.

[clinician-36] Liu Y, Lv Z, Zhou S, et al. "A smartwatch sphygmomanometer-based model for predicting short-term new-onset hypertension in individuals with high-normal blood pressure: a cohort study." Clinical and Experimental Hypertension, 2024;46(1):2304023. DOI:10.1080/10641963.2024.2304023 | PMID:38346228 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=38346228&rettype=abstract&retmode=text — Type: prospective cohort (ChiCTR2200057354) — Key numbers: people with high-normal BP; training 3,180, validation 1,000; ABPM and HBPM by smartwatch sphygmomanometer; 693 (21.8%) new-onset hypertension within 6 months; nomogram C-index 0.854 (0.843–0.867) training, 0.917 (0.904–0.930) validation; HR 8.415 (middle vs low score), 86.824 (high vs low). Predictor list and outcome definition not given in the abstract. — Verified: PubMed abstract; Crossref metadata.

[clinician-37] Hove C, Seeberg TM, Bøtker-Rasmussen KG, et al. "Nocturnal Blood Pressure Dipping in Adults: A Comparison Between Cuffless and Ambulatory Blood Pressure Monitoring." American Journal of Hypertension, 2026 (online 21 Sep 2026). DOI:10.1093/ajh/hpag115 | PMID:42768439 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42768439&rettype=abstract&retmode=text — Type: validation study — Key numbers: N=50, aged 18–80, office BP 120.1/75.3; PPG-based cuffless device on upper arm vs validated oscillometric 24-h ABPM; awake–asleep change mean difference SBP 1.6 (LoA −8.0 to 11.2) mmHg, DBP 1.2 (−6.7 to 9.1); r 0.75 (SBP), 0.74 (DBP); deviated from the ESH 2023 awake/asleep test (simultaneous readings only); over-representation of normal/low BP; "full validation is required before clinical use". — Verified: PubMed abstract; Crossref.

[clinician-38] Lee SM, Kwon H, Cho B, et al. "Validation of ring-type cuffless blood pressure (BP) monitoring device for detecting awake-asleep BP variations compared to ambulatory BP monitoring device." Hypertension Research, 2026 (online 5 Aug 2026). DOI:10.1038/s41440-026-02759-6 | PMID:42557439 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42557439&rettype=abstract&retmode=text — Type: validation study — Key numbers: ring calibrated ≥1 day before; 35 of 84 recruited selected per the ESH awake/asleep test; awake–asleep SBP change 15.61 ± 8.74 (ABPM) vs 13.87 ± 9.04 mmHg; difference −1.74 ± 6.47 (LoA −14.42 to 10.94) SBP, 0.08 ± 5.84 (LoA −11.37 to 11.53) DBP; r = 0.736; four-category dipping weighted κ = 0.58; only the awake/asleep test performed; senior author reports fees from Sky Labs. — Verified: PubMed abstract; Crossref.

[clinician-39] Parati G, Pengo MF, Avolio A, et al.; ESH Working Group on Blood Pressure Monitoring and Cardiovascular Variability. "Nocturnal blood pressure: pathophysiology, measurement and clinical implications. Position paper of the European Society of Hypertension." Journal of Hypertension, 2025;43(8):1296–1318. DOI:10.1097/HJH.0000000000004053 | PMID:40509714 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=40509714&rettype=abstract&retmode=text — Type: guideline (society position paper) — Key numbers: 24-h ABPM is the reference for nocturnal BP; validated home devices with a nocturnal function may be used; "new cuffless and wearable technologies hold great potential but require further validation"; isolated nocturnal hypertension may be considered a type of masked hypertension; nocturnal hypertension and non-dipping are particularly prevalent with sleep disorders (e.g. OSA), kidney disease and autonomic neuropathy; therapy targeting nocturnal BP remains debated. — Verified: PubMed abstract; Crossref.

*Retrieved but deliberately not cited:* Bhatt BJ et al., Eur Heart J Digit Health 2025 (PMID:40703116), a cuffless 24-h validation study. It was **retracted** (DOI:10.1093/ehjdh/ztag002, Jan 2026), and other debaters should not use it.

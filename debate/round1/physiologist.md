# Round 1 — Position paper: THE PHYSIOLOGIST (`physiologist`)

## 1. Persona

Integrative cardiovascular physiologist (PhD; 15 years of human autonomic, baroreflex, arterial-stiffness and sleep–BP studies). My prior: early hypertension leaves mechanistic footprints, and a wearable model not anchored to physiology and context will learn confounders. My known bias favours hand-crafted features; where evidence favours learned representations I say so (§3.3).

## 2. Reading of the challenge (what actually scores)

All 60 points (RQ1–RQ6) concern one slow process: a person's drift from their own baseline toward hypertension. None rewards detecting an acute cardiac event. RQ4 ("is the physiology changing, or just the situation?") is a physiology question before it is an ML question, and it is where I expect most teams to lose points. The organisers reward the "most credible scientific approach", not the most accurate model.

Timescale is the key physiological fact. The cohort associations below come from follow-ups of years: 3.8 y [physiologist-1], 4.5 y [physiologist-7], 1.66 y [physiologist-11]. Confounders act over hours to weeks. Alcohol-raised nocturnal HR recovers within days [physiologist-23]. Infection signals appear about 3 days before symptoms [physiologist-22]. HR and temperature follow the menstrual cycle [physiologist-21]. **Timescale separation is therefore the backbone of RQ2/RQ4:** a trajectory alert must persist longer than any known transient.

## 3. Verdict on the user's idea: REFRAME (F4 primary, F3 thin secondary). Reject F2 as the scored target.

**Interpretation evaluated.** "Electromagnetic signals" = ECG (bio-potential), bioimpedance/ICG, and RF radar. "Sudden/premature cardiac attack" = sudden cardiac arrest (VT/VF) or acute MI in a free-living population.

### 3.1 F2 as stated does not fit the scoring, and its evidence base is thin for free-living prediction
- Pre-arrest warning symptoms are real but nonspecific and differ by sex. In men, chest pain, dyspnoea and diaphoresis gave ORs of 2.2, 2.2 and 1.7. In women only dyspnoea was significant (OR 2.9). Both groups were compared with EMS-attended controls who had similar symptoms [physiologist-27].
- The best near-term arrhythmia prediction is a deep model on 14-day single-lead patch ECGs: AUROC 0.957 internal and 0.948 external. At 97.0% specificity, sensitivity was 70.6% and 66.1% [physiologist-28]. Prevalence, however, was 0.5% (1,104/247,254 recordings) in a population already referred for monitoring. *My derivation from those numbers:* PPV is about 9–10% at that operating point, so roughly nine false alarms for every true one in an enriched population. In an unselected population it would be worse.
- A smartwatch ECG plus AI can *diagnose* an ongoing acute coronary syndrome (AUROC 0.987 vs control; N = 71) [physiologist-29]. That is detection at the event, not advance warning.

Acute-event prediction is legitimate science for a different challenge. Here it would score near zero on RQ1–RQ3.

### 3.2 Does EM sensing measure anything mechanistically closer to early hypertension than PPG? Partly.
| EM modality | What it physically measures | Closer to HTN mechanism than PPG? |
|---|---|---|
| ECG | Timing of ventricular depolarisation; gives R-peaks for accurate HRV and the start point of PAT | **Yes, for autonomic tone and timing.** Also a learned-representation signal (see 3.3). It adds the PEP confound to PAT. |
| Bioimpedance / ICG | Volume and flow pulses; ICG measures PEP directly [physiologist-13] | **Yes, as a corrector.** PAT − PEP ≈ PTT isolates the vascular component. Graphene-tattoo bioimpedance tracked BP for >300 min (0.2 ± 5.8 mmHg SBP) in a lab setting only [physiologist-30]. |
| mmWave radar | "minute superficial displacements of the skin", i.e. a mechanical pulse [physiologist-31] | **No.** Radar is a contactless mechanical sensor like tonometry or SCG. Multi-site PTT r = 0.75–0.86, but in N = 25 seated, static participants with per-subject calibration [physiologist-31]. |
| MCG / OPM | Cardiac magnetic field (ischaemia) | Not relevant to the HTN trajectory. |

The quantities closest to the mechanism are **vascular (PTT/PWV, pulse-wave morphology) and autonomic (nocturnal HR/HRV)**. Higher PWV predicts incident HTN (pooled RR 1.09, 95% CI 1.05–1.12, with considerable heterogeneity) [physiologist-3]. PPG alone already carries some of this signal: in 902 normotensive men, the lowest quartile of the second-derivative PPG index d/a predicted incident HTN (HR 2.84, 1.58–5.13) [physiologist-4]. EM adds value where it *corrects* PPG (ECG timing, ICG-measured PEP), not where it replaces it.

### 3.3 Where the evidence corrects my bias
A residual CNN on 12-lead ECG (AIRE-HTN) predicted incident HTN with C-index 0.70 internally and externally (UK Biobank). It kept C 0.67–0.72 in people with normal ECGs and added to clinical risk factors (NRI 0.32–0.44) [physiologist-20]. Apple's PPG machine-learning notification feature is 510(k)-cleared [physiologist-19]. Against home BP it reached sensitivity 41% and specificity 92% (N = 2,229) [physiologist-18]. Learned representations carry real information that hand-crafted features may miss. Both results, however, are level-based: neither shows a learned score *tracking within-person change* free of context. My prototype includes a learned axis, and it goes through the same context normalisation as the other axes.

## 4. Proposed prototype: **NOCTURNE**, a night-anchored, context-normalised physiological trajectory engine

**Principle.** Physiology is read only where nature has run a controlled experiment. The primary window is the **main sleep period**, meaning the person's own longest sleep bout rather than clock-night, so shift workers are handled. The secondary window is a **standardised 2-minute seated morning spot-check** (ECG + PPG, with a weekly home cuff reading). All other data describe *context and behaviour* and are never used as trajectory physiology.

**Why nights?** The best consumer wearables reach near-ECG nocturnal accuracy (CCC 0.97–0.98 for RHR, 0.97–0.99 for HRV; 536 nights) [physiologist-25]. PRV–HRV agreement holds at rest but should not be generalised to free-living conditions [physiologist-26]. Nighttime BP is the stronger predictor of events [physiologist-10].

**Feature set: four mechanistic axes with prospective evidence, plus an optional learned axis**
1. **Autonomic axis.** Nocturnal RHR and nocturnal RMSSD/SDNN, as level and slope. Lowest vs highest RMSSD quintile gave HR 1.58 for incident HTN (N = 232,587), and a rise in HRV over time was associated with lower risk [physiologist-1]. RHR: HR 1.06 per 10 bpm (older adults) [physiologist-2].
2. **Vascular axis.** PPG morphology (SDPTG d/a, pulse-wave-analysis stiffness indices) [physiologist-4, physiologist-5]. PAT is used only at matched posture and state (see RQ4). A nocturnal PAT response to respiratory events was associated with incident CVD (HR 1.20 per SD) [physiologist-15].
3. **Sleep–breathing axis.** Sleep duration, sleep regularity and OSA surrogates such as SpO2 dips. Each 1 h increase in the SD of sleep duration gave OR 1.56 (1.35–1.81) for incident HTN. Averaging 5 h vs 6.8 h of sleep gave HR 1.29 [physiologist-7]. Meta-analysis of short sleep: HR 1.07, and 1.11 at <5 h [physiologist-8]. OSA prevalence is 40–80% in hypertension [physiologist-9].
4. **Behavioural-load axis.** Daily steps (hypertension OR 0.92 per +1,000 steps; nonlinear with a plateau at 8,000–9,000) [physiologist-6] and weight change (>10% gain gave HR 1.60 at normal weight, 2.44 overweight, 4.51 obese) [physiologist-11].
5. **Optional learned axis.** A frozen ECG/PPG encoder score (inspired by [physiologist-20]), passed through the same residualisation.

**Coherent evidence patterns (M11).** "Sympathetic drift" = ↑nocturnal RHR + ↓RMSSD + ↓PAT at matched posture. "Vascular drift" = worsening PPG stiffness index + ↓PTT at matched HR. "Sleep–breathing drift" = ↑irregularity + ↑desaturation index. Two or more agreeing axes with no contextual explanation point to physiology. One axis moving alongside a tagged confounder points to the situation.

```
PROTOTYPE CARD — NOCTURNE (night-anchored, context-normalised HTN trajectory engine)
Target (exactly what is detected/predicted, and the clinical reference point):
  P(individual i is on a persistent trajectory toward HTN) + timestamp of first reliable
  warning. Reference = the challenge's longitudinal cuff-BP label; in deployment,
  HBPM/ABPM confirmation. A notification, never a diagnosis [physiologist-17].
Sensors/modalities (part numbers if hardware):
  Wrist PPG + 3-axis IMU + skin temperature (commodity). Single-lead ECG spot-check
  (watch electrode or patch) for PAT and HRV. Validated home cuff weekly (S10). Research
  add-on: ICG for PEP. Part numbers and costs deferred to device_engineer. Radar is not
  required.
Development data (datasets, availability, licence):
  Primary: the challenge dataset. Aurora-BP (public; N=1,125; ECG+PPG+tonometry+ambulatory
  BP [physiologist-16]) to fit the PAT posture/state model. Possible external checks:
  MESA Sleep, the cohort in [physiologist-15]. Access terms unverified by me; team to confirm.
RQ1 Personal baseline:
  Hierarchical Bayesian model (M2). Population prior + person-specific intercepts and
  covariate slopes, learned from the first 4–8 weeks of valid nights per axis. Cold start
  borrows strength from the prior. Deviations are posterior z-scores, not raw differences.
RQ2 Temporal/trajectory:
  Weekly aggregates of the context-residualised D_i(t). Bayesian online change-point
  detection + one-sided CUSUM per axis (M3), plus a slope term in a dynamic linear model
  (M4). An axis "drifts" only if deviation persists ≥4 of 6 consecutive weeks. The
  window exceeds every known transient (days to one menstrual cycle).
RQ3 Early-warning / lead-time strategy:
  Tiered: Watch (1 axis drifting) → Warning (≥2 coherent axes, or 1 axis + rising cuff
  BP). Lead time counts from the first Warning. Hypothesis: autonomic and sleep axes
  move before cuff BP crosses threshold.
RQ4 Context handling:
  (a) Physiology is read only in the main sleep period and the morning seated spot-check.
  (b) Day-level covariates are regressed out, giving "rest-equivalent" values: prior-24 h
  activity load; alcohol (self-report; ~3 bpm nocturnal RHR rise [physiologist-23]);
  acute illness (temperature + RHR/step anomaly pattern [physiologist-22]; affected days
  excluded); menstrual phase from the temperature rhythm [physiologist-21]; ambient
  temperature/season (0.61 mmHg per 1 °C decrease [physiologist-24]); posture matched
  for PAT (SD fell 15–20% when constrained to the calibration posture [physiologist-16]).
  (c) PAT is never interpreted during or after exertion or stress: PEP halves under
  physical stress and falls 16% under mental stress [physiologist-13], and the PAT–DBP
  sign flips across exercise types [physiologist-14].
RQ5 Robustness to missing/noisy data:
  Beat-level SQI on-device. A night counts only with ≥N h of low-motion, SQI-passing
  data. Axes are modelled independently (no ECG → no PAT, the other axes survive).
  Missingness widens posteriors instead of being imputed.
RQ6 Uncertainty & abstention (3-state output):
  SUFFICIENT = posterior P(drift) above threshold AND ≥2 coherent axes AND coverage met.
  INSUFFICIENT = coverage met but posterior uncertain or only 1 axis → keep monitoring.
  POOR QUALITY = <K valid nights in the window or SQI failure → warning suppressed.
  Thresholds are tuned on validation folds for an alarm budget per person-month (M14).
Evidence/explanation output:
  Per-warning ledger: axes moved, magnitude (personal SD units), weeks persisted,
  cross-axis agreement, confounders ruled out, data coverage. E.g. "Nocturnal RHR +4 bpm,
  RMSSD −18% vs baseline for 6 weeks; not explained by activity, illness, cycle phase or
  season; confirm with 7-day home BP."
Edge vs cloud split · power · BOM cost estimate:
  Edge: SQI, beat detection, nightly summaries (only tens of numbers per night leave the
  device; R4). Cloud: hierarchical model + change detection. Power/BOM: deferred to
  device_engineer (commodity wearable + cuff).
Validation plan (metrics A–F, splits, standards):
  E1 subject-wise + forward-chaining splits; metrics A–F as specified by the challenge.
  Falsifiable ablations (E7): (i) all-day features instead of night/spot-check windows;
  (ii) no covariate residualisation; (iii) single axis vs multi-axis agreement.
  Prediction: (i) and (ii) raise false alarms at equal sensitivity. If they do not, my
  core claim fails.
Regulatory / real-world path:
  Notification software, not a BP measurement device. Precedent: Apple HTNF, 510(k)
  K250507, product code SFR "Hypertension Machine Learning-Based Notification Software"
  [physiologist-19]. Any BP-number output would fall under cuffless validation
  requirements [physiologist-17].
Biggest risk + mitigation:
  Population effect sizes are modest (HR 1.06–1.6 per axis). Within-person change may be
  small relative to night-to-night noise. Mitigation: multi-axis agreement, weekly
  aggregation, cuff-BP fusion, abstention. The learned axis is the backup if the
  hand-crafted axes underperform.
Buildable by a student team for the challenge? (4–8 weeks vs later):
  Yes, in 4–8 weeks: window selection, covariate tagging, hierarchical residual model,
  CUSUM/BOCPD, evidence ledger, 3-state logic and ablations on challenge data (raw or
  pre-aggregated). Later: ICG-PEP hardware, own prospective cohort.
```

## 5. Claims table

| ID | Claim | Refs | Strength |
|---|---|---|---|
| PHY-1 | Lower HRV (and a falling HRV over time) precedes incident HTN (10-s ECG, N = 232,587) | 1 | STRONG |
| PHY-2 | Higher RHR is associated with incident HTN (HR 1.06/10 bpm, older adults) | 2 | MODERATE |
| PHY-3 | Arterial stiffness (PWV) predicts incident HTN, with considerable heterogeneity | 3 | MODERATE |
| PHY-4 | A PPG morphology index (SDPTG d/a) predicts incident HTN | 4, 5 | WEAK–MODERATE (single cohort, N = 902 men) |
| PHY-5 | Low wearable-measured steps and sleep irregularity, and short sleep (plus long sleep in one wearable cohort; not in meta-analysis), precede incident HTN | 6, 7, 8 | STRONG (large EHR-linked; mostly white, college-educated) |
| PHY-6 | Weight gain raises short-term HTN risk across BMI groups | 11 | MODERATE (self-reported weight; drug-initiation outcome) |
| PHY-7 | PAT = PEP + PTT. PEP is state-dependent (halves with exercise, −16% with mental stress), and PAT–BP slopes are individual | 12, 13, 14 | MODERATE |
| PHY-8 | Posture, alcohol, illness, menstrual phase and ambient temperature produce shifts comparable to a trajectory signal | 16, 21, 22, 23, 24 | MODERATE |
| PHY-9 | Nocturnal HR/HRV from good wearables nearly matches ECG, so night is a valid measurement window | 25, 26 | WEAK–MODERATE (N = 13, 536 nights) |
| PHY-10 | Learned ECG representations predict incident HTN (C 0.70, externally validated) | 20 | STRONG |
| PHY-11 | PPG-ML HTN notification is regulated but has low sensitivity (41%) and high specificity (92%) | 18, 19 | MODERATE |
| PHY-12 | Radar senses mechanical skin displacement; PTT/BP only in small calibrated lab studies | 31 | WEAK |
| PHY-13 | Pre-SCA symptoms are nonspecific. Near-term VT prediction yields low PPV at low prevalence (PPV is my derivation) | 27, 28 | MODERATE |
| PHY-14 | OSA is highly prevalent in HTN (40–80%) and is a plausible mechanistic driver | 9 | MODERATE (guideline statement) |
| PHY-15 | Cuffless devices are not endorsed for HTN diagnosis | 17 | STRONG (society statement) |

## 6. Anticipated attacks and pre-emptive defence

1. **"Learned models beat your hand-crafted axes."** Partly conceded (PHY-10, PHY-11). But AIRE-HTN is 12-lead, clinic-acquired and level-based. NOCTURNE includes a learned axis and lets ablation E7 decide. If the learned axis wins on forward-chained splits after context residualisation, I accept it.
2. **"EM (radar/bioimpedance) sees more than PPG."** The radar PTT evidence is N = 25, seated, static and per-subject calibrated [physiologist-31]. Bioimpedance BP is a lab study [physiologist-30]. Neither has HTN-onset data. ICG's real value is PEP correction, which I adopt as a research add-on.
3. **"Population HRs of 1.06–1.6 cannot support individual alarms."** Agreed. That is why the design requires multi-axis agreement, persistence, cuff confirmation and abstention.
4. **"People take the watch off at night."** The morning spot-check is the fallback. Otherwise the model abstains rather than reading daytime noise.
5. **"Between-person associations ≠ within-person change."** Valid. Within-person evidence is limited to HRV change [physiologist-1] and weight change [physiologist-11]. This is the main scientific uncertainty.

## 7. Risks and limitations
- Baroreflex sensitivity, which I consider mechanistically important, is excluded: I found no 2021+ prospective wearable evidence for it.
- Skin-tone optical bias (E8), wrist-SpO2 OSA accuracy and wearable non-dipping were not researched here; I defer to ppg_scientist and clinician.
- Cohorts are Asian, US or European. Transfer to Tunisian populations is unverified (R6).
- Lead time is a hypothesis. No cited study measures wearable lead time before clinical HTN.

## 8. References (all retrieved this session)

[physiologist-1] Kang J et al. "Ten-Second Heart Rate Variability, Its Changes Over Time, and the Development of Hypertension." Hypertension, 2022. DOI:10.1161/HYPERTENSIONAHA.121.18589 | PMID:35317608 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35317608&rettype=abstract&retmode=text — Type: prospective cohort — Key numbers: N=232,587 Koreans, mean age 37.6; median FU 3.8 y; 40,268 cases; Q1 vs Q5 RMSSD HR 1.58 (1.52–1.63), SDNN 1.35 (1.30–1.39); stronger in young adults; HRV increase inversely associated (subsample 150,301); 10-s 12-lead ECG, not wearable — Verified: PubMed abstract.

[physiologist-2] Lou S et al. "Association Between Resting Heart Rate and the Risk of Incident Hypertension Among Older Chinese Adults: A Prospective Cohort Study." J Clin Hypertens, 2025. DOI:10.1111/jch.14973 | PMID:39826132 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39826132&rettype=abstract&retmode=text — Type: prospective cohort — Key numbers: N=3,836 (CLHLS); 4.86 y FU; 1,449 cases; HR 1.06 (1.01–1.12) per +10 bpm — Verified: PubMed abstract.

[physiologist-3] Saz-Lara A et al. "Association Between Arterial Stiffness and Blood Pressure Progression With Incident Hypertension: A Systematic Review and Meta-Analysis." Front Cardiovasc Med, 2022. DOI:10.3389/fcvm.2022.798934 | PMID:35224042 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35224042&rettype=abstract&retmode=text — Type: meta-analysis — Key numbers: PWV RR 1.09 (1.05–1.12) for incident HTN in normotensives; SBP RR 1.08; "considerable heterogeneity"; corrigendum exists (DOI:10.3389/fcvm.2022.877296) — Verified: PubMed abstract.

[physiologist-4] Otsuka T et al. "Second Derivative of the Finger Photoplethysmogram Predicts the Risk of Developing Hypertension in Middle-Aged Men." J Atheroscler Thromb, 2025 (epub 2024). DOI:10.5551/jat.65123 | PMID:39168623 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39168623&rettype=abstract&retmode=text — Type: prospective cohort — Key numbers: N=902 normotensive men, mean age 44; ≤4 y FU; 124 cases; lowest vs highest d/a quartile HR 2.84 (1.58–5.13); b/a not significant; finger PPG at checkup, not wearable — Verified: PubMed abstract.

[physiologist-5] Charlton PH et al. "Assessing hemodynamics from the photoplethysmogram to gain insights into vascular age: a review from VascAgeNet." Am J Physiol Heart Circ Physiol, 2022. DOI:10.1152/ajpheart.00392.2021 | PMID:34951543 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34951543&rettype=abstract&retmode=text — Type: review — Key numbers: PPG shape and timing are influenced by vascular aging, arterial stiffness, BP and atherosclerosis; three approach classes (single PPG, multi-PPG PTT, PPG+other PAT) — Verified: PubMed abstract.

[physiologist-6] Master H et al. "Association of step counts over time with the risk of chronic disease in the All of Us Research Program." Nat Med, 2022. DOI:10.1038/s41591-022-02012-w | PMID:36216933 — URL fetched: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9671804/fullTextXML — Type: prospective cohort (EHR-linked Fitbit) — Key numbers: N=6,042; median 4.0 y monitoring; hypertension n=482 incident; OR 0.92 (0.89–0.95) per +1,000 steps/day (n/N=498/4,897); nonlinear, no further reduction above 8,000–9,000 steps; 73% female, 84% white — Verified: full text (Europe PMC).

[physiologist-7] Zheng NS et al. "Sleep patterns and risk of chronic disease as measured by long-term monitoring with commercial wearable devices in the All of Us Research Program." Nat Med, 2024. DOI:10.1038/s41591-024-03155-8 | PMID:39030265 — URL fetched: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11405268/fullTextXML — Type: prospective cohort (EHR-linked Fitbit) — Key numbers: N=6,785; median 4.5 y; sleep irregularity (per hour change in SD of daily sleep duration) → essential HTN OR 1.56 (1.35–1.81); 5 h vs 6.8 h median sleep HR 1.29 (1.09–1.54); 10 h HR 1.61 (1.01–2.58); J-shaped — Verified: full text (Europe PMC).

[physiologist-8] Hosseini K et al. "Association between sleep duration and hypertension incidence: Systematic review and meta-analysis of cohort studies." PLoS One, 2024. DOI:10.1371/journal.pone.0307120 | PMID:39008468 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39008468&rettype=abstract&retmode=text — Type: meta-analysis — Key numbers: 16 cohorts, 1,044,035 people, FU 2.4–18 y; short sleep HR 1.07 (1.06–1.09); <5 h HR 1.11 (1.08–1.14); long sleep not associated — Verified: PubMed abstract.

[physiologist-9] Yeghiazarians Y et al. "Obstructive Sleep Apnea and Cardiovascular Disease: A Scientific Statement From the American Heart Association." Circulation, 2021. DOI:10.1161/CIR.0000000000000988 | PMID:34148375 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34148375&rettype=abstract&retmode=text — Type: guideline/scientific statement — Key numbers: OSA in ~34% of middle-aged men and 17% of women; 40–80% prevalence in hypertension and other CVD; screening recommended in resistant/poorly controlled HTN — Verified: PubMed abstract.

[physiologist-10] Liu J et al. "Asian Expert Consensus on Nocturnal Hypertension Management." Hypertension, 2025. DOI:10.1161/HYPERTENSIONAHA.124.24026 | PMID:40211950 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=40211950&rettype=abstract&retmode=text — Type: consensus statement — Key numbers: "consistent and strong evidence that nighttime blood pressure is a better predictor of target organ damage and cardiovascular events"; nocturnal HTN prevalence higher in Asians — Verified: PubMed abstract.

[physiologist-11] Nielsen LHS et al. "Weight change and short-term risk of hypertension in healthy adults." Eur J Prev Cardiol, 2026 (online ahead of print). DOI:10.1093/eurjpc/zwag356 | PMID:42448322 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42448322&rettype=abstract&retmode=text — Type: retrospective cohort — Key numbers: N=81,954 Danish blood donors; median FU 1.66 y; 5,503 initiated antihypertensives; >10% gain HR 1.60 (1.30–1.96) normal weight, 2.44 (2.02–2.96) overweight, 4.51 (3.57–5.70) obesity; self-reported weight — Verified: PubMed abstract.

[physiologist-12] Finnegan E et al. "Pulse arrival time as a surrogate of blood pressure." Sci Rep, 2021. DOI:10.1038/s41598-021-01358-4 | PMID:34815419 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34815419&rettype=abstract&retmode=text — Type: validation study (lab) — Key numbers: N=30 healthy; phenylephrine; PEP +5.5 ± 4.5 ms vs PTT −16.8 ± 7.5 ms; individual PAT–SBP slope −2946 to −470.64 mmHg/s; calibrated RMSE SBP 5.49 (PAT) vs 4.51 mmHg (PTT); population models ~2× error — Verified: PubMed abstract.

[physiologist-13] Pilz N et al. "The pre-ejection period is a highly stress dependent parameter of paramount importance for pulse-wave-velocity based applications." Front Cardiovasc Med, 2023. DOI:10.3389/fcvm.2023.1138356 | PMID:36873391 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=36873391&rettype=abstract&retmode=text — Type: lab study — Key numbers: N=71 young adults, ICG; PEP rest 104.5 ms, mental stress −16% (90.0 ms), physical stress halves (53.9 ms); PEP–HR R² 0.06/0.29/0.65 — Verified: PubMed abstract.

[physiologist-14] Heimark S et al. "Blood pressure altering method affects correlation with pulse arrival time." Blood Press Monit, 2022. DOI:10.1097/MBP.0000000000000577 | PMID:34855653 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34855653&rettype=abstract&retmode=text — Type: validation study — Key numbers: N=75 (43.7% hypertensive); PAT–SBP r −0.82 ± 0.14; PAT–DBP r 0.25 ± 0.35 full protocol, −0.74 isometric, 0.39 dynamic (sign change) — Verified: PubMed abstract.

[physiologist-15] Kwon Y et al. "Pulse arrival time, a novel sleep cardiovascular marker: the multi-ethnic study of atherosclerosis." Thorax, 2021. DOI:10.1136/thoraxjnl-2020-216399 | PMID:33863828 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=33863828&rettype=abstract&retmode=text — Type: prospective cohort — Key numbers: N=1,407 (MESA Sleep); PAT response to apnoeas/hypopnoeas; 65 incident CVD events over 4.1 y; HR 1.20 (1.02–1.42) per SD — Verified: PubMed abstract.

[physiologist-16] Mieloszyk R et al. "A Comparison of Wearable Tonometry, Photoplethysmography, and Electrocardiography for Cuffless Measurement of Blood Pressure in an Ambulatory Setting." IEEE J Biomed Health Inform, 2022. DOI:10.1109/JBHI.2022.3153259 | PMID:35201992 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35201992&rettype=abstract&retmode=text — Type: validation study + public dataset — Key numbers: N=1,125, 21–85 y; SBP error SD reduced 15–20% when constrained to calibration posture; "first public dataset of ambulatory tonometry and cuffless BP over a 24-hour period" — Verified: PubMed abstract.

[physiologist-17] Stergiou GS et al. "Cuffless blood pressure measuring devices: review and statement by the European Society of Hypertension Working Group on Blood Pressure Monitoring and Cardiovascular Variability." J Hypertens, 2022. DOI:10.1097/HJH.0000000000003224 | PMID:35708294 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35708294&rettype=abstract&retmode=text — Type: guideline/statement — Key numbers: ESH guidelines "do not recommend cuffless devices for the diagnosis and management of hypertension"; validation must address calibration, post-calibration stability, tracking of change, ML — Verified: PubMed abstract.

[physiologist-18] Cohen JB et al. "The Apple Watch for Hypertension Screening." Hypertension, 2026. DOI:10.1161/HYPERTENSIONAHA.125.26031 | PMID:41564145 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC12826266/ — Type: review/commentary (reporting manufacturer validation) — Key numbers: PPG analysed over 30 days; validation N=2,229 without prior HTN vs home BP over 30 days (≥15 days); sensitivity 41%, specificity 92%; "59% of individuals with undiagnosed hypertension … will not be alerted" — Verified: PMC full text via WebFetch.

[physiologist-19] U.S. FDA. "510(k) Premarket Notification K250507 — Hypertension Notification Feature (HTNF), Apple Inc." 2025. — URL fetched: https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID=K250507 — Type: regulatory — Key numbers: decision 11 Sep 2025, Substantially Equivalent; product code SFR "Hypertension Machine Learning-Based Notification Software"; Traditional 510(k); PCCP authorized — Verified: FDA database page (summary PDF could not be parsed).

[physiologist-20] Sau A et al. "Artificial Intelligence-Enhanced Electrocardiography for Prediction of Incident Hypertension." JAMA Cardiol, 2025. DOI:10.1001/jamacardio.2024.4796 | PMID:39745684 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39745684&rettype=abstract&retmode=text — Type: retrospective development + external validation — Key numbers: trained on 1,163,401 ECGs / 189,539 patients (BIDMC); C-index 0.70 (0.69–0.71) BIDMC and UKB (35,806 evaluated); C 0.67–0.72 in no-LVH/normal-ECG; NRI 0.44 / 0.32; 12-lead ECG — Verified: PubMed abstract.

[physiologist-21] Alzueta E et al. "Menstrual Cycle Variations in Wearable-Detected Finger Temperature and Heart Rate, But Not in Sleep Metrics, in Young and Midlife Individuals." J Biol Rhythms, 2024. DOI:10.1177/07487304241265018 | PMID:39108015 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39108015&rettype=abstract&retmode=text — Type: prospective observational — Key numbers: N=116 females (Oura Gen2); temperature oscillation in 96; HR lowest during menses; RMSSD lower late-luteal vs menses (young group); sleep metrics stable — Verified: PubMed abstract.

[physiologist-22] Alavi A et al. "Real-time alerting system for COVID-19 and other stress events using wearable data." Nat Med, 2022. DOI:10.1038/s41591-021-01593-2 | PMID:34845389 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34845389&rettype=abstract&retmode=text — Type: prospective cohort — Key numbers: N=3,318 (84 infected); alerts in 67/84 (80%); median 3 days before symptoms; stress, alcohol, travel also triggered alerts (1.15 vs 3.42 alert-days/person) — Verified: PubMed abstract.

[physiologist-23] Strüven A et al. "The Impact of Alcohol on Sleep Physiology: A Prospective Observational Study on Nocturnal Resting Heart Rate Using Smartwatch Technology." Nutrients, 2025. DOI:10.3390/nu17091470 | PMID:40362779 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=40362779&rettype=abstract&retmode=text — Type: prospective observational — Key numbers: N=40; nocturnal RHR 63.6 → 66.6 bpm with 40–60 g/day alcohol; 64.9 post-exposure — Verified: PubMed abstract.

[physiologist-24] Liu H et al. "Short-Term Effects of Personal-Level Environmental Temperature on Ambulatory Blood Pressure in Patients With Hypertension: A Multicity Panel Study." J Am Heart Assoc, 2025. DOI:10.1161/JAHA.125.045295 | PMID:41120825 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=41120825&rettype=abstract&retmode=text — Type: panel study — Key numbers: N=277 hypertensives, 4 Chinese cities; +0.61 (0.48–0.75) mmHg ambulatory BP per 1 °C decrease; nocturnal decline also associated — Verified: PubMed abstract.

[physiologist-25] Dial MB et al. "Validation of nocturnal resting heart rate and heart rate variability in consumer wearables." Physiol Rep, 2025. DOI:10.14814/phy2.70527 | PMID:40834291 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=40834291&rettype=abstract&retmode=text — Type: validation study — Key numbers: N=13, 536 nights vs ECG; Oura RHR CCC 0.97–0.98; HRV CCC 0.97–0.99; Polar HRV CCC 0.82 — Verified: PubMed abstract.

[physiologist-26] Xu S et al. "Accuracy of Photoplethysmography-Derived Pulse Rate Variability Compared with Electrocardiography-Derived Heart Rate Variability: A Systematic Review and Meta-Analysis." Sensors, 2026. DOI:10.3390/s26165192 | PMID:42655500 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42655500&rettype=abstract&retmode=text — Type: meta-analysis — Key numbers: 43 studies (10 quantitative); pooled absolute standardised error RMSSD 0.188 (0.066–0.309), SDNN 0.134; not generalisable to sleep/exercise/free-living — Verified: PubMed abstract.

[physiologist-27] Reinier K et al. "Warning symptoms associated with imminent sudden cardiac arrest: a population-based case-control study with external validation." Lancet Digit Health, 2023. DOI:10.1016/S2589-7500(23)00147-4 | PMID:37640599 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=37640599&rettype=abstract&retmode=text — Type: case-control with external replication — Key numbers: 411 SCA vs 1,171 EMS controls (discovery); men: chest pain OR 2.2, dyspnoea 2.2, diaphoresis 1.7; women: dyspnoea OR 2.9 only; replication 427 vs 1,238 — Verified: PubMed abstract.

[physiologist-28] Fiorina L et al. "Near-term prediction of sustained ventricular arrhythmias applying artificial intelligence to single-lead ambulatory electrocardiogram." Eur Heart J, 2025. DOI:10.1093/eurheartj/ehaf073 | PMID:40157386 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=40157386&rettype=abstract&retmode=text — Type: retrospective development + external validation — Key numbers: 247,254 14-day recordings; 1,104 (0.5%) sustained VA; AUROC 0.957 internal / 0.948 external; at 97.0% specificity, sensitivity 70.6% / 66.1% (PPV ≈ 9–10% is my derivation assuming overall prevalence) — Verified: PubMed abstract.

[physiologist-29] Choi J et al. "Smartwatch ECG and artificial intelligence in detecting acute coronary syndrome compared to traditional 12-lead ECG." Int J Cardiol Heart Vasc, 2025 (online 2024). DOI:10.1016/j.ijcha.2024.101573 | PMID:39687687 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39687687&rettype=abstract&retmode=text — Type: diagnostic accuracy (small) — Key numbers: 56 ACS + 15 controls; smartwatch 9-lead asynchronous ECG; qACS AUROC 0.987 (smartwatch) vs 0.991 (12-lead); ACS-O(+) vs rest AUROC 0.880 — Verified: PubMed abstract.

[physiologist-30] Kireev D et al. "Continuous cuffless monitoring of arterial blood pressure via graphene bioimpedance tattoos." Nat Nanotechnol, 2022. DOI:10.1038/s41565-022-01145-w | PMID:35725927 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35725927&rettype=abstract&retmode=text — Type: bench/lab — Key numbers: >300 min monitoring; DBP 0.2 ± 4.5, SBP 0.2 ± 5.8 mmHg; N not stated in abstract — Verified: PubMed abstract.

[physiologist-31] Zhu J et al. "Measuring multi-site pulse transit time with an AI-enabled mmWave radar." Nat Commun, 2026. DOI:10.1038/s41467-026-73453-x | PMID:42185285 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=42185285&rettype=abstract&retmode=text and https://pmc.ncbi.nlm.nih.gov/articles/PMC13201791/ — Type: lab validation — Key numbers: 25 participants, 279 sessions, seated static; per-subject calibration (3 recordings); PTT r 0.75–0.86; DBP r 0.90–0.91, SD 4.54–5.20 mmHg; radar senses "minute superficial displacements of the skin" — Verified: PubMed abstract + PMC full text via WebFetch.

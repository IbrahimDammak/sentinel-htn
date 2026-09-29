# Round 1 — Position paper: THE CLINICIAN (`clinician`)

## 1. Persona

Consultant cardiologist and hypertension specialist: 20 years across preventive cardiology, a hypertension clinic with a home/ambulatory BP (HBPM/ABPM) service, and a chest-pain unit; member of a hospital medical-device evaluation committee. My test for any device is simple: *who receives the alert, what confirmatory test do they order, and what happens to the thousands who were alerted wrongly?* My known bias is to dismiss engineering novelty too quickly; I try to separate "the sensor is interesting" from "the clinical target is right".

**Interpretation I evaluate.** "Electromagnetic signals" = primarily bio-potential ECG (the only EM modality with mature clinical evidence), with bioimpedance and RF/radar treated as alternative front-ends. "Sudden or premature cardiac attack" = acute myocardial infarction (MI) and sudden cardiac arrest (SCA).

## 2. Reading of the challenge: what actually scores

All 60 points (RQ1–RQ6) reward one thing: a *personalized, longitudinal, uncertainty-aware warning that an individual is drifting toward hypertension before clinical detection*. Nothing is scored for acute-event detection. So the clinically decisive design question is **what "clinical detection" means**, because RQ3 (lead time) is measured against it.

- **2024 ESC:** office BP is non-elevated <120/70, elevated 120–139/70–89, hypertension ≥140/90 [clinician-2]; out-of-office equivalents for hypertension are home ≥135/85, 24-h ABPM ≥130/80, daytime ≥135/85, night-time ≥120/70 [clinician-1]. STRONG.
- **2025 AHA/ACC:** stage 1 hypertension begins at ≥130/80; HBPM and ABPM are both recommended to confirm the diagnosis [clinician-3, clinician-4, clinician-5]. STRONG.
- **2023 ESH:** hypertension ≥140/90, high-normal 130–139/85–89 [clinician-6]. STRONG.

**Proposed clinical reference point for E2:** `t_ref` = the first date an individual meets hypertension **on validated cuff out-of-office BP** (ESC: home ≥135/85 or 24-h ≥130/80 as primary analysis; AHA ≥130/80 as a sensitivity analysis). If the organisers provide only intermittent office BP, use the first of two consecutive qualifying visits (my operational choice, to avoid single-reading labels), and state that office labels include white-coat misclassification. Out-of-office anchors are the right choice because they track outcomes better: in 59,124 patients, 24-h systolic BP was more strongly associated with death than clinic BP (HR 1.41 vs 1.18 per SD), night-time SBP was the most informative measure, and masked hypertension (not white-coat) carried excess cardiovascular mortality (HR 1.37) [clinician-18]. STRONG.

**Where continuous wearables could legitimately add value (my open-minded prior, now evidence-backed).** Office-based detection misses a lot. Masked hypertension has a pooled prevalence of 18% and RR 1.64 for all-cause mortality [clinician-19]. Nocturnal hypertension affects 45% of the general population and non-dipping 39% (heterogeneous, I²≈97%) [clinician-20]. Office-masked nocturnal hypertension on home monitoring carried an adjusted HR 1.72 for CVD events [clinician-21]. Worldwide, 626 million women and 652 million men aged 30–79 had hypertension in 2019, and only 59% of women and 49% of men had been diagnosed [clinician-22]. The *trajectory*, not just the level, carries risk: an elevated-increasing SBP trajectory across ages 18–39 had HR 3.91 for later CVD [clinician-23]. And modalities in the challenge's data do move before diagnosis: low HRV predicted 4-year incident hypertension in 7,665 normotensive adults [clinician-24]. The challenge's framing is clinically sound.

## 3. Verdict on the user's idea (F2): REFRAME, do not submit as stated

**Does F2 fit the scoring? No.** Four independent reasons:

1. **Wrong disease process.** Type 1 MI is an atherothrombotic event diagnosed with a 12-lead ECG at presentation plus high-sensitivity troponin 0h/1h or 0h/2h algorithms [clinician-25]. SCA is an abrupt arrhythmic collapse, and ventricular fibrillation is "a common cardiac arrest arrhythmia" [clinician-30]. Neither is "a gradual departure from baseline toward hypertension", so RQ1–RQ6 would be scored against a target the system does not model.
2. **Prediction is not proven, only detection or long-horizon stratification.** The strongest AI-ECG result for acute MI is *in-hospital diagnosis*, not prediction: in 24,511 emergency chest-pain patients (occlusion MI prevalence 1.9%), the Queen of Hearts model reached sensitivity 52%, specificity 99% and **PPV 51%** on a 12-lead ECG [clinician-26]. AI-ECG for SCD risk reached AUROC 0.889 internally and 0.820 externally, but in a case-control design with 12-lead ECGs and no imminent-event lead time [clinician-27]. Warning symptoms precede about half of witnessed SCAs, but with modest odds ratios (≈2.2–2.9) and no uniform time window [clinician-29]. MODERATE.
3. **The base rate is fatal for prediction.** SCD incidence in the EU is 36.8–39.7 per 100,000 per year [clinician-31]. *My arithmetic (inputs from [clinician-31])*: a hypothetical daily "imminent SCA" predictor with 90% sensitivity and 99.9% specificity, run on 100,000 people, catches ≈36 events per year at the cost of ≈36,500 false alarms: **PPV ≈0.1%**. Even with an implausible 99.999% daily specificity, PPV is ≈9%. For comparison, Google's loss-of-pulse feature, which *detects* arrest after it has happened rather than predicting it, needed a large engineering program to reach 1 unintentional emergency call per 21.67 user-years, with 67.23% sensitivity in a simulation model [clinician-30].
4. **Emerging hypertension is base-rate-friendly.** Apple's FDA-cleared hypertension notification reached PPV 70.9% at 31.4% prevalence [clinician-15]. The same numbers applied to the NHANES undiagnosed population give PPV 69.1% [clinician-16]. Screening is only viable where the prevalence is high.

**What to keep from the user's idea:** the EM front-end. Single-lead ECG from a watch or patch gives beat timing for HRV and, paired with PPG, pulse arrival time (F4). That is the right reframe: EM signals as *features* in a hypertension-trajectory engine, not as an MI or SCA oracle.

**F3 (hybrid): would dilute the score.** It earns 0 extra points and uses up the ≤5-page budget. It also adds a second alarm stream that competes with E3 (false-alarm burden). The only acute wearable features with real evidence are AF notification (Fitbit: PPV 98.2% for concurrent AF, yet AF was confirmed on the 1-week patch in only 32.2% of those notified [clinician-34]) and loss-of-pulse detection [clinician-30]. Both are detection features already on the market. My recommendation: at most one sentence in "future work".

## 4. Proposed prototype and what a clinically credible output looks like

**Principle: a wearable warning is a referral, not a diagnosis.** Every guideline body says cuffless devices must not be used to diagnose or manage hypertension: ESC 2024 still calls for validation standards for cuffless devices [clinician-1], ESH [clinician-6, clinician-9] and AHA 2025 recommend against them [clinician-4], and the AHA statement says marketed devices "have not yet been adequately vetted for accuracy and efficacy" [clinician-8]. The within-person trend is exactly where cuffless BP is weakest. Validation protocols test accuracy right after calibration, not stability over time [clinician-8]. One wrist device over-read night-time SBP by 15.5 mmHg, under-estimated the nocturnal dip by 14.2 mmHg, and missed a medication-induced fall (−1.0 vs −19.7 mmHg, n=3) [clinician-13]. The 1,125-participant Aurora study was negative [clinician-12]. There is "no compelling evidence" that pulse wave analysis or pulse arrival time add accuracy beyond the calibration data [clinician-11]. **So the system must not output mmHg.** It should output a calibrated *risk-of-transition* with evidence, and route every warning to cuff confirmation. This is a notification claim, the same category as the FDA-cleared Apple feature (21 CFR 870.2380), which is explicitly "not intended to replace traditional methods of diagnosis" [clinician-15].

**Who acts and with which test.** (1) The user performs a structured home-BP series with a validated upper-arm cuff. (2) A primary-care clinician or pharmacist reviews it and orders 24-h ABPM when the evidence ledger points to a nocturnal pattern: nocturnal hypertension is under-diagnosed and daytime HBPM can miss it [clinician-20, clinician-21]. (3) No drug decision is made from wearable data.

**Clinically meaningful lead time: ≥3 months, ideally 6–12.** Guidelines prescribe a lifestyle window before pharmacotherapy: 3 months in ESC 2024 for elevated BP with high CVD risk [clinician-2], and 3–6 months in AHA 2025 for lower-risk stage 1 [clinician-5]. A warning that arrives ≥3–6 months before `t_ref` allows one full lifestyle cycle and a confirmatory HBPM. In my clinical judgement, days-level lead time has no value for hypertension. A years-early warning is only useful if it is precise; otherwise it becomes a labelling harm (see R5).

**Why the false-alarm budget matters clinically.** Apple's feature had 41.2% sensitivity and 92.3% specificity per 30-day window, and specificity in non-hypertensives was 86.4% across six 30-day windows over 2 years [clinician-15]. Over repeated windows, false alarms accumulate. Missed cases cause false reassurance: 59% of undiagnosed hypertension gets no alert [clinician-16, clinician-17]. Wearable users with AF reported more symptom preoccupation and used more AF-specific health care [clinician-33]. The JACC statement warns about psychological harms and "clinically nonactionable data" [clinician-32].

```
PROTOTYPE CARD — CONFIRM-HTN (wearable trajectory screening with a cuff-confirmation loop)
Target (exactly what is detected/predicted, and the clinical reference point):
  Individual probability of transition to confirmed hypertension within the next 3–12 months.
  t_ref = first validated out-of-office confirmation (ESC: home ≥135/85 or 24-h ABPM ≥130/80;
  AHA ≥130/80 sensitivity analysis); if the data carry only office labels: first of two consecutive
  qualifying visits. Secondary flag: "pattern suggests nocturnal/masked hypertension → ABPM".
Sensors/modalities (part numbers if hardware):
  S1 wrist PPG+IMU (commodity watch); S2 single-lead ECG (watch/patch) → HRV, PAT at rest/sleep
  (the user's EM component); S10 validated upper-arm cuff HBPM as sparse anchor/label; S11 context
  (sleep, activity, illness/caffeine/alcohol flags). Specific part numbers deferred to device_engineer.
Development data (datasets, availability, licence):
  Challenge dataset first. Any external set is acceptable only if its BP labels come from a
  validated cuff (not cuffless estimates). Dataset scouting deferred to ML colleagues.
RQ1 Personal baseline: context-stratified robust baseline (median/MAD of nocturnal HR, HRV, PAT,
  resting PPG morphology) over weeks 2–4, shrunk toward a hierarchical population prior (M1+M2).
RQ2 Temporal/trajectory: sequential change detection (CUSUM/BOCPD) on personal residuals; warning
  requires persistence (≥N nights), recurrence and multimodal agreement (M3, M11).
RQ3 Early-warning / lead-time strategy: "sticky" warnings (the first warning counts only if the state
  persists or recurs until t_ref); report median lead time and % of converters warned ≥90 and ≥180 days early.
RQ4 Context handling: compare like with like: sleep and seated-rest windows only; exclude
  post-exercise windows, fever/illness, alcohol nights; circadian phase as covariate (M10).
RQ5 Robustness to missing/noisy data: SQI gating on the edge; minimum-coverage rules per window;
  modality-dropout tests (E5).
RQ6 Uncertainty & abstention (3-state output): Sufficient evidence → "emerging risk: do home BP";
  Insufficient → "keep monitoring" (no message); Poor quality → suppressed + data-quality notice.
Evidence/explanation output: ledger (which signals moved, for how long, in which context, data
  coverage, calibrated probability); never mmHg.
Edge vs cloud split · power · BOM cost estimate: SQI/feature extraction on the watch, trajectory model
  on phone/cloud; BOM/power deferred to device_engineer (commodity watch + validated cuff).
Validation plan (metrics A–F, splits, standards): subject-wise + forward-chaining splits (E1);
  E2 against t_ref above; E3 alarms per non-converter person-year and warning precision, with a target
  at least matching the regulatory precedent (≥92% specificity per 30-day window; ≤~14% of
  non-hypertensives alerted over 2 years [clinician-15]); E4 calibration; E5–E8 incl. skin tone,
  age, BMI (subgroup gaps exist even in cleared devices [clinician-15]).
Regulatory / real-world path: notification-only software (FDA precedent K250507, 21 CFR 870.2380);
  cuffless-BP validation standards are not the relevant bar because no BP value is displayed.
Biggest risk + mitigation: labels based on office BP (white-coat, single readings) make lead time
  meaningless → persistence-based t_ref, out-of-office labels where available, dual ESC/AHA analysis.
Buildable by a student team for the challenge? Yes: in 4–8 weeks, baseline + change detection +
  3-state output + evidence ledger + full E1–E7 evaluation on challenge data. Later: a prospective
  pilot in which each alert triggers home BP and the result feeds back as a label.
```

## 5. Claims table

| ID | Claim | Refs | Strength |
|---|---|---|---|
| C1 | Hypertension is defined by guideline thresholds and confirmed out of office (ESC home ≥135/85, 24-h ≥130/80, night ≥120/70; AHA ≥130/80) | clinician-1, -2, -4, -5, -6 | STRONG |
| C2 | Out-of-office/nocturnal BP predicts mortality better than clinic BP; masked hypertension carries excess risk, white-coat does not | clinician-18, -19, -21 | STRONG |
| C3 | Masked and nocturnal hypertension are common and under-detected | clinician-19, -20, -22 | MODERATE–STRONG |
| C4 | ESC, ESH and AHA do not accept cuffless BP for diagnosis or management; validation does not cover stability or change tracking | clinician-1, -4, -6, -8, -9, -10 | STRONG |
| C5 | Cuffless devices fail to track within-person change (night dip, drug effect); PWA/PAT add no proven accuracy beyond calibration | clinician-11, -12, -13 | MODERATE |
| C6 | A regulator-cleared PPG hypertension *notification* exists: sensitivity 41.2%, specificity 92.3%, PPV 70.9% at 31.4% prevalence | clinician-15, -16 | STRONG |
| C7 | AI-ECG for acute MI is ED diagnosis (PPV 51% at 1.9% prevalence), not wearable prediction | clinician-25, -26 | MODERATE |
| C8 | SCA prediction evidence is case-control or symptom-based with modest ORs; no validated imminent-event lead time | clinician-27, -29 | MODERATE |
| C9 | At SCD incidence ≈40/100,000/yr, a daily predictor has PPV ≈0.1% (arithmetic) | clinician-31 | STRONG input, derived |
| C10 | Wearable alarms carry psychological and utilisation costs; missed alerts cause false reassurance | clinician-16, -17, -32, -33 | MODERATE |
| C11 | BP trajectory and HRV carry pre-diagnostic signal | clinician-23, -24 | MODERATE |
| C12 | A lead time of ≥3 months matches the guideline lifestyle window | clinician-2, -5 | MODERATE (inference from guidelines) |

## 6. Anticipated attacks and pre-emptive defence

- **"You are killing engineering novelty (radar, MCG)."** No. I endorse EM sensing as a front-end (F4). My objection is to the *target*. Radar-derived HRV or bioimpedance PTT fit well into the ledger if they beat PPG on SQI.
- **"AI-ECG predicts SCD with AUROC 0.82–0.89."** Those are 12-lead, case-control risk-stratification results with no imminent lead time [clinician-27]. AUROC does not survive a 1-per-million-per-day base rate (C9).
- **"Loss-of-pulse detection proves acute wearables work."** Conceded for *detection*, at 1 false call per 21.67 user-years [clinician-30]. It is not prediction, it is not scored, and it is already a product.
- **"Guidelines reject cuffless, so the challenge is invalid."** Screening and notification are a different bar from measurement. The FDA cleared a PPG notification on that basis [clinician-15]. CONFIRM-HTN outputs no BP value and hands off to cuff confirmation.
- **"Personal baselines beat HBPM labels."** HBPM/ABPM are the outcome-validated reference [clinician-18]. A baseline without cuff anchoring cannot tell drift from disease [clinician-13].
- **"3 months is arbitrary."** It is tied to guideline lifestyle windows [clinician-2, clinician-5], and I propose reporting the full lead-time distribution.

## 7. Risks and limitations of my position

- The challenge labels may be office-based. My `t_ref` then partly measures white-coat noise, and lead-time claims weaken.
- Evidence that treating nocturnal hypertension specifically improves outcomes is still limited [clinician-20].
- The regulatory precedent comes from one manufacturer with a 30-day design. Its numbers are a benchmark, not a ceiling.
- Access to ABPM is limited [clinician-4], which matters for Tunisian/LMIC deployment (R6). HBPM must be the default confirmation step.
- The "≥3 months" meaningful-lead-time threshold is my inference from guideline windows, not a trial-derived number.
- My bias: I may undervalue the precision gains from multimodal EM sensing. Round 2 should test that with evidence.

## 8. References

[clinician-1] McEvoy JW et al. "2024 ESC Guidelines for the management of elevated blood pressure and hypertension." European Heart Journal, 2024. DOI:10.1093/eurheartj/ehae178 | PMID:39210715 — URL fetched: https://academic.oup.com/eurheartj/article/45/38/3912/7741010 — Type: guideline — Key numbers: Table 5: hypertension = office ≥140/90, home ≥135/85, 24-h ABPM ≥130/80, daytime ≥135/85, night-time ≥120/70; elevated = office 120/70–<140/90, home 120/70–<135/85, 24-h 115/65–<130/80; masked/white-coat definitions; "Validation standards and methodology need to be developed and implemented for novel BP measurement devices that are non-occlusive and 'cuffless'." — Verified: partial full text via WebFetch (OUP page) + Europe PMC record.

[clinician-2] McCarthy CP, Bruno RM, McEvoy JW, Touyz RM. "2024 ESC Guidelines for the management of elevated blood pressure and hypertension: what is new in pharmacotherapy?" European Heart Journal – Cardiovascular Pharmacotherapy, 2025 (issue; online 2024). DOI:10.1093/ehjcvp/pvae084 | PMID:39439212 — URL fetched: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11805683/fullTextXML — Type: review (guideline summary by guideline authors) — Key numbers: non-elevated <120/70, elevated 120–139/70–89, hypertension ≥140/90 (office); drug therapy for elevated BP + high CVD risk with repeated BP ≥130/80 "despite 3 months of lifestyle measures (Class I)"; SBP target 120–129 mmHg. — Verified: Europe PMC full text.

[clinician-3] Jones DW, Ferdinand KC, Taler SJ, et al. "2025 AHA/ACC/AANP/AAPA/ABC/ACCP/ACPM/AGS/AMA/ASPC/NMA/PCNA/SGIM Guideline for the Prevention, Detection, Evaluation and Management of High Blood Pressure in Adults: A Report of the American College of Cardiology/American Heart Association Joint Committee on Clinical Practice Guidelines." Hypertension, 2025. DOI:10.1161/HYP.0000000000000249 | PMID:40811516 — URL fetched: https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1161/hyp.0000000000000249 (full text at ahajournals.org returned HTTP 403) — Type: guideline — Key numbers: abstract only (replaces 2017 guideline; literature search Dec 2023–Jun 2024); specific content cited via [clinician-4] and [clinician-5]. — Verified: Europe PMC record/abstract.

[clinician-4] Brown C, Clark D, Jones DW. "Updates in the 2025 AHA/ACC Hypertension Guideline." Current Hypertension Reports, 2026. DOI:10.1007/s11906-026-01372-9 | PMID:41843050 — URL fetched: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12995957/fullTextXML — Type: review (co-authored by the guideline chair) — Key numbers: "Both HBPM and ABPM are recommended for confirming hypertension diagnosis"; "Given mixed evidence and lack of external validations on cuffless BP devices, they are not recommended for diagnosing or treating elevated BP"; "disparities in access to ABPM limit widespread implementation". — Verified: Europe PMC full text.

[clinician-5] Sayed A, Peterson ED, Navar AM. "Implications of the 2025 AHA/ACC high blood pressure guidelines on the initiation and intensification of blood pressure-lowering medications among US adults." American Journal of Preventive Cardiology, 2026. DOI:10.1016/j.ajpc.2025.101400 | PMID:41767443 — URL fetched: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC12946893/fullTextXML — Type: retrospective (NHANES analysis) — Key numbers: 2025 initiation: BP ≥140/90, or ≥130/80 with PREVENT ≥7.5%, diabetes, CKD or CVD; lower-risk stage 1 (≥130/80) treated "if 3–6 months of lifestyle modification does not reduce BP to <130/80"; up to 19.0 million additional US adults eligible. — Verified: Europe PMC full text.

[clinician-6] Vemu PL, Yang E, Ebinger JE, et al. "Moving Toward a Consensus." (subtitle: Comparison of the 2023 ESH and 2017 ACC/AHA Hypertension Guidelines; Crossref lists the main title only) JACC: Advances, 2024. DOI:10.1016/j.jacadv.2024.101230 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC11399577/ — Type: review — Key numbers: "ESH defines hypertension as BP ≥140/90 mm Hg"; high-normal 130–139/85–89; "The ESH guideline recommends against the use of cuffless devices…" (incompletely validated technologies, no standard protocols, need for cuff calibration). — Verified: PMC full text via WebFetch.

[clinician-8] Cohen JB, Byfield RL, Hardy ST, et al. "Cuffless Devices for the Measurement of Blood Pressure: A Scientific Statement From the American Heart Association." Hypertension, 2026. DOI:10.1161/HYP.0000000000000254 | PMID:41376592 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC13335599/ — Type: guideline (scientific statement) — Key numbers: the devices "have not yet been adequately vetted for accuracy and efficacy"; validation protocols "do not address stability over time"; poor tracking of exercise-, sleep- and treatment-induced BP changes; ISO 81060-3:2022 uses an intra-arterial reference (OR/ICU); ESH 2023 six-test protocol; nocturnal BP is a *potential* future use. — Verified: Europe PMC abstract + PMC full text via WebFetch.

[clinician-9] Stergiou GS, Mukkamala R, Avolio A, et al. "Cuffless blood pressure measuring devices: review and statement by the European Society of Hypertension Working Group on Blood Pressure Monitoring and Cardiovascular Variability." Journal of Hypertension, 2022. DOI:10.1097/HJH.0000000000003224 | PMID:35708294 — URL fetched: Europe PMC REST search (AUTH:"Stergiou GS" AND TITLE:cuffless) — Type: guideline (society statement) — Key numbers: ESH guidelines "do not recommend cuffless devices for the diagnosis and management of hypertension"; validation must address calibration, post-calibration stability, tracking of BP changes, and machine learning. — Verified: Europe PMC abstract.

[clinician-10] Stergiou GS, Avolio AP, Palatini P, et al. "European Society of Hypertension recommendations for the validation of cuffless blood pressure measuring devices: European Society of Hypertension Working Group on Blood Pressure Monitoring and Cardiovascular Variability." Journal of Hypertension, 2023. DOI:10.1097/HJH.0000000000003483 | PMID:37303198 — URL fetched: Europe PMC REST search (as above) — Type: standard (society validation protocol) — Key numbers: six tests: static, device position, treatment, awake/asleep, exercise, recalibration. — Verified: Europe PMC abstract.

[clinician-11] Mukkamala R, Shroff SG, Kyriakoulis KG, Avolio AP, Stergiou GS. "Cuffless Blood Pressure Measurement: Where Do We Actually Stand?" Hypertension, 2025. DOI:10.1161/HYPERTENSIONAHA.125.24822 | PMID:40231350 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC12331212/ — Type: review — Key numbers: "no compelling evidence that pulse wave analysis and pulse arrival time can provide significant added value in BP measurement accuracy beyond the cuff BP or demographic data for calibration"; ISO 81060-3 targets critical-care devices; ISO 81060-7 (hypertension use) under development; CE-marked devices need cuff calibration (e.g., Samsung every 28 days; Aktiia monthly, or demographic calibration). — Verified: abstract + PMC full text via WebFetch.

[clinician-12] Mukkamala R, Shroff SG, Landry C, Kyriakoulis KG, Avolio AP, Stergiou GS. "The Microsoft Research Aurora Project: Important Findings on Cuffless Blood Pressure Measurement." Hypertension, 2023. DOI:10.1161/HYPERTENSIONAHA.122.20410 | PMID:36458550 — URL fetched: Europe PMC REST search — Type: review (of a 1,125-participant evaluation) — Key numbers: "The overall results from 1125 participants were clear-cut negative" for PWA and PWA+PAT devices. — Verified: Europe PMC abstract.

[clinician-13] Tan I, Gnanenthiran SR, Chan J, et al. "Evaluation of the ability of a commercially available cuffless wearable device to track blood pressure changes." Journal of Hypertension, 2023. DOI:10.1097/HJH.0000000000003428 | PMID:37016925 — URL fetched: Europe PMC REST search — Type: validation study — Key numbers: n=41, device worn 6–12 days vs 24-h ABPM; night-time SBP +15.5 mmHg (11.8–19.1); SBP dip under-estimated by 14.2 mmHg; medication-induced change −1.0/−0.8 (device) vs −19.7/−11.5 mmHg (HBPM), n=3. — Verified: Europe PMC abstract.

[clinician-15] Apple Inc. / U.S. FDA. "Hypertension Notification Feature (HTNF)" 510(k) K250507 — Substantial Equivalence letter and 510(k) Summary, cleared September 11, 2025; 21 CFR 870.2380 (Cardiovascular Machine Learning-Based Notification Software), product code SFR (updated from QXO). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250507.pdf — Type: regulatory — Key numbers: OTC, adults ≥22 without prior diagnosis; "not intended to replace traditional methods of diagnosis… The absence of a notification does not indicate the absence of hypertension"; reference = HBPM average ≥130/80 over 30 days; 2,229 enrolled, 1,863 analysed; sensitivity 41.2% (37.2–45.3), specificity 92.3% (90.6–93.7), PPV 70.9% at prevalence 31.4%; stage 2 sensitivity 53.7%; long-term specificity in non-hypertensives 86.4% (80.2–92.5) across six 30-day windows over 2 years (N=187); sensitivity risk ratio 0.69 for age <60. — Verified: PDF text extracted with pdftotext.

[clinician-16] Cohen JB, Addo DK, Jacobs JA, et al. "Impact of a Smartwatch Hypertension Notification Feature for Population Screening." JAMA, 2026. DOI:10.1001/jama.2025.26925 | PMID:41661624 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC12887835/ — Type: retrospective (cross-sectional NHANES 2017–2020 modelling) — Key numbers: 3,983 participants ≈127 million US adults unaware of hypertension; PPV 69.1% (63.3–74.9), NPV 79.0%; age <30: pre-test 0.14 → 0.47 with alert; age ≥60: 0.45 → 0.81, and 0.34 without alert; warns of "false reassurance". — Verified: PubMed record + PMC full text via WebFetch.

[clinician-17] Cohen JB, Brady TM, Juraschek SP, Picone DS, Yang E, Schutte AE. "Apple Watch for Hypertension Screening." Hypertension, 2026. DOI:10.1161/HYPERTENSIONAHA.125.26031 | PMID:41564145 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC12826266/ — Type: review (commentary) — Key numbers: "59% of individuals with undiagnosed hypertension wearing the Apple Watch will not be alerted"; risk of "false reassurance, deferred care, and delayed diagnosis". — Verified: PMC full text via WebFetch.

[clinician-18] Staplin N, de la Sierra A, Ruilope LM, et al. "Relationship between clinic and ambulatory blood pressure and mortality: an observational cohort study in 59 124 patients." Lancet, 2023. DOI:10.1016/S0140-6736(23)00733-X | PMID:37156250 — URL fetched: Europe PMC REST search (DOI query) — Type: prospective cohort (registry) — Key numbers: 59,124 patients, median 9.7 y; 24-h SBP HR 1.41 per SD vs clinic 1.18; night-time SBP informativeness 591% (all-cause) and 604% (CV) of clinic; masked HTN all-cause HR 1.24 (1.12–1.37), CV HR 1.37 (1.15–1.63); white-coat not associated with excess risk. — Verified: Europe PMC abstract.

[clinician-19] Zhu H, Li J, Li L, et al. "Prevalence and Cardio-Renal Comorbidities of Masked Hypertension: A Meta-Analysis." Journal of Evidence-Based Medicine, 2024. DOI:10.1111/jebm.12672 | PMID:39722158 — URL fetched: Europe PMC REST search — Type: meta-analysis — Key numbers: 26 studies, 129,061 participants, median follow-up 7.38 y; prevalence 18% (15–21%); all-cause mortality RR 1.64 (1.32–2.04); incident CVD RR 1.57 (1.45–1.69). — Verified: Europe PMC abstract.

[clinician-20] Show KL, Lim ZY, Teong CCY, et al. "Global prevalence of nocturnal hypertension: systematic review and meta-analysis." BMC Public Health, 2026. DOI:10.1186/s12889-026-28066-w | PMID:42265642 — URL fetched: Europe PMC REST search (DOI query) — Type: meta-analysis — Key numbers: 449 studies; nocturnal hypertension 45% (39–51, I²=97.4%) in the general population; isolated nocturnal 23%; non-dipping 39%; "Evidence demonstrating that targeted reduction of nocturnal BP improves long-term cardiovascular outcomes is still limited." — Verified: Europe PMC abstract.

[clinician-21] Fujiwara T, Hoshide S, Sheppard JP, McManus RJ, Kario K. "Cardiovascular Events Risk in Office-Masked Nocturnal Hypertension Defined by Home Blood Pressure Monitoring." JACC: Advances, 2024. DOI:10.1016/j.jacadv.2024.101352 | PMID:39600985 — URL fetched: Europe PMC REST search (DOI query) — Type: prospective cohort — Key numbers: 2,545 high-risk Japanese participants, median 7.8 y, 152 CVD events; office-masked nocturnal HTN 23.2%; adjusted HR 1.72 (1.01–2.92) vs nocturnal normotension, after adjustment for daytime home BP. — Verified: Europe PMC abstract.

[clinician-22] NCD Risk Factor Collaboration (NCD-RisC). "Worldwide trends in hypertension prevalence and progress in treatment and control from 1990 to 2019: a pooled analysis of 1201 population-representative studies with 104 million participants." Lancet, 2021. DOI:10.1016/S0140-6736(21)01330-1 | PMID:34450083 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34450083&rettype=abstract&retmode=text — Type: meta-analysis (pooled population studies) — Key numbers: 626 million women and 652 million men aged 30–79 with hypertension in 2019; 59% of women and 49% of men previously diagnosed; control 23% and 18%. — Verified: PubMed abstract.

[clinician-23] Xia M, An J, Fischer H, Allen NB, Xanthakis V, Zhang Y. "Blood Pressure Trajectories During Young Adulthood and Cardiovascular Events in Later Life." American Journal of Hypertension, 2024. DOI:10.1093/ajh/hpae126 | PMID:39325713 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=39325713&rettype=abstract&retmode=text — Type: prospective cohort (pooled CARDIA + Framingham) — Key numbers: 6,579 participants; elevated-increasing vs low-stable SBP trajectory (ages 18–39): composite CVD HR 3.91 (2.38–6.41); adding trajectory to baseline BP raised C-index by 0.0084–0.0192. — Verified: PubMed abstract.

[clinician-24] Hoshi RA, Santos IS, Dantas EM, et al. "Reduced heart-rate variability and increased risk of hypertension-a prospective study of the ELSA-Brasil." Journal of Human Hypertension, 2021. DOI:10.1038/s41371-020-00460-w | PMID:33462386 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=33462386&rettype=abstract&retmode=text — Type: prospective cohort — Key numbers: 7,665 adults free of hypertension, 4-year follow-up; low values of all HRV indices associated with higher incident hypertension after full adjustment (issue 2021; epub 18 Jan 2021). — Verified: PubMed abstract.

[clinician-25] Byrne RA, Rossello X, Coughlan JJ, et al. "2023 ESC Guidelines for the management of acute coronary syndromes." European Heart Journal, 2023. DOI:10.1093/eurheartj/ehad191 | PMID:37622654 — URL fetched: https://academic.oup.com/eurheartj/article/44/38/3720/7243210 — Type: guideline — Key numbers: 12-lead ECG at presentation for triage; hs-troponin 0h/1h or 0h/2h rule-in/rule-out algorithms; Type 1 MI = atherothrombotic event. — Verified: partial full text via WebFetch + PubMed esummary.

[clinician-26] Lindow T, Nyström A, Forberg JL, et al. "Improved Detection of Acute Coronary Occlusion Myocardial Infarction by an Artificial Intelligence Electrocardiogram Model in Swedish Emergency Departments." Journal of the American College of Emergency Physicians Open, 2026. DOI:10.1016/j.acepjo.2026.100473 | PMID:42614578 — URL fetched: Europe PMC REST search — Type: retrospective — Key numbers: 24,511 ED chest-pain patients, OMI 467 (1.9%); Queen of Hearts sensitivity 52% (47–57), specificity 99%, PPV 51% (47–54), NPV 99%; STEMI criteria sensitivity 23%, PPV 17%. — Verified: Europe PMC abstract.

[clinician-27] Holmstrom L, Chugh H, Nakamura K, et al. "An ECG-based artificial intelligence model for assessment of sudden cardiac death risk." Communications Medicine, 2024. DOI:10.1038/s43856-024-00451-9 | PMID:38413711 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=38413711&rettype=abstract&retmode=text — Type: retrospective (case-control) — Key numbers: 1,827 pre-arrest 12-lead ECGs from 1,796 SCD cases; controls 1,342 ECGs, ≥50% with CAD; AUROC 0.889 (0.861–0.917) internal, 0.820 external (714 cases); conventional ECG score 0.712/0.743. — Verified: PubMed abstract.

[clinician-29] Reinier K, Dizon B, Chugh H, et al. "Warning symptoms associated with imminent sudden cardiac arrest: a population-based case-control study with external validation." Lancet Digital Health, 2023. DOI:10.1016/S2589-7500(23)00147-4 | PMID:37640599 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC10746352/ and PubMed efetch — Type: retrospective (case-control) — Key numbers: 411 SCA cases vs 1,171 EMS controls; 411/823 (50%) witnessed SCAs had an inclusion symptom; dyspnoea 41% vs 22%; men chest pain OR 2.2, dyspnoea OR 2.2; women dyspnoea OR 2.9; no uniform pre-arrest time window (EMS narrative). — Verified: PubMed abstract + PMC full text via WebFetch.

[clinician-30] Shah K, Wang A, Chen Y, et al. "Automated loss of pulse detection on a consumer smartwatch." Nature, 2025. DOI:10.1038/s41586-025-08810-9 | PMID:40010378 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=40010378&rettype=abstract&retmode=text — Type: prospective validation study (industry authors) — Key numbers: 1 unintentional emergency call per 21.67 user-years across two prospective studies; sensitivity 67.23% (64.32–70.05) in a prospective arterial-occlusion simulation; PPG pulselessness from ventricular fibrillation resembles occlusion-induced pulselessness. — Verified: PubMed abstract.

[clinician-31] Empana JP, Lerner I, Valentin E, et al. "Incidence of Sudden Cardiac Death in the European Union." Journal of the American College of Cardiology, 2022. DOI:10.1016/j.jacc.2022.02.041 | PMID:35512862 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35512862&rettype=abstract&retmode=text — Type: prospective cohort (4 population registries) — Key numbers: SCD 36.8–39.7 per 100,000/year; ≈249,538 SCD/year in the EU; OHCA 47.8–57.9 per 100,000/year. — Verified: PubMed abstract.

[clinician-32] Varma N, Han JK, Passman R, et al. "Promises and Perils of Consumer Mobile Technologies in Cardiovascular Care: JACC Scientific Statement." Journal of the American College of Cardiology, 2024. DOI:10.1016/j.jacc.2023.11.024 | PMID:38296406 — URL fetched: PubMed efetch (Rosman L[au] query) — Type: guideline (scientific statement) — Key numbers: challenges include "questionable data reliability, potential misinterpretation of information, unintended psychological impacts, and an influx of clinically nonactionable data that may overburden the health care system". — Verified: PubMed abstract.

[clinician-33] Rosman L, Lampert R, Zhuo S, et al. "Wearable Devices, Health Care Use, and Psychological Well-Being in Patients With Atrial Fibrillation." Journal of the American Heart Association, 2024. DOI:10.1161/JAHA.123.033750 — URL fetched: PubMed efetch (Rosman L[au] query) — Type: retrospective (propensity-matched) — Key numbers: 172 AF patients, 83 wearable users; more symptom monitoring/preoccupation (P=0.03); 20% of users anxious and always contacted doctors after irregular-rhythm notifications; higher AF-specific health care use (P=0.04). — Verified: PubMed abstract.

[clinician-34] Lubitz SA, Faranesh AZ, Selvaggi C, et al. "Detection of Atrial Fibrillation in a Large Population Using Wearable Devices: The Fitbit Heart Study." Circulation, 2022. DOI:10.1161/CIRCULATIONAHA.122.060291 | PMID:36148649 — URL fetched: PubMed efetch ("Fitbit Heart Study"[ti]) — Type: prospective (remote trial) — Key numbers: 455,699 enrolled; 4,728 with irregular-rhythm detection; AF on ECG patch in 340/1,057 (32.2%); PPV of IHRD during patch for concurrent AF 98.2% (95.5–99.5). — Verified: PubMed abstract.

*Numbering gaps (clinician-7, -14, -28) are intentional: these references were retrieved but dropped during editing, and the IDs were kept stable.*

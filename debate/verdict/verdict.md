# Chair's Verdict — BioVance AIoT Challenge × "EM signals for sudden cardiac attack"

`PS-n` = `ppg_scientist-n`. No new research.

## 1. Consensus and unresolved disagreements

**Consensus (all six debaters, consistent with the audits):**

1. The deliverable is an **emerging-hypertension trajectory warning**, not an acute-event detector. F2 as stated maps to no RQ. With no acute labels and about 37–40 SCD per 100,000 per year [clinician-31], the daily PPV is about 0.1% even at 99.9% specificity (Auditor B checked this).
2. **The submission is software only, on PPG+IMU data.** EM and hardware form a later path.
3. **The engine is hybrid:** a pooled *level* score plus a personal *change* lane. It must beat **mandatory level-only and cuff-only nulls**. (Aurora: cuff plus time of day beat all waveform models [PS-8]).
4. **There are exactly three states, and none of them is "STABLE".** At the cleared operating point, 58.8% of prevalent cases get no alert [bayesian_ml-4].
5. **The system never outputs mmHg.** Proxies attenuate change: 1.8 vs 7.4 mmHg, N=166 [PS-11].
6. **Joint posterior, not axis counting** (channels share sympathetic drive).
7. **Evaluation is event-level.** Abstention counts as a miss. Alarm burden is reported per non-converter person-year. Precision is censoring-aware.
8. **Rhythm is used only as an internal gate.** No MI/SCA wording appears anywhere.

**Unresolved:**

- *Whether change beats level.* In-domain ΔC is only 0.008–0.019, and HELIUS was null for SDNN/RMSSD [PS-28].
- *Night windows vs daytime stillness.* The night-window evidence rests on N=13, and night competes with charging.
- *The primary t_ref.* I rule: HBPM ≥130/80 is primary, and ESC ≥135/85 is a sensitivity analysis.
- *Raw-PPG access; class of a bundled rhythm flag; the ≤0.5 alarms/person-year budget (a proposal).*

## 2. Score table (Chair)

I discounted the teams' own round-3 scores. For example, BayesTrack's RQ6 drops from 9 to 8 because conformal prediction is vacuous with few positives, and EM-ANCHOR's RQ3 drops because its EM channels have no testable data. "Ev" is my evidence score; the audit integrity score is in brackets.

| Option | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 | RQ6 | **/60** | Ev (audit) | Eng | Stu |
|---|---|---|---|---|---|---|---|---|---|---|
| CONFIRM-HTN | 5 | 6 | 7 | 5 | 5 | 6 | **34** | 6 (7.5) | 7 | 8 |
| EM-ANCHOR | 6 | 6 | 4 | 6 | 6 | 6 | **34** | 3 (7.0) | 4 | 4 |
| TRACE-PPG | 7 | 6 | 5 | 6 | 8 | 6 | **38** | 7 (8.0) | 8 | 8 |
| NOCTURNE | 7 | 8 | 5 | 8 | 6 | 6 | **40** | 5 (8.0) | 5 | 6 |
| BayesTrack-HTN | 8 | 8 | 6 | 6 | 8 | 8 | **44** | 6 (8.0) | 6 | 5 |
| BioVance-Edge | 5 | 5 | 5 | 5 | 7 | 6 | **33** | 5 (7.5) | 8 | 3 |
| **F2 as stated** | 1 | 2 | 1 | 2 | 2 | 2 | **10** | 2 | 1 | 2 |

No option scores above 7 on RQ3. None has lead-time evidence from real events, and the persistence rules alone cost at least 28 days.

## 3. OPTIMAL PROTOTYPE — SENTINEL-HTN

Merges BayesTrack (engine, harness), TRACE (data, SQI), NOCTURNE (context), CONFIRM (t_ref, action), BioVance-Edge (budgets, regulation), EM-ANCHOR (optional EM tier).

**Target.** SENTINEL-HTN produces a calibrated risk of *emerging HTN* in untreated adults, enrolling elevated or high-normal BP first. In that group, warning PPV is about 60%, against 6–14% in unselected people (Auditor B's arithmetic). It also reports the timestamp of the first sustained warning. t_ref is the organiser label if one exists; otherwise two qualifying HBPM occasions ≥130/80.

**Learn → Detect → Predict → Warn**
- **Learn.** Hierarchical multivariate local-level state-space model (Student-t, population prior, person effects; ≥28 valid nights), per-channel quality weight and *attenuation gain* (prior <1). Channels: night RHR, night RMSSD, daytime-stillness HR (separate), steps, sleep duration/regularity, skin temperature, frozen PPG-encoder level score if raw PPG exists.
- **Detect.** Weekly CUSUM/BOCPD on the posterior residuals D_i(t). At most three pre-registered persistence rules; the main one is ≥4 of 6 weeks. Thresholds are set on non-converters only. A non-alerting "watch" tier runs alongside.
- **Predict.** A penalised discrete-time landmark hazard on level and deviation features, with isotonic calibration. If there are fewer than about 10 events per predictor, fall back to a level model plus a change threshold.
- **Warn.** Three states plus an evidence ledger. A warning triggers a **7-day HBPM surveillance series**.
- **Context (RQ4).** Post-exercise masks (a tunable window). Sleep and wake modelled separately. Timescale separation for alcohol, infection and the menstrual cycle. Season and ambient temperature as covariates: +0.61 mmHg per 1 °C fall [physiologist-24]. Weight and steps are tagged. A firmware change forces a re-baseline. In year one, warnings are capped at "watch".

**Sensors and BOM**
- *Submission:* challenge data or a commodity watch (PPG, IMU, skin temperature) plus a validated cuff.
- *v2 device:* MAX86176 PPG/ECG front end ($9.87 at 2,500) and an nRF52840. Estimated draw is 151–301 µA, or 21–42 days on 150 mAh (not yet measured). The inference rate must be stated: one inference per 15 minutes adds about 14 µA. The rest of the BOM is unsourced.

**Where EM sensing fits (optional, quality-weighted, never a key channel)**
1. **ECG** as an on-demand AF/irregularity gate. It can make a window ineligible or raise a persistence-gated "see a clinician" flag outside the HTN alarm budget.
2. **Seated ECG+PPG PAT**, in the pilot only, under a three-arm ablation: passive PPG / PPG ritual / PPG+ECG. It stays only if arm 3 beats arm 2 and adherence at week 4 is at least 60%.
3. **60 GHz bedside radar** as a pilot logger for OSA context and nights on the charger. It is never used for BP, and at 690–1290 mW it cannot go into a wearable.
4. **ICG/SCG** as the pilot reference for separating PEP from vascular PAT.

**Uncertainty and the three states**
- **POOR-QUALITY:** triggered by SQI, the rhythm-aware gate, or fewer than 15 valid days out of 30 [bayesian_ml-4]. A missing EM channel never triggers it.
- **INSUFFICIENT:** the posterior straddles the threshold, too few weeks can be evaluated, or the seasonal component is unidentified. Missing weeks count as "not evaluable", never as negative, and missingness is modelled as MNAR.
- **SUFFICIENT-warning:** the posterior crosses the threshold and the persistence rule is met.
- **Conformal prediction** is used only with at least 9 positives per stratum (α=0.1).

**Evidence ledger.** Weeks exceeded, recurrence, magnitude trend with interval, per-channel posterior contribution, confounders explaining part away, valid days and weights, calendar month.

**Evaluation**
Subject-grouped forward-chaining splits; scheduled HBPM for all. **A** AUROC/AUPRC · **B** Se at 0/30/90/180 d with label-interval width (synthetic onsets appendix-only) · **C** alarms per non-converter person-year, censoring-aware precision · **D** Brier, ECE · **E** dropout, noise, MNAR, coverage by ITA (dark skin: 50–85% of missing data [PS-22]) · **F** AURC, confidence vs evidence.
- **Ablations:** level-only, cuff-only, no personalisation, no context, night vs all-day, each channel removed in turn, treated vs untreated.
- **Kill criteria:** gain over level-only CI includes zero → drop RQ1 claim; >0.5 alarms/person-year → retune; EM fails ablation or adherence → drop; wrist covers ≥80% of nights → drop radar.

**Regulatory path.** Intended use is *risk notification*, which is EU MDR class IIa (Rule 11). The US precedent is K250507 (Class II) [bayesian_ml-4]. The model is locked with per-user state, and the PCCP excludes continuous learning. The build follows IEC 62304, ISO 14971 and IEC 60601-1, plus GDPR and Tunisian Law 2004-63. Because it shows no mmHg, the cuffless validation tests do not apply [device_engineer-9]. Any acute claim would put it in class IIb/III (the WCD is PMA Class III).

**Student build (8 weeks)**
W1 data audit, pre-registration · W2 SQI, context, nulls · W3 state-space, CUSUM/BOCPD · W4 hazard, calibration, 3 states, ledger · W5 A–F harness · W6 ablations, robustness · W7 failure cases · W8 paper, slides, repo.

**Path to a product.** 6–12-month pilot (≥100 high-normal BP; HBPM, EM ablation, radar, ICG/SCG) → cohort powered for ~85 converters → v2 device, QMS, CE IIa.

## 4. Verdict on the user's idea

**REFRAME. Drop F2 as the deliverable, and keep EM as an optional front-end tier that the pilot can kill.**

The evidence:
- F2 scores 10/60, because there are no acute labels for it to be scored against.
- In unselected people, daily PPV is about 0.1% [clinician-31].
- The only consumer arrest-detection analogue needed 99.965% day-level specificity [PS-16].
- An acute claim puts the device in class IIb/III.

The science itself is real in referred populations: a 14-day single-lead ECG gave near-term VA prediction with external AUROC 0.948, but PPV was only about 10% [physiologist-28]. That is a different product, with different data and different metrics.

**What survives:** ECG as rhythm/quality gate and pilot PAT channel; the baseline → persistent change → calibrated abstention chain, reusable for a future risk-drift F2.

## 5. Strongest audited references (SUPPORTED in audits A/B/C; entries copied from round 1)

- [bayesian_ml-1] Alavi A et al. "Real-time alerting system for COVID-19 and other stress events using wearable data." Nat Med, 2022 (epub 2021-11-29). DOI:10.1038/s41591-021-01593-2 | PMID:34845389 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34845389&rettype=abstract&retmode=text ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8799466/ — Type: prospective cohort — Key numbers: 3,318 participants, 84 SARS-CoV-2+; alerts in 67 (80%); median 3 days before symptom onset; other events 1.15 vs COVID-19 3.42 alert days/person; NightSignal = streaming median of overnight (24:00–7:00) RHR baseline, red alert at ≥4 bpm above baseline on 2 consecutive nights; specificity 87.7%; online CuSum 72%, RHRAD 69% sensitivity (Fitbit); proper baseline after 7 nights for >80% — Verified: PubMed abstract + PMC full text.
- [bayesian_ml-4] U.S. FDA. 510(k) Summary K250507, "Hypertension Notification Feature (HTNF)," Apple Inc., cleared 2025-09-11 — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250507.pdf — Type: regulatory — Key numbers: self-supervised DL encoder (unlabeled Apple Watch data, >86,000 participants) + linear model; development data 9,800 participants with home BP; 30-day windows; HTN = mean SBP ≥130 or DBP ≥80; 2,229 enrolled, 1,863 with ≥15 usable days; sensitivity 41.2% (37.2–45.3), specificity 92.3% (90.6–93.7); stage-2 sensitivity 53.7%; sensitivity risk ratio age <60 vs ≥60 0.69 (0.55–0.85), BMI ≤30 vs >30 0.67 (0.55–0.81); longitudinal specificity 86.4% (80.2–92.5), six 30-day windows, N = 187; "will not surface a notification if insufficient data is collected"; PCCP excludes continuously learning algorithms; predicate DEN230003 — Verified: full PDF text extracted.
- [clinician-18] Staplin N, de la Sierra A, Ruilope LM, et al. "Relationship between clinic and ambulatory blood pressure and mortality: an observational cohort study in 59 124 patients." Lancet, 2023. DOI:10.1016/S0140-6736(23)00733-X | PMID:37156250 — URL fetched: Europe PMC REST search (DOI query) — Type: prospective cohort (registry) — Key numbers: 59,124 patients, median 9.7 y; 24-h SBP HR 1.41 per SD vs clinic 1.18; night-time SBP informativeness 591% (all-cause) and 604% (CV) of clinic; masked HTN all-cause HR 1.24 (1.12–1.37), CV HR 1.37 (1.15–1.63); white-coat not associated with excess risk. — Verified: Europe PMC abstract.
- [clinician-31] Empana JP, Lerner I, Valentin E, et al. "Incidence of Sudden Cardiac Death in the European Union." Journal of the American College of Cardiology, 2022. DOI:10.1016/j.jacc.2022.02.041 | PMID:35512862 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35512862&rettype=abstract&retmode=text — Type: prospective cohort (4 population registries) — Key numbers: SCD 36.8–39.7 per 100,000/year; ≈249,538 SCD/year in the EU; OHCA 47.8–57.9 per 100,000/year. — Verified: PubMed abstract.
- [ppg_scientist-8] Mukkamala R et al. "The Microsoft Research Aurora Project: Important Findings on Cuffless Blood Pressure Measurement." Hypertension, 2023;80:534–540. DOI:10.1161/hypertensionaha.122.20410 | PMID:36458550 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC9931644/ ; BioC full text PMC9931644 — Type: review — Key numbers: 1,125 participants; none of the four waveform models (PWA, PWA-PAT) predicted next-day auscultatory or 24 h ambulatory cuff BP better than a baseline using only the calibration cuff BP and time of day; "essentially no value". — Verified: full-text passages (verbatim).
- [ppg_scientist-11] Derendinger FC et al. "Ability of a 24-h ambulatory cuffless blood pressure monitoring device to track blood pressure changes in clinical practice." J Hypertens, 2024;42:662–671. DOI:10.1097/hjh.0000000000003667 | PMID:38288945 — URL fetched: Europe PMC REST (abstract) — Type: prospective validation — Key numbers: N=166, Somnotouch-NIBP (PTT); difference between calibration BP and mean 24 h SBP was 7.4 (13.2) on cuff vs 1.8 (8.3) mmHg on the cuffless device; error grew with BP change. — Verified: abstract.
- [ppg_scientist-16] Fitbit (Google). "Loss of Pulse Detection — 510(k) Summary K242967." FDA CDRH, 2025 (decision 2025-02-25). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf24/K242967.pdf ; openFDA API — Type: regulatory — Key numbers: PPG + accelerometer, CNN; sensitivity 69.3% (64.3–74.1) across 135 users, 64.5% adjusted for simulated collapse; day-level specificity 99.965% (131 participants); not for people with known high SCD risk; analyses only while the user is still. — Verified: PDF text extracted.
- [ppg_scientist-22] Mulholland AM et al. "Influence of skin pigmentation on the accuracy and data quality of photoplethysmographic heart rate measurement during exercise." Eur J Appl Physiol, online 2025-09-18 (vol 126, 2026). DOI:10.1007/s00421-025-05977-x | PMID:40968160 — URL fetched: Europe PMC REST (abstract) — Type: validation study (lab) — Key numbers: N=28, ITA° colorimetry; missing data disproportionately from dark-skin participants (ITA° <10°; 36%): Apple 50%, SlateSafety 85%; error rose about 1 bpm for one device only. — Verified: abstract.
- [ppg_scientist-28] Bouwmeester TA et al. "Autonomic cardiac control independently predicts incident hypertension and systolic blood pressure in a multi-ethnic population: the HELIUS study." Eur J Prev Cardiol, online 2025-01-16 (33(7):1116–1124, 2026). DOI:10.1093/eurjpc/zwaf011 | PMID:39820403 — URL fetched: PubMed efetch abstract — Type: prospective cohort — Key numbers: median follow-up 6.6 y; 50% lower xBRS gave OR 1.31 (1.09–1.57) for new-onset HTN; SDNN and RMSSD were not associated with new-onset HTN. — Verified: abstract.
- [physiologist-24] Liu H et al. "Short-Term Effects of Personal-Level Environmental Temperature on Ambulatory Blood Pressure in Patients With Hypertension: A Multicity Panel Study." J Am Heart Assoc, 2025. DOI:10.1161/JAHA.125.045295 | PMID:41120825 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=41120825&rettype=abstract&retmode=text — Type: panel study — Key numbers: N=277 hypertensives, 4 Chinese cities; +0.61 (0.48–0.75) mmHg ambulatory BP per 1 °C decrease; nocturnal decline also associated — Verified: PubMed abstract.
- [physiologist-28] Fiorina L et al. "Near-term prediction of sustained ventricular arrhythmias applying artificial intelligence to single-lead ambulatory electrocardiogram." Eur Heart J, 2025. DOI:10.1093/eurheartj/ehaf073 | PMID:40157386 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=40157386&rettype=abstract&retmode=text — Type: retrospective development + external validation — Key numbers: 247,254 14-day recordings; 1,104 (0.5%) sustained VA; AUROC 0.957 internal / 0.948 external; at 97.0% specificity, sensitivity 70.6% / 66.1% (PPV ≈ 9–10% is my derivation assuming overall prevalence) — Verified: PubMed abstract.
- [device_engineer-9] Stergiou GS et al. "European Society of Hypertension recommendations for the validation of cuffless blood pressure measuring devices." J Hypertens, 2023;41(12):2074–2087. DOI:10.1097/HJH.0000000000003483 | PMID:37303198 — URL fetched: PubMed efetch (id=37303198) — Type: guideline/consensus — Key numbers: six tests for intermittent cuffless devices (static, device position, treatment, awake/asleep, exercise, recalibration), selected according to calibration and use — Verified: abstract + Crossref.

Scope notes from the audits:
- bayesian_ml-4 and ppg_scientist-16 are sponsor data and are cited for their numbers only.
- bayesian_ml-1 supports the baseline and context figures, not "gating matters".

## 6. Top risks

1. **Change adds nothing over level.** Then RQ1 collapses. Mitigation: the nulls, reported honestly.
2. **Too few converters with dense data before onset.** Then lead time can't be estimated. Report delay distributions with CIs.
3. **The label or data format is wrong for this design.** Examples: no raw PPG, or labels that are prevalent, treated or self-reported.
4. **Missingness tracks skin tone and engagement (MNAR).** Abstention then becomes an inequitable loss of sensitivity.
5. **Slow confounders** (season, weight, medication, firmware) mimic drift.
6. **Alarm fatigue, verification bias, and acute-claim scope creep.**

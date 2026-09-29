# Round 1 — Position paper: THE PPG SCIENTIST (`ppg_scientist`)

In-text citations `[PS-n]` refer to reference entry `[ppg_scientist-n]` in §8. Every number below is copied from a source retrieved in this session (2026-09-29).

---

## 1. Persona

I am a wearable-biosignal scientist: PhD in biomedical engineering, ten years on PPG signal processing, cuffless BP and large smartwatch cohorts, formerly in consumer-wearables R&D. My prior is that **deployability beats novelty**: PPG and accelerometers are already on hundreds of millions of wrists, and the challenge's own data (P, H, A, S) is PPG-and-motion data. My declared bias is **incumbency toward optical sensing**, so below I list where the evidence goes against me (§6, §7). I distrust claims that PPG can regress absolute BP, and I prefer trend and risk formulations.

## 2. Reading of the challenge (what actually scores)

- **The target is F1 (emerging hypertension trajectory), not an acute event.** All 60 points go to RQ1–RQ6: personal baseline, persistent change, lead time, context, robustness and abstention. No criterion rewards new sensors. The organisers ask who built "the most credible scientific approach … rather than just the most accurate model".
- **The data is P/H/A/S/C with realistic missingness.** It may arrive as raw waveforms or as aggregated features. Any design has to work on aggregated features, so a hardware front-end only matters if the organisers ship its signals.
- **Lead time needs a defined clinical reference point.** The strongest precedent defines hypertension as a 30-day mean home BP ≥130/80 mmHg under AHA 2017 [PS-1]. I adopt that definition, or the organisers' label if they provide one.
- **Formulation (F5):** change detection plus a discrete-time hazard on personal residuals (M3+M8). I do not propose regressing BP and then applying a threshold (M7), for the reasons in §3.2.

## 3. Verdict on the user's idea

**Interpretation evaluated:** "EM signals" means ECG, bioimpedance or RF. "Sudden/premature cardiac attack" means sudden cardiac arrest (VT/VF), acute MI, or prediction of either before onset.

**Verdict: reject F2 as the submission for this challenge; accept a narrow F4 as an ablation arm; keep F3 as an out-of-scope stub.**

### 3.1 F2 against the evidence

1. **Wearable sudden-arrest detection exists, and the cleared version is optical and fires at onset, not before.** Google/Fitbit's *Loss of Pulse Detection* (K242967, cleared 25 Feb 2025) uses **PPG + accelerometer**. Its validation reports sensitivity **69.3% (95% CI 64.3–74.1%)** across 135 users and day-level specificity **99.965%** [PS-16]. Its label excludes people already diagnosed at high SCD risk (CAD, cardiomyopathy, unexplained syncope) [PS-16]. The peer-reviewed study reports **1 unintentional emergency call per 21.67 user-years** and sensitivity **67.23%** in a prospective arterial-occlusion model [PS-17].
2. **The evidence for predicting ventricular arrhythmia in advance is thin, and it did not come from EM sensing.** SAFEHEART followed 277 ICD patients with 56 VA events and used **accelerometer** behaviour data. It reached AUROC **0.74 ± 0.05** [PS-19], in a high-risk cohort with k-fold CV. My 2021–2026 searches found no prospective wearable EM study that predicts MI or SCA before onset in unselected people. The em_engineer should produce one if it exists.
3. **EM is proven for arrhythmic SCD therapy, not for early warning.** The wearable cardioverter-defibrillator (ECG detection plus shock) was assessed across 40 studies and 59,647 adults. The pooled rate of appropriate intervention was **3% (95% CI 2–3%)** [PS-20]. That is a prescription device for high-risk patients, and it is neither a hypertension tool nor a student prototype.
4. **Smartwatch ECG is on demand.** Samsung's cleared ECG app records Lead I only when the opposite hand's finger touches the watch. Its background monitoring (IHRN) is PPG and runs "when the user is still" [PS-18].

**Conclusion:** F2 misses the scoring target. Where wearable evidence exists, it favours optical sensing for detection at onset and implanted or worn ECG plus a shock for therapy. None of it offers the longitudinal RQ1–RQ6 structure the jury scores.

### 3.2 F4 (EM as a front-end for the hypertension engine): what the numbers say

| Where PPG fails | Numbers | Does EM fix it? |
|---|---|---|
| Rhythm diagnosis | PPG only flags irregular rhythm. Watch ECG classifies AF with sensitivity **96.0%** and specificity **98.7%** at HR 50–150 [PS-18] | **Yes**: on-demand ECG confirmation |
| Data loss on dark skin | Participants with ITA° <10° were 36% of the sample but accounted for **50%** (Apple) and **85%** (SlateSafety) of missing data [PS-22]. Wearable pulse-rate 95% LoA were **−33.69 to 32.54 bpm** for dark skin vs −16.02 to 13.54 for light, with no significant mean bias [PS-21] | **Plausible**: bioimpedance showed no skin-tone sensitivity, but only in **n=3** [PS-23] (WEAK) |
| Absolute BP and BP-change tracking | PPG-PWA fails (below) | **No**: ECG-based PAT did not help (Aurora [PS-8]). A PTT device failed to track changes (calibration-to-24 h SBP gap 7.4 vs 1.8 mmHg) [PS-11]. The PAT–SBP slope ranged from −2946 to −470 mmHg/s across individuals [PS-12] |
| Hypertension screening signal | Foundation-model **PPG** embeddings reached AUROC **0.819** for self-reported high BP. **ECG** embeddings reached 0.769 and demographics plus HR reached 0.770 [PS-3] | **No measurable gain** from ECG |
| Sudden arrest | Optical detection at onset works (above) | EM adds **therapy**, not warning |

**Why I refuse BP regression as the core (M7).** In PulseDB (5,361 subjects), models generalise poorly to unseen subjects [PS-5]. The best model in an external benchmark had MAE **13.9/8.5 mmHg** without calibration, and **10.0–18.6 mmHg** SBP on external sets [PS-6]. PPG→BP shows mutual information of only **9.8%**, against 87.7% for heart rate [PS-7]. In the Aurora project (1,125 participants), waveform models with or without PAT were no better than a baseline that used only the calibration cuff BP and the time of day [PS-8, PS-9]. A regulator-grade PPG bracelet did not track medication-induced changes: **−1.0/−0.8 mmHg** on the device vs **−19.7/−11.5 mmHg** on home cuff BP [PS-10]. The currently cleared Aktiia G0 needs cuff calibration **every 24 hours**, covers ages 22–59, and was validated only in the static ISO 81060-2 setting for spot checks [PS-15]. ESH requires dedicated tests for BP change (treatment, awake/asleep, exercise, recalibration) [PS-13]. Scientific societies do not currently recommend cuffless BP devices [PS-14].

**Where PPG does work at screening grade.** Apple's Hypertension Notification Feature (K250507, 11 Sep 2025, 21 CFR 870.2380, Class II, OTC) analyses opportunistic **PPG only** over 30-day windows. In 2,229 people without a prior diagnosis it had sensitivity **41.2%** (37.2–45.3) and specificity **92.3%** (90.6–93.7), sensitivity **53.7%** for stage 2, and long-term specificity **86.4%** over two years (N=187) [PS-1]. Its model is a **self-supervised encoder trained on unlabeled data from more than 86,000 participants plus a linear head** [PS-1]. That is M6 validated at regulatory level.

## 4. Proposed prototype: **TRACE-PPG** (Trajectory, Robustness, Abstention, Context, Evidence)

The flow is L0 → L4, with the 3-state output at the end.

- **L0 · Qualification (edge).** An accelerometer stillness gate and a two-tier SQI: *HR-grade* for rate and HRV, *morphology-grade* for waveform shape. This follows the basic/high-quality split in 24 h wrist PPG, where both classifiers reached accuracy 0.96/0.97 [PS-24]. The same "analyse only when still and sufficient" pattern appears in cleared devices [PS-16, PS-18]. A usable-day counter runs per 30-day window.
- **L1 · Features per qualified window, split by context** (sleep, awake-rest, ≤30 min after activity, other):
  - sleep resting HR, and sleep RMSSD/SDNN;
  - PPG morphology descriptors;
  - an optional open PPG foundation-model embedding. PaPaGei was trained on more than 57,000 hours, has open weights, and includes a skin-tone analysis [PS-4]. The embedding is reduced to a 1-D "PPG-HTN score" with a linear probe, following [PS-1, PS-3];
  - daily steps, sedentary time, and sleep duration and regularity.
- **L2 · Personal baseline (RQ1).** A robust median/MAD per feature and context over the first 30 qualifying days. A hierarchical population prior (M2) covers cold start. The reference stays frozen, with slow re-baselining only after confirmed stability, so a real drift is not absorbed into the baseline.
- **L3 · Trajectory (RQ2).** Standardised residuals feed one-sided CUSUM per stream. The **evidence ledger** records persistence (number of 30-day windows), recurrence, magnitude trend, multimodal agreement and temporal consistency, which is exactly the challenge's §4 list. The analogue is a real-time personal-baseline alerting system that flagged **80%** (67/84) of infections a median **3 days** before symptoms, with a measurable false-alert rate of 1.15 alert-days per person [PS-25].
- **L4 · Risk (RQ3).** A discrete-time hazard, P(reaching the clinical reference within H days), with inputs:
  - population-level terms (age, sex, BMI, PPG-HTN score). PPG-derived vascular age supports this: an AI-PPG age gap >9 years gave HR **2.88** for hypertension in UK Biobank (N=212,231) [PS-27];
  - trajectory statistics from L3.
  Outputs are isotonic-calibrated, with Mondrian conformal sets stratified by data-quality level.
- **Output (RQ6).** The three states are defined in the card below. Every confirmed warning prompts a home-cuff confirmation, because the PPG-only precedent has an LR− of only 0.64 [PS-2].

```
PROTOTYPE CARD — TRACE-PPG
Target: probability that the individual reaches the clinical hypertension
  reference (30-day mean home BP ≥130/80, AHA 2017 as in [PS-1], or organisers'
  label / EHR first diagnosis) within horizon H (e.g., 90/180 d); reference point =
  first reference-positive date. Not absolute BP, not acute events.
Sensors/modalities: commodity smartwatch wrist PPG + 3-axis accelerometer (no new
  hardware); sleep/steps derived on-device; optional on-demand watch ECG (ablation
  only); validated upper-arm home cuff for sparse labels/confirmation.
Development data: organisers' data (primary). All of Us Fitbit — 6,042 participants,
  median 4.0 y, 482 incident hypertension, EHR-linked, registered access [PS-26]
  (lead-time evaluation). LifeSnaps — 71 people, >4 months, Fitbit Sense, public
  [PS-29] (missingness/baseline engineering). Aurora-BP — 1,125, 24 h ambulatory
  PPG+ECG+tonometry, public [PS-9] (PPG vs PAT ablation). PulseDB — 5,361
  subjects, ODbL / CC BY-NC-SA [PS-5] (SQI/morphology pre-training only).
RQ1 Personal baseline: context-stratified robust baseline + hierarchical prior.
RQ2 Temporal/trajectory: per-stream CUSUM + ledger (persistence ≥2 of 3 windows).
RQ3 Early-warning: hazard model over trajectory features; first "Sufficient"
  timestamp = early-warning time; lead time = reference date − warning date.
RQ4 Context: features computed only within context strata; post-activity windows
  excluded from rest baselines; activity/sedentary as covariates.
RQ5 Robustness: SQI gating, usable-day counts, missingness indicators as model
  inputs; stress tests with MCAR/MAR/MNAR dropout incl. skin-tone-linked MNAR
  pattern from [PS-22].
RQ6 3-state output: POOR-QUALITY (< 15 usable days/30 — the gate used by [PS-1],
  where 1,863/2,229 met it; or morphology-grade SQI coverage below threshold) →
  warning suppressed. INSUFFICIENT (conformal set = {risk, no-risk} or
  persistence < 2 windows) → keep monitoring. SUFFICIENT → warning.
Evidence output: ledger (which streams, how many windows, magnitude trend,
  context), calibrated risk + interval, data-quality summary.
Edge vs cloud: watch = SQI + features (+ embedding); phone/cloud = baseline,
  CUSUM, hazard, calibration (same split as [PS-1]). Opportunistic sampling at
  rest keeps power low. Hardware BOM: none beyond watch + home cuff.
Validation: subject-wise + forward-chaining splits (E1); AUROC/AUPRC/sens/spec (A);
  lead time, % caught early (B); alarms per person-month, warning precision (C);
  Brier/ECE (D); modality dropout/noise (E); risk–coverage/AURC (F); ablations:
  no-personalisation, no-context, no-SQI, embedding vs handcrafted, PPG vs PPG+PAT
  (E7); fairness by Fitzpatrick/age/BMI/sex (E8).
Regulatory path: software-only OTC notification, precedent K250507 (21 CFR
  870.2380, Class II, with PCCP; that PCCP excludes algorithms that continuously
  learn in the field [PS-1]). Not a BP measurement claim, so ISO 81060-3/ESH
  cuffless protocols [PS-13] are not the primary route.
Biggest risk: no longitudinal labels in organisers' data → lead time unmeasurable.
  Mitigation: All of Us + synthetic drift injection into LifeSnaps; report as
  limitation.
Buildable in 4–8 weeks? Yes: wk1–2 SQI+features; wk3–4 baseline+CUSUM+ledger;
  wk5–6 hazard+calibration+conformal+3-state; wk7–8 ablations, fairness, report.
  Later: All of Us application; prospective Tunisian pilot with home cuffs.
```

## 5. Claims table

| ID | Claim | Refs | Strength |
|---|---|---|---|
| C1 | PPG-only opportunistic analysis reaches regulatory-cleared screening performance (sens 41.2%, spec 92.3%, N=2,229) | PS-1 | STRONG (regulatory) |
| C2 | Absence of a notification weakly rules out hypertension (LR− 0.64, NPV 79.0%) | PS-1, PS-2 | MODERATE |
| C3 | Subject-independent PPG→BP regression generalises poorly (MAE 13.9/8.5 ID; 10.0–18.6 SBP external) | PS-5, PS-6, PS-7 | MODERATE |
| C4 | ECG-derived PAT added no value beyond calibration and time of day for resting/24 h BP (N=1,125) | PS-8, PS-9 | STRONG (large study; one sponsor) |
| C5 | Cuff-calibrated cuffless devices (PPG or PTT) failed to track BP changes | PS-10, PS-11 | MODERATE |
| C6 | The only cleared wearable sudden-arrest feature is PPG+accelerometer and detects at onset (sens 69.3%) | PS-16, PS-17 | STRONG (regulatory + Nature) |
| C7 | No evidence retrieved for wearable EM *prediction* of MI/SCA in unselected people; best prediction evidence is accelerometer-based in ICD patients (AUROC 0.74) | PS-19 | WEAK (absence of evidence) |
| C8 | Smartwatch ECG is on demand; background monitoring is PPG | PS-18 | STRONG (regulatory) |
| C9 | ECG adds value for rhythm confirmation (AF sens 96.0%, spec 98.7%) | PS-18 | STRONG (regulatory) |
| C10 | Dark skin mainly degrades PPG data quality and completeness rather than mean bias | PS-21, PS-22, PS-1 | MODERATE |
| C11 | Self-supervised PPG embeddings beat ECG embeddings for hypertension status (0.819 vs 0.769) | PS-3 | MODERATE (self-report labels) |
| C12 | Personal-baseline change detection on wearables gives lead time at a measurable false-alert cost | PS-25 | MODERATE (infection, not HTN) |
| C13 | PPG morphology carries prognostic vascular-ageing information for incident hypertension | PS-27 | MODERATE |
| C14 | HRV alone did not predict new-onset hypertension; baroreflex sensitivity (which needs beat-to-beat BP) did | PS-28 | MODERATE |

## 6. Anticipated attacks and pre-emptive defence

- **"41.2% sensitivity is poor."** Agreed. That is why the output has three states, why confirmation goes through a cuff, and why no claim of "no hypertension" is ever made [PS-1, PS-2]. My contribution is trajectory and lead time, which must be measured (§4) and not assumed.
- **"HTNF detects prevalent hypertension; that is not early warning."** Conceded. Its only longitudinal data are two-year specificity figures [PS-1]. TRACE-PPG's lead-time claim therefore rests on All of Us or organiser labels, not on HTNF.
- **"PPG is biased against dark skin."** In HTNF, sensitivity for Fitzpatrick I–IV vs V–VI had a risk ratio of **1.11 [0.84, 1.47]** after adjustment [PS-1], and pooled wearable pulse-rate bias was not significant [PS-21]. The real harm is **missingness** [PS-22], which the POOR-QUALITY state and the MNAR stress tests address. I will report coverage by skin tone and not hide it.
- **"Bioimpedance and radar avoid optics."** Possibly. The bioimpedance BP evidence is N=10 with within-subject models, and the skin-tone comparison had n=3 [PS-23]. I accept an EM arm **only** as an ablation against the same RQ1–RQ6 metrics.
- **"HRV is non-specific."** Conceded [PS-28]. That is why HRV is one stream among morphology, activity and sleep, and why persistence and cross-modal agreement are required.
- **"Foundation models are black boxes."** They are optional and reduced to one linear-probe score. The ledger is built on interpretable features.

## 7. Risks and limitations

- My incumbency bias. PPG→BP information content is low [PS-7], and HRV has limits [PS-28].
- Personal baselines can drift with device or firmware changes. This is a hypothesis to test; I found no source for it.
- Regulators may view per-user adaptation as "learning in the field" [PS-1].
- All of Us is predominantly white, female and college-educated (84% white, 73% female) [PS-26], which limits generalisation to Tunisia.
- The wearable evidence against F2 partly rests on absence of evidence (C7).

## 8. References

[ppg_scientist-1] Apple Inc. "Hypertension Notification Feature (HTNF) — 510(k) Summary K250507." FDA CDRH, 2025 (cleared 2025-09-11). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250507.pdf — Type: regulatory — Key numbers: 21 CFR 870.2380, Class II, OTC, adults ≥22 without HTN diagnosis; PPG only, 30-day windows; SSL encoder on >86,000 participants plus linear head, dev set >9,800; pivotal N=2,229 (1,863 with ≥15 usable days); HTN = mean home SBP ≥130 or DBP ≥80; sens 41.2% [37.2, 45.3], spec 92.3% [90.6, 93.7], PPV 70.9% at prevalence 31.4%; stage-2 sens 53.7%; Fitzpatrick I–IV vs V–VI sensitivity RR 1.11 [0.84, 1.47]; age <60 RR 0.69, BMI ≤30 RR 0.67; two-year specificity 86.4% (N=187); PCCP excludes continuously learning algorithms. (The 68.4%/99.1% pair in the summary belongs to the predicate, Viz HCM.) — Verified: full PDF text extracted with pypdf.

[ppg_scientist-2] Cohen JB et al. "Impact of a Smartwatch Hypertension Notification Feature for Population Screening." JAMA, 2026;335(11):1001–1003. DOI:10.1001/jama.2025.26925 | PMID:41661624 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC12887835/ — Type: retrospective (cross-sectional modelling, NHANES 2017–2020) — Key numbers: 3,983 NHANES participants representing about 127 million US adults unaware of HTN; applying K250507 sens/spec gives LR+ 5.35, LR− 0.64, PPV 69.1% (63.3–74.9), NPV 79.0% (76.6–81.3); authors warn of false reassurance. — Verified: PubMed record; full text through WebFetch (model-summarised; LR values are arithmetically consistent with [PS-1]).

[ppg_scientist-3] Abbaspourazad S et al. "Large-scale Training of Foundation Models for Wearable Biosignals." ICLR 2024. arXiv:2312.05409 — URL fetched: https://arxiv.org/abs/2312.05409 ; https://arxiv.org/html/2312.05409v2 — Type: PREPRINT / peer-reviewed conference — Key numbers: Apple Heart and Movement Study, about 141,207 PPG participants (19.85M segments) and about 106,643 ECG participants; participant-level linear probing with participant-disjoint splits; self-reported "Blood pressure" condition AUROC: PPG 0.819, ECG 0.769, baseline (age, BMI, sex, race/ethnicity, HR) 0.770; labels are self-reported. — Verified: arXiv abstract plus HTML full text (Table 9).

[ppg_scientist-4] Pillai A et al. "PaPaGei: Open Foundation Models for Optical Physiological Signals." ICLR 2025. arXiv:2410.20542 — URL fetched: https://arxiv.org/abs/2410.20542 — Type: PREPRINT / peer-reviewed conference — Key numbers: >57,000 h, 20M unlabeled PPG segments; 20 tasks across 10 datasets; +6.3% (classification) and +2.9% (regression) in at least 14 tasks; open code and weights; skin-tone robustness analysis. — Verified: arXiv abstract.

[ppg_scientist-5] Wang W et al. "PulseDB: A large, cleaned dataset based on MIMIC-III and VitalDB for benchmarking cuff-less blood pressure estimation methods." Front Digit Health, 2022;4:1090854 (Crossref issued 2023-02-08). DOI:10.3389/fdgth.2022.1090854 | PMID:36844249 — URL fetched: Europe PMC fullTextXML PMC9944565; https://www.frontiersin.org/articles/10.3389/fdgth.2022.1090854/full — Type: dataset / benchmark — Key numbers: 5,245,454 ten-second ECG/PPG/ABP segments from 5,361 subjects; calibration-free test set 279 subjects; a summarised prior CNN (PPG+ECG) showed SBP r 0.97 with record-wise CV vs r 0.22 subject-wise; licences ODbL (MIMIC) and CC BY-NC-SA 4.0 (VitalDB). — Verified: abstract plus full text.

[ppg_scientist-6] Moulaeifard M, Charlton PH, Strodthoff N. "Generalizable deep learning for photoplethysmography-based blood pressure estimation — A benchmarking study." Machine Learning: Health, 2025;1:010501. DOI:10.1088/3049-477x/ae01a8 | PMID:40959521 — URL fetched: Europe PMC REST (abstract); Crossref — Type: bench/lab (benchmark) — Key numbers: best model XResNet1d101, in-distribution MAE 9.0/5.8 mmHg with subject calibration and 13.9/8.5 without; external sets without calibration 10.0–18.6 (SBP) and 5.9–10.3 (DBP). — Verified: abstract plus Crossref metadata.

[ppg_scientist-7] Mehta S, Kwatra N, Jain M, McDuff D. "Examining the challenges of blood pressure estimation via photoplethysmogram." Sci Rep, 2024;14:18318. DOI:10.1038/s41598-024-68862-1 | PMID:39112533 — URL fetched: Europe PMC REST (abstract) — Type: bench/lab — Key numbers: prior work prone to data leakage; PPG→BP multi-valued mapping 33.2% and mutual information 9.8%, vs 0.75% and 87.7% for heart rate. — Verified: abstract.

[ppg_scientist-8] Mukkamala R et al. "The Microsoft Research Aurora Project: Important Findings on Cuffless Blood Pressure Measurement." Hypertension, 2023;80:534–540. DOI:10.1161/hypertensionaha.122.20410 | PMID:36458550 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC9931644/ ; BioC full text PMC9931644 — Type: review — Key numbers: 1,125 participants; none of the four waveform models (PWA, PWA-PAT) predicted next-day auscultatory or 24 h ambulatory cuff BP better than a baseline using only the calibration cuff BP and time of day; "essentially no value". — Verified: full-text passages (verbatim).

[ppg_scientist-9] Mieloszyk R et al. "A Comparison of Wearable Tonometry, Photoplethysmography, and Electrocardiography for Cuffless Measurement of Blood Pressure in an Ambulatory Setting." IEEE JBHI, 2022;26:2864–2875. DOI:10.1109/jbhi.2022.3153259 | PMID:35201992 — URL fetched: Europe PMC REST (abstract) — Type: prospective cohort / validation — Key numbers: N=1,125 (21–85 y); tonometry best (in-lab 0.32 ± 9.8 SBP); posture and setting affect error; first public ambulatory tonometry/PPG/ECG dataset (Aurora-BP). — Verified: abstract.

[ppg_scientist-10] Tan I et al. "Evaluation of the ability of a commercially available cuffless wearable device to track blood pressure changes." J Hypertens, 2023;41:1003–1010. DOI:10.1097/hjh.0000000000003428 | PMID:37016925 — URL fetched: Europe PMC REST (abstract) — Type: validation study — Key numbers: Aktiia, 41 participants over 6–12 days; night-time SBP over-read 15.5 mmHg; medication-induced change −1.0/−0.8 (device) vs −19.7/−11.5 mmHg (HBPM), n=3. — Verified: abstract.

[ppg_scientist-11] Derendinger FC et al. "Ability of a 24-h ambulatory cuffless blood pressure monitoring device to track blood pressure changes in clinical practice." J Hypertens, 2024;42:662–671. DOI:10.1097/hjh.0000000000003667 | PMID:38288945 — URL fetched: Europe PMC REST (abstract) — Type: prospective validation — Key numbers: N=166, Somnotouch-NIBP (PTT); difference between calibration BP and mean 24 h SBP was 7.4 (13.2) on cuff vs 1.8 (8.3) mmHg on the cuffless device; error grew with BP change. — Verified: abstract.

[ppg_scientist-12] Finnegan E et al. "Pulse arrival time as a surrogate of blood pressure." Sci Rep, 2021;11:22767. DOI:10.1038/s41598-021-01358-4 | PMID:34815419 — URL fetched: Europe PMC REST (abstract) — Type: bench/lab (phenylephrine) — Key numbers: N=30; the PAT–SBP gradient varied between individuals from −2946 to −470 mmHg/s; population models gave large errors. — Verified: abstract.

[ppg_scientist-13] Stergiou GS et al. "European Society of Hypertension recommendations for the validation of cuffless blood pressure measuring devices." J Hypertens, 2023;41:2074–2087. DOI:10.1097/hjh.0000000000003483 | PMID:37303198 — URL fetched: Europe PMC REST (abstract) — Type: guideline — Key numbers: six tests (static, position, treatment, awake/asleep, exercise, recalibration). — Verified: abstract.

[ppg_scientist-14] Stergiou GS et al. "The quest for accurate wearable blood pressure monitors." Hypertens Res, 2025 (online 2025-11-05; vol 49, 2026). DOI:10.1038/s41440-025-02410-w | PMID:41193706 — URL fetched: Europe PMC REST (abstract) — Type: review — Key numbers: no convincing evidence that any cuffless technology is accurate enough for clinical use; societies do not recommend them; HTNF useful for detection but needs cuff confirmation. — Verified: abstract.

[ppg_scientist-15] Aktiia SA. "G0 Blood Pressure Monitoring System — 510(k) Summary K250415." FDA CDRH, 2025 (decision 2025-07-02). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250415.pdf ; openFDA 510(k) API — Type: regulatory — Key numbers: product code DXN; PPG pulse-wave analysis; calibration every 24 h with an oscillometric cuff; ages 22–59; wrist 14–21 cm; spot-check home use; ISO 81060-2 seated validation. — Verified: PDF pages rendered and read.

[ppg_scientist-16] Fitbit (Google). "Loss of Pulse Detection — 510(k) Summary K242967." FDA CDRH, 2025 (decision 2025-02-25). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf24/K242967.pdf ; openFDA API — Type: regulatory — Key numbers: PPG + accelerometer, CNN; sensitivity 69.3% (64.3–74.1) across 135 users, 64.5% adjusted for simulated collapse; day-level specificity 99.965% (131 participants); not for people with known high SCD risk; analyses only while the user is still. — Verified: PDF text extracted.

[ppg_scientist-17] Shah K et al. "Automated loss of pulse detection on a consumer smartwatch." Nature, 2025;642:174–181. DOI:10.1038/s41586-025-08810-9 | PMID:40010378 — URL fetched: Europe PMC REST (abstract); Crossref — Type: prospective validation — Key numbers: 1 unintentional emergency call per 21.67 user-years; sensitivity 67.23% (64.32–70.05%) in an arterial-occlusion model. — Verified: abstract plus Crossref.

[ppg_scientist-18] Samsung Electronics. "Samsung ECG App v1.3 — 510(k) Summary K240909." FDA CDRH, 2024 (decision 2024-08-02). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf24/K240909.pdf ; openFDA API — Type: regulatory — Key numbers: on-demand Lead I needs the opposite finger on the watch; background IHRN is green PPG, acquired while still; ECG AF sensitivity 96.0%, sinus-rhythm specificity 98.7% (HR 50–150). — Verified: PDF text extracted.

[ppg_scientist-19] Kolk MZH et al. "Artificial intelligence-enhanced wearable technology enables ventricular arrhythmia prediction." Eur Heart J Digit Health, online 2024-09-21 (vol 7, 2026). DOI:10.1093/ehjdh/ztae069 | PMID:42077378 — URL fetched: Europe PMC REST (abstract); Crossref — Type: prospective cohort — Key numbers: SAFEHEART, 277 ICD patients, 56 VA, 64,995 days of accelerometry; deep representations AUROC 0.74 ± 0.05 vs 0.67 ± 0.14. — Verified: abstract.

[ppg_scientist-20] Matteucci A et al. "Wearable cardioverter defibrillator for transient arrhythmic risk and sudden cardiac death prevention: a systematic review and updated meta-analysis." Open Heart, 2025;12:e003648. DOI:10.1136/openhrt-2025-003648 | PMID:40992797 — URL fetched: Europe PMC REST (abstract) — Type: meta-analysis — Key numbers: 40 studies, 59,647 adults; appropriate intervention 3% (95% CI 2–3%), I²=88.9%. — Verified: abstract.

[ppg_scientist-21] Singh S et al. "Impact of Skin Pigmentation on Pulse Oximetry Blood Oxygenation and Wearable Pulse Rate Accuracy: Systematic Review and Meta-Analysis." J Med Internet Res, 2024;26:e62769. DOI:10.2196/62769 | PMID:39388258 — URL fetched: Europe PMC REST (abstract) — Type: meta-analysis — Key numbers: 4 wearable pulse-rate studies (n=176; 140,771 pairs); LoA light −16.02 to 13.54, medium −18.62 to 16.84, dark −33.69 to 32.54 bpm; no significant pigmentation bias. — Verified: abstract.

[ppg_scientist-22] Mulholland AM et al. "Influence of skin pigmentation on the accuracy and data quality of photoplethysmographic heart rate measurement during exercise." Eur J Appl Physiol, online 2025-09-18 (vol 126, 2026). DOI:10.1007/s00421-025-05977-x | PMID:40968160 — URL fetched: Europe PMC REST (abstract) — Type: validation study (lab) — Key numbers: N=28, ITA° colorimetry; missing data disproportionately from dark-skin participants (ITA° <10°; 36%): Apple 50%, SlateSafety 85%; error rose about 1 bpm for one device only. — Verified: abstract.

[ppg_scientist-23] Sel K et al. "Continuous cuffless blood pressure monitoring with a wearable ring bioimpedance device." npj Digit Med, 2023;6:59. DOI:10.1038/s41746-023-00796-w | PMID:36997608 — URL fetched: PubMed abstract; Europe PMC fullTextXML PMC10063561 — Type: bench/lab — Key numbers: N=10, exercise-induced BP change; SBP error 0.11 ± 5.27 mmHg; skin-tone comparison against PPG in 3 participants (Fitzpatrick I/IV/VI). — Verified: abstract plus full text.

[ppg_scientist-24] Moscato S et al. "Wrist Photoplethysmography Signal Quality Assessment for Reliable Heart Rate Estimate and Morphological Analysis." Sensors, 2022;22:5831. DOI:10.3390/s22155831 | PMID:35957395 — URL fetched: PubMed efetch abstract — Type: validation study — Key numbers: 31 participants, 24 h wrist PPG; SVM accuracy 0.96 (basic quality) and 0.97 (high quality). — Verified: abstract.

[ppg_scientist-25] Alavi A et al. "Real-time alerting system for COVID-19 and other stress events using wearable data." Nat Med, 2022;28:175–184 (online 2021-11-29). DOI:10.1038/s41591-021-01593-2 | PMID:34845389 — URL fetched: PubMed efetch abstract — Type: prospective cohort — Key numbers: 3,318 participants, 84 infected; alerts in 67 (80%); median 3 days before symptoms; 1.15 alert-days per person for non-COVID events. — Verified: abstract.

[ppg_scientist-26] Master H et al. "Association of step counts over time with the risk of chronic disease in the All of Us Research Program." Nat Med, 2022;28:2301–2308. DOI:10.1038/s41591-022-02012-w | PMID:36216933 — URL fetched: PubMed efetch abstract — Type: retrospective cohort — Key numbers: 6,042 participants, median monitoring 4.0 y, 5.9M person-days; 482 incident hypertension; 84% white, 73% female. — Verified: abstract. (Registered-tier Workbench access with DUA, as described in a 2026 All of Us paper's data statement, DOI:10.1038/s41467-026-71652-0, which was retrieved but is not cited for any claim.)

[ppg_scientist-27] Nie G et al. "Artificial intelligence-derived photoplethysmography age as a digital biomarker for cardiovascular health." Commun Med, 2025;5:481. DOI:10.1038/s43856-025-01188-9 | PMID:41258400 — URL fetched: PubMed abstract; Europe PMC fullTextXML PMC12630966 — Type: retrospective cohort — Key numbers: UK Biobank N=212,231; age gap >9 y gave MACCE HR 2.37 and hypertension HR 2.88; hypertension HR 1.05 per year of gap; external MIMIC N=2,343. — Verified: abstract plus full text.

[ppg_scientist-28] Bouwmeester TA et al. "Autonomic cardiac control independently predicts incident hypertension and systolic blood pressure in a multi-ethnic population: the HELIUS study." Eur J Prev Cardiol, online 2025-01-16 (33(7):1116–1124, 2026). DOI:10.1093/eurjpc/zwaf011 | PMID:39820403 — URL fetched: PubMed efetch abstract — Type: prospective cohort — Key numbers: median follow-up 6.6 y; 50% lower xBRS gave OR 1.31 (1.09–1.57) for new-onset HTN; SDNN and RMSSD were not associated with new-onset HTN. — Verified: abstract.

[ppg_scientist-29] Yfantidou S et al. "LifeSnaps, a 4-month multi-modal dataset capturing unobtrusive snapshots of our lives in the wild." Sci Data, 2022;9:663. DOI:10.1038/s41597-022-01764-x | PMID:36316345 — URL fetched: PubMed efetch abstract — Type: dataset — Key numbers: n=71, >4 months, Fitbit Sense plus surveys/EMA, >35 data types, >71M rows, public release. — Verified: abstract.

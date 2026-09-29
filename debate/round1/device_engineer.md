# Round 1 — Position paper: THE DEVICE ENGINEER (`device_engineer`)

## 1. Persona

Medical-device systems engineer: 15 years shipping Class II wearables (IEC 60601-1, IEC 62304, ISO 14971, IEC 62366; FDA 510(k)/De Novo and EU MDR files), embedded and edge-AI firmware, now advising MedTech start-ups in North Africa. My priors: minimise sensors; the intended use decides the regulatory class and the design; edge for signal quality and features, cloud for longitudinal models; sceptical of radar inside a wearable. The bias I watch in myself is conservatism. Where evidence moved me, I mark it **Update**.

## 2. Reading of the challenge (what actually scores)

- The 60 points are RQ1–RQ6 at 10 each. No points go to sensor novelty, hardware, or acute cardiac events. The jury rewards the "most credible scientific approach", lead time *with* reliability, calibration, a low false-alarm burden and abstention.
- The deliverables (5-page paper, 15 slides, GitHub) are judged as **software on the organisers' dataset**. Hardware can score only indirectly: it can capture context (RQ4), gate data quality at the edge (RQ5), and fill the paper's "System Architecture" section.
- The regulated version of this product already exists. Apple's Hypertension Notification Feature (HTNF, 510(k) K250507, cleared 11 Sep 2025) is Class II software under 21 CFR 870.2380. It turns PPG collected over 30-day windows into a notification for adults ≥22 without a hypertension diagnosis. Its reported sensitivity is 41.2% and specificity 92.3% [device_engineer-1]. Read in engineering terms, the challenge asks teams to beat that bar using personalisation, trajectory modelling, context and abstention.

## 3. Verdict on the user's idea

**Interpretations evaluated.** For "EM" I considered ECG (biopotential), bioimpedance, radar (both inside a wearable and at the bedside), NCS and OPM-MCG. For "sudden/premature cardiac attack" I considered sudden cardiac arrest (VT/VF, loss of pulse) and acute MI.

**Verdict: REJECT as stated (F2) for this challenge; REFRAME to F4.** Keep EM sensing as the physiological front-end of the hypertension-trajectory engine. The reasons:

1. **Scoring mismatch.** None of RQ1–RQ6 rewards detecting acute events.
2. **The regulatory class jumps.** Under EU MDR Rule 11, software that monitors vital parameters whose variations "could result in immediate danger" is Class IIb, and software informing decisions whose error may cause death is Class III. Software that analyses physiological parameters "to prevent the risk of illnesses" (the guidance's own example is arterial stiffness) is Class IIa [device_engineer-16]. In the US, the wearable response device for sudden cardiac arrest (the WCD, product code MVK) is Class III under PMA [device_engineer-8].
3. **The only cleared consumer SCA detector is not EM.** Loss of Pulse Detection (K242967, Feb 2025) uses PPG and an accelerometer. Its sensitivity was 69.3% in 135 users and its day-level specificity 99.965% [device_engineer-2]. The companion Nature paper reports 1 unintentional emergency call per 21.67 user-years and 67.23% sensitivity in an arterial-occlusion model of cardiac arrest [device_engineer-3]. The programme had to *simulate* pulselessness because real arrests cannot be collected prospectively. A student team cannot reproduce that.
4. **EM evidence for acute detection is thin.**
   - Every cleared radar monitor measures HR/RR in clinical settings only. Each is "not indicated for active patient monitoring", provides no alarms and is "not intended to monitor heart rate in patients with arrhythmias": XK300 (IR-UWB, 2021), Circadia C200 (UWB, 2024) and C300 (60 GHz FMCW, 2026) [device_engineer-4, -5, -6].
   - Radar arrhythmia classification reached 75% accuracy in 15 subjects [device_engineer-28].
   - MCG normally needs a magnetically shielded room; unshielded, movable OPM systems are still research demonstrations [device_engineer-30].
   - ECG is the only EM modality with a pedigree for sudden cardiac arrest, but it needs continuous electrode contact. WCD users wear the vest about 21 h/day [device_engineer-27]. That is a garment, not a watch.

**Which EM variant is engineerable, and which has the best feasibility/value ratio?**

| EM variant | Buildable by students? | Product precedent | Value for the HTN trajectory | Call |
|---|---|---|---|---|
| **Single-lead ECG spot-check + PPG → PAT, HRV** | Yes: one AFE with synchronised PPG/ECG, designed to IEC 60601-2-47 [device_engineer-18] | Class II PPG notification [-1] | PAT/HRV features measured in a standardised rest context | **Best ratio** |
| Bedside 60 GHz radar node | Yes, mains-powered evaluation board | C300, clinical settings only [-6]; radar OSA screening [-29] | Nocturnal HR/RR, sleep and OSA context (RQ4) | Phase 2 |
| Radar inside the wearable | No: 690–1290 mW when active [-17] | none | — | Reject |
| Radar-derived BP | Feasibility studies only [-15] | no validation protocol | — | Research only |
| Bioimpedance | Possible, but adds electrodes and current injection | — | Marginal over PAT | Defer |
| NCS / OPM-MCG | No | none for wearables | Ischaemia rather than HTN | Reject |

**Update:** I expected no regulatory path for radar at all. There is one, a 60 GHz FMCW HR/RR monitor cleared in 2026 [-6], but only at the bedside and without alarms. That supports a nightstand node, not radar on the wrist.

## 4. Proposed prototype — "BioVance-Edge"

**D1. Intended use is a notification, not a BP measurement.** Three reasons:
- There is a Class II notification precedent [-1].
- Claiming BP values triggers heavy validation. That means either the ESH six tests (static, position, treatment, awake/asleep, exercise, recalibration) [-9] or ISO 81060-3:2022 for continuous devices [-11]. A training-phase ISO 81060-3 study used an invasive radial-artery reference and needed ≥50 change points per subject [-12].
- Calibrated cuffless devices stay anchored to their calibration. Against 24-h cuff BPM in 166 participants, the change from the calibration value to the mean 24-h SBP was 7.4 (13.2) mmHg by cuff but only 1.8 (8.3) mmHg by the cuffless device [-14]. The "estimate BP, then threshold" route (M7) would therefore hide exactly the drift we want to catch.

The model instead runs the trajectory directly on personal features, with sparse cuff labels (S10). Every warning is routed to a validated upper-arm cuff for confirmation, as professional bodies advise [-13].

**D2. Minimise sensors.**
- PPG and accelerometer run passively all the time.
- A single-lead ECG spot-check takes 30 s, seated, twice a day (finger on the top electrode) and gives PAT.
- The spot-check protocol is itself an RQ4 answer: it produces a "rest-equivalent" measurement.

**D3. The edge handles signal quality and features; the cloud handles trajectory.** TinyML is feasible here:
- A quantised TCN on an STM32WB55 reached 4.41 BPM MAE at 47.65 mJ per inference, and a 1.9 kB variant used 1.79 mJ [-20].
- An INT8 PPG→BP CNN ran in real time on an STM32N6, though INT8 drift depended on the architecture [-21].
- Feature-based PPG quality assessment reached 95.6% accuracy on 35,712 epochs from daily activities [-22].
- Only features and SQI leave the device, which is data minimisation by design.

**D4. Locked models with per-user state; no on-device training.** Apple's cleared change-control plan explicitly excludes "adaptive algorithms that will continuously learn in the field" [-1]. The federated-learning evidence is weak for deployment:
- A systematic review of 22 cardiovascular FL studies found them mostly retrospective, many with *simulated* client splits [-23].
- One wearable study measured a 13.87-point accuracy loss and about 70× longer training for naive FL [-24].

Personalisation is therefore done with Bayesian baseline parameters per user (M1/M2), updated on the phone or in the cloud. FL appears only as a simulated ablation.

**D5. Radar only at the bedside, and only in phase 2.** The IWRL6432 draws 690–1290 mW when active. Its datasheet reports 1.2 mW average only for 1-Hz presence detection [-17]. Tracking vital signs needs continuous frames, so the node must be mains-powered.

**Power budget, wrist unit** (estimates, except where cited; to be measured with a power profiler in week 6):

| Block | Average current |
|---|---|
| PPG readout at 25 fps | <11 µA [-18] + LED drive ≈30–60 µA (est.) |
| PAT bursts (2 × 30 s/day) | negligible |
| IMU in low-power mode | ≈10–30 µA (est.) |
| BLE batch upload every 15 min | ≈50–100 µA (est.); radio peak 6.40 mA TX at 0 dBm [-19] |
| MCU: SQI and features | ≈50–100 µA (est.) |
| **Total** | **≈0.15–0.3 mA → a 150 mAh cell lasts ≈3 weeks nominal and ≥1 week after 50% derating** |

My "one week on a battery" test passes for the wrist unit and fails for any wearable radar.

```
PROTOTYPE CARD — BioVance-Edge (EM front-end + abstaining personal-trajectory engine)
Target (exactly what is detected/predicted, and the clinical reference point): Per-person probability that
  30-day physiology has entered an emerging-hypertension trajectory; reference = first time the home/ambulatory
  cuff mean crosses the organisers' clinical label (e.g. ≥130/80 per the dataset definition). A notification,
  not a BP value.
Sensors/modalities (part numbers if hardware): Wrist PPG+IMU (passive); single-lead ECG spot-check → PAT
  (MAX86176 synchronised PPG/ECG AFE); nRF52840 BLE SoC; validated BLE upper-arm cuff weekly (S10).
  Phase 2: mains-powered 60 GHz FMCW bedside node (IWRL6432 evaluation board) for nocturnal HR/RR and sleep.
Development data (datasets, availability, licence): Organisers' dataset (primary). Own pilot recordings only
  after ethics approval. Public PPG/ECG sets for SQI pre-training (licence per dataset).
RQ1 Personal baseline: Robust per-person, per-context baselines (median/MAD, EWMA) as the prior; hierarchical
  Bayesian shrinkage for cold start (M1+M2).
RQ2 Temporal/trajectory: CUSUM/BOCPD on personal residuals D_i(t) + slope of a state-space trend (M3/M4); an
  alert needs persistence AND recurrence.
RQ3 Early-warning / lead-time strategy: Alarm budget per person-month; the threshold is chosen on validation
  folds to maximise lead time at fixed warning precision (M14); cuff confirmation closes the loop.
RQ4 Context handling: Features stratified by IMU activity state, sleep/wake and time of day; spot-check PAT
  = standardised rest context; post-exercise windows excluded.
RQ5 Robustness to missing/noisy data: Edge SQI gate; missingness-aware likelihood (only observed windows
  update the state); modality-dropout tests.
RQ6 Uncertainty & abstention (3-state output): Posterior + conformal interval → "emerging risk" /
  "insufficient evidence, keep monitoring" / "poor-quality data, warning suppressed" (SQI or coverage below
  minimum, cf. Apple's ≥15-days-of-data rule).
Evidence/explanation output: Ledger per alert: days of persistence, recurrence count, magnitude trend,
  modalities agreeing, data coverage %.
Edge vs cloud split · power · BOM cost estimate: Edge = SQI, beats, PAT, HR/HRV, activity; phone = BLE hub,
  cuff ingest, encryption; cloud = longitudinal model, calibration, dashboard. ≈0.15–0.3 mA → ≥1 week.
  BOM: AFE $14.36 (1 pc) / $9.87 (2,500 pcs) [retrieved]; whole wrist BOM ≈$35–60 at 1k units (my estimate).
Validation plan (metrics A–F, splits, standards): Subject-wise + forward-chaining splits; AUROC/AUPRC, lead
  time, alarms/person-month, Brier/ECE, risk–coverage (E1–E7); skin-tone/BMI/age subgroups (E8). Product:
  prospective 30-day home-cuff-referenced study with subject-level sensitivity/specificity (Apple design);
  IEC 60601-1/-1-2, IEC 62304 and IEEE C63.27 as listed in cleared radar 510(k)s.
Regulatory / real-world path: Software-first: SaMD notification, EU MDR Rule 11 Class IIa, FDA 510(k) with
  predicate K250507. No BP-value claims, so no ISO 81060-3. Tunisia: registration after CE/FDA.
Biggest risk + mitigation: Adherence and data sufficiency (see §7) → passive PPG, only 2 × 30 s of user
  effort per day, coverage-aware abstention.
Buildable by a student team for the challenge? (what in 4–8 weeks, what later): YES. Wk1 data audit + SQI
  and missingness map; Wk2–3 baselines + change detection; Wk4 calibration/abstention/alarm policy;
  Wk5 ablations and robustness; Wk6 optional MAX86176 + nRF52840 evaluation-kit demo streaming PAT features
  into the same pipeline + measured power; Wk7–8 paper, slides, repo. Later: custom PCB, 60601 testing,
  clinical study, bedside radar.
```

**Minimum viable real-world prototype:** software only. A commodity wrist PPG + IMU device plus a validated BLE cuff feed the trajectory engine. Apple's software-only device on a general-purpose platform needed no medical-device hardware testing [-1].
**My preferred prototype:** the card above, i.e. the MVP plus the ECG spot-check for PAT, with the bedside radar in phase 2.

## 5. Claims table

| ID | Claim | Refs | Strength |
|---|---|---|---|
| DE-C1 | A PPG-only HTN notification is FDA Class II (21 CFR 870.2380) at 41.2% sensitivity / 92.3% specificity, N=2,229 enrolled | -1 | STRONG (regulatory) |
| DE-C2 | Cleared SCA detection on a consumer wearable is PPG-based, not EM: 67–69% sensitivity, 1 false call per 21.67 user-years | -2, -3 | STRONG |
| DE-C3 | SCA/vital-danger software is MDR Class IIb/III and the WCD is FDA Class III; HTN-risk analysis is Class IIa | -16, -8 | STRONG (regulatory) |
| DE-C4 | Cleared radar monitors are HR/RR-only, clinical settings, no alarms, not for arrhythmia | -4, -5, -6 | STRONG (regulatory) |
| DE-C5 | Radar arrhythmia and radar-BP evidence is small and heterogeneous | -28, -15 | WEAK / MODERATE |
| DE-C6 | Radar in a wearable breaks the power budget (690–1290 mW active) | -17 | MODERATE (INDUSTRY-CLAIM spec) |
| DE-C7 | Calibrated cuffless BP under-tracks change from calibration, so M7 masks drift | -14, -13 | MODERATE |
| DE-C8 | Claiming BP values brings ESH six-test / ISO 81060-3 burden, including an invasive reference | -9, -10, -11, -12 | STRONG (standard/consensus) |
| DE-C9 | SQI and feature extraction are feasible on MCUs at mJ per inference | -20, -21, -22 | MODERATE |
| DE-C10 | FL for cardiovascular prediction is mostly simulated/retrospective; naive FL costs accuracy and time | -23, -24 | MODERATE / WEAK |
| DE-C11 | Regulators accepted locked models with change control, not continuous field learning | -1 | STRONG (regulatory) |
| DE-C12 | Real-world failure modes: 16% of HTNF participants lacked ≥15 usable days; 12-month wear-time 77.4%; false alerts degrade patient-reported health; specificity 86.4% over 2 years | -1, -25, -26 | MODERATE |
| DE-C13 | Bedside radar has clinical value for sleep/OSA context | -29 | MODERATE |
| DE-C14 | Tunisian need: HTN controlled in 51.7% (140/90) / 18.6% (130/80) of 25,890 patients; African device oversight relies on international certification | -32, -31 | MODERATE |

## 6. Anticipated attacks and pre-emptive defence

1. **"Conservative: you gutted the user's EM idea."** EM stays in the device in two places: the ECG gives PAT, and phase 2 adds a bedside radar with a 2026 regulatory precedent [-6]. What I reject is (a) the acute target, which scores zero and jumps the regulatory class, and (b) radar on the wrist, which the power figures rule out [-17].
2. **"41% sensitivity is a weak bar."** It is the bar regulators *accepted*, which makes it the right baseline. Our contribution is to improve it with personal baselines, context and abstention, and to report the trade-off honestly on metrics B, C and F.
3. **"The ECG spot-check needs user effort, which kills adherence."** PAT is additive. Passive PPG carries the model, and missing spot-checks move the output to "insufficient evidence" rather than degrading it silently.
4. **"The organisers list federated learning."** We include it as a simulated ablation on their data. The deployment evidence is simulation-heavy [-23], and the one precedent that got cleared used locked models [-1].
5. **"Cuffless BP now has standards, so estimate BP."** Look at the burden [-11, -12] and the anchoring failure [-14]. A notification is faster to market and scientifically cleaner for trajectory detection.
6. **"Hardware doesn't score."** Agreed. That is why the hardware is optional (week 6), and why its only jobs are the RQ4 context and the RQ5 quality gate.

## 7. Risks and limitations

- **Failure modes observed in the field:**
  - Of 2,229 HTNF participants, 1,863 (83.6%) had ≥15 days of usable data.
  - Long-term specificity for non-hypertensives fell to 86.4% (N=187) over two years [-1].
  - Wear-time averaged 77.4% over 12 months even with active engagement support (273/298 completed) [-25].
  - In one study, 10,107 of 35,712 daily-life PPG epochs (28%) were poor quality [-22].
  - False AF alerts produced a dose-dependent decline in self-perceived health [-26].
  
  The design must budget for all of these; better models do not remove them.
- The power figures and the whole-BOM cost are **my estimates**. Only the AFE, radar and BLE figures come from retrieved vendor documents (INDUSTRY-CLAIM).
- Adding an ECG may change the predicate or product code relative to K250507. I have not verified this.
- Tunisia: the regulator is transitioning (DPM → ANMPS), which I could verify only from non-peer-reviewed sources, so I rely on it for nothing. African device oversight leans on international certification [-31], so the practical order is CE (Class IIa) or FDA first, then local registration. Data protection falls under Organic Law 2004-63 [background, pre-2021, text not retrieved]. Features-only upload helps under any regime.

## 8. References

[device_engineer-1] Apple Inc. (applicant); FDA CDRH. "510(k) Summary K250507 — Hypertension Notification Feature (HTNF)." FDA, 2025 (cleared 11 Sep 2025; SE letter re-issued with product code SFR). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250507.pdf (also openFDA 510k API) — Type: regulatory — Key numbers: 21 CFR 870.2380, Class II, OTC, adults ≥22 without HTN diagnosis, not in pregnancy; predicate Viz HCM DEN230003; SSL encoder on data from >86,000 participants, development set >9,800; pivotal study 2,229 enrolled, 1,863 with ≥15 days of usable data, 30-day wear, FDA-cleared home cuff reference (AHA ≥130/80); sensitivity 41.2% (37.2–45.3), specificity 92.3% (90.6–93.7), stage-2 sensitivity 53.7%, PPV 70.9% at prevalence 31.4%; longitudinal specificity 86.4% (N=187, six 30-day windows over 2 years); PCCP excludes continuously learning algorithms; software-only, so "medical device hardware testing is not applicable" — Verified: full PDF text extracted and read.

[device_engineer-2] Fitbit (Google) (applicant); FDA CDRH. "510(k) Summary K242967 — Loss of Pulse Detection." FDA, 2025 (cleared 25 Feb 2025). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf24/K242967.pdf — Type: regulatory — Key numbers: 21 CFR 870.2790, product code SDY, OTC; PPG + accelerometer; sensitivity 69.3% (64.3–74.1) in 135 users, 64.5% (55.7–74.2) adjusted for simulated collapse; day-level specificity 99.965% (99.804–99.999) in 131 participants; human-factors validation performed — Verified: full PDF text read.

[device_engineer-3] Shah K et al. "Automated loss of pulse detection on a consumer smartwatch." Nature, 2025;642:174–181. DOI:10.1038/s41586-025-08810-9 | PMID:40010378 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=40010378&rettype=abstract&retmode=text — Type: prospective validation study — Key numbers: 1 unintentional emergency call per 21.67 user-years across two prospective studies; sensitivity 67.23% (64.32–70.05) in a prospective arterial-occlusion cardiac-arrest simulation model — Verified: PubMed abstract + Crossref metadata.

[device_engineer-4] Xandar Kardian (applicant); FDA CDRH. "510(k) Summary K202464 — Vital Sign Monitoring Sensor XK300." FDA, 2021 (cleared 26 Apr 2021). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf20/K202464.pdf — Type: regulatory — Key numbers: IR-UWB radar; HR 60–120 bpm, RR 6–55 brpm; adults in a general-care hospital environment; product code DRT — Verified: PDF text read.

[device_engineer-5] Circadia Technologies (applicant); FDA CDRH. "510(k) Summary K234003 — Circadia C200 System." FDA, 2024 (cleared 30 May 2024). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf23/K234003.pdf — Type: regulatory — Key numbers: 6.4–7.8 GHz UWB radar; clinical settings (skilled nursing/long-term care); "not indicated for active patient monitoring… does not provide alarms"; "not intended to monitor heart rate in patients with arrhythmias"; HR agreement within ±5 bpm in n=49 and n=41; tested to IEC 62304, IEC 60601-1, IEC 60601-1-2, IEEE C63.27 — Verified: PDF text read.

[device_engineer-6] Circadia Health (applicant); FDA CDRH. "510(k) Summary K252676 — Circadia C300 System." FDA, 2026 (cleared 3 Feb 2026). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K252676.pdf — Type: regulatory — Key numbers: 58.0–61.5 GHz FMCW radar (centre 59.8 GHz); controlled n=45, uncontrolled n=40; HR within ±5 bpm; RR ARMS within ±3 brpm; same clinical-setting, no-alarm, no-arrhythmia limits as C200 — Verified: PDF text read.

[device_engineer-7] Aktiia SA (applicant); FDA CDRH. "510(k) K250415 — G0 Blood Pressure Monitoring System." FDA, 2025 (cleared 2 Jul 2025); plus Aktiia press release, 9 Jul 2025 (INDUSTRY-CLAIM). — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250415.pdf ; https://www.prnewswire.com/news-releases/aktiias-hilo-band-becomes-first-cuffless-blood-pressure-monitor-cleared-by-fda-for-over-the-counter-use-302501123.html — Type: regulatory + INDUSTRY-CLAIM — Key numbers: 21 CFR 870.1130, product code DXN, Class II (from the letter); press release: first OTC cuffless optical BP monitor, "requires calibration using a cuff" — Verified: SE letter text read (summary pages are image-only); press release fetched. Used only as a precedent; not load-bearing for the claims table.

[device_engineer-8] ZOLL Manufacturing (applicant); FDA. "PMA P010030 — LifeVest Wearable Defibrillator" (supplements S198–S202, Dec 2025–Sep 2026) and classification product code MVK. — URL fetched: https://api.fda.gov/device/pma.json?search=pma_number:"P010030" ; https://api.fda.gov/device/classification.json?search=product_code:MVK — Type: regulatory — Key numbers: wearable automated external defibrillator, device class 3, PMA pathway — Verified: openFDA API responses.

[device_engineer-9] Stergiou GS et al. "European Society of Hypertension recommendations for the validation of cuffless blood pressure measuring devices." J Hypertens, 2023;41(12):2074–2087. DOI:10.1097/HJH.0000000000003483 | PMID:37303198 — URL fetched: PubMed efetch (id=37303198) — Type: guideline/consensus — Key numbers: six tests for intermittent cuffless devices (static, device position, treatment, awake/asleep, exercise, recalibration), selected according to calibration and use — Verified: abstract + Crossref.

[device_engineer-10] Mukkamala R et al. "Evaluation of the Accuracy of Cuffless Blood Pressure Measurement Devices: Challenges and Proposals." Hypertension, 2021;78(5):1161–1167. DOI:10.1161/HYPERTENSIONAHA.121.17747 | PMID:34510915 — URL fetched: PubMed efetch (id=34510915) — Type: review — Key numbers: the 2018 AAMI/ESH/ISO universal standard is "inappropriate for the validation of cuffless devices"; 2021 ESH guidelines do not recommend cuffless devices for clinical use — Verified: abstract + Crossref.

[device_engineer-11] ISO. "ISO 81060-3:2022 Non-invasive sphygmomanometers — Part 3: Clinical investigation of continuous automated measurement type." Edition 1, 2022. — URL fetched: https://www.sis.se/en/produkter/health-care-technology/medical-equipment/anaesthetic-respiratory-and-reanimation-equipment/iso-81060-32022/ (iso.org returned 403) — Type: standard — Key numbers: approved 16 Dec 2022; scope covers clinical investigation of continuous automated NIBP devices, both trending and absolute-accuracy types; usability excluded — Verified: SIS catalogue page (scope text).

[device_engineer-12] Lai CL et al. "Continuous BP monitoring of ICU Taiwanese patients: training-phase evaluation of oCare BP100 according to ISO 81060-3:2022." Front Med Technol, 2026. DOI:10.3389/fmedt.2026.1681323 | PMID:42483325 — URL fetched: PubMed efetch (id=42483325) — Type: validation study (training phase) — Key numbers: 40 ICU patients with invasive radial-artery reference; Type T thresholds s_corr ≤6 mmHg; BP change test minimum 50 change points per subject, Ē50th ≤25%, Ē85th ≤50%; full ISO protocol not completed — Verified: abstract + Crossref. WEAK as a description of the standard (secondary source).

[device_engineer-13] Wehbe F, Hiremath S. "Cuffless blood pressure in 2025: from promise to practice: a narrative review." Curr Opin Nephrol Hypertens, 2026;35(2):164–173. DOI:10.1097/MNH.0000000000001150 | PMID:41460057 — URL fetched: PubMed efetch (id=41460057) — Type: review — Key numbers: outputs reliable for trends around the last calibration; professional bodies advise against diagnosis or titration from cuffless readings unless the device passes cuffless protocols; confirm with validated upper-arm measurement — Verified: abstract + Crossref.

[device_engineer-14] Derendinger FC et al. "Ability of a 24-h ambulatory cuffless blood pressure monitoring device to track blood pressure changes in clinical practice." J Hypertens, 2024;42(4). DOI:10.1097/HJH.0000000000003667 | PMID:38288945 — URL fetched: PubMed efetch (id=38288945) — Type: prospective validation study — Key numbers: N=166; Somnotouch-NIBP (PTT) vs cuff 24-h BPM; mean(SD) difference between calibration BP and 24-h mean SBP 7.4 (13.2) by cuff vs 1.8 (8.3) mmHg by cuffless; DBP 6.6 (6.8) vs 1.6 (5.8); the larger the BP change, the larger the device disagreement — Verified: abstract + Crossref.

[device_engineer-15] Falconer D et al. "Emerging radar-based technologies for cuffless blood pressure monitoring — a systematic review." Lancet Digit Health, 2026;8(2):100936. DOI:10.1016/j.landig.2025.100936 | PMID:41690859 — URL fetched: PubMed efetch (id=41690859) — Type: systematic review — Key numbers: 23 articles (searched to Aug 2024); feasible under controlled conditions, but heterogeneous methods, small samples and narrow BP ranges; no accepted validation protocols (authors include a radar-company CEO) — Verified: abstract + Crossref.

[device_engineer-16] Medical Device Coordination Group. "MDCG 2019-11 Rev.1 — Guidance on Qualification and Classification of Software in Regulation (EU) 2017/745 – MDR and 2017/746 – IVDR." European Commission, June 2025 (rev.1 of Oct 2019). — URL fetched: https://health.ec.europa.eu/document/download/b45335c5-1679-4c71-a91c-fc7a4d37f12b_en?filename=mdcg_2019_11_en.pdf — Type: regulatory guidance — Key numbers: Rule 11 text: decisions → IIa, IIb (serious deterioration), III (death/irreversible); monitoring → IIa, IIb if vital parameters with immediate danger; example: analysing physiological parameters (e.g. arterial stiffness) to prevent illness = Class IIa — Verified: PDF text read (section 4.2.1).

[device_engineer-17] Texas Instruments. "IWRL6432 Single-Chip 57- to 64-GHz Industrial Radar Sensor — datasheet SWRS298B." Dec 2022, revised Mar 2025. — URL fetched: https://www.ti.com/lit/ds/symlink/iwrl6432.pdf ; https://www.ti.com/product/IWRL6432 — Type: INDUSTRY-CLAIM (spec) — Key numbers: 2 TX / 3 RX, Cortex-M4F 160 MHz; active 690–1290 mW depending on TX/RX configuration and power topology (3.3 V IO table); idle 11.2 mW; deep sleep 0.66 mW; presence-detection use case at 1 Hz update averages 1.2 mW — Verified: datasheet text extracted.

[device_engineer-18] Analog Devices. "MAX86176/MAX30005 Ultra-Low-Power, Optical PPG and Single-Lead ECG AFE — data sheet (summary) Rev.3." 2022–2023; plus DigiKey price page for MAX86176ENX+T. — URL fetched: https://datasheet.lcsc.com/datasheet/pdf/6429318518b89c70a7ad24789040d528.pdf?productCode=C3197546 ; https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX86176ENX-T/15930386 — Type: INDUSTRY-CLAIM (spec/price) — Key numbers: optical readout <11 µA (typ) at 25 fps; shutdown 0.5 µA; PPG and ECG fully synchronised "for PTT measurements"; designed to meet IEC 60601-2-47; price $14.36 (1 pc), $9.87 (2,500-pc reel) — Verified: datasheet text extracted; DigiKey page fetched 2026-09-29.

[device_engineer-19] Nordic Semiconductor. "nRF52840 product page and SoC Product Brief v2.3." — URL fetched: https://www.nordicsemi.com/Products/nRF52840 ; https://nsscprodmedia.blob.core.windows.net/prod/software-and-other-downloads/product-briefs/nrf52840-soc-product-brief.pdf — Type: INDUSTRY-CLAIM (spec) — Key numbers: 64 MHz Cortex-M4 with FPU, 1 MB flash, 256 KB RAM; 6.40 mA at 0 dBm TX, 16.40 mA at +8 dBm — Verified: page and PDF text read. (Product-brief publication year not stated in the extracted text.)

[device_engineer-20] Burrello A et al. "Q-PPG: Energy-Efficient PPG-Based Heart Rate Monitoring on Wearable Devices." IEEE Trans Biomed Circuits Syst, 2021;15(6):1196–1209. DOI:10.1109/TBCAS.2021.3122017 | PMID:34673496 — URL fetched: PubMed efetch (id=34673496) — Type: bench/lab (PPG-DaLiA dataset + MCU deployment) — Key numbers: STM32WB55; best model MAE 4.41 BPM, 47.65 mJ per inference, 412 kB; smallest model 1.9 kB, 1.79 mJ per inference, MAE 8 BPM — Verified: abstract + Crossref.

[device_engineer-21] Leogrande E et al. "From PPG to Blood Pressure at the Edge: Quantization-Aware Architecture Selection and On-MCU Validation." Sensors, 2026;26(9):2674. DOI:10.3390/s26092674 | PMID:42122397 — URL fetched: PubMed efetch (id=42122397) — Type: bench/lab — Key numbers: several lightweight CNNs drift after INT8 conversion; a compact residual 1D CNN kept near-identical errors; real-time integer-only inference on STM32N6 — Verified: abstract + Crossref. WEAK (single group, no clinical validation).

[device_engineer-22] Wei L et al. "Assessing photoplethysmography signal quality for wearable devices during unrestricted daily activities." Biomed Phys Eng Express, 2025 (online; issue 2026). DOI:10.1088/2057-1976/ae250f | PMID:41308204 — URL fetched: PubMed efetch (id=41308204) — Type: validation study (single site) — Key numbers: 54 participants, headband PPG + accelerometer, 35,712 5-s epochs (good 10,817 / moderate 14,788 / poor 10,107); random forest 95.6% test accuracy; no significant accuracy difference across activity intensities — Verified: abstract + Crossref.

[device_engineer-23] Li J et al. "Federated learning for cardiovascular disease prediction: a systematic review of clinical applications, validation, and translation readiness." Front Cardiovasc Med, 2026;13:1831342. DOI:10.3389/fcvm.2026.1831342 | PMID:42338727 — URL fetched: PubMed efetch (id=42338727) — Type: systematic review — Key numbers: 22 studies (2022–2025); mostly horizontal FedAvg; evidence predominantly retrospective, often public datasets or simulated client splits; inconsistent reporting of external validation, calibration and system costs — Verified: abstract + Crossref.

[device_engineer-24] S R, Khekare G, Kumar Y, Soni G. "Quantifying energy and accuracy trade-offs of federated learning on wearable health devices." Front Big Data, 2026;9:1769948. DOI:10.3389/fdata.2026.1769948 | PMID:42221061 — URL fetched: PubMed efetch (id=42221061) — Type: simulation/bench — Key numbers: naive FL 35.3% energy saving (3.84 vs 5.93 kJ) but accuracy 84.94% vs 98.81% centralised (−13.87 points); 4.24 MFLOPs per training sample; training 1,066.26 s (~70× centralised) — Verified: abstract + Crossref. WEAK.

[device_engineer-25] Wilton AR et al. "Participant-Centered Engagement for Sustained Adherence to Smartwatches: A 12-Month Prospective Decentralized Digital Health Study." Clin Transl Sci, 2025;18(2):e70155. DOI:10.1111/cts.70155 | PMID:39954233 — URL fetched: PubMed efetch (id=39954233) — Type: prospective cohort — Key numbers: 298 recruited, 273 (92%) completed 12 months; mean wear-time adherence 77.4% (SD 32.64) with protocolised engagement and technology support; discomfort/intrusiveness associated with lower adherence — Verified: abstract + Crossref.

[device_engineer-26] Tran KV et al. "False Atrial Fibrillation Alerts from Smartwatches are Associated with Decreased Perceived Physical Well-being and Confidence in Chronic Symptoms Management." Cardiol Cardiovasc Med, 2023;7(2):97–107. DOI:10.26502/fccm.92920314 | PMID:37476150 — URL fetched: PubMed efetch (id=37476150) — Type: secondary analysis of RCT (Pulsewatch) — Key numbers: patients ≥50 y after stroke/TIA, 14-day wear; false AF alerts associated with a dose-dependent decline in self-perceived physical health and self-management — Verified: abstract + Crossref.

[device_engineer-27] Abumayyaleh M et al. "Sex differences and adherence of patients treated with wearable cardioverter-defibrillator: Insights from an international multicenter register." J Cardiovasc Electrophysiol, 2022. DOI:10.1111/jce.15648 | PMID:35930623 — URL fetched: PubMed efetch (id=35930623) — Type: retrospective registry — Key numbers: N=708; daily wear 21.1±4.3 h (men) vs 21.5±4.4 h (women); appropriate shocks 2.4% vs 3.9% — Verified: abstract + Crossref.

[device_engineer-28] Iyer S et al. "mm-Wave Radar-Based Vital Signs Monitoring and Arrhythmia Detection Using Machine Learning." Sensors, 2022;22(9):3106. DOI:10.3390/s22093106 | PMID:35590796 — URL fetched: PubMed efetch (id=35590796) — Type: bench/lab — Key numbers: 77 GHz FMCW; ANN trained on MIT-BIH (training accuracy 93.9%); tested on 15 subjects, mean test accuracy 75% — Verified: abstract + Crossref. WEAK.

[device_engineer-29] Gross-Isselmann JA et al. "Validation of the Sleepiz One + as a radar-based sensor for contactless diagnosis of sleep apnea." Sleep Breath, 2024;28(4):1691–1699. DOI:10.1007/s11325-024-03057-6 | PMID:38744804 — URL fetched: PubMed efetch (id=38744804) — Type: validation study vs PSG — Key numbers: N=141; AHI correlation r=0.94 (with SpO2) / 0.87 (without); sensitivity/specificity 85%/88% without SpO2, 88%/98% with SpO2 — Verified: abstract + Crossref.

[device_engineer-30] Xiao W et al. "A movable unshielded magnetocardiography system." Sci Adv, 2023;9(13):eadg1746. DOI:10.1126/sciadv.adg1746 | PMID:36989361 — URL fetched: PubMed efetch (id=36989361) — Type: bench/lab — Key numbers: MCG "usually require[s]… a magnetically shielded room"; OPM sensitivity 140 fT/Hz^1/2; resting and exercise MCG demonstrated unshielded — Verified: abstract + Crossref.

[device_engineer-31] Nasir N et al. "Medical device regulation and oversight in African countries: a scoping review of literature and development of a conceptual framework." BMJ Glob Health, 2023;8:e012308. DOI:10.1136/bmjgh-2023-012308 | PMID:37558270 — URL fetched: PubMed efetch (id=37558270) — Type: scoping review — Key numbers: 39 documents; limited pre-market testing, reliance on international certifications, weak post-market surveillance; funding and expertise gaps — Verified: abstract + Crossref.

[device_engineer-32] Abid L et al. "Epidemiologic features and management of hypertension in Tunisia, the results from the Hypertension National Registry (NaTuRe HTN)." BMC Cardiovasc Disord, 2022;22. DOI:10.1186/s12872-022-02584-y | PMID:35351007 — URL fetched: PubMed efetch (id=35351007) — Type: prospective registry (cross-sectional) — Key numbers: 25,890 hypertensive patients, 321 investigators; BP controlled in 51.7% (140/90 target) and 18.6% (130/80 target) — Verified: abstract + Crossref.

[background, pre-2021] IEEE 1708a-2019 (amendment to IEEE 1708 for wearable cuffless BP devices); Tunisian Organic Law 2004-63 on personal data protection; GDPR (2016). Context only; not retrieved this session and not used as sole support for any claim.

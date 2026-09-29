# Round 1 — Position paper: THE EM ENGINEER (`em_engineer`)

*Champion of the user's idea — the strongest case I can make honestly. Where the evidence goes against the idea, I say so.*

## 1 Persona

RF/microwave and bioelectromagnetics engineer (PhD); 12 years building mmWave/UWB radar vital-sign sensors, wrist bioimpedance front-ends and capacitive-ECG systems. Prior: the heart is an electromechanical pump. ECG gives electrical timing, bioimpedance volumetric change, radar mechanical motion; PPG gives none of these directly. Known bias: technology enthusiasm, underestimating motion artefacts and validation cost. Section 3.5 lists where this session's evidence corrected me.

## 2 Reading of the challenge: what actually scores

- **Everything that scores is longitudinal.** 60 points on RQ1–RQ6, judged by metrics A–F; the organisers reward *"the most credible scientific approach to detecting risk earlier."*
- **The target is emerging hypertension (F1).** An acute-MI or cardiac-arrest detector would score near zero on RQ1–RQ3 however good it was.
- **The supplied data probably has no ECG, radar or bioimpedance** (it lists PPG, HR/HRV, SpO2, respiration, activity, sleep, intermittent BP). EM therefore scores only through: (i) better *trajectory features* where EM channels exist or can be piloted; (ii) RQ5, via a modality-optional design; (iii) a credible engineering path in the report.
- **Hardware is not scored,** but the user wants a prototype that can really be built, so the proposal must earn its place inside and outside the scoring.

## 3 Verdict on the user's idea: REFRAME (keep the EM sensing, change the target)

### 3.1 Interpretations I evaluate

| "EM signal" | Maturity for this use (2021+ evidence) | My stance |
|---|---|---|
| Single-lead ECG (S2/S7) | Wearable, standards-grade AFEs exist [em_engineer-44]; PVC burden agrees with Holter [em_engineer-21] | **Defend: core** |
| Bioimpedance IPG (S3) | Promising, but only tiny, per-subject-calibrated studies [em_engineer-8, -9, -10] | Later (Tier C) |
| 60 GHz FMCW radar (S4) | HR/RR good; BP/PTT only feasibility-level [em_engineer-1, -2, -7] | **Defend: optional bedside tier** |
| RF→ECG reconstruction (S4) | r = 0.75 vs ECG in 6,974 people; ischaemia only qualitative [em_engineer-6] | Not a substitute for electrical ECG |
| NCS (S5) | I found no 2021+ BP validation; closest is an HF near-field resonator tested on N=2 [em_engineer-12] | Reject for now |
| OPM-MCG (S6) | Hospital/ED diagnostic, not wearable [em_engineer-13, -14, -15] | Reject for this challenge |

For **"sudden/premature cardiac attack"** I evaluate all four readings: acute MI, SCA, early-onset events and PVCs. I defend only the **PVC/arrhythmia** reading, and only as a secondary safety channel (F3).

### 3.2 Where F2 (as stated) fails on evidence

1. **Acute MI.** The best AI-ECG results for occlusion MI (7,313 patients) use **12-lead ECGs at triage, after symptoms start** [em_engineer-16]: diagnosis, not prediction. I found no 2021+ prospective study in which a *wearable* EM signal warns of MI hours to days ahead in free-living people. MCG in ED chest-pain patients: sensitivity 66.7%, specificity 57.1% (N=390) [em_engineer-13]; OPM-MCG: AUC 0.864 before angiography (N=141, single centre) [em_engineer-14]. Both are hospital tests.
2. **SCA.** 12-lead deep-learning risk scores reach external AUROC 0.820 [em_engineer-17]. Even with ECGs from within one day of arrest, specificity is **31% at 95% sensitivity**, "not clinically applicable" per the authors [em_engineer-18]. The best-evidenced consumer arrest detector I found is **PPG-based loss-of-pulse detection**, which detects rather than predicts: sensitivity 67.23%, 1 unintentional emergency call per 21.67 user-years [em_engineer-19]. Documented pre-arrest warnings are *symptoms* (dyspnoea 41% vs 22% in controls), not EM signatures [em_engineer-20].
3. **Fit.** Even if it worked, F2 would not score on RQ1–RQ6.

### 3.3 What survives from F2

"Premature" read as **PVCs**, together with AF, is well served by single-lead ECG. A patch measured PVC burden against Holter with a mean difference of −0.07% (LoA −1.44% to 1.30%, N=134) [em_engineer-21]. I keep this as an **F3 safety channel**: not scored, labelled "rhythm finding: see a clinician", and making no MI/SCA claim.

### 3.4 What EM adds over PPG, quantitatively (an honest ledger)

**For EM:**
- **ECG-HRV is not PPG-PRV.** In 931 clinical adults PPG-PRV significantly underestimated SDNN; in cardiovascular patients by 8.50 ms (95% CI 5.25–11.74) [em_engineer-29]. A 2026 meta-analysis found small errors, but only at rest, and warned against assuming interchangeability [em_engineer-30]. This matters: low HRV was associated with higher 4-year hypertension incidence in 7,665 normotensives [em_engineer-28].
- **Electrical timing enables PAT/PTT, a stiffness proxy.** Higher PWV is associated with incident hypertension (pooled RR 1.09, 95% CI 1.05–1.12; heterogeneous) [em_engineer-27]. Within a person, PAT tracked SBP with mean r = −0.82 ± 0.14 (N=75, 43.7% hypertensive) [em_engineer-25].
- **PAT-based estimates are repeatable.** Test–retest ICC > 0.7 despite poor absolute accuracy [em_engineer-11]: a profile suited to *personal change detection*, not cuffless BP.
- **PPG-only screening leaves headroom.** The FDA-cleared PPG hypertension notification: sensitivity **41.2%**, specificity 92.3% (N=2,229 enrolled, 30 days) [em_engineer-32]; a *Hypertension* commentary notes 59% of undiagnosed hypertensives would not be alerted [em_engineer-33].
- **Bioimpedance may see deeper.** Forearm IPG amplitude differed by BP status (p = 0.024, N=261); co-located PPG did not [em_engineer-10] (PREPRINT).

**Against EM (these rule out BP-estimation claims):**
- Two PPG morphology features outperformed PAT for BP across 2.4 million cycles [em_engineer-26].
- An expert review finds "no compelling evidence" that PAT/pulse-wave analysis add accuracy beyond calibration [em_engineer-23].
- Calibrated ECG + impedance timing BP had MAE 10.1–12.9 mmHg and missed mental-stress responses (N=41) [em_engineer-11].
- The PAT–SBP slope ranged from −2946 to −470.64 mmHg/s across 30 people [em_engineer-24], so EM features only work with personalisation (RQ1); the PAT–DBP correlation changed sign between exercise types [em_engineer-25].

**Net:** EM adds *physiologically distinct, repeatable timing features*, not proven absolute-BP accuracy. Whether it improves early warning over PPG alone is **untested**, so my prototype makes that the pre-registered ablation (E7).

### 3.5 Where the evidence corrected my priors

- **Skin tone:** evidence of PPG bias is **mixed** (4 of 10 studies found reduced accuracy in darker skin, 4 no effect) [em_engineer-31]. "EM avoids optical bias" is a design convenience, not a proven clinical advantage.
- **Radar BP is not ready:** 60 GHz radar SBP error 9.2 ± 8.3 mmHg, failing AAMI/BHS (N=55) [em_engineer-3]; the best radar-PTT result (DBP error SD 4.54–5.20 mmHg) needed per-subject calibration, static participants and a 12TX/16RX 77 GHz cascade board [em_engineer-7]; a 23-study review calls the field feasibility-level [em_engineer-1].
- **Capacitive ECG** still lacks sufficient clinical accuracy because of motion artefacts [em_engineer-40].
- **PEP matters:** separating PEP from PAT cut SBP error from 10.1 to 4.2 mmHg (MAD, N=10) [em_engineer-36], although under phenylephrine PEP moved only 5.5 ms vs −16.8 ms for PTT [em_engineer-24].

### 3.6 Direct answers to the required questions

- **Interpretations defended:** ECG as core, 60 GHz radar as optional bedside tier, bioimpedance later; "premature" only as PVC/AF in a safety channel.
- **Where the idea fails:** acute MI/SCA *prediction* (no wearable EM lead-time evidence) and fit to the scoring.
- **EM over PPG:** ECG-grade HRV (PRV underestimates SDNN by up to ~8.5 ms), within-person PAT–SBP r ≈ −0.82, possibly deep-tissue IPG; no proven absolute-BP gain.
- **Now vs later:** now, single-lead ECG + PPG wearable and bedside 60 GHz HR/RR/HRV; later, IPG, radar-PTT, PEP separation; never for this challenge, OPM-MCG.
- **Preferred prototype:** EM-ANCHOR.

## 4 Proposed prototype: EM-ANCHOR

Electrical timing *anchors* each person's hemodynamic baseline. (1) Twice-daily, context-standardised 2-minute seated spot-checks (fingertip on the watch electrode) give ECG-timed PAT, ECG-HRV and a rhythm check. (2) An optional bedside radar gives nightly HR, RR, radar-IBI and movement in stable sleep. (3) Both feed a personal-baseline trajectory engine whose backbone remains the challenge's PPG/activity data. The output is *risk of an emerging trajectory*, not BP.

```
PROTOTYPE CARD — EM-ANCHOR (ECG-anchored personal hemodynamic trajectory monitor + optional bedside radar)
Target: Primary — probability that a person has entered a persistent trajectory toward hypertension + timestamp of first reliable warning; reference = first HBPM/ABPM-confirmed hypertension (or the challenge's label). Secondary (unscored F3 safety channel) — AF/PVC-burden flags from ECG spot-checks; NO MI/SCA claim.
Sensors/modalities: Wrist unit — MAX86176 (2-channel PPG + single-lead ECG, hardware-synchronised for PTT) [em_engineer-44] + IMU + nRF52840 BLE SoC [em_engineer-45]; alternative chest-strap ECG + respiration-impedance front end ADS1292R [em_engineer-43]. Optional bedside 60 GHz FMCW radar — TI IWR6843(AOP) or low-power IWRL6432 [em_engineer-41, -42]. Validated home cuff weekly (S10) for sparse labels. Later: bioimpedance IPG (Tier C).
Development data: Challenge data for the trajectory engine; PulseDB (5,245,454 ECG+PPG+ABP 10-s segments, 5,361 subjects; access terms to check) [em_engineer-37] for PAT/HRV/SQI; 60 GHz radar + ECG dataset (110 participants) [em_engineer-38]; own 4-week pilot.
RQ1 Personal baseline: Robust per-person baselines (median/MAD) per feature *per context* (rest spot-check; stable-sleep window); hierarchical prior on the individual PAT→SBP slope, because slopes vary ~6-fold between people [em_engineer-24].
RQ2 Temporal/trajectory: Multivariate CUSUM/BOCPD on personal residuals; a trajectory is declared only with persistence (≥k of n weeks) plus multimodal agreement (PAT shortening, rising nocturnal HR, falling ECG-HRV).
RQ3 Early-warning / lead-time: Target pre-clinical drift in stiffness/autonomic markers (PWV and low HRV precede incident HTN [em_engineer-27, -28]); lead time measured against the clinical reference; alarm budget per person-month.
RQ4 Context handling: EM spot-checks are only accepted seated, IMU-still, ≥30 min after exercise; radar features only in stable-sleep windows (radar sleep staging 80.3% accuracy, κ 0.614 vs PSG, N=200 [em_engineer-39]); PEP-driven stress changes flagged as context, not trajectory [em_engineer-11].
RQ5 Robustness: Per-modality SQI (hardware ECG lead-off detection [em_engineer-44], PPG perfusion, radar motion index); modality-dropout training; automatic fallback to PPG-only (the probable challenge data) with widened uncertainty.
RQ6 Uncertainty & abstention: Poor-quality → suppressed (SQI fail); Insufficient → "keep monitoring" (too few valid days, or posterior credible interval of drift includes 0); Sufficient → calibrated risk + conformal interval.
Evidence/explanation output: Ledger — ΔPAT (ms vs baseline), weeks persistent, Δnocturnal HR, ΔRMSSD, modalities agreeing, valid-day coverage, SQI summary.
Edge vs cloud · power · BOM: Edge (nRF52840): R-peak/PPG-foot detection, PAT, HRV, SQI; phone/cloud: trajectory model. ECG only during spot-checks (low duty); radar mains-powered. BOM: UNSOURCED author estimate (to be quoted) — wearable parts < US$60, radar node < US$100; one group reports a 60 GHz radar system < US$30 (author-reported) [em_engineer-6].
Validation plan: Subject-wise + forward-chaining splits (E1); A–F metrics; pre-registered ablation PPG-only vs +ECG vs +radar (E7) with kill criterion (drop EM from the submission if no AUROC/lead-time gain); fairness by skin tone/BMI (E8). Any displayed BP number would need ESH intermittent-cuffless validation [em_engineer-22]; we output risk, not BP.
Regulatory / real-world path: ECG AFE designed for IEC 60601-2-47 (vendor claim) [em_engineer-44]. Radar under FCC §15.255 as amended by FCC 23-35 (57.0–59.4 GHz ≤20 dBm peak EIRP indoor, no off-time; 57–64 GHz ≤14 dBm with ≥25.5 ms off per 33 ms) [em_engineer-34]; EU ETSI EN 305 550 (cited in that order); Tunisian type approval to verify. No confirmed hazard from low-level RF > 6 GHz [em_engineer-35]. IEC 62304/ISO 14971 once medical claims are made.
Biggest risk + mitigation: EM features add nothing over PPG, or the challenge data lacks EM channels → modality-optional architecture, ablation with kill criterion, negative result reported honestly; pilot data shows feasibility only (not HTN prediction).
Buildable by a student team? 4–8 weeks: trajectory engine on challenge data; PAT/HRV/SQI pipeline on PulseDB; MAX86176 or ADS1292R + nRF52840 spot-check logger; optional IWR6843AOP bedside logger vs chest ECG on 5–10 volunteers. Later: IPG, radar-PTT, PEP separation, ABPM clinical cohort.
```

## 5 Claims table

| ID | Claim | Refs | Strength |
|---|---|---|---|
| C1 | AI-ECG detection of occlusion MI relies on 12-lead ECGs at triage (N=7,313), not wearable prediction | 16 | STRONG |
| C2 | MCG/OPM-MCG detect ischaemia only in hospital settings (sens 66.7%/spec 57.1%, N=390; AUC 0.864, N=141) | 13, 14 | MODERATE |
| C3 | 12-lead DL predicts SCA risk (ext. AUROC 0.820) but at 95% sensitivity specificity is 31% | 17, 18 | MODERATE |
| C4 | The best-evidenced consumer arrest detector is PPG loss-of-pulse (sens 67.23%; 1 unintentional emergency call per 21.67 user-years) — detection, not prediction | 19 | STRONG |
| C5 | Single-lead ECG patch quantifies PVC burden vs Holter (mean diff −0.07%) | 21 | MODERATE |
| C6 | PPG-PRV underestimates ECG-HRV in clinical populations (SDNN gap 8.50 ms, CV patients) | 29, 30 | MODERATE |
| C7 | Low HRV and higher PWV precede incident hypertension | 27, 28 | STRONG |
| C8 | PAT tracks SBP within individuals (r −0.82 ± 0.14), but slopes are highly individual and DBP relations unstable; PAT-based estimates are repeatable (ICC > 0.7) | 11, 24, 25 | MODERATE |
| C9 | PAT/PTT-based cuffless BP is not accurate enough for clinical use, even with calibration | 11, 23 | STRONG |
| C10 | PPG morphology can outperform PAT for BP estimation | 26 | MODERATE |
| C11 | PPG-only FDA-cleared HTN notification: sens 41.2%, spec 92.3% | 32, 33 | STRONG |
| C12 | Radar HR within 10% of reference in 87% of studies; radar HRV HF-norm error ~5% (N=25) | 2, 4 | MODERATE |
| C13 | Radar BP/PTT is feasibility-level only (small N, calibration, static subjects) | 1, 3, 7 | MODERATE |
| C14 | Radar-to-ECG reconstruction r = 0.75 (N=6,974); ischaemia shown only qualitatively | 6 | MODERATE |
| C15 | Bioimpedance BP results come from very small, per-subject-calibrated studies; IPG may carry BP-status information that PPG lacks | 8, 9, 10 | WEAK |
| C16 | US rules permit 57.0–59.4 GHz radar at ≤20 dBm peak EIRP indoors (FCC 23-35); no confirmed health hazard from low-level RF > 6 GHz | 34, 35 | STRONG (regulatory) / MODERATE (review) |
| C17 | Evidence of PPG skin-tone bias is inconclusive | 31 | MODERATE |

## 6 Anticipated attacks and pre-emptive defence

- **ppg_scientist — "PAT adds nothing; PPG morphology wins [26, 23]."** Agreed for *absolute BP*. My claim is narrower: ECG-HRV ≠ PRV [29] and repeatable PAT [11] suit change detection. The E7 ablation with a kill criterion decides; I concede if it fails.
- **clinician — "'Cardiac attack' language invites false reassurance."** Agreed. The safety channel covers only AF/PVC, where wearable-ECG evidence exists [21], with explicit no-MI/no-SCA labelling.
- **device_engineer — "Radar is fragile (motion, multipath, cost, regulation)."** Hence radar is *optional*, nightly and bedside (lowest motion), using single-chip 60 GHz parts permitted under FCC 23-35 [34]. Radar BP/PTT needs cascade hardware and static subjects [7], so it is deferred.
- **bayesian_ml — "The challenge data has no ECG."** The architecture is modality-optional (scores on RQ5); the EM tier serves the user's real-world prototype requirement.
- **physiologist — "PAT includes PEP; sympathetic state confounds it."** Rest-context standardisation limits this; under vasoconstriction PEP change is small relative to PTT [24]; PEP/PTT separation (radar/SCG/ICG fiducials [36]) is Tier C.

## 7 Risks and limitations

- There is no longitudinal evidence yet that EM features give *earlier* hypertension warnings than PPG. This is my central unproven hypothesis.
- Spot-check ECG needs user action, so adherence decays.
- Radar needs an unobstructed line of sight; bed partners cause multi-target confusion; I found no 2021+ multi-month in-home radar-HTN study.
- Most radar and bioimpedance studies are small and lab-based, with young and healthy participants [1, 9, 11].
- PulseDB is ICU/surgical data, so there is a domain shift from free-living wearables [37].
- BOM figures are unsourced estimates, and hardware specs are vendor claims.

## 8 References

[em_engineer-1] Falconer D et al. "Emerging radar-based technologies for cuffless blood pressure monitoring—a systematic review." Lancet Digit Health, 2026. DOI:10.1016/j.landig.2025.100936 | PMID:41690859 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=41690859&rettype=abstract&retmode=text — Type: review (systematic) — Key numbers: 23 articles (1990–Aug 2024); feasible under controlled conditions; heterogeneous methods, small samples, narrow BP ranges; needs large multimorbid cohorts incl. hypertension — Verified: PubMed abstract read.

[em_engineer-2] Liebetruth M et al. "Systematic Literature Review Regarding Heart Rate and Respiratory Rate Measurement by Means of Radar Technology." Sensors, 2024. DOI:10.3390/s24031003 | PMID:38339721 — URL fetched: PubMed efetch (id=38339721) — Type: review (systematic) — Key numbers: max deviation ≤5% in 48% (HR) / 37% (RR) of studies; ≤10% in 87% (HR) / 85% (RR); limited comparability — Verified: PubMed abstract read.

[em_engineer-3] Vysotskaya N et al. "Continuous Non-Invasive Blood Pressure Measurement Using 60 GHz-Radar—A Feasibility Study." Sensors, 2023. DOI:10.3390/s23084111 | PMID:37112454 — URL fetched: PubMed efetch (id=37112454) — Type: validation study (lab) — Key numbers: N=55; 21 radar features + age/gender/height/weight; SBP error 9.2±8.3, DBP 7.7±5.7 mmHg; did not meet AAMI/BHS — Verified: PubMed abstract read.

[em_engineer-4] Shi K et al. "Contactless analysis of heart rate variability during cold pressor test using radar interferometry and bidirectional LSTM networks." Sci Rep, 2021. DOI:10.1038/s41598-021-81101-1 | PMID:33542260 — URL fetched: PubMed efetch (id=33542260) — Type: validation study (lab) — Key numbers: 24 GHz six-port radar; N=25; 638 min; heartbeat F-score >95%; HRV indices (e.g., HF norm) relative error ~5% — Verified: PubMed abstract read.

[em_engineer-6] Lu Z et al. "Contactless 12-lead electrocardiogram via deep computational radar." npj Biomed Innov, 2026. DOI:10.1038/s44385-025-00060-8 | PMID:42032310 — URL fetched: PubMed efetch (id=42032310) and https://pmc.ncbi.nlm.nih.gov/articles/PMC13055045/ — Type: validation study — Key numbers: N=6,974; mean correlation 0.75 (median 0.77), RMSE 0.09 mV vs ECG; 60 GHz LFMCW, 4 GHz BW, 3×4 MIMO, ~0.5 m, system cost <$30 (author-reported); AF sens 0.867 / spec 0.993; ST depression shown qualitatively only — Verified: abstract + PMC full text via WebFetch.

[em_engineer-7] Zhu J et al. "Measuring multi-site pulse transit time with an AI-enabled mmWave radar." Nat Commun, 2026. DOI:10.1038/s41467-026-73453-x | PMID:42185285 — URL fetched: PubMed efetch (id=42185285) and https://pmc.ncbi.nlm.nih.gov/articles/PMC13201791/ — Type: validation study (lab) — Key numbers: N=47 (22 development, 25 evaluation; 6 hypertensive, 2 AF); TI AWR2243 cascade 77–81 GHz, 12TX/16RX; PTT r 0.75–0.86; DBP r 0.90–0.91, mean error −0.62 to 0.06, SD 4.54–5.20 mmHg; per-subject calibration (3 recordings); exercise protocol; participants static — Verified: abstract + PMC full text via WebFetch.

[em_engineer-8] Kireev D et al. "Continuous cuffless monitoring of arterial blood pressure via graphene bioimpedance tattoos." Nat Nanotechnol, 2022. DOI:10.1038/s41565-022-01145-w | PMID:35725927 — URL fetched: PubMed efetch (id=35725927) — Type: bench/lab validation — Key numbers: >300 min monitoring; DBP 0.2±4.5, SBP 0.2±5.8 mmHg; N not stated in abstract — Verified: PubMed abstract read (full text paywalled).

[em_engineer-9] Sel K et al. "Continuous cuffless blood pressure monitoring with a wearable ring bioimpedance device." npj Digit Med, 2023. DOI:10.1038/s41746-023-00796-w | PMID:36997608 — URL fetched: PubMed efetch (id=36997608) and https://pmc.ncbi.nlm.nih.gov/articles/PMC10063561/ — Type: validation study (lab) — Key numbers: N=10 (19–26 y, 9 male); cold pressor; Finapres reference; per-subject 5-fold models; SBP 0.11±5.27, DBP 0.11±3.87 mmHg; r 0.76/0.81; 10 kHz injection — Verified: abstract + PMC full text via WebFetch.

[em_engineer-10] Thomson S et al. "Deep-Tissue Hemodynamic Sensing: Comparing Impedance and Photoplethysmography for Wearable Blood Pressure Estimation." medRxiv (openRxiv), 2026. DOI:10.64898/2026.06.17.26355894 — URL fetched: Europe PMC REST search (PPR1257288) + https://api.crossref.org/works/10.64898/2026.06.17.26355894 — Type: PREPRINT — Key numbers: N=261 (130 hypertensive); >150,000 cycles; forearm IPG amplitude main effect for BP status p=0.024, absent in co-located PPG; BMI attenuates steep-upstroke IPG archetypes p=0.035 — Verified: abstract read; DOI confirmed on Crossref.

[em_engineer-11] Schoenmakers M et al. "Validation study on cuffless ambulatory blood pressure monitoring method using bio-impedance, impedance cardiography and electrocardiography." Eur J Appl Physiol, 2026. DOI:10.1007/s00421-026-06404-5 | PMID:42782336 — URL fetched: PubMed efetch (id=42782336) — Type: validation study — Key numbers: N=41 young healthy; posture/activity/mental stress; test–retest ICC >0.7; calibrated MAE 10.1–12.9 mmHg, 59.2–68.5% within 10 mmHg; mental-stress BP responses not detected — Verified: PubMed abstract read.

[em_engineer-12] Mohammed N et al. "A Flexible Near-Field Biosensor for Multisite Arterial Blood Flow Detection." Sensors, 2022. DOI:10.3390/s22218389 | PMID:36366092 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC9657423/ — Type: bench/lab — Key numbers: HF resonator ~34.5 MHz; 2 subjects; SNR 18.18 dB; multisite pulse waveforms — Verified: PMC full text via WebFetch.

[em_engineer-13] Mace SE et al. "Accelerated magnetocardiography in the evaluation of patients with suspected cardiac ischemia: The MAGNETO trial." Am Heart J Plus, 2024. DOI:10.1016/j.ahjo.2024.100372 | PMID:38586432 — URL fetched: PubMed efetch (id=38586432) — Type: prospective cohort (multicentre, ED) — Key numbers: N=390; 90-s MCG; sens 66.7% (50.5–80.4), spec 57.1% (50.0–63.3) vs stress-test spec 89.9% — Verified: PubMed abstract read.

[em_engineer-14] Yang S et al. "Development and validation of a clinical diagnostic model for myocardial ischaemia in borderline coronary lesions based on optical pumped magnetometer magnetocardiography." BMJ Open, 2024. DOI:10.1136/bmjopen-2024-086433 | PMID:39461859 — URL fetched: PubMed efetch (id=39461859) — Type: prospective cohort (single centre) — Key numbers: n=141; AUC 0.864 (0.803–0.925); sens 79.4%, spec 80.8%; FFR reference before angiography — Verified: PubMed abstract read.

[em_engineer-15] Xiao W et al. "A movable unshielded magnetocardiography system." Sci Adv, 2023. DOI:10.1126/sciadv.adg1746 | PMID:36989361 — URL fetched: PubMed efetch (id=36989361) — Type: bench/lab — Key numbers: OPM sensitivity 140 fT/Hz^1/2; resting and exercise MCG demonstrated unshielded; conventional MCG needs a shielded room and a still participant — Verified: PubMed abstract read.

[em_engineer-16] Al-Zaiti SS et al. "Machine learning for ECG diagnosis and risk stratification of occlusion myocardial infarction." Nat Med, 2023. DOI:10.1038/s41591-023-02396-3 | PMID:37386246 — URL fetched: PubMed efetch (id=37386246) — Type: prospective/observational cohort with external validation — Key numbers: 7,313 consecutive chest-pain patients, multisite; outperformed clinicians and commercial systems; reclassified 1 in 3 patients — Verified: PubMed abstract read.

[em_engineer-17] Holmstrom L et al. "An ECG-based artificial intelligence model for assessment of sudden cardiac death risk." Commun Med, 2024. DOI:10.1038/s43856-024-00451-9 | PMID:38413711 — URL fetched: PubMed efetch (id=38413711) — Type: retrospective case-control with external validation — Key numbers: 1,827 pre-arrest 12-lead ECGs (1,796 SCD cases); AUROC 0.889 internal, 0.820 external; conventional ECG model 0.712/0.743 — Verified: PubMed abstract read.

[em_engineer-18] Oberdier MT et al. "Sudden cardiac arrest prediction via deep learning electrocardiogram analysis." Eur Heart J Digit Health, 2025. DOI:10.1093/ehjdh/ztae088 | PMID:40110219 — URL fetched: PubMed efetch (id=40110219) — Type: retrospective — Key numbers: 221 SCA vs 1,046 controls; 10-s 12-lead ECG within 1 day of arrest; AUROC 0.77; at 95% sensitivity specificity 31% ("not clinically applicable") — Verified: PubMed abstract read.

[em_engineer-19] Shah K et al. "Automated loss of pulse detection on a consumer smartwatch." Nature, 2025. DOI:10.1038/s41586-025-08810-9 | PMID:40010378 — URL fetched: Europe PMC REST (MED 40010378) abstract — Type: prospective validation — Key numbers: PPG-based multimodal ML; 1 unintentional emergency call per 21.67 user-years; sensitivity 67.23% (64.32–70.05%) in a prospective arterial-occlusion simulation — Verified: abstract read.

[em_engineer-20] Reinier K et al. "Warning symptoms associated with imminent sudden cardiac arrest: a population-based case-control study with external validation." Lancet Digit Health, 2023. DOI:10.1016/S2589-7500(23)00147-4 | PMID:37640599 — URL fetched: Europe PMC REST abstract — Type: retrospective case-control — Key numbers: 411 SCA (discovery) vs 1,171 controls; dyspnoea 41% vs 22%, chest pain 33% vs 25% — Verified: abstract read.

[em_engineer-21] Ahn HJ et al. "Three-Day Monitoring of Adhesive Single-Lead Electrocardiogram Patch for Premature Ventricular Complex." J Med Internet Res, 2024. DOI:10.2196/46098 | PMID:38512332 — URL fetched: PubMed efetch (id=38512332) — Type: prospective validation study — Key numbers: N=134; PVC burden vs Holter mean diff −0.07% (LoA −1.44% to 1.30%) — Verified: PubMed abstract read.

[em_engineer-22] Stergiou GS et al. "European Society of Hypertension recommendations for the validation of cuffless blood pressure measuring devices." J Hypertens, 2023. DOI:10.1097/HJH.0000000000003483 | PMID:37303198 — URL fetched: PubMed efetch (id=37303198) — Type: guideline — Key numbers: six validation tests for intermittent cuffless devices (incl. static, device-position, treatment tests); tests depend on calibration and use — Verified: PubMed abstract read.

[em_engineer-23] Mukkamala R et al. "Cuffless Blood Pressure Measurement: Where Do We Actually Stand?" Hypertension, 2025. DOI:10.1161/HYPERTENSIONAHA.125.24822 | PMID:40231350 — URL fetched: PubMed efetch (id=40231350) — Type: review (expert) — Key numbers: "no compelling evidence" that PWA/PAT add accuracy beyond cuff/demographic calibration — Verified: PubMed abstract read.

[em_engineer-24] Finnegan E et al. "Pulse arrival time as a surrogate of blood pressure." Sci Rep, 2021. DOI:10.1038/s41598-021-01358-4 | PMID:34815419 — URL fetched: PubMed efetch (id=34815419) — Type: validation study (pharmacological) — Key numbers: N=30 healthy; phenylephrine; PEP +5.5±4.5 ms vs PTT −16.8±7.5 ms; individual PAT–SBP slope −2946 to −470.64 mmHg/s; calibrated RMSE SBP 5.49 (PAT) / 4.51 (PTT) mmHg; population models ~2× error — Verified: PubMed abstract read.

[em_engineer-25] Heimark S et al. "Blood pressure altering method affects correlation with pulse arrival time." Blood Press Monit, 2022. DOI:10.1097/MBP.0000000000000577 | PMID:34855653 — URL fetched: PubMed efetch (id=34855653) — Type: validation study — Key numbers: N=75 (43.7% hypertensive); chest-belt ECG+PPG; within-subject PAT–SBP r −0.82±0.14; PAT–DBP r 0.25±0.35 (sign varies by exercise type) — Verified: PubMed abstract read.

[em_engineer-26] Yang S et al. "Estimation and Validation of Arterial Blood Pressure Using Photoplethysmogram Morphology Features in Conjunction With Pulse Arrival Time in Large Open Databases." IEEE J Biomed Health Inform, 2021. DOI:10.1109/JBHI.2020.3009658 | PMID:32750963 — URL fetched: PubMed efetch (id=32750963) — Type: retrospective (open databases) — Key numbers: 2.4 million cycles; two PPG morphology features outperformed PAT; SBP 0.05±6.92 mmHg; external 334 ICU patients — Verified: PubMed abstract read.

[em_engineer-27] Saz-Lara A et al. "Association Between Arterial Stiffness and Blood Pressure Progression With Incident Hypertension: A Systematic Review and Meta-Analysis." Front Cardiovasc Med, 2022. DOI:10.3389/fcvm.2022.798934 | PMID:35224042 — URL fetched: PubMed efetch (id=35224042) — Type: meta-analysis — Key numbers: PWV RR 1.09 (1.05–1.12), SBP RR 1.08 (1.05–1.10) for incident HTN; considerable heterogeneity — Verified: PubMed abstract read.

[em_engineer-28] Hoshi RA et al. "Reduced heart-rate variability and increased risk of hypertension—a prospective study of the ELSA-Brasil." J Hum Hypertens, 2021. DOI:10.1038/s41371-020-00460-w | PMID:33462386 — URL fetched: PubMed efetch (id=33462386) — Type: prospective cohort — Key numbers: 7,665 normotensives; 4-year follow-up; low (<P25) HRV indices associated with increased hypertension incidence after full adjustment — Verified: PubMed abstract read.

[em_engineer-29] Kantrowitz AB et al. "Pulse rate variability is not the same as heart rate variability: findings from a large, diverse clinical population study." Front Physiol, 2025. DOI:10.3389/fphys.2025.1630032 | PMID:40809286 — URL fetched: PubMed efetch (id=40809286) — Type: validation study — Key numbers: N=931; PPG-PRV significantly underestimated SDNN/rMSSD/pNN50; SDNN difference cardiovascular 8.50 ms (5.25–11.74) — Verified: PubMed abstract read.

[em_engineer-30] Xu S et al. "Accuracy of Photoplethysmography-Derived Pulse Rate Variability Compared with Electrocardiography-Derived Heart Rate Variability: A Systematic Review and Meta-Analysis." Sensors, 2026. DOI:10.3390/s26165192 | PMID:42655500 — URL fetched: PubMed efetch (id=42655500) — Type: meta-analysis — Key numbers: 10 studies; pooled absolute standardized error 0.188 (RMSSD), 0.134 (SDNN); resting/controlled only; not evidence of interchangeability — Verified: PubMed abstract read.

[em_engineer-31] Koerber D et al. "Accuracy of Heart Rate Measurement with Wrist-Worn Wearable Devices in Various Skin Tones: a Systematic Review." J Racial Ethn Health Disparities, 2023. DOI:10.1007/s40615-022-01446-9 | PMID:36376641 — URL fetched: PubMed efetch (id=36376641) — Type: review (systematic) — Key numbers: 10 studies, 469 participants; 4 reduced accuracy in darker skin, 4 no effect, 2 mixed — Verified: PubMed abstract read.

[em_engineer-32] U.S. FDA. 510(k) K250507, Hypertension Notification Feature (Apple Inc.), decision letter dated 12 Sep 2025, 21 CFR 870.2380. — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250507.pdf — Type: regulatory — Key numbers: PPG-based; 2,229 enrolled, 1,863 analysable; 30-day HBPM reference (≥130/80 mmHg); sens 41.2% (37.2–45.3), spec 92.3% (90.6–93.7), PPV 70.9% at 31.4% prevalence — Verified: PDF text extracted this session.

[em_engineer-33] Cohen JB et al. "Apple Watch for Hypertension Screening." Hypertension, 2026. DOI:10.1161/HYPERTENSIONAHA.125.26031 | PMID:41564145 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC12826266/ — Type: review (commentary) — Key numbers: 59% of undiagnosed hypertensives would not be alerted; judged not suitable for large-scale reliable screening — Verified: PMC full text via WebFetch.

[em_engineer-34] U.S. FCC. Report and Order FCC 23-35, "Amendment of Section 15.255 of the Commission's Rules," ET Docket No. 21-264, adopted 18 May 2023, released 19 May 2023. — URL fetched: https://docs.fcc.gov/public/attachments/FCC-23-35A1_Rcd.pdf — Type: regulatory — Key numbers: FDS/radar 57.0–59.4 GHz ≤20 dBm peak EIRP indoor (30 outdoor), no off-time; 57.0–61.56 GHz ≤3 dBm, or ≤20 dBm with ≥16.5 ms off per 33 ms; 57–64 GHz ≤14 dBm with ≥25.5 ms off per 33 ms; references ETSI EN 305 550 — Verified: PDF text extracted this session.

[em_engineer-35] Karipidis K et al. "5G mobile networks and health—a state-of-the-science review of the research into low-level RF fields above 6 GHz." J Expo Sci Environ Epidemiol, 2021. DOI:10.1038/s41370-021-00297-6 | PMID:33727687 — URL fetched: PubMed efetch (id=33727687) — Type: review — Key numbers: 107 experimental + 31 epidemiological (radar) studies; no confirmed evidence that low-level RF > 6 GHz is hazardous — Verified: PubMed abstract read.

[em_engineer-36] Beutel F et al. "Pulse Arrival Time Segmentation Into Cardiac and Vascular Intervals—Implications for Pulse Wave Velocity and Blood Pressure Estimation." IEEE Trans Biomed Eng, 2021. DOI:10.1109/TBME.2021.3055154 | PMID:33513094 — URL fetched: PubMed efetch (id=33513094) — Type: bench/lab — Key numbers: N=10; SBP MAD from central PWV 4.2 vs peripheral PWV 7.1 vs PAT 10.1 mmHg — Verified: PubMed abstract read.

[em_engineer-37] Wang W et al. "PulseDB: A large, cleaned dataset based on MIMIC-III and VitalDB for benchmarking cuff-less blood pressure estimation methods." Front Digit Health, 2023. DOI:10.3389/fdgth.2022.1090854 | PMID:36844249 — URL fetched: PubMed efetch (id=36844249) — Type: dataset paper — Key numbers: 5,245,454 10-s ECG+PPG+ABP segments; 5,361 subjects — Verified: PubMed abstract read.

[em_engineer-38] Parralejo F et al. "Extensive Age-Balanced and Subject-Varied mmWave Radar Dataset of Referenced Records for Vital Signs." Sci Data, 2026. DOI:10.1038/s41597-026-07172-9 | PMID:41946749 — URL fetched: PubMed efetch (id=41946749) — Type: dataset paper — Key numbers: 110 participants; two commercial 60 GHz FMCW radars; class IIa ECG+accelerometer reference; 15 with heart issues; postures, post-exercise, breath-hold — Verified: PubMed abstract read.

[em_engineer-39] Sun L et al. "Validation of a low-load monitoring system based on millimeter-wave radar and pulse oximetry vs. polysomnography for obstructive sleep apnea diagnosis." Sleep Health, 2025. DOI:10.1016/j.sleh.2025.09.002 | PMID:41073231 — URL fetched: PubMed efetch (id=41073231) — Type: validation study (diagnostic) — Key numbers: N=200; AHI ICC 0.965; event-level apnea-hypopnea sens 83.4%/spec 94.3%; sleep staging accuracy 80.3% (κ 0.614) — Verified: PubMed abstract read.

[em_engineer-40] Khalili M et al. "Motion artifacts in capacitive ECG monitoring systems: a review of existing models and reduction techniques." Med Biol Eng Comput, 2024. DOI:10.1007/s11517-024-03165-1 | PMID:39031328 — URL fetched: PubMed efetch (id=39031328) — Type: review — Key numbers: capacitive-ECG signals often lack sufficient clinical accuracy due to motion artefacts; ETI-reference DSP promising — Verified: PubMed abstract read.

[em_engineer-41] Texas Instruments. IWR6843 product page. — URL fetched: https://www.ti.com/product/IWR6843 — Type: INDUSTRY-CLAIM — Key numbers: 60–64 GHz, 4 GHz continuous BW, 3TX/4RX, C67x DSP 600 MHz + Cortex-R4F 200 MHz, FFT/CFAR accelerator, 10.4×10.4 mm FCBGA; no price shown — Verified: WebFetch.

[em_engineer-42] Texas Instruments. IWRL6432 product page. — URL fetched: https://www.ti.com/product/IWRL6432 — Type: INDUSTRY-CLAIM — Key numbers: 57–64 GHz, 2TX/3RX, Cortex-M4F 160 MHz, idle/deep-sleep low-power modes, 6.45×6.45 mm; no price shown — Verified: WebFetch.

[em_engineer-43] Texas Instruments. ADS1292R product page. — URL fetched: https://www.ti.com/product/ADS1292R — Type: INDUSTRY-CLAIM — Key numbers: 2-channel 24-bit ΔΣ, 335 µW/channel, integrated respiration impedance measurement; no price shown — Verified: WebFetch.

[em_engineer-44] Analog Devices. MAX86176/MAX30005 data sheet, Rev. 3 (distributor mirror). — URL fetched: https://datasheet.lcsc.com/datasheet/pdf/6429318518b89c70a7ad24789040d528.pdf?productCode=C3197546 — Type: INDUSTRY-CLAIM — Key numbers: 2 optical channels (≤6 LEDs, 4 PDs) fully synchronised with single-lead ECG "for PTT measurements"; optical channel <11 µA typ at 25 fps; AC/DC lead-off detection; designed to meet IEC 60601-2-47 with dry electrodes; 36-bump WLP — Verified: PDF text extracted (analog.com unreachable from this machine).

[em_engineer-45] Nordic Semiconductor. nRF52840 product page. — URL fetched: https://www.nordicsemi.com/Products/nRF52840 — Type: INDUSTRY-CLAIM — Key numbers: 64 MHz Cortex-M4F, 1 MB flash, 256 KB RAM, Bluetooth LE 5.4, +8 dBm TX — Verified: WebFetch.

*(ID -5 intentionally unused: source retrieved but dropped as redundant.)*

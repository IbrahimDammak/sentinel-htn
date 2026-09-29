# Audit round 1, team C (Auditor): does each source support what it is cited for?

Levels: STRONG / MODERATE / WEAK / REG (regulatory record) / SPEC (vendor spec, INDUSTRY-CLAIM). "Unv." = unverifiable from abstract.

# PART 1. PHYSIOLOGIST (31 refs)

| Ref | Cited for (line) | Verdict | Evidence level | Note |
|---|---|---|---|---|
| 1 | HRV Q1 vs Q5 HR 1.58, N=232,587, 3.8 y; HRV rise protective (L11, 44, 157) | SUPPORTED | STRONG (association only) | Numbers exact. 10-s clinic ECG, not wearable. L157 "within-person" is only a change-score association. |
| 2 | RHR HR 1.06/10 bpm, older adults (L44) | SUPPORTED | MODERATE-WEAK | CI 1.01-1.12 borderline; CLHLS elderly only. |
| 3 | PWV pooled RR 1.09, heterogeneity (L32) | SUPPORTED | MODERATE | Heterogeneity disclosed. Corrigendum exists. |
| 4 | SDPTG d/a HR 2.84, N=902 men (L32, 45) | SUPPORTED | WEAK-MODERATE | 124 cases, one cohort, finger PPG at checkup. b/a null, not mentioned. |
| 5 | PPG morphology as vascular axis (L45) | SUPPORTED | MODERATE (review) | Generic narrative review; does not test HTN prediction. |
| 6 | Steps OR 0.92/1,000; plateau 8-9k (L47) | SUPPORTED | MODERATE | OR from full text. Reverse causation/healthy-user not mentioned; 84% white. |
| 7 | Sleep-SD OR 1.56; 5 h vs 6.8 h HR 1.29 (L11, 46) | SUPPORTED | MODERATE | Full-text numbers. OR and HR from one cohort. Fitbit EHR-linked, self-selected. |
| 8 | Short sleep HR 1.07; <5 h 1.11 (L46) | SUPPORTED | STRONG | Exact match. |
| 9 | OSA 40-80% in hypertension (L46) | SUPPORTED | STRONG (AHA statement) | Abstract lumps HTN with HF, CAD, AF. |
| 10 | Night BP better predictor (L41) | SUPPORTED | MODERATE (expert consensus) | Asian consensus; not primary evidence. |
| 11 | Weight gain >10% HR 1.60/2.44/4.51, 1.66 y (L11, 47, 157) | SUPPORTED | MODERATE | Exact. Self-reported weight, drug-start outcome, blood donors; weight is not wearable physiology. |
| 12 | none | UNCITED | n/a | Listed only. Remove or use. |
| 13 | ICG PEP; PEP -16% mental, halves physical (L28, 89) | SUPPORTED | MODERATE-WEAK | Lab, N=71 young adults. |
| 14 | PAT-DBP sign flips with exercise type (L90) | SUPPORTED | MODERATE | Flip is DBP only; SBP stays negative. Line says "PAT-DBP", correct. |
| 15 | PAT response HR 1.20/SD for CVD (L45, 66) | PARTIAL | WEAK | 65 events, CI 1.02-1.42, outcome CVD (not HTN), older MESA sleep cohort. |
| 16 | SBP error SD -15-20% in calibration posture (L65, 87) | SUPPORTED | MODERATE | Exact. |
| 17 | Cuffless: notification not diagnosis (L57, 119) | SUPPORTED | STRONG (society statement) | Fine. |
| 18 | Apple 41% sens, 92% spec, N=2,229 (L35) | PARTIAL | MODERATE; should be INDUSTRY-CLAIM | Commentary relaying manufacturer data. 2,229 is enrolled; 1,863 analysable per device_engineer-1. Not labelled INDUSTRY-CLAIM. |
| 19 | Apple ML notification 510(k)-cleared (L35) | UNV. | n/a | **Reference entry is corrupted**: it holds a paragraph of the paper, not a citation. Clearance confirmed by device_engineer-1 (K250507). |
| 20 | AIRE-HTN C 0.70 int/ext, C 0.67-0.72, NRI 0.32-0.44 (L35, 48) | SUPPORTED | MODERATE | Exact. Retrospective development; C 0.70 modest. |
| 21 | HR/temp follow menstrual cycle (L11, 85) | SUPPORTED | MODERATE-WEAK | N=116, one cycle each. |
| 22 | Illness: 3 days pre-symptom; "temperature + RHR/step" pattern (L11, 84) | PARTIAL | MODERATE | Study used HR and steps only; "temperature" not in abstract. Non-infection alerts honestly support L11. |
| 23 | Alcohol raises nocturnal RHR ~3 bpm, recovers (L11, 83) | SUPPORTED | WEAK | N=40, heavy dosing (40-60 g/d), young; post-exposure 64.9 vs 63.6 baseline. |
| 24 | 0.61 mmHg per 1 C drop (L86) | SUPPORTED | MODERATE | Concurrent-day panel of hypertensives. |
| 25 | Wearables CCC 0.97-0.98 RHR, 0.97-0.99 HRV, 536 nights (L41) | PARTIAL | WEAK-MODERATE | Best device (Oura) only; N=13; nights not independent. Polar 0.86/0.82, Whoop 0.91/0.94. |
| 26 | PRV-HRV not generalisable to free-living (L41) | SUPPORTED | MODERATE | Honest; 10 studies quantitative. |
| 27 | Warning-symptom ORs by sex (L18) | SUPPORTED | MODERATE | Exact; control caveat honest. Men's diaphoresis did not replicate (omitted). |
| 28 | Near-term VT AUROC 0.957/0.948; sens 70.6/66.1 at spec 97% (L19) | SUPPORTED | MODERATE | Exact. "Already referred for monitoring" not in abstract (Unv.). |
| 29 | Smartwatch ECG+AI "diagnose" ACS AUROC 0.987, N=71 (L20) | OVERSTATED | WEAK | 56 ACS vs 15 healthy controls; spectrum-biased. Abstract says "aiding". ACS-O(+) vs others only 0.88. |
| 30 | Graphene tattoo 0.2 +/- 5.8 mmHg >300 min, lab (L28, 154) | SUPPORTED | WEAK | N not stated; correctly called lab-only. |
| 31 | Radar PTT r 0.75-0.86, N=25 seated, per-subject calibration (L29, 154) | SUPPORTED | WEAK | Limits honestly stated. |

**Labels.** No PREPRINT items. Refs 18/19 should carry INDUSTRY-CLAIM. STRONG tags: PHY-1 fine. PHY-5 (STRONG) unjustified: refs 6 and 7 are ~6-7k-person self-selected EHR-linked cohorts, so MODERATE. PHY-10 (STRONG) unjustified: retrospective development, C 0.70, so MODERATE. PHY-15 fine.

**Strike list:** none (all refs exist and are on topic). Fix ref 19 entry text; remove or use ref 12.

**Downgrade list:** PHY-5 STRONG->MODERATE; PHY-10 STRONG->MODERATE; ref 29 wording "diagnose" -> "separated ACS from healthy controls (N=71)"; ref 22 delete "temperature"; ref 25 name Oura specifically; ref 18 add INDUSTRY-CLAIM and "1,863 analysed"; ref 15 note 65 events and CVD outcome.

**Top 5 most reliable:** 8 (exact meta-analysis), 9 (AHA statement), 17 (ESH statement), 1 (very large cohort, exact), 3 (meta-analysis, heterogeneity disclosed).

**Integrity score: 8/10.** Numerics are exact almost everywhere, and the paper labels its own derivation (PPV) and limits (radar N=25, PRV not generalisable) honestly. Deductions: a corrupted reference entry (19), two inflated STRONG tags, a diagnostic claim (29) that overstates a 71-person spectrum-biased study, an unsupported "temperature" element attributed to ref 22, and a best-device generalisation from N=13. Confounding is mostly acknowledged (L157 is the paper's own main caveat), but reverse causation for steps and sleep is not spelled out.

**Arithmetic check (PPV).** Prevalence p=0.005, operating point specificity 97.0% (AUROC alone cannot give PPV; the point is a fixed threshold at 97% spec):
- Internal, sens 0.706: TP=0.00353; FP=0.995x0.03=0.02985; PPV=0.00353/0.03338 = **10.6%** (~8.5 false per true).
- External, sens 0.661: TP=0.003305; PPV=0.003305/0.033155 = **10.0%** (~9 false per true).
- Paper's "about 9-10%" and "roughly nine false alarms per true one" are right to within rounding (internal is slightly above the range). Caveats: 0.5% is prevalence over all 247,254 recordings, validation sets may differ; the unit is a 14-day recording (13-day horizon), not an alert-day; threshold fixed on validation data.

# PART 2. DEVICE ENGINEER (32 refs)

| Ref | Cited for (line) | Verdict | Evidence level | Note |
|---|---|---|---|---|
| 1 | Apple HTNF K250507: Class II, 41.2/92.3, PCCP, spec 86.4% N=187 (L11, 32, 44, 61, 126, 153, 161) | SUPPORTED (L153 OVERSTATED) | REG | L153 "the one precedent... locked models" generalises one PCCP. L161 "fell" compares different populations. Upstream PDF read; not refetched. |
| 2 | Fitbit LoP K242967: sens 69.3% (135 users), day spec 99.965% (L21) | SUPPORTED | REG (simulated pulselessness) | Matches ref 3's 67.23%. "The only cleared consumer SCA detector" is a universal claim I cannot verify. |
| 3 | 1 call/21.67 user-years; 67.23% sens (L21) | SUPPORTED | MODERATE | Sensitivity in arterial-occlusion model, as the text says. |
| 4 | XK300 radar HR/RR, hospital, no alarms (L23) | SUPPORTED (limits Unv.) | REG | Upstream PDF read; not refetched (budget). |
| 5 | C200 UWB limits (L23) | SUPPORTED (existence) | REG | My fetch confirmed K234003, decided 30 May 2024. Page showed no indication limits; product code "cardiac monitor incl. rate alarm". |
| 6 | C300 60 GHz, cleared 2026 (L23, 33, 39, 150) | SUPPORTED (existence) | REG | My fetch confirmed K252676, decided 3 Feb 2026. Limits Unv. from the database page. |
| 7 | Aktiia K250415 | UNCITED | REG | My fetch confirmed G0, Aktiia SA, 2 Jul 2025, DXN. Listed only. |
| 8 | WCD is Class III PMA (L20) | SUPPORTED | REG | openFDA. |
| 9 | ESH six tests (L45) | SUPPORTED | STRONG (consensus) | Exact. |
| 10 | Cuffless accuracy review | UNCITED | n/a | Listed only. |
| 11 | ISO 81060-3:2022 for continuous devices (L45, 154) | SUPPORTED | REG (scope page) | Catalogue page only; says nothing on "burden". |
| 12 | ISO study, invasive reference, >=50 change points (L45, 154) | PARTIAL | WEAK | Abstract garbled: "at most 22 subjects" met the 50-point minimum; study incomplete. Secondary source for the standard. |
| 13 | Route warnings to upper-arm cuff (L48) | SUPPORTED | MODERATE (narrative review) | Fine. |
| 14 | Calibration anchoring 7.4 (13.2) vs 1.8 (8.3) mmHg, N=166 (L46, 154) | PARTIAL | MODERATE | Numbers exact. "Would hide exactly the drift" extrapolates from a 24-h surrogate to weeks-months. One device. |
| 15 | Radar BP: feasibility only (L35) | SUPPORTED | MODERATE (systematic review) | Fair; an author is a radar-company CEO. |
| 16 | MDR Rule 11 classes (L20) | UNV. | REG | No abstract; consistent with known Rule 11 text. |
| 17 | IWRL6432 690-1290 mW; 1.2 mW presence (L34, 67, 150) | SUPPORTED | SPEC | Labelled INDUSTRY-CLAIM, correct. |
| 18 | MAX86176 <11 uA, synchronised PPG/ECG, IEC 60601-2-47 (L32, 73) | SUPPORTED | SPEC | "Designed to meet" is not certified. |
| 19 | nRF52840 6.40 mA TX at 0 dBm (L76) | SUPPORTED | SPEC | Fine. |
| 20 | Q-PPG 4.41 BPM MAE, 47.65 mJ; 1.9 kB/1.79 mJ (L56) | SUPPORTED | MODERATE (bench) | Exact. Smallest model MAE ~8 BPM omitted. Energy conflicts with power budget (below). |
| 21 | INT8 PPG->BP on STM32N6 (L57) | SUPPORTED | WEAK | Bench, no clinical validation. |
| 22 | PPG SQI 95.6%; 10,107/35,712 poor (L58, 163) | PARTIAL | WEAK | Numbers exact (28.3%). Headband PPG, 54 people; 80/20 epoch split, no subject-wise split stated: likely leakage inflates 95.6%. |
| 23 | FL reviews mostly retrospective/simulated (L62, 153) | SUPPORTED | MODERATE-STRONG | Exact. |
| 24 | Naive FL -13.87 points, ~70x longer (L63) | PARTIAL | WEAK | Numbers exact. Same abstract proposes H-FedSL restoring 98.81%; simulation. |
| 25 | Wear-time 77.4%, 273/298 (L162) | SUPPORTED | MODERATE | 273/298 = 91.6%. SD 32.6 shows huge spread. |
| 26 | False AF alerts: dose-dependent decline (L164) | SUPPORTED | MODERATE-WEAK | Secondary RCT analysis, stroke/TIA >=50 y; association. |
| 27 | WCD wear ~21 h/day (L26) | SUPPORTED | MODERATE | Exact (21.1/21.5 h). |
| 28 | Radar arrhythmia 75%, 15 subjects (L24) | SUPPORTED | WEAK | Correct; training 93.9% omitted. |
| 29 | Radar OSA screening (L33) | SUPPORTED | MODERATE | N=141, r 0.87-0.94; pointer only. |
| 30 | Unshielded MCG research demo (L25) | SUPPORTED | WEAK | Fine. |
| 31 | African regulators rely on international certification (L169) | SUPPORTED | MODERATE | Scoping review; Tunisia-specific claim rightly not relied on. |
| 32 | none | UNCITED | n/a | Listed only. |

**FDA checks (3 fetches: K252676, K234003, K250415).** IDs, titles, applicants, dates and SESE decisions all confirmed. The database pages do not show indication limits (clinical setting, no alarms, no arrhythmia); those rest on the engineer's PDF read and were not re-verified. C300's product code reads "cardiac monitor incl. cardiotachometer & rate alarm" while the paper says "no alarms": consistent only if the indication excludes alarming (unconfirmed). L23 "Every cleared radar monitor" is a universal claim; restrict to the three named.

**Labels.** Vendor specs (17-19) correctly INDUSTRY-CLAIM; no PREPRINT items. DE-C1 fine. DE-C2 (STRONG) should be MODERATE: sensitivity is on simulated pulselessness. DE-C8 (STRONG) should be MODERATE: refs 10 uncited, 12 WEAK. DE-C11 (STRONG) should be MODERATE: one PCCP does not show "regulators accepted locked models".

**Strike list:** none. Cleanup: uncited refs 7, 10, 32.

**Downgrade list:** DE-C2, DE-C8, DE-C11 STRONG->MODERATE; L153 rephrase to "the one PCCP reviewed excluded continuous learning"; L23 restrict "every"; ref 14 lines soften to "over 24 h"; ref 22 note leakage risk; ref 24 add "same paper proposes a fix".

**Top 5 most reliable:** 9 (ESH validation tests), 1 (K250507 record), 8 (openFDA class 3), 3 (Nature LoP, exact), 23 (systematic review, exact).

**Integrity score: 7.5/10.** Citations match the abstracts, and the regulatory records I re-fetched exist and match on IDs and dates. The paper openly says power and BOM figures are its own estimates. Weaknesses: three STRONG tags overreach, the ISO argument leans on an uncited or weak pair of refs, a PPG-quality accuracy likely inflated by leakage, and a power table that omits neural-network inference despite citing a 47.65 mJ/inference model.

**Arithmetic checks (power, battery, BOM).**
- Power sum: low 11+30+0+10+50+50 = 151 uA; high 11+60+0+30+100+100 = 301 uA. Stated "0.15-0.3 mA" is correct (PAT bursts as 0).
- Battery, 150 mAh: 150/0.15 = 1,000 h = 41.7 d (~6 wk); 150/0.30 = 500 h = 20.8 d (~3 wk). "~3 weeks nominal" is the pessimistic end (conservative). With 50% derating: 10.4-20.8 d, so ">=1 week" holds. Self-discharge and ECG AFE shutdown (0.5 uA) excluded; immaterial.
- Radar: 690-1290 mW at 3.7 V = 186-349 mA, so 150 mAh lasts 0.43-0.81 h (26-49 min), about 600-2,300x the wrist budget. "Fails for any wearable radar" holds. The 1.2 mW presence mode (~1 mW) gives no vitals; correctly caveated.
- **Inconsistency:** ref 20's 47.65 mJ/inference at one per minute = 0.79 mW = ~215 uA at 3.7 V, which alone exceeds the 50-100 uA MCU line and roughly doubles the total. At one per 15 min it is ~14 uA (fine). The paper must state the inference rate or use the 1.79 mJ model.
- BOM: only the AFE is sourced ($14.36 x1, $9.87 at 2,500). Whole-wrist "$35-60 at 1k" is an unsourced estimate; the AFE would be 16-28% of it at the reel price ($9.87/60 to $9.87/35), and the 1k price is not the 2,500 price. No line items sum to $35-60 in the paper.

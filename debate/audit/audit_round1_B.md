# Audit round 1 - Auditor B

Scope: whether each source supports what it is cited for. FDA K250507 was read directly from the FDA PDF (web fetch 1 of 3; text extracted locally).

## PAPER 1: clinician (round1/clinician.md)

Verdicts: S=SUPPORTED, P=PARTIAL, O=OVERSTATED, N=NOT-SUPPORTED, U=UNVERIFIABLE-FROM-ABSTRACT. Line numbers refer to round1/clinician.md. c-N = [clinician-N].

| Ref | Cited for (line) | Verdict | Evidence level | Note |
|---|---|---|---|---|
| c-1 ESC 2024 | Thresholds (L13) | S | Guideline, STRONG ok | Table 5 values match. |
| c-1 | "Every guideline body says cuffless must not be used" (L36) | P | Guideline | ESC only asks for validation standards; blanket "every body" is generalised. |
| c-2 ESC pharmacotherapy | 3-month lifestyle window (L40, L112) | S | Review by guideline authors | Class I, 3 months matches. Extension to "lead time" is inference. |
| c-3 AHA/ACC 2025 | >=130/80, HBPM+ABPM (L14) | U | Guideline | Abstract has no thresholds; support only via c-4/c-5. |
| c-4 Brown 2026 | HBPM+ABPM; cuffless not recommended; ABPM access (L14, L36, L119) | S | Review, guideline-chair co-author | Quotes per full text; abstract silent. |
| c-5 Sayed 2026 | 3-6 mo lifestyle, stage 1 (L40) | S | NHANES modelling | Cited as guideline source; is a secondary retrospective analysis. |
| c-6 Vemu 2024 | ESH >=140/90, high-normal, against cuffless (L15, L36) | S | Review | Abstract empty; full text checked by parent. |
| c-8 AHA cuffless 2026 | "not adequately vetted" (L36) | S | Scientific statement | Quote verbatim. |
| c-8 | "Protocols test accuracy after calibration, not stability" (L36) | P | Statement | True of ISO 81060-3; ESH 2023 (c-10) has a recalibration-stability test. |
| c-9 ESH 2022 | ESH does not recommend cuffless (L36) | S | Society statement | Matches abstract. |
| c-10 ESH 2023 | Listed only, never cited in text | S | Society protocol | Orphan; contradicts the L36 stability claim. |
| c-11 Mukkamala 2025 | "no compelling evidence" (L36) | S | Review | Quote matches. |
| c-12 Aurora review | 1,125-participant study negative (L36) | S | Review of one study | Secondary source; fine. |
| c-13 Tan 2023 | +15.5 night SBP, dip 14.2, drug -1.0 vs -19.7 n=3 (L36) | S | Validation n=41; drug arm n=3 | Numbers exact. |
| c-13 | Trend tracking "exactly where weakest"; drift vs disease (L36, L111) | O | One device (Aktiia) | n=3 drug arm; drift claim is inference, not tested. |
| c-15 Apple 510(k) | 41.2/92.3, PPV 70.9@31.4%, N 2,229/1,863, 86.4% N=187 (L28, L42) | S | Regulatory, sponsor data | All match K250507 exactly. |
| c-15 | "reached PPV 70.9%" as support for "Emerging hypertension is base-rate-friendly" (L28) | O | Regulatory | PPV computed at stated prevalence; device detects existing undiagnosed hypertension, not incident. |
| c-15 | Target "<=~14% of non-hypertensives alerted over 2 years" (L77) | O | Regulatory | 86.4% is mean per-window specificity (6 windows, N=187, adjusted), not cumulative. |
| c-15 | Subgroup gaps in cleared devices (L78) | S | Regulatory | Sensitivity RR 0.69 for age <60. |
| c-16 Cohen JAMA | PPV 69.1% NHANES (L28); 59% unalerted (L42) | S | Modelling of c-15 sens/spec | Abstract empty; verified from full text by parent. Tagged STRONG; is a model. |
| c-17 Cohen 2026 | 59% not alerted (L42) | S | Commentary | 1-0.412=58.8%. Commentary, not evidence. |
| c-18 Staplin | HR 1.41 vs 1.18, 591%, masked 1.37 (L17) | S | Registry cohort n=59,124 | All exact. |
| c-18 | "HBPM/ABPM outcome-validated reference" (L111) | P | Cohort | Study is ABPM vs clinic; HBPM not tested. |
| c-19 Zhu | Masked HTN 18%, RR 1.64 (L19) | S | Meta-analysis | Exact. |
| c-20 Show | 45%, non-dipping 39%, I2 97% (L19, L38, L117) | S | Meta-analysis | Exact; limited-treatment-benefit caveat correctly quoted. |
| c-20/21 | "daytime HBPM can miss it" (L38) | U | - | Not in either abstract. |
| c-21 Fujiwara | HR 1.72 (L19) | P | Prospective cohort, 152 events | Number exact; CI 1.01-2.92 borderline; high-risk Japanese; tagged STRONG (L93). |
| c-22 NCD-RisC | 626M/652M; 59%/49% (L19) | S | Pooled analysis | Exact. |
| c-23 Xia | Trajectory HR 3.91 (L19) | S | Cohort n=6,579 | Exact; clinic BP, not wearable. |
| c-24 Hoshi | "Low HRV predicted 4-yr hypertension" (L19) | P | Cohort | Association (RR), no discrimination metric; "predicted" strong. |
| c-25 ESC ACS 2023 | 12-lead ECG + hs-troponin (L25) | S | Guideline | No abstract; consistent with entry. |
| c-26 Lindow | 52/99/PPV 51, 24,511, 1.9% (L26) | S | Retrospective | Exact; consistent with prevalence. |
| c-26 | "Strongest AI-ECG result for acute MI" (L26) | O | Retrospective | Superlative unsupported; OMI, single country. |
| c-27 Holmstrom | AUROC 0.889/0.820 case-control (L26, L108) | S | Case-control | Exact; "no lead time" not in abstract. |
| c-29 Reinier | ~50% symptom; OR 2.2-2.9 (L26) | S | Case-control | ORs exact; 50% from full text per parent. |
| c-30 Shah | 1 call/21.67 user-yr, 67.23% (L27, L109) | S | Prospective, industry authors | Exact; sensitivity is in occlusion simulation (stated). No INDUSTRY label. |
| c-30 | "large engineering program"; "already on the market" (L27, L109) | U | - | Rhetoric/external fact, not in abstract. |
| c-31 Empana | SCD 36.8-39.7/100k/yr (L27) | S | 4 registries | Exact; EMS-attended only (undercount). |
| c-32 Varma | "clinically nonactionable data" (L42) | S | Scientific statement | Verbatim. |
| c-33 Rosman | Preoccupation, more AF care (L42) | P | Retrospective n=172 | Correct but AF patients, association only; stretched to hypertension alarms. |
| c-34 Fitbit | PPV 98.2%, 32.2% (L32) | P | Prospective, industry-funded | Numbers exact. PPV is among 225 with repeat IHRD; "only 32.2%" ignores 1-week patch missing paroxysmal AF; "only ... real evidence" unsupported. |

Labels: the only PREPRINT/INDUSTRY mention in the file is in a reference-list line; c-15 (sponsor data), c-30 and c-34 (industry authors) carry no INDUSTRY-CLAIM label in-text.

**Strike list (NOT-SUPPORTED):** none outright.

**Downgrade list**
1. L77 "<=~14% of non-hypertensives alerted over 2 years": per-window specificity misread as cumulative. Restate as per-window false-positive rate, or drop.
2. L28 "Emerging hypertension is base-rate-friendly": c-15/c-16 describe prevalent undiagnosed hypertension vs a 30-day HBPM label; PPV 70.9% is at assumed 31.4%. Not incident; reword, drop "reached".
3. C6 (c-15, c-16) STRONG to MODERATE, add INDUSTRY-CLAIM (sponsor 510(k) data plus a modelling study).
4. C2 STRONG: c-21 is MODERATE (152 events, CI floor 1.01); c-18/c-19 stay STRONG.
5. C4 STRONG: ESC has no explicit "do not use" statement; "protocols do not test stability" is contradicted by c-10 (ESH 2023).
6. c-13 within-person claims (L36, L111): one device, n=3; WEAK-MODERATE.
7. c-26 "strongest" and c-34 "only ... real evidence": delete superlatives.
8. c-30, c-34: add INDUSTRY-CLAIM.
9. C1 STRONG: c-3 abstract gives nothing; STRONG survives only via c-4/c-5.

**Top 5 most reliable refs:** c-18 (Staplin), c-19 (Zhu meta-analysis), c-22 (NCD-RisC), c-31 (Empana), c-1/c-6 guideline thresholds. Runner-up c-15 for the numbers themselves (verified exact against FDA).

**FDA K250507 check:** the SE letter is dated Sept 11, 2025 (clearance date); a Sept 12, 2025 letter is an administrative correction (correct 510(k) Summary, new product code SFR). "Cleared Sep 11" is correct. Sens 41.2 (37.2-45.3), spec 92.3 (90.6-93.7), PPV 70.9 (65.7-75.7) at prevalence 31.4%, N 2,229 enrolled / 1,863 analysed, stage-2 sens 53.7 (47.7-59.7), long-term spec 86.4 (80.2-92.5) N=187: all match. The 68.4%/99.1%/PPV 13.7% at prevalence 0.002 in the same table belongs to the predicate (HCM ECG feature), not HTNF.

**Integrity score: 7.5/10.** Almost every number matches its source exactly, including the FDA figures, and the paper labels its own arithmetic as its own. Deductions are for interpretive overreach: prevalent-detection performance is used to support "emerging" hypertension, per-window specificity becomes a cumulative 2-year alert rate, and two superlatives ("strongest", "only ... real evidence") are unsupported. STRONG tags are generous for modelling and sponsor data, industry labelling is absent, and the "every guideline body" and "protocols do not test stability" generalisations are contradicted by the paper's own reference c-10.

**Arithmetic check (L27).** Inputs: 36.8-39.7 SCD/100k/yr (c-31). Implicit assumptions: sensitivity 90%, specificity 99.9%, predictor applied per person-day, one positive day per event, independent days.
- Events: 100,000 x ~40/100,000 = 40; x0.9 = 36 (34-36 across the range). OK "~36".
- Person-days 36.5M x 0.1% FP = 36,500 false alarms. OK.
- PPV = 36/(36+36,500) = 0.099%. OK "~0.1%".
- Specificity 99.999%: FP = 365, PPV = 36/401 = 9.0%. OK "~9%".
- Daily event rate 40e-5/365 = 1.1e-6 per person-day; "1 per million per day" (L108) OK.
Caveats: EMS-attended SCD undercounts; high-risk subgroups have 10-100x higher base rate, so PPV is population-specific; an alert window longer than one day changes both terms.

---

## PAPER 2: ppg_scientist (round1/ppg_scientist.md; short form [PS-n])

Web budget used (3 of 3): K250507, K242967 (Fitbit loss-of-pulse) and K250415 (Aktiia G0), each read from the FDA PDF. Line numbers refer to round1/ppg_scientist.md.

| Ref | Cited for (line) | Verdict | Evidence level | Note |
|---|---|---|---|---|
| PS-1 Apple 510(k) | Sens 41.2, spec 92.3, 53.7% stage 2, N 2,229, 86.4% N=187, >86,000-participant SSL encoder (L45) | S | Regulatory, sponsor data | All verified in FDA text. Cleared 11 Sep 2025 correct. |
| PS-1 | Definition 30-day mean home BP >=130/80; 15-day usable gate (L15, L68, L89) | S | Regulatory | Matches summary. |
| PS-1 | "That is M6 validated at regulatory level" (L45) | O | Regulatory | Cleared as notification for prevalent HTN, sens 41%; nothing on lead time or trajectory. PS concedes this at L137. |
| PS-1 | Fitzpatrick RR 1.11 [0.84,1.47] rebuts skin-tone bias (L138) | P | Regulatory | Number exact, but wide CI (down to 0.84): underpowered, not evidence of no bias. |
| PS-1 | "same split as [PS-1]" (L96); PCCP excludes learning (L105, L147) | U | - | Split not verified; PCCP claim rests on parent extraction. |
| PS-2 Cohen JAMA | LR- 0.64 (L63, L136) | S | Modelling of PS-1 sens/spec | 0.588/0.923 = 0.637. Abstract empty; verified by parent from full text. |
| PS-3 Abbaspourazad | PPG 0.819 vs ECG 0.769 vs demographics 0.770 (L40, L55) | P | Conference paper, Apple authors | Numbers from Table 9 per parent. Self-reported label; gain over demographics only 0.05; cross-sectional. No INDUSTRY label. |
| PS-4 PaPaGei | >57,000 h, open weights, skin-tone analysis (L55) | S | Conference paper/preprint | Matches abstract; no hypertension validation claimed. |
| PS-5 PulseDB | Poor generalisation to unseen subjects (L43); licences (L79) | P | Dataset paper | Abstract shows only the calibration-based vs calibration-free gap; r 0.97 vs 0.22 is a summarised prior study. ICU/surgical sources. |
| PS-6 Moulaeifard | MAE 13.9/8.5 "in an external benchmark" (L43) | P | Benchmark | 13.9/8.5 is in-distribution, no calibration; external is 10.0-18.6 SBP. Table (L121) labels correctly; prose does not. |
| PS-7 Mehta | MI 9.8% vs 87.7% (L43, L145) | S | Bench analysis | Exact. Single paper using its own metric. |
| PS-8 Aurora review | 1,125 participants, no better than calibration baseline (L39, L43) | S | Review of one study | Consistent with "clear-cut negative"; detail from parent full-text read. |
| PS-9 Mieloszyk | Waveform models with/without PAT no better than baseline (L43, L78) | P | Dataset/validation paper | Abstract says tonometry features beat baselines; PPG/PAT vs baseline not stated. Partly contradicts the claim. |
| PS-10 Tan | -1.0/-0.8 vs -19.7/-11.5 (L43) | S | Validation n=41; drug arm n=3 | Exact; n=3 omitted in PS text. "Regulator-grade" = CE at the time. |
| PS-11 Derendinger | 7.4 vs 1.8 mmHg (L39) | S | Prospective n=166 | Exact; PTT device, not PPG. |
| PS-12 Finnegan | PAT-SBP slope -2946 to -470 (L39) | S | Lab n=30, phenylephrine | Exact; healthy volunteers. |
| PS-13 ESH 2023 | Six tests (L43, L106) | S | Society protocol | Matches. |
| PS-14 Stergiou 2025 | No convincing evidence; societies do not recommend (L43) | S | Review | Matches abstract. |
| PS-15 Aktiia K250415 | Cleared; 24-h cuff calibration; ages 22-59; ISO 81060-2 (L43) | U | Regulatory | Clearance 2 Jul 2025, DXN, 21 CFR 870.1130 confirmed. Indications are image pages; calibration/age not verifiable by me. Clinician-11 says Aktiia calibrates monthly: sources conflict. |
| PS-16 Fitbit K242967 | Sens 69.3 (64.3-74.1), n=135, 99.965% (131), exclusions, cleared 25 Feb 2025 (L26) | S | Regulatory, industry | All match FDA. Omits that sensitivity comes from induced/simulated pulselessness; FDA also gives 1 call per 75 person-years vs Nature 1 per 21.67. |
| PS-17 Shah | 21.67 user-years, 67.23% (L26) | S | Prospective, industry authors | Exact; occlusion model stated. |
| PS-18 Samsung K240909 | On-demand ECG; AF sens 96.0/spec 98.7 (L29, L37, L51) | U | Regulatory | Not fetched by me; plausible; verified by parent from PDF text. |
| PS-19 Kolk | 277 pts, 56 VA, AUROC 0.74 +/- 0.05 (L27) | S | Prospective cohort, ICD patients | Exact. Comparison vs 0.67 has P=0.05; PS calls it thin. |
| PS-20 Matteucci | "EM is proven for arrhythmic SCD therapy" (L28) | O | Meta-analysis of single-arm rates | 3% (2-3), I2 88.9%: pooled appropriate-intervention incidence, no comparator; shows shocks delivered, not proven benefit. |
| PS-21 Singh | LoA -33.69/32.54 dark vs -16.02/13.54 light; no significant bias (L38, L138) | P | Meta-analysis, 4 studies n=176 | Exact. Bias CI -9.4 to 8.3 is wide; authors say PR breaches thresholds in all groups. |
| PS-22 Mulholland | 36% of sample, 50% Apple, 85% SlateSafety missing (L38) | S | Lab study N=28 | Exact; small, exercise setting. |
| PS-23 Sel | Bioimpedance skin-tone n=3, WEAK (L38, L139) | S | Bench N=10 | PS more cautious than the abstract; correct. |
| PS-24 Moscato | Accuracy 0.96/0.97, 31 participants (L51) | S | Validation | Exact; pulses sampled equally per activity range. |
| PS-25 Alavi | 80% (67/84), 3 days, 1.15 alert-days (L58) | P | Prospective cohort | Numbers exact. 1.15 is alert-days per person for non-COVID events (vs 3.42 COVID), not an overall false-alert rate. Infection, not HTN. |
| PS-26 Master | 6,042, 4.0 y, 482 HTN, 84% white, 73% female (L75, L148) | S | Retrospective cohort | Exact. |
| PS-27 Nie | Age gap >9 y, HR 2.88 hypertension, N=212,231 (L60) | P | Retrospective cohort | N exact; 2.88 not in abstract (parent read full text; abstract gives 2.37 for MACCE). Single finger PPG, not wrist wearable; personal-baseline inference is a stretch. |
| PS-28 Bouwmeester | HRV limits (L140, L145) | S | Prospective cohort | SDNN/RMSSD not associated with new-onset HTN; xBRS OR 1.31. Fair. |
| PS-29 LifeSnaps | Dataset for missingness (L77) | U | Dataset | Dataset facts match; "missingness" use not in abstract. |

Labels: STRONG used for PS-1 (regulatory), PS-8/9, PS-16/17. PREPRINT appears only in reference-list types (PS-3, PS-4); no in-text INDUSTRY-CLAIM for PS-1, PS-3, PS-16, PS-17.

**Strike list (NOT-SUPPORTED):** none.

**Downgrade list**
1. PS-20 / L28: "proven" to "reported"; single-arm pooled intervention rate, no control.
2. PS-1 / L45: drop "M6 validated at regulatory level"; regulatory evidence covers prevalent-HTN notification only.
3. PS-9 / L43: remove as support for "no better than baseline" (tonometry beat baselines). Keep PS-8 only.
4. STRONG for PS-16/17: sensitivity is in induced pulselessness, no real arrests; MODERATE plus INDUSTRY-CLAIM. PS-1 (sponsor 510(k)): STRONG fair for "cleared", not for effectiveness.
5. PS-6 prose (L43): relabel 13.9/8.5 as in-distribution.
6. PS-1 skin tone (L138): report the CI as "cannot exclude ~16% lower sensitivity", not as reassurance.
7. PS-25 (L58): 1.15 alert-days is not an overall false-alert rate; add the 3.42 comparator.
8. PS-21 (L138): "not significant" is underpowered (4 studies).
9. PS-3: add INDUSTRY-CLAIM; note self-reported label.

**Top 5 most reliable refs:** PS-1 (numbers exact against FDA), PS-16 (exact against FDA), PS-8 (large negative study, faithfully summarised), PS-7, PS-10/PS-11 (exact, correctly scoped).

**Integrity score: 8/10.** The numbers are the strongest feature: every checked FDA and abstract figure is exact, and the paper hedges repeatedly (n=3, WEAK, "conceded", MNAR). Faults: two overstatements (WCD "proven", HTNF "validated at regulatory level"), one citation that partly contradicts its claim (PS-9), and a setting slip (in-distribution MAE called external). STRONG tags on sponsor/regulatory and simulation-based results should be MODERATE with an INDUSTRY-CLAIM label. Unverified regulatory details (Aktiia calibration interval, Samsung figures) rest on the parent's extraction.

**Arithmetic check.**
- LR+ = 0.412/0.077 = 5.35; LR- = 0.588/0.923 = 0.637 (L63 "0.64"). OK.
- PPV at 31.4%: 0.1294/(0.1294+0.0528) = 71.0%; FDA 70.9%. OK.
- 86.4% specificity means 13.6% false-positive per window, not a cumulative 2-year rate.
- Loss-of-pulse: 99.965% day-level specificity implies 365 x 0.00035 = 0.128 false calls per person-year (1 per ~7.8 y); FDA real-world 1 per 75 py and Nature 1 per 21.67 py are lower because of extra gates. Consistent, but not interchangeable.

---

## ROUND-2 NEW REFERENCES (abstracts fetched from PubMed; not counted against the web budget)

Line numbers refer to round2/clinician.md (c-35..c-39) and round2/ppg_scientist.md (PS-30..PS-33, packet name ppg_scientist-30..33).

| Ref | Cited for (line) | Verdict | Evidence level | Note |
|---|---|---|---|---|
| c-35 Ceyhun 2026 | "New evidence supports him": AUC 0.54 to 0.67, PPG HRV/activity, no ECG (L22, L84) | P | Single-centre cohort, 230, 28 events | Abstract: low HRV, low MVPA, high BMI associated; ML "exploratory". AUC and CI 0.57-0.76 from full text; lower bound near chance, no external validation. "Supports" overstated. |
| c-35 | Outcome definition, office >=140/90 or drug start (L99); HRV positive (L110) | S | Cohort | Matches abstract. HRV direction anomaly correctly avoided. |
| c-36 Liu 2024 | Validation C-index 0.917; 21.8% converted in 6 months (L85, L109) | S | Prospective cohort, 3,180+1,000 | 693/3,180 = 21.8%. Exact. Abstract lists no predictors or outcome definition. |
| c-36 | "Best short-term prediction came from watch-cuff BP" (L95) | P | Cohort | Predictors not in abstract; HR 86.8 and C-index 0.917 hint at circularity (BP predicting BP-defined outcome), same-centre validation. WEAK-MODERATE. |
| c-37 Hove 2026 | N=50, r 0.74-0.75, LoA ~ +/-10 (L40) | S | Validation, N=50 | LoA -8.0/11.2 exact. "Calibrated" not in abstract (U). Aidee Health (manufacturer) authors: add INDUSTRY. |
| c-38 Lee 2026 | Ring N=35, LoA -14.4/10.9, kappa 0.58 (L40) | S | Validation, ESH awake/asleep test only | All exact. Author fees from Sky Labs. |
| c-39 Parati 2025 | ABPM reference; wearables "require further validation"; OSA clustering (L41, L96) | S | Society position paper | Quote and content match abstract. Some authors have device-maker fees. |
| PS-30 van der Velden | Median adherence 83.3%; full days 16/27 (L97, L154) | S | RCT sub-analysis, 335 AF patients | Matches entry; motivated post-ED AF patients, 4 weeks. PS hedges "motivated". Generalising to healthy monitored people is the limit. |
| PS-31 Andersen | 75.0% missed no day (L98, L154) | S | Single-centre cohort | 123/164 = 75.0%. Post-cardioversion patients. |
| PS-32 Apple SANF K240929 | Sens 66.3, spec 98.5, n=1,499 (L93) | U | Regulatory, sponsor data | Not fetched by me; consistent with entry; sens is for AHI >=15, spec for AHI <15 (different denominators). Says nothing on radar. |
| PS-33 Samsung DEN230041 | 82.7% / 87.7% under "FDA authorisation" (L94) | P | Regulatory | Entry says specificity missed its pre-set acceptance criterion; text omits it. Granted De Novo anyway. |

**Strike list:** none.

**Downgrade list**
1. c-35 "supports him" (L22): WEAK; 28 events, CI floor 0.57. Reword as hypothesis-generating.
2. c-36 (L95, L109, R2-C1): outcome-circularity risk and unknown predictors; do not rest design decision D1 or the "64%" PPV on it. WEAK-MODERATE.
3. c-37, c-38: small single-test validations with manufacturer links; label INDUSTRY-CLAIM.
4. PS-33 (L94): add that specificity 87.7% failed its own acceptance criterion.
5. PS-32/33: they show a wrist OSA feature exists, not that radar adds nothing; do not tag STRONG for the radar argument.

**Arithmetic check (clinician round 2, L109).** Assumes sensitivity 50%, specificity 92.3% (device: 41.2% overall, 53.7% stage 2).
- Incidence 1%: TP 0.005; FP 0.99 x 0.077 = 0.0762; PPV 6.2%. OK "~6".
- Incidence 2.5%: TP 0.0125; FP 0.975 x 0.077 = 0.0751; PPV 14.3%. OK "~14".
- Incidence 21.8%: TP 0.109; FP 0.782 x 0.077 = 0.0602; PPV 64.4%. OK "~64".
- With sensitivity 41.2%: 5.1% / 12.1% / 59.9%. Conclusion unchanged, but "50%" is an assumption, and HTNF specificity is for detecting present hypertension, not predicting 6-month conversion.
- PPG round 2: 0.923^6 = 0.618 (61.8%, ppg L120). OK, correctly flagged as conditional.

**Integrity score, round-2 new refs: 7.5/10 (clinician), 8/10 (ppg_scientist).** New sources exist and their numbers are exact against abstracts. The clinician's round 2 leans on two small or circular-looking studies (c-35, c-36) to "support" a positive-signal claim beyond what they show, though the claims table hedges (WEAK-MODERATE). The ppg_scientist's additions are honestly hedged (adherence "motivated", conditional 61.8%), with one omitted caveat on Samsung's specificity criterion.


# Audit round 1 - Auditor A (support-of-claim only; existence/recency pre-settled)

Verdict key: S = SUPPORTED, P = PARTIAL, O = OVERSTATED, N = NOT-SUPPORTED, U = UNVERIFIABLE-FROM-ABSTRACT.
Evidence level = strength the source can bear (STRONG / MODERATE / WEAK / PREPRINT / INDUSTRY-CLAIM / GUIDELINE).
FDA K250507 decision date confirmed on the FDA record: 09/11/2025 = 11 Sep 2025 (round-1 "cleared 2025-09-11" is correct).
Note: bayesian_ml uses no STRONG tags; only one WEAK and two PREPRINT tags appear in the text.

# 1. bayesian_ml

| Ref | Cited for (line) | Verdict | Evidence level | Note |
|---|---|---|---|---|
| 1 Alavi | L38 baseline stable in 7 nights, >80% | S (full text) | MODERATE | Not in abstract; matches PMC full text per packet |
| 1 | L45 "persistence gating matters empirically"; 80% vs 72%/69% | O | MODERATE | Study compares algorithms, never ablates 2-night gating; 72/69% is a Fitbit-subset comparison; specificity 87.7% omitted |
| 1 | L99 false-alarm contexts 1.15 vs 3.42 | S | MODERATE | Matches; abstract says heart rate and steps, not RHR alone |
| 2 Mason | L101 accuracy varied by age/sex | S | MODERATE | Oura, 73 training cases; supports only "varied" |
| 3 Mitratza | not cited in text | U (orphan) | STRONG (SR, moderate RoB) | Listed only; cite for the 20-88% range or delete |
| 4 FDA K250507 | L9 sens 41.2/spec 92.3, n=1,863, 30-day windows | S | STRONG (regulatory) | Sponsor-run study; numbers match packet |
| 4 | L61 "Apple requires >=15 usable days" | P | INDUSTRY-CLAIM | 15 days is the analysis-inclusion rule, not shown as a device gate. "Silent if insufficient data" is supported |
| 4 | L65 92.3% vs 86.4% over six windows, N=187 | S | STRONG (regulatory) | Exact match |
| 4 | L101 ratios 0.69, 0.67 | S | STRONG (regulatory) | "covariate-adjusted" not confirmed by packet |
| 4 | L104, L124, L157 encoder, PCCP, subgroup gaps | S | STRONG (regulatory) | Matches |
| 5 Cohen | L9 PPV 69.1, NPV 79.0, 58.8% no alert | P | MODERATE | Modelled on NHANES from manufacturer sens/spec; not observed. Say "modelled" |
| 6 Lautman | L15 4-6 month step change, n=1 | S | WEAK | Honestly tagged WEAK |
| 7 Dunn | L37 wearable RHR more consistent than clinic | S | MODERATE | Matches abstract |
| 8 Gibbs | L59, L148 ACI, long-run coverage | S | PREPRINT (published NeurIPS 2021) | Guarantee assumes feedback each step; "whenever a cuff label arrives" (sparse) weakens it |
| 9 Zaffran | L59, L148 ACI for time series | S | PREPRINT | Fine |
| 10 Shen | L18 daytime SBP MAD 14.32 | S | MODERATE | Exact; retrospective Aurora-BP, not stated in line |
| 11 Kwon | L59 -49.6% / -46.7% at 80% coverage | S | MODERATE | Exact; relative reduction, sepsis setting stated |
| 12 Traub | L91 AUGRC changed rankings on 5/6 | S | PREPRINT | Line lacks PREPRINT tag |
| 13 Kim | L73 PA inflates, random score SOTA | S | MODERATE (AAAI) | Exact |
| 14 Zeng | L108 linear beats Transformers on 9 datasets | S | MODERATE (AAAI) | Forecasting benchmarks, not health; analogical |
| 15 Zhang | L106 up to 11.4 F1 points | S | PREPRINT | Exact; "up to" best case; add tag |
| 16 Shukla | L107 mTAN comparator | S | PREPRINT | Existence cite only |
| 17 Gu | L107 Mamba comparator | S | PREPRINT | No wearable evidence; comparator is a design choice |
| 18 Abbaspourazad | L104 Apple feature "built on" SSL encoder | P | PREPRINT | ~141K-participant model is related; link to cleared feature (>86K) inferred |
| 19 Xu LSM-2 | L94 mean missingness 49% | S (full text) | PREPRINT | Matches full text, not abstract |
| 19 | L105 AUROC 0.754, F1 0.651 vs 0.516, N=1,250 | S | PREPRINT | Tagged; label is self-reported HTN, not incident |
| 20 PaPaGei | L107 open PPG model | S | PREPRINT | Existence cite |
| 21 Wong | L65 alerts 18%, missed 67% | S | MODERATE | Exact; single health system, retrospective |
| 22 TRIPOD+AI | L58, L123 report Brier/ECE/reliability | P | GUIDELINE | Abstract confirms reporting guideline, not the named metrics |
| 23 Mukkamala | L17 four models no better than baseline | S | MODERATE (review) | Secondary source of Mieloszyk 2022; cite primary |
| 23 | L114 Aurora-BP 1,125 with ABPM | P | MODERATE | ABPM only in the 483-person ambulatory arm |
| 23 | L150 Aurora sceptical for absolute BP "not within-person change" | O | MODERATE | Abstract: overall "clear-cut negative"; no carve-out for change tracking |
| 24 ESH | L21 BP proxy "also needs" ESH tests | P | GUIDELINE | ESH: not all tests required; covers cuffless BP devices, not latent-state proxies |
| 25 Walzel | L19 3.4/5.1 mmHg at 10 mmHg from calibration | O | WEAK-MODERATE | Numbers exact, but n=37, one watch; authors conclude acceptable. "Exactly the regime where hypertension emerges" unsupported |
| 25 | L53 PPG proxy variance grows with distance from calibration | O | WEAK-MODERATE | Study reports mean difference (bias) at one threshold, Samsung watch; not variance or PAT |
| 26 Master | L55 steps associated with incident HTN | P | MODERATE | Association only; "predictors" not shown |
| 26 | L114 All of Us Fitbit+EHR | S | MODERATE | "Registered access" not verifiable |
| 27 Zheng | L55 sleep irregularity, incident HTN | P | MODERATE | Association only |
| 27 | L114 All of Us | S | MODERATE | as above |
| 28 Cossu | L36 RMSE 2.84 to 1.21 bpm | P | WEAK | Numbers exact, but ALS/MS patients, Garmin; a Bayesian smoother, not Kalman; reference unclear |
| 29 Finelli | L54 landmark AUC 0.743 to 0.800 | P | MODERATE | Exact, flagged analogical; SEs 0.018 each, no test; single prostate RCT |

**Strike list (only support is NOT-SUPPORTED):** none.

**Downgrade list:**
- L45 "persistence gating matters empirically" (ref 1): study did not test gating; use "consistent with".
- L19 "exactly the regime where hypertension emerges" (ref 25): unsupported inference; n=37; authors concluded acceptable accuracy.
- L53 variance grows with calibration distance (ref 25): tag as design hypothesis; source shows bias only.
- L150 "not for within-person change" (ref 23): remove or mark speculation.
- L104 Apple feature built on ref 18: say "related Apple foundation model".
- L21 ESH "needs" tests (ref 24): "ESH suggests tests as applicable".
- L55 steps/sleep as "predictors" (refs 26, 27): "associated with".
- L9 (ref 5): label PPV/NPV as modelled.
- L61 15-day rule (ref 4): describe as study inclusion.
- Missing PREPRINT tags where refs 12, 15 are cited.

**Top 5 most reliable:** 4 (FDA K250507; exact), 21 (Wong; exact), 1 (Alavi; prospective, mostly exact), 11 (Kwon; exact, setting stated), 13 (Kim; exact, peer-reviewed).

**Integrity score: 8/10.** Every quoted figure matches the abstract or full-text key numbers, and WEAK, PREPRINT and analogical labels are used honestly (n=1 case, sepsis, prostate). Weaknesses are interpretive: the Walzel-based BP-proxy narrative and the Aurora "not for change" carve-out go beyond the sources, "persistence gating matters empirically" is an unsupported causal reading, and association studies are read as predictors. One orphan reference (3) and some missing PREPRINT tags.


# 2. em_engineer

FDA K250507: the FDA database Decision Date is 09/11/2025 (11 Sep). em_engineer-32 says "decision letter dated 12 Sep 2025"; bayesian_ml-4 says 11 Sep. I did not check the letter date itself. Use 11 Sep 2025 (decision date) in both papers, or cite the 12 Sep letter date only if the PDF shows it.

| Ref | Cited for (line) | Verdict | Evidence level | Note |
|---|---|---|---|---|
| 1 Falconer | L24, L61 radar BP feasibility-level | S | MODERATE (SR) | Matches |
| 1 | L131 "small, lab-based, young and healthy" | P | MODERATE | Abstract: small N, narrow BP range; "young and healthy" not stated |
| 2 Liebetruth | L24 radar "HR/RR good" | O | MODERATE (SR) | Only 48% (HR) / 37% (RR) of studies within 5%; comparability "very limited" |
| 3 Vysotskaya | L61 SBP 9.2+-8.3, fails AAMI/BHS, N=55 | S | WEAK (lab) | Exact |
| 4 Shi | not cited in text (claim table C12 uses it) | U | WEAK | Orphan in text |
| 6 Lu | L25 r=0.75, N=6,974, ischaemia qualitative | S | MODERATE | Qualitative point from full text |
| 6 | L89 radar <$30 author-reported | S | INDUSTRY-CLAIM | Correctly labelled author-reported |
| 7 Zhu | L24 feasibility-level | S | WEAK (lab) | N=47 (25 evaluated) |
| 7 | L61, L122 needed calibration, static, cascade board | S (full text) | WEAK (lab) | Abstract silent; matches full-text key numbers |
| 8 Kireev | L23 "tiny, per-subject-calibrated" | U | WEAK | N and calibration not in abstract; abstract claims Grade A |
| 9 Sel | L23, L131 N=10 young | S | WEAK | Exact |
| 10 Thomson | L23 "tiny, per-subject-calibrated" | O | PREPRINT | N=261, not tiny, not a BP-calibration study |
| 10 | L48 IPG amplitude p=0.024 vs PPG | S | PREPRINT | Tagged PREPRINT; single p-value, prototype |
| 11 Schoenmakers | L53 MAE 10.1-12.9, missed stress, N=41 | S | WEAK | Exact |
| 11 | L46, L120 PAT "suited to change detection" | O | WEAK | Reliability high, but construct validity poor; mental-stress changes not detected |
| 11 | L85 PEP-driven stress flagged as context | P | WEAK | Study did not attribute to PEP |
| 12 Mohammed | L26 near-field resonator N=2 | S | WEAK | Abstract says one subject; 2 per full text |
| 13 Mace | L27, L33 sens 66.7, spec 57.1, N=390 | S | MODERATE | Exact |
| 14 Yang | L27, L33 AUC 0.864, N=141 | S | MODERATE | Exact; bootstrap internal validation |
| 15 Xiao | L27 OPM-MCG "hospital, not wearable" | P | WEAK | Paper shows a movable unshielded system; "reject" is judgement |
| 16 Al-Zaiti | L33 12-lead AI-ECG N=7,313 at triage | S | MODERATE | "best" superlative unverified |
| 17 Holmstrom | L34 external AUROC 0.820 | P | MODERATE | Retrospective case-control (SCD vs CAD controls), not stated |
| 18 Oberdier | L34 31% spec at 95% sens | S | MODERATE | Exact; retrospective |
| 19 Shah | L34 sens 67.23%, 1 call/21.67 user-yr | O | MODERATE | Sensitivity is from an arterial-occlusion simulation, not real arrests; line omits it |
| 20 Reinier | L34 dyspnoea 41% vs 22% | S | MODERATE | Exact; controls are EMS patients with similar symptoms |
| 21 Ahn | L22, L39 PVC burden vs Holter, N=134 | S | MODERATE | Exact; one patch product, PVC patients |
| 21 | L39, L121 "AF/PVC ... evidence exists [21]" | O | MODERATE | Ref covers PVC only; AF unsupported by it |
| 22 ESH | L90 ESH validation for displayed BP | S | GUIDELINE | Fine |
| 23 Mukkamala | L52 "no compelling evidence" | S | MODERATE (expert review) | Matches quote |
| 24 Finnegan | L54, L82 slope range, ~6-fold | S | WEAK | N=30, phenylephrine; exact |
| 24 | L63 PEP 5.5 vs -16.8 ms | S | WEAK | Exact; authors say PEP negligible here |
| 24 | L124 rebuts "sympathetic state confounds PAT" | O | WEAK | Phenylephrine infusion only; no sympathetic/stress/exercise test |
| 25 Heimark | L45 r=-0.82+-0.14, N=75; L54 DBP sign flip | S | WEAK | Exact |
| 26 Yang | L51 two PPG features beat PAT, 2.4M cycles | P | MODERATE | Surgical patients (1,376) plus ICU external; setting omitted |
| 27 Saz-Lara | L45 PWV RR 1.09 | S | MODERATE | Exact; heterogeneity noted. PWV is not PAT: "PAT/PTT, a stiffness proxy" is inference |
| 27 | L84 PWV "precedes" incident HTN | P | MODERATE | Association in normotensives; causal order not tested |
| 28 Hoshi | L44 7,665, 4-year; L84 | S | MODERATE | Exact; observational cohort |
| 29 Kantrowitz | L44 SDNN -8.50 ms, N=931 | S | MODERATE | Exact |
| 30 Xu | L44 small errors only at rest | S | MODERATE (MA) | Only 10 studies, healthy people |
| 31 Koerber | L60 4 of 10 vs 4 no effect | S | MODERATE (SR) | Exact; 469 participants |
| 32 FDA K250507 | L47 41.2/92.3, "N=2,229 enrolled" | P | STRONG (regulatory) | Sens/spec computed on 1,863 analysable, not 2,229 enrolled. Date: see note above |
| 33 Cohen | L47 59% not alerted | S | MODERATE (commentary) | 59% is 1 minus sensitivity; no independent evidence |
| 34 FCC 23-35 | L91 57.0-59.4 GHz, 57-64 GHz limits | S | STRONG (regulatory) | Matches key numbers; US only, Tunisia flagged by author |
| 34 | L122 single-chip parts "permitted" | P | STRONG (regulatory) | Depends on each part's actual output and duty cycle |
| 35 Karipidis | L91 no confirmed hazard | S | MODERATE (review) | Review notes many low-quality studies; "no confirmed" is faithful |
| 36 Beutel | L63 error 10.1 to 4.2 mmHg, N=10 | P | WEAK | 4.2 uses carotid ultrasound central PWV, not a wearable; peripheral PWV gave 7.1 |
| 36 | L124 PEP/PTT separation via radar/SCG/ICG [36] | N | WEAK | Study used carotid ultrasound; no radar/SCG/ICG |
| 37 PulseDB | L81, L132 5,245,454 segments, 5,361 subjects | S | MODERATE | Exact; ICU/surgical shift stated |
| 38 Parralejo | L81 110 participants, 60 GHz | S | MODERATE | Exact |
| 39 Sun | L85 radar sleep staging 80.3%, kappa 0.614, N=200 | P | WEAK-MODERATE | Device is radar plus pulse oximetry, 3-class; authors say staging precludes replacing PSG |
| 40 Khalili | L62 capacitive ECG motion artefacts | S | MODERATE (review) | Matches |
| 41-43, 45 TI, Nordic | L80 sensor specs | S (vendor) | INDUSTRY-CLAIM | Accepted as vendor specs; not fetched |
| 44 ADI MAX86176 | L80, L86 sync PPG+ECG, lead-off | S (vendor) | INDUSTRY-CLAIM | Accepted |
| 44 | L22 "standards-grade AFEs exist" | O | INDUSTRY-CLAIM | "Designed to meet" IEC 60601-2-47 is a vendor design claim; L91 labels it, L22 does not |

**Strike list:**
- L124 parenthetical "PEP/PTT separation (radar/SCG/ICG fiducials [36])": ref 36 used carotid ultrasound; NOT-SUPPORTED. Strike the fiducial list or cite other work.

**Downgrade list:**
- Claim table C1 (ref 16) STRONG to MODERATE: single observational cohort.
- C4 (ref 19) STRONG to MODERATE: sensitivity from a simulation model; single vendor study.
- C7 (refs 27, 28) STRONG to MODERATE: heterogeneous meta-analysis of associations; "precede" is temporal association only.
- C9 (refs 11, 23) STRONG to MODERATE: expert narrative review plus one N=41 study.
- C11 (refs 32, 33) STRONG: acceptable for sens/spec (regulatory); ref 33 adds nothing independent; add sponsor-data caveat.
- L46/L120 (ref 11) "suited to change detection": contradicted by the study's construct-validity finding.
- L124 (ref 24): PEP small under phenylephrine does not answer sympathetic confounding.
- L39, L121 AF via ref 21: cite an AF study or drop AF.
- L34 (ref 19): add "in a simulated arrest model".
- L22 (ref 44): "designed to meet", not "standards-grade".
- L23 (ref 10): N=261 is not tiny; separate from the small-study bullet.
- L24 (ref 2): "HR/RR good" to "moderate, heterogeneous".
- L85 (ref 39): say "radar plus oximetry, 3-class".
- L47 (ref 32): state 1,863 analysable; unify the FDA date.

**Top 5 most reliable:** 34 (FCC; numbers match), 29 and 30 (Kantrowitz, Xu; exact, limits stated), 31 (Koerber; exact, honest "mixed"), 27 (Saz-Lara; exact, heterogeneity flagged), 18 (Oberdier; exact, authors' own "not clinically applicable").

**Integrity score: 7/10.** Numbers are almost always exact, and vendor, PREPRINT, author-reported and UNSOURCED labels are used well. Deductions are for interpretive leaps: PAT "suited to change detection" against a study that found poor construct validity, AF support borrowed from a PVC study, a radar/SCG/ICG claim citing an ultrasound paper, and loss-of-pulse sensitivity quoted without noting it came from a simulation. Four STRONG tags are inflated. One orphan reference (4) and an FDA date inconsistency (11 vs 12 Sep) between the two papers.


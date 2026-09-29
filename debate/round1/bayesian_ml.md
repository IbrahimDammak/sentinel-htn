# Round 1 — Position paper: THE BAYESIAN (`bayesian_ml`)

## 1. Persona
Probabilistic ML researcher (PhD statistics/ML) working on personalized longitudinal models, change-point detection, conformal prediction and selective classification for health time series; reviewer for NeurIPS / ML4H / CHIL. My prior: when a longitudinal cohort is small, irregular and noisy, a hierarchical state-space model with sequential detection and calibrated abstention beats an end-to-end transformer, and foundation models are best used as frozen encoders. My biases are dismissing deep learning and over-engineering statistics, so I flag where evidence moves me.

## 2. Reading of the challenge: what actually scores
The six criteria RQ1–RQ6 carry 10 points each, and none rewards sensor novelty. Five are about modelling and evaluation. RQ5 scores *robustness to* bad data, not better data. The target is a slow transition (baseline → persistent change → trajectory → warning). It is judged on lead time before a clinical reference point, on false-alarm burden, and on calibrated three-state abstention. The organisers write that "an extremely early but unreliable warning is not useful". A credible paper therefore has to specify (i) event-level lead time, (ii) an alarm budget, and (iii) how misses hidden inside abstention are counted. Most teams will report per-window AUROC, so these three items are where points are cheapest.

**Reality check from the closest deployed analogue.** Apple's Hypertension Notification Feature (FDA 510(k) K250507, Sept 2025) runs a self-supervised PPG encoder, pre-trained on data from >86,000 participants, under a *linear* head. It works on 30-day windows and stays silent when data are insufficient. Against home BP ≥130/80 in 1,863 analysable participants it reached sensitivity 41.2% (95% CI 37.2–45.3) and specificity 92.3% (90.6–93.7) [bayesian_ml-4]. That task is detecting *current* hypertension. Detecting *emerging* hypertension should be harder, so any student result far above these numbers needs a leakage audit first. Applied to NHANES adults with undiagnosed hypertension, the same operating point gives PPV 69.1% and NPV 79.0%, and 58.8% of cases get no alert [bayesian_ml-5]. "No alert" does not mean "no hypertension", which is why the organisers ask for an *insufficient-evidence* state separate from "stable".

## 3. Verdict on the user's idea (F2): reframe, do not keep as stated
I read "EM signals" as ECG, bioimpedance or RF/radar, and "sudden cardiac attack" as MI or SCA.

- **Fit to scoring: poor.** The challenge data (PPG, HR/HRV, activity, sleep, context, intermittent BP) carry hypertension-trajectory labels, not MI/SCA labels. An acute-event model could not be measured against the organisers' clinical reference point, so RQ3 would score near zero.
- **Evidence for predicting sudden cardiac death from wearables is anecdotal.** The best recent item I found is one case. Change-point analysis of that patient's wearable data showed a coordinated step change about 4–6 months before death: HRV halved, and resting and nocturnal HR rose [bayesian_ml-6] (WEAK, n = 1). It supports my *method* (personal-baseline change detection), not the *target*.
- **EM-derived features do not change the modelling story.**
  - Aurora project (1,125 participants): none of four waveform models predicted next-day or 24-h cuff BP with meaningfully lower error than a baseline model. The models were tonometry+ECG, PPG+ECG, PPG alone and ECG alone [bayesian_ml-23].
  - ECG+PPG with conformal intervals on ambulatory Aurora-BP data (483 participants): daytime SBP mean absolute difference was 14.32 mmHg [bayesian_ml-10].
  - A cuff-calibrated smartwatch was stable over 28 days, but its mean difference rose to 3.4/5.1 mmHg (SBP/DBP) once true BP sat 10 mmHg from the calibration point [bayesian_ml-25]. That is exactly the regime where hypertension emerges.

  So PAT, PEP and ECG-grade nocturnal HRV/RR belong in the same state-space model as extra noisy observation channels, not as BP ground truth. Whether they help is settled by ablation A8. Any BP proxy also needs the ESH tracking tests: awake/asleep, exercise, treatment and recalibration [bayesian_ml-24].
- **Recommendation:** F1 + F4, with EM as an optional front-end. At most about 10% of effort should go to an unscored F3 acute appendix.

## 4. Proposed prototype: BayesTrack-HTN (Learn → Detect → Predict → Warn)
**Unit of analysis:** person *i*, night *t*, irregular gaps Δt. Channels *k* are nightly aggregates taken from *rest-equivalent windows* only: sleep, or stillness of 5 minutes or more at least 60 minutes after vigorous activity. Examples are nocturnal RHR, ln-RMSSD, respiratory rate, SpO2, PPG morphology or frozen-encoder PCs, and PAT when ECG is present. Each observation carries a signal-quality weight *q* ∈ (0,1].

**LEARN (RQ1, RQ4, RQ5; M1, M2, M4, M10).** A quality-weighted hierarchical local-level model:
```
y_ikt  = μ_ik(t) + β_ikᵀ c_it + ε_ikt,     ε ~ Student-t_ν(0, σ_k²/q_ikt)     (artefact-robust)
μ_ik(t) = μ_ik(t−Δt) + η,                  η ~ N(0, τ_k² Δt)                   (irregular gaps)
μ_ik(0) ~ N(m_k(z_i), s_k²),  β_ik ~ N(β_k^pop, Σ_k)                            (population prior → cold start)
```
- *c* is residual context (time since exercise, temperature, alcohol/illness flags). *z* is demographics.
- The baseline B_ik is the posterior of μ_ik over the first 14–28 valid nights.
- The deviation is z_ikt = (μ̂_ik(t) − B_ik)/sd.
- Fitting is a Kalman filter with adaptive noise. An adaptive Bayesian filter cut smartwatch HR RMSE from 2.84 to 1.21 bpm [bayesian_ml-28].
- Wearable RHR gives a more consistent picture than clinic readings [bayesian_ml-7].
- Precedent: NightSignal's streaming-median overnight-RHR baseline stabilised within 7 nights for more than 80% of participants [bayesian_ml-1].

**DETECT (RQ2; M3).** Two detectors run on a direction-signed, quality-weighted multimodal score z̃ (RHR↑, HRV↓, PAT↓, stiffness↑):
```
CUSUM:  S_it = max(0, S_i,t−1 + q_it (z̃_it − κ));   persistent change if S_it > h
BOCPD:  p(r_t | y_1:t) → P(change within L nights)   [background, pre-2021: Adams & MacKay 2007]
```
Alongside them sit a recurrence count (excursions per 30 days) and multimodal agreement (the share of channels deviating in the same direction). Persistence gating matters empirically. In a prospective cohort of 3,318 people, NightSignal raised a red alert only when RHR was ≥ baseline + 4 bpm on 2 consecutive nights. It reached 80% sensitivity, against 72% for online CuSum and 69% for RHRAD [bayesian_ml-1].

**PREDICT (RQ3; M8).** A landmark discrete-time hazard, refitted every 7 days as a penalised pooled logistic model:
```
logit P(E_i ∈ (s, s+H] | E_i > s, F_i(s)) = α_s + γᵀ F_i(s)
F_i(s) = [90-d slope of μ̂ ± SE, S_is, BOCPD prob, recurrence, agreement, latent BP-load,
          steps trend, sleep irregularity, demographics]
```
- **Cuff readings and proxies.** Intermittent cuff readings enter as sparse, low-variance observations of a latent "BP-load" state. PAT/PPG proxies enter as dense observations whose variance grows with distance from calibration [bayesian_ml-25]. This is M7 done probabilistically rather than by thresholding estimated BP.
- **Slopes add information.** In a landmark model, adding a biomarker slope raised AUC from 0.743 to 0.800 [bayesian_ml-29]. That result is from another domain, so it is analogical.
- **Context trends are predictors too, not only confounders.** Steps [bayesian_ml-26] and sleep irregularity [bayesian_ml-27] are each associated with incident hypertension.

**WARN (RQ5, RQ6; M9, M11, M14).**
1. **Calibration:** isotonic, fitted on held-out subjects. Report Brier, ECE and reliability curves, following TRIPOD+AI [bayesian_ml-22].
2. **Conformal sets:** score s = 1 − p̂_y. Calibrate on held-out *subjects* with one random landmark each, so exchangeability holds across people, not time. Online, update with adaptive conformal inference, α_{t+1} = α_t + γ(α − err_t), whenever a cuff label arrives [bayesian_ml-8, bayesian_ml-9]. Conformal selective deferral cut error on retained cases by 49.6% (in-distribution) and 46.7% (out-of-distribution) at 80% coverage on temporally split sepsis data [bayesian_ml-11].
3. **Three states:**
   - **POOR QUALITY** (suppressed): fewer than 50% valid nights out of the last 14, or a key channel missing. Apple likewise requires ≥15 usable days and stays silent on insufficient data [bayesian_ml-4].
   - **EMERGING RISK:** conformal set = {1} **and** the CUSUM/BOCPD persistence gate is met.
   - **STABLE:** set = {0}.
   - **INSUFFICIENT EVIDENCE:** anything else. After K weeks in this state, suggest a home-BP week.
4. **Alarm policy:** tune (h, α, threshold) to maximise event sensitivity at 90 days, subject to at most *b* WARN episodes per person-year, with a 90-day refractory period. Budgets must be set per **person-time**. Apple's specificity was 92.3% for one 30-day window but 86.4% across six windows (N = 187) [bayesian_ml-4]. The cautionary tale is the Epic sepsis model: it alerted on 18% of hospitalised patients and still missed 67% of sepsis cases [bayesian_ml-21].
5. **Evidence ledger:** persistence, recurrence, slope ± CI, k/K channels agreeing, rest vs post-activity share, and valid nights out of 14.

**Lead time and event metrics (E2, E3).**
- T_i is the first guideline-confirmed hypertension in the data. t_i* is the first *sustained* WARN (one not retracted within R days).
- Lead time is L_i = T_i − t_i* when t_i* ∈ [T_i − W, T_i]. An earlier WARN counts as a false alarm.
- Report Se(ℓ) for ℓ ∈ {0, 30, 90, 180} days, median L (IQR), false alarms per person-year in non-cases, and warning precision. Plot Se(90 d) against false alarms per person-year.
- **A case the system abstained on throughout counts as a miss.** Abstention time is reported as coverage.
- No point-adjust scoring: it can make even a random anomaly score look state-of-the-art [bayesian_ml-13].
- T_i depends on when BP happened to be measured. So report measurement density, and add a synthetic benchmark with injected onsets (M13).

| RQ | Component | Metrics |
|---|---|---|
| RQ1 | Hierarchical prior + personal level μ_i | A, D (with/without personalization) |
| RQ2 | CUSUM/BOCPD + recurrence + agreement | B, C |
| RQ3 | Landmark hazard + slopes | B, A |
| RQ4 | Rest-equivalent windows, β_i c, context trends | C (false alarms after activity) |
| RQ5 | Student-t noise, q-weights, Kalman over gaps | E |
| RQ6 | Calibration + conformal 3-state + ACI | D, F |

**Ablations (E7):**
- A0: population threshold.
- A1: personal z-threshold only.
- A2 to A6 add, in turn: persistence, then context, then multimodal agreement, then the hazard model, then conformal abstention.
- A7: GRU-D / mTAN / frozen-FM embeddings in place of the state-space features. This is the direct Bayes-vs-deep test.
- A8: leave one channel out at a time, including EM-derived PAT.
- Uncertainty is scored with AUGRC, which changed method rankings on 5 of 6 datasets [bayesian_ml-12].

**Robustness (E5):**
- MCAR missingness at 10–70%. Real wearable records are never complete, with mean missingness of 49% [bayesian_ml-19].
- MNAR missingness (drop active or poor-sleep nights), 7-day failure blocks, and injected motion artefacts.
- Pass condition: calibration holds while abstention rises.

**Failure-case analysis:**
- Tag each false alarm by context: infection, stress, alcohol, travel. All four triggered RHR alerts in the COVID cohort, at 1.15 alert days per person versus 3.42 in COVID-19 cases [bayesian_ml-1].
- Also track medication changes, device swaps, and people already hypertensive at enrolment. The last group is handled by the prior m_k(z) plus a parallel cross-sectional classifier.
- Stratify by age, sex and BMI. Apple's covariate-adjusted sensitivity ratios were 0.69 (age <60 vs ≥60) and 0.67 (BMI ≤30 vs >30) [bayesian_ml-4]. Wearable COVID detection accuracy also varied by age and sex [bayesian_ml-2].

**Concessions to deep learning.**
- Apple's cleared feature is built on a deep self-supervised encoder [bayesian_ml-4, bayesian_ml-18].
- Masked self-supervised pre-training on incomplete data reached AUROC 0.754 for self-reported hypertension (N = 1,250), with F1 0.651 against 0.516 for a supervised ResNet [bayesian_ml-19] (PREPRINT).
- Raindrop gained up to 11.4 absolute F1 points on irregular series [bayesian_ml-15].
- So frozen encoders enter as channels (for example the open PPG model PaPaGei [bayesian_ml-20]), and mTAN [bayesian_ml-16] and Mamba-type state-space models [bayesian_ml-17] are comparators.
- The counterweight is that a one-layer linear model beat Transformer forecasters on all nine long-horizon benchmarks [bayesian_ml-14]. I found no evidence that end-to-end deep models improve *event-level lead time* for hypertension.

```
PROTOTYPE CARD — BayesTrack-HTN
Target: Emerging hypertension; reference = first guideline-confirmed HTN (≥130/80 averaged HBPM/cuff, or organiser diagnosis label). Outputs: risk over horizon H (90/180 d), first sustained-warning timestamp.
Sensors/modalities: Sensor-agnostic. Minimum: wrist PPG + IMU (S1), sparse cuff (S10), context (S11). Optional EM channels: single-lead ECG → PAT, nocturnal HRV/RR (S2/S7); bioimpedance/radar (S3/S4) as extra y_k. Part numbers deferred to device_engineer.
Development data: Organiser data; synthetic injected-onset trajectories (M13); Aurora-BP (ECG+PPG+ABPM, 1,125 participants [23]) for the EM ablation (access terms to verify). I found no open dataset with dense pre-onset wearable data plus incident-HTN labels (All of Us has Fitbit+EHR [26,27], registered access).
RQ1 Personal baseline: Posterior μ_ik over 14–28 valid rest-equivalent nights; population prior m_k(z) for cold start, shrinkage fading with data.
RQ2 Temporal/trajectory: CUSUM + BOCPD on quality-weighted multimodal residuals; recurrence; agreement; 90-d slope ± SE.
RQ3 Early-warning / lead-time: Landmark discrete-time hazard; sustained-WARN rule; Se(ℓ), median lead time, false alarms/person-year curve; abstained cases = misses.
RQ4 Context handling: Rest-equivalent windows; residual context regression; context trends as predictors; false alarms stratified by context tag.
RQ5 Robustness: Student-t noise, SQI weights, Kalman across gaps, per-channel dropout; MCAR/MNAR/failure/noise stress tests.
RQ6 Uncertainty & abstention: Isotonic calibration + subject-level split conformal + ACI → POOR-QUALITY (suppress) / INSUFFICIENT (monitor, suggest HBPM week) / EMERGING-RISK; plus STABLE.
Evidence/explanation output: Ledger: persistence, recurrence, slope ± CI, k/K channels agreeing, rest vs post-activity share, valid nights/14, top hazard contributions.
Edge vs cloud · power · BOM: Watch: SQI + nightly aggregation. Phone: Kalman/CUSUM/BOCPD/hazard/conformal (O(K²)/night; power not measured). Cloud: prior refits, recalibration. BOM = wearable choice (device_engineer).
Validation plan: A landmark AUROC/AUPRC · B Se(ℓ), lead time · C false alarms/person-year, precision · D Brier/ECE · E dropout/MNAR/noise · F AUGRC, confidence vs evidence. Subject-wise + forward-chaining splits; calibration/conformal on disjoint subjects; TRIPOD+AI [22]; ESH tracking tests if a BP proxy is reported [24].
Regulatory / real-world path: Output = referral for HBPM confirmation, not a diagnosis. Precedent: Class II 510(k) K250507 [4]; its PCCP excludes continuously learning algorithms, so per-user Kalman updates must be argued as a locked algorithm with state.
Biggest risk + mitigation: Too few incident-HTN events with dense pre-onset data → lead-time CIs too wide. Mitigation: subject-bootstrap CIs, synthetic onset benchmark, secondary cross-sectional current-HTN task.
Buildable by a student team? YES. Wk 1–2 data audit, SQI, nightly aggregation, Kalman (statsmodels). Wk 3–4 CUSUM, BOCPD, context residuals, landmark logistic. Wk 5–6 isotonic + split conformal + 3-state + alarm-budget grid; event-level evaluation harness. Wk 7–8 ablations, robustness, report. Later: deep comparator (A7), federated refits (M12), EM hardware, prospective pilot.
```

## 5. Claims table
| ID | Claim | Refs | Strength |
|---|---|---|---|
| C1 | Personal baseline + persistence rule caught 80% of infections (median 3 d pre-symptom); beat CuSum 72% and RHRAD 69% | 1 | MODERATE |
| C2 | Wearable infection detection: AUC 0.52–0.92, presymptomatic detection 20–88% | 3 | MODERATE |
| C3 | Cleared PPG hypertension feature: sensitivity 41.2%, specificity 92.3%, 30-day windows, silent on insufficient data | 4 | STRONG |
| C4 | Population PPV 69.1%, NPV 79.0%; 58.8% of undiagnosed cases missed | 5 | MODERATE |
| C5 | Repeated windows erode specificity (86.4% over six windows) → per-person-time alarm budgets | 4 | MODERATE |
| C6 | ECG/PAT did not beat a baseline for cuff BP; ambulatory ECG+PPG error ≈14 mmHg; calibrated-watch error grows away from the calibration point | 23, 10, 25 | MODERATE |
| C7 | Wearable records never complete (mean 49% missing); masked SSL handles it; night data carry hypertension signal | 19 | WEAK |
| C8 | Deep irregular-series models can beat baselines; simple linear models beat Transformers on forecasting | 15, 14 | WEAK |
| C9 | Point-adjust inflates anomaly-detection scores → event-level metrics needed | 13 | MODERATE |
| C10 | Adaptive conformal keeps long-run coverage under shift; conformal deferral cut retained-case error 47–50% at 80% coverage | 8, 9, 11 | WEAK |
| C11 | A deployed alert model alerted on 18% of patients and missed 67% of cases | 21 | MODERATE |
| C12 | Step and sleep-regularity patterns are associated with incident hypertension | 26, 27 | MODERATE |
| C13 | Wearable prediction of sudden cardiac death rests on single-case evidence | 6 | WEAK |

## 6. Anticipated attacks and pre-emptive defence
- **"Deep or foundation models win; Bayes underfits."** Partly conceded (§4). Frozen encoders are included, and A7 decides. But the target metric is *lead time at a fixed alarm budget*, not window AUROC, and I found no deep-model evidence on that metric.
- **"Conformal needs exchangeability."** True. I calibrate across subjects and use ACI online, whose guarantee is long-run frequency [8, 9]. Coverage is marginal over people, not conditional per person, and the paper says so.
- **"A personal baseline cannot see someone already hypertensive."** True. The population prior m_k(z) and a cross-sectional channel handle this, and the subgroup is reported separately.
- **"EM sensing is the innovation" (em_engineer).** EM enters as channels, and A8 measures its marginal lead-time gain. Aurora [23] sets a sceptical prior for *absolute* BP, not for within-person *change*.
- **"No BP labels, no truth" (clinician).** Agreed. The warning is a referral for home-BP confirmation, and lead time is always measured against a recorded reference.

## 7. Risks and limitations
- Label scarcity dominates, so every lead-time number needs a CI.
- Conformal guarantees are marginal and weaken if the labelling process shifts.
- The COVID analogues work over days and hypertension over months, so the *design* transfers but the lead times do not.
- There are subgroup sensitivity gaps [4].
- Against my own bias: the minimum viable version is Kalman + CUSUM + split conformal. BOCPD and ACI are optional.

## 8. References
[bayesian_ml-1] Alavi A et al. "Real-time alerting system for COVID-19 and other stress events using wearable data." Nat Med, 2022 (epub 2021-11-29). DOI:10.1038/s41591-021-01593-2 | PMID:34845389 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=34845389&rettype=abstract&retmode=text ; https://pmc.ncbi.nlm.nih.gov/articles/PMC8799466/ — Type: prospective cohort — Key numbers: 3,318 participants, 84 SARS-CoV-2+; alerts in 67 (80%); median 3 days before symptom onset; other events 1.15 vs COVID-19 3.42 alert days/person; NightSignal = streaming median of overnight (24:00–7:00) RHR baseline, red alert at ≥4 bpm above baseline on 2 consecutive nights; specificity 87.7%; online CuSum 72%, RHRAD 69% sensitivity (Fitbit); proper baseline after 7 nights for >80% — Verified: PubMed abstract + PMC full text.

[bayesian_ml-2] Mason AE et al. "Detection of COVID-19 using multimodal data from a wearable device: results from the first TemPredict Study." Sci Rep, 2022. DOI:10.1038/s41598-022-07314-0 | PMID:35236896 — URL fetched: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=35236896&rettype=abstract&retmode=text — Type: cohort (Oura ring; 63,153 participants; 73 PCR-confirmed used for training) — Key numbers: 2.75 days before testing on average; sensitivity 82%, specificity 63%; AUC 0.819 (0.809–0.830); temperature +4.9% AUC; accuracy varied by age and sex — Verified: PubMed abstract.

[bayesian_ml-3] Mitratza M et al. "The performance of wearable sensors in the detection of SARS-CoV-2 infection: a systematic review." Lancet Digit Health, 2022;4(5):e370-e383. DOI:10.1016/S2589-7500(22)00019-X | PMID:35461692 — URL fetched: efetch PMID 35461692 — Type: systematic review (12 articles, 12 protocols) — Key numbers: AUC 0.52–0.92; presymptomatic detection 20–88% of cases, from 14 to 1 days before onset; mostly moderate risk of bias — Verified: PubMed abstract.

[bayesian_ml-4] U.S. FDA. 510(k) Summary K250507, "Hypertension Notification Feature (HTNF)," Apple Inc., cleared 2025-09-11 — URL fetched: https://www.accessdata.fda.gov/cdrh_docs/pdf25/K250507.pdf — Type: regulatory — Key numbers: self-supervised DL encoder (unlabeled Apple Watch data, >86,000 participants) + linear model; development data 9,800 participants with home BP; 30-day windows; HTN = mean SBP ≥130 or DBP ≥80; 2,229 enrolled, 1,863 with ≥15 usable days; sensitivity 41.2% (37.2–45.3), specificity 92.3% (90.6–93.7); stage-2 sensitivity 53.7%; sensitivity risk ratio age <60 vs ≥60 0.69 (0.55–0.85), BMI ≤30 vs >30 0.67 (0.55–0.81); longitudinal specificity 86.4% (80.2–92.5), six 30-day windows, N = 187; "will not surface a notification if insufficient data is collected"; PCCP excludes continuously learning algorithms; predicate DEN230003 — Verified: full PDF text extracted.

[bayesian_ml-5] Cohen JB et al. "Impact of a Smartwatch Hypertension Notification Feature for Population Screening." JAMA, 2026;335(11):1001-1003. DOI:10.1001/jama.2025.26925 | PMID:41661624 — URL fetched: https://pmc.ncbi.nlm.nih.gov/articles/PMC12887835/ — Type: cross-sectional (NHANES modelling) — Key numbers: 3,983 NHANES adults unaware of HTN (representing 127 million); using manufacturer-reported sensitivity/specificity: PPV 69.1% (63.3–74.9), NPV 79.0% (76.6–81.3); 58.8% of undiagnosed HTN get no alert — Verified: PMC full text.

[bayesian_ml-6] Lautman Z et al. "Longitudinal Changes in Wearable-Captured Physiology Before Sudden Cardiac Death." JACC Case Rep, 2026 (online ahead of print). DOI:10.1016/j.jaccas.2026.110397 | PMID:42788912 — URL fetched: efetch PMID 42788912 — Type: case report (n = 1) — Key numbers: 76-year-old man with structural heart disease; change-point analysis: most changes 4–6 months before SCD; HRV halved; resting and nocturnal HR rose — Verified: PubMed abstract.

[bayesian_ml-7] Dunn J et al. "Wearable sensors enable personalized predictions of clinical laboratory measurements." Nat Med, 2021;27(6):1105-1112. DOI:10.1038/s41591-021-01339-0 | PMID:34031607 — URL fetched: efetch PMID 34031607 — Type: prospective cohort — Key numbers: wearable RHR "more consistent and precise" than clinic RHR; monitoring length and proximity to prediction date matter — Verified: PubMed abstract.

[bayesian_ml-8] Gibbs I, Candès E. "Adaptive Conformal Inference Under Distribution Shift." arXiv:2106.00170, 2021 — URL fetched: https://export.arxiv.org/api/query?id_list=2106.00170 ; https://arxiv.org/abs/2106.00170 — Type: PREPRINT (methods) — Key numbers: provably achieves target coverage frequency over long intervals irrespective of the data-generating process — Verified: arXiv abstract.

[bayesian_ml-9] Zaffran M et al. "Adaptive Conformal Predictions for Time Series." arXiv:2202.07282, 2022 — URL fetched: https://export.arxiv.org/api/query?id_list=2202.07282 — Type: PREPRINT (methods, simulation) — Key numbers: analyses the ACI learning rate; proposes parameter-free AgACI — Verified: arXiv abstract.

[bayesian_ml-10] Shen Z et al. "Conformal prediction quantifies wearable cuffless blood pressure with certainty." Sci Rep, 2025;15:26697. DOI:10.1038/s41598-025-09580-0 | PMID:40695893 — URL fetched: efetch PMID 40695893 — Type: validation study (retrospective, Aurora-BP) — Key numbers: 483 ambulatory participants; ECG+PPG quantile GBRT + conformal CIs; daytime MAD SBP 14.32 / DBP 9.53 mmHg; nighttime 14.22 / 10.13 mmHg — Verified: PubMed abstract.

[bayesian_ml-11] Kwon H, Kim DJ. "Conformal selective prediction with cost aware deferral for safe clinical triage under distribution shift." Sci Rep, 2026;16:10016. DOI:10.1038/s41598-026-40637-w | PMID:41721063 — URL fetched: efetch PMID 41721063 — Type: retrospective (early sepsis prediction, temporally separated splits) — Key numbers: retained-case error reduced 49.6% (ID) and 46.7% (OOD) at 80% coverage — Verified: PubMed abstract.

[bayesian_ml-12] Traub J et al. "Overcoming Common Flaws in the Evaluation of Selective Classification Systems." arXiv:2407.01032, 2024 — URL fetched: https://export.arxiv.org/api/query?id_list=2407.01032 — Type: PREPRINT (benchmark) — Key numbers: AUGRC; 6 datasets, 13 confidence-scoring functions; rankings change on 5 of 6 datasets — Verified: arXiv abstract.

[bayesian_ml-13] Kim S et al. "Towards a Rigorous Evaluation of Time-Series Anomaly Detection." AAAI, 2022. DOI:10.1609/aaai.v36i7.20680 | arXiv:2109.05257 — URL fetched: https://export.arxiv.org/api/query?id_list=2109.05257 ; https://api.crossref.org/works?query.bibliographic=Towards+a+Rigorous+Evaluation+of+Time-Series+Anomaly+Detection — Type: bench/lab — Key numbers: point adjustment can make a random anomaly score state-of-the-art; untrained model comparable to existing methods without PA — Verified: arXiv abstract + Crossref metadata.

[bayesian_ml-14] Zeng A et al. "Are Transformers Effective for Time Series Forecasting?" AAAI, 2023. DOI:10.1609/aaai.v37i9.26317 | arXiv:2205.13504 — URL fetched: https://arxiv.org/abs/2205.13504 ; api.crossref.org — Type: bench/lab — Key numbers: one-layer LTSF-Linear beats Transformer LTSF models "in all cases" on nine real-life datasets — Verified: arXiv abstract + Crossref.

[bayesian_ml-15] Zhang X et al. "Graph-Guided Network for Irregularly Sampled Multivariate Time Series" (Raindrop). arXiv:2110.05357, 2021 — URL fetched: https://export.arxiv.org/api/query?id_list=2110.05357 — Type: PREPRINT (bench) — Key numbers: up to 11.4% absolute F1 over state-of-the-art on three healthcare and human-activity datasets — Verified: arXiv abstract.

[bayesian_ml-16] Shukla SN, Marlin BM. "Multi-Time Attention Networks for Irregularly Sampled Time Series." arXiv:2101.10318, 2021 — URL fetched: https://export.arxiv.org/api/query?id_list=2101.10318 — Type: PREPRINT (bench) — Key numbers: as good as or better than baselines, with faster training — Verified: arXiv abstract.

[bayesian_ml-17] Gu A, Dao T. "Mamba: Linear-Time Sequence Modeling with Selective State Spaces." arXiv:2312.00752, 2023 — URL fetched: https://export.arxiv.org/api/query?id_list=2312.00752 — Type: PREPRINT (architecture) — Key numbers: selective SSM, linear-time in sequence length — Verified: arXiv abstract.

[bayesian_ml-18] Abbaspourazad S et al. "Large-scale Training of Foundation Models for Wearable Biosignals." arXiv:2312.05409, 2023 (arXiv comment: "Camera ready version for ICLR 2024") — URL fetched: https://arxiv.org/abs/2312.05409 — Type: PREPRINT — Key numbers: PPG and ECG from ~141K participants over ~3 years (Apple Heart and Movement Study); embeddings encode demographics and health conditions — Verified: arXiv abstract page.

[bayesian_ml-19] Xu MA et al. "LSM-2: Learning from Incomplete Wearable Sensor Data." arXiv:2506.05321, 2025 — URL fetched: https://arxiv.org/html/2506.05321v1 — Type: PREPRINT — Key numbers: 40M hours pre-training; "0% of records are complete", mean missingness 49% (median 48%, SD 15%, range 2–80%); self-reported hypertension (N = 1,250 of 4,416 enrolled): AUROC 0.754, F1 0.651 vs supervised ResNet F1 0.516; removing nighttime data → ~5% F1 degradation — Verified: arXiv HTML full text.

[bayesian_ml-20] Pillai A et al. "PaPaGei: Open Foundation Models for Optical Physiological Signals." arXiv:2410.20542, 2024 — URL fetched: https://export.arxiv.org/api/query?id_list=2410.20542 — Type: PREPRINT — Key numbers: open PPG foundation model; >57,000 hours, 20M segments; 20 tasks across 10 datasets — Verified: arXiv abstract.

[bayesian_ml-21] Wong A et al. "External Validation of a Widely Implemented Proprietary Sepsis Prediction Model in Hospitalized Patients." JAMA Intern Med, 2021;181(8):1065-1070. DOI:10.1001/jamainternmed.2021.2626 | PMID:34152373 — URL fetched: efetch PMID 34152373 — Type: retrospective cohort — Key numbers: 27,697 patients / 38,455 hospitalisations; AUROC 0.63 (0.62–0.64); missed 1,709 of 2,552 sepsis cases (67%) while alerting on 6,971 of 38,455 (18%) — Verified: PubMed abstract.

[bayesian_ml-22] Collins GS et al. "TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods." BMJ, 2024;385:e078378. DOI:10.1136/bmj-2023-078378 | PMID:38626948 — URL fetched: efetch PMID 38626948 — Type: guideline — Key numbers: 27-item checklist; supersedes TRIPOD 2015 — Verified: PubMed abstract.

[bayesian_ml-23] Mukkamala R et al. "The Microsoft Research Aurora Project: Important Findings on Cuffless Blood Pressure Measurement." Hypertension, 2023;80(3):534-540. DOI:10.1161/HYPERTENSIONAHA.122.20410 | PMID:36458550 — URL fetched: efetch PMID 36458550 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC9931644/ — Type: review of a validation study (Mieloszyk et al., IEEE JBHI 2022, DOI:10.1109/JBHI.2022.3153259, checked via Crossref) — Key numbers: 1,125 participants (642 auscultatory arm, 483 ambulatory arm); none of four waveform-feature models (tonometry+ECG, PPG+ECG, PPG, ECG) predicted next-day auscultatory or 24-h ambulatory cuff BP with meaningfully lower error than the baseline model; results "clear-cut negative" — Verified: abstract + PMC full text.

[bayesian_ml-24] Stergiou GS et al. "European Society of Hypertension recommendations for the validation of cuffless blood pressure measuring devices." J Hypertens, 2023;41(12):2074-2087. DOI:10.1097/HJH.0000000000003483 | PMID:37303198 — URL fetched: efetch PMID 37303198 — Type: guideline/consensus — Key numbers: six tests: static, device position, treatment, awake/asleep, exercise, recalibration — Verified: PubMed abstract.

[bayesian_ml-25] Walzel S et al. "Long-term accuracy and stability of blood pressure measurements from a smartwatch: Prospective validation study." Digit Health, 2026;12:20552076261415923. DOI:10.1177/20552076261415923 | PMID:41602947 — URL fetched: efetch PMID 41602947 — Type: validation study (prospective, single-arm) — Key numbers: 37 participants, 28 days, Samsung Galaxy Watch 5 vs Omron M4; MD SBP −0.34, DBP 0.62 mmHg; drift −0.19 / 1.02 mmHg; with reference BP 10 mmHg from the calibration point, MD 3.4 (SBP) / 5.1 (DBP) mmHg — Verified: PubMed abstract.

[bayesian_ml-26] Master H et al. "Association of step counts over time with the risk of chronic disease in the All of Us Research Program." Nat Med, 2022;28(11):2301-2308. DOI:10.1038/s41591-022-02012-w | PMID:36216933 — URL fetched: efetch PMID 36216933 — Type: retrospective cohort (Fitbit + EHR) — Key numbers: 6,042 participants, median 4.0 years; nonlinear relation with incident hypertension (n = 482), no further risk reduction above 8,000–9,000 steps — Verified: PubMed abstract.

[bayesian_ml-27] Zheng NS et al. "Sleep patterns and risk of chronic disease as measured by long-term monitoring with commercial wearable devices in the All of Us Research Program." Nat Med, 2024;30(9):2648-2656. DOI:10.1038/s41591-024-03155-8 | PMID:39030265 — URL fetched: efetch PMID 39030265 — Type: retrospective cohort — Key numbers: 6,785 participants, median 4.5 years; sleep irregularity associated with incident hypertension; J-shaped association of sleep duration with hypertension — Verified: PubMed abstract.

[bayesian_ml-28] Cossu L et al. "Adaptive and self-learning Bayesian filtering algorithm to statistically characterize and improve signal-to-noise ratio of heart-rate data in wearable devices." J R Soc Interface, 2024;21(218):20240222. DOI:10.1098/rsif.2024.0222 | PMID:39226927 — URL fetched: efetch PMID 39226927 — Type: validation study (Garmin Vivoactive 4; ALS/MS patients) — Key numbers: RMSE 2.84 → 1.21 bpm; MARE 3.46% → 1.36% — Verified: PubMed abstract.

[bayesian_ml-29] Finelli A et al. "Comparison of Joint and Landmark Modeling for Predicting Cancer Progression in Men With Castration-Resistant Prostate Cancer." JAMA Netw Open, 2021;4(6):e2112426. DOI:10.1001/jamanetworkopen.2021.12426 | PMID:34129025 — URL fetched: efetch PMID 34129025 — Type: prognostic study (secondary analysis of RCT, 763 men) — Key numbers: adding PSA slope to landmark models: AUC 0.743 → 0.800 at month 10 — Verified: PubMed abstract.

[background, pre-2021] Adams RP, MacKay DJC. "Bayesian Online Changepoint Detection." arXiv:0710.3742, 2007 — URL fetched: https://export.arxiv.org/api/query?id_list=0710.3742 — algorithm origin only; not the sole support of any claim.

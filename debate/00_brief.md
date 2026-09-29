# Shared Debate Brief — BioVance AIoT Challenge × "EM signals for sudden cardiac attack"

Today's date: 2026-09-29. Every debater reads this file first. It is the single source of truth for the challenge text, the user's idea, the idea catalogue (with IDs you must reference), the evidence rules, and the file layout.

Original PDF (image-only, 2 pages): `C:\Users\Lenovo\Downloads\BioVance Technical Challenge.pdf`
Rendered pages (you can open them with the Read tool as images):
- `C:\Users\Lenovo\AppData\Local\Temp\claude\C--Users-Lenovo-AppData-Roaming-Claude-scratch-workspaces-7bef7003-202a-461f-8904-cd460ee4efbe-83caa651-f07d-4cfb-a91b-4e4d8fcdcdc2-scratch-2026-09-28-8b8ef1\a0a2aee5-d9e3-4f85-bd8d-166179ded0a9\scratchpad\page1.png`
- `...same folder...\page2.png`

---

## PART 1 — The challenge (faithful transcription)

**Organisers:** IEEE EMBS Tunisia Section, IEEE EMBS Student Branch École Polytechnique de Sousse, IEEE EMBS.
**Title:** *BioVance — An AIoT Challenge for Personalized Early Detection of Emerging Hypertension.*
**Tagline:** From episodic blood pressure checks to continuous, personalized, uncertainty-aware early warning.

### 1. Background & Motivation
- **Core problem:** Hypertension is a major cardiovascular risk factor that can develop silently for years. Conventional BP checks give only intermittent snapshots of a process that evolves continuously.
- Quote: *"By the time hypertension is detectable, important physiological changes may have already occurred."*
- Wearables and IoT enable continuous multimodal sensing (PPG, heart rate, HRV, activity, sleep). But continuous sensing alone is not enough: signals are noisy, individual, context dependent, and population-level thresholds miss personal deviations.
- **The real challenge:** detect whether an individual's physiology is progressively departing from their own baseline toward hypertension risk, as early and reliably as possible.

### 2. Problem Statement & Data Environment
- For individual *i* at time *t*: `X_i(t) = {P, H, A, S, C, ...}` — P: PPG & cardiovascular signals; H: heart rate & HRV; A: activity/motion; S: sleep; C: context/behaviour.
- Rather than only `X(t) → Hypertension`, the challenge asks: `X(1:t) → Baseline → Change → Trajectory → Early Warning`.
- **AIoT data environment:** Physiological: PPG, heart rate, HRV, SpO2, respiration · Behavioural: activity, sedentary time, sleep, temporal patterns · Clinical: intermittent BP, demographics, longitudinal labels.
- Data intentionally reflects real AIoT conditions: missing observations, irregular sampling, sensor noise, motion artefacts, missing modalities, varying data quality. *"This is not a clean dataset classification problem."*
- (Unknown: whether organisers ship raw waveforms or pre-aggregated features. Design for both.)

### 3. Research Question
*Can longitudinal multimodal AIoT data identify an individual's transition from stability to emerging hypertension risk before clinical detection?*
- **RQ1 Personalization:** learn a personal baseline vs. population variability?
- **RQ2 Temporal reasoning:** detect persistent change, not isolated readings?
- **RQ3 Early detection:** how far ahead of clinical detection?
- **RQ4 Context awareness:** physiology changing, or just the situation?
- **RQ5 Reliability:** robust to noisy / incomplete IoT data?
- **RQ6 Uncertainty:** abstain when evidence is insufficient?

### 4. Key Concepts: Baseline, Trajectory & Context
- **Personal baseline problem:** a value unusual for one person may be normal for another. `B_i = f(X_i(1:t0))`, `D_i(t) = X_i(t) − B_i`. What is a meaningful deviation *for this individual*?
- **From deviation to trajectory:** an isolated deviation should not automatically trigger an alert. Assess persistence, recurrence, increasing magnitude, multimodal agreement, temporal consistency.
  - Baseline → isolated deviation (transient)
  - Baseline → repeated deviation → persistent change → emerging trajectory → early risk warning
  - How can AI distinguish transient variability from an emerging pathological trajectory?
- **Context-aware detection:** a cardiovascular change right after intense activity should not be read the same way as a similar change occurring repeatedly at rest. Abnormal because the person is changing, or because the situation changed?

### 5. Objective & Expected Output
- Four stages: **Learn → Detect → Predict → Warn** (Learn: represent the individual's normal state · Detect: identify meaningful deviations · Predict: assess if deviations form a risk trajectory · Warn: interpretable, uncertainty-aware alert).
- **Uncertainty & abstention** — three states: *Sufficient evidence* → emerging risk signal detected; *Insufficient evidence* → no reliable conclusion, keep monitoring; *Poor-quality observation* → warning suppressed.
- **Early-warning requirement:** detecting hypertension only once clinically apparent does not meet the objective. Maximise lead time between the first *reliable* AI warning and the clinical reference point. *An extremely early but unreliable warning is not useful.* (Baseline → Emerging change → Clinical detection; AI early warning ← Lead Time →.)
- **Required system outputs:** Risk estimate (emerging HTN risk) · Early-warning time (timestamp of first strong signal) · Confidence/uncertainty · Evidence (contributing physiological/contextual factors) · Data-quality assessment (sufficiency of observations). From "Hypertension: Yes/No" to a calibrated, evidence-backed early-risk statement.

### 6. Evaluation Framework
A. Predictive: AUROC, AUPRC, sensitivity, specificity, F1 · B. Early detection: lead time, % events caught early, sensitivity · C. False-alarm burden: alarms/individual, warning precision · D. Calibration: Brier, ECE, calibration curves · E. Robustness: missing modalities, noise, sensor failure · F. Uncertainty quality: confidence drops when evidence is weak.

### 7. Research Expectations & Directions
- Teams submit a research-oriented technical report, not only a model: problem formulation & related work; methodology & architecture; personalization & temporal modelling; missing/noisy IoT data handling; early warning & uncertainty; ablations, failure cases, interpretability; limitations & future work.
- Quote: *"Who developed the most credible scientific approach to detecting risk earlier, rather than just the most accurate model?"*
- Suggested directions (algorithmically open): temporal transformers, RNNs, state-space models · anomaly & change-point detection · self-supervised & multimodal representation learning · Bayesian/uncertainty-aware AI · personalized, few-shot & continual learning · federated learning · explainable AI · edge AI.
- Expected contribution: move cardiovascular monitoring from episodic detection to continuous, personalized, proactive early warning; show subtle longitudinal change is an actionable signal before HTN becomes clinically evident.

### 8. Deliverables
Research paper (≤5 pages, IEEE conference format: Abstract, Intro, Related Work, Methodology, System Architecture, Experiments, Results, Limitations, Conclusion, References) · Presentation (≤15 slides) · GitHub repository.

### 9. Scoring (/60)
RQ1 Personalization 10 · RQ2 Temporal reasoning 10 · RQ3 Early detection 10 · RQ4 Context awareness 10 · RQ5 Reliability 10 · RQ6 Uncertainty 10.

---

## PART 2 — The user's idea (verbatim intent)

> "My idea is to have an AI model that uses **electromagnetic signals** to detect **sudden or premature cardiac attack**."

The user wants: all possible ideas extracted from the challenge; agents with distinct backgrounds/beliefs to critique each other using **recent** facts and research papers; each theory defended; and the **optimal prototype that can be built and engineered in a real situation.**

Ambiguities every debater must handle explicitly (state which interpretation you evaluate):
- "Electromagnetic signals" may mean: ECG (bio-potential), bioimpedance (IPG/ICG), RF/radar (mmWave FMCW, UWB, CW Doppler), near-field coherent sensing (NCS), magnetocardiography (MCG, e.g. optically-pumped magnetometers), capacitive ECG, RF resonator sensors.
- "Sudden or premature cardiac attack" may mean: acute myocardial infarction, sudden cardiac arrest (SCA / VT-VF), premature (early-onset) cardiac events, or premature beats (PVCs).

**Moderator's framing (not a conclusion):** the challenge's target is *emerging hypertension* — a slow, longitudinal process scored on RQ1–RQ6 — whereas the user's idea targets *acute* cardiac events. The debate must settle, on evidence: (a) does the idea as stated fit this challenge's scoring? (b) can/should it be reframed (e.g. EM sensing as the physiological front-end of a hypertension-trajectory system)? (c) what prototype is optimal *and* engineerable in the real world? Honesty over flattery: the user asked for critique grounded in facts.

---

## PART 3 — Idea catalogue (reference these IDs; add new ones as `NEW-<yourslug>-n`)

**F — Problem framing**
- F1 Emerging-hypertension trajectory (the challenge target): warn before clinical detection.
- F2 User's original target: EM signals → sudden/premature cardiac attack (MI / SCA / early-onset events).
- F3 Hybrid: HTN-trajectory engine primary + acute-event safety channel (arrhythmia/ischemia flags) secondary.
- F4 Reframe: EM sensing as front-end for the HTN challenge (ECG, bioimpedance, RF → PAT/PTT/PWV, PEP, HRV, respiration) feeding the personalized trajectory model.
- F5 Formulation choice: time-to-event/hazard forecasting vs anomaly/change detection vs cuffless-BP estimation + thresholding.

**S — Sensing / modality**
- S1 Wrist PPG + accelerometer (commodity smartwatch).
- S2 PPG + single-lead ECG (watch/ring/patch) → pulse arrival time (PAT); multi-site PPG → PTT.
- S3 Bioimpedance (wrist/finger IPG, e-tattoos, ICG) → pulse, PTT/BP surrogates, stroke volume.
- S4 RF/radar (mmWave FMCW 60/77 GHz, UWB impulse, CW Doppler) → contactless HR/RR/HRV, pulse wave, radar-PTT/BP, sleep; RF-to-ECG reconstruction.
- S5 Near-field coherent sensing (NCS) RF tags.
- S6 Magnetocardiography (OPM-MCG) → ischemia/MI detection.
- S7 Capacitive / textile / dry-electrode ECG (garment, bed, seat).
- S8 Seismo-/ballistocardiography (mechanical, non-EM comparator) + ECG → PEP, PTT.
- S9 Wearable ultrasound (non-EM comparator) for BP waveform.
- S10 Cuff BP (home/ambulatory) as sparse labels/calibration.
- S11 Context sensors: IMU, skin/ambient temperature, time/location, phone use, questionnaires (caffeine, salt, alcohol, stress), sleep staging.
- S12 Smartphone camera rPPG / facial video.

**M — Modelling**
- M1 Personal baseline via robust statistics (rolling median/MAD, EWMA), context-stratified (rest/sleep/activity/time-of-day).
- M2 Hierarchical Bayesian / mixed-effects (population prior + individual effects) → personalization, cold start.
- M3 Change-point & sequential detection (BOCPD, CUSUM, EWMA charts, SPRT) on personal residuals D_i(t).
- M4 State-space / latent dynamics (Kalman/DLM, Gaussian processes, switching SSM, S4/Mamba, neural ODE/CDE).
- M5 Missingness-aware deep sequence models (GRU-D, mTAN, Raindrop, masked temporal transformers, TCN).
- M6 Self-supervised / foundation models for wearable biosignals as encoders; multimodal contrastive learning.
- M7 Cuffless BP estimation (PPG/PAT → BP with periodic cuff calibration) as an intermediate, then trajectory on estimated BP.
- M8 Direct risk modelling: discrete-time hazard, landmarking, joint longitudinal–survival models.
- M9 Uncertainty: ensembles, MC dropout, Bayesian posteriors, conformal prediction (incl. time-series/adaptive), evidential DL, selective prediction/reject option, SQI-gated abstention.
- M10 Context modelling: activity recognition, post-exercise windows, sleep vs wake, circadian phase, covariate normalisation ("rest-equivalent" values).
- M11 Explainability: evidence ledger (persistence, recurrence, magnitude trend, multimodal agreement, temporal consistency), SHAP/attributions, prototypes.
- M12 Federated / on-device / continual learning; edge AI (TinyML) for SQI + features.
- M13 Synthetic data / digital twins / physiological simulation for pre-training and stress-testing.
- M14 Alarm policy: tiered alerts, hysteresis, alarm budget per person-month, decision-theoretic thresholds, lead-time vs precision trade-off.

**E — Evaluation**
- E1 Subject-wise and forward-chaining temporal splits; no calibration/subject leakage.
- E2 Lead time vs clinical reference; % events caught early; event-level sensitivity.
- E3 False-alarm burden (alarms/person-month), warning precision.
- E4 Calibration (Brier, ECE, reliability curves).
- E5 Robustness: modality dropout, noise injection, sensor-failure simulation, MCAR/MAR/MNAR missingness.
- E6 Uncertainty quality: risk–coverage curves (AURC), selective accuracy, confidence vs evidence strength.
- E7 Ablations: no personalization / no context / no uncertainty / per-modality.
- E8 Fairness: skin tone (optical bias), age, sex, BMI.

**R — Real-world engineering**
- R1 Validation standards for cuffless BP (e.g. ISO 81060-3:2022, IEEE 1708a, ESH validation recommendations).
- R2 Regulatory path (FDA 510(k)/De Novo precedents, EU MDR class, IEC 60601-1, IEC 62304, ISO 14971).
- R3 Hardware BOM & power budget; edge vs cloud split; battery life.
- R4 Privacy/security (GDPR; Tunisian Organic Law 2004-63), federated learning.
- R5 Human factors: alarm fatigue, actionable messaging, confirmation via HBPM/ABPM, clinician-in-the-loop.
- R6 Cost/access in LMIC settings (Tunisia/Africa).

---

## PART 4 — Evidence rules (non-negotiable)

1. **Recency:** every factual claim must be supported by ≥1 source published **2021-01-01 or later** (prefer 2023–2026). Pre-2021 works may appear only as `[background, pre-2021]` for definitions/algorithm origins and can never be the sole support of a claim.
2. **Admissible sources:** peer-reviewed papers; clinical guidelines/consensus statements; regulatory decisions (FDA 510(k)/De Novo summaries, CE); standards (ISO/IEC/IEEE); preprints (arXiv/medRxiv/bioRxiv) **labelled PREPRINT**. Company press releases/blogs only as `INDUSTRY-CLAIM` and never as scientific proof.
3. **Retrieved, not remembered:** cite only what you actually retrieved this session (abstract or full text). Never invent or reconstruct a citation from memory. If you cannot verify it now, do not use it.
4. **Reference entry format (mandatory):**
   `[<slug>-<n>] First-author et al. "Title." Venue, Year. DOI:… | PMID:… | arXiv:… — URL fetched: <url> — Type: <meta-analysis | RCT | prospective cohort | retrospective | validation study | bench/lab | simulation | review | guideline | regulatory | standard | PREPRINT | INDUSTRY-CLAIM> — Key numbers: <N, setting, metric values, validation protocol> — Verified: <how>`
5. **Numbers exactly as reported**, with population (ICU vs lab vs free-living), N, and protocol (subject-independent? calibrated? how often?).
6. **Evidence strength tags on every claim:** STRONG (meta-analysis/large prospective/regulatory-validated) · MODERATE (validation studies, mid-size cohorts) · WEAK (small lab studies, simulations, preprints, single-site).
7. An independent **Auditor** checks every reference (existence, year, metadata, claim–source match, overstatement). Flagged claims are struck.

## PART 5 — Research tools

> **Status update (2026-09-29, mid-round-1):** Europe PMC returns HTTP 503/timeouts under load; OpenAlex has paused anonymous *search* (site-wide outage); www.analog.com is unreachable from this machine. **Working:** PubMed E-utilities, Crossref, arXiv, ti.com, WebSearch, WebFetch. Use the shared failure-tolerant helper `debate/tools/fetch.py` (`from fetch import get, get_json` — retries with backoff, returns None instead of raising). Machine citation pre-check: `python debate/tools/refcheck.py <out.md> <papers...>`.

- `WebSearch`, `WebFetch` (if not directly callable, load them via `ToolSearch` with query `select:WebSearch,WebFetch`).
- Scholarly APIs via Bash `curl` or Python 3.10 + `requests`:
  - Europe PMC (abstracts, year filter): `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=<q>%20AND%20PUB_YEAR:[2021%20TO%202026]&format=json&pageSize=25&resultType=core`
  - PubMed search: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<q>&mindate=2021&maxdate=2026&datetype=pdat&retmode=json` · abstracts: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=<pmids>&rettype=abstract&retmode=text`
  - Crossref DOI check: `https://api.crossref.org/works/<DOI>`
  - OpenAlex: `https://api.openalex.org/works?search=<q>&filter=from_publication_date:2021-01-01`
  - arXiv: `https://export.arxiv.org/api/query?search_query=all:<q>&max_results=20&sortBy=submittedDate`
  - Semantic Scholar returns HTTP 429 (rate-limited) — avoid or back off.
- Do **not** use the in-app browser pane (shared by all agents — you would collide). Read-only lookups only; no sign-ups, forms, or executable downloads. Write only inside `debate/`.

## PART 6 — Standard PROTOTYPE CARD (every position paper must end its proposal with one)
```
PROTOTYPE CARD — <name>
Target (exactly what is detected/predicted, and the clinical reference point):
Sensors/modalities (part numbers if hardware):
Development data (datasets, availability, licence):
RQ1 Personal baseline:
RQ2 Temporal/trajectory:
RQ3 Early-warning / lead-time strategy:
RQ4 Context handling:
RQ5 Robustness to missing/noisy data:
RQ6 Uncertainty & abstention (3-state output):
Evidence/explanation output:
Edge vs cloud split · power · BOM cost estimate:
Validation plan (metrics A–F, splits, standards):
Regulatory / real-world path:
Biggest risk + mitigation:
Buildable by a student team for the challenge? (what in 4–8 weeks, what later):
```

## PART 7 — Rounds & file layout (all paths under `debate/`)
- **Round 1 — Position papers:** `round1/<slug>.md` (1,500–2,500 words + references). Sections: 1 Persona · 2 Reading of the challenge (what actually scores) · 3 Verdict on the user's idea (keep / reframe / reject — with evidence) · 4 Proposed prototype + PROTOTYPE CARD · 5 Claims table (ID | claim | refs | strength) · 6 Anticipated attacks & pre-emptive defence · 7 Risks/limitations · 8 References.
- **Audit 1:** `audit/audit_round1.md` (Auditor).
- **Round 2 — Cross-critique:** `round2/<slug>.md` — for each other debater: strongest point, weakest point + counter-evidence, pointed questions; then your concessions and updated position.
- **Round 3 — Defence & final position:** `round3/<slug>.md` — answer every critique aimed at you and every audit flag on your references; revised PROTOTYPE CARD; final ranking of all proposals scored on RQ1–RQ6 (0–10 each) + evidence strength + engineerability.
- **Audit 2:** `audit/audit_round3.md`.
- **Verdict:** `verdict/verdict.md` (Chair).

Debater slugs: `clinician`, `em_engineer`, `ppg_scientist`, `physiologist`, `bayesian_ml`, `device_engineer`. Oversight: `auditor`, `chair`.

# Round 2 — Cross-critique: THE PHYSIOLOGIST (`physiologist`)

*Prior position: NOCTURNE (`round1/physiologist.md`). Other debaters' sources are cited by their round-1 IDs; [PS-n] = [ppg_scientist-n]. "My derivation" marks my own arithmetic on published numbers. Claim audits A–C did not exist when I drafted this.*

## 1. Cross-critique

### 1.1 clinician — CONFIRM-HTN
**Steelman.** The decisive variable is the reference point, not the sensor. Only a persistence-confirmed, out-of-office `t_ref` (C1–C2) gives lead time a meaning. In 59,124 patients, night-time SBP was the most informative BP measure [clinician-18].

**Attack.**
- *§3 point 4 ("emerging hypertension is base-rate-friendly") misapplies C6.* The 70.9% PPV was for *prevalent* hypertension at 31.4% prevalence [clinician-15]. The challenge predicts *transition*. Incidence in the cited cohorts runs from about 2.5%/yr (498/4,897 over 4.0 y [physiologist-6]) to about 4.6%/yr (40,268/232,587 over 3.8 y [physiologist-1]), which is 0.6–1.1% per 90 days. At HTNF's operating point, PPV would then be about 3–6% (my derivation). Emerging hypertension has a friendlier base rate than SCA, but it is not friendly.
- *The nocturnal/masked flag has no sensor.* C2–C3 motivate an "→ ABPM" flag. Yet the only wrist-cuffless night data cited over-read night SBP by 15.5 mmHg and under-read the dip by 14.2 mmHg [clinician-13].
- *Internal inconsistency.* C5 says PAT adds nothing beyond calibration, yet the card puts "PAT at rest/sleep" into the ledger. C5's drug-tracking half rests on n = 3 [clinician-13]; N = 166 [PS-11] is the better support.
- *C12 (≥3 months) is expert inference, not MODERATE evidence.* The guideline windows [clinician-2, -5] describe deferring treatment *after* detection.

**Questions.** Q1: Which wearable feature triggers the nocturnal flag, and on what evidence? Q2: With PPV of about 3–6% at a 90-day horizon, what specificity does CONFIRM-HTN need? Does the horizon have to become 1–2 years? Q3: Keep PAT or drop it?

### 1.2 em_engineer — EM-ANCHOR
**Steelman.** This is the most self-critical paper. It has an explicit for/against ledger (§3.4) and a pre-registered kill criterion. The PVC reading is the one form of F2 that wearable ECG genuinely supports (PVC burden vs Holter −0.07% [em_engineer-21]).

**Attack.**
- *C8's r = −0.82 is an acute-perturbation number* [em_engineer-25]. It comes from within-session induced BP changes, where PEP moves strongly: it halves under physical stress and falls 16% under mental stress [physiologist-13]. Emerging hypertension is a resting, vascular change. Under pure vasoconstriction PEP moved the opposite way (+5.5 ms vs −16.8 ms for PTT [em_engineer-24]), so PAT captured only about two-thirds of the vascular change (my derivation). The mental-stress PEP shift alone (−14.5 ms [physiologist-13]) is about 86% of that phenylephrine PTT response (cross-study derivation). A single stressed morning spot-check can therefore look like vascular drift.
- *Reference misuse: [em_engineer-11].* Its ICC > 0.7 is cited as "suited to personal change detection". The same study reported MAE of 10.1–12.9 mmHg and did not detect mental-stress BP responses. Reliability is not responsiveness. A feature that is stable because it does not move cannot detect change.
- *C6: a constant PRV offset cancels out in a personal baseline.* The 8.50-ms SDNN gap [em_engineer-29] matters for population cut-offs. At night, consumer PPG-HRV reached CCC 0.97–0.99 against ECG [physiologist-25]. For HRV, the recording window (a whole night vs a 2-min spot-check) matters more than the sensor.
- *C15:* a cross-sectional p = 0.024 in a preprint [em_engineer-10] does not show that IPG "sees deeper".

**Questions.** Q1: Which dataset has both ECG and incident-HTN labels to test the kill criterion on lead time? Aurora-BP and PulseDB have no onset labels. Q2: What resting PAT change, net of PEP, do you predict per 10 mmHg of vascular SBP rise, and how does it compare with the day-to-day SD of a 2-min spot-check? Q3: Apart from OSA screening and covering nights when the watch is charging, what does radar add over wrist HR/IBI?

### 1.3 ppg_scientist — TRACE-PPG
**Steelman.** This is deployability backed by evidence. The only regulator-validated hypertension system is PPG-only [PS-1]. Background monitoring runs on PPG, while ECG is on demand [PS-18]. Learned PPG embeddings beat demographics plus HR (AUROC 0.819 vs 0.770 [PS-3]). This corrects my bias toward hand-crafted features.

**Attack.**
- *C11 over-reads [PS-3].* Its labels were self-reported, prevalent "blood pressure" conditions. Dense passive PPG was compared with on-demand ECG, so modality is confounded with sampling density and recording context. If treated participants were included, the embedding may partly learn treatment (a hypothesis). The comparison tests neither untreated *emerging* hypertension nor *change*.
- *Self-contradiction.* C14 [PS-28] reports that SDNN/RMSSD did not predict new-onset hypertension, yet sleep RMSSD/SDNN is a TRACE stream. This also hits my PHY-1 (§4).
- *Morphology transfer is unshown.* The prognostic morphology results come from finger PPG at a single visit ([PS-27]; my [physiologist-4]). No cited study shows that wrist morphology is repeatable night to night.
- *[PS-25] reframed.* The 1.15 alert-days/person were alerts fired by stress, alcohol and travel, i.e. confounders triggering a personal-baseline detector. That is evidence *for* the RQ4 problem, not a benign false-alarm rate.

**Questions.** Q1: In [PS-3], were PPG and ECG matched for recordings per person, and were treated participants excluded? Q2: Which wrist morphology feature has published within-person repeatability? Q3: "≥2 of 3 30-day windows" spans a season. How is seasonal drift separated from a trajectory?

### 1.4 bayesian_ml — BayesTrack-HTN
**Steelman.** This is the best evaluation specification in the debate. It uses event-level lead time, counts abstained cases as misses, rejects point-adjust [bayesian_ml-13], and sets alarm budgets in person-time because specificity decays across windows (92.3% → 86.4% [bayesian_ml-4]). Its admission that nobody has evidence on *lead time at a fixed alarm budget* binds all six of us.

**Attack.**
- *"Rest-equivalent" pools states that are not equivalent.* Daytime stillness (≥5 min, ≥60 min after exercise) mixes posture and mental stress with sleep. Error SD fell 15–20% when restricted to the calibration posture [physiologist-16], and PEP falls 16% under mental stress [physiologist-13]. Sleep and daytime stillness should be separate channels.
- *z̃ (RHR↑, HRV↓, PAT↓) is the generic sympathetic signature.* Alcohol raises nocturnal RHR [physiologist-23]. Infection moves RHR days before symptoms [physiologist-22]. Late-luteal RMSSD falls [physiologist-21]. Stress shortens PAT via PEP [physiologist-13]. NightSignal fired on stress, alcohol and travel [bayesian_ml-1]. Agreement across channels shows that *something* changed, not that the *vascular* system did. Specificity needs a channel that transients move less, e.g. PTT or stiffness at matched HR (my hypothesis).
- *C12* uses between-person All of Us associations as within-person predictors. Within-person evidence exists only for HRV change [physiologist-1] and weight change [physiologist-11].

**Questions.** Q1: What evidence supports 60 minutes as sufficient post-exercise recovery for HRV and PAT? Q2: Which channel separates a winter, a stressful month or an infection from hypertension onset? Q3: Does the hazard model include season or ambient temperature?

### 1.5 device_engineer — BioVance-Edge
**Steelman.** Intended use sets both regulatory class and design. HTN-risk software is MDR Class IIa, vital-danger software is IIb/III, and the WCD is FDA Class III [device_engineer-16, -8]. Radar on the wrist fails the power budget (690–1290 mW active [device_engineer-17]). Locked models with per-user state are the route regulators have cleared [device_engineer-1].

**Attack.**
- *The power budget assumes 25-fps PPG* [device_engineer-18]. That is enough for beat detection. Second-derivative morphology, the PPG feature class with prognostic hypertension evidence [physiologist-4, PS-27], and millisecond-scale PAT both need faster sampling in the windows that matter. The budget should be recomputed for a sleep-morphology window.
- *Spot-check PAT noise is unquantified.* No cited study gives the day-to-day SD of a 30-s seated PAT, so its minimum detectable change is unknown, and a stress-related PEP shift (~15 ms, above) falls inside it.
- *DE-C12/DE-C14 transfer poorly.* The harm from false AF alerts was measured in post-stroke patients aged ≥50 [device_engineer-26]. The Tunisian registry covers *known* hypertensives [device_engineer-32].

**Questions.** Q1: What sampling rate and duty cycle give 0.15–0.3 mA, and what is the figure at a morphology-grade rate during sleep? Q2: If a one-week-battery watch does not charge overnight, when does it charge, and what happens to the nocturnal window? Q3: What result would make you drop the ECG?

## 2. Red-team of the consensus

The strongest case that our shared design is wrong comes from our own reference lists.
1. **Level may beat change.** The only level-vs-trajectory comparison cited is for later CVD, not incident hypertension. Adding the young-adult SBP trajectory to baseline BP raised the C-index by just 0.0084–0.0192 [clinician-23]. The only regulator-validated system classifies 30-day windows with an encoder and a linear head [PS-1], and none of the cited summaries describes a personal baseline. AIRE-HTN is level-based (C 0.70 [physiologist-20]). Pure personal-deviation designs, including NOCTURNE's posterior z-scores, throw away between-person level. Someone already at high-normal BP needs almost no drift to cross the threshold.
2. **The cuff is the real competitor.** All six cards include a sparse or weekly home cuff. All six define `t_ref` with it, and at least two (NOCTURNE, BayesTrack) feed it into the warning. If users take cuff readings anyway, the wearable earns only the lead time *beyond* a cuff-only CUSUM, and nobody proposes that baseline.
3. **Physiology may lag rather than lead.** The prospective markers (PWV RR 1.09 [physiologist-3]; HRV HR 1.58 [physiologist-1]; d/a HR 2.84 [physiologist-4]) are between-person associations from a baseline measurement followed for years. They fit equally well a model in which high-normal BP drives both the marker and the later diagnosis. No paper here shows a wearable signal changing *within* a person before that person's cuff BP changes.
4. **Against rejecting F2.** The rejection rests on base rates in unselected populations [clinician-31]. In referred cohorts, near-term ventricular-arrhythmia prediction reached an external AUROC of 0.948 [physiologist-28], and one case shows a 4–6-month wearable prodrome before SCD [bayesian_ml-6]. F2 fails *this challenge's* scoring, not science.

**Falsifiers.** Hold the alarm budget equal and use forward-chained splits. The consensus is wrong if either (a) a level-only model (frozen encoder plus a linear head on the same features) or (b) a cuff-only CUSUM matches the full personal-change model on Se(90 d) and warning precision. Both tests are cheap, and all six prototypes should run them as mandatory ablations.

## 3. Positions on D1–D6

- **D1 Sensors.** Choose the measurement windows first, then the sensors. Core: wrist PPG, IMU and skin temperature, read in the main-sleep window, plus a weekly cuff. ECG is optional, justified by (a) a rhythm gate and (b) PAT at a fixed morning posture. Its net value over PPG is unproven and confounded by PEP (§1.2). My round-1 card listed ECG as core; I now demote it.
- **D2 Radar.** Partly revised. Radar is no closer than PPG to the *vascular* mechanism: radar PTT needed cascade hardware, static subjects and per-subject calibration [em_engineer-7]. But radar's OSA evidence is better than that for the wrist-SpO2 route I assumed: AHI ICC 0.965 with oximetry (N = 200 [em_engineer-39]); 85%/88% without SpO2 (N = 141 [device_engineer-29]). OSA affects 40–80% of hypertensives [physiologist-9]. Radar belongs in phase 2, at the bedside, for the sleep-breathing axis and for charging nights, and never for BP.
- **D3 F3.** Treat it as a rhythm *gate*, not an alarm stream. Irregular-rhythm windows are excluded from HRV/PAT and count against data quality (RQ5). Rhythm findings get a separate "see a clinician" message outside the hypertension alarm budget, with no MI/SCA claim. This keeps F3's safety value without diluting E3.
- **D4 Formulation.** Change detection generates the evidence, and a landmark hazard calibrates it [bayesian_ml], plus a population level term (§2). Persistence rules should follow the timescales of confounders, so they must span at least one menstrual cycle [physiologist-21]. No k-of-n rule excludes season, which acts over months (+0.61 mmHg per 1 °C fall [physiologist-24]), so temperature and season must be modelled explicitly. Report 4-of-6 weeks and 2-of-3 months as a sensitivity analysis.
- **D5 Reference.** Adopt the clinician's `t_ref`: ESC home ≥135/85 or 24-h ≥130/80 as primary, AHA ≥130/80 as sensitivity, first of two consecutive. Report Se at ≥90 and ≥180 days, together with the calendar months of warnings and of `t_ref`. Autumn physiology "predicting" a winter crossing would be spurious lead time.
- **D6 Data.** If the data are PPG-derived features only, no EM component can be tested. EM then enters through modality-dropout design (RQ5) and an external Aurora-BP ablation (24-h ECG+PPG+ABP [physiologist-16]). That ablation tests posture/PEP effects over a day, not lead time. Likewise, my night-vs-all-day ablation needs sleep-period aggregates or sub-daily timestamps. With daily aggregates it cannot be tested, and the paper must say so.

## 4. Concessions

1. **PHY-1 downgraded from STRONG to MODERATE.** HELIUS found no association between SDNN/RMSSD and new-onset hypertension over 6.6 y, whereas baroreflex sensitivity was associated (OR 1.31 [PS-28]). The positive evidence comes from 10-s ECGs [physiologist-1] and ELSA-Brasil [clinician-24]. HRV stays in the model, interpreted jointly with RHR.
2. **Withdrawn:** "the persistence window exceeds every known transient". Season acts over months, and changes in weight or activity are real risk drivers, not transients.
3. **PHY-4 downgraded to WEAK for wearables.** The evidence is finger PPG at a check-up in 902 men.
4. **PHY-9 remains a hypothesis.** It rests on N = 13. Removing night data cost only about 5% F1 in [bayesian_ml-19] (PREPRINT), so my night-vs-all-day ablation has to show that night is better.
5. **Weakened: "≥2 agreeing axes point to physiology".** Confounders are multimodal (§1.4 applies to me too). Specificity must come from context, timescale and HR-adjusted vascular timing.
6. **Revised: personal-only deviation.** A population level term is added, because round-1 NOCTURNE would miss people already at high-normal BP.
7. **Promoted: learned representations.** A frozen PPG encoder score [PS-1, PS-3] becomes a first-class level input rather than an "optional axis".
8. **PHY-13 recomputed:** PPV about 10.6% internal and about 10.0% external (my derivation). The conclusion is unchanged.

## 5. Updated position — NOCTURNE v2

NOCTURNE v2 is a night-anchored, context-normalised change engine **plus** a population level term. It runs cuff-only and level-only baselines as mandatory falsifiers. It merges:
- BayesTrack's quality-weighted Student-t local-level model and its event-level metrics;
- the clinician's `t_ref` and lead-time reporting;
- TRACE-PPG's frozen encoder score, two-tier SQI and skin-tone-linked MNAR test;
- EM-ANCHOR's kill criterion and a rhythm channel, used as a gate;
- BioVance-Edge's locked-model route and failure budgets (1,863/2,229 with enough data [device_engineer-1]; 77.4% wear-time [device_engineer-25]).

My distinctive bets remain: sleep and daytime as separate channels, HR-adjusted vascular timing as the specificity channel, explicit modelling of season, and the night-vs-all-day ablation as my own falsifier.

## References

Round-1 references are cited by their IDs (see `round1/*.md`). New references (numbering continues from round 1):

*(No new references: this critique cites round-1 references by ID. The optional verification lookups were interrupted by a usage limit.)*

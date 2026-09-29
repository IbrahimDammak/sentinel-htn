# Round 3 — Defence and final position: THE EM ENGINEER (EM-ANCHOR v3)

I championed the user's idea as far as evidence allowed. Most of what follows is concession. IDs are as in earlier rounds; no new research.

## 1. Rebuttal

**clinician: "C8 treats repeatability as validity."** Conceded. The ICC above 0.7 in [em_engineer-11] sits beside a calibrated MAE of 10.1–12.9 mmHg and missed mental-stress responses, and the audit says the same: reliability is not responsiveness. "PAT is suited to change detection" is withdrawn. The r of -0.82 [em_engineer-25] came from exercise-induced swings, where PEP moves, and the PAT–DBP sign flipped by exercise type.

**clinician / bayesian_ml: "The kill criterion cannot be run for lead time."** Conceded, and Bayes' arithmetic hurts: about 85 converters with dense pre-onset ECG are needed to detect Se(90 d) 40% to 55%. No dataset named in round 1 has them. So the kill criterion is redefined as a *feasibility and coverage* test in a pilot (valid spot-check completion, PAT day-to-day SD and MDC, coverage by skin-tone group), not a lead-time test. Any lead-time claim for EM goes to future work.

**clinician: "Why PAT over a validated cuff?" and "What action follows a PVC flag?"** No good answer for either, so I drop both. PVC burden was validated on a 3-day continuous patch [em_engineer-21], not on 2 x 2 min a day, and 4 minutes is 0.28% of the day (device_engineer's arithmetic). PVC burden leaves the card. The only surviving rhythm output is an AF/irregularity gate plus a persistence-gated "see a clinician" flag.

**clinician / device_engineer / ppg_scientist: "C9 does not transfer to F3" was my point, but the 9.5 false flags per person-year stands against my round-1 design.** Agreed that unguarded 98.7% specificity times 730 checks a year gives about 9.5 flags. Two consecutive positives gives about 0.12 (lower bound, independence assumed). Because the flag sits outside the alarm budget, the clinician's concern shifts to cost and class, which the device engineer answers below.

**ppg_scientist: "C7 is labelled STRONG but rests on PWV."** Conceded: RR 1.09 with considerable heterogeneity, and PWV is not wrist PAT. It is MODERATE and is not evidence for PAT.

**ppg_scientist / physiologist / bayesian_ml: agreement double-counted (PEP is sympathetic).** Accepted. PAT, nocturnal HR and ECG-HRV share sympathetic drive, so the "≥2 modalities agree" rule can count one cause twice. I adopt Bayes' joint state-space posterior in place of axis counting. Without ICG or SCG I cannot separate PEP-driven from vascular PAT change. This is a blind spot shared with device_engineer, and the pilot needs an SCG or ICG reference.

**ppg_scientist: minimum detectable change; three-arm ablation.** Adopted: passive PPG, PPG spot-check in the same seated ritual, PPG plus ECG spot-check. ECG survives only if arm 3 beats arm 2 by a pre-set margin. I cannot give PAT's MDC from cited work. It is the first pilot output.

**physiologist: radar and axis 3 (OSA).** Partly defended. Radar has the better direct evidence for the breathing axis: AHI ICC 0.965 with oximetry (N=200) [em_engineer-39] and 85%/88% without SpO2 (N=141) [device_engineer-29]. But ppg_scientist shows wrist accelerometer and SpO2 features are already FDA-authorised [PS-32, PS-33] (K240929 sens 66.3%/spec 98.5%; Samsung 82.7%/87.7%, whose specificity missed its own acceptance criterion). Radar is therefore a **pilot-only bedside logger**, killed if the wrist covers at least 80% of nights and radar adds nothing to OSA context. It is not a product component.

**physiologist / bayesian_ml: the night window rests on N=13; "IPG sees deeper" is a p=0.024 preprint.** Both conceded. Neither is used as a design premise. Radar HR within 10% is about 6 bpm at 60 bpm, coarser than drift and not usable as a pulse channel.

**bayesian_ml: no level-only comparator; ECG as "key channel" turns missed checks into misses.** Both fixed. A level-only model is mandatory. ECG is never a key channel: POOR-QUALITY may not fire on a missing EM channel, and spot-check missingness is modelled as MNAR.

**device_engineer: rhythm flag class; radar in the pilot.** I keep the AF function as a separately cleared on-demand ECG feature (a 510(k) [PS-18], not a PMA like the WCD [device_engineer-8]). Whether a bundled second function stays Class II is a regulatory question I cannot answer from the corpus, so I state it as open.

## 2. Audit response

- **Struck:** the parenthetical "PEP/PTT separation via radar/SCG/ICG fiducials [36]". Ref 36 used carotid ultrasound (10.1 to 4.2 mmHg used central PWV, not a wearable; peripheral PWV gave 7.1).
- **Downgraded STRONG to MODERATE:** C1 ([16] single cohort), C4 ([19]: 67.23% sensitivity is from a simulated arterial-occlusion model, so add "in a simulated arrest model"), C7, C9, and C11 (sponsor data; [33] adds nothing independent).
- **Withdrawn:** "suited to change detection" ([11]); "sympathetic confounding rebutted" ([24]: phenylephrine only, not stress or exercise).
- **Restated:** radar HR/RR is "moderate, heterogeneous" (48% and 37% of studies within 5%) [2]; [10] Thomson N=261 is not "tiny"; AF evidence via [21] is dropped (PVC only); vendor AFE is "designed to meet IEC 60601-2-47", not "standards-grade"; radar sleep staging is "radar plus oximetry, 3-class" [39]; HTNF sensitivity is quoted on 1,863 analysable, not 2,229 enrolled; K250507 date is 11 Sep 2025.
- **Orphans:** ref 4 is deleted.

## 3. PROTOTYPE CARD (v3), EM-ANCHOR

- **Target:** HTN-trajectory engine (primary) with an optional EM tier; no MI/SCA claim.
- **Challenge submission:** BayesTrack-style quality-weighted state-space engine on PPG-derived features, modality-optional (RQ5 by dropout); level-only comparator mandatory.
- **EM tier (pilot, kill criteria):** 30–60 s seated ECG spot-check (PAT plus rhythm gate) via MAX86176 and nRF52840; bedside 60 GHz radar as a logger only.
- **Output:** three states, never mmHg; rhythm finding routed separately.
- **Pre-registered:** PAT MDC, spot-check adherence at week 4 and month 6, ITA-stratified valid-day coverage, and a power analysis (about 85 converters) for any future EM claim.
- **Risk:** the EM tier adds nothing measurable on the challenge data. That outcome is reported as a negative result.

## 4. Final ranking (Ev = evidence strength, Eng = real-world engineerability, Stu = student buildability, 4–8 weeks)

| Option | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 | RQ6 | Ev | Eng | Stu | Justification |
|---|---|---|---|---|---|---|---|---|---|---|
| CONFIRM-HTN | 5 | 6 | 7 | 5 | 5 | 6 | 6 | 7 | 8 | Best labelling and action logic; thin model. |
| EM-ANCHOR (mine) | 6 | 6 | 5 | 6 | 7 | 6 | 3 | 5 | 4 | Modality-optional RQ5 design helps, but EM cannot score on likely data; I mark Ev low myself. |
| TRACE-PPG | 7 | 6 | 6 | 6 | 8 | 6 | 7 | 8 | 8 | Most testable and deployable; ignores fairness fallback for dark skin. |
| NOCTURNE | 7 | 8 | 6 | 8 | 6 | 6 | 5 | 6 | 6 | Best context handling. |
| BayesTrack-HTN | 8 | 8 | 7 | 6 | 8 | 9 | 6 | 6 | 5 | Best container for optional channels and best metrics. |
| BioVance-Edge | 5 | 5 | 6 | 5 | 7 | 6 | 5 | 8 | 4 | Realistic BOM and class; hardware eats student time. |
| F2 as stated | 2 | 2 | 1 | 2 | 3 | 3 | 3 | 2 | 2 | Legitimate science in referred groups (AUROC 0.948 near-term VA), off-target here. |

## 5. Recommendation

- Submit a PPG+IMU, software-only engine; EM is not scored on likely data.
- Make every channel optional and report modality-dropout curves (RQ5).
- Treat ECG spot-check and radar as pilot experiments with pre-registered MDC, adherence and coverage kill criteria.
- Adopt the joint state-space posterior so correlated sympathetic channels are not double-counted.
- Run the three-arm ablation (PPG, PPG ritual, PPG+ECG).
- Keep AF/irregularity as a gate and a separate flag; drop PVC burden.
- Add an SCG or ICG reference in the pilot to test PEP against vascular PAT.
- State honestly that no EM lead-time claim is possible within the challenge.

**Verdict on the user's idea.** EM signals for sudden or premature cardiac attack cannot be the deliverable here. The challenge scores personalised, longitudinal hypertension warning, and the acute target fails on base rate (PPV about 0.1% daily in unselected people) and on regulation (MDR IIb/III; WCD is Class III). Two parts survive: EM as an optional sensing tier with kill criteria, and the personal-baseline-to-change architecture as the right future frame for F2 read as risk drift, validated on hypertension first.

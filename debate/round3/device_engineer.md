# Round 3 — Defence and final position: THE DEVICE ENGINEER (BioVance-Edge v3)

`[device_engineer-n]` are my references; `[PS-n]` = ppg_scientist. Power and BOM figures are my own estimates unless a reference is given. No new research this round.

## 1. Rebuttal

**clinician / em_engineer / physiologist: "Spot-check PAT contradicts DE-C7; PEP confound; noise unquantified."** Conceded. I rejected cuffless-then-threshold because calibrated PTT under-tracks change (1.8 of 7.4 mmHg over 24 h, N=166 [device_engineer-14]), yet my core EM feature was PAT, which has the same responsiveness problem plus PEP: mental stress alone shortens PEP by about 14.5 ms, 0.7–4.3 times the PAT signal of a 10 mmHg SBP shift (my arithmetic from [em_engineer-24] slopes and [physiologist-13]). Aurora tested PAT features directly with no gain [PS-8]. PAT leaves my core and becomes a pre-registered ablation. No cited study gives the day-to-day SD of a 30-s seated PAT, so I cannot state a minimum detectable change. I withdrew "best ratio" for the ECG spot-check in round 2.

**clinician / physiologist: "What evidence shows raw PAT tracks drift over months? What spot-check completion at 6 months? What does ECG add on organiser data?"** None, none, and probably nothing. Four-week adherence in motivated AF patients was 83.3% median (only 16 of 27 full-protocol days) and 75.0% missing no day [PS-30, PS-31]. Months-long adherence in asymptomatic users is unevidenced; wear-time was already 77.4% at 12 months (273/298 = 91.6% of people had some, SD 32.6 shows wide spread) [device_engineer-25]. Missed checks are MNAR; the least engaged users drift into permanent abstention, and evaluation counts abstention as a miss. If organisers ship no ECG, the ECG adds nothing to the score. I give the answer the physiologist asked for: **drop the ECG if arm 3 does not beat arm 2 in the three-arm ablation, or if week-4 adherence falls below the pre-registered floor** (I propose 60%, my number, unevidenced).

**clinician: "The radar precedent is misapplied."** Yes. C200 (K234003, 30 May 2024) and C300 (K252676, 3 Feb 2026) are clinical-setting HR/RR monitors, not home devices. The audit says my "every cleared radar monitor" is universal; I restrict it to those three named devices. Their database pages show no indication limits, and C300's product code reads "cardiac monitor including rate alarm", so "no alarms" is unconfirmed.

**em_engineer: "Deferring radar gives up the only test of zero-wear coverage; what about a pilot logger?"** Reversed in part. My round-2 build plan dropped radar. Given the 16% of HTNF enrollees who lacked ≥15 usable days [device_engineer-1], a bedside radar as a **pilot logger outside the product** is acceptable as an OSA and coverage experiment, not as a product part. Radar at 690–1290 mW [device_engineer-17] still fails a wearable (150 mAh lasts about 26–49 minutes at 3.7 V, my arithmetic, checked by Auditor C).

**em_engineer / ppg_scientist: "Does a rhythm flag stay Class II? A software-only MVP needs no hardware."** Two functions cleared separately (HTN notification K250507; on-demand ECG/AF [PS-18], a 510(k)) is plausible, but whether the bundle stays Class II is unresolved and the corpus cannot settle it. The audit corrects my claim that K250507 is "the one precedent" for locked models: it shows one PCCP that excluded continuous learning. PPG-scientist's point stands: hardware is justified only by an RQ metric that moves, and none is predicted. So the challenge submission is software-only, and the hardware plan is a v2 product path.

**ppg_scientist / device_engineer self-test: which raw-PPG platform?** Open question I raised against TRACE-PPG applies to me too: morphology, PaPaGei and my ECG/PPG synchronisation need raw signal. I have no verified answer for a commodity watch SDK, sampling rate or licence.

**physiologist: power budget at 25 fps; morphology and PAT need faster sampling; charging conflict.** Conceded. Recompute for a sleep burst before claiming a week. The audit found a further inconsistency: 47.65 mJ per inference [device_engineer-20] at one a minute is about 215 µA, which alone exceeds the 50–100 µA MCU line and doubles the total (151–301 µA). Fix: state the inference rate. At one inference per 15 minutes it is about 14 µA (fine), or use the 1.79 mJ model. A one-week battery that charges daily deletes the night window. My ≥1-week claim is an unmeasured estimate, and darker skin or higher BMI (LED drive) is my inferred failure point.

**physiologist / bayesian_ml: DE-C12/DE-C14 transfer poorly; wear-time removal is MNAR.** Agreed. The false-AF-alert dose-response was in post-stroke/TIA patients ≥50 y over 14 days [device_engineer-26]; the Tunisian registry covers known hypertensives [device_engineer-32]. Both are analogies, WEAK. Wear-time loss likely clusters in illness and travel, so stress tests need MNAR.

**bayesian_ml: "Fixed warning precision does not transport; no cuff-only baseline in the ablations."** Both accepted. The constraint is false alarms per non-converter person-year, which is prevalence-free. Cuff-only and cross-sectional nulls are mandatory (my own R1/R3 already demand them).

## 2. Audit response

- **DE-C2, DE-C8, DE-C11:** STRONG to MODERATE (C2: loss-of-pulse sensitivity is from simulated pulselessness; C8: ref 10 uncited and ref 12 is a garbled WEAK abstract; C11: one PCCP).
- **L153:** "the one PCCP reviewed excluded continuous learning."
- **L23:** restricted to the three named radar devices.
- **Ref 14 (Derendinger):** "over 24 h"; my "would hide exactly the drift" is an extrapolation from a 24-h surrogate to weeks–months, one device.
- **Ref 22 (SQI 95.6%):** headband PPG, 54 people, 80/20 epoch split with no subject-wise split: likely leakage. Use as WEAK.
- **Ref 24:** naive FL loses 13.87 points and takes about 70x longer, but the same abstract proposes H-FedSL restoring 98.81% (simulation).
- **L161:** "fell" compares different populations; withdrawn.
- **Ref 2:** "the only cleared consumer SCA detector" is unverifiable; removed. Sensitivity 69.3% (n=135) is in simulated pulselessness.
- **BOM:** only the AFE is sourced ($14.36 x1, $9.87 at 2,500). "$35–60 at 1k" is an unsourced estimate; no line items sum to it.
- **Cleanup:** uncited refs 7, 10, 32 deleted. Ref 18 "designed to meet IEC 60601-2-47", not certified. Ref 20 omits that the smallest model has an MAE of about 8 BPM.

## 3. PROTOTYPE CARD (v3), BioVance-Edge

- **Challenge submission:** software-only PPG+IMU notifier on the merged engine (TRACE SQI, NOCTURNE windows plus seasonal covariate, BayesTrack model and harness, CONFIRM dual t_ref).
- **Hybrid core:** population level classifier sets the prior; personal change is layered and the ablation sizes it.
- **Output:** three states, no STABLE, never mmHg; a warning triggers cuff *surveillance*, not one-shot confirmation.
- **Real device (v2 path):** wrist PPG+IMU plus ECG electrodes (MAX86176 <11 µA in PPG/ECG mode; nRF52840) as a rhythm/quality gate only; optional seated PAT for the ablation; no radar in product.
- **Power:** 0.15–0.30 mA (151–301 µA sum), 41.7 to 20.8 days at 150 mAh nominal; unmeasured; inference rate to be stated; morphology-burst recompute pending.
- **Regulatory:** intended use is HTN risk notification (MDR IIa); no acute language; locked model with per-user state; features-only upload.

## 4. Final ranking

| Option | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 | RQ6 | Ev | Eng | Stu | Justification |
|---|---|---|---|---|---|---|---|---|---|---|
| CONFIRM-HTN | 5 | 6 | 7 | 5 | 5 | 6 | 6 | 7 | 8 | Cleanest intended use and label logic. |
| EM-ANCHOR | 6 | 6 | 5 | 6 | 7 | 6 | 3 | 4 | 4 | Two extra modalities with no scoring path and a class-jump risk. |
| TRACE-PPG | 7 | 6 | 6 | 6 | 8 | 6 | 7 | 8 | 8 | Fits the only precedent and the likely data. |
| NOCTURNE | 7 | 8 | 6 | 8 | 6 | 6 | 5 | 5 | 6 | Night window collides with charging and sampling power. |
| BayesTrack-HTN | 8 | 8 | 7 | 6 | 8 | 8 | 6 | 6 | 5 | Best evaluation; edge-implementable if features are simple. |
| BioVance-Edge (mine) | 5 | 5 | 6 | 5 | 7 | 6 | 5 | 8 | 3 | Best failure and regulatory budgeting; I score my own student buildability lowest because hardware is not 4–8 weeks. |
| F2 as stated | 2 | 2 | 1 | 2 | 3 | 2 | 3 | 1 | 2 | Class IIb/III at best (WCD is Class III via PMA); no evidence base for a wearable EM detector. |

## 5. Recommendation

- Submit software-only; treat hardware as a follow-on product path.
- Locked model with per-user state; features-only upload; edge SQI.
- Report false alarms per non-converter person-year and wear-time/MNAR failure budgets.
- Cuff-only and cross-sectional nulls are mandatory.
- Post-warning cuff surveillance, not confirmation.
- ECG stays a rhythm/quality gate; drop it if week-4 adherence or the ablation fails.
- No radar in the product; bedside radar only in a pilot.
- Measure real power before claiming a week.

**Verdict on the user's idea.** "EM signals for sudden or premature cardiac attack" implies acute monitoring, which raises the regulatory class (MDR IIb/III; the closest cleared arrest device, the WCD, is Class III via PMA), and the only consumer analogue, Fitbit loss-of-pulse, needed a 99.965% day-level specificity and gated calls to reach about one false call per 75 person-years. The challenge scores hypertension, so F2 earns nothing. Reframed as an ECG-gated front end in a hypertension engine, the idea is buildable and honest.

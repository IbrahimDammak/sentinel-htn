# Round 2 — Cross-critique: THE EM ENGINEER (`em_engineer`)

*I champion the user's idea as far as the evidence allows. Round-1 references keep their IDs ([PS-n] = ppg_scientist-n). Claim IDs are the authors' own (clinician C9, PHY-12, DE-C3 …). New references continue from [em_engineer-46]. "My arithmetic" marks numbers I derived from cited inputs.*

## 0 Bottom line

- The consensus is right to score F1. It has two problems: it **assumes trajectory beats level** without in-domain evidence, and it **runs on a PPG monoculture** whose data loss is linked to skin tone.
- **F2 survives only in a scoped form:** a user-initiated ECG rhythm channel. It serves first as a data-quality gate for the trajectory engine and second as a persistence-gated "see a clinician" flag. It makes no claim to predict MI or SCA.
- I **withdraw** PAT as a BP tracker and radar as a pulse sensor. Both remain as ablation arms with kill criteria.

## 1 Critiques of the other five

### 1.1 clinician — CONFIRM-HTN

**Steelman.** C9 is decisive. At 36.8–39.7 SCD per 100,000 per year [clinician-31], a daily imminent-arrest predictor has a PPV of about 0.1% even at 99.9% specificity. The out-of-office t_ref (C1–C2) and the rule never to output mmHg (C4–C5) should bind every team.

**Attack.**
- *C9 does not transfer to F3.* Rhythm detection has a different base rate: a wearable irregular-rhythm alert had 98.2% PPV for concurrent AF [clinician-34], and on-demand ECG classifies AF at 96.0% sensitivity and 98.7% specificity [PS-18]. Without C9, "F3 dilutes" comes down to page budget and alarm burden, and both can be fixed (D3).
- *Sleep PAT cannot be built as specified.* The card lists "HRV, PAT at rest/sleep" from a watch or patch ECG. Watch ECG is on demand only and background sensing is PPG [PS-18]. The patch's wear time is not specified.
- *C11 is overstated.* The HR of 3.91 in [clinician-23] concerns later CVD, not incident HTN. The same abstract shows the trajectory adds only 0.0084–0.0192 to the C-index over baseline BP. C11 also omits HELIUS, where SDNN and RMSSD did not predict new-onset HTN [PS-28].

**Questions.** (1) Which device records ECG during sleep, and at what adherence? (2) If the rhythm flag is persistence-gated (about 0.12 false flags per person-year, see D3), does "F3 dilutes" still hold, and what budget would you accept? (3) Given [clinician-23], what gain over a level-only model would justify a trajectory engine?

### 1.2 ppg_scientist — TRACE-PPG

**Steelman.** This is the most deployable paper.
- PPG is already the background sensor [PS-18].
- A PPG-only self-supervised encoder with a linear head is FDA-cleared [PS-1].
- All of Us (482 incident HTN, EHR-linked) [PS-26] is the only lead-time dataset anyone named.
- It correctly reframes the skin-tone issue from bias to **missingness** [PS-22].

**Attack.**
- *C11 ("no measurable gain from ECG") misreads [PS-3].*
  - That study compared ECG embeddings *instead of* PPG (0.769 vs 0.819) for self-reported *prevalent* high BP. That tests substitution, not addition; there is no PPG+ECG arm and no PAT arm.
  - For *incident* HTN, a 12-lead AI-ECG reached C 0.70, with NRI 0.32–0.44 over clinical factors [physiologist-20].
  - The fair reading: single-lead ECG morphology adds little to prevalent detection (0.769 vs 0.770 for demographics plus HR). ECG *timing* added to PPG has not been tested.
- *C4 is applied to ECG only.* Aurora's failed models also included "PPG alone" [bayesian_ml-23]. The device that missed a 19.7 mmHg drug-induced fall was optical [PS-10]. No wrist modality has shown within-person tracking, so the evidence does not separate PPG from PAT.
- *C7 is contradicted inside the corpus.* A 14-day single-lead patch ECG predicted near-term sustained VA with AUROC 0.957 internally and 0.948 externally [physiologist-28]. That is wearable EM prediction, albeit in a referred population, and it is stronger than accelerometry's 0.74 [PS-19].
- *Fairness hole.* POOR-QUALITY leads to abstention, and abstention counts as a miss. Skin-tone-linked missingness therefore becomes skin-tone-linked sensitivity loss: participants with ITA° <10° were 36% of the sample but accounted for 50–85% of missing data [PS-22]. TRACE-PPG reports this gap but has no fallback.

**Questions.** (1) Does [PS-3] contain any fusion or PAT arm? If not, will you restate C11 as "ECG alone ≤ PPG alone"? (2) What coverage and sensitivity do you expect by ITA group, and what would restore them? (3) Will you run PPG vs PPG+PAT on Aurora-BP [PS-9] for *change* tracking, for example the awake-to-asleep dip?

### 1.3 physiologist — NOCTURNE

**Steelman.** Timescale separation is the best RQ2/RQ4 idea in the debate: an alert must outlast the effects of alcohol [physiologist-23], infection [physiologist-22] and the menstrual cycle [physiologist-21]. The PEP data (−16% under mental stress, halved under exercise [physiologist-13]) are the right reason to read PAT only at matched state.

**Attack.**
- *PHY-12/D2 argues the wrong mechanism.* I concede that radar is no better than PPG for the *pulse*. But NOCTURNE's axis 3 (sleep–breathing; OSA is present in 40–80% of hypertensives [physiologist-9]) relies on wrist SpO2 dips, which §7 admits were not researched. Radar measures breathing directly:
  - AHI ICC 0.965 vs PSG, N=200, radar with oximetry [em_engineer-39];
  - AHI r 0.87 and sensitivity/specificity 85%/88% *without* SpO2, N=141 [device_engineer-29].

  For that axis, radar is the better-evidenced sensor.
- *"Vascular drift = ↓PTT at matched HR" cannot be computed from a wrist.* Single-site PPG gives PAT, not PTT, and matching HR does not remove PEP: at rest, HR explained 6% of PEP variance (R² 0.06) [physiologist-13]. Sympathetic and vascular drift are therefore confounded unless an EM corrector is added (ICG, or ECG plus mechanical aortic-opening timing). That is the hardware NOCTURNE deferred.
- *The night window rests on 13 people.* The claim that PRV ≈ HRV at night comes from N=13 [physiologist-25]. The physiologist's own meta-analysis reference says the agreement is "not generalisable to sleep" [physiologist-26].

**Questions.** (1) Without ICG, how do you separate sympathetic from vascular drift? (2) What evidence favours wrist SpO2 over a bedside radar for axis 3? (3) Will the pilot carry an ECG-grade nocturnal reference?

### 1.4 bayesian_ml — BayesTrack-HTN

**Steelman.** This is the best evaluation protocol:
- abstention counts as a miss;
- lead time is measured from a sustained WARN;
- alarm budgets are set per person-time (specificity 92.3% for one window but 86.4% over six [bayesian_ml-4]);
- no point-adjust [bayesian_ml-13];
- synthetic onsets;
- leave-one-channel-out ablation (A8).

The q-weighted state-space model is the right container for optional EM channels, and I adopt it.

**Attack.**
- C13 ("wearable SCD prediction rests on single-case evidence") ignores [physiologist-28] and [PS-19].
- The case for slopes rests on an analogy from prostate cancer (PSA, AUC 0.743→0.800 [bayesian_ml-29]). The in-domain test gave only +0.008–0.019 C-index [clinician-23].
- The ablation ladder starts at A0, a "population threshold". No arm tests a full-feature **cross-sectional** model, which is the strongest non-trajectory rival and the kind of model that was cleared [PS-1].
- POOR-QUALITY fires when "a key channel [is] missing". If ECG is a key channel, missed spot-checks silently become misses; wear-time was 77.4% even with engagement support [device_engineer-25].

**Questions.** (1) Will you pre-register A8's minimal effect (ΔSe at 90 days at a fixed rate of false alarms per person-year), and is it detectable with the likely event count? (2) Is ECG a key channel, and how is MNAR spot-check missingness modelled? (3) Will you add a level-only comparator?

### 1.5 device_engineer — BioVance-Edge

**Steelman.** This is the most engineerable paper, and it independently arrives at my hardware: a MAX86176 at $14.36 [device_engineer-18] plus an nRF52840. It settles four questions:
- wearable radar fails on power (690–1290 mW active [device_engineer-17]);
- acute monitoring moves the device up a class under MDR Rule 11 [device_engineer-16];
- cleared radar devices measure HR/RR only, without alarms [device_engineer-4, -5, -6];
- models must be locked, with per-user state [device_engineer-1].

**Attack.**
- *We share a blind spot.* "Spot-check PAT = standardised rest context" ignores two facts: mental stress alone shortens PEP by 16%, and HR barely predicts PEP at rest [physiologist-13]. Neither of our cards measures PEP, so the pilot needs an ICG or SCG reference.
- *Deferring radar to "phase 2" gives up the only test* of whether a zero-wear sensor recovers lost coverage. 16.4% of HTNF enrolees lacked ≥15 usable days [device_engineer-1].
- *DE-C3 is right for F2 but does not cover a scoped rhythm function.* User-initiated ECG AF classification was cleared through a 510(k) [PS-18], not a PMA like the WCD [device_engineer-8].

**Questions.** (1) What spot-check adherence at week 4 would kill PAT? (2) Would you add radar to the *pilot* as a coverage and OSA logger, outside the product? (3) Do two separately cleared functions keep the rhythm flag at Class II? These would be the HTN notification [device_engineer-1] and an on-demand ECG [PS-18].

## 2 Red-teaming the consensus

1. **"Trajectory beats level" is assumed, not shown.**
   - The only cleared system is level-based [PS-1].
   - Cuff trajectories added only 0.008–0.019 C-index [clinician-23].
   - The HRV evidence conflicts ([physiologist-1] and [em_engineer-28] vs [PS-28]).
   - Single-axis HRs are 1.06–1.6 [physiologist-2, -7, -8].

   *Falsifier:* on forward-chained splits, a cross-sectional model with identical features at each landmark matches the trajectory engine's sensitivity at ≥90 days' lead for the same number of false alarms per person-year. If that happens, Learn→Detect→Predict is decoration.
2. **A PPG monoculture means unequal coverage.**
   - All six backbones are wrist PPG.
   - Missing data concentrate in dark skin [PS-22], and abstention counts as a miss.
   - Deployment in Tunisia and Africa (R6) makes this worse.

   A non-optical fallback (ECG spot-check, bedside radar) is one way to *restore* coverage. This is a hypothesis: I retrieved no evidence that these modalities are independent of pigmentation in practice. *Falsifier:* pilot valid-days per 30 show no gradient across ITA groups.
3. **F2 was rejected too broadly.** Base rates rule out imminent-arrest prediction in unselected people [clinician-31]. They do not rule out rhythm detection or VA risk in referred populations.
   - Single-lead patch ECG predicts near-term VA (external AUROC 0.948). Its PPV of about 10% (physiologist's derivation) is above the 3% appropriate-intervention rate at which WCDs are prescribed [PS-20]. This is a cross-study inference with different populations and windows.
   - A case report found HRV halved 4–6 months before SCD [bayesian_ml-6] (n=1).

   **What survives of F2:**
   - (a) a rhythm *gate* that removes AF- or ectopy-contaminated windows from the HRV and morphology streams (RQ4/RQ5);
   - (b) a persistence-gated "rhythm finding — see a clinician" flag;
   - (c) the recognition that the consensus engine (personal baseline → change) is the right *future* architecture for F2 read as risk drift, validated first on HTN.

   *Falsifier for (a):* if gating changes neither false alarms nor drift estimates in the pilot, drop F3.

## 3 Positions on D1–D6

| | Position |
|---|---|
| D1 | PPG+IMU is the backbone (conceded). A 30–60 s ECG spot-check (seated, IMU-still) is optional and supplies PAT at matched state plus the rhythm gate. Rest standardisation does not solve PEP [physiologist-13], so ΔPAT counts only if it persists and a second axis agrees. Value for trajectories: *no evidence* either way. For absolute BP: *evidence against* [PS-8, em_engineer-11]. |
| D2 | Not for pulse or BP (conceded). Yes as a pilot-only bedside logger for the sleep–breathing axis [em_engineer-39, device_engineer-29] and for coverage without wear. Kill it if the wrist covers ≥80% of nights and radar adds nothing to OSA context. |
| D3 | Use F3 as an input plus a gated flag, with one sentence in the paper. Unguarded, 98.7% specificity [PS-18] × 730 spot-checks per year ≈ 9.5 false flags per person-year. Requiring 2 consecutive positives gives ≈ 0.12 (my arithmetic, assuming independent errors, so a lower bound). |
| D4 | Change detection first (CUSUM on rest residuals), then a landmark hazard; a level-only comparator is mandatory. "Warning" needs ≥4 of 6 weeks, which outlasts cycle-linked shifts, with a faster "Watch" tier. Tune k-of-n under an alarm budget per person-year. |
| D5 | The reference is cuff-confirmed out-of-office BP. Use the organiser label first, otherwise an HBPM mean ≥130/80 as in [PS-1], with ESC ≥135/85 as a sensitivity analysis. Report Se at 0/30/90/180 days. The ≥90-day target is the clinician's inference, and I accept it. |
| D6 | With PPG-only features, EM can be tested only as: (i) a modality-optional design (RQ5); (ii) an external PPG vs PPG+PAT ablation on Aurora-BP [PS-9]; (iii) PulseDB pipeline tests [em_engineer-37]. Radar and the rhythm gate go to the pilot or future work. |

## 4 Concessions

1. **Withdrawn:** my C8 used the within-person PAT–SBP r of −0.82 [em_engineer-25] as tracking evidence. That value came from exercise, where PEP co-varies. Under phenylephrine, PEP moved the other way (+5.5 ms) [em_engineer-24], and PAT-family devices failed to track change [PS-11, em_engineer-11].
2. **Weakened:** C6. The 8.50 ms SDNN gap comes from a clinical population [em_engineer-29]. Pooled errors at rest are small [em_engineer-30], and good devices reach CCC 0.97–0.99 at night [physiologist-25]. An ECG-HRV advantage now stands only as a hypothesis for arrhythmic or ectopic recordings.
3. **To the clinician:** my round-1 F3 raised a flag on every spot-check and would have produced about 9.5 false flags per person-year. It is redesigned (D3).
4. **To the physiologist:** radar is a mechanical pulse sensor, and radar PTT/BP stays research [em_engineer-1, em_engineer-7].
5. **To all:** EM carries almost none of the challenge score (D6). Spot-checks shrink from 2 × 2 min to 30–60 s (device_engineer's design) to protect adherence.

## 5 Updated position — EM-ANCHOR v2

EM-ANCHOR v2 combines the consensus engine with an optional EM tier:
- **Engine and evaluation** (bayesian_ml): q-weighted hierarchical local-level model, CUSUM and landmark hazard; abstention counts as a miss; person-time alarm budgets; **plus** a mandatory level-only comparator.
- **Windows and persistence** (physiologist): night window plus morning spot-check, timescale-separated persistence, covariates.
- **Data and fairness** (ppg_scientist): All of Us lead-time evaluation, PPG-HTN score, MNAR tests stratified by ITA.
- **Clinical anchor** (clinician): t_ref, cuff confirmation, never mmHg.
- **Product** (device_engineer): locked model, Class IIa, measured power budget.
- **EM tier** (mine; pre-registered, with kill criteria): a 30–60 s ECG spot-check gives PAT and the rhythm gate and flag; a pilot bedside 60 GHz radar covers the breathing/OSA axis and coverage.

## 6 References

*Round-1 references are cited by their round-1 IDs and entries. New references for round 2 follow.*

*(No new references: this critique cites round-1 references by ID. The optional verification lookups were interrupted by a usage limit.)*

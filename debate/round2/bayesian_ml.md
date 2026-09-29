# Round 2 — Cross-critique: THE BAYESIAN (`bayesian_ml`)

**Lens.** The scarce resource in this challenge is not sensors or parameters. It is **incident-hypertension events with dense pre-onset data**. I judge every design choice by how many events it consumes, and every metric by whether it is computed per event or per window. My round-1 position was BayesTrack-HTN: hierarchical state-space baseline → CUSUM/BOCPD → landmark hazard → calibrated 3-state output. In-text `[PS-n]` = `[ppg_scientist-n]`.

## 1. Cross-critique

### 1.1 clinician — CONFIRM-HTN
**Steelman.** RQ3 cannot be scored until the clinical reference point is defined, and the clinician defines it best: sustained, out-of-office, with dual ESC/AHA thresholds [clinician-1, clinician-5]. "Never output mmHg" follows directly from the under-tracking evidence [device_engineer-14].

**Attack.**
- *Verification bias in the proposed pilot.* "Each alert triggers home BP and the result feeds back as a label" means alerted people are verified early, and non-alerted converters are verified late or never. Sensitivity among verified converters is then inflated by design (partial verification). Fix: scheduled HBPM weeks for everyone (e.g., quarterly), alert-triggered HBPM as an extra, and lead time computed against scheduled measurements only.
- *False alarms under censoring.* The E3 target (≤~14% of non-hypertensives alerted over 2 years) transplants a *prevalent*-HTN specificity [clinician-15] into an *incident* task. A WARN in a non-converter near the end of follow-up may be a correct warning whose event is right-censored. Counting it as a false alarm penalises exactly the earliest true warnings.
- *Lead-time resolution.* If labels come from office visits every ~3 months, onset is interval-censored with ~90-day width, and the ≥3-month target (C12) cannot be distinguished from zero. Lead time must be reported together with its label interval.
- C5's medication-tracking evidence is n = 3 [clinician-13]; the claim stays MODERATE only because Derendinger (N = 166) [device_engineer-14] carries it.

**Questions.** (1) When and how are non-alerted participants verified in your pilot? (2) What lead-time resolution do office-only labels allow? (3) Do you accept "abstained throughout = miss" for E2?

**Overstated reference.** [clinician-23] is cited for "the trajectory, not just the level, carries risk". Its HR 3.91 compares elevated-increasing with low-stable groups, which conflates level and slope. Its own increment for trajectory over baseline BP is ΔC = 0.0084–0.0192: level dominates (§2).

### 1.2 em_engineer — EM-ANCHOR
**Steelman.** The most honest champion paper: a ledger against its own idea and a pre-registered ablation with a kill criterion. Its best evidence is [em_engineer-29]: PPG-PRV underestimates SDNN by 8.50 ms in cardiovascular patients, so "PRV = HRV" cannot be assumed in the population that matters.

**Attack.**
- *C8: ICC is not detectability.* ICC = σ²_between/(σ²_between + σ²_within) measures how well a feature *ranks people*, not whether it detects change *within* a person. With SEM = SD·√(1−ICC) and MDC95 = 1.96·√2·SEM (standard definitions), ICC = 0.7 gives a single-measurement MDC95 ≈ 1.5 SD of the measure across people (my arithmetic). The same study reports calibrated MAE of 10.1–12.9 mmHg [em_engineer-11], about the size of the whole transition to stage 1. Averaging helps only if daily errors are independent, and calibrated-watch error grows systematically with distance from the calibration point [bayesian_ml-25].
- *C8: wrong timescale.* The within-person PAT–SBP r = −0.82 [em_engineer-25] was measured under acute, exercise-induced BP changes. The target regime is a few mmHg over months against daily state noise, and state noise is large. Mental stress shortened PEP from 104.5 to 90.0 ms, i.e. −14.5 ms [physiologist-13]. That is more than the net PAT shortening under phenylephrine: PTT −16.8 ms offset by PEP +5.5 ms ≈ −11 ms (my arithmetic from [em_engineer-24]). The cohorts differ, but one stressful morning moves a spot-check PAT about as much as a pressor drug.
- *The kill criterion is underpowered.* Detecting a Se(90 d) gain from 40% to 55% (paired; discordant proportions 20%/5%; α = 0.05; power 0.8) needs about 85 converters with dense pre-onset ECG (my arithmetic, standard McNemar approximation). No dataset named in round 1 has them, and the challenge data probably has no ECG (their §2). "No gain" will be the outcome whether or not EM helps.
- C12: radar HR "within 10%" in 87% of studies [em_engineer-2] means ±6 bpm at 60 bpm. That is larger than the +4 bpm threshold NightSignal used for acute infection [bayesian_ml-1].

**Questions.** (1) What is the *within-subject* day-to-day SD of resting spot-check PAT, and hence its MDC? (2) What effect size can your kill criterion detect with the data you actually have? (3) Without ICG, how do you separate PEP-driven from vascular PAT change?

**Overstated references.** [em_engineer-11] (ICC used as evidence for change detection) and [em_engineer-25] (acute correlation used for slow drift), as above.

### 1.3 ppg_scientist — TRACE-PPG
**Steelman.** The most realistic reading of the data (everything must run on PPG-derived features) and the most useful fairness insight. Dark skin mainly causes *missingness*: participants with ITA° < 10° were 36% of the sample but accounted for 50% and 85% of missing data [PS-22]. That is missing-not-at-random, so abstention rates will differ by skin tone. I adopt their skin-tone-linked MNAR stress test and coverage-by-subgroup reporting.

**Attack.**
- *C11 overstates [PS-3].* PPG 0.819 vs ECG 0.769 compares ECG *instead of* PPG, on self-reported labels. It shows ECG alone is weaker. It does not test ECG *added to* PPG, so "no measurable gain from ECG" is not established.
- *Mondrian conformal will be vacuous for the rare class.* Split conformal at miscoverage α needs at least (1−α)/α calibration points per stratum and label: 9 at α = 0.1, 19 at α = 0.05. Below that, the quantile is infinite and the label is always in the set. With tens of converters split across quality strata and subject-disjoint folds, "risk" is always in the set: nobody is ever STABLE, and INSUFFICIENT becomes the default output. (My design has the same flaw; see §4.)
- *All of Us lead time is partly care-seeking time.* Incident HTN there comes from EHR linkage [PS-26], so lead time against it partly measures the gap to the next clinic visit, not physiology.

**Questions.** (1) How many positive calibration subjects per Mondrian stratum do you expect, and what does TRACE-PPG output when there are fewer than 9? (2) How do you adjust All of Us lead times for visit frequency? (3) Can a Tunisian student team obtain registered-tier access within the challenge window?

**Overstated reference.** [PS-3], as above. [PS-25] is a days-scale analogue for a months-scale problem, the same caveat I apply to my own C1.

### 1.4 physiologist — NOCTURNE
**Steelman.** Timescale separation is the only *principled* rule anyone offered for setting persistence. The window must outlast every known transient: alcohol (~3 bpm, days) [physiologist-23], infection (~3 days before symptoms) [physiologist-22], the menstrual cycle [physiologist-21]. This turns a free hyperparameter into a physiologically bounded one, and their ablations (i)–(ii) are genuinely falsifiable.

**Attack.**
- *Slow confounders pass straight through.* Season (0.61 mmHg per 1 °C drop [physiologist-24]), weight change, detraining, device or firmware swaps and new medication act over the same weeks-to-months as the drift. "≥4 of 6 weeks" cannot reject them; only covariates or a seasonally adjusted baseline can.
- *"≥2 coherent axes" can be one axis counted twice.* PAT appears in both "sympathetic drift" and "vascular drift", and the PEP inside PAT is sympathetic (it halves under physical stress [physiologist-13]). One sympathetic shift can therefore satisfy "2 axes". Counting agreeing axes assumes independent noise. Correlated channels should be combined in a joint posterior, where they add less evidence.
- *The false-alarm rate of k-of-n cannot be read off the rule.* With independent weekly exceedances at p = 0.10, P(≥4 of 6) ≈ 0.0013 (my arithmetic). Slow confounders create exactly the autocorrelation that breaks independence, so the rate must be measured on non-converter person-time.
- 4–8 weeks of baseline plus 4 of 6 weeks of persistence means no warning before ~10–14 weeks of wear.

**Questions.** (1) Which model term removes seasonal and weight-driven drift that lasts more than 6 weeks? (2) With PPG-only data (no PAT), can NOCTURNE still reach "≥2 axes"? (3) What minimum follow-up per person does NOCTURNE need to warn at all?

**Overstated reference.** None found. [physiologist-25] is N = 13 and device-dependent (Polar HRV CCC 0.82), which they already tag WEAK–MODERATE.

### 1.5 device_engineer — BioVance-Edge
**Steelman.** The single most important fact for formulation: calibrated cuffless devices reported a 1.8 mmHg change where the cuff saw 7.4 mmHg (N = 166) [device_engineer-14]. Estimate-then-threshold (M7) shrinks toward the calibration point, and the drift is the quantity we want. That settles F5 against M7. Their locked model with per-user state [device_engineer-1] is also the right regulatory reading.

**Attack.**
- *"Fixed warning precision" does not transport.* Precision depends on the converter prevalence of the development cohort. Tune on a cohort enriched with converters and deployment alarms multiply. The constraint should be false alarms per non-converter person-year: prevalence-free, and estimable from plentiful negatives.
- *Wear-time of 77.4%* [device_engineer-25] is unlikely to be a random loss. Removal plausibly clusters in illness and travel, the same states that confound, so the stress tests need MNAR missingness, not only the ≥15-day enrolment gate.

**Questions.** (1) What false-alarm rate per person-year does your fixed-precision threshold imply at deployment prevalence? (2) At one spot-check every 3 days, does ECG still measurably shrink the posterior variance of drift?

**Overstated reference.** [device_engineer-26] comes from post-stroke/TIA patients ≥50 years wearing a watch for 14 days; transfer to healthy screening users is untested.

## 2. Red-teaming the consensus

**Case A — deviation-only designs throw away the level.** All six prototypes subtract a personal baseline. Yet nearly every prospective predictor cited is a between-person *level*: RMSSD Q1 vs Q5 HR 1.58 [physiologist-1], PWV RR 1.09 [em_engineer-27], PPG-age gap HR 2.88 [PS-27], AIRE-HTN C = 0.70 [physiologist-20]. Apple's cleared feature is a 30-day level classifier [bayesian_ml-4]. Where trajectory was tested against level, it added ΔC ≤ 0.02 [clinician-23]. The only within-person evidence cited is 10-s clinic-ECG HRV change [physiologist-1], not wearable data; the physiologist concedes that "lead time is a hypothesis". Someone enrolled at 128/78 and creeping upward is normalised by their own baseline. The strongest rival is therefore a **pooled, level-based landmark classifier re-scored monthly, with no personal baseline**.
*Falsifier:* at an equal false-alarm budget per non-converter person-year, the level-only model reaches Se(90 d) and median lead time within the CI of the deviation pipeline. Then personalisation adds nothing measurable, and the RQ1 claim must be dropped.

**Case B — convergence from shared sources.** The six papers lean on the same few studies: K250507, Aurora, NightSignal, Finnegan/Heimark. NightSignal detects infections over days [bayesian_ml-1]; hypertension develops over months to years. The architecture's core has **no direct evidence on incident hypertension**, and agreement among us is not corroboration. *Falsifier:* the same test as Case A.

**Case C — the F2 rejection is over-scoped.** The base-rate argument [clinician-31] holds for a daily predictor in unselected people. In enriched populations, prediction is not empty. A 14-day single-lead patch ECG (an EM signal) predicted near-term sustained VA with external AUROC 0.948 [physiologist-28], although PPV was only ≈9–10% even in a referred population (physiologist's derivation). Wrist accelerometry reached AUROC 0.74 in ICD patients [PS-19]. The correct verdict is that F2 is out of scope for *this challenge* and for *unselected consumers*, not that it is infeasible. *Falsifier within the challenge:* the organisers' data turns out to carry acute-event labels or ECG.

## 3. Positions on D1–D6
- **D1 Sensor set.** Channel-agnostic core. PPG+IMU is the minimum and the only configuration testable in the challenge. ECG/PAT is a *hypothesis*: its PEP component duplicates HR and stress information already present, and showing its value needs ~85 converters (§1.2). Keep the ECG spot-check as an optional real-world tier with a pre-registered power analysis, never as a claim.
- **D2 Radar.** Not for the challenge. HR "within 10%" is too coarse for drift. Radar's distinctive value is sleep-apnoea context (AHI r = 0.94 with SpO2 [device_engineer-29]), i.e. a later covariate.
- **D3 F3 channel.** Not an alarm stream: the alarm budget is per person, and a second stream spends it. Use rhythm flags only to *gate* HRV/PAT windows (quality/context), unscored.
- **D4 Formulation and tuning.** Both, in sequence. Change detection supplies features and the warning timestamp; a penalised discrete-time landmark hazard supplies calibrated risk and handles censoring. k-of-n rules are crude sequential tests, so compare every candidate at *equal false alarms per person-year* and report delay distributions. Anti-overfitting protocol:
  1. Set all thresholds (h, k-of-n, α) on **non-converters only** to meet a pre-registered budget (Neyman–Pearson; negatives are plentiful).
  2. Use converters only to *evaluate* Se(ℓ) and lead time, in outer subject-grouped forward-chaining folds.
  3. Pre-register at most 3 persistence rules (≥2/3 windows, ≥4/6 weeks, CUSUM).
  4. Subject-bootstrap CIs; injected-onset synthetic data for delay-vs-magnitude curves.
  5. Abstained throughout = miss. WARNs in non-converters within W days of the end of follow-up = censored, not false alarms.
- **D5 Reference.** The organiser label is primary. With raw cuff data: sustained crossing (two consecutive qualifying periods), ≥130/80 as primary (regulatory precedent [bayesian_ml-4]; more events, more power), ESC home ≥135/85 as a sensitivity analysis, and report the label-reversal rate. Cuff labels are themselves seasonal [physiologist-24], so report t_ref by season. I accept ≥90 days as the pre-registered meaningful lead time, reported with the label-interval width.
- **D6 Data reality.** On PPG-derived features, no EM physiology (PAT, ECG-HRV, radar) is testable. What is testable: (i) channel-agnosticism, by dropping and adding channels; (ii) the spot-check *sampling regime*, by subsampling a PPG channel to twice daily with MNAR skipping, as an upper bound on what a sparse channel can add; (iii) a power analysis for a future EM pilot. EM claims belong in limitations and future work.

## 4. Concessions
1. **C10 weakened.** My conformal layer has the rare-class flaw I attacked in §1.3. Subject-level split conformal gives marginal coverage dominated by non-converters, with no guarantee for converters. Conformal becomes optional, used only when label-conditional calibration counts allow it. The primary uncertainty is the hierarchical posterior predictive plus isotonic calibration.
2. **My E2 rule was wrong for non-converters.** Late WARNs in non-converters are now censored (D4).
3. **C1 transfer weakened.** NightSignal [bayesian_ml-1] supports the *design pattern*, not months-scale detection (Case B).
4. **My A0 was a strawman.** A population *threshold* is replaced by a strong pooled level model (Case A).
5. **Baseline length.** 14 nights is too short by the physiologist's timescale argument. The minimum is now 28 valid nights (one menstrual cycle).

## 5. Updated position
**BayesTrack-HTN v2** keeps the same skeleton, with these merges:
- **Level + deviation.** The hazard takes both current levels (pooled) and personal-deviation features. The level-only A0 is the falsification test for RQ1.
- **Correlation-aware evidence.** A joint multivariate state-space posterior replaces axis counting, with season and ambient temperature as covariates (physiologist).
- **Reference and output.** Sustained out-of-office t_ref, never mmHg, and scheduled HBPM to avoid verification bias (clinician).
- **Fairness.** Coverage and abstention reported by skin tone, age and BMI under MNAR stress tests (ppg_scientist).
- **Deployment.** Locked model with per-user state and features-only upload (device_engineer); optional ECG spot-check tier with a power analysis (em_engineer, device_engineer).

## 6. References
Round-1 references are cited by their IDs. New references for round 2 follow.

*(No new references: this critique cites round-1 references by ID. The optional verification lookups were interrupted by a usage limit.)*

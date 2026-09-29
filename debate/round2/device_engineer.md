# Round 2 — Cross-critique: THE DEVICE ENGINEER (`device_engineer`)

**My round-1 position (BioVance-Edge):** passive wrist PPG+IMU, a 30-s twice-daily single-lead ECG spot-check for PAT, a weekly cuff, edge SQI, a cloud trajectory engine and a bedside radar in phase 2. The output is a notification, never mmHg. Citations use each author's IDs ([PS-n] = ppg_scientist-n). Arithmetic marked *(derived)* is mine, computed from the cited inputs.

## 1. Cross-critique

### 1.1 Clinician (CONFIRM-HTN)
**Steelman.** This is the best clinical anchoring in the debate. The reference point is out-of-office and analysed under both ESC and AHA definitions (C1, C2). The base-rate arithmetic (C9) rules out imminent-SCA prediction in unselected people.

**Attacks.**
- *§3 point 4 / C6: "Emerging hypertension is base-rate-friendly."* The 31.4% figure is the prevalence of *already-present*, undiagnosed hypertension [clinician-15]. It is not the incidence of emerging hypertension. For incidence I use [physiologist-1]: 40,268 cases in 232,587 adults over a median of 3.8 years, or roughly 4.6% per year (crude, derived). Suppose HTNF's operating point transferred unchanged, which is optimistic. A warning with a 6-month horizon would then have a PPV of about 11%, and one with a 12-month horizon about 21% (derived). Emerging hypertension is not base-rate-friendly. Prevalent hypertension is.
- *C12 (lead time of at least 3 months).* [clinician-2] and [clinician-5] describe the lifestyle window *after* diagnosis and before drugs. They set no minimum for how early a pre-diagnostic warning must come. The 3-month figure should be one point on an Se(ℓ) curve, not a pass/fail threshold.
- *Card, S2: "PAT at rest/sleep".* Watch ECG is on demand and needs the opposite finger on the electrode [PS-18]. PAT during sleep therefore needs a chest patch or garment, which is a different product. Even patients prescribed a life-saving vest wear it for only about 21 h/day [device_engineer-27].
- *C11 (HRV carries signal before diagnosis).* This is contested: in HELIUS, SDNN and RMSSD were not associated with new-onset hypertension, and only baroreflex sensitivity was [PS-28].

**Questions.** (1) At a PPV of about 11–21%, most true early warnings meet a *normal* home-BP series. What does the user do next, and does your E3 count that as a false alarm? (2) Which device gives you PAT during sleep? (3) What evidence, other than a post-diagnosis window, makes 3 months the minimum?

**Reference use.** [clinician-23] is cited to show that "the trajectory carries risk". Its own key number points the other way: adding the trajectory to baseline BP raised the C-index by only 0.0084–0.0192.

### 1.2 EM engineer (EM-ANCHOR)
**Steelman.** This is the most honest ledger of round 1, and the only paper with a pre-registered kill criterion for its own modality (E7). Its narrow claim is that EM features are for *within-person change*, not absolute BP. That is the right hypothesis to test.

**Attacks.**
- *C8: "PAT is repeatable (ICC >0.7), so it suits change detection".* A signal can be repeatable because it barely moves. The same study missed the BP responses to mental stress, and its calibrated MAE was 10.1–12.9 mmHg [em_engineer-11]. That is the anchoring failure I cited in round 1 [device_engineer-14].
- *The PEP confound, quantified (derived).* PAT–SBP slopes range from −470.64 to −2946 mmHg/s [em_engineer-24], so a 10 mmHg rise in SBP shortens PAT by 3.4–21.2 ms. Mental stress alone shortens PEP by about 14.5 ms (104.5 → 90.0 ms) [physiologist-13], which is 0.7–4.3 times that signal. A seated spot-check does not control mental state.
- *C5, the F3 channel.* [em_engineer-21] validated PVC burden on a *continuous* 3-day patch. EM-ANCHOR records 2 × 2 min per day, 0.28% of the day (derived). Burden cannot be estimated from that.
- *C7 is graded STRONG.* The pooled RR is 1.09 with "considerable heterogeneity" [em_engineer-27]. Carotid–femoral PWV is also not wrist PAT.

**Questions.** (1) Show responsiveness: within-person PAT change against cuff change over weeks, not repeatability. (2) How do you estimate AF/PVC *burden* from 4 minutes a day? (3) Without an ICG or SCG channel, how do you tell a PEP drop (stress) from a PTT drop (vascular)?

**Reference use.** [em_engineer-21], as above. The "<$30" in [em_engineer-6] is the authors' report of a research build, not a product BOM.

### 1.3 PPG scientist (TRACE-PPG)
**Steelman.** This proposal matches both the likely data (D6) and the one regulatory precedent: PPG only, 30-day windows, a self-supervised encoder with a linear head [PS-1], a two-tier SQI and a usable-day counter. If the organisers ship only PPG features, it is the only fully testable design.

**Attacks.**
- *C11: "PPG embeddings beat ECG embeddings" (0.819 vs 0.769).* The labels are self-reported and the analysis is cross-sectional. The participant sets also differ: 141,207 for PPG against 106,643 for ECG [PS-3]. The result shows that PPG discriminates *prevalent* self-reported hypertension. It does not show that ECG adds nothing to change detection. For D1 I grade it WEAK.
- *C4 (Aurora).* This is strong evidence against PAT for absolute next-day BP [PS-8]. A risk-trajectory notifier was never tested. I take it as a sceptical prior, not a verdict.
- *"Hardware BOM: none beyond watch".* Morphology features and PaPaGei need raw PPG. Whether a commodity watch exposes it to third parties is a platform-access question the card does not answer (verification pending, §6).
- *Latency (derived).* A 30-day baseline plus persistence in ≥2 of 3 windows means no warning before about 90 qualifying days. 16% of HTNF enrolees failed the ≥15-of-30-days gate [device_engineer-1], so calendar time is longer still.

**Questions.** (1) Which watch, SDK, sampling rate and licence give you raw PPG? (2) If the earliest possible warning is around day 90, how much follow-up before t_ref does the organisers' data contain? (3) In [PS-3], what separates the effect of modality from the effect of data volume?

**Reference use.** [PS-25] reports COVID alerts 3 days ahead, triggered by resting HR 4 bpm above baseline. That signal is larger and faster than a pre-hypertensive drift. It supports the machinery, not the lead-time claim.

### 1.4 Physiologist (NOCTURNE)
**Steelman.** Timescale separation and night anchoring are the best RQ4 answers in the debate. Its ablations (all-day vs night windows, with and without residualisation) are falsifiable, and the paper states its prediction for them.

**Attacks.**
- *Timescale separation fails for season.* Ambulatory BP rises 0.61 mmHg for each 1 °C fall in personal ambient temperature [physiologist-24]. A 10 °C drop therefore gives about 6 mmHg (derived). That is the size of the transition, on the same months-long timescale. A rule of persistence in ≥4 of 6 weeks cannot tell autumn from disease without a seasonal prior.
- *PHY-9.* The CCC of 0.97–0.99 comes from a finger ring in N=13 people, and the Polar HRV CCC was 0.82 [physiologist-25]. Transfer to the wrist is not shown.
- *The vascular axis against the hardware.* The nocturnal PAT in [physiologist-15] needs overnight ECG plus PPG (polysomnography). NOCTURNE's ECG is a morning spot-check.
- *PHY-5 is graded STRONG.* It rests on two EHR-linked Fitbit cohorts of 6,042 and 6,785 people, with 482 incident hypertension cases in the steps cohort [physiologist-6, -7]. That is MODERATE.

**Questions.** (1) Which seasonal model do you fit in year one? (2) What validates wrist-SpO2 dips as the OSA surrogate on your sleep–breathing axis? (3) A 4–8-week baseline plus 4 drifting weeks puts the first warning at 8–12 weeks at the earliest. Is that compatible with the length of the data?

**Reference use.** [physiologist-15], as above.

### 1.5 Bayesian ML (BayesTrack-HTN)
**Steelman.** Its evaluation protocol is the most valuable scoring asset in the debate:
- abstentions count as misses;
- alarm budgets are set per person-time (specificity 92.3% for one window but 86.4% over six [bayesian_ml-4]);
- no point-adjust [bayesian_ml-13];
- lead time counts from a sustained warning;
- measurement density is reported.

**Attacks.**
- *No null model.* The ablations A0–A8 have no **cuff-only** baseline: intermittent cuff BP plus its slope and demographics, fed to the hazard. The latent "BP-load" state may carry most of the lead time. In Aurora, a baseline of the calibration cuff plus time of day beat every waveform model [bayesian_ml-23]. A0 (a population threshold) is a straw man; the real competitor is a trained cross-sectional classifier in the style of HTNF.
- *The STABLE state.* Your own [bayesian_ml-5] shows that 58.8% of undiagnosed cases get no alert. A message saying "STABLE" is the false reassurance warned about in [clinician-17], and the challenge specifies three states.
- *Conformal prediction with few positives.* Subject-level split conformal with a handful of converters gives unstable class-1 sets. The supporting claim (C10) is graded WEAK and comes from sepsis.

**Questions.** (1) Once you add the cuff-only baseline, by what margin must the wearable channels beat it? (2) How many converters do you need before EMERGING-RISK sets are non-trivial? (3) Why emit STABLE at all?

**Reference use.** I found no misuse; the hedging is appropriate.

## 2. Red-team the consensus

**R1: The evidence favours levels, not personal change.** Every positive wearable- or ECG-to-hypertension result retrieved so far is between-person and based on levels:
- HTNF, a cross-sectional 30-day classifier with no personal baseline [device_engineer-1];
- AIRE-HTN, C-index 0.70 from one 12-lead ECG [physiologist-20];
- the PPG-age gap, HR 2.88 [PS-27];
- LSM-2, AUROC 0.754 [bayesian_ml-19].

The only head-to-head comparison found that the trajectory added 0.0084–0.0192 C-index over baseline BP [clinician-23]. Personal baselines are also blind, by construction, to people who enrol mid-transition: in the HTNF pivotal study, 31.4% of people with no diagnosis already met the reference [device_engineer-1]. We converged on the architecture the rubric advertises (RQ1), not on one that evidence has tested.

*Falsifier:* on the organisers' data, run a trained cross-sectional classifier (window features, demographics, last cuff reading) against the full personal-change pipeline at equal false alarms per person-year. If the personal-change parts do not raise event-level Se(90 d) by a pre-registered margin, with a CI that excludes 0, the consensus core is decoration.

**R2: The confirmation paradox.** A truly *early* warning comes before cuff-detectable hypertension, so a confirmatory home-BP series at that moment should be *normal*. A warning that the cuff confirms caught prevalent hypertension that nobody had measured. That is earlier *diagnosis*, and its "lead time" is an artefact of sparse cuff sampling. All six cards end with "confirm by cuff", which is logically inconsistent with "warn before clinical detection".

*Test:* for each warning that has a cuff reading within ±14 days, tabulate whether that reading was above or below the threshold. *Design fix:* after a warning, run a home-BP *surveillance schedule* (repeated weekly series), not a one-shot confirmation.

**R3: Two null models nobody ran.** These are the cuff-only hazard (§1.5) and a seasonal check (§1.4).

*Falsifier:* the cuff-only model performs at least as well as the full model, or non-converters show more false alarms in winter.

**R4: F2.** The rejection is right *for this challenge*: there are no event labels, so RQ3 cannot be measured. It is also right for unselected populations, because of the base rate in C9. It is not right *as science*:
- near-term ventricular-arrhythmia prediction from 14-day single-lead ECG reached an external AUROC of 0.948 in a referred population [physiologist-28];
- SAFEHEART reached 0.74 [PS-19];
- a case report found change-points 4–6 months before SCD using exactly our method [bayesian_ml-6].

In enriched cohorts, F2 is the same architecture with a different label. *Falsifier of our rejection:* organiser data that carries acute-event labels.

## 3. Positions on D1–D6

| | Position | What would change my mind |
|---|---|---|
| D1 | The submission uses PPG+IMU (plus cuff). ECG/PAT is unproven: Aurora was null [PS-8], PEP change is 0.7–4.3 times the signal (derived), and watch ECG is on demand only [PS-18]. In hardware, the ECG electrodes stay as a rhythm/quality gate (AF sensitivity 96.0%, specificity 98.7% [PS-18]). The MAX86176 already does the PPG, so this costs two electrodes. PAT enters only as a pre-registered ablation, with em_engineer's kill criterion. | PPG+PAT beats PPG alone at tracking within-person BP change in Aurora-BP [PS-9] |
| D2 | Radar is no closer to the vascular mechanism (physiologist). Its unique value is sleep-apnoea context, which already-validated devices provide [device_engineer-29, em_engineer-39]. Refer patients to those devices; do not build radar. | Evidence that nightly radar context lowers false alarms compared with wrist-only data |
| D3 | No user-facing acute channel: it earns 0 points, adds a second intended use [PS-18] and adds a second alarm stream [clinician-32]. Rhythm checking stays internal, as a gate. Never use "cardiac attack" language. | Organiser acute-event labels |
| D4 | Change detection generates the evidence; a calibrated discrete-time hazard gives the risk and the timestamp. Tune k-of-n under an alarm budget and report the whole curve. Physiology sets the floor (at least one menstrual cycle, about 4 weeks); lead time sets the ceiling. Unobserved weeks extend the window and never count as drift. | — |
| D5 | The organisers' label is primary. ESC (home ≥135/85) and AHA (≥130/80, comparable with HTNF) are sensitivity analyses. Report Se(ℓ) at 0/30/90/180 days rather than a 3-month pass/fail, plus cuff measurement density and the R2 cuff-status table. | — |
| D6 | No EM channel can be scored on RQ1–RQ6 within the challenge. EM is testable only (a) as modality dropout (RQ5) and (b) on Aurora-BP, for a proxy (BP-change tracking) that cannot give lead time. If only aggregated features ship, the morphology and SSL encoders cannot be tested either. | The organisers' data dictionary |

## 4. Concessions
1. **DE-C1 framing withdrawn.** I wrote that teams should "beat the HTNF bar". That was wrong: HTNF detects *prevalent* hypertension cross-sectionally [PS-1, bayesian_ml-4]. It is a comparability anchor, not the same task.
2. **The ECG spot-check's "best ratio" is weakened.** It is still the cheapest EM add-on, but its value is unproven (Aurora, PS-3, and the PEP arithmetic). It leaves the core of my prototype.
3. **DE-C13, the phase-2 radar, is withdrawn from the build plan** (see D2).
4. **DE-C7 cuts both ways.** The under-tracking in [device_engineer-14] reflects weak responsiveness of the features as much as calibration anchoring, which also weakens my own PAT channel.
5. **DE-C12 is downgraded to WEAK.** [device_engineer-26] concerns AF alerts in post-stroke patients aged 50 or over; for hypertension notifications it is only an analogy.
6. **The DE-C11 extension is unverified.** My claim that per-user baseline state is not "continuous learning" was my own interpretation (verification pending, §6).
7. **The power budget (≥1 week) is an unmeasured estimate.** I expect LED drive on darker skin or higher BMI to be where it fails. That is my inference; the evidence only shows missing data concentrated in dark skin [PS-22].

## 5. Updated position: BioVance-Edge v2
- **Challenge submission (software only).** It merges:
  - from TRACE-PPG, the two-tier SQI and usable-day counter;
  - from NOCTURNE, the main-sleep windows and confounder tags, to which I add a seasonal covariate;
  - from BayesTrack, the quality-weighted local-level model, CUSUM, landmark hazard and evaluation harness;
  - from CONFIRM-HTN, the dual-guideline t_ref.

  The cuff-only and cross-sectional nulls (R1, R3) become mandatory ablations. The output has three states, with no STABLE state. Warnings trigger cuff *surveillance*, not confirmation (R2).
- **Hybrid core (R1).** A population-level classifier sets the prior and covers people who enrol already hypertensive. Personal change detection is layered on top, and the ablation decides how much it adds.
- **Real-world device.**
  - passive wrist PPG+IMU on a platform that exposes raw PPG;
  - ECG electrodes as a rhythm gate, plus an optional seated PAT for the ablation;
  - no radar;
  - a locked model with per-user state;
  - only features are uploaded.

## 6. Verification log (lookups after drafting)
*(No new references: this critique cites round-1 references by ID. The optional verification lookups were interrupted by a usage limit.)*

## References (new in round 2; round-1 entries [device_engineer-1…32] unchanged)
*(No new references: this critique cites round-1 references by ID. The optional verification lookups were interrupted by a usage limit.)*

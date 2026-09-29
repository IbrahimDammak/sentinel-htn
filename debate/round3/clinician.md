# Round 3 — Defence and final position: THE CLINICIAN (CONFIRM-HTN v3)

Round-1 references keep their `[clinician-n]` IDs. `[PS-n]` = ppg_scientist. No new research this round.

## 1. Rebuttal

**em_engineer: "C9 does not transfer to F3."** Conceded in part. Rhythm detection has a different base rate: concurrent AF PPV was 98.2% [clinician-34] and on-demand AF classification reaches 96.0%/98.7% [PS-18]. What still holds is that a user-facing acute or rhythm stream costs class, care utilisation and anxiety [clinician-32, -33], and (audit B) [clinician-33] is AF patients, so it is an analogy. I accept an *internal* rhythm gate and one persistence-gated "see a clinician" message outside the hypertension alarm budget. I do not accept any MI/SCA wording.

**em_engineer: "Sleep PAT cannot be built as specified."** Correct. Watch ECG is on demand only [PS-18]. "PAT at rest/sleep" is withdrawn from my card. PAT stays a pre-registered ablation, not a component.

**em_engineer / ppg_scientist / device_engineer: "C11 overstated" (HR 3.91 concerns CVD; trajectory adds ΔC 0.0084–0.0192; HELIUS null).** Conceded. [clinician-23] uses clinic BP and a CVD outcome, and level dominates slope. C11 is now: "HRV/trajectory evidence is contested; the personal-change engine has to earn its place against a level model."

**ppg_scientist: "Persistence uses up lead time."** Accepted. Two of three 30-day windows costs at least 60 days. I move to weekly aggregates, ≥4 of 6 weeks (a floor of about 28 days, one menstrual cycle), plus a faster non-alerting "watch" tier. A 90-day target needs drift visible about 120 days before t_ref.

**ppg_scientist: "Which threshold is primary? What is the E3 number?"** The organisers' label is primary. If none exists, an HBPM mean ≥130/80 is primary because it is comparable to the only regulatory benchmark [PS-1], and ESC ≥135/85 / 24-h ≥130/80 is a pre-registered sensitivity analysis. Each needs two qualifying occasions. I concede that ESC-primary would inflate lead time. Budget number (my proposal, not an evidence-derived value): at most 0.5 alerts per non-converter person-year. The audit-B correction applies: 86.4% is a mean per-window specificity over six windows, so my "≤~14% alerted over 2 years" line is dropped.

**physiologist: "Base-rate-friendly is a misapplication."** Withdrawn in round 2, and I keep it withdrawn. The 70.9% PPV holds at 31.4% *prevalence* of existing disease. At 1–2.5% six-month incidence a 50%/92.3% warning has a PPV of about 6–14% (arithmetic checked by Auditor B); in high-normal BP, where 21.8% converted in 6 months [clinician-36], about 64%. Who is monitored decides the value, so enrolment targets elevated or high-normal BP first.

**physiologist / device_engineer: "The nocturnal flag has no sensor; no evidence for 3 months."** Downgraded to a triage hypothesis. Calibrated arm and ring devices track awake–asleep change only moderately (LoA about ±10–13 mmHg, κ 0.58) [clinician-37, -38], and the ESH says ABPM stays the reference [clinician-39]. The ≥90-day figure is my inference from post-diagnosis lifestyle windows [clinician-2, -5], not evidence. I report Se(ℓ) at 0/30/90/180 days and drop pass/fail.

**bayesian_ml: verification bias, censoring, interval-censored labels.** All accepted. Scheduled HBPM weeks for everyone (quarterly), alert-triggered HBPM as an extra, and lead time computed against scheduled series only. Warnings within W days of end of follow-up are censored, not false. Lead time is always reported with its label-interval width.

**device_engineer: "Confirmation paradox" and "missed spot-checks are informative."** Accepted. A truly early warning meets a *normal* cuff series, so the action is a 7-day weekly *surveillance* series, not one-shot confirmation. Missing spot-checks are MNAR and feed abstention and coverage reporting.

**device_engineer: "PAT contradicts DE-C7"; "radar precedent misapplied."** PAT is dropped from my core. I never proposed radar; I accept that C200/C300 are clinical-setting devices without alarms [device_engineer-5, -6] and that the audit limits "every cleared radar monitor" to three named devices.

**bayesian_ml / ppg_scientist: unsafe "STABLE".** Agreed. Three states only, and "no alert" never means "no hypertension" (58.8% of cases unalerted at the precedent's point [clinician-16/-17]).

## 2. Audit response

- **[c-15]/[c-16] (C6):** STRONG becomes MODERATE plus INDUSTRY-CLAIM (sponsor 510(k) data and a NHANES model; PPV/NPV are *modelled*). The 70.9% PPV concerned prevalent disease.
- **C2 ([c-21] Fujiwara, HR 1.72):** MODERATE (152 events, CI floor 1.01). [c-18], [c-19] stay STRONG.
- **C4 (cuffless):** ESC asks for validation standards and gives no blanket "do not use"; "every guideline body" is withdrawn. "Protocols test accuracy after calibration, not stability" is wrong for ESH 2023 [clinician-10], which has a recalibration-stability test. Restated: ESH/AHA do not recommend cuffless for diagnosis.
- **[c-13] within-person claims:** WEAK–MODERATE (one device; the drug arm has n=3). "Drift vs disease" is my inference.
- **Superlatives deleted:** "strongest AI-ECG result" ([c-26]) and "only real evidence" ([c-34]).
- **[c-30], [c-34]:** industry-authored, now INDUSTRY-CLAIM; Fitbit's 32.2% is recurrence on a later patch, not alert accuracy.
- **[c-24] Hoshi:** "associated with", not "predicted". **[c-33]:** an AF-patient analogy. **[c-3] AHA thresholds:** STRONG stands only through [c-4]/[c-5]. **[c-35]:** hypothesis-generating (28 events, CI 0.57–0.76). **[c-36]:** possible outcome circularity (BP predicting BP), WEAK–MODERATE, so no design decision rests on it. **[c-37], [c-38]:** small validations with manufacturer links, INDUSTRY-CLAIM.

## 3. PROTOTYPE CARD (v3), CONFIRM-HTN

- **Target:** emerging elevated-BP risk in adults with elevated or high-normal BP first; timestamp of first sustained warning; no mmHg output; no acute-event claim.
- **Sensors:** commodity wrist PPG+IMU (locked features); validated home cuff (scheduled quarterly 7-day series, plus a surveillance series after any warning). ECG only as an internal rhythm/quality gate.
- **Model:** Lane A, pooled level score (PPG-HTN encoder score plus demographics); Lane B, night-anchored, context-residualised personal change (weekly aggregates, ≥4/6 weeks, season covariate). Landmark logistic risk layer.
- **Output states:** SUFFICIENT-warning / INSUFFICIENT / POOR-QUALITY; evidence ledger; never "stable".
- **t_ref:** two qualifying out-of-office occasions; organiser label first, else HBPM ≥130/80 with ESC as sensitivity.
- **Budget:** ≤0.5 alerts per non-converter person-year (proposal).
- **Mandatory falsifier:** level-only and cuff-only models against the full pipeline at matched false alarms; if the CI of the gain includes zero, personalisation is decoration and the paper says so.

## 4. Final ranking (0–10; "Ev" = evidence strength, "Eng" = real-world engineerability, "Stu" = student buildability in 4–8 weeks)

| Option | RQ1 | RQ2 | RQ3 | RQ4 | RQ5 | RQ6 | Ev | Eng | Stu | Justification |
|---|---|---|---|---|---|---|---|---|---|---|
| CONFIRM-HTN (mine) | 5 | 6 | 7 | 5 | 5 | 6 | 6 | 7 | 8 | Best reference-point and cuff logic; light ML and no robustness engine, so I mark RQ1/RQ5 down. |
| EM-ANCHOR | 6 | 6 | 5 | 6 | 6 | 6 | 3 | 5 | 4 | EM tier is untestable on likely data and PAT lacks responsiveness evidence. |
| TRACE-PPG | 7 | 6 | 6 | 6 | 8 | 6 | 7 | 8 | 8 | Only design mapped to a cleared precedent and testable data; latency and level-vs-change unresolved. |
| NOCTURNE | 7 | 8 | 6 | 8 | 6 | 6 | 5 | 6 | 6 | Best context reasoning; season and 13-person night evidence are open. |
| BayesTrack-HTN | 8 | 8 | 7 | 6 | 8 | 9 | 6 | 6 | 5 | Best evaluation and uncertainty; conformal weak with few events; heavy for 4–8 weeks. |
| BioVance-Edge | 5 | 5 | 6 | 5 | 7 | 6 | 5 | 8 | 4 | Best regulatory and power realism; hardware shrinks student scope. |
| F2 as stated | 2 | 2 | 1 | 2 | 3 | 2 | 3 | 2 | 2 | Wrong target: PPV about 0.1% daily (CI arithmetic checked); no RQ maps; Class IIb/III. |

## 5. Recommendation

- Build software-only PPG+IMU with a hybrid engine: pooled level lane plus personal-change lane.
- Enrol elevated or high-normal BP first, where a warning has a PPV worth acting on.
- Define t_ref out-of-office with two occasions; report Se at 0/30/90/180 days with label-interval width.
- Use BayesTrack's event-level harness: abstention is a miss, alarms per non-converter person-year, censoring-aware precision.
- Post-warning action is weekly cuff surveillance, not one-shot confirmation.
- Never output mmHg or "stable"; three states only.
- Run the level-only and cuff-only nulls as mandatory ablations.
- Rhythm is an internal gate only; no MI/SCA language.

**Verdict on the user's idea (F2).** As stated, "EM signals to detect sudden or premature cardiac attack" does not fit this challenge: it scores zero on RQ3 because no acute-event labels exist, and in unselected people the base rate (about 37–40 SCD per 100,000 per year) gives a PPV near 0.1% even at 99.9% specificity. It is not wrong as science in referred populations (14-day ECG, external AUROC 0.948 for near-term VA, PPV about 10%). The salvageable form is EM as a front end and rhythm gate inside an HTN trajectory engine, validated first on hypertension.

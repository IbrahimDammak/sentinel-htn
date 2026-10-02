# Panel review: cardiologist / hypertension specialist

Performance numbers are synthetic (`results/summary_3seeds.md`).

## 1. Who should wear it

**Target:** untreated adults aged 30–65 whose **onboarding 7-day home-cuff mean is <130/80**, enriched for risk: home BP in the ESC "elevated" band (120/70 to <135/85 [ESC24]), a hypertensive parent, overweight, or previous pre-eclampsia. Why: detection needs a normotensive start, and pre-test probability is the only lever on precision.

**Exclude:**
- **Diagnosed or treated hypertension; beta-blockers, ivabradine, verapamil or diltiazem:** the label is meaningless and night HR/HRV are clamped.
- **Pregnancy to 12 weeks postpartum:** different thresholds; pre-eclampsia cannot wait 4–6 weeks.
- **AF, frequent ectopy, pacemaker:** PPG HRV is invalid.
- **CKD 4–5, heart failure, secondary hypertension:** already under specialist care.
- Keep diabetics with autonomic neuropathy (ignore HRV) and shift workers (anchor "night" to sleep).

## 2. Is a warning clinically meaningful?

At 18% precision, four in five warnings are false; 1,000 healthy wearers trigger ~460 cuff series a year; 51% of converters are never warned.

**Useful only as a prompt to measure:** a false warning costs a week of readings, not a drug. Harms:
- **False reassurance** (largest: misses outnumber hits).
- **Overdiagnosis:** treating on the strap or one office reading.
- **Alarm fatigue:** suppress repeats for 3 months after a normal cuff series.
- **Anxiety:** modest with calm wording.

A 69-day lead is clinically trivial; risk builds over years. The value is **case-finding**: in Tunisia's 2019 May Measurement Month (11,271 screened), 27.5% of hypertensives were unaware and only 38.2% controlled [MMM-TN]. Compare against *usual care* and *an annual cuff check*.

**I would accept:** precision ≥30% in the enrolled group, ≤0.3 alarms per healthy person-year, sensitivity published (the cleared comparator: 41% sensitivity, 92% specificity [bayesian_ml-4]). Beating an annual cuff matters more than lead time.

## 3. Pathway

**WARNING → 7-day HBPM.** Use a validated upper-arm cuff (validatebp.org) sized to the arm; never a wrist cuff.
- Take **2 readings 1–2 minutes apart, morning and evening, for 3–7 days** (7 preferred) [ESC24-rev].
- 5 minutes seated, back supported, arm at heart level, silent; no caffeine, smoking or exercise for 30 minutes; mornings before breakfast and medication.
- Discard day 1, average the rest (≥12 readings); the app captures them by Bluetooth or photo.

What the mean means:
- **<130/80:** not confirmed. Repeat in 12 months.
- **130–134/80–84:** the team's label, below the ESC home threshold (≥135/85 [ESC24]). See a GP within 1–3 months for lifestyle advice and a CV risk check.
- **≥135/85:** see a GP within 2–4 weeks for work-up (eGFR, electrolytes, HbA1c, lipids, urine albumin, ECG).
- **≥160/100:** see a GP within 1 week.
- **≥180/110:** see section 5.

**ABPM only for discordance:** office and home disagree, HBPM is not feasible, or the strap keeps warning while home BP is normal (suspected **nocturnal hypertension**, ≥120/70 [ESC24]; night BP is the most prognostic [clinician-18]). Reserve it: in Tunisia it is mostly hospital or private.

**Tunisia:** many households won't buy a cuff; lend them via pharmacies or the CSB (public primary care). Pictorial instructions in Tunisian Arabic and French.

**INSUFFICIENT:** not a clean bill of health. Keep usual screening (every 3 years under 40, yearly from 40 [ESC24-rev]); after 8 weeks, prompt a cuff series.

**POOR_QUALITY:** fix fit, wear at night. After 4 weeks, **automatic cuff fallback** (a series now, then 6-monthly); this closes the 23% vs 5% skin-tone gap. **Irregular rhythm is never "poor quality".**

## 4. Patient messages

| State | English | Français |
|---|---|---|
| WARNING | "Your night-time signals have shifted from your usual pattern for several weeks; this is not a diagnosis, but please check your blood pressure with an arm cuff morning and evening for 7 days." | « Vos signaux nocturnes s'écartent de votre profil habituel depuis plusieurs semaines ; ce n'est pas un diagnostic, mais mesurez votre tension au bras matin et soir pendant 7 jours. » |
| INSUFFICIENT | "No conclusion yet: keep wearing the strap and keep your usual blood-pressure checks, because no alert does not mean normal blood pressure." | « Pas encore de conclusion : continuez à porter le bracelet et gardez vos contrôles de tension habituels, car l'absence d'alerte ne signifie pas une tension normale. » |
| POOR_QUALITY | "We do not have enough good-quality data to assess you; please check the fit, wear the strap at night and, if in doubt, measure your blood pressure with an arm cuff." | « Nous n'avons pas assez de données fiables pour vous évaluer ; vérifiez l'ajustement, portez le bracelet la nuit et, en cas de doute, mesurez votre tension au bras. » |

Never say "normal", "healthy" or "your heart is fine"; never show strap mmHg (cuffless validation standards are still lacking [ESC24]).

## 5. Red flags

The strap cannot see BP or an emergency. The symptom screen runs **independently of the model, in every state**:
- **Chest pain, sudden breathlessness, fainting, one-sided weakness, facial droop, speech trouble, sudden severe headache, sudden vision loss or confusion:** "Call 190 (SAMU) now. This strap cannot detect emergencies." / « Appelez le 190 (SAMU) immédiatement. Ce bracelet ne détecte pas les urgences. »
- **Cuff reading ≥180/110 on a repeat measurement:** with symptoms, call 190; without symptoms, see a doctor within 24 hours.
- **Pregnant or postpartum user** with headache, visual disturbance, swelling or a reading ≥140/90: same-day maternity review.
- **Irregular rhythm** (ECG spot-check or repeated PPG): GP within days for a 12-lead ECG (possible AF); 190 if chest pain or fainting.
- **Never use** "heart attack", "no arrhythmia detected" or "risk cleared".

## 6. Signals I would trust

1. **Night resting HR, sleep-anchored:** most robust; confounded by fitness, fever, alcohol, heat and **Ramadan** (needs a context flag).
2. **Steps:** reliable.
3. **Sleep duration and regularity:** acceptable; ignore wrist staging.
4. **Night RMSSD:** lowest weight. PPG pulse-rate variability is not true HRV, and RMSSD did not predict incident hypertension in HELIUS [ppg_scientist-28].
5. **ECG spot-check:** a rhythm gate only.

**Missing feature: obstructive sleep apnoea.** A leading secondary cause of nocturnal and resistant hypertension; it raises night HR, which the model will misread as "drift". Add a nocturnal desaturation index (red/IR PPG) plus STOP-BANG; a positive screen means a sleep study, not a BP warning.

## 7. Verdict

**Defensible as a "time to measure your blood pressure" prompt, not as an early-warning diagnostic.** An AUROC of 0.64 on synthetic data is weak.

1. **Narrow the population and add an annual-cuff null.** Report precision (≥30%) and alarms (≤0.3/person-year) there.
2. **Build the cuff loop in:** guided HBPM, GP thresholds, ABPM for discordance only, automatic cuff fallback (fixes the skin-tone gap), cuff lending.
3. **A model-independent safety layer:** red-flag screen in every state, rhythm separate from quality, a never-say list, Arabic/French/English messages tested with patients.

## References (retrieved, 2021+)

- [ESC24] McEvoy JW et al. 2024 ESC hypertension guidelines. *Eur Heart J* 2024;45:3912–4018. PMID 39210715 (full text fetched).
- [ESC24-rev] Burlacu A et al. *Medicina* 2025;61:193. DOI 10.3390/medicina61020193 (HBPM protocol, screening intervals).
- [MMM-TN] Haj Amor S et al. *Eur Heart J Suppl* 2021. DOI 10.1093/eurheartj/suab032.
- [bayesian_ml-4], [clinician-18], [ppg_scientist-28]: `debate/verdict/verdict.md` §5.
- Not cited (standard practice): 180/110, discarding day 1, SAMU 190, OSA.

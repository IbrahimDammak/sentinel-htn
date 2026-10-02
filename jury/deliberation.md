# Jury deliberation — team SENTINEL-HTN

## Scores (/10 per research question)

| RQ | Chair (academic) | Cardiologist | Industry CTO | ML researcher | **Mean** |
|---|---|---|---|---|---|
| RQ1 Personalization | 7 | 8 | 8 | 7 | **7.5** |
| RQ2 Temporal reasoning | 8 | 8 | 8 | 7 | **7.75** |
| RQ3 Early detection | 6 | 5 | 5 | 5 | **5.25** |
| RQ4 Context awareness | 6 | 6 | 7 | 5 | **6.0** |
| RQ5 Reliability | 6 | 7 | 6 | 6 | **6.25** |
| RQ6 Uncertainty | 5 | 8 | 8 | 5 | **6.5** |
| **Total /60** | **38** | **42** | **42** | **35** | **39.25** |

## Placement

**Consensus: a Top-3 contender, conditional on the missing deliverables.** Three jurors predict Top-3. The chair rates it "Finalist as it stands; Top-3 once the deck and repo are fixed".

- **Why it can place high:** it is the most credible methodology the jury expects in a student field. The random-alarm floor, the mandatory nulls, abstention counted as a miss, the fairness split and the honest "90 days = chance" result all match the brief's emphasis on credibility. All four jurors re-ran the code and found the paper's numbers match the results. No leakage was found.
- **Why it could lose a close call:** there is no slide deck. The paper and trend code are not on GitHub `main`. An AUROC of about 0.65 looks weak beside transformer entries. The evidence is circular: it comes from a simulator built with the model's own assumptions.

## Consensus findings (how many jurors raised each)

| Finding | Jurors |
|---|---|
| No slide deck; paper and trend code not committed/pushed to `main`; author block unfinished | 4/4 |
| Simulator circularity: context/personalization gains partly built in; no misspecification test; age, BMI and baseline BP unlinked to conversion, so "baselines at chance" is partly an artefact | 4/4 |
| The 30-day chance floor (0.301) is not produced by any committed code | 3/4 |
| RQ3: 90 days is at chance; the gain is about 1 month on compressed drift | 4/4 |
| RQ6: abstention is only a valid-day count; the band barely responds to data quality; "good calibration" overstated (Brier skill score ≈0.04–0.05) | 2/4 (chair, ML) |
| Noise doubles alarms; MCAR-30% raises alarms to 0.66 (not stated in the paper); 4× abstention in darker skin | 4/4 |
| Statistics: population SD over 3 seeds; no fresh seeds (a juror's fresh seeds give Se30 = 0.42) | 2/4 |
| Clinical: ESC home threshold ≥135/85, beta-blockers, AF, Ramadan fasting, red-flag number (SAMU 190) missing from intended use | 1/4 (cardiologist) |

## Must-fix list before submission (jury priority order)

1. **Deliverables:**
   - a ≤15-slide deck with a live demo of a WARNING and its evidence ledger;
   - commit the paper and the `rq3-trend` code, and push them to `main`;
   - fill in the authors;
   - compile the paper and confirm it is ≤5 pages.
2. **Reproducibility:** add the Se30 chance floor to `run.py`, commit a script that generates Table I, report sample SD and add fresh seeds 3–5.
3. **Defuse circularity:**
   - give the simulator realistic static risk (age, BMI and baseline BP linked to conversion), or drop the "baselines at chance" claim;
   - add a misspecification stress test: a different exercise threshold, a nonlinear temperature effect, and one unmodelled confounder such as sleep apnoea.
4. **Honest RQ6:** report the Brier skill score and a calibration slope instead of "good calibration". Either make the uncertainty band respond to data quality, or tone down the claim.
5. **Clinical intended use:** a sensitivity analysis at ESC ≥135/85; exclusions (treated HTN, AF, beta-blockers); Ramadan; a red-flag screen with the SAMU 190 number.

## Questions to prepare for the pitch Q&A
- What real-data result would falsify SENTINEL-HTN, and when will you run it?
- Can you beat a Framingham-type score plus an annual cuff check, which is what a Tunisian GP actually has?
- At 0.21 precision, how many cuff series and GP visits does one true warning cost, and who pays?
- Why build a strap instead of software for existing Fitbit, Samsung or Apple Health data?
- The trend was designed and scored on seeds 0–2, and fresh seeds give Se30 0.42. Which number is in the paper?
- Why call calibration "good" at a Brier skill score of about 0.04?

# BioVance AIoT Challenge — Final Judging Session (mock jury)

**Event:** BioVance, *An AIoT Challenge for Personalized Early Detection of Emerging Hypertension* (IEEE EMBS Tunisia Section; IEEE EMBS Student Branch, École Polytechnique de Sousse).

**Setting:** final judging day. The jury has a fixed review window per team, then a 10-minute pitch plus Q&A, then private deliberation. Teams are students; the field typically includes several strong ML entries (transformers, foundation models, dashboards). Judges must score each team independently before deliberating.

## Official task (from the challenge brief)
Design an AIoT early-warning system that goes **Learn → Detect → Predict → Warn**.
- It must learn a personal baseline, detect persistent (not isolated) deviations and account for context.
- It must be robust to noisy or incomplete IoT data, and abstain when evidence is insufficient.
- Required outputs: risk estimate, early-warning time, confidence/uncertainty, evidence (contributing factors) and a data-quality assessment.
- The challenge's own emphasis: *"Who developed the most credible scientific approach to detecting risk earlier, rather than just the most accurate model?"* and *"An extremely early but unreliable warning is not useful."*

## Official scoring (/60)

| Criterion | Question | Points |
|---|---|---|
| RQ1 Personalization | Personal baseline vs population variability? | 10 |
| RQ2 Temporal reasoning | Persistent change, not isolated readings? | 10 |
| RQ3 Early detection | How far ahead of clinical detection? | 10 |
| RQ4 Context awareness | Is the physiology changing, or just the situation? | 10 |
| RQ5 Reliability | Robust to noisy or incomplete IoT data? | 10 |
| RQ6 Uncertainty | Abstains when evidence is insufficient? | 10 |

**Evaluation framework the organisers named:**
- A. Predictive: AUROC, AUPRC, sensitivity, specificity, F1
- B. Early detection: lead time, % caught early
- C. False-alarm burden: alarms per individual, warning precision
- D. Calibration: Brier, ECE
- E. Robustness: missing modalities, noise, sensor failure
- F. Uncertainty quality: confidence drops when evidence is weak

## Required deliverables
1. **Research paper:** ≤5 pages, IEEE conference format. Sections: Abstract, Intro, Related Work, Methodology, System Architecture, Experiments, Results, Limitations, Conclusion, References.
2. **Presentation:** ≤15 slides.
3. **GitHub repository:** the code.

## The submission under review: team "SENTINEL-HTN"
Local folder `E:\bureau\cardiacAttackDetectionHakathon\` (judge the local state; the currently checked-out git branch is `rq3-trend`):
- **Paper:** `paper/main.tex` (IEEEtran source; not compiled because LaTeX isn't installed on this machine). The figures are `paper/figures/*.pdf`; render them to PNG with PyMuPDF (`import fitz`) if you want to see them.
- **Code:** `sentinel/`, `run.py`, `tests/test_pipeline.py`, `README.md`, `CONTRACT.md`. Run the tests with `python tests/test_pipeline.py` (~10 s). A full run is `python run.py --synthetic --n 1200 --seed 0 --out <tmpdir>` (~30 s).
- **Results:** `results/rq3_trend/seed*/` (final model), `results/summary_3seeds.md` (the earlier model without the trend features).
- **Supporting material (optional):**
  - `panel/`: cardiologist, hardware-engineer and AI-engineer reviews
  - `debate/verdict/verdict.md`: the team's design-selection verdict
  - `debate/audit/`: citation audits

**Known status:**
- There is no slide deck yet.
- All results are on the team's own synthetic cohort; the organisers' dataset was not available to them.
- The pushed GitHub `main` branch does not yet contain the paper or the trend features.

## Judging rules
- Score each RQ 0–10 **with evidence from the submission**: cite the file and section, or the number.
- Check the claims: run the test, and spot-check at least two numbers in the paper against `results/`.
- Judge scientific credibility as the brief asks, not only headline accuracy.
- Note deliverable compliance (page estimate, missing slides, repo state).
- Be a real judge: fair, specific and willing to be harsh. No flattery.

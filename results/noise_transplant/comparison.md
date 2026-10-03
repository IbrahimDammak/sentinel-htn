# Real noise in the evaluation: noise transplant + plasmode (sentinel/realnoise.py)

## 1. Noise transplant (full system, 3 seeds x 1,200 people x 540 days, same people/drifts/labels as the paper)

The AR(1) day-to-day noise is replaced by 14-day blocks of real LifeSnaps within-person residuals (67 people), drawn
jointly across channels and rescaled to the calibrated SD. What changes is the noise shape: heavy tails (excess
kurtosis up to 2.5 for steps and sleep) and real cross-channel correlation (night HR vs RMSSD -0.71; AR(1): 0).

| metric | AR(1) noise (paper) | transplanted real noise | per-seed difference |
|---|---|---|---|
| AUROC | 0.621 ± 0.014 | 0.623 ± 0.024 | +0.007 −0.030 +0.030 |
| AUPRC | 0.120 ± 0.020 | 0.107 ± 0.005 | −0.015 −0.028 +0.003 |
| Se30 (chance) | 0.322 (0.257) | 0.315 (0.250) | above chance 3/3 seeds in both |
| Se90 (chance) | 0.161 (0.206) | 0.169 (0.200) | above chance 1/3 seeds in both |
| median lead (days) | 61 | 56 | +8 −17 −6 (noisy, ~20 warned per seed) |
| alarms per non-converter person-year | 0.405 | 0.392 | |
| prompts/py with 26-week refractory | 0.254 | 0.250 | |
| KM first false prompt at 12 months | 0.228 | 0.211 | |
| warning precision | 0.209 | 0.196 | −0.011 −0.017 −0.013 |
| ECE | 0.006 | 0.003 | |
| abstention | 0.111 | 0.111 | |

Reading: the conclusions do not depend on the AR(1) noise assumption. Discrimination, the 30-day lead over chance,
calibration and alarm burden are unchanged within seed-to-seed variation; precision is ~0.01 lower in every seed.

## 2. Plasmode injection (Detect level): see results/plasmode/summary.md

| noise | people | detected after onset | false (no drift) |
|---|---|---|---|
| real LifeSnaps series (plasmode) | 18 | 0.31 | 0.06 |
| simulated, AR(1) noise | 276 | 0.77 | 0.24 |
| simulated, transplanted noise | 276 | 0.73 | 0.31 |

Reading: the same injected drift is detected far less often in real series. Transplanted noise alone barely moves the
simulated rate (0.77 -> 0.73), so the gap comes from what the transplant keeps simulated: real missingness and sparse
evaluable weeks (25% of LifeSnaps weeks are evaluable vs 71% simulated), which starve the 4-of-6-week persistence rule.
Only 18 LifeSnaps people have a ready baseline plus 6 weeks of follow-up, and the ramp is compressed to 28 days, so these
rates are indicative. The simulator is optimistic about data completeness, not about noise shape.

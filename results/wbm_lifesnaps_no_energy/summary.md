# Frozen WBM on LifeSnaps: linear probe

68 people, 606 person-weeks (>= 84 worn hours). 4 of 19 WBM (3 with --no-energy) channels filled (watch steps, distance, HR, active energy); iPhone, sleep and workout channels flagged missing. No BP labels: this checks only whether frozen WBM features carry person-level information on Fitbit data. Person = mean of their weekly 256-d embeddings.

Probe: standardise + L2 logistic (C by inner 3-fold CV), 20x repeated stratified 5-fold over people. AUROC = mean over repeats (SD over repeats is not a CI). p = label-permutation test, 200 permutations. Baseline = mean steps, distance, active energy (not with --no-energy), HR, HR 5th pct, HR SD.

**Variant --no-energy:** energy channel flagged missing (3 of 19 filled); baseline = hand features without energy (5).

| Label | n (pos) | hand AUROC | p | WBM-256 AUROC | p |
|---|---|---|---|---|---|
| age >= 30 (LifeSnaps band) | 65 (31) | 0.48 ± 0.05 | 0.507 | 0.43 ± 0.05 | 0.716 |
| sex = male | 66 (40) | 0.66 ± 0.07 | 0.015 | 0.76 ± 0.04 | 0.010 |
| BMI >= 25 | 65 (19) | 0.48 ± 0.04 | 0.488 | 0.53 ± 0.04 | 0.249 |

Domain shift: WBM was pretrained on Apple Watch + iPhone data with 19 channels; here it sees Fitbit data with 15 channels missing and harmonised units (energy scaled by one pooled factor, 8.95). Weak results would be expected and are not evidence against WBM.

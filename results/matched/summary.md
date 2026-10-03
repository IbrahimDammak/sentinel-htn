# Statistically matched LifeSnaps x PPG-BP cohort (exploratory, NOT validation)

65 LifeSnaps people; BP label (SBP >= 130 or DBP >= 80 mmHg on one PPG-BP cuff reading (ACC/AHA stage 1)) borrowed from a random PPG-BP donor of the same sex and age band among the 5 nearest in BMI; 20 imputations (prevalence 0.30). Different people: by construction wearables relate to BP only through sex, age band and BMI.

Probe: standardise + L2 logistic (C by inner 3-fold CV), 4x 5-fold per imputation. Wearables exclude the profile-derived energy channel (see results/wbm_lifesnaps_no_energy).

| Features | AUROC (mean ± SD over imputations) |
|---|---|
| demographics (age band, sex, BMI) | 0.73 ± 0.08 |
| wearable: hand5 | 0.43 ± 0.05 |
| wearable: WBM-256 | 0.44 ± 0.07 |
| demographics + hand5 | 0.70 ± 0.08 |
| demographics + WBM-256 | 0.58 ± 0.12 |

| Added to demographics | AUROC gain |
|---|---|
| hand5 | -0.034 ± 0.039 |
| WBM-256 | -0.148 ± 0.099 |

Reading: a wearable-only AUROC above 0.5 comes from wearables encoding sex/age/BMI (the matching variables), not from BP. The only meaningful number is the gain over demographics, which this design forces toward zero; it cannot show that wearables predict BP. Real paired data (OpenMHC) is required.

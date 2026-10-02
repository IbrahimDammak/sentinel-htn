# SENTINEL-HTN on the LifeSnaps-calibrated simulator (3 seeds, n=1,200 x 540 d; sample SD)

Before = optimistic simulator (results/rq3_trend). After = noise, autocorrelation, means and spreads calibrated on
LifeSnaps (results/lifesnaps/real_world.md), with the overfitting/calibration fixes in predict.fit.

| metric | before | after |
|---|---|---|
| auroc | 0.648 ± 0.035 | 0.604 ± 0.025 |
| auprc | 0.150 ± 0.027 | 0.104 ± 0.020 |
| sens_lead_0 | 0.590 ± 0.110 | 0.383 ± 0.118 |
| sens_lead_30 | 0.483 ± 0.096 | 0.255 ± 0.082 |
| sens_lead_90 | 0.190 ± 0.021 | 0.098 ± 0.051 |
| median_lead | 64.000 ± 5.292 | 54.333 ± 16.653 |
| alarms_per_nonconv_py | 0.493 ± 0.029 | 0.365 ± 0.096 |
| warning_precision | 0.211 ± 0.056 | 0.186 ± 0.041 |
| brier | 0.060 ± 0.006 | 0.060 ± 0.004 |
| ece | 0.006 ± 0.002 | 0.005 ± 0.001 |
| abstention_rate | 0.112 ± 0.010 | 0.110 ± 0.004 |

**Chance floor** (random warnings at 0.5/person-year): Se@0 0.334 ± 0.008, Se@30 0.306 ± 0.009, Se@90 0.247 ± 0.011

## Ablations (after)

| run | AUROC | AUPRC | Se@30 | Se@90 | alarms/py |
|---|---|---|---|---|---|
| full | 0.604 ± 0.025 | 0.104 ± 0.020 | 0.255 ± 0.082 | 0.098 ± 0.051 | 0.365 ± 0.096 |
| level_only | 0.537 ± 0.033 | 0.070 ± 0.007 | 0.124 ± 0.122 | 0.091 ± 0.086 | 0.197 ± 0.194 |
| cuff_only | 0.545 ± 0.020 | 0.074 ± 0.005 | 0.125 ± 0.108 | 0.091 ± 0.098 | 0.180 ± 0.132 |
| change_only | 0.594 ± 0.024 | 0.104 ± 0.018 | 0.319 ± 0.013 | 0.161 ± 0.042 | 0.390 ± 0.068 |
| no_personalisation | 0.558 ± 0.031 | 0.080 ± 0.016 | 0.200 ± 0.020 | 0.128 ± 0.037 | 0.409 ± 0.043 |
| no_context | 0.556 ± 0.017 | 0.081 ± 0.015 | 0.139 ± 0.066 | 0.099 ± 0.067 | 0.254 ± 0.106 |

Per-seed full AUROC: [0.612, 0.624, 0.577]; full > level_only and > cuff_only in every seed: True

# Channel weighting (evidence prior x label-free reliability) — 3 seeds, calibrated simulator

| metric | equal weights (results/calibrated) | weighted (results/weighted) |
|---|---|---|
| auroc | 0.604 ± 0.025 | 0.621 ± 0.014 |
| auprc | 0.104 ± 0.020 | 0.120 ± 0.020 |
| sens_lead_0 | 0.383 ± 0.118 | 0.481 ± 0.049 |
| sens_lead_30 | 0.255 ± 0.082 | 0.322 ± 0.051 |
| sens_lead_90 | 0.098 ± 0.051 | 0.161 ± 0.072 |
| median_lead | 54.333 ± 16.653 | 60.833 ± 8.505 |
| alarms_per_nonconv_py | 0.365 ± 0.096 | 0.405 ± 0.036 |
| warning_precision | 0.186 ± 0.041 | 0.209 ± 0.010 |
| brier | 0.060 ± 0.004 | 0.059 ± 0.004 |
| ece | 0.005 ± 0.001 | 0.006 ± 0.004 |
| abstention_rate | 0.110 ± 0.004 | 0.111 ± 0.004 |
| chance sens_lead_30 at weighted alarm rate | 0.232 ± 0.054 | 0.254 ± 0.021 (model above chance in 3/3 seeds) |
| chance sens_lead_90 at weighted alarm rate | 0.186 ± 0.044 | 0.204 ± 0.018 (model above chance in 1/3 seeds) |

## Ablations (weighted run)

| run | AUROC | AUPRC | Se@30 | Se@90 | alarms/py |
|---|---|---|---|---|---|
| full (weighted) | 0.621 ± 0.014 | 0.120 ± 0.020 | 0.322 ± 0.051 | 0.161 ± 0.072 | 0.405 ± 0.036 |
| level_only | 0.537 ± 0.033 | 0.070 ± 0.007 | 0.124 ± 0.122 | 0.083 ± 0.086 | 0.174 ± 0.152 |
| cuff_only | 0.545 ± 0.020 | 0.074 ± 0.005 | 0.149 ± 0.137 | 0.099 ± 0.111 | 0.236 ± 0.188 |
| change_only | 0.620 ± 0.007 | 0.121 ± 0.015 | 0.324 ± 0.083 | 0.154 ± 0.037 | 0.456 ± 0.107 |
| no_personalisation | 0.567 ± 0.038 | 0.083 ± 0.019 | 0.190 ± 0.048 | 0.120 ± 0.009 | 0.372 ± 0.041 |
| no_context | 0.550 ± 0.022 | 0.078 ± 0.010 | 0.193 ± 0.046 | 0.138 ± 0.043 | 0.357 ± 0.054 |
| equal_weights | 0.605 ± 0.024 | 0.104 ± 0.020 | 0.248 ± 0.084 | 0.105 ± 0.040 | 0.360 ± 0.101 |
| reliability_only | 0.609 ± 0.021 | 0.107 ± 0.020 | 0.249 ± 0.122 | 0.130 ± 0.080 | 0.360 ± 0.141 |

Per seed AUROC  weighted: [0.632, 0.626, 0.606]  equal: [0.613, 0.624, 0.577]
Per seed AUPRC  weighted: [0.126, 0.137, 0.098]  equal: [0.109, 0.121, 0.082]

## Normalised channel weights (share of total), per seed

- night_rhr 0.24, night_rmssd 0.21, still_hr 0.06, steps 0.20, sleep_dur 0.24, sleep_reg 0.05  | trend_r 0.101
- night_rhr 0.25, night_rmssd 0.21, still_hr 0.06, steps 0.20, sleep_dur 0.24, sleep_reg 0.05  | trend_r 0.097
- night_rhr 0.24, night_rmssd 0.22, still_hr 0.06, steps 0.20, sleep_dur 0.23, sleep_reg 0.05  | trend_r 0.098

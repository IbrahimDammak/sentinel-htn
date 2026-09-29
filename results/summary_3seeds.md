# SENTINEL-HTN — synthetic results over 3 seeds

n=1,200 people × 540 days per seed; 240 held-out test people per seed (41–47 converters). Synthetic data — not clinical evidence.

Tuned thresholds per seed: [{'thr': 0.1, 'thr_p': 0.115}, {'thr': 0.1, 'thr_p': 0.12}, {'thr': 0.1, 'thr_p': 0.125}]

## Main model (mean ± SD)

| metric | value |
|---|---|
| auroc | 0.638 ± 0.041 |
| auprc | 0.132 ± 0.018 |
| sens_lead_0 | 0.489 ± 0.101 |
| sens_lead_30 | 0.334 ± 0.074 |
| sens_lead_90 | 0.203 ± 0.052 |
| sens_lead_180 | 0.135 ± 0.048 |
| median_lead | 68.833 ± 20.778 |
| alarms_per_nonconv_py | 0.463 ± 0.020 |
| warning_precision | 0.182 ± 0.052 |
| brier | 0.060 ± 0.005 |
| ece | 0.006 ± 0.004 |
| aurc | 0.041 ± 0.006 |
| abstention_rate | 0.110 ± 0.008 |

## Ablations (mean ± SD)

| run | auroc | auprc | sens_lead_90 | alarms_per_nonconv_py | warning_precision |
|---|---|---|---|---|---|
| full | 0.638 ± 0.041 | 0.132 ± 0.018 | 0.203 ± 0.052 | 0.463 ± 0.020 | 0.182 ± 0.052 |
| level_only | 0.578 ± 0.025 | 0.083 ± 0.003 | 0.219 ± 0.051 | 0.372 ± 0.069 | 0.153 ± 0.022 |
| cuff_only | 0.561 ± 0.022 | 0.080 ± 0.010 | 0.205 ± 0.048 | 0.441 ± 0.080 | 0.143 ± 0.024 |
| change_only | 0.630 ± 0.042 | 0.121 ± 0.019 | 0.133 ± 0.072 | 0.496 ± 0.062 | 0.218 ± 0.069 |
| no_personalisation | 0.609 ± 0.007 | 0.092 ± 0.008 | 0.191 ± 0.047 | 0.372 ± 0.047 | 0.114 ± 0.029 |
| no_context | 0.608 ± 0.010 | 0.094 ± 0.003 | 0.169 ± 0.033 | 0.405 ± 0.080 | 0.182 ± 0.033 |

## Robustness — test data degraded, models fitted on clean data (mean ± SD)

| run | auroc | sens_lead_90 | alarms_per_nonconv_py | warning_precision | abstention_rate |
|---|---|---|---|---|---|
| mcar_0.3 | 0.618 ± 0.025 | 0.237 ± 0.055 | 0.601 ± 0.005 | 0.172 ± 0.027 | 0.110 ± 0.008 |
| mcar_0.6 | 0.587 ± 0.006 | 0.185 ± 0.041 | 0.481 ± 0.050 | 0.109 ± 0.045 | 0.141 ± 0.008 |
| noise_1.0 | 0.570 ± 0.029 | 0.362 ± 0.092 | 1.028 ± 0.094 | 0.113 ± 0.021 | 0.111 ± 0.008 |
| drop_night_rmssd | 0.626 ± 0.031 | 0.199 ± 0.015 | 0.492 ± 0.012 | 0.145 ± 0.037 | 0.110 ± 0.008 |
| mnar_0.4 | 0.598 ± 0.015 | 0.082 ± 0.034 | 0.321 ± 0.027 | 0.166 ± 0.040 | 0.331 ± 0.009 |
| sensor_fail_0.3 | 0.626 ± 0.021 | 0.082 ± 0.033 | 0.196 ± 0.026 | 0.202 ± 0.037 | 0.519 ± 0.006 |

## Fairness by skin-tone (ITA) tercile (mean ± SD; darker skin = lowest tercile)

| tercile | auroc | sens_lead_0 | sens_lead_90 | abstention_rate |
|---|---|---|---|---|
| T1 | 0.646 ± 0.055 | 0.467 ± 0.169 | 0.151 ± 0.059 | 0.228 ± 0.016 |
| T2 | 0.618 ± 0.050 | 0.426 ± 0.082 | 0.186 ± 0.059 | 0.056 ± 0.005 |
| T3 | 0.658 ± 0.030 | 0.565 ± 0.051 | 0.277 ± 0.070 | 0.049 ± 0.003 |

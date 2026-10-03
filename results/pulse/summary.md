# SENTINEL-HTN: main model (pulse OFF) and the with_pulse variant: 3 seeds (seed0, seed1, seed2), mean ± SD over seeds

Synthetic cohort (calibrated simulator). with_pulse adds the optional pulse_htn channel (the embedding-drift channel pulse_drift was removed after the audit: non-directional, near-zero simulated signal). Its within-person BP coupling (0.0092 night SD per mmHg here, the cross-sectional slope, an UPPER bound) and night-to-night noise are ASSUMPTIONS (CONTRACT.md). The zero-coupling arm is in coupling_sweep.md and must be read with every with_pulse number.

**Result: no improvement from the pulse channel** (decision rule, set after the own-operating-point results were known: with_pulse above main in every seed for AUROC and for Se30 and Se90 at main's realised alarm rate, budget 0.5). Separately tuned thresholds put the two arms at different alarm rates, so a lower alarm rate or a higher cumulative specificity for with_pulse at its own operating point is an operating-point shift, not better separation; compare the arms at matched alarm rates below.

## with_pulse vs main at matched alarm rates (operating curve)

For each warning budget (thresholds tuned on calibration people), main's realised test alarm rate is the reference; with_pulse's sensitivity is read off its own operating curve at that rate (linear interpolation, 0 alarms = 0). Se0 = warned before t_ref; Se30 / Se90 = warned >= 30 / 90 days before t_ref.

| budget | realised alarms/py: main; with_pulse | metric | main | with_pulse at main's rate | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |
|---|---|---|---|---|---|---|---|
| 0.25 | 0.187 ± 0.057; 0.174 ± 0.031 | sens_lead_0 | 0.304 ± 0.074 | 0.286 ± 0.113 | +0.018 +0.000 -0.073 | -0.018 ± 0.048 | 1/3 |
| 0.25 | 0.187 ± 0.057; 0.174 ± 0.031 | sens_lead_30 | 0.159 ± 0.059 | 0.165 ± 0.102 | +0.053 +0.000 -0.034 | 0.006 ± 0.043 | 1/3 |
| 0.25 | 0.187 ± 0.057; 0.174 ± 0.031 | sens_lead_90 | 0.080 ± 0.016 | 0.104 ± 0.083 | +0.101 +0.000 -0.031 | 0.023 ± 0.069 | 1/3 |
| 0.5 | 0.405 ± 0.036; 0.387 ± 0.014 | sens_lead_0 | 0.481 ± 0.049 | 0.453 ± 0.073 | -0.011 -0.064 -0.008 | -0.028 ± 0.032 | 0/3 |
| 0.5 | 0.405 ± 0.036; 0.387 ± 0.014 | sens_lead_30 | 0.322 ± 0.051 | 0.313 ± 0.075 | -0.003 -0.041 +0.017 | -0.009 ± 0.029 | 1/3 |
| 0.5 | 0.405 ± 0.036; 0.387 ± 0.014 | sens_lead_90 | 0.161 ± 0.072 | 0.165 ± 0.100 | +0.035 -0.020 -0.002 | 0.004 ± 0.028 | 1/3 |
| 1.0 | 0.833 ± 0.049; 0.811 ± 0.073 | sens_lead_0 | 0.611 ± 0.072 | 0.620 ± 0.094 | +0.043 -0.033 +0.018 | 0.009 ± 0.039 | 2/3 |
| 1.0 | 0.833 ± 0.049; 0.811 ± 0.073 | sens_lead_30 | 0.490 ± 0.066 | 0.515 ± 0.060 | +0.088 -0.017 +0.004 | 0.025 ± 0.056 | 2/3 |
| 1.0 | 0.833 ± 0.049; 0.811 ± 0.073 | sens_lead_90 | 0.282 ± 0.052 | 0.288 ± 0.087 | +0.044 -0.030 +0.004 | 0.006 ± 0.037 | 2/3 |
| 2.0 | 1.298 ± 0.260; 1.398 ± 0.117 | sens_lead_0 | 0.727 ± 0.102 | 0.722 ± 0.071 | +0.030 -0.022 -0.026 | -0.006 ± 0.031 | 1/3 |
| 2.0 | 1.298 ± 0.260; 1.398 ± 0.117 | sens_lead_30 | 0.623 ± 0.139 | 0.633 ± 0.079 | +0.079 +0.000 -0.051 | 0.009 ± 0.066 | 1/3 |
| 2.0 | 1.298 ± 0.260; 1.398 ± 0.117 | sens_lead_90 | 0.461 ± 0.085 | 0.446 ± 0.076 | +0.005 -0.022 -0.026 | -0.014 ± 0.017 | 1/3 |

## Main model and ablations (with_pulse = main + pulse_htn), each at its own operating point

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| main (no pulse) | 0.621 ± 0.014 | 0.120 ± 0.020 | 0.191 ± 0.026 | 0.481 ± 0.049 | 0.322 ± 0.051 | 0.161 ± 0.072 | 60.833 ± 8.505 | 0.405 ± 0.036 | 0.209 ± 0.010 | 0.658 ± 0.042 | 0.308 ± 0.009 | 0.059 ± 0.004 | 0.006 ± 0.004 | 0.044 ± 0.003 | 0.111 ± 0.004 |
| level_only | 0.537 ± 0.033 | 0.070 ± 0.007 | 0.041 ± 0.038 | 0.199 ± 0.178 | 0.124 ± 0.122 | 0.083 ± 0.086 | n/a | 0.174 ± 0.152 | n/a | 0.856 ± 0.126 | 0.166 ± 0.147 | 0.060 ± 0.005 | 0.001 ± 0.001 | 0.056 ± 0.008 | 0.109 ± 0.005 |
| cuff_only | 0.545 ± 0.020 | 0.074 ± 0.005 | 0.084 ± 0.010 | 0.248 ± 0.234 | 0.149 ± 0.137 | 0.099 ± 0.111 | n/a | 0.236 ± 0.188 | 0.106 ± 0.093 | 0.791 ± 0.155 | 0.172 ± 0.154 | 0.060 ± 0.005 | 0.001 ± 0.001 | 0.057 ± 0.004 | 0.110 ± 0.005 |
| change_only | 0.620 ± 0.007 | 0.121 ± 0.015 | 0.196 ± 0.016 | 0.468 ± 0.093 | 0.324 ± 0.083 | 0.154 ± 0.037 | 60.000 ± 11.533 | 0.456 ± 0.107 | 0.189 ± 0.027 | 0.602 ± 0.084 | 0.276 ± 0.030 | 0.059 ± 0.004 | 0.004 ± 0.003 | 0.047 ± 0.001 | 0.111 ± 0.005 |
| no_personalisation | 0.567 ± 0.038 | 0.083 ± 0.019 | 0.108 ± 0.040 | 0.297 ± 0.033 | 0.190 ± 0.048 | 0.120 ± 0.009 | 57.333 ± 26.312 | 0.372 ± 0.041 | 0.145 ± 0.034 | 0.737 ± 0.022 | 0.232 ± 0.016 | 0.060 ± 0.005 | 0.004 ± 0.002 | 0.047 ± 0.003 | 0.111 ± 0.005 |
| no_context | 0.550 ± 0.022 | 0.078 ± 0.010 | 0.081 ± 0.023 | 0.346 ± 0.051 | 0.193 ± 0.046 | 0.138 ± 0.043 | 39.333 ± 17.502 | 0.357 ± 0.054 | 0.158 ± 0.009 | 0.720 ± 0.063 | 0.260 ± 0.048 | 0.060 ± 0.005 | 0.002 ± 0.001 | 0.053 ± 0.008 | 0.110 ± 0.004 |
| equal_weights | 0.605 ± 0.024 | 0.104 ± 0.020 | 0.162 ± 0.027 | 0.376 ± 0.121 | 0.248 ± 0.084 | 0.105 ± 0.040 | 57.667 ± 16.042 | 0.360 ± 0.101 | 0.185 ± 0.040 | 0.691 ± 0.065 | 0.260 ± 0.054 | 0.060 ± 0.004 | 0.005 ± 0.001 | 0.046 ± 0.003 | 0.110 ± 0.004 |
| reliability_only | 0.609 ± 0.021 | 0.107 ± 0.020 | 0.169 ± 0.036 | 0.354 ± 0.138 | 0.249 ± 0.122 | 0.130 ± 0.080 | 58.000 ± 20.075 | 0.360 ± 0.141 | 0.180 ± 0.039 | 0.704 ± 0.103 | 0.250 ± 0.047 | 0.060 ± 0.004 | 0.005 ± 0.001 | 0.045 ± 0.004 | 0.110 ± 0.005 |
| with_pulse | 0.619 ± 0.013 | 0.120 ± 0.021 | 0.191 ± 0.033 | 0.451 ± 0.068 | 0.308 ± 0.074 | 0.162 ± 0.094 | 60.333 ± 28.184 | 0.387 ± 0.014 | 0.195 ± 0.012 | 0.670 ± 0.049 | 0.296 ± 0.007 | 0.059 ± 0.004 | 0.005 ± 0.003 | 0.044 ± 0.003 | 0.111 ± 0.004 |

## with_pulse minus main at their own operating points (NOT alarm-matched), per seed

| metric | main (no pulse) | with_pulse | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |
|---|---|---|---|---|---|
| auroc | 0.621 ± 0.014 | 0.619 ± 0.013 | -0.003 -0.001 -0.001 | -0.002 ± 0.001 | 0/3 |
| auprc | 0.120 ± 0.020 | 0.120 ± 0.021 | +0.005 -0.005 -0.003 | -0.001 ± 0.005 | 1/3 |
| sens_spec92 | 0.191 ± 0.026 | 0.191 ± 0.033 | +0.009 -0.008 +0.000 | 0.000 ± 0.008 | 1/3 |
| sens_lead_0 | 0.481 ± 0.049 | 0.451 ± 0.068 | -0.024 -0.067 +0.000 | -0.030 ± 0.034 | 0/3 |
| sens_lead_30 | 0.322 ± 0.051 | 0.308 ± 0.074 | -0.024 -0.044 +0.026 | -0.014 ± 0.036 | 1/3 |
| sens_lead_90 | 0.161 ± 0.072 | 0.162 ± 0.094 | +0.024 -0.022 +0.000 | 0.001 ± 0.023 | 1/3 |
| median_lead | 60.833 ± 8.505 | 60.333 ± 28.184 | +22.500 -14.500 -9.500 | -0.500 ± 20.075 | 1/3 |
| alarms_per_nonconv_py | 0.405 ± 0.036 | 0.387 ± 0.014 | -0.054 -0.007 +0.007 | -0.018 ± 0.032 | 1/3 |
| warning_precision | 0.209 ± 0.010 | 0.195 ± 0.012 | -0.014 -0.011 -0.017 | -0.014 ± 0.003 | 0/3 |
| specificity | 0.658 ± 0.042 | 0.670 ± 0.049 | +0.010 +0.036 -0.010 | 0.012 ± 0.023 | 2/3 |
| f1 | 0.308 ± 0.009 | 0.296 ± 0.007 | -0.008 -0.024 -0.005 | -0.012 ± 0.011 | 0/3 |
| brier | 0.059 ± 0.004 | 0.059 ± 0.004 | -0.000 +0.000 +0.000 | -0.000 ± 0.000 | 2/3 |
| ece | 0.006 ± 0.004 | 0.005 ± 0.003 | +0.000 -0.002 +0.000 | -0.001 ± 0.001 | 2/3 |
| aurc | 0.044 ± 0.003 | 0.044 ± 0.003 | +0.000 +0.001 +0.000 | 0.000 ± 0.000 | 3/3 |
| abstention_rate | 0.111 ± 0.004 | 0.111 ± 0.004 | -0.000 -0.000 +0.000 | -0.000 ± 0.000 | 1/3 |

## False prompts over time (non-converters, test people)

Day 0 = first landmark week (after the personal-baseline warm-up). false_prompt_6mo / 12mo = Kaplan-Meier probability of >= 1 false prompt by 6 / 12 months of monitoring, censored at end of follow-up. specificity = non-converters never prompted, CUMULATIVE over the median follow-up (followup_median_days), not a single-window specificity. ppv_person = person-level PPV of a prompt at the test conversion rate (0.173 ± 0.013); lr_pos = Se0 / share of non-converters prompted. alarms_per_nonconv_py divides by calendar time (warm-up included), alarms_per_nonconv_monitored_py by monitored, post-warm-up time.

prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year with repeat suppression: a 26-week refractory period after each prompt (not the clinical panel's rule, which was 13 weeks after a normal cuff series), because 26 weeks is the prediction horizon. It is a BURDEN metric only: first warnings are unchanged (asserted in evaluate.metrics), and every other metric, the tuned thresholds and the operating curve's chance floor use the unsuppressed episodes.

| metric | main (no pulse) | with_pulse | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |
|---|---|---|---|---|---|
| false_prompt_6mo | 0.095 ± 0.029 | 0.095 ± 0.040 | -0.005 -0.010 +0.015 | -0.000 ± 0.013 | 1/3 |
| false_prompt_12mo | 0.228 ± 0.028 | 0.221 ± 0.038 | -0.005 -0.036 +0.020 | -0.007 ± 0.028 | 1/3 |
| followup_median_days | 504.000 ± 0.000 | 504.000 ± 0.000 | +0.000 +0.000 +0.000 | 0.000 ± 0.000 | 0/3 |
| specificity | 0.658 ± 0.042 | 0.670 ± 0.049 | +0.010 +0.036 -0.010 | 0.012 ± 0.023 | 2/3 |
| false_prompts_per_nonconv | 0.599 ± 0.053 | 0.573 ± 0.021 | -0.080 -0.010 +0.010 | -0.027 ± 0.047 | 1/3 |
| ppv_person | 0.228 ± 0.014 | 0.222 ± 0.012 | -0.004 -0.008 -0.005 | -0.006 ± 0.002 | 0/3 |
| lr_pos | 1.410 ± 0.042 | 1.367 ± 0.040 | -0.028 -0.058 -0.044 | -0.044 ± 0.015 | 0/3 |
| alarms_per_nonconv_py | 0.405 ± 0.036 | 0.387 ± 0.014 | -0.054 -0.007 +0.007 | -0.018 ± 0.032 | 1/3 |
| alarms_per_nonconv_monitored_py | 0.437 ± 0.040 | 0.418 ± 0.016 | -0.058 -0.007 +0.007 | -0.020 ± 0.034 | 1/3 |
| prompts_per_nonconv_py_r26 | 0.254 ± 0.032 | 0.247 ± 0.042 | +0.000 -0.024 +0.003 | -0.007 ± 0.015 | 1/3 |

## Pre-onset warnings (simulator: drift onset known)

sens_post_onset_30/90 = Se30/Se90 counting a converter whose first warning came BEFORE the simulated drift onset as a miss (an added sensitivity analysis; sens_lead_* are unchanged and count every warning before t_ref). n_pre_onset_first_warnings = converters whose first warning preceded onset.

| metric | main (no pulse) | with_pulse | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |
|---|---|---|---|---|---|
| sens_lead_30 | 0.322 ± 0.051 | 0.308 ± 0.074 | -0.024 -0.044 +0.026 | -0.014 ± 0.036 | 1/3 |
| sens_post_onset_30 | 0.281 ± 0.036 | 0.259 ± 0.054 | -0.049 -0.044 +0.026 | -0.023 ± 0.042 | 1/3 |
| sens_lead_90 | 0.161 ± 0.072 | 0.162 ± 0.094 | +0.024 -0.022 +0.000 | 0.001 ± 0.023 | 1/3 |
| sens_post_onset_90 | 0.120 ± 0.065 | 0.113 ± 0.071 | +0.000 -0.022 +0.000 | -0.007 ± 0.013 | 0/3 |
| n_pre_onset_first_warnings | 1.667 ± 0.577 | 2.333 ± 1.528 | +2.000 +0.000 +0.000 | 0.667 ± 1.155 | 1/3 |

## Robustness (test people perturbed; with_pulse_drop_pulse = with_pulse model, pulse removed at test time)

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.621 ± 0.014 | 0.120 ± 0.020 | 0.191 ± 0.026 | 0.481 ± 0.049 | 0.322 ± 0.051 | 0.161 ± 0.072 | 60.833 ± 8.505 | 0.405 ± 0.036 | 0.209 ± 0.010 | 0.658 ± 0.042 | 0.308 ± 0.009 | 0.059 ± 0.004 | 0.006 ± 0.004 | 0.044 ± 0.003 | 0.111 ± 0.004 |
| mcar_0.3 | 0.592 ± 0.019 | 0.101 ± 0.020 | 0.197 ± 0.037 | 0.486 ± 0.100 | 0.366 ± 0.104 | 0.194 ± 0.109 | 79.333 ± 17.388 | 0.505 ± 0.042 | 0.158 ± 0.032 | 0.543 ± 0.016 | 0.264 ± 0.050 | 0.060 ± 0.004 | 0.005 ± 0.003 | 0.048 ± 0.002 | 0.111 ± 0.004 |
| mcar_0.6 | 0.557 ± 0.009 | 0.083 ± 0.009 | 0.198 ± 0.070 | 0.313 ± 0.050 | 0.266 ± 0.060 | 0.186 ± 0.056 | 103.167 ± 22.805 | 0.472 ± 0.036 | 0.096 ± 0.015 | 0.573 ± 0.035 | 0.186 ± 0.015 | 0.062 ± 0.004 | 0.017 ± 0.006 | 0.053 ± 0.003 | 0.143 ± 0.006 |
| noise_1.0 | 0.600 ± 0.022 | 0.099 ± 0.015 | 0.244 ± 0.046 | 0.515 ± 0.094 | 0.435 ± 0.078 | 0.266 ± 0.060 | 92.667 ± 13.051 | 0.722 ± 0.072 | 0.129 ± 0.003 | 0.443 ± 0.061 | 0.244 ± 0.015 | 0.060 ± 0.004 | 0.008 ± 0.005 | 0.046 ± 0.005 | 0.112 ± 0.005 |
| drop_night_rmssd | 0.604 ± 0.020 | 0.103 ± 0.022 | 0.162 ± 0.035 | 0.392 ± 0.066 | 0.263 ± 0.031 | 0.144 ± 0.023 | 65.333 ± 9.292 | 0.415 ± 0.059 | 0.169 ± 0.019 | 0.647 ± 0.045 | 0.253 ± 0.030 | 0.060 ± 0.004 | 0.006 ± 0.002 | 0.046 ± 0.003 | 0.111 ± 0.004 |
| mnar_0.4 | 0.597 ± 0.049 | 0.121 ± 0.052 | 0.153 ± 0.061 | 0.240 ± 0.088 | 0.201 ± 0.101 | 0.105 ± 0.057 | 78.833 ± 20.978 | 0.246 ± 0.067 | 0.184 ± 0.074 | 0.781 ± 0.043 | 0.233 ± 0.085 | 0.059 ± 0.005 | 0.009 ± 0.004 | 0.044 ± 0.003 | 0.314 ± 0.028 |
| sensor_fail_0.3 | 0.599 ± 0.036 | 0.116 ± 0.020 | 0.147 ± 0.086 | 0.267 ± 0.133 | 0.203 ± 0.105 | 0.066 ± 0.039 | 52.667 ± 10.693 | 0.171 ± 0.017 | 0.208 ± 0.060 | 0.813 ± 0.025 | 0.239 ± 0.092 | 0.062 ± 0.004 | 0.013 ± 0.004 | 0.048 ± 0.003 | 0.518 ± 0.013 |
| with_pulse_drop_pulse | 0.619 ± 0.015 | 0.119 ± 0.020 | 0.202 ± 0.024 | 0.483 ± 0.073 | 0.332 ± 0.095 | 0.178 ± 0.104 | 67.167 ± 31.533 | 0.406 ± 0.037 | 0.192 ± 0.014 | 0.653 ± 0.026 | 0.306 ± 0.018 | 0.059 ± 0.004 | 0.005 ± 0.005 | 0.044 ± 0.003 | 0.111 ± 0.004 |

## By skin_ita tercile, main model (T1 = lowest; edges differ per seed)

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 80.000 ± 0.000 | 15.667 ± 6.658 | 0.584 ± 0.085 | 0.132 ± 0.096 | 0.128 ± 0.038 | 0.368 ± 0.114 | 0.210 ± 0.132 | 0.091 ± 0.079 | 61.000 ± 30.512 | 0.312 ± 0.054 | 0.225 ± 0.097 | 0.713 ± 0.052 | 0.278 ± 0.097 | 0.070 ± 0.028 | 0.026 ± 0.019 | 0.055 ± 0.012 | 0.234 ± 0.005 |
| T2 | 80.000 ± 0.000 | 12.667 ± 2.309 | 0.633 ± 0.048 | 0.125 ± 0.032 | 0.214 ± 0.064 | 0.500 ± 0.000 | 0.348 ± 0.058 | 0.119 ± 0.149 | 70.667 ± 32.624 | 0.420 ± 0.064 | 0.205 ± 0.050 | 0.654 ± 0.037 | 0.299 ± 0.050 | 0.055 ± 0.010 | 0.014 ± 0.010 | 0.034 ± 0.006 | 0.059 ± 0.003 |
| T3 | 80.667 ± 0.577 | 13.333 ± 3.215 | 0.651 ± 0.046 | 0.147 ± 0.075 | 0.234 ± 0.055 | 0.579 ± 0.187 | 0.409 ± 0.106 | 0.234 ± 0.103 | 72.333 ± 38.750 | 0.478 ± 0.118 | 0.196 ± 0.079 | 0.612 ± 0.083 | 0.326 ± 0.105 | 0.055 ± 0.014 | 0.017 ± 0.002 | 0.043 ± 0.010 | 0.045 ± 0.001 |

## By age tercile, main model (T1 = lowest; edges differ per seed): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 82.333 ± 3.215 | 15.667 ± 3.215 | 0.623 ± 0.031 | 0.147 ± 0.037 | 0.152 ± 0.038 | 0.397 ± 0.057 | 0.206 ± 0.113 | 0.083 ± 0.083 | 43.500 ± 29.787 | 0.311 ± 0.103 | 0.258 ± 0.047 | 0.727 ± 0.080 | 0.312 ± 0.048 | 0.066 ± 0.013 | 0.014 ± 0.012 | 0.047 ± 0.017 | 0.115 ± 0.021 |
| T2 | 79.333 ± 4.041 | 13.000 ± 3.606 | 0.653 ± 0.010 | 0.156 ± 0.043 | 0.256 ± 0.015 | 0.560 ± 0.063 | 0.495 ± 0.064 | 0.266 ± 0.061 | 87.833 ± 14.003 | 0.405 ± 0.005 | 0.196 ± 0.081 | 0.650 ± 0.026 | 0.332 ± 0.090 | 0.057 ± 0.016 | 0.020 ± 0.002 | 0.041 ± 0.007 | 0.105 ± 0.014 |
| T3 | 79.000 ± 2.000 | 13.000 ± 1.732 | 0.591 ± 0.092 | 0.091 ± 0.040 | 0.165 ± 0.056 | 0.478 ± 0.146 | 0.281 ± 0.007 | 0.143 ± 0.143 | 51.667 ± 29.263 | 0.505 ± 0.023 | 0.180 ± 0.047 | 0.595 ± 0.022 | 0.270 ± 0.085 | 0.056 ± 0.009 | 0.011 ± 0.006 | 0.045 ± 0.003 | 0.112 ± 0.018 |

## Normalised channel weights (weights), per seed

- night_rhr 0.24, night_rmssd 0.21, still_hr 0.06, steps 0.20, sleep_dur 0.24, sleep_reg 0.05
- night_rhr 0.25, night_rmssd 0.21, still_hr 0.06, steps 0.20, sleep_dur 0.24, sleep_reg 0.05
- night_rhr 0.24, night_rmssd 0.22, still_hr 0.06, steps 0.20, sleep_dur 0.23, sleep_reg 0.05

## Normalised channel weights (weights_with_pulse), per seed

- night_rhr 0.22, night_rmssd 0.19, still_hr 0.05, steps 0.18, sleep_dur 0.21, sleep_reg 0.04, pulse_htn 0.11
- night_rhr 0.22, night_rmssd 0.19, still_hr 0.05, steps 0.18, sleep_dur 0.21, sleep_reg 0.04, pulse_htn 0.11
- night_rhr 0.21, night_rmssd 0.20, still_hr 0.06, steps 0.18, sleep_dur 0.21, sleep_reg 0.04, pulse_htn 0.11

Example with_pulse ledger (seed0, P0068 week 38): channel_contrib (mean weekly z, last 6 weeks) night_rhr 0.685, night_rmssd 0.095, still_hr -0.525, steps -0.481, sleep_dur 0.051, sleep_reg 0.512, pulse_htn 0.122

## Default-off invariant: every value shared with results/weighted/<seed>/metrics.json

- seed0: main identical; 340 shared values, all identical
- seed1: main identical; 340 shared values, all identical
- seed2: main identical; 340 shared values, all identical

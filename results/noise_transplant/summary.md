# SENTINEL-HTN: main model (pulse OFF) and the with_pulse variant: 3 seeds (seed0, seed1, seed2), mean ± SD over seeds

Synthetic cohort (calibrated simulator). with_pulse adds the optional pulse_htn channel (the embedding-drift channel pulse_drift was removed after the audit: non-directional, near-zero simulated signal). Its within-person BP coupling (0.0092 night SD per mmHg here, the cross-sectional slope, an UPPER bound) and night-to-night noise are ASSUMPTIONS (CONTRACT.md). The zero-coupling arm is in coupling_sweep.md and must be read with every with_pulse number.

**Result: no improvement from the pulse channel** (decision rule, set after the own-operating-point results were known: with_pulse above main in every seed for AUROC and for Se30 and Se90 at main's realised alarm rate, budget 0.5). Separately tuned thresholds put the two arms at different alarm rates, so a lower alarm rate or a higher cumulative specificity for with_pulse at its own operating point is an operating-point shift, not better separation; compare the arms at matched alarm rates below.

## with_pulse vs main at matched alarm rates (operating curve)

For each warning budget (thresholds tuned on calibration people), main's realised test alarm rate is the reference; with_pulse's sensitivity is read off its own operating curve at that rate (linear interpolation, 0 alarms = 0). Se0 = warned before t_ref; Se30 / Se90 = warned >= 30 / 90 days before t_ref.

| budget | realised alarms/py: main; with_pulse | metric | main | with_pulse at main's rate | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |
|---|---|---|---|---|---|---|---|
| 0.25 | 0.201 ± 0.069; 0.192 ± 0.095 | sens_lead_0 | 0.258 ± 0.051 | 0.272 ± 0.061 | +0.026 +0.003 +0.012 | 0.014 ± 0.011 | 3/3 |
| 0.25 | 0.201 ± 0.069; 0.192 ± 0.095 | sens_lead_30 | 0.170 ± 0.036 | 0.150 ± 0.015 | -0.034 +0.014 -0.040 | -0.020 ± 0.030 | 1/3 |
| 0.25 | 0.201 ± 0.069; 0.192 ± 0.095 | sens_lead_90 | 0.088 ± 0.010 | 0.075 ± 0.017 | -0.007 -0.011 -0.020 | -0.013 ± 0.007 | 0/3 |
| 0.5 | 0.392 ± 0.026; 0.449 ± 0.044 | sens_lead_0 | 0.465 ± 0.022 | 0.440 ± 0.077 | -0.024 -0.089 +0.041 | -0.024 ± 0.065 | 1/3 |
| 0.5 | 0.392 ± 0.026; 0.449 ± 0.044 | sens_lead_30 | 0.315 ± 0.063 | 0.303 ± 0.064 | -0.045 -0.013 +0.023 | -0.012 ± 0.034 | 1/3 |
| 0.5 | 0.392 ± 0.026; 0.449 ± 0.044 | sens_lead_90 | 0.169 ± 0.045 | 0.164 ± 0.033 | -0.017 +0.012 -0.011 | -0.005 ± 0.015 | 1/3 |
| 1.0 | 0.864 ± 0.159; 0.839 ± 0.115 | sens_lead_0 | 0.620 ± 0.093 | 0.603 ± 0.138 | +0.009 -0.075 +0.015 | -0.017 ± 0.050 | 2/3 |
| 1.0 | 0.864 ± 0.159; 0.839 ± 0.115 | sens_lead_30 | 0.494 ± 0.123 | 0.481 ± 0.135 | +0.017 -0.030 -0.027 | -0.013 ± 0.026 | 1/3 |
| 1.0 | 0.864 ± 0.159; 0.839 ± 0.115 | sens_lead_90 | 0.316 ± 0.102 | 0.323 ± 0.114 | +0.026 -0.004 -0.001 | 0.007 ± 0.016 | 1/3 |
| 2.0 | 1.242 ± 0.027; 1.186 ± 0.019 | sens_lead_0 | 0.668 ± 0.110 | 0.655 ± 0.142 | +0.049 -0.089 +0.000 | -0.013 ± 0.070 | 1/3 |
| 2.0 | 1.242 ± 0.027; 1.186 ± 0.019 | sens_lead_30 | 0.588 ± 0.078 | 0.582 ± 0.120 | +0.049 -0.067 +0.000 | -0.006 ± 0.058 | 1/3 |
| 2.0 | 1.242 ± 0.027; 1.186 ± 0.019 | sens_lead_90 | 0.450 ± 0.045 | 0.422 ± 0.139 | +0.049 -0.133 +0.000 | -0.028 ± 0.094 | 1/3 |

## Main model and ablations (with_pulse = main + pulse_htn), each at its own operating point

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| main (no pulse) | 0.623 ± 0.024 | 0.107 ± 0.005 | 0.189 ± 0.026 | 0.465 ± 0.022 | 0.315 ± 0.063 | 0.169 ± 0.045 | 55.833 ± 21.032 | 0.392 ± 0.026 | 0.196 ± 0.006 | 0.668 ± 0.042 | 0.305 ± 0.009 | 0.060 ± 0.005 | 0.003 ± 0.002 | 0.042 ± 0.007 | 0.111 ± 0.004 |
| level_only | 0.536 ± 0.032 | 0.070 ± 0.008 | 0.041 ± 0.037 | 0.216 ± 0.198 | 0.157 ± 0.148 | 0.107 ± 0.110 | n/a | 0.194 ± 0.171 | n/a | 0.864 ± 0.123 | 0.182 ± 0.161 | 0.060 ± 0.005 | 0.001 ± 0.002 | 0.056 ± 0.007 | 0.110 ± 0.005 |
| cuff_only | 0.545 ± 0.020 | 0.074 ± 0.005 | 0.084 ± 0.010 | 0.328 ± 0.033 | 0.194 ± 0.038 | 0.132 ± 0.096 | 96.167 ± 71.502 | 0.291 ± 0.078 | 0.139 ± 0.036 | 0.728 ± 0.054 | 0.250 ± 0.006 | 0.060 ± 0.005 | 0.001 ± 0.001 | 0.057 ± 0.004 | 0.110 ± 0.003 |
| change_only | 0.619 ± 0.025 | 0.114 ± 0.003 | 0.215 ± 0.055 | 0.485 ± 0.096 | 0.339 ± 0.063 | 0.194 ± 0.056 | 62.667 ± 22.502 | 0.435 ± 0.073 | 0.191 ± 0.046 | 0.624 ± 0.089 | 0.298 ± 0.069 | 0.059 ± 0.005 | 0.004 ± 0.003 | 0.047 ± 0.007 | 0.111 ± 0.004 |
| no_personalisation | 0.582 ± 0.039 | 0.087 ± 0.016 | 0.130 ± 0.044 | 0.359 ± 0.041 | 0.281 ± 0.023 | 0.166 ± 0.036 | 88.333 ± 28.259 | 0.353 ± 0.045 | 0.153 ± 0.026 | 0.739 ± 0.011 | 0.275 ± 0.032 | 0.060 ± 0.005 | 0.003 ± 0.001 | 0.046 ± 0.003 | 0.111 ± 0.004 |
| no_context | 0.557 ± 0.036 | 0.080 ± 0.008 | 0.098 ± 0.020 | 0.320 ± 0.185 | 0.197 ± 0.117 | 0.130 ± 0.056 | 94.333 ± 74.929 | 0.317 ± 0.182 | 0.139 ± 0.045 | 0.752 ± 0.113 | 0.234 ± 0.087 | 0.060 ± 0.005 | 0.002 ± 0.001 | 0.051 ± 0.007 | 0.110 ± 0.005 |
| equal_weights | 0.630 ± 0.026 | 0.107 ± 0.006 | 0.182 ± 0.032 | 0.466 ± 0.068 | 0.306 ± 0.061 | 0.176 ± 0.037 | 58.833 ± 3.786 | 0.394 ± 0.079 | 0.200 ± 0.011 | 0.675 ± 0.060 | 0.307 ± 0.007 | 0.060 ± 0.005 | 0.003 ± 0.001 | 0.041 ± 0.008 | 0.111 ± 0.004 |
| reliability_only | 0.611 ± 0.028 | 0.100 ± 0.009 | 0.175 ± 0.042 | 0.419 ± 0.056 | 0.332 ± 0.099 | 0.226 ± 0.083 | 79.667 ± 32.258 | 0.435 ± 0.079 | 0.145 ± 0.004 | 0.627 ± 0.018 | 0.260 ± 0.013 | 0.060 ± 0.005 | 0.002 ± 0.001 | 0.044 ± 0.007 | 0.111 ± 0.004 |
| with_pulse | 0.622 ± 0.023 | 0.108 ± 0.006 | 0.193 ± 0.034 | 0.493 ± 0.107 | 0.357 ± 0.100 | 0.193 ± 0.046 | 62.333 ± 16.289 | 0.449 ± 0.044 | 0.179 ± 0.028 | 0.628 ± 0.030 | 0.299 ± 0.040 | 0.060 ± 0.005 | 0.003 ± 0.001 | 0.043 ± 0.007 | 0.111 ± 0.004 |

## with_pulse minus main at their own operating points (NOT alarm-matched), per seed

| metric | main (no pulse) | with_pulse | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |
|---|---|---|---|---|---|
| auroc | 0.623 ± 0.024 | 0.622 ± 0.023 | -0.006 -0.001 +0.003 | -0.001 ± 0.004 | 1/3 |
| auprc | 0.107 ± 0.005 | 0.108 ± 0.006 | +0.003 -0.000 +0.001 | 0.001 ± 0.001 | 2/3 |
| sens_spec92 | 0.189 ± 0.026 | 0.193 ± 0.034 | +0.009 -0.006 +0.007 | 0.003 ± 0.008 | 2/3 |
| sens_lead_0 | 0.465 ± 0.022 | 0.493 ± 0.107 | +0.024 -0.067 +0.128 | 0.029 ± 0.098 | 2/3 |
| sens_lead_30 | 0.315 ± 0.063 | 0.357 ± 0.100 | +0.024 +0.000 +0.103 | 0.042 ± 0.054 | 2/3 |
| sens_lead_90 | 0.169 ± 0.045 | 0.193 ± 0.046 | +0.024 +0.022 +0.026 | 0.024 ± 0.002 | 3/3 |
| median_lead | 55.833 ± 21.032 | 62.333 ± 16.289 | +3.500 +19.500 -3.500 | 6.500 ± 11.790 | 2/3 |
| alarms_per_nonconv_py | 0.392 ± 0.026 | 0.449 ± 0.044 | +0.047 +0.031 +0.094 | 0.057 ± 0.032 | 3/3 |
| warning_precision | 0.196 ± 0.006 | 0.179 ± 0.028 | -0.013 -0.049 +0.014 | -0.016 ± 0.032 | 1/3 |
| specificity | 0.668 ± 0.042 | 0.628 ± 0.030 | -0.030 -0.021 -0.069 | -0.040 ± 0.026 | 0/3 |
| f1 | 0.305 ± 0.009 | 0.299 ± 0.040 | -0.000 -0.049 +0.030 | -0.006 ± 0.040 | 1/3 |
| brier | 0.060 ± 0.005 | 0.060 ± 0.005 | -0.000 -0.000 -0.000 | -0.000 ± 0.000 | 0/3 |
| ece | 0.003 ± 0.002 | 0.003 ± 0.001 | +0.000 -0.000 +0.001 | 0.000 ± 0.000 | 2/3 |
| aurc | 0.042 ± 0.007 | 0.043 ± 0.007 | +0.000 +0.001 +0.001 | 0.001 ± 0.000 | 3/3 |
| abstention_rate | 0.111 ± 0.004 | 0.111 ± 0.004 | +0.000 +0.000 +0.001 | 0.000 ± 0.000 | 3/3 |

## False prompts over time (non-converters, test people)

Day 0 = first landmark week (after the personal-baseline warm-up). false_prompt_6mo / 12mo = Kaplan-Meier probability of >= 1 false prompt by 6 / 12 months of monitoring, censored at end of follow-up. specificity = non-converters never prompted, CUMULATIVE over the median follow-up (followup_median_days), not a single-window specificity. ppv_person = person-level PPV of a prompt at the test conversion rate (0.173 ± 0.013); lr_pos = Se0 / share of non-converters prompted. alarms_per_nonconv_py divides by calendar time (warm-up included), alarms_per_nonconv_monitored_py by monitored, post-warm-up time.

prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year with repeat suppression: a 26-week refractory period after each prompt (not the clinical panel's rule, which was 13 weeks after a normal cuff series), because 26 weeks is the prediction horizon. It is a BURDEN metric only: first warnings are unchanged (asserted in evaluate.metrics), and every other metric, the tuned thresholds and the operating curve's chance floor use the unsuppressed episodes.

| metric | main (no pulse) | with_pulse | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |
|---|---|---|---|---|---|
| false_prompt_6mo | 0.082 ± 0.011 | 0.097 ± 0.005 | +0.025 +0.010 +0.010 | 0.015 ± 0.009 | 3/3 |
| false_prompt_12mo | 0.211 ± 0.002 | 0.249 ± 0.031 | +0.045 +0.005 +0.064 | 0.038 ± 0.030 | 3/3 |
| followup_median_days | 504.000 ± 0.000 | 504.000 ± 0.000 | +0.000 +0.000 +0.000 | 0.000 ± 0.000 | 0/3 |
| specificity | 0.668 ± 0.042 | 0.628 ± 0.030 | -0.030 -0.021 -0.069 | -0.040 ± 0.026 | 0/3 |
| false_prompts_per_nonconv | 0.579 ± 0.038 | 0.664 ± 0.065 | +0.070 +0.046 +0.139 | 0.085 ± 0.048 | 3/3 |
| ppv_person | 0.227 ± 0.015 | 0.215 ± 0.021 | -0.005 -0.038 +0.006 | -0.012 ± 0.023 | 1/3 |
| lr_pos | 1.412 ± 0.148 | 1.327 ± 0.279 | -0.036 -0.271 +0.052 | -0.085 ± 0.167 | 1/3 |
| alarms_per_nonconv_py | 0.392 ± 0.026 | 0.449 ± 0.044 | +0.047 +0.031 +0.094 | 0.057 ± 0.032 | 3/3 |
| alarms_per_nonconv_monitored_py | 0.422 ± 0.029 | 0.484 ± 0.049 | +0.051 +0.034 +0.101 | 0.062 ± 0.035 | 3/3 |
| prompts_per_nonconv_py_r26 | 0.250 ± 0.024 | 0.285 ± 0.021 | +0.027 +0.021 +0.057 | 0.035 ± 0.019 | 3/3 |

## Pre-onset warnings (simulator: drift onset known)

sens_post_onset_30/90 = Se30/Se90 counting a converter whose first warning came BEFORE the simulated drift onset as a miss (an added sensitivity analysis; sens_lead_* are unchanged and count every warning before t_ref). n_pre_onset_first_warnings = converters whose first warning preceded onset.

| metric | main (no pulse) | with_pulse | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |
|---|---|---|---|---|---|
| sens_lead_30 | 0.315 ± 0.063 | 0.357 ± 0.100 | +0.024 +0.000 +0.103 | 0.042 ± 0.054 | 2/3 |
| sens_post_onset_30 | 0.226 ± 0.045 | 0.252 ± 0.078 | -0.024 +0.000 +0.103 | 0.026 ± 0.067 | 1/3 |
| sens_lead_90 | 0.169 ± 0.045 | 0.193 ± 0.046 | +0.024 +0.022 +0.026 | 0.024 ± 0.002 | 3/3 |
| sens_post_onset_90 | 0.096 ± 0.048 | 0.104 ± 0.037 | +0.000 +0.000 +0.026 | 0.009 ± 0.015 | 1/3 |
| n_pre_onset_first_warnings | 3.667 ± 0.577 | 4.333 ± 1.528 | +2.000 +0.000 +0.000 | 0.667 ± 1.155 | 1/3 |

## Robustness (test people perturbed; with_pulse_drop_pulse = with_pulse model, pulse removed at test time)

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.623 ± 0.024 | 0.107 ± 0.005 | 0.189 ± 0.026 | 0.465 ± 0.022 | 0.315 ± 0.063 | 0.169 ± 0.045 | 55.833 ± 21.032 | 0.392 ± 0.026 | 0.196 ± 0.006 | 0.668 ± 0.042 | 0.305 ± 0.009 | 0.060 ± 0.005 | 0.003 ± 0.002 | 0.042 ± 0.007 | 0.111 ± 0.004 |
| mcar_0.3 | 0.611 ± 0.013 | 0.104 ± 0.011 | 0.191 ± 0.015 | 0.418 ± 0.063 | 0.304 ± 0.033 | 0.166 ± 0.036 | 66.500 ± 26.782 | 0.444 ± 0.009 | 0.152 ± 0.031 | 0.620 ± 0.054 | 0.260 ± 0.048 | 0.060 ± 0.005 | 0.004 ± 0.002 | 0.045 ± 0.005 | 0.111 ± 0.004 |
| mcar_0.6 | 0.582 ± 0.027 | 0.092 ± 0.007 | 0.183 ± 0.049 | 0.320 ± 0.061 | 0.272 ± 0.060 | 0.178 ± 0.066 | 123.833 ± 39.713 | 0.383 ± 0.029 | 0.100 ± 0.014 | 0.634 ± 0.060 | 0.208 ± 0.021 | 0.061 ± 0.005 | 0.011 ± 0.008 | 0.046 ± 0.004 | 0.143 ± 0.005 |
| noise_1.0 | 0.619 ± 0.028 | 0.105 ± 0.007 | 0.247 ± 0.053 | 0.476 ± 0.086 | 0.379 ± 0.063 | 0.234 ± 0.049 | 84.833 ± 10.396 | 0.681 ± 0.068 | 0.132 ± 0.010 | 0.493 ± 0.067 | 0.242 ± 0.019 | 0.060 ± 0.005 | 0.006 ± 0.005 | 0.044 ± 0.009 | 0.112 ± 0.004 |
| drop_night_rmssd | 0.611 ± 0.028 | 0.100 ± 0.009 | 0.154 ± 0.036 | 0.376 ± 0.016 | 0.282 ± 0.060 | 0.160 ± 0.051 | 68.333 ± 32.960 | 0.351 ± 0.056 | 0.169 ± 0.023 | 0.698 ± 0.058 | 0.268 ± 0.021 | 0.060 ± 0.005 | 0.003 ± 0.001 | 0.044 ± 0.008 | 0.110 ± 0.004 |
| mnar_0.4 | 0.567 ± 0.028 | 0.102 ± 0.035 | 0.145 ± 0.064 | 0.204 ± 0.114 | 0.155 ± 0.089 | 0.089 ± 0.052 | 82.833 ± 36.484 | 0.229 ± 0.034 | 0.155 ± 0.063 | 0.793 ± 0.034 | 0.197 ± 0.091 | 0.060 ± 0.006 | 0.008 ± 0.004 | 0.048 ± 0.007 | 0.314 ± 0.029 |
| sensor_fail_0.3 | 0.578 ± 0.026 | 0.100 ± 0.009 | 0.121 ± 0.041 | 0.243 ± 0.094 | 0.168 ± 0.047 | 0.079 ± 0.025 | 58.000 ± 28.792 | 0.167 ± 0.025 | 0.191 ± 0.038 | 0.819 ± 0.035 | 0.225 ± 0.059 | 0.062 ± 0.004 | 0.012 ± 0.003 | 0.051 ± 0.001 | 0.518 ± 0.013 |
| with_pulse_drop_pulse | 0.624 ± 0.022 | 0.108 ± 0.005 | 0.199 ± 0.021 | 0.500 ± 0.072 | 0.355 ± 0.057 | 0.193 ± 0.066 | 68.500 ± 23.817 | 0.474 ± 0.053 | 0.178 ± 0.017 | 0.621 ± 0.038 | 0.301 ± 0.030 | 0.060 ± 0.005 | 0.004 ± 0.002 | 0.043 ± 0.008 | 0.111 ± 0.004 |

## By skin_ita tercile, main model (T1 = lowest; edges differ per seed)

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 80.000 ± 0.000 | 15.667 ± 6.658 | 0.612 ± 0.035 | 0.114 ± 0.051 | 0.122 ± 0.034 | 0.278 ± 0.074 | 0.143 ± 0.057 | 0.105 ± 0.083 | 62.500 ± 60.566 | 0.273 ± 0.105 | 0.234 ± 0.172 | 0.748 ± 0.119 | 0.251 ± 0.149 | 0.070 ± 0.029 | 0.027 ± 0.019 | 0.049 ± 0.024 | 0.234 ± 0.004 |
| T2 | 80.000 ± 0.000 | 12.667 ± 2.309 | 0.659 ± 0.029 | 0.120 ± 0.018 | 0.227 ± 0.048 | 0.567 ± 0.115 | 0.405 ± 0.082 | 0.210 ± 0.072 | 65.667 ± 28.676 | 0.471 ± 0.046 | 0.179 ± 0.022 | 0.605 ± 0.056 | 0.303 ± 0.016 | 0.055 ± 0.010 | 0.014 ± 0.015 | 0.037 ± 0.001 | 0.059 ± 0.003 |
| T3 | 80.667 ± 0.577 | 13.333 ± 3.215 | 0.642 ± 0.016 | 0.121 ± 0.041 | 0.249 ± 0.055 | 0.567 ± 0.130 | 0.450 ± 0.108 | 0.233 ± 0.050 | 79.667 ± 31.005 | 0.418 ± 0.038 | 0.201 ± 0.111 | 0.663 ± 0.023 | 0.344 ± 0.091 | 0.056 ± 0.015 | 0.019 ± 0.001 | 0.041 ± 0.010 | 0.045 ± 0.001 |

## By age tercile, main model (T1 = lowest; edges differ per seed): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 | 82.333 ± 3.215 | 15.667 ± 3.215 | 0.647 ± 0.016 | 0.146 ± 0.047 | 0.163 ± 0.010 | 0.426 ± 0.154 | 0.303 ± 0.119 | 0.169 ± 0.052 | 73.667 ± 30.616 | 0.288 ± 0.115 | 0.262 ± 0.081 | 0.747 ± 0.097 | 0.341 ± 0.119 | 0.066 ± 0.013 | 0.013 ± 0.013 | 0.045 ± 0.013 | 0.115 ± 0.021 |
| T2 | 79.333 ± 4.041 | 13.000 ± 3.606 | 0.617 ± 0.056 | 0.114 ± 0.059 | 0.205 ± 0.078 | 0.533 ± 0.166 | 0.407 ± 0.177 | 0.266 ± 0.061 | 91.667 ± 32.716 | 0.364 ± 0.060 | 0.169 ± 0.074 | 0.665 ± 0.055 | 0.326 ± 0.118 | 0.058 ± 0.016 | 0.017 ± 0.007 | 0.040 ± 0.010 | 0.104 ± 0.013 |
| T3 | 79.000 ± 2.000 | 13.000 ± 1.732 | 0.601 ± 0.067 | 0.097 ± 0.056 | 0.181 ± 0.124 | 0.407 ± 0.037 | 0.203 ± 0.074 | 0.071 ± 0.071 | 37.833 ± 23.634 | 0.533 ± 0.038 | 0.163 ± 0.025 | 0.584 ± 0.069 | 0.232 ± 0.031 | 0.056 ± 0.010 | 0.010 ± 0.005 | 0.041 ± 0.009 | 0.113 ± 0.018 |

## Normalised channel weights (weights), per seed

- night_rhr 0.21, night_rmssd 0.19, still_hr 0.11, steps 0.19, sleep_dur 0.24, sleep_reg 0.07
- night_rhr 0.20, night_rmssd 0.19, still_hr 0.11, steps 0.20, sleep_dur 0.24, sleep_reg 0.07
- night_rhr 0.20, night_rmssd 0.18, still_hr 0.11, steps 0.20, sleep_dur 0.24, sleep_reg 0.07

## Normalised channel weights (weights_with_pulse), per seed

- night_rhr 0.18, night_rmssd 0.17, still_hr 0.10, steps 0.17, sleep_dur 0.21, sleep_reg 0.06, pulse_htn 0.12
- night_rhr 0.18, night_rmssd 0.16, still_hr 0.09, steps 0.17, sleep_dur 0.21, sleep_reg 0.06, pulse_htn 0.12
- night_rhr 0.18, night_rmssd 0.16, still_hr 0.09, steps 0.17, sleep_dur 0.21, sleep_reg 0.06, pulse_htn 0.12

Example with_pulse ledger (seed0, P0045 week 41): channel_contrib (mean weekly z, last 6 weeks) night_rhr -0.089, night_rmssd -0.306, still_hr 0.534, steps 0.686, sleep_dur 0.111, sleep_reg 0.151, pulse_htn -0.241

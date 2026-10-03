# SENTINEL-HTN results

Run: n=1200, days=540, seed=1, n_boot=20. Test people: 240 (45 converters). Thresholds: persistence dev > 0.100, warning p_lo >= 0.100. Synthetic data unless stated; research prototype, not a diagnostic; no blood-pressure value is output.

## Main model (metrics A-F, held-out test people)

| set | metric | value |
|---|---|---|
| A | auroc | 0.626 |
| A | auprc | 0.137 |
| A | sens_spec92 | 0.180 |
| A | spec_spec92_test | 0.942 |
| A | thr_spec92 | 0.106 |
| B | sens_lead_0 | 0.444 |
| B | sens_lead_30 | 0.267 |
| B | sens_lead_90 | 0.111 |
| B | sens_lead_180 | 0.044 |
| B | median_lead | 52.500 |
| B | sens_post_onset_30 | 0.244 |
| B | sens_post_onset_90 | 0.089 |
| B | n_pre_onset_first_warnings | 1.000 |
| C | alarms_per_nonconv_py | 0.378 |
| C | alarms_per_nonconv_monitored_py | 0.407 |
| C | prompts_per_nonconv_py_r26 | 0.232 |
| C | warning_precision | 0.220 |
| C | specificity | 0.682 |
| C | f1 | 0.315 |
| C | ppv_person | 0.244 |
| C | lr_pos | 1.398 |
| C | false_prompt_6mo | 0.062 |
| C | false_prompt_12mo | 0.215 |
| C | followup_median_days | 504.000 |
| C | false_prompts_per_nonconv | 0.559 |
| D | brier | 0.064 |
| D | ece | 0.010 |
| F | aurc | 0.046 |
| F | abstention_rate | 0.106 |

## Ablations vs full (delta vs full in parentheses)

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full | 0.626 | 0.137 | 0.180 | 0.444 | 0.267 | 0.111 | 52.500 | 0.378 | 0.220 | 0.682 | 0.315 | 0.064 | 0.010 | 0.046 | 0.106 |
| level_only | 0.500 (-0.126) | 0.070 (-0.067) | 0.000 (-0.180) | 0.000 (-0.444) | 0.000 (-0.267) | 0.000 (-0.111) | n/a | 0.000 (-0.378) | n/a | 1.000 (+0.318) | 0.000 (-0.315) | 0.065 (+0.001) | 0.000 (-0.010) | 0.061 (+0.015) | 0.104 (-0.002) |
| cuff_only | 0.553 (-0.073) | 0.079 (-0.057) | 0.076 (-0.104) | 0.000 (-0.444) | 0.000 (-0.267) | 0.000 (-0.111) | n/a | 0.024 (-0.354) | 0.000 (-0.220) | 0.964 (+0.282) | 0.000 (-0.315) | 0.065 (+0.001) | 0.000 (-0.010) | 0.061 (+0.015) | 0.104 (-0.002) |
| change_only | 0.624 (-0.002) | 0.138 (+0.001) | 0.179 (-0.001) | 0.378 (-0.067) | 0.244 (-0.022) | 0.111 (+0.000) | 48.000 (-4.500) | 0.340 (-0.038) | 0.208 (-0.012) | 0.692 (+0.010) | 0.279 (-0.036) | 0.064 (-0.000) | 0.007 (-0.003) | 0.046 (+0.000) | 0.106 (-0.000) |
| no_personalisation | 0.551 (-0.074) | 0.084 (-0.053) | 0.091 (-0.088) | 0.289 (-0.156) | 0.244 (-0.022) | 0.111 (+0.000) | 62.000 (+9.500) | 0.330 (-0.049) | 0.180 (-0.039) | 0.754 (+0.072) | 0.245 (-0.070) | 0.065 (+0.001) | 0.004 (-0.007) | 0.048 (+0.002) | 0.106 (-0.001) |
| no_context | 0.530 (-0.096) | 0.077 (-0.060) | 0.073 (-0.106) | 0.289 (-0.156) | 0.156 (-0.111) | 0.089 (-0.022) | 39.000 (-13.500) | 0.402 (+0.024) | 0.148 (-0.071) | 0.651 (-0.031) | 0.206 (-0.109) | 0.065 (+0.001) | 0.001 (-0.010) | 0.056 (+0.010) | 0.106 (-0.000) |
| equal_weights | 0.624 (-0.002) | 0.121 (-0.016) | 0.164 (-0.015) | 0.333 (-0.111) | 0.222 (-0.044) | 0.067 (-0.044) | 59.000 (+6.500) | 0.271 (-0.108) | 0.219 (-0.001) | 0.749 (+0.067) | 0.275 (-0.040) | 0.064 (+0.000) | 0.006 (-0.005) | 0.046 (-0.000) | 0.105 (-0.001) |
| reliability_only | 0.623 (-0.003) | 0.123 (-0.013) | 0.159 (-0.021) | 0.267 (-0.178) | 0.178 (-0.089) | 0.067 (-0.044) | 49.000 (-3.500) | 0.215 (-0.163) | 0.220 (+0.000) | 0.805 (+0.123) | 0.253 (-0.062) | 0.064 (+0.000) | 0.006 (-0.004) | 0.047 (+0.001) | 0.105 (-0.001) |
| with_pulse | 0.623 (-0.003) | 0.131 (-0.006) | 0.170 (-0.010) | 0.378 (-0.067) | 0.222 (-0.044) | 0.089 (-0.022) | 38.000 (-14.500) | 0.340 (-0.038) | 0.224 (+0.004) | 0.744 (+0.062) | 0.304 (-0.011) | 0.064 (+0.000) | 0.008 (-0.003) | 0.047 (+0.001) | 0.106 (-0.001) |

## Robustness (E): test people perturbed, models fitted on clean data

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.626 | 0.137 | 0.180 | 0.444 | 0.267 | 0.111 | 52.500 | 0.378 | 0.220 | 0.682 | 0.315 | 0.064 | 0.010 | 0.046 | 0.106 |
| mcar_0.3 | 0.611 (-0.014) | 0.116 (-0.021) | 0.186 (+0.006) | 0.489 (+0.044) | 0.378 (+0.111) | 0.111 (+0.000) | 66.000 (+13.500) | 0.496 (+0.118) | 0.183 (-0.036) | 0.554 (-0.128) | 0.286 (-0.029) | 0.064 (+0.000) | 0.005 (-0.006) | 0.049 (+0.003) | 0.106 (-0.000) |
| mcar_0.6 | 0.547 (-0.079) | 0.086 (-0.050) | 0.162 (-0.018) | 0.267 (-0.178) | 0.200 (-0.067) | 0.133 (+0.022) | 79.500 (+27.000) | 0.447 (+0.069) | 0.114 (-0.106) | 0.610 (-0.072) | 0.180 (-0.135) | 0.066 (+0.002) | 0.012 (+0.002) | 0.055 (+0.009) | 0.136 (+0.030) |
| noise_1.0 | 0.588 (-0.037) | 0.111 (-0.026) | 0.198 (+0.018) | 0.422 (-0.022) | 0.356 (+0.089) | 0.200 (+0.089) | 78.000 (+25.500) | 0.669 (+0.291) | 0.127 (-0.092) | 0.492 (-0.190) | 0.233 (-0.082) | 0.064 (+0.000) | 0.002 (-0.008) | 0.051 (+0.005) | 0.107 (+0.001) |
| drop_night_rmssd | 0.619 (-0.007) | 0.121 (-0.016) | 0.162 (-0.018) | 0.378 (-0.067) | 0.267 (+0.000) | 0.133 (+0.022) | 68.000 (+15.500) | 0.409 (+0.031) | 0.188 (-0.032) | 0.677 (-0.005) | 0.272 (-0.043) | 0.064 (+0.000) | 0.007 (-0.004) | 0.048 (+0.002) | 0.106 (-0.000) |
| mnar_0.4 | 0.548 (-0.078) | 0.093 (-0.043) | 0.112 (-0.068) | 0.200 (-0.244) | 0.133 (-0.133) | 0.067 (-0.044) | 55.000 (+2.500) | 0.181 (-0.197) | 0.205 (-0.014) | 0.814 (+0.132) | 0.214 (-0.101) | 0.057 (-0.007) | 0.005 (-0.005) | 0.045 (-0.001) | 0.334 (+0.228) |
| sensor_fail_0.3 | 0.574 (-0.052) | 0.113 (-0.024) | 0.095 (-0.085) | 0.156 (-0.289) | 0.111 (-0.156) | 0.022 (-0.089) | 41.000 (-11.500) | 0.153 (-0.225) | 0.184 (-0.035) | 0.841 (+0.159) | 0.169 (-0.146) | 0.067 (+0.003) | 0.013 (+0.002) | 0.047 (+0.001) | 0.504 (+0.398) |
| with_pulse_drop_pulse | 0.621 (-0.005) | 0.134 (-0.003) | 0.198 (+0.018) | 0.378 (-0.067) | 0.200 (-0.067) | 0.089 (-0.022) | 34.000 (-18.500) | 0.361 (-0.017) | 0.195 (-0.025) | 0.692 (+0.010) | 0.279 (-0.036) | 0.064 (+0.000) | 0.011 (+0.001) | 0.046 (+0.000) | 0.106 (-0.000) |

## Fairness (E8): by skin_ita tercile

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (-40.1, 9.6] | 80 | 23 | 0.656 | 0.236 | 0.150 | 0.304 | 0.174 | 0.130 | 86.000 | 0.249 | 0.300 | 0.772 | 0.326 | 0.101 | 0.048 | 0.068 | 0.229 |
| (9.6, 33.7] | 80 | 10 | 0.647 | 0.125 | 0.254 | 0.500 | 0.400 | 0.000 | 78.000 | 0.493 | 0.161 | 0.629 | 0.244 | 0.043 | 0.026 | 0.028 | 0.056 |
| (33.7, 70.0] | 80 | 12 | 0.600 | 0.104 | 0.172 | 0.667 | 0.333 | 0.167 | 30.500 | 0.368 | 0.226 | 0.662 | 0.372 | 0.052 | 0.019 | 0.043 | 0.045 |

## By age tercile (years): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (29.9, 40.0] | 86 | 17 | 0.643 | 0.163 | 0.132 | 0.412 | 0.118 | 0.000 | 11.000 | 0.255 | 0.304 | 0.768 | 0.350 | 0.067 | 0.010 | 0.044 | 0.120 |
| (40.0, 53.0] | 75 | 14 | 0.641 | 0.178 | 0.247 | 0.500 | 0.429 | 0.214 | 80.000 | 0.410 | 0.185 | 0.672 | 0.341 | 0.064 | 0.018 | 0.046 | 0.105 |
| (53.0, 65.0] | 79 | 14 | 0.600 | 0.097 | 0.169 | 0.429 | 0.286 | 0.143 | 84.000 | 0.479 | 0.188 | 0.600 | 0.261 | 0.060 | 0.010 | 0.048 | 0.093 |

sens_spec92 = per-WEEK sensitivity at 92% per-WEEK specificity: landmark weeks, p threshold from the y=0 weeks of the CALIBRATION people (spec_spec92_test = per-week specificity reached on test); not the system's operating point. specificity = non-converters never prompted during follow-up (median 16.6 months of monitoring after the warm-up): CUMULATIVE over follow-up, not a single-window specificity; f1 and ppv_person (person-level PPV of a prompt) at this test conversion rate of 19%; lr_pos = Se0 / share of non-converters prompted. false_prompt_6mo / 12mo = Kaplan-Meier probability that a non-converter has >= 1 false prompt by 6 / 12 months of monitoring (day 0 = first landmark week, censored at end of follow-up). alarms_per_nonconv_py: per calendar person-year (warm-up included); alarms_per_nonconv_monitored_py: per monitored (post-warm-up) person-year. prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year after a 26-week refractory period (chosen to equal the 26-week prediction horizon; not the clinical panel rule of 13 weeks after a normal cuff series). It is a burden metric only: first warnings, every other metric, the tuned thresholds and the chance floor use the unsuppressed episodes. sens_post_onset_30/90 = Se30/Se90 counting a first warning before the simulated drift onset as a miss (n_pre_onset_first_warnings = how many); sens_lead_* count every warning before t_ref.

## Early-warning operating curve: sensitivity at >= 90 d lead (alarms/non-converter-yr) per warning budget

| budget | full | level_only | cuff_only | with_pulse | chance |
|---|---|---|---|---|---|
| 0.25 | 0.067 (0.139) | 0.000 (0.000) | 0.000 (0.024) | 0.067 (0.173) | 0.128 (0.250) |
| 0.5 | 0.111 (0.378) | 0.000 (0.000) | 0.000 (0.024) | 0.089 (0.340) | 0.238 (0.500) |
| 1.0 | 0.222 (0.777) | 0.000 (0.000) | 0.222 (0.447) | 0.200 (0.774) | 0.413 (1.000) |
| 2.0 | 0.556 (1.526) | 0.556 (1.526) | 0.556 (1.526) | 0.533 (1.492) | 0.640 (2.000) |

## Example evidence ledger (first warning of a warned converter)

```json
{
  "pid": "P0872",
  "week": 40,
  "first_warning_day": 286.0,
  "lead_days": 45.0,
  "state": "WARNING",
  "p": 0.12649837058174476,
  "p_lo": 0.10272117510466885,
  "p_hi": 0.1469828880530215,
  "weeks_exceeded": "6/6",
  "episodes": 5,
  "dev_slope12": 0.05604425795853595,
  "channel_contrib": {
    "night_rhr": 0.8068478532557821,
    "night_rmssd": 0.4291630811141676,
    "still_hr": 1.7891510015025527,
    "steps": 0.010879263598757507,
    "sleep_dur": 0.29164310680204253,
    "sleep_reg": 0.14430235608341765
  },
  "valid_days_30": 24,
  "ctx_masked_6w": 14,
  "month": 10
}
```

Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`.

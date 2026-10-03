# SENTINEL-HTN results

Run: n=1200, days=540, seed=2, n_boot=20. Test people: 241 (39 converters). Thresholds: persistence dev > 0.100, warning p_lo >= 0.090. Synthetic data unless stated; research prototype, not a diagnostic; no blood-pressure value is output.

## Main model (metrics A-F, held-out test people)

| set | metric | value |
|---|---|---|
| A | auroc | 0.606 |
| A | auprc | 0.098 |
| A | sens_spec92 | 0.173 |
| A | spec_spec92_test | 0.928 |
| A | thr_spec92 | 0.101 |
| B | sens_lead_0 | 0.462 |
| B | sens_lead_30 | 0.333 |
| B | sens_lead_90 | 0.128 |
| B | sens_lead_180 | 0.026 |
| B | median_lead | 60.500 |
| B | sens_post_onset_30 | 0.282 |
| B | sens_post_onset_90 | 0.077 |
| B | n_pre_onset_first_warnings | 2.000 |
| C | alarms_per_nonconv_py | 0.392 |
| C | alarms_per_nonconv_monitored_py | 0.422 |
| C | prompts_per_nonconv_py_r26 | 0.238 |
| C | warning_precision | 0.207 |
| C | specificity | 0.683 |
| C | f1 | 0.298 |
| C | ppv_person | 0.220 |
| C | lr_pos | 1.457 |
| C | false_prompt_6mo | 0.114 |
| C | false_prompt_12mo | 0.208 |
| C | followup_median_days | 504.000 |
| C | false_prompts_per_nonconv | 0.579 |
| D | brier | 0.055 |
| D | ece | 0.003 |
| F | aurc | 0.040 |
| F | abstention_rate | 0.113 |

## Ablations vs full (delta vs full in parentheses)

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full | 0.606 | 0.098 | 0.173 | 0.462 | 0.333 | 0.128 | 60.500 | 0.392 | 0.207 | 0.683 | 0.298 | 0.055 | 0.003 | 0.040 | 0.113 |
| level_only | 0.548 (-0.058) | 0.063 (-0.036) | 0.049 (-0.124) | 0.256 (-0.205) | 0.128 (-0.205) | 0.077 (-0.051) | 36.500 (-24.000) | 0.244 (-0.147) | 0.157 (-0.050) | 0.797 (+0.114) | 0.222 (-0.075) | 0.056 (+0.001) | 0.001 (-0.002) | 0.047 (+0.007) | 0.112 (-0.001) |
| cuff_only | 0.560 (-0.046) | 0.069 (-0.029) | 0.080 (-0.093) | 0.282 (-0.179) | 0.179 (-0.154) | 0.077 (-0.051) | 41.000 (-19.500) | 0.301 (-0.090) | 0.143 (-0.064) | 0.743 (+0.059) | 0.216 (-0.082) | 0.056 (+0.001) | 0.000 (-0.003) | 0.058 (+0.018) | 0.112 (-0.001) |
| change_only | 0.612 (+0.006) | 0.108 (+0.010) | 0.201 (+0.028) | 0.564 (+0.103) | 0.410 (+0.077) | 0.179 (+0.051) | 71.000 (+10.500) | 0.475 (+0.084) | 0.200 (-0.007) | 0.589 (-0.094) | 0.306 (+0.008) | 0.055 (-0.000) | 0.001 (-0.001) | 0.048 (+0.008) | 0.114 (+0.001) |
| no_personalisation | 0.540 (-0.065) | 0.064 (-0.034) | 0.080 (-0.093) | 0.333 (-0.128) | 0.154 (-0.179) | 0.128 (+0.000) | 29.000 (-31.500) | 0.412 (+0.020) | 0.141 (-0.066) | 0.713 (+0.030) | 0.236 (-0.061) | 0.056 (+0.001) | 0.006 (+0.003) | 0.043 (+0.003) | 0.114 (+0.001) |
| no_context | 0.547 (-0.058) | 0.069 (-0.029) | 0.064 (-0.110) | 0.385 (-0.077) | 0.179 (-0.154) | 0.154 (+0.026) | 22.000 (-38.500) | 0.372 (-0.020) | 0.159 (-0.048) | 0.733 (+0.050) | 0.278 (-0.020) | 0.056 (+0.001) | 0.002 (-0.001) | 0.044 (+0.004) | 0.113 (+0.000) |
| equal_weights | 0.577 (-0.028) | 0.082 (-0.017) | 0.134 (-0.040) | 0.282 (-0.179) | 0.179 (-0.154) | 0.103 (-0.026) | 73.000 (+12.500) | 0.338 (-0.054) | 0.141 (-0.066) | 0.703 (+0.020) | 0.200 (-0.098) | 0.056 (+0.000) | 0.004 (+0.002) | 0.042 (+0.002) | 0.113 (-0.000) |
| reliability_only | 0.585 (-0.021) | 0.084 (-0.014) | 0.139 (-0.034) | 0.282 (-0.179) | 0.179 (-0.154) | 0.103 (-0.026) | 44.000 (-16.500) | 0.368 (-0.023) | 0.143 (-0.064) | 0.708 (+0.025) | 0.202 (-0.096) | 0.055 (+0.000) | 0.004 (+0.001) | 0.040 (+0.000) | 0.113 (-0.000) |
| with_pulse | 0.607 (+0.002) | 0.098 (-0.001) | 0.176 (+0.003) | 0.564 (+0.103) | 0.385 (+0.051) | 0.128 (+0.000) | 46.000 (-14.500) | 0.412 (+0.020) | 0.222 (+0.015) | 0.663 (-0.020) | 0.341 (+0.044) | 0.055 (+0.000) | 0.003 (+0.000) | 0.040 (+0.000) | 0.113 (+0.000) |

## Robustness (E): test people perturbed, models fitted on clean data

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.606 | 0.098 | 0.173 | 0.462 | 0.333 | 0.128 | 60.500 | 0.392 | 0.207 | 0.683 | 0.298 | 0.055 | 0.003 | 0.040 | 0.113 |
| mcar_0.3 | 0.573 (-0.033) | 0.078 (-0.021) | 0.167 (-0.006) | 0.385 (-0.077) | 0.256 (-0.077) | 0.154 (+0.026) | 73.000 (+12.500) | 0.469 (+0.077) | 0.123 (-0.085) | 0.550 (-0.134) | 0.207 (-0.091) | 0.056 (+0.001) | 0.008 (+0.006) | 0.045 (+0.005) | 0.114 (+0.001) |
| mcar_0.6 | 0.563 (-0.042) | 0.073 (-0.025) | 0.154 (-0.020) | 0.308 (-0.154) | 0.282 (-0.051) | 0.179 (+0.051) | 105.000 (+44.500) | 0.455 (+0.064) | 0.091 (-0.116) | 0.569 (-0.114) | 0.174 (-0.124) | 0.058 (+0.003) | 0.023 (+0.021) | 0.050 (+0.010) | 0.147 (+0.034) |
| noise_1.0 | 0.587 (-0.018) | 0.082 (-0.016) | 0.245 (+0.072) | 0.513 (+0.051) | 0.436 (+0.103) | 0.282 (+0.154) | 103.000 (+42.500) | 0.693 (+0.301) | 0.132 (-0.076) | 0.460 (-0.223) | 0.238 (-0.059) | 0.056 (+0.001) | 0.012 (+0.009) | 0.043 (+0.003) | 0.115 (+0.002) |
| drop_night_rmssd | 0.581 (-0.025) | 0.079 (-0.019) | 0.128 (-0.045) | 0.333 (-0.128) | 0.231 (-0.103) | 0.128 (+0.000) | 73.000 (+12.500) | 0.358 (-0.033) | 0.150 (-0.057) | 0.668 (-0.015) | 0.218 (-0.079) | 0.056 (+0.001) | 0.007 (+0.004) | 0.042 (+0.002) | 0.113 (-0.000) |
| mnar_0.4 | 0.597 (-0.009) | 0.089 (-0.009) | 0.125 (-0.048) | 0.179 (-0.282) | 0.154 (-0.179) | 0.077 (-0.051) | 87.000 (+26.500) | 0.314 (-0.077) | 0.102 (-0.105) | 0.732 (+0.049) | 0.159 (-0.138) | 0.055 (+0.000) | 0.010 (+0.007) | 0.040 (-0.000) | 0.282 (+0.169) |
| sensor_fail_0.3 | 0.584 (-0.021) | 0.098 (-0.000) | 0.100 (-0.073) | 0.231 (-0.231) | 0.179 (-0.154) | 0.077 (-0.051) | 62.000 (+1.500) | 0.174 (-0.218) | 0.163 (-0.044) | 0.802 (+0.119) | 0.205 (-0.093) | 0.058 (+0.003) | 0.017 (+0.014) | 0.051 (+0.010) | 0.521 (+0.408) |
| with_pulse_drop_pulse | 0.604 (-0.002) | 0.096 (-0.002) | 0.180 (+0.006) | 0.513 (+0.051) | 0.385 (+0.051) | 0.154 (+0.026) | 60.500 (+0.000) | 0.462 (+0.070) | 0.191 (-0.016) | 0.634 (-0.050) | 0.301 (+0.003) | 0.055 (+0.000) | 0.003 (+0.000) | 0.041 (+0.001) | 0.113 (+0.000) |

## Fairness (E8): by skin_ita tercile

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (-40.1, 5.7] | 80 | 14 | 0.606 | 0.113 | 0.150 | 0.500 | 0.357 | 0.143 | 70.000 | 0.338 | 0.259 | 0.697 | 0.341 | 0.063 | 0.015 | 0.046 | 0.239 |
| (5.7, 37.4] | 80 | 14 | 0.579 | 0.093 | 0.140 | 0.500 | 0.286 | 0.071 | 35.000 | 0.369 | 0.259 | 0.697 | 0.341 | 0.060 | 0.009 | 0.041 | 0.061 |
| (37.4, 70.0] | 81 | 11 | 0.666 | 0.104 | 0.252 | 0.364 | 0.364 | 0.182 | 107.000 | 0.464 | 0.107 | 0.657 | 0.205 | 0.043 | 0.015 | 0.033 | 0.044 |

## By age tercile (years): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (29.9, 41.0] | 80 | 12 | 0.639 | 0.105 | 0.129 | 0.333 | 0.167 | 0.083 | 50.000 | 0.249 | 0.211 | 0.779 | 0.258 | 0.052 | 0.005 | 0.032 | 0.133 |
| (41.0, 54.0] | 80 | 16 | 0.660 | 0.184 | 0.248 | 0.625 | 0.500 | 0.250 | 79.500 | 0.402 | 0.281 | 0.656 | 0.417 | 0.068 | 0.020 | 0.044 | 0.091 |
| (54.0, 65.0] | 81 | 11 | 0.495 | 0.048 | 0.107 | 0.364 | 0.273 | 0.000 | 44.000 | 0.522 | 0.129 | 0.614 | 0.190 | 0.045 | 0.017 | 0.044 | 0.115 |

sens_spec92 = per-WEEK sensitivity at 92% per-WEEK specificity: landmark weeks, p threshold from the y=0 weeks of the CALIBRATION people (spec_spec92_test = per-week specificity reached on test); not the system's operating point. specificity = non-converters never prompted during follow-up (median 16.6 months of monitoring after the warm-up): CUMULATIVE over follow-up, not a single-window specificity; f1 and ppv_person (person-level PPV of a prompt) at this test conversion rate of 16%; lr_pos = Se0 / share of non-converters prompted. false_prompt_6mo / 12mo = Kaplan-Meier probability that a non-converter has >= 1 false prompt by 6 / 12 months of monitoring (day 0 = first landmark week, censored at end of follow-up). alarms_per_nonconv_py: per calendar person-year (warm-up included); alarms_per_nonconv_monitored_py: per monitored (post-warm-up) person-year. prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year after a 26-week refractory period (chosen to equal the 26-week prediction horizon; not the clinical panel rule of 13 weeks after a normal cuff series). It is a burden metric only: first warnings, every other metric, the tuned thresholds and the chance floor use the unsuppressed episodes. sens_post_onset_30/90 = Se30/Se90 counting a first warning before the simulated drift onset as a miss (n_pre_onset_first_warnings = how many); sens_lead_* count every warning before t_ref.

## Early-warning operating curve: sensitivity at >= 90 d lead (alarms/non-converter-yr) per warning budget

| budget | full | level_only | cuff_only | with_pulse | chance |
|---|---|---|---|---|---|
| 0.25 | 0.077 (0.171) | 0.026 (0.070) | 0.077 (0.117) | 0.051 (0.151) | 0.141 (0.250) |
| 0.5 | 0.128 (0.392) | 0.077 (0.244) | 0.077 (0.301) | 0.128 (0.412) | 0.260 (0.500) |
| 1.0 | 0.308 (0.861) | 0.256 (0.780) | 0.205 (0.589) | 0.282 (0.753) | 0.446 (1.000) |
| 2.0 | 0.436 (1.353) | 0.436 (1.353) | 0.436 (1.353) | 0.410 (1.272) | 0.680 (2.000) |

## Example evidence ledger (first warning of a warned converter)

```json
{
  "pid": "P0496",
  "week": 35,
  "first_warning_day": 251.0,
  "lead_days": 70.0,
  "state": "WARNING",
  "p": 0.12621036383392079,
  "p_lo": 0.09563743875640902,
  "p_hi": 0.137781793363258,
  "weeks_exceeded": "4/5",
  "episodes": 3,
  "dev_slope12": 0.03857075429949349,
  "channel_contrib": {
    "night_rhr": 1.117337021766027,
    "night_rmssd": 1.1970905319827119,
    "still_hr": 1.470632184867251,
    "steps": 0.21728977377217448,
    "sleep_dur": 0.060284519360096434,
    "sleep_reg": 0.11860082144706047
  },
  "valid_days_30": 18,
  "ctx_masked_6w": 10,
  "month": 11
}
```

Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`.

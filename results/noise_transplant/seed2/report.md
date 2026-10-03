# SENTINEL-HTN results

Run: n=1200, days=540, seed=2, n_boot=20. Test people: 241 (39 converters). Thresholds: persistence dev > 0.150, warning p_lo >= 0.080. Synthetic data unless stated; research prototype, not a diagnostic; no blood-pressure value is output.

## Main model (metrics A-F, held-out test people)

| set | metric | value |
|---|---|---|
| A | auroc | 0.635 |
| A | auprc | 0.102 |
| A | sens_spec92 | 0.201 |
| A | spec_spec92_test | 0.919 |
| A | thr_spec92 | 0.089 |
| B | sens_lead_0 | 0.462 |
| B | sens_lead_30 | 0.333 |
| B | sens_lead_90 | 0.154 |
| B | sens_lead_180 | 0.077 |
| B | median_lead | 54.500 |
| B | sens_post_onset_30 | 0.231 |
| B | sens_post_onset_90 | 0.051 |
| B | n_pre_onset_first_warnings | 4.000 |
| C | alarms_per_nonconv_py | 0.388 |
| C | alarms_per_nonconv_monitored_py | 0.419 |
| C | prompts_per_nonconv_py_r26 | 0.231 |
| C | warning_precision | 0.195 |
| C | specificity | 0.708 |
| C | f1 | 0.310 |
| C | ppv_person | 0.234 |
| C | lr_pos | 1.580 |
| C | false_prompt_6mo | 0.084 |
| C | false_prompt_12mo | 0.213 |
| C | followup_median_days | 504.000 |
| C | false_prompts_per_nonconv | 0.574 |
| D | brier | 0.055 |
| D | ece | 0.002 |
| F | aurc | 0.036 |
| F | abstention_rate | 0.113 |

## Ablations vs full (delta vs full in parentheses)

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full | 0.635 | 0.102 | 0.201 | 0.462 | 0.333 | 0.154 | 54.500 | 0.388 | 0.195 | 0.708 | 0.310 | 0.055 | 0.002 | 0.036 | 0.113 |
| level_only | 0.546 (-0.089) | 0.062 (-0.040) | 0.049 (-0.152) | 0.256 (-0.205) | 0.179 (-0.154) | 0.103 (-0.051) | 67.500 (+13.000) | 0.261 (-0.127) | 0.136 (-0.058) | 0.832 (+0.124) | 0.241 (-0.069) | 0.056 (+0.001) | 0.001 (-0.001) | 0.047 (+0.012) | 0.112 (-0.001) |
| cuff_only | 0.560 (-0.075) | 0.069 (-0.033) | 0.080 (-0.121) | 0.359 (-0.103) | 0.231 (-0.103) | 0.179 (+0.026) | 95.500 (+41.000) | 0.305 (-0.084) | 0.129 (-0.066) | 0.723 (+0.015) | 0.257 (-0.053) | 0.056 (+0.001) | 0.000 (-0.002) | 0.058 (+0.022) | 0.113 (-0.000) |
| change_only | 0.642 (+0.007) | 0.116 (+0.015) | 0.247 (+0.046) | 0.564 (+0.103) | 0.385 (+0.051) | 0.205 (+0.051) | 45.000 (-9.500) | 0.362 (-0.027) | 0.244 (+0.049) | 0.723 (+0.015) | 0.376 (+0.066) | 0.055 (-0.000) | 0.007 (+0.005) | 0.041 (+0.006) | 0.113 (+0.000) |
| no_personalisation | 0.577 (-0.058) | 0.071 (-0.030) | 0.085 (-0.117) | 0.359 (-0.103) | 0.308 (-0.026) | 0.128 (-0.026) | 60.500 (+6.000) | 0.385 (-0.003) | 0.134 (-0.060) | 0.738 (+0.030) | 0.264 (-0.046) | 0.056 (+0.001) | 0.003 (+0.002) | 0.043 (+0.008) | 0.113 (+0.000) |
| no_context | 0.561 (-0.074) | 0.073 (-0.028) | 0.078 (-0.123) | 0.385 (-0.077) | 0.231 (-0.103) | 0.154 (+0.000) | 41.000 (-13.500) | 0.475 (+0.087) | 0.118 (-0.076) | 0.698 (-0.010) | 0.261 (-0.049) | 0.056 (+0.001) | 0.002 (-0.000) | 0.043 (+0.007) | 0.114 (+0.001) |
| equal_weights | 0.638 (+0.003) | 0.100 (-0.002) | 0.195 (-0.006) | 0.462 (+0.000) | 0.308 (-0.026) | 0.154 (+0.000) | 54.500 (+0.000) | 0.392 (+0.003) | 0.198 (+0.003) | 0.688 (-0.020) | 0.300 (-0.010) | 0.055 (+0.000) | 0.002 (-0.000) | 0.035 (-0.000) | 0.113 (+0.000) |
| reliability_only | 0.620 (-0.015) | 0.090 (-0.012) | 0.182 (-0.020) | 0.462 (+0.000) | 0.359 (+0.026) | 0.205 (+0.051) | 80.500 (+26.000) | 0.516 (+0.127) | 0.149 (-0.046) | 0.624 (-0.084) | 0.271 (-0.040) | 0.055 (+0.000) | 0.002 (+0.000) | 0.038 (+0.002) | 0.114 (+0.001) |
| with_pulse | 0.638 (+0.003) | 0.103 (+0.001) | 0.209 (+0.007) | 0.590 (+0.128) | 0.436 (+0.103) | 0.179 (+0.026) | 51.000 (-3.500) | 0.482 (+0.094) | 0.208 (+0.014) | 0.639 (-0.069) | 0.341 (+0.030) | 0.055 (-0.000) | 0.002 (+0.001) | 0.036 (+0.001) | 0.114 (+0.001) |

## Robustness (E): test people perturbed, models fitted on clean data

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.635 | 0.102 | 0.201 | 0.462 | 0.333 | 0.154 | 54.500 | 0.388 | 0.195 | 0.708 | 0.310 | 0.055 | 0.002 | 0.036 | 0.113 |
| mcar_0.3 | 0.626 (-0.009) | 0.099 (-0.003) | 0.203 (+0.001) | 0.487 (+0.026) | 0.333 (+0.000) | 0.128 (-0.026) | 45.000 (-9.500) | 0.452 (+0.064) | 0.176 (-0.018) | 0.673 (-0.035) | 0.306 (-0.004) | 0.055 (+0.000) | 0.002 (+0.000) | 0.040 (+0.004) | 0.114 (+0.001) |
| mcar_0.6 | 0.587 (-0.048) | 0.085 (-0.017) | 0.142 (-0.059) | 0.282 (-0.179) | 0.231 (-0.103) | 0.179 (+0.026) | 148.000 (+93.500) | 0.355 (-0.033) | 0.085 (-0.110) | 0.703 (-0.005) | 0.200 (-0.110) | 0.056 (+0.001) | 0.010 (+0.008) | 0.042 (+0.006) | 0.146 (+0.033) |
| noise_1.0 | 0.630 (-0.005) | 0.100 (-0.002) | 0.285 (+0.084) | 0.513 (+0.051) | 0.436 (+0.103) | 0.256 (+0.103) | 89.000 (+34.500) | 0.713 (+0.325) | 0.139 (-0.056) | 0.530 (-0.178) | 0.260 (-0.051) | 0.055 (+0.000) | 0.003 (+0.001) | 0.039 (+0.003) | 0.114 (+0.001) |
| drop_night_rmssd | 0.620 (-0.015) | 0.091 (-0.011) | 0.154 (-0.047) | 0.359 (-0.103) | 0.282 (-0.051) | 0.128 (-0.026) | 62.000 (+7.500) | 0.345 (-0.044) | 0.169 (-0.026) | 0.748 (+0.040) | 0.269 (-0.041) | 0.055 (+0.000) | 0.003 (+0.001) | 0.037 (+0.002) | 0.112 (-0.001) |
| mnar_0.4 | 0.574 (-0.061) | 0.082 (-0.020) | 0.126 (-0.075) | 0.205 (-0.256) | 0.154 (-0.179) | 0.077 (-0.077) | 54.500 (+0.000) | 0.224 (-0.164) | 0.150 (-0.045) | 0.796 (+0.088) | 0.203 (-0.108) | 0.055 (+0.000) | 0.008 (+0.006) | 0.042 (+0.007) | 0.281 (+0.169) |
| sensor_fail_0.3 | 0.564 (-0.071) | 0.089 (-0.012) | 0.102 (-0.099) | 0.231 (-0.231) | 0.128 (-0.205) | 0.051 (-0.103) | 38.000 (-16.500) | 0.144 (-0.244) | 0.200 (+0.005) | 0.847 (+0.139) | 0.228 (-0.082) | 0.058 (+0.003) | 0.015 (+0.013) | 0.052 (+0.016) | 0.520 (+0.407) |
| with_pulse_drop_pulse | 0.637 (+0.002) | 0.103 (+0.001) | 0.214 (+0.013) | 0.564 (+0.103) | 0.385 (+0.051) | 0.154 (+0.000) | 54.500 (+0.000) | 0.506 (+0.117) | 0.196 (+0.001) | 0.653 (-0.054) | 0.336 (+0.026) | 0.055 (-0.000) | 0.003 (+0.001) | 0.036 (+0.000) | 0.114 (+0.001) |

## Fairness (E8): by skin_ita tercile

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (-40.1, 5.7] | 80 | 14 | 0.649 | 0.115 | 0.138 | 0.286 | 0.143 | 0.071 | 34.500 | 0.277 | 0.222 | 0.788 | 0.250 | 0.062 | 0.014 | 0.037 | 0.238 |
| (5.7, 37.4] | 80 | 14 | 0.629 | 0.105 | 0.189 | 0.500 | 0.357 | 0.143 | 62.000 | 0.430 | 0.200 | 0.652 | 0.318 | 0.060 | 0.007 | 0.038 | 0.061 |
| (37.4, 70.0] | 81 | 11 | 0.657 | 0.101 | 0.307 | 0.636 | 0.545 | 0.273 | 57.000 | 0.454 | 0.172 | 0.686 | 0.350 | 0.043 | 0.019 | 0.032 | 0.044 |

## By age tercile (years): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (29.9, 41.0] | 80 | 12 | 0.642 | 0.104 | 0.165 | 0.250 | 0.167 | 0.167 | 97.000 | 0.239 | 0.188 | 0.809 | 0.214 | 0.052 | 0.003 | 0.030 | 0.132 |
| (41.0, 54.0] | 80 | 16 | 0.674 | 0.173 | 0.290 | 0.688 | 0.562 | 0.250 | 57.000 | 0.370 | 0.250 | 0.672 | 0.458 | 0.069 | 0.018 | 0.044 | 0.091 |
| (54.0, 65.0] | 81 | 11 | 0.576 | 0.054 | 0.103 | 0.364 | 0.182 | 0.000 | 26.500 | 0.551 | 0.138 | 0.643 | 0.200 | 0.044 | 0.015 | 0.032 | 0.115 |

sens_spec92 = per-WEEK sensitivity at 92% per-WEEK specificity: landmark weeks, p threshold from the y=0 weeks of the CALIBRATION people (spec_spec92_test = per-week specificity reached on test); not the system's operating point. specificity = non-converters never prompted during follow-up (median 16.6 months of monitoring after the warm-up): CUMULATIVE over follow-up, not a single-window specificity; f1 and ppv_person (person-level PPV of a prompt) at this test conversion rate of 16%; lr_pos = Se0 / share of non-converters prompted. false_prompt_6mo / 12mo = Kaplan-Meier probability that a non-converter has >= 1 false prompt by 6 / 12 months of monitoring (day 0 = first landmark week, censored at end of follow-up). alarms_per_nonconv_py: per calendar person-year (warm-up included); alarms_per_nonconv_monitored_py: per monitored (post-warm-up) person-year. prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year after a 26-week refractory period (chosen to equal the 26-week prediction horizon; not the clinical panel rule of 13 weeks after a normal cuff series). It is a burden metric only: first warnings, every other metric, the tuned thresholds and the chance floor use the unsuppressed episodes. sens_post_onset_30/90 = Se30/Se90 counting a first warning before the simulated drift onset as a miss (n_pre_onset_first_warnings = how many); sens_lead_* count every warning before t_ref.

## Early-warning operating curve: sensitivity at >= 90 d lead (alarms/non-converter-yr) per warning budget

| budget | full | level_only | cuff_only | with_pulse | chance |
|---|---|---|---|---|---|
| 0.25 | 0.077 (0.164) | 0.051 (0.084) | 0.051 (0.097) | 0.051 (0.151) | 0.141 (0.250) |
| 0.5 | 0.154 (0.388) | 0.103 (0.261) | 0.179 (0.305) | 0.179 (0.482) | 0.260 (0.500) |
| 1.0 | 0.359 (0.964) | 0.256 (0.750) | 0.308 (0.847) | 0.333 (0.917) | 0.446 (1.000) |
| 2.0 | 0.462 (1.212) | 0.462 (1.212) | 0.462 (1.212) | 0.462 (1.165) | 0.680 (2.000) |

## Example evidence ledger (first warning of a warned converter)

```json
{
  "pid": "P0078",
  "week": 43,
  "first_warning_day": 307.0,
  "lead_days": 52.0,
  "state": "WARNING",
  "p": 0.10478699401183084,
  "p_lo": 0.08526580062418435,
  "p_hi": 0.12302271520156673,
  "weeks_exceeded": "4/5",
  "episodes": 1,
  "dev_slope12": 0.07103770598194893,
  "channel_contrib": {
    "night_rhr": 0.5177656203509295,
    "night_rmssd": 0.40680329395521114,
    "still_hr": 1.6157456599684399,
    "steps": -0.011571512247913689,
    "sleep_dur": -0.09376500410739759,
    "sleep_reg": 0.49223937558546343
  },
  "valid_days_30": 22,
  "ctx_masked_6w": 12,
  "month": 12
}
```

Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`.

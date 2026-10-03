# SENTINEL-HTN results

Run: n=1200, days=540, seed=1, n_boot=20. Test people: 240 (45 converters). Thresholds: persistence dev > 0.150, warning p_lo >= 0.095. Synthetic data unless stated; research prototype, not a diagnostic; no blood-pressure value is output.

## Main model (metrics A-F, held-out test people)

| set | metric | value |
|---|---|---|
| A | auroc | 0.596 |
| A | auprc | 0.109 |
| A | sens_spec92 | 0.160 |
| A | spec_spec92_test | 0.937 |
| A | thr_spec92 | 0.095 |
| B | sens_lead_0 | 0.444 |
| B | sens_lead_30 | 0.244 |
| B | sens_lead_90 | 0.133 |
| B | sens_lead_180 | 0.067 |
| B | median_lead | 35.500 |
| B | sens_post_onset_30 | 0.178 |
| B | sens_post_onset_90 | 0.089 |
| B | n_pre_onset_first_warnings | 3.000 |
| C | alarms_per_nonconv_py | 0.368 |
| C | alarms_per_nonconv_monitored_py | 0.395 |
| C | prompts_per_nonconv_py_r26 | 0.243 |
| C | warning_precision | 0.202 |
| C | specificity | 0.672 |
| C | f1 | 0.310 |
| C | ppv_person | 0.238 |
| C | lr_pos | 1.354 |
| C | false_prompt_6mo | 0.092 |
| C | false_prompt_12mo | 0.210 |
| C | followup_median_days | 504.000 |
| C | false_prompts_per_nonconv | 0.544 |
| D | brier | 0.064 |
| D | ece | 0.005 |
| F | aurc | 0.050 |
| F | abstention_rate | 0.107 |

## Ablations vs full (delta vs full in parentheses)

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full | 0.596 | 0.109 | 0.160 | 0.444 | 0.244 | 0.133 | 35.500 | 0.368 | 0.202 | 0.672 | 0.310 | 0.064 | 0.005 | 0.050 | 0.107 |
| level_only | 0.500 (-0.096) | 0.070 (-0.039) | 0.000 (-0.160) | 0.000 (-0.444) | 0.000 (-0.244) | 0.000 (-0.133) | n/a | 0.000 (-0.368) | n/a | 1.000 (+0.328) | 0.000 (-0.310) | 0.065 (+0.001) | 0.000 (-0.005) | 0.061 (+0.011) | 0.104 (-0.003) |
| cuff_only | 0.553 (-0.044) | 0.079 (-0.030) | 0.076 (-0.084) | 0.333 (-0.111) | 0.156 (-0.089) | 0.022 (-0.111) | 25.000 (-10.500) | 0.361 (-0.007) | 0.179 (-0.023) | 0.677 (+0.005) | 0.244 (-0.066) | 0.065 (+0.001) | 0.000 (-0.005) | 0.061 (+0.011) | 0.106 (-0.000) |
| change_only | 0.593 (-0.003) | 0.111 (+0.001) | 0.152 (-0.008) | 0.378 (-0.067) | 0.267 (+0.022) | 0.133 (+0.000) | 55.000 (+19.500) | 0.437 (+0.069) | 0.158 (-0.044) | 0.600 (-0.072) | 0.243 (-0.067) | 0.064 (-0.000) | 0.003 (-0.002) | 0.055 (+0.005) | 0.107 (+0.000) |
| no_personalisation | 0.546 (-0.050) | 0.088 (-0.021) | 0.133 (-0.027) | 0.400 (-0.044) | 0.267 (+0.022) | 0.200 (+0.067) | 87.500 (+52.000) | 0.302 (-0.066) | 0.183 (-0.019) | 0.728 (+0.056) | 0.310 (+0.000) | 0.065 (+0.000) | 0.001 (-0.004) | 0.049 (-0.001) | 0.106 (-0.001) |
| no_context | 0.519 (-0.077) | 0.077 (-0.032) | 0.097 (-0.062) | 0.111 (-0.333) | 0.067 (-0.178) | 0.067 (-0.067) | 180.000 (+144.500) | 0.118 (-0.250) | 0.107 (-0.095) | 0.882 (+0.210) | 0.137 (-0.173) | 0.065 (+0.001) | 0.001 (-0.004) | 0.056 (+0.006) | 0.104 (-0.002) |
| equal_weights | 0.600 (+0.004) | 0.108 (-0.001) | 0.145 (-0.014) | 0.400 (-0.044) | 0.244 (+0.000) | 0.156 (+0.022) | 60.500 (+25.000) | 0.316 (-0.052) | 0.211 (+0.009) | 0.728 (+0.056) | 0.310 (+0.000) | 0.064 (+0.000) | 0.004 (-0.001) | 0.050 (-0.000) | 0.106 (-0.000) |
| reliability_only | 0.580 (-0.016) | 0.101 (-0.008) | 0.130 (-0.030) | 0.356 (-0.089) | 0.222 (-0.022) | 0.156 (+0.022) | 47.000 (+11.500) | 0.357 (-0.010) | 0.141 (-0.061) | 0.646 (-0.026) | 0.246 (-0.064) | 0.065 (+0.000) | 0.001 (-0.004) | 0.052 (+0.002) | 0.106 (-0.000) |
| with_pulse | 0.595 (-0.001) | 0.109 (-0.000) | 0.153 (-0.006) | 0.378 (-0.067) | 0.244 (+0.000) | 0.156 (+0.022) | 55.000 (+19.500) | 0.399 (+0.031) | 0.153 (-0.049) | 0.651 (-0.021) | 0.262 (-0.049) | 0.064 (-0.000) | 0.005 (-0.000) | 0.051 (+0.001) | 0.107 (+0.000) |

## Robustness (E): test people perturbed, models fitted on clean data

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.596 | 0.109 | 0.160 | 0.444 | 0.244 | 0.133 | 35.500 | 0.368 | 0.202 | 0.672 | 0.310 | 0.064 | 0.005 | 0.050 | 0.107 |
| mcar_0.3 | 0.602 (+0.006) | 0.116 (+0.007) | 0.173 (+0.014) | 0.400 (-0.044) | 0.311 (+0.067) | 0.200 (+0.067) | 96.500 (+61.000) | 0.434 (+0.066) | 0.163 (-0.039) | 0.621 (-0.051) | 0.263 (-0.047) | 0.064 (-0.000) | 0.005 (-0.000) | 0.050 (-0.000) | 0.106 (-0.000) |
| mcar_0.6 | 0.552 (-0.044) | 0.099 (-0.010) | 0.170 (+0.010) | 0.289 (-0.156) | 0.244 (+0.000) | 0.111 (-0.022) | 78.000 (+42.500) | 0.413 (+0.045) | 0.111 (-0.091) | 0.605 (-0.067) | 0.193 (-0.117) | 0.065 (+0.001) | 0.004 (-0.001) | 0.050 (+0.000) | 0.137 (+0.030) |
| noise_1.0 | 0.588 (-0.008) | 0.102 (-0.008) | 0.186 (+0.026) | 0.378 (-0.067) | 0.311 (+0.067) | 0.178 (+0.044) | 73.000 (+37.500) | 0.604 (+0.236) | 0.120 (-0.082) | 0.533 (-0.138) | 0.222 (-0.088) | 0.065 (+0.000) | 0.003 (-0.002) | 0.055 (+0.005) | 0.107 (+0.001) |
| drop_night_rmssd | 0.580 (-0.016) | 0.099 (-0.010) | 0.118 (-0.042) | 0.378 (-0.067) | 0.222 (-0.022) | 0.133 (+0.000) | 39.000 (+3.500) | 0.298 (-0.069) | 0.192 (-0.011) | 0.713 (+0.041) | 0.288 (-0.022) | 0.065 (+0.000) | 0.002 (-0.003) | 0.053 (+0.003) | 0.106 (-0.001) |
| mnar_0.4 | 0.537 (-0.059) | 0.080 (-0.029) | 0.093 (-0.067) | 0.089 (-0.356) | 0.067 (-0.178) | 0.044 (-0.089) | 124.000 (+88.500) | 0.197 (-0.170) | 0.094 (-0.109) | 0.826 (+0.154) | 0.104 (-0.206) | 0.057 (-0.007) | 0.005 (-0.000) | 0.048 (-0.002) | 0.335 (+0.229) |
| sensor_fail_0.3 | 0.561 (-0.035) | 0.105 (-0.004) | 0.092 (-0.068) | 0.156 (-0.289) | 0.156 (-0.089) | 0.089 (-0.044) | 91.000 (+55.500) | 0.163 (-0.205) | 0.150 (-0.052) | 0.831 (+0.159) | 0.165 (-0.145) | 0.067 (+0.003) | 0.011 (+0.006) | 0.051 (+0.001) | 0.505 (+0.398) |
| with_pulse_drop_pulse | 0.599 (+0.003) | 0.112 (+0.003) | 0.175 (+0.015) | 0.422 (-0.022) | 0.289 (+0.044) | 0.156 (+0.022) | 55.000 (+19.500) | 0.413 (+0.045) | 0.176 (-0.027) | 0.631 (-0.041) | 0.279 (-0.031) | 0.064 (-0.000) | 0.006 (+0.001) | 0.051 (+0.001) | 0.107 (+0.000) |

## Fairness (E8): by skin_ita tercile

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (-40.1, 9.6] | 80 | 23 | 0.581 | 0.165 | 0.083 | 0.348 | 0.087 | 0.043 | 21.000 | 0.166 | 0.412 | 0.842 | 0.400 | 0.102 | 0.048 | 0.076 | 0.229 |
| (9.6, 33.7] | 80 | 10 | 0.685 | 0.114 | 0.282 | 0.700 | 0.500 | 0.200 | 39.000 | 0.522 | 0.179 | 0.543 | 0.286 | 0.043 | 0.031 | 0.036 | 0.056 |
| (33.7, 70.0] | 80 | 12 | 0.624 | 0.095 | 0.199 | 0.417 | 0.333 | 0.250 | 115.000 | 0.378 | 0.107 | 0.662 | 0.250 | 0.052 | 0.020 | 0.040 | 0.046 |

## By age tercile (years): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (29.9, 40.0] | 86 | 17 | 0.665 | 0.198 | 0.172 | 0.529 | 0.353 | 0.118 | 39.000 | 0.206 | 0.348 | 0.797 | 0.450 | 0.067 | 0.008 | 0.052 | 0.120 |
| (40.0, 53.0] | 75 | 14 | 0.562 | 0.114 | 0.188 | 0.357 | 0.214 | 0.214 | 122.000 | 0.421 | 0.103 | 0.607 | 0.233 | 0.065 | 0.009 | 0.049 | 0.104 |
| (53.0, 65.0] | 79 | 14 | 0.551 | 0.075 | 0.115 | 0.429 | 0.143 | 0.071 | 22.000 | 0.489 | 0.188 | 0.600 | 0.261 | 0.061 | 0.006 | 0.050 | 0.094 |

sens_spec92 = per-WEEK sensitivity at 92% per-WEEK specificity: landmark weeks, p threshold from the y=0 weeks of the CALIBRATION people (spec_spec92_test = per-week specificity reached on test); not the system's operating point. specificity = non-converters never prompted during follow-up (median 16.6 months of monitoring after the warm-up): CUMULATIVE over follow-up, not a single-window specificity; f1 and ppv_person (person-level PPV of a prompt) at this test conversion rate of 19%; lr_pos = Se0 / share of non-converters prompted. false_prompt_6mo / 12mo = Kaplan-Meier probability that a non-converter has >= 1 false prompt by 6 / 12 months of monitoring (day 0 = first landmark week, censored at end of follow-up). alarms_per_nonconv_py: per calendar person-year (warm-up included); alarms_per_nonconv_monitored_py: per monitored (post-warm-up) person-year. prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year after a 26-week refractory period (chosen to equal the 26-week prediction horizon; not the clinical panel rule of 13 weeks after a normal cuff series). It is a burden metric only: first warnings, every other metric, the tuned thresholds and the chance floor use the unsuppressed episodes. sens_post_onset_30/90 = Se30/Se90 counting a first warning before the simulated drift onset as a miss (n_pre_onset_first_warnings = how many); sens_lead_* count every warning before t_ref.

## Early-warning operating curve: sensitivity at >= 90 d lead (alarms/non-converter-yr) per warning budget

| budget | full | level_only | cuff_only | with_pulse | chance |
|---|---|---|---|---|---|
| 0.25 | 0.089 (0.160) | 0.000 (0.000) | 0.000 (0.021) | 0.067 (0.125) | 0.128 (0.250) |
| 0.5 | 0.133 (0.368) | 0.000 (0.000) | 0.022 (0.361) | 0.156 (0.399) | 0.238 (0.500) |
| 1.0 | 0.200 (0.680) | 0.000 (0.000) | 0.022 (0.361) | 0.200 (0.708) | 0.413 (1.000) |
| 2.0 | 0.400 (1.249) | 0.400 (1.249) | 0.400 (1.249) | 0.267 (1.193) | 0.640 (2.000) |

## Example evidence ledger (first warning of a warned converter)

```json
{
  "pid": "P0001",
  "week": 55,
  "first_warning_day": 391.0,
  "lead_days": 32.0,
  "state": "WARNING",
  "p": 0.10440172371955811,
  "p_lo": 0.09537464426823102,
  "p_hi": 0.11800524123860823,
  "weeks_exceeded": "4/6",
  "episodes": 4,
  "dev_slope12": 0.024421967305046394,
  "channel_contrib": {
    "night_rhr": 0.5086868710583471,
    "night_rmssd": 0.5829846102948238,
    "still_hr": 0.8254580590127174,
    "steps": 0.14393711930696296,
    "sleep_dur": 0.1057594900180816,
    "sleep_reg": -0.20062245136967916
  },
  "valid_days_30": 25,
  "ctx_masked_6w": 14,
  "month": 7
}
```

Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`.

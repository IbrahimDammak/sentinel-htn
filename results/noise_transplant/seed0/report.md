# SENTINEL-HTN results

Run: n=1200, days=540, seed=0, n_boot=20. Test people: 241 (41 converters). Thresholds: persistence dev > 0.150, warning p_lo >= 0.085. Synthetic data unless stated; research prototype, not a diagnostic; no blood-pressure value is output.

## Main model (metrics A-F, held-out test people)

| set | metric | value |
|---|---|---|
| A | auroc | 0.639 |
| A | auprc | 0.111 |
| A | sens_spec92 | 0.207 |
| A | spec_spec92_test | 0.916 |
| A | thr_spec92 | 0.110 |
| B | sens_lead_0 | 0.488 |
| B | sens_lead_30 | 0.366 |
| B | sens_lead_90 | 0.220 |
| B | sens_lead_180 | 0.073 |
| B | median_lead | 77.500 |
| B | sens_post_onset_30 | 0.268 |
| B | sens_post_onset_90 | 0.146 |
| B | n_pre_onset_first_warnings | 4.000 |
| C | alarms_per_nonconv_py | 0.419 |
| C | alarms_per_nonconv_monitored_py | 0.453 |
| C | prompts_per_nonconv_py_r26 | 0.277 |
| C | warning_precision | 0.189 |
| C | specificity | 0.625 |
| C | f1 | 0.294 |
| C | ppv_person | 0.211 |
| C | lr_pos | 1.301 |
| C | false_prompt_6mo | 0.070 |
| C | false_prompt_12mo | 0.210 |
| C | followup_median_days | 504.000 |
| C | false_prompts_per_nonconv | 0.620 |
| D | brier | 0.059 |
| D | ece | 0.003 |
| F | aurc | 0.041 |
| F | abstention_rate | 0.113 |

## Ablations vs full (delta vs full in parentheses)

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full | 0.639 | 0.111 | 0.207 | 0.488 | 0.366 | 0.220 | 77.500 | 0.419 | 0.189 | 0.625 | 0.294 | 0.059 | 0.003 | 0.041 | 0.113 |
| level_only | 0.562 (-0.077) | 0.077 (-0.034) | 0.074 (-0.134) | 0.390 (-0.098) | 0.293 (-0.073) | 0.220 (+0.000) | 175.500 (+98.000) | 0.321 (-0.098) | 0.141 (-0.049) | 0.760 (+0.135) | 0.305 (+0.011) | 0.060 (+0.001) | 0.003 (+0.001) | 0.059 (+0.018) | 0.112 (-0.001) |
| cuff_only | 0.523 (-0.116) | 0.073 (-0.038) | 0.096 (-0.111) | 0.293 (-0.195) | 0.195 (-0.171) | 0.195 (-0.024) | 168.000 (+90.500) | 0.206 (-0.213) | 0.109 (-0.080) | 0.785 (+0.160) | 0.250 (-0.044) | 0.060 (+0.001) | 0.002 (-0.000) | 0.053 (+0.012) | 0.111 (-0.002) |
| change_only | 0.623 (-0.017) | 0.114 (+0.003) | 0.246 (+0.039) | 0.512 (+0.024) | 0.366 (+0.000) | 0.244 (+0.024) | 88.000 (+10.500) | 0.507 (+0.088) | 0.171 (-0.018) | 0.550 (-0.075) | 0.276 (-0.018) | 0.059 (+0.000) | 0.003 (-0.000) | 0.046 (+0.005) | 0.114 (+0.000) |
| no_personalisation | 0.624 (-0.016) | 0.103 (-0.008) | 0.173 (-0.034) | 0.317 (-0.171) | 0.268 (-0.098) | 0.171 (-0.049) | 117.000 (+39.500) | 0.372 (-0.047) | 0.143 (-0.047) | 0.750 (+0.125) | 0.250 (-0.044) | 0.060 (+0.000) | 0.004 (+0.001) | 0.045 (+0.004) | 0.112 (-0.001) |
| no_context | 0.591 (-0.048) | 0.089 (-0.023) | 0.119 (-0.088) | 0.463 (-0.024) | 0.293 (-0.073) | 0.171 (-0.049) | 62.000 (-15.500) | 0.358 (-0.061) | 0.190 (+0.001) | 0.675 (+0.050) | 0.304 (+0.010) | 0.060 (+0.001) | 0.002 (-0.000) | 0.053 (+0.012) | 0.112 (-0.001) |
| equal_weights | 0.650 (+0.011) | 0.112 (+0.000) | 0.206 (-0.001) | 0.537 (+0.049) | 0.366 (+0.000) | 0.220 (+0.000) | 61.500 (-16.000) | 0.473 (+0.054) | 0.190 (+0.001) | 0.610 (-0.015) | 0.312 (+0.018) | 0.059 (-0.000) | 0.004 (+0.001) | 0.039 (-0.003) | 0.113 (+0.000) |
| reliability_only | 0.633 (-0.007) | 0.108 (-0.003) | 0.213 (+0.006) | 0.439 (-0.049) | 0.415 (+0.049) | 0.317 (+0.098) | 111.500 (+34.000) | 0.433 (+0.014) | 0.146 (-0.044) | 0.610 (-0.015) | 0.263 (-0.031) | 0.059 (+0.000) | 0.003 (+0.000) | 0.042 (+0.001) | 0.113 (-0.000) |
| with_pulse | 0.633 (-0.006) | 0.114 (+0.003) | 0.216 (+0.009) | 0.512 (+0.024) | 0.390 (+0.024) | 0.244 (+0.024) | 81.000 (+3.500) | 0.467 (+0.047) | 0.176 (-0.013) | 0.595 (-0.030) | 0.294 (-0.000) | 0.059 (-0.000) | 0.003 (+0.000) | 0.041 (+0.000) | 0.113 (+0.000) |

## Robustness (E): test people perturbed, models fitted on clean data

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.639 | 0.111 | 0.207 | 0.488 | 0.366 | 0.220 | 77.500 | 0.419 | 0.189 | 0.625 | 0.294 | 0.059 | 0.003 | 0.041 | 0.113 |
| mcar_0.3 | 0.604 (-0.035) | 0.097 (-0.014) | 0.197 (-0.011) | 0.366 (-0.122) | 0.268 (-0.098) | 0.171 (-0.049) | 58.000 (-19.500) | 0.446 (+0.027) | 0.118 (-0.072) | 0.565 (-0.060) | 0.210 (-0.084) | 0.060 (+0.001) | 0.006 (+0.003) | 0.044 (+0.003) | 0.113 (-0.000) |
| mcar_0.6 | 0.606 (-0.034) | 0.092 (-0.019) | 0.237 (+0.030) | 0.390 (-0.098) | 0.341 (-0.024) | 0.244 (+0.024) | 145.500 (+68.000) | 0.382 (-0.037) | 0.103 (-0.086) | 0.595 (-0.030) | 0.232 (-0.062) | 0.062 (+0.002) | 0.019 (+0.016) | 0.046 (+0.004) | 0.146 (+0.033) |
| noise_1.0 | 0.640 (+0.001) | 0.112 (+0.001) | 0.270 (+0.063) | 0.537 (+0.049) | 0.390 (+0.024) | 0.268 (+0.049) | 92.500 (+15.000) | 0.727 (+0.308) | 0.137 (-0.053) | 0.415 (-0.210) | 0.244 (-0.050) | 0.060 (+0.000) | 0.012 (+0.009) | 0.039 (-0.002) | 0.115 (+0.001) |
| drop_night_rmssd | 0.633 (-0.006) | 0.110 (-0.002) | 0.190 (-0.017) | 0.390 (-0.098) | 0.341 (-0.024) | 0.220 (+0.000) | 104.000 (+26.500) | 0.409 (-0.010) | 0.146 (-0.043) | 0.635 (+0.010) | 0.246 (-0.048) | 0.059 (+0.000) | 0.003 (+0.001) | 0.043 (+0.001) | 0.113 (-0.000) |
| mnar_0.4 | 0.591 (-0.048) | 0.143 (+0.031) | 0.216 (+0.009) | 0.317 (-0.171) | 0.244 (-0.122) | 0.146 (-0.073) | 70.000 (-7.500) | 0.265 (-0.154) | 0.220 (+0.031) | 0.758 (+0.133) | 0.286 (-0.008) | 0.066 (+0.007) | 0.013 (+0.010) | 0.055 (+0.014) | 0.326 (+0.213) |
| sensor_fail_0.3 | 0.608 (-0.031) | 0.104 (-0.007) | 0.168 (-0.039) | 0.341 (-0.146) | 0.220 (-0.146) | 0.098 (-0.122) | 45.000 (-32.500) | 0.193 (-0.227) | 0.224 (+0.035) | 0.780 (+0.155) | 0.283 (-0.011) | 0.062 (+0.002) | 0.010 (+0.008) | 0.050 (+0.009) | 0.530 (+0.417) |
| with_pulse_drop_pulse | 0.637 (-0.003) | 0.110 (-0.001) | 0.207 (+0.000) | 0.512 (+0.024) | 0.390 (+0.024) | 0.268 (+0.049) | 96.000 (+18.500) | 0.504 (+0.085) | 0.162 (-0.028) | 0.580 (-0.045) | 0.288 (-0.006) | 0.059 (+0.000) | 0.004 (+0.001) | 0.041 (-0.001) | 0.114 (+0.000) |

## Fairness (E8): by skin_ita tercile

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (-40.1, 7.1] | 80 | 10 | 0.605 | 0.062 | 0.143 | 0.200 | 0.200 | 0.200 | 132.000 | 0.377 | 0.069 | 0.614 | 0.103 | 0.046 | 0.018 | 0.033 | 0.235 |
| (7.1, 31.2] | 80 | 14 | 0.664 | 0.140 | 0.212 | 0.500 | 0.357 | 0.286 | 96.000 | 0.461 | 0.156 | 0.621 | 0.304 | 0.060 | 0.004 | 0.036 | 0.060 |
| (31.2, 70.0] | 81 | 17 | 0.644 | 0.168 | 0.241 | 0.647 | 0.471 | 0.176 | 67.000 | 0.423 | 0.324 | 0.641 | 0.431 | 0.072 | 0.018 | 0.052 | 0.044 |

## By age tercile (years): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (29.9, 41.0] | 81 | 18 | 0.633 | 0.137 | 0.152 | 0.500 | 0.389 | 0.222 | 85.000 | 0.419 | 0.250 | 0.635 | 0.360 | 0.079 | 0.028 | 0.053 | 0.092 |
| (41.0, 54.0] | 83 | 9 | 0.614 | 0.055 | 0.137 | 0.556 | 0.444 | 0.333 | 96.000 | 0.302 | 0.154 | 0.716 | 0.286 | 0.039 | 0.023 | 0.029 | 0.118 |
| (54.0, 65.0] | 77 | 14 | 0.678 | 0.161 | 0.323 | 0.429 | 0.286 | 0.143 | 65.000 | 0.558 | 0.162 | 0.508 | 0.235 | 0.062 | 0.008 | 0.042 | 0.130 |

sens_spec92 = per-WEEK sensitivity at 92% per-WEEK specificity: landmark weeks, p threshold from the y=0 weeks of the CALIBRATION people (spec_spec92_test = per-week specificity reached on test); not the system's operating point. specificity = non-converters never prompted during follow-up (median 16.6 months of monitoring after the warm-up): CUMULATIVE over follow-up, not a single-window specificity; f1 and ppv_person (person-level PPV of a prompt) at this test conversion rate of 17%; lr_pos = Se0 / share of non-converters prompted. false_prompt_6mo / 12mo = Kaplan-Meier probability that a non-converter has >= 1 false prompt by 6 / 12 months of monitoring (day 0 = first landmark week, censored at end of follow-up). alarms_per_nonconv_py: per calendar person-year (warm-up included); alarms_per_nonconv_monitored_py: per monitored (post-warm-up) person-year. prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year after a 26-week refractory period (chosen to equal the 26-week prediction horizon; not the clinical panel rule of 13 weeks after a normal cuff series). It is a burden metric only: first warnings, every other metric, the tuned thresholds and the chance floor use the unsuppressed episodes. sens_post_onset_30/90 = Se30/Se90 counting a first warning before the simulated drift onset as a miss (n_pre_onset_first_warnings = how many); sens_lead_* count every warning before t_ref.

## Early-warning operating curve: sensitivity at >= 90 d lead (alarms/non-converter-yr) per warning budget

| budget | full | level_only | cuff_only | with_pulse | chance |
|---|---|---|---|---|---|
| 0.25 | 0.098 (0.281) | 0.098 (0.166) | 0.195 (0.206) | 0.098 (0.301) | 0.131 (0.250) |
| 0.5 | 0.220 (0.419) | 0.220 (0.321) | 0.195 (0.206) | 0.244 (0.467) | 0.244 (0.500) |
| 1.0 | 0.390 (0.947) | 0.317 (0.588) | 0.341 (0.517) | 0.390 (0.893) | 0.424 (1.000) |
| 2.0 | 0.488 (1.265) | 0.488 (1.265) | 0.488 (1.265) | 0.537 (1.201) | 0.658 (2.000) |

## Example evidence ledger (first warning of a warned converter)

```json
{
  "pid": "P0341",
  "week": 37,
  "first_warning_day": 265.0,
  "lead_days": 85.0,
  "state": "WARNING",
  "p": 0.10568226915786645,
  "p_lo": 0.08745667024883486,
  "p_hi": 0.13827852310128644,
  "weeks_exceeded": "6/6",
  "episodes": 2,
  "dev_slope12": -0.0047954267116586,
  "channel_contrib": {
    "night_rhr": 0.5749994938082518,
    "night_rmssd": 0.7498767910647822,
    "still_hr": 0.8823939941261143,
    "steps": 0.11178897271443143,
    "sleep_dur": -0.1671096203618225,
    "sleep_reg": 0.6835916376306815
  },
  "valid_days_30": 26,
  "ctx_masked_6w": 11,
  "month": 12
}
```

Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`.

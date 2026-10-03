# SENTINEL-HTN results

Run: n=1200, days=540, seed=0, n_boot=20. Test people: 241 (41 converters). Thresholds: persistence dev > 0.150, warning p_lo >= 0.090. Synthetic data unless stated; research prototype, not a diagnostic; no blood-pressure value is output.

## Main model (metrics A-F, held-out test people)

| set | metric | value |
|---|---|---|
| A | auroc | 0.632 |
| A | auprc | 0.126 |
| A | sens_spec92 | 0.221 |
| A | spec_spec92_test | 0.922 |
| A | thr_spec92 | 0.102 |
| B | sens_lead_0 | 0.537 |
| B | sens_lead_30 | 0.366 |
| B | sens_lead_90 | 0.244 |
| B | sens_lead_180 | 0.049 |
| B | median_lead | 69.500 |
| B | sens_post_onset_30 | 0.317 |
| B | sens_post_onset_90 | 0.195 |
| B | n_pre_onset_first_warnings | 2.000 |
| C | alarms_per_nonconv_py | 0.446 |
| C | alarms_per_nonconv_monitored_py | 0.483 |
| C | prompts_per_nonconv_py_r26 | 0.291 |
| C | warning_precision | 0.200 |
| C | specificity | 0.610 |
| C | f1 | 0.312 |
| C | ppv_person | 0.220 |
| C | lr_pos | 1.376 |
| C | false_prompt_6mo | 0.110 |
| C | false_prompt_12mo | 0.260 |
| C | followup_median_days | 504.000 |
| C | false_prompts_per_nonconv | 0.660 |
| D | brier | 0.059 |
| D | ece | 0.003 |
| F | aurc | 0.046 |
| F | abstention_rate | 0.113 |

## Ablations vs full (delta vs full in parentheses)

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| full | 0.632 | 0.126 | 0.221 | 0.537 | 0.366 | 0.244 | 69.500 | 0.446 | 0.200 | 0.610 | 0.312 | 0.059 | 0.003 | 0.046 | 0.113 |
| level_only | 0.562 (-0.070) | 0.077 (-0.049) | 0.075 (-0.146) | 0.341 (-0.195) | 0.244 (-0.122) | 0.171 (-0.073) | 81.000 (+11.500) | 0.277 (-0.169) | 0.150 (-0.050) | 0.770 (+0.160) | 0.277 (-0.035) | 0.060 (+0.001) | 0.003 (-0.000) | 0.060 (+0.015) | 0.112 (-0.001) |
| cuff_only | 0.523 (-0.109) | 0.073 (-0.053) | 0.096 (-0.125) | 0.463 (-0.073) | 0.268 (-0.098) | 0.220 (-0.024) | 43.000 (-26.500) | 0.382 (-0.064) | 0.174 (-0.026) | 0.665 (+0.055) | 0.299 (-0.013) | 0.060 (+0.001) | 0.002 (-0.001) | 0.053 (+0.007) | 0.113 (-0.000) |
| change_only | 0.624 (-0.008) | 0.118 (-0.008) | 0.209 (-0.012) | 0.463 (-0.073) | 0.317 (-0.049) | 0.171 (-0.073) | 61.000 (-8.500) | 0.551 (+0.105) | 0.158 (-0.042) | 0.525 (-0.085) | 0.245 (-0.067) | 0.059 (+0.000) | 0.002 (-0.001) | 0.046 (+0.000) | 0.114 (+0.000) |
| no_personalisation | 0.610 (-0.022) | 0.102 (-0.024) | 0.154 (-0.067) | 0.268 (-0.268) | 0.171 (-0.195) | 0.122 (-0.122) | 81.000 (+11.500) | 0.375 (-0.071) | 0.113 (-0.087) | 0.745 (+0.135) | 0.214 (-0.098) | 0.060 (+0.001) | 0.003 (+0.000) | 0.049 (+0.003) | 0.113 (-0.000) |
| no_context | 0.574 (-0.058) | 0.089 (-0.037) | 0.107 (-0.113) | 0.366 (-0.171) | 0.244 (-0.122) | 0.171 (-0.073) | 57.000 (-12.500) | 0.298 (-0.149) | 0.167 (-0.033) | 0.775 (+0.165) | 0.297 (-0.015) | 0.060 (+0.001) | 0.003 (-0.001) | 0.059 (+0.014) | 0.112 (-0.001) |
| equal_weights | 0.613 (-0.019) | 0.109 (-0.017) | 0.188 (-0.033) | 0.512 (-0.024) | 0.341 (-0.024) | 0.146 (-0.098) | 41.000 (-28.500) | 0.470 (+0.024) | 0.196 (-0.004) | 0.620 (+0.010) | 0.304 (-0.008) | 0.060 (+0.000) | 0.003 (+0.000) | 0.049 (+0.003) | 0.113 (+0.000) |
| reliability_only | 0.619 (-0.013) | 0.113 (-0.013) | 0.208 (-0.013) | 0.512 (-0.024) | 0.390 (+0.024) | 0.220 (-0.024) | 81.000 (+11.500) | 0.497 (+0.051) | 0.178 (-0.022) | 0.600 (-0.010) | 0.296 (-0.016) | 0.060 (+0.000) | 0.004 (+0.000) | 0.046 (+0.000) | 0.113 (+0.000) |
| with_pulse | 0.628 (-0.004) | 0.129 (+0.003) | 0.225 (+0.004) | 0.512 (-0.024) | 0.341 (-0.024) | 0.293 (+0.049) | 99.000 (+29.500) | 0.446 (+0.000) | 0.176 (-0.024) | 0.595 (-0.015) | 0.294 (-0.018) | 0.059 (-0.000) | 0.004 (+0.000) | 0.046 (+0.000) | 0.113 (+0.000) |

## Robustness (E): test people perturbed, models fitted on clean data

| run | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clean | 0.632 | 0.126 | 0.221 | 0.537 | 0.366 | 0.244 | 69.500 | 0.446 | 0.200 | 0.610 | 0.312 | 0.059 | 0.003 | 0.046 | 0.113 |
| mcar_0.3 | 0.592 (-0.040) | 0.108 (-0.018) | 0.239 (+0.018) | 0.585 (+0.049) | 0.463 (+0.098) | 0.317 (+0.073) | 99.000 (+29.500) | 0.551 (+0.105) | 0.168 (-0.032) | 0.525 (-0.085) | 0.300 (-0.012) | 0.060 (+0.001) | 0.003 (-0.001) | 0.049 (+0.003) | 0.114 (+0.001) |
| mcar_0.6 | 0.561 (-0.071) | 0.090 (-0.036) | 0.278 (+0.057) | 0.366 (-0.171) | 0.317 (-0.049) | 0.244 (+0.000) | 125.000 (+55.500) | 0.514 (+0.068) | 0.084 (-0.116) | 0.540 (-0.070) | 0.203 (-0.109) | 0.062 (+0.003) | 0.016 (+0.013) | 0.054 (+0.008) | 0.147 (+0.034) |
| noise_1.0 | 0.626 (-0.006) | 0.105 (-0.021) | 0.290 (+0.070) | 0.610 (+0.073) | 0.512 (+0.146) | 0.317 (+0.073) | 97.000 (+27.500) | 0.805 (+0.358) | 0.127 (-0.073) | 0.375 (-0.235) | 0.262 (-0.050) | 0.060 (+0.001) | 0.011 (+0.008) | 0.044 (-0.002) | 0.115 (+0.002) |
| drop_night_rmssd | 0.612 (-0.020) | 0.110 (-0.016) | 0.197 (-0.023) | 0.463 (-0.073) | 0.293 (-0.073) | 0.171 (-0.073) | 55.000 (-14.500) | 0.477 (+0.030) | 0.170 (-0.030) | 0.595 (-0.015) | 0.270 (-0.043) | 0.060 (+0.000) | 0.004 (+0.000) | 0.048 (+0.002) | 0.113 (-0.000) |
| mnar_0.4 | 0.646 (+0.014) | 0.181 (+0.055) | 0.224 (+0.003) | 0.341 (-0.195) | 0.317 (-0.049) | 0.171 (-0.073) | 94.500 (+25.000) | 0.243 (-0.203) | 0.244 (+0.044) | 0.797 (+0.187) | 0.326 (+0.014) | 0.066 (+0.006) | 0.012 (+0.009) | 0.046 (+0.000) | 0.327 (+0.214) |
| sensor_fail_0.3 | 0.640 (+0.008) | 0.137 (+0.011) | 0.246 (+0.025) | 0.415 (-0.122) | 0.317 (-0.049) | 0.098 (-0.146) | 55.000 (-14.500) | 0.186 (-0.260) | 0.276 (+0.076) | 0.795 (+0.185) | 0.343 (+0.031) | 0.061 (+0.002) | 0.009 (+0.005) | 0.045 (-0.001) | 0.530 (+0.417) |
| with_pulse_drop_pulse | 0.632 (+0.001) | 0.126 (+0.000) | 0.231 (+0.011) | 0.585 (+0.049) | 0.463 (+0.098) | 0.317 (+0.073) | 101.500 (+32.000) | 0.477 (+0.030) | 0.170 (-0.030) | 0.590 (-0.020) | 0.327 (+0.014) | 0.059 (-0.000) | 0.003 (-0.001) | 0.045 (-0.001) | 0.114 (+0.000) |

## Fairness (E8): by skin_ita tercile

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (-40.1, 7.1] | 80 | 10 | 0.490 | 0.047 | 0.084 | 0.300 | 0.100 | 0.000 | 27.000 | 0.348 | 0.115 | 0.671 | 0.167 | 0.047 | 0.015 | 0.049 | 0.235 |
| (7.1, 31.2] | 80 | 14 | 0.671 | 0.156 | 0.249 | 0.500 | 0.357 | 0.286 | 99.000 | 0.400 | 0.194 | 0.636 | 0.311 | 0.060 | 0.007 | 0.034 | 0.059 |
| (31.2, 70.0] | 81 | 17 | 0.687 | 0.233 | 0.278 | 0.706 | 0.529 | 0.353 | 79.500 | 0.602 | 0.256 | 0.516 | 0.400 | 0.071 | 0.018 | 0.053 | 0.045 |

## By age tercile (years): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (29.9, 41.0] | 81 | 18 | 0.588 | 0.173 | 0.196 | 0.444 | 0.333 | 0.167 | 69.500 | 0.429 | 0.258 | 0.635 | 0.327 | 0.079 | 0.028 | 0.065 | 0.092 |
| (41.0, 54.0] | 83 | 9 | 0.659 | 0.106 | 0.273 | 0.556 | 0.556 | 0.333 | 104.000 | 0.402 | 0.121 | 0.622 | 0.238 | 0.038 | 0.023 | 0.033 | 0.118 |
| (54.0, 65.0] | 77 | 14 | 0.678 | 0.127 | 0.218 | 0.643 | 0.286 | 0.286 | 27.000 | 0.515 | 0.222 | 0.571 | 0.360 | 0.063 | 0.005 | 0.042 | 0.129 |

sens_spec92 = per-WEEK sensitivity at 92% per-WEEK specificity: landmark weeks, p threshold from the y=0 weeks of the CALIBRATION people (spec_spec92_test = per-week specificity reached on test); not the system's operating point. specificity = non-converters never prompted during follow-up (median 16.6 months of monitoring after the warm-up): CUMULATIVE over follow-up, not a single-window specificity; f1 and ppv_person (person-level PPV of a prompt) at this test conversion rate of 17%; lr_pos = Se0 / share of non-converters prompted. false_prompt_6mo / 12mo = Kaplan-Meier probability that a non-converter has >= 1 false prompt by 6 / 12 months of monitoring (day 0 = first landmark week, censored at end of follow-up). alarms_per_nonconv_py: per calendar person-year (warm-up included); alarms_per_nonconv_monitored_py: per monitored (post-warm-up) person-year. prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year after a 26-week refractory period (chosen to equal the 26-week prediction horizon; not the clinical panel rule of 13 weeks after a normal cuff series). It is a burden metric only: first warnings, every other metric, the tuned thresholds and the chance floor use the unsuppressed episodes. sens_post_onset_30/90 = Se30/Se90 counting a first warning before the simulated drift onset as a miss (n_pre_onset_first_warnings = how many); sens_lead_* count every warning before t_ref.

## Early-warning operating curve: sensitivity at >= 90 d lead (alarms/non-converter-yr) per warning budget

| budget | full | level_only | cuff_only | with_pulse | chance |
|---|---|---|---|---|---|
| 0.25 | 0.098 (0.250) | 0.098 (0.129) | 0.122 (0.169) | 0.195 (0.206) | 0.131 (0.250) |
| 0.5 | 0.244 (0.446) | 0.171 (0.277) | 0.220 (0.382) | 0.293 (0.446) | 0.244 (0.500) |
| 1.0 | 0.317 (0.862) | 0.317 (0.710) | 0.317 (0.724) | 0.366 (0.873) | 0.424 (1.000) |
| 2.0 | 0.390 (1.015) | 0.390 (1.015) | 0.390 (1.015) | 0.488 (1.417) | 0.658 (2.000) |

## Example evidence ledger (first warning of a warned converter)

```json
{
  "pid": "P0841",
  "week": 43,
  "first_warning_day": 307.0,
  "lead_days": 55.0,
  "state": "WARNING",
  "p": 0.12098390979651363,
  "p_lo": 0.10455933219802364,
  "p_hi": 0.16716187064639554,
  "weeks_exceeded": "5/6",
  "episodes": 1,
  "dev_slope12": 0.05404684231682002,
  "channel_contrib": {
    "night_rhr": 0.3303991360964395,
    "night_rmssd": 0.11187008639015239,
    "still_hr": 1.3498601003443378,
    "steps": 0.17478031252289358,
    "sleep_dur": 0.3566315950883041,
    "sleep_reg": 0.8791198014839255
  },
  "valid_days_30": 19,
  "ctx_masked_6w": 15,
  "month": 10
}
```

Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`.

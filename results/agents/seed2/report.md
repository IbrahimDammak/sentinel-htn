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
| with_pulse | 0.604 (-0.001) | 0.095 (-0.003) | 0.173 (+0.000) | 0.462 (+0.000) | 0.359 (+0.026) | 0.128 (+0.000) | 51.000 (-9.500) | 0.398 (+0.007) | 0.190 (-0.017) | 0.673 (-0.010) | 0.293 (-0.005) | 0.055 (+0.000) | 0.003 (+0.000) | 0.040 (+0.000) | 0.113 (+0.000) |

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
| with_pulse_drop_pulse | 0.603 (-0.003) | 0.096 (-0.003) | 0.182 (+0.008) | 0.513 (+0.051) | 0.385 (+0.051) | 0.154 (+0.026) | 60.500 (+0.000) | 0.435 (+0.044) | 0.202 (-0.005) | 0.658 (-0.025) | 0.312 (+0.015) | 0.055 (+0.000) | 0.003 (-0.000) | 0.041 (+0.001) | 0.113 (+0.000) |

## Fairness (E8): by skin_ita tercile

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (-40.1, 5.7] | 81 | 14 | 0.609 | 0.112 | 0.150 | 0.500 | 0.357 | 0.143 | 70.000 | 0.333 | 0.259 | 0.701 | 0.341 | 0.062 | 0.014 | 0.045 | 0.239 |
| (5.7, 37.4] | 80 | 14 | 0.574 | 0.092 | 0.140 | 0.500 | 0.286 | 0.071 | 35.000 | 0.369 | 0.259 | 0.697 | 0.341 | 0.060 | 0.009 | 0.041 | 0.058 |
| (37.4, 70.0] | 80 | 11 | 0.667 | 0.105 | 0.252 | 0.364 | 0.364 | 0.182 | 107.000 | 0.471 | 0.107 | 0.652 | 0.205 | 0.044 | 0.014 | 0.033 | 0.043 |

## By age tercile (years): model behaviour by age; age has no causal role in the simulator

| run | n_people | n_converters | auroc | auprc | sens_spec92 | sens_lead_0 | sens_lead_30 | sens_lead_90 | median_lead | alarms_per_nonconv_py | warning_precision | specificity | f1 | brier | ece | aurc | abstention_rate |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (29.9, 41.0] | 87 | 14 | 0.670 | 0.127 | 0.164 | 0.357 | 0.214 | 0.143 | 73.000 | 0.250 | 0.238 | 0.781 | 0.286 | 0.055 | 0.010 | 0.032 | 0.129 |
| (41.0, 54.0] | 80 | 15 | 0.620 | 0.158 | 0.215 | 0.600 | 0.467 | 0.200 | 72.000 | 0.416 | 0.242 | 0.631 | 0.375 | 0.064 | 0.014 | 0.046 | 0.087 |
| (54.0, 65.0] | 74 | 10 | 0.502 | 0.049 | 0.119 | 0.400 | 0.300 | 0.000 | 44.000 | 0.528 | 0.143 | 0.625 | 0.211 | 0.045 | 0.018 | 0.044 | 0.121 |

sens_spec92 = per-WEEK sensitivity at 92% per-WEEK specificity: landmark weeks, p threshold from the y=0 weeks of the CALIBRATION people (spec_spec92_test = per-week specificity reached on test); not the system's operating point. specificity = non-converters never prompted during follow-up (median 16.6 months of monitoring after the warm-up): CUMULATIVE over follow-up, not a single-window specificity; f1 and ppv_person (person-level PPV of a prompt) at this test conversion rate of 16%; lr_pos = Se0 / share of non-converters prompted. false_prompt_6mo / 12mo = Kaplan-Meier probability that a non-converter has >= 1 false prompt by 6 / 12 months of monitoring (day 0 = first landmark week, censored at end of follow-up). alarms_per_nonconv_py: per calendar person-year (warm-up included); alarms_per_nonconv_monitored_py: per monitored (post-warm-up) person-year. prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year after a 26-week refractory period (chosen to equal the 26-week prediction horizon; not the clinical panel rule of 13 weeks after a normal cuff series). It is a burden metric only: first warnings, every other metric, the tuned thresholds and the chance floor use the unsuppressed episodes. sens_post_onset_30/90 = Se30/Se90 counting a first warning before the simulated drift onset as a miss (n_pre_onset_first_warnings = how many); sens_lead_* count every warning before t_ref.

## Early-warning operating curve: sensitivity at >= 90 d lead (alarms/non-converter-yr) per warning budget

| budget | full | level_only | cuff_only | with_pulse | chance |
|---|---|---|---|---|---|
| 0.25 | 0.077 (0.171) | 0.026 (0.070) | 0.077 (0.117) | 0.051 (0.191) | 0.141 (0.250) |
| 0.5 | 0.128 (0.392) | 0.077 (0.244) | 0.077 (0.301) | 0.128 (0.398) | 0.260 (0.500) |
| 1.0 | 0.308 (0.861) | 0.256 (0.780) | 0.205 (0.589) | 0.282 (0.740) | 0.446 (1.000) |
| 2.0 | 0.436 (1.353) | 0.436 (1.353) | 0.436 (1.353) | 0.410 (1.269) | 0.680 (2.000) |

## Example evidence ledger (first warning of a warned converter)

```json
{
  "pid": "P0496",
  "week": 35,
  "first_warning_day": 251.0,
  "lead_days": 70.0,
  "state": "WARNING",
  "p": 0.12621036383392106,
  "p_lo": 0.09563743875640876,
  "p_hi": 0.13778179335590454,
  "weeks_exceeded": "4/5",
  "episodes": 3,
  "dev_slope12": 0.038570754299493054,
  "channel_contrib": {
    "night_rhr": 1.1173370217660297,
    "night_rmssd": 1.1970905319827114,
    "still_hr": 1.4706321848672448,
    "steps": 0.2172897737721746,
    "sleep_dur": 0.06028451936009538,
    "sleep_reg": 0.1186008214470614
  },
  "valid_days_30": 18,
  "ctx_masked_6w": 10,
  "month": 11,
  "agents": {
    "profiler": {
      "pid": "P0496",
      "week": 35,
      "quality": {
        "valid_days_30": 18,
        "n_eval": 5,
        "ctx_masked_6w": 10,
        "ctx_masked_weekly": [
          3,
          2,
          0,
          1,
          3,
          1
        ],
        "verdict": "marginal"
      },
      "deviation": {
        "dev": 1.419293435884622,
        "cusum": 2.145560078869914,
        "weeks_exceeded": [
          4,
          5
        ],
        "dev_slope12": 0.038570754299493054,
        "trend_z": 1.1941049979859384,
        "persist": true
      },
      "drivers": [
        {
          "channel": "night_rhr",
          "mean_z_6w": 1.1173370217660297,
          "toward_risk": true
        },
        {
          "channel": "night_rmssd",
          "mean_z_6w": 1.1970905319827114,
          "toward_risk": true
        },
        {
          "channel": "still_hr",
          "mean_z_6w": 1.4706321848672448,
          "toward_risk": true
        },
        {
          "channel": "steps",
          "mean_z_6w": 0.2172897737721746,
          "toward_risk": true
        },
        {
          "channel": "sleep_dur",
          "mean_z_6w": 0.06028451936009538,
          "toward_risk": true
        },
        {
          "channel": "sleep_reg",
          "mean_z_6w": 0.1186008214470614,
          "toward_risk": true
        }
      ],
      "usual_range": {
        "night_rhr": [
          55.450405715386026,
          72.04794034886682
        ],
        "night_rmssd": [
          15.899907893057833,
          41.09101296016166
        ],
        "still_hr": [
          65.89668401479,
          73.01735913646462
        ],
        "steps": [
          4386.629752213439,
          20328.71863043574
        ],
        "sleep_dur": [
          2.032135129186189,
          7.678683576292665
        ],
        "sleep_reg": [
          28.48962545942385,
          80.59838802086614
        ]
      },
      "concerns": [
        {
          "claim": "Data quality is marginal: 18 valid days in the last 30 and 5 of the last 6 weeks evaluable.",
          "ref": "profile.quality.verdict"
        },
        {
          "claim": "The weekly deviation exceeded the personal threshold in 4 of 5 evaluable weeks.",
          "ref": "profile.deviation.weeks_exceeded"
        },
        {
          "claim": "night_rhr averaged +1.12 personal SD from baseline over the last 6 weeks, in the risk direction.",
          "ref": "profile.drivers.0.mean_z_6w"
        },
        {
          "claim": "night_rmssd averaged +1.20 personal SD from baseline over the last 6 weeks, in the risk direction.",
          "ref": "profile.drivers.1.mean_z_6w"
        },
        {
          "claim": "still_hr averaged +1.47 personal SD from baseline over the last 6 weeks, in the risk direction.",
          "ref": "profile.drivers.2.mean_z_6w"
        },
        {
          "claim": "steps averaged +0.22 personal SD from baseline over the last 6 weeks, in the risk direction.",
          "ref": "profile.drivers.3.mean_z_6w"
        },
        {
          "claim": "sleep_dur averaged +0.06 personal SD from baseline over the last 6 weeks, in the risk direction.",
          "ref": "profile.drivers.4.mean_z_6w"
        },
        {
          "claim": "sleep_reg averaged +0.12 personal SD from baseline over the last 6 weeks, in the risk direction.",
          "ref": "profile.drivers.5.mean_z_6w"
        },
        {
          "claim": "The Kalman trend of the deviation has z = 1.19.",
          "ref": "profile.deviation.trend_z"
        },
        {
          "claim": "Acute context (exercise, alcohol, illness) masked the night channels on 10 days in the last 6 weeks.",
          "ref": "profile.quality.ctx_masked_6w"
        }
      ],
      "summary": "Data quality is marginal: 18 valid days in the last 30 and 5 of the last 6 weeks evaluable. The weekly deviation exceeded the personal threshold in 4 of 5 evaluable weeks. night_rhr averaged +1.12 personal SD from baseline over the last 6 weeks, in the risk direction. night_rmssd averaged +1.20 personal SD from baseline over the last 6 weeks, in the risk direction. still_hr averaged +1.47 personal SD from baseline over the last 6 weeks, in the risk direction. steps averaged +0.22 personal SD from baseline over the last 6 weeks, in the risk direction. sleep_dur averaged +0.06 personal SD from baseline over the last 6 weeks, in the risk direction. sleep_reg averaged +0.12 personal SD from baseline over the last 6 weeks, in the risk direction. The Kalman trend of the deviation has z = 1.19. Acute context (exercise, alcohol, illness) masked the night channels on 10 days in the last 6 weeks."
    },
    "predictor": {
      "pid": "P0496",
      "week": 35,
      "p": 0.12621036383392106,
      "p_lo": 0.09563743875640876,
      "p_hi": 0.13778179335590454,
      "thr_p": 0.09,
      "cuff": {
        "sbp_last": 116.25494906284281,
        "dbp_last": 75.1434663410025,
        "days_since": 8.0
      },
      "pipeline_state": "WARNING",
      "imputed_inputs": [],
      "proposed_state": "WARNING",
      "agrees_with_pipeline": true,
      "reasons": [
        {
          "claim": "The calibrated risk lower bound (0.096) is at or above the warning threshold (0.090).",
          "ref": "predictor.p_lo"
        },
        {
          "claim": "The deviation is persistent: 4 of 5 evaluable weeks above threshold.",
          "ref": "profile.deviation.persist"
        },
        {
          "claim": "18 valid days in the last 30.",
          "ref": "profile.quality.valid_days_30"
        },
        {
          "claim": "The last home-cuff reading was 8 days before this week.",
          "ref": "predictor.cuff.days_since"
        }
      ],
      "band_drivers": [
        {
          "claim": "Risk band 0.096 to 0.138 (bootstrap 10th-90th percentile).",
          "ref": "predictor.p_hi"
        },
        {
          "claim": "Evaluable weeks in the window: 5 of 6.",
          "ref": "profile.quality.n_eval"
        }
      ],
      "action": "Take home-cuff readings for 7 days."
    },
    "auditor": {
      "pid": "P0496",
      "week": 35,
      "checks": [
        {
          "name": "quality_gate",
          "pass": true,
          "detail": "valid_days_30 18 >= 15"
        },
        {
          "name": "risk_gate",
          "pass": true,
          "detail": "p_lo 0.09563743875640876 >= thr_p 0.09"
        },
        {
          "name": "persistence",
          "pass": true,
          "detail": "4 of 5 evaluable weeks in the last 6 above threshold; need >= 4"
        },
        {
          "name": "refs_resolve",
          "pass": true,
          "detail": "16 of 16 refs resolve, 4 reasons"
        },
        {
          "name": "no_bp_number",
          "pass": true,
          "detail": "no BP number or diagnostic wording"
        },
        {
          "name": "context_confound",
          "pass": true,
          "detail": "2 of the last 6 weeks had >= 3 acute-context masked days (fails at >= 3)"
        }
      ],
      "verdict": "approve",
      "final_state": "WARNING",
      "rationale": "Approved: all 6 checks pass."
    },
    "returned": null
  }
}
```

## Agent audit layer (--agents, template backend, main model only)

Profiler -> Predictor -> Auditor on every prompt (warn.prompts), re-run until no new prompt appears. The only allowed change is WARNING -> INSUFFICIENT for a whole episode. Purpose: traceability and a conservative second check, NOT better discrimination. For WARNING rows quality_gate, risk_gate and persistence pass by construction and the template backend cannot produce broken refs or BP numbers (invariant checks); on synthetic data context_confound (fixed rule: >= 3 of the last 6 weeks with >= 3 acute-context masked days) is the only check that can veto, and since the simulator puts illness/alcohol effects only on days the quality gate already masks, its vetoes are expected to be pure cost. The main tables above are pre-audit.

| metric | before audit | after audit | after - before |
|---|---|---|---|
| alarms_per_nonconv_py | 0.392 | 0.198 | -0.194 |
| prompts_per_nonconv_py_r26 | 0.238 | 0.131 | -0.107 |
| sens_lead_0 | 0.462 | 0.282 | -0.179 |
| sens_lead_30 | 0.333 | 0.154 | -0.179 |
| sens_lead_90 | 0.128 | 0.026 | -0.103 |
| sens_post_onset_30 | 0.282 | 0.154 | -0.128 |
| median_lead | 60.500 | 36.000 | -24.500 |
| warning_precision | 0.207 | 0.229 | +0.022 |
| specificity | 0.683 | 0.817 | +0.134 |
| chance_sens_lead_30 | 0.258 | 0.141 | -0.118 |
| chance_sens_lead_90 | 0.211 | 0.113 | -0.098 |
| chance_sens_post_onset_30 | 0.091 | 0.052 | -0.039 |

| count | value |
|---|---|
| prompts_audited | 124 |
| vetoes | 73 |
| returned_once | 0 |
| converters_first_warning_vetoed | 11 |
| converters_warned_before | 18 |
| converters_warned_after | 11 |
| converters_losing_all_warnings | 7 |
| nonconverters_warned_before | 64 |
| nonconverters_warned_after | 37 |
| nonconverters_spared | 27 |
| converter_vetoes | 15 |
| nonconverter_vetoes | 58 |

Failed checks (first audit round): quality_gate 0, risk_gate 0, persistence 0, refs_resolve 0, no_bp_number 0, context_confound 73

Vetoes by skin_ita tercile: (-40.1, 5.7]: 25/39, (5.7, 37.4]: 23/38, (37.4, 70.0]: 25/47

Converters whose first warning moved or vanished (lead days before -> after):

- P0078: 87.000 -> 17.000 (Se30 True->False, Se90 False->False)
- P0369: 73.000 -> n/a (Se30 True->False, Se90 False->False)
- P0372: 162.000 -> 22.000 (Se30 True->False, Se90 True->False)
- P0389: 35.000 -> n/a (Se30 True->False, Se90 False->False)
- P0395: 44.000 -> n/a (Se30 True->False, Se90 False->False)
- P0482: 21.000 -> n/a (Se30 False->False, Se90 False->False)
- P0566: 6.000 -> n/a (Se30 False->False, Se90 False->False)
- P0869: 120.000 -> n/a (Se30 True->False, Se90 True->False)
- P1065: 127.000 -> 36.000 (Se30 True->True, Se90 True->False)
- P1119: 204.000 -> 22.000 (Se30 True->False, Se90 True->False)
- P1187: 27.000 -> n/a (Se30 False->False, Se90 False->False)

Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`.

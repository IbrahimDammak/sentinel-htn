# Agent audit layer: before vs after audit, 3 seeds (seed0, seed1, seed2), mean ± SD over seeds

Template backend, main model, held-out test people. The layer can only downgrade whole WARNING episodes to INSUFFICIENT; it is a traceability layer and a conservative second check, not a better classifier. chance_* = random warnings at that column's own realised alarm rate. Nothing was tuned: thresholds, the warning budget and the context_confound rule are as fixed before the runs.

| metric | before | after | after - before per seed | mean ± SD |
|---|---|---|---|---|
| alarms_per_nonconv_py | 0.405 ± 0.036 | 0.217 ± 0.018 | -0.227 -0.146 -0.194 | -0.189 ± 0.041 |
| prompts_per_nonconv_py_r26 | 0.254 ± 0.032 | 0.141 ± 0.011 | -0.152 -0.080 -0.107 | -0.113 ± 0.037 |
| sens_lead_0 | 0.481 ± 0.049 | 0.265 ± 0.019 | -0.268 -0.200 -0.179 | -0.216 ± 0.046 |
| sens_lead_30 | 0.322 ± 0.051 | 0.138 ± 0.043 | -0.195 -0.178 -0.179 | -0.184 ± 0.010 |
| sens_lead_90 | 0.161 ± 0.072 | 0.063 ± 0.036 | -0.146 -0.044 -0.103 | -0.098 ± 0.051 |
| sens_post_onset_30 | 0.281 ± 0.036 | 0.138 ± 0.043 | -0.146 -0.156 -0.128 | -0.143 ± 0.014 |
| median_lead | 60.833 ± 8.505 | 34.000 ± 22.068 | -14.500 -41.500 -24.500 | -26.833 ± 13.650 |
| warning_precision | 0.209 ± 0.010 | 0.219 ± 0.009 | +0.016 -0.008 +0.022 | 0.010 ± 0.016 |
| specificity | 0.658 ± 0.042 | 0.802 ± 0.014 | +0.190 +0.108 +0.134 | 0.144 ± 0.042 |
| chance_sens_lead_30 | 0.257 ± 0.020 | 0.147 ± 0.006 | -0.129 -0.083 -0.118 | -0.110 ± 0.024 |
| chance_sens_lead_90 | 0.206 ± 0.018 | 0.117 ± 0.004 | -0.105 -0.067 -0.098 | -0.090 ± 0.020 |
| chance_sens_post_onset_30 | 0.093 ± 0.014 | 0.055 ± 0.004 | -0.047 -0.026 -0.039 | -0.038 ± 0.011 |

## Raw counts per seed

| count | seed0 | seed1 | seed2 | total |
|---|---|---|---|---|
| prompts_audited | 139 | 112 | 124 | 375 |
| vetoes | 87 | 56 | 73 | 216 |
| returned_once | 0 | 0 | 0 | 0 |
| converters_first_warning_vetoed | 15 | 12 | 11 | 38 |
| converters_warned_before | 22 | 20 | 18 | 60 |
| converters_warned_after | 11 | 11 | 11 | 33 |
| converters_losing_all_warnings | 11 | 9 | 7 | 27 |
| nonconverters_warned_before | 78 | 62 | 64 | 204 |
| nonconverters_warned_after | 40 | 41 | 37 | 118 |
| nonconverters_spared | 38 | 21 | 27 | 86 |
| converter_vetoes | 20 | 14 | 15 | 49 |
| nonconverter_vetoes | 67 | 42 | 58 | 167 |

## Failed checks (first audit round) per seed

| check | seed0 | seed1 | seed2 |
|---|---|---|---|
| quality_gate | 0 | 0 | 0 |
| risk_gate | 0 | 0 | 0 |
| persistence | 0 | 0 | 0 |
| refs_resolve | 0 | 0 | 0 |
| no_bp_number | 0 | 0 | 0 |
| context_confound | 87 | 56 | 73 |

## Vetoes / audited prompts by skin_ita tercile (T1 = darkest; edges differ per seed)

| seed | T1 | T2 | T3 |
|---|---|---|---|
| seed0 | 21/35 | 33/46 | 33/58 |
| seed1 | 13/25 | 23/43 | 20/44 |
| seed2 | 25/39 | 23/38 | 25/47 |

## Every converter whose first pre-t_ref warning moved or vanished

| seed | pid | lead before (d) | lead after (d) | Se30 before -> after | Se90 before -> after |
|---|---|---|---|---|---|
| seed0 | P0045 | 221 | none | True -> False | True -> False |
| seed0 | P0056 | 124 | none | True -> False | True -> False |
| seed0 | P0068 | 50 | none | True -> False | False -> False |
| seed0 | P0071 | 120 | none | True -> False | True -> False |
| seed0 | P0150 | 120 | 92 | True -> True | True -> True |
| seed0 | P0252 | 16 | none | False -> False | False -> False |
| seed0 | P0460 | 11 | none | False -> False | False -> False |
| seed0 | P0538 | 29 | 1 | False -> False | False -> False |
| seed0 | P0589 | 48 | 34 | True -> True | False -> False |
| seed0 | P0785 | 6 | none | False -> False | False -> False |
| seed0 | P0787 | 104 | none | True -> False | True -> False |
| seed0 | P0828 | 210 | none | True -> False | True -> False |
| seed0 | P0841 | 55 | none | True -> False | False -> False |
| seed0 | P0915 | 133 | 14 | True -> False | True -> False |
| seed0 | P0997 | 2 | none | False -> False | False -> False |
| seed1 | P0001 | 18 | none | False -> False | False -> False |
| seed1 | P0170 | 80 | none | True -> False | False -> False |
| seed1 | P0401 | 86 | none | True -> False | False -> False |
| seed1 | P0533 | 34 | none | True -> False | False -> False |
| seed1 | P0702 | 120 | none | True -> False | True -> False |
| seed1 | P0790 | 82 | none | True -> False | False -> False |
| seed1 | P0828 | 94 | none | True -> False | True -> False |
| seed1 | P0867 | 190 | 134 | True -> True | True -> True |
| seed1 | P0869 | 249 | 130 | True -> True | True -> True |
| seed1 | P0872 | 45 | 3 | True -> False | False -> False |
| seed1 | P0924 | 4 | none | False -> False | False -> False |
| seed1 | P1045 | 60 | none | True -> False | False -> False |
| seed2 | P0078 | 87 | 17 | True -> False | False -> False |
| seed2 | P0369 | 73 | none | True -> False | False -> False |
| seed2 | P0372 | 162 | 22 | True -> False | True -> False |
| seed2 | P0389 | 35 | none | True -> False | False -> False |
| seed2 | P0395 | 44 | none | True -> False | False -> False |
| seed2 | P0482 | 21 | none | False -> False | False -> False |
| seed2 | P0566 | 6 | none | False -> False | False -> False |
| seed2 | P0869 | 120 | none | True -> False | True -> False |
| seed2 | P1065 | 127 | 36 | True -> True | True -> False |
| seed2 | P1119 | 204 | 22 | True -> False | True -> False |
| seed2 | P1187 | 27 | none | False -> False | False -> False |

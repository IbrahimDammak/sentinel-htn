"""SENTINEL-HTN — personalized, uncertainty-aware early warning of emerging hypertension.

Learn (learn.py) -> Detect (detect.py) -> Predict (predict.py) -> Warn (warn.py); evaluate.py scores A–F.
Shared constants live here so every stage agrees on names. See CONTRACT.md for the data schema.
"""

# Physiological channels (daily values). Sign = direction that points toward hypertension risk.
RISK_SIGN = {
    'night_rhr': +1,     # nocturnal resting HR (bpm) rises with sympathetic drive
    'night_rmssd': -1,   # nocturnal HRV (ms) falls
    'still_hr': +1,      # daytime-stillness HR (bpm), modelled separately from night
    'steps': -1,         # daily steps fall
    'sleep_dur': -1,     # sleep duration (h) falls
    'sleep_reg': -1,     # sleep regularity index (0-100) falls
    'pulse_htn': +1,     # optional: nightly median PaPaGei-S hypertension-head logit (sentinel/pulse.py)
}
# Optional pulse-wave channels: absent or all-NaN (LifeSnaps, summary-only data) -> every stage runs on CHANNELS
# alone, exactly as without them (see channels()).
PULSE = ['pulse_htn']
CHANNELS = [c for c in RISK_SIGN if c not in PULSE]

# Evidence prior per channel for the joint deviation (multiplied by a label-free reliability weight, detect.py).
# Autonomic channels: the most direct, sympathetic-drive pathway and the largest cohort effects (low HRV: HR 1.58 for
# incident hypertension, Kang 2022). Behavioural channels: smaller or indirect, volitional and confounded effects
# (steps OR 0.92 per 1,000/day, Master 2022; short or irregular sleep HR 1.29 / OR 1.56, Zheng 2024). Never fitted
# to simulated labels (the simulator's couplings would just be recovered). Pulse channels: 0.5, cross-sectional
# evidence only (PPG-BP, results/ppg_bp), never validated longitudinally.
EVIDENCE = {'night_rhr': 1.0, 'night_rmssd': 1.0, 'still_hr': 1.0, 'steps': 0.5, 'sleep_dur': 0.5, 'sleep_reg': 0.5,
            'pulse_htn': 0.5}


def channels(df, suffix=''):
    """CHANNELS plus the PULSE channels with any non-NaN value in df[c + suffix] (suffix '', '_adj', '_z', '_w')."""
    return CHANNELS + [c for c in PULSE if c + suffix in df and df[c + suffix].notna().any()]

# Slow confounders are regressed out; acute ones mask the day for night/still channels.
SLOW_CONTEXT = ['ambient_temp', 'month', 'menses']
ACUTE_CONTEXT = ['exercise_min', 'alcohol', 'illness']
QUALITY = ['sqi', 'rhythm_irregular']
CUFF = ['sbp', 'dbp']

DAILY_COLUMNS = ['pid', 'day', 'month', *CHANNELS, 'ambient_temp', 'menses', *ACUTE_CONTEXT,
                 'firmware', *QUALITY, *CUFF]
PEOPLE_COLUMNS = ['pid', 'age', 'sex', 'bmi', 'skin_ita', 'converter', 't_ref', 'onset', 'end_day']

# Output states — exactly three, no "STABLE" (Chair's verdict, consensus point 4).
STATES = ('POOR_QUALITY', 'INSUFFICIENT', 'WARNING')

HTN_SBP, HTN_DBP = 130, 80   # primary t_ref: HBPM >= 130/80 on two qualifying occasions

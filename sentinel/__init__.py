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
}
CHANNELS = list(RISK_SIGN)

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

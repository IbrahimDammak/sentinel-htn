"""LifeSnaps adapter: rais_anonymized/csv_rais_anonymized/daily_fitbit_sema_df_unprocessed.csv -> (daily, people).

LifeSnaps (71 people, ~4 months, Fitbit Sense; Kaggle skywescar/lifesnaps-fitbit-dataset, CC BY 4.0) has no BP labels:
everyone is treated as a non-converter (t_ref NaN). Column meanings follow the official build notebook
(Datalab-AUTH/LifeSnaps-EDA, notebooks_preprocessing/visualization_df_creation.ipynb):
  nremhr        mean HR during non-REM sleep  (Fitbit "Daily Heart Rate Variability Summary") -> night_rhr
  rmssd         RMSSD during sleep, ms        (same summary)                                   -> night_rmssd
  resting_hr    Fitbit resting heart rate                                                      -> still_hr
  minutesAsleep main sleep, minutes (sleep_duration is time in bed, ms - not used)             -> sleep_dur (h)
  steps, very_active_minutes, age ('<30'/'>=30'), gender (MALE/FEMALE), bmi (number or '<19'/'>=25')
Fitbit dates both sleep and the HRV summary by the morning the sleep ended.
"""
import re

import numpy as np
import pandas as pd

from . import DAILY_COLUMNS, PEOPLE_COLUMNS


def _num(v, below=-0.5, above=1.0):
    """'23.0' -> 23.0; '<19' -> 18.5; '>=25' -> 26.0; unparseable -> NaN (bucket edges nudged inward)."""
    s = str(v).strip()
    m = re.search(r'\d+(\.\d+)?', s)
    if not m:
        return np.nan
    x = float(m.group())
    return x + below if s.startswith('<') else x + above if s.startswith('>') else x


def load_lifesnaps(csv_path):
    raw = pd.read_csv(csv_path, low_memory=False)
    raw = raw.drop(columns=[c for c in raw if c.startswith('Unnamed')])
    raw['pid'] = raw['id'].astype(str)
    raw['date'] = pd.to_datetime(raw['date']).dt.normalize()
    # outer merges of multi-row sources (badges, SEMA) duplicate (id, date): keep the first non-null per column
    df = raw.groupby(['pid', 'date'], as_index=False).first().sort_values(['pid', 'date'])

    num = lambda c: pd.to_numeric(df[c], errors='coerce') if c in df else pd.Series(np.nan, index=df.index)
    pos = lambda c: num(c).where(lambda s: s > 0)   # Fitbit writes 0 for "not measured" / not worn
    asleep = pos('minutesAsleep')
    d = pd.DataFrame({'pid': df.pid, 'date': df.date})
    d['day'] = (d.date - d.groupby('pid').date.transform('min')).dt.days
    d['month'] = d.date.dt.month
    d['night_rhr'] = pos('nremhr')
    d['night_rmssd'] = pos('rmssd')
    d['still_hr'] = pos('resting_hr')
    d['steps'] = pos('steps')
    d['sleep_dur'] = asleep / 60
    # ponytail: sleep-regularity proxy = 100 - (trailing 7-night SD of minutes asleep)/2; swap for a
    # sleep-regularity index once bed/wake times are extracted from the hourly file
    sd = (d.assign(m=asleep).set_index('date').groupby('pid').m
          .rolling('7D', min_periods=4).std().reset_index(drop=True))
    d['sleep_reg'] = (100 - sd.to_numpy() / 2).clip(0, 100)
    # vigorous minutes of day D-1 precede the night that ends on morning D
    prev = (pd.DataFrame({'pid': df.pid, 'date': df.date + pd.Timedelta(days=1), 'exercise_min': num('very_active_minutes')})
            .groupby(['pid', 'date'], as_index=False).first())
    d = d.merge(prev, on=['pid', 'date'], how='left')
    d['exercise_min'] = d.exercise_min.fillna(0.0)
    # not in LifeSnaps: weather, menses, alcohol, illness, firmware, rhythm, cuff
    d['ambient_temp'], d['menses'], d['alcohol'], d['illness'], d['firmware'] = 0.0, np.nan, 0.0, 0.0, 0
    d['rhythm_irregular'], d['sbp'], d['dbp'] = 0, np.nan, np.nan
    # Fitbit exposes no SQI: a night counts as good-quality only if a main sleep was recorded
    d['sqi'] = asleep.notna().astype(float).to_numpy()

    prof = df.groupby('pid').agg({c: 'first' for c in ('age', 'gender', 'bmi') if c in df})
    people = pd.DataFrame({'pid': prof.index})
    people['age'] = prof.get('age', pd.Series(dtype=object)).map(lambda v: _num(v, -5.0, 5.0)).to_numpy()  # '<30'->25
    people['sex'] = prof.get('gender', pd.Series(dtype=object)).map({'MALE': 'M', 'FEMALE': 'F'}).to_numpy()
    people['bmi'] = prof.get('bmi', pd.Series(dtype=object)).map(_num).to_numpy()
    people['skin_ita'], people['converter'], people['t_ref'], people['onset'] = np.nan, False, np.nan, np.nan
    people['end_day'] = people.pid.map(d.groupby('pid').day.max()).astype(int)
    return d[DAILY_COLUMNS].reset_index(drop=True), people[PEOPLE_COLUMNS]


if __name__ == '__main__':
    import os, tempfile
    rows = [  # LifeSnaps-shaped sample: duplicate badge rows, a gap day, bucketed profile fields
        dict(id='a1', date='2021-05-24', nremhr=57.4, rmssd=89.6, resting_hr=55, minutesAsleep=420, steps=8000,
             very_active_minutes=60, age='<30', gender='MALE', bmi='<19', badgeType='DAILY_STEPS'),
        dict(id='a1', date='2021-05-24', badgeType='LIFETIME_DISTANCE'),
        dict(id='a1', date='2021-05-25', nremhr=0.0, rmssd=94.3, resting_hr=0, minutesAsleep=0, steps=0,
             very_active_minutes=10),
        dict(id='a1', date='2021-05-27', nremhr=57.5, rmssd=111.7, resting_hr=56, minutesAsleep=400, steps=7000),
        dict(id='b2', date='2021-06-01', nremhr=61.0, rmssd=40.0, resting_hr=60, minutesAsleep=380, steps=5000,
             age='>=30', gender='FEMALE', bmi='23.0'),
    ]
    path = os.path.join(tempfile.mkdtemp(), 'daily.csv')
    pd.DataFrame(rows).to_csv(path)
    d, p = load_lifesnaps(path)
    a = d[d.pid == 'a1'].set_index('day')
    assert list(d.columns) == DAILY_COLUMNS and list(p.columns) == PEOPLE_COLUMNS
    assert len(a) == 3 and list(a.index) == [0, 1, 3]                     # duplicates collapsed, gap kept
    assert a.loc[0, 'night_rhr'] == 57.4 and a.loc[0, 'sleep_dur'] == 7.0
    assert a.loc[1, ['still_hr', 'night_rhr', 'steps', 'sleep_dur']].isna().all()   # Fitbit zeros -> missing
    assert a.loc[1, 'sqi'] == 0.0 and a.loc[0, 'sqi'] == 1.0               # no main sleep -> poor quality
    assert a.loc[1, 'exercise_min'] == 60 and a.loc[0, 'exercise_min'] == 0  # previous day's vigorous minutes
    assert a.loc[3, 'exercise_min'] == 0                                   # day 2 missing -> no exercise known
    q = p.set_index('pid')
    assert q.loc['a1', 'age'] == 25 and q.loc['b2', 'age'] == 35 and q.loc['a1', 'bmi'] == 18.5
    assert q.loc['b2', 'bmi'] == 23.0 and q.loc['a1', 'sex'] == 'M' and not p.converter.any()
    assert q.loc['a1', 'end_day'] == 3
    print('lifesnaps adapter OK')

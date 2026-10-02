"""End-to-end test: python tests/test_pipeline.py (~15 s). Uses a strong-signal cohort (effect=4): at the calibrated
realistic effect a single small cohort can sit at chance by luck, so it could not tell a bug from noise."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tempfile

import numpy as np
import pandas as pd

import run
from sentinel import STATES, data
from sentinel.lifesnaps import load_lifesnaps
from sentinel.evaluate import metrics
from sentinel.predict import FEATURE_SETS, local_trend

KEYS = ['auroc', 'auprc', 'sens_lead_0', 'sens_lead_30', 'sens_lead_90', 'sens_lead_180', 'median_lead',
        'alarms_per_nonconv_py', 'warning_precision', 'brier', 'ece', 'aurc', 'abstention_rate']

if __name__ == '__main__':
    assert 'STABLE' not in STATES and len(STATES) == 3
    assert all('onset' not in cols for cols in FEATURE_SETS.values())
    y = np.random.default_rng(0).normal(0, .2, (5, 40))
    ok = y > -.3
    s1 = local_trend(y, ok)[0]
    y[:, 25:] += 3
    assert np.allclose(s1[:, :25], local_trend(y, ok)[0][:, :25])   # Kalman trend at week t ignores weeks > t
    daily, people = data.make_cohort(600, 450, seed=0, effect=4.0)   # strong-signal sanity cohort: catches broken/inverted pipelines
    split = run.make_split(people, 0)
    tp = people[people.pid.isin(split['test'])]
    cfg = {**run.BASE, 'n_boot': 5}
    dec, wk, models, th = run.pipeline(daily, people, split, cfg)
    assert set(dec.state) <= set(STATES)
    m = metrics(dec, tp)
    assert all(k in m for k in KEYS), [k for k in KEYS if k not in m]
    assert m['auroc'] > 0.6, m['auroc']
    dec6 = run.pipeline(daily, people, split, cfg, (models, th), ('mcar', 0.6, {}))[0]
    m6 = metrics(dec6, tp)
    assert m6['abstention_rate'] > m['abstention_rate'], (m['abstention_rate'], m6['abstention_rate'])
    # real-world path: test people rewritten in LifeSnaps CSV format -> adapter -> label-free transfer metrics
    t = daily[daily.pid.isin(tp.pid)]
    csv = os.path.join(tempfile.mkdtemp(), 'lifesnaps.csv')
    pd.DataFrame({'id': t.pid, 'date': pd.Timestamp('2021-05-24') + pd.to_timedelta(t.day, unit='D'),
                  'nremhr': t.night_rhr, 'rmssd': t.night_rmssd, 'resting_hr': t.still_hr, 'steps': t.steps,
                  'minutesAsleep': t.sleep_dur * 60, 'very_active_minutes': t.exercise_min,
                  'age': '<30', 'gender': 'MALE', 'bmi': '23.0'}).to_csv(csv)
    rw = run.real_world(*load_lifesnaps(csv), cfg, (models, th))
    assert rw['people'] == tp.pid.nunique() and 0 <= rw['abstention_rate'] <= 1 and rw['warning_episodes_py'] >= 0, rw
    print('pipeline test OK', {k: round(m[k], 3) for k in ('auroc', 'abstention_rate')}, 'mcar0.6 abstention', round(m6['abstention_rate'], 3))

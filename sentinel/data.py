"""Synthetic AIoT cohort, CSV loader and robustness perturbations (schema: CONTRACT.md)."""
import numpy as np
import pandas as pd

from . import CHANNELS, ACUTE_CONTEXT, DAILY_COLUMNS, PEOPLE_COLUMNS, HTN_SBP, HTN_DBP

# channel: (between-person mean, between-person SD, day-to-day SD, coupling per mmHg of latent dSBP)
_CH = {
    'night_rhr': (60, 7, 2.5, 0.15),
    'night_rmssd': (40, 12, 6, -0.35),
    'still_hr': (70, 8, 4, 0.12),
    'steps': (8000, 2500, 2000, -40),
    'sleep_dur': (7, 0.7, 0.8, -0.01),
    'sleep_reg': (75, 10, 8, -0.15),
}


def _spans(rng, days, per_year, lo, hi):
    """Boolean mask of ~per_year episodes/year, each lo..hi days long."""
    m = np.zeros(days, bool)
    for s in rng.integers(0, days, rng.poisson(per_year * days / 365)):
        m[s:s + rng.integers(lo, hi + 1)] = True
    return m


def _person(rng, days, conv):
    """One person's daily arrays (dict) and people-row fields (dict)."""
    d = np.arange(days)
    sex = 'F' if rng.random() < .5 else 'M'
    ita = float(np.clip(rng.normal(23, 30), -40, 70))          # ~1/3 below 10
    # baseline kept clear of 130/80 so winter (+~5.5 mmHg) + cuff noise rarely creates a label on its own
    sbp0 = np.clip(rng.normal(116, 5), 100, 123)
    dbp0 = np.clip(rng.normal(72, 3.5), 60, 74)
    # latent BP: drift (converter ramp or +-2 mmHg wander) + season
    onset = rng.uniform(120, days - 120) if conv else np.nan
    if conv:
        drift = rng.uniform(12, 22) * np.clip((d - onset) / rng.uniform(120, 200), 0, 1)
    else:
        drift = rng.uniform(-2, 2) * d / days
    month = ((rng.uniform(0, 365) + d) % 365 // 30.4375).astype(int) + 1
    temp = 18 + 9 * np.sin(2 * np.pi * (month - 4) / 12) + rng.normal(0, 2, days)
    cold = 18 - temp
    dsbp = drift + 0.61 * cold                                  # latent dBP above own baseline
    sbp, dbp = sbp0 + dsbp, dbp0 + 0.6 * dsbp
    # confounders
    ill = _spans(rng, days, 3, 3, 7)
    alc = rng.random(days) < 1 / 7
    ex = np.where(rng.random(days) < 1.5 / 7, rng.uniform(46, 120, days),
                  np.minimum(rng.exponential(12, days), 45))   # vigorous min previous evening
    men = np.full(days, np.nan)
    if sex == 'F' and rng.random() < .5:
        men = ((d + rng.integers(0, 28)) % 28 >= 14).astype(float)   # luteal phase = 1
    fw = (d >= rng.integers(0, days)).astype(int) if rng.random() < .3 else np.zeros(days, int)
    # channels
    x = {c: rng.normal(mu, sd) + k * dsbp + rng.normal(0, sdd, days) for c, (mu, sd, sdd, k) in _CH.items()}
    x['night_rhr'] += 0.05 * cold + 5 * ill + 3 * alc + 2 * (ex > 45) + 2 * (men == 1) + 1.5 * fw
    x['night_rmssd'] += -8 * ill - 6 * alc
    x['steps'] = np.maximum(x['steps'], 0)
    x['night_rmssd'] = np.maximum(x['night_rmssd'], 5)
    x['sleep_dur'] = np.clip(x['sleep_dur'], 3, 11)
    x['sleep_reg'] = np.clip(x['sleep_reg'], 0, 100)
    # missingness: MCAR + charging + off-wrist bursts (+ MNAR for dark skin)
    dark = ita < 10
    down = (rng.random(days) < .08) | _spans(rng, days, 2, 5, 15)
    gone = down | (rng.random(days) < .12) | (dark & (rng.random(days) < .12))
    sqi = rng.beta(7, 2.5, days) if dark else rng.beta(12, 2, days)
    sqi[down] = 0
    x = {c: np.where(gone, np.nan, v) for c, v in x.items()}
    # cuff: 3-day series every 60-120 days
    cs, cd = np.full(days, np.nan), np.full(days, np.nan)
    starts, s = [], rng.integers(0, 15)
    while s + 3 <= days:
        starts.append(s)
        cs[s:s + 3] = sbp[s:s + 3] + rng.normal(0, 6, 3)
        cd[s:s + 3] = dbp[s:s + 3] + rng.normal(0, 4, 3)
        s += rng.integers(60, 121)
    hi = np.array([cs[s:s + 3].mean() >= HTN_SBP or cd[s:s + 3].mean() >= HTN_DBP for s in starts], bool)
    two = np.flatnonzero(hi[:-1] & hi[1:])
    t_ref = float(starts[two[0]]) if len(two) else np.nan
    daily = dict(day=d, month=month, **x, ambient_temp=temp, menses=men, exercise_min=ex,
                 alcohol=alc.astype(float), illness=ill.astype(float), firmware=fw, sqi=sqi,
                 rhythm_irregular=(rng.random(days) < .01).astype(int), sbp=cs, dbp=cd)
    person = dict(age=int(rng.integers(30, 66)), sex=sex, bmi=rng.uniform(20, 38), skin_ita=ita,
                  converter=not np.isnan(t_ref), t_ref=t_ref, onset=onset, end_day=days - 1)
    return daily, person


def make_cohort(n_people=600, days=540, seed=0, converter_rate=0.35):
    """Simulate (daily, people) with latent BP drift, confounders, missingness and cuff labels."""
    rng = np.random.default_rng(seed)
    pids = [f'P{i:04d}' for i in range(n_people)]
    ds, ps = zip(*[_person(rng, days, rng.random() < converter_rate) for _ in pids])
    daily = pd.DataFrame({k: np.concatenate([d[k] for d in ds]) for k in ds[0]})
    daily.insert(0, 'pid', np.repeat(pids, days))
    people = pd.DataFrame(list(ps))
    people.insert(0, 'pid', pids)
    return daily[DAILY_COLUMNS], people[PEOPLE_COLUMNS]


def load_csv(daily_path, people_path):
    """Read + validate real data; fill optional columns with neutral defaults."""
    d, p = pd.read_csv(daily_path), pd.read_csv(people_path)
    for df, need, name in ((d, ['pid', 'day', *CHANNELS], 'daily'),
                           (p, ['pid', 'age', 'sex', 'bmi', 'skin_ita', 't_ref'], 'people')):
        bad = [c for c in need if c not in df]
        if bad:
            raise ValueError(f'{name} csv missing required columns: {bad}')
    fill = {'month': 1, 'ambient_temp': 0.0, 'menses': np.nan, 'firmware': 0, 'rhythm_irregular': 0,
            'sqi': 1.0, 'sbp': np.nan, 'dbp': np.nan, **{c: 0.0 for c in ACUTE_CONTEXT}}
    for c, v in fill.items():
        if c not in d:
            d[c] = v
    d['pid'], p['pid'] = d['pid'].astype(str), p['pid'].astype(str)
    d = d.astype({'day': int}).sort_values(['pid', 'day']).reset_index(drop=True)
    if 'onset' not in p:
        p['onset'] = np.nan
    if 'converter' not in p:
        p['converter'] = p['t_ref'].notna()
    if 'end_day' not in p:
        p['end_day'] = p['pid'].map(d.groupby('pid')['day'].max()).fillna(0).astype(int)
    p['converter'] = p['converter'].astype(bool)
    return (d[DAILY_COLUMNS + [c for c in d if c not in DAILY_COLUMNS]],
            p[PEOPLE_COLUMNS + [c for c in p if c not in PEOPLE_COLUMNS]])


def perturb(daily, kind, level, seed=0, channel=None, people=None):
    """Return a perturbed copy of daily (see CONTRACT.md for kinds); the input is never modified."""
    rng = np.random.default_rng(seed)
    out = daily.copy()
    chs = [channel] if channel else CHANNELS
    if kind == 'mcar':
        v = out[chs].to_numpy(float, copy=True)
        v[rng.random(v.shape) < level] = np.nan
        out[chs] = v
    elif kind == 'noise':
        for c in chs:
            out[c] = out[c] + rng.normal(0, level * daily[c].std(), len(out))
    elif kind == 'drop_channel':
        out[channel] = np.nan
    elif kind == 'mnar':
        ita = out['pid'].map(people.set_index('pid')['skin_ita']).to_numpy(float)
        w = 1 / (1 + np.exp((ita - 10) / 15))                    # darker skin -> more missing
        gone = rng.random(len(out)) < np.clip(level * w / w.mean(), 0, 1)
        out.loc[gone, CHANNELS] = np.nan
    elif kind == 'sensor_fail':
        key, inv = np.unique(out['pid'].astype(str) + '_' + (out['day'] // 14).astype(str), return_inverse=True)
        out.loc[(rng.random(len(key)) < level)[inv], 'sqi'] = 0.0
    else:
        raise ValueError(f'unknown perturbation kind: {kind}')
    return out


if __name__ == '__main__':
    import time
    t0 = time.time()
    daily, people = make_cohort(600, 540)
    dt = time.time() - t0
    assert set(DAILY_COLUMNS) <= set(daily) and set(PEOPLE_COLUMNS) <= set(people)
    conv = people['converter'].mean()
    miss = daily[CHANNELS].isna().all(axis=1).mean()
    assert 0.15 <= conv <= 0.40, conv
    assert 0.20 <= miss <= 0.40, miss
    # converters: mean night_rhr after onset minus before onset
    on = daily.merge(people[['pid', 'onset']], on='pid')
    on = on[on['onset'].notna()]
    post = on['day'] >= on['onset']
    g = on.groupby(['pid', post])['night_rhr'].mean().unstack()
    assert (g[True] - g[False]).mean() > 0, 'night_rhr should rise after onset'
    # perturb returns copies and leaves input untouched
    before = daily.copy()
    for kind, lv, kw in [('mcar', .3, {}), ('noise', 1., {}), ('drop_channel', 0, {'channel': 'night_rmssd'}),
                         ('mnar', .4, {'people': people}), ('sensor_fail', .3, {})]:
        out = perturb(daily, kind, lv, **kw)
        assert out is not daily and not np.shares_memory(out['night_rhr'].to_numpy(), daily['night_rhr'].to_numpy())
        pd.testing.assert_frame_equal(daily, before)
    assert perturb(daily, 'mcar', .3)[CHANNELS].isna().to_numpy().mean() > daily[CHANNELS].isna().to_numpy().mean()
    assert perturb(daily, 'sensor_fail', .3)['sqi'].eq(0).mean() > daily['sqi'].eq(0).mean()
    a, _ = make_cohort(20, 300, seed=1)
    b, _ = make_cohort(20, 300, seed=1)
    pd.testing.assert_frame_equal(a, b)
    print(f'ok: {dt:.1f}s converter={conv:.2f} missing={miss:.2f} dark={(people.skin_ita < 10).mean():.2f} '
          f'rhr_shift={(g[True] - g[False]).mean():.2f}')

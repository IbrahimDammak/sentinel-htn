"""DETECT: weekly aggregation, CUSUM, persistence rule, alarm-budget threshold tuning."""
import numpy as np
import pandas as pd

from . import CHANNELS

WEEKS_PER_YEAR = 365.25 / 7


def weekly(resid):
    """Per pid-week channel means, joint deviation `dev` and evaluability. Absent weeks appear as non-evaluable."""
    zc = [c + '_z' for c in CHANNELS]
    g = resid.assign(week=resid['day'] // 7).groupby(['pid', 'week'])
    wk = g[zc].mean().where(g[zc].count() >= 3)                       # NaN if < 3 days
    wk.columns = [c + '_w' for c in CHANNELS]
    wk['dev'] = wk.mean(axis=1)                                       # mean of available channel z's
    wk['n_valid'] = g['valid'].sum()
    wk['evaluable'] = (wk['n_valid'] >= 4) & (g['baseline_ready'].mean() > 0.5) & wk['dev'].notna()
    wk['ctx_masked'] = g['ctx_masked'].sum()
    last = wk.index.to_frame(index=False).groupby('pid')['week'].max()   # complete week grid per person
    full = pd.MultiIndex.from_arrays([np.repeat(last.index, last + 1), np.concatenate([np.arange(m + 1) for m in last])],
                                     names=['pid', 'week'])
    wk = wk.reindex(full)
    wk[['n_valid', 'ctx_masked']] = wk[['n_valid', 'ctx_masked']].fillna(0).astype(int)
    wk['evaluable'] = wk['evaluable'].fillna(False).astype(bool)
    return wk.reset_index()


def cusum(wk, k=0.25, h=3.0):
    """One-sided upper CUSUM of dev per person (carried forward over non-evaluable weeks); `cusum_alarm` = cusum >= h."""
    dev, ev = wk['dev'].to_numpy(), wk['evaluable'].to_numpy()
    out = np.zeros(len(wk))
    for ix in wk.groupby('pid').indices.values():                     # wk is sorted by pid, week
        s = 0.0
        for i in ix:
            if ev[i]:
                s = max(0.0, s + dev[i] - k)
            out[i] = s
    wk = wk.copy()
    wk['cusum'] = out
    wk['cusum_alarm'] = out >= h
    return wk


def _roll(x, pid, n):
    """Sum over the last n rows within each person (rows are consecutive weeks)."""
    cs = x.groupby(pid).cumsum()
    return cs - cs.groupby(pid).shift(n, fill_value=0)


def persistence(wk, thr=0.5, m=4, n=6):
    """persist = at least m of the last n weeks evaluable and dev > thr; non-evaluable weeks are neither yes nor no."""
    wk = wk.copy()
    pid = wk['pid']
    wk['n_eval'] = _roll(wk['evaluable'].astype(int), pid, n)
    wk['n_exceed'] = _roll((wk['evaluable'] & (wk['dev'] > thr)).astype(int), pid, n)
    wk['persist'] = wk['n_exceed'] >= m
    prev = wk['persist'].groupby(pid).shift(fill_value=False)
    wk['episodes'] = (wk['persist'] & ~prev).groupby(pid).cumsum()
    return wk


def tune_threshold(wk, people, budget=0.5, grid=None):
    """Smallest dev threshold with persist episodes per non-converter person-year <= budget.

    Person-years = evaluable (observed, monitored) weeks / 52.18. Returns the largest grid value if none fits.
    """
    grid = np.round(np.arange(0, 3.01, 0.05), 2) if grid is None else grid
    nc = wk[wk['pid'].isin(people.loc[~people['converter'].astype(bool), 'pid'])]
    years = nc['evaluable'].sum() / WEEKS_PER_YEAR
    for thr in sorted(grid):
        if persistence(nc, thr).groupby('pid')['episodes'].max().sum() <= budget * years:
            return float(thr)
    return float(max(grid))


if __name__ == '__main__':
    def person(pid, z, ok=None):
        """Daily resid rows for one person from weekly night_rhr z values; ok[w]=False -> week not valid."""
        ok = [True] * len(z) if ok is None else ok
        n = len(z) * 7
        r = pd.DataFrame({'pid': pid, 'day': np.arange(n)})
        for c in CHANNELS:
            r[c + '_z'] = np.nan
        r['night_rhr_z'] = np.repeat(np.where(ok, z, np.nan), 7)
        r['valid'] = np.repeat(ok, 7)
        r['ctx_masked'], r['baseline_ready'] = 0, True
        return r

    resid = pd.concat([
        person('A', [0] * 10 + [1.0] * 10),                                       # sustained shift from week 10
        person('B', [0] * 5 + [3.0] + [0] * 14),                                  # single spike at week 5
        person('C', [1.0] * 3 + [0, 0, 1.0, 1.0] + [0] * 3, [True] * 3 + [False] * 2 + [True] * 5),  # gap weeks 3-4
    ], ignore_index=True)
    wk = persistence(cusum(weekly(resid)))
    A, B, C = (wk[wk.pid == p].set_index('week') for p in 'ABC')

    assert wk.evaluable.sum() == 20 + 20 + 8 and (wk.dev.dropna() == wk.night_rhr_w.dropna()).all()
    assert A.cusum[9] == 0 and A.cusum[19] > A.cusum[12] > A.cusum[10] > 0 and A.cusum[19] == 7.5
    assert A.persist[13] and not A.persist[12] and A.episodes[19] == 1          # >=4 of 6 exceeding weeks
    assert not B.persist.any() and B.n_exceed.max() == 1 and B.cusum[5] == 2.75  # one spike never persists
    assert C.cusum[3] == C.cusum[4] == C.cusum[2] and not C.evaluable[3]         # gap carries CUSUM forward
    assert C.n_eval[4] == 3 and C.n_eval[5] == 4 and C.n_exceed[5] == 4 and C.persist[5]  # gap not negative

    rng = np.random.default_rng(1)
    noise = pd.concat([person(f'n{i}', rng.normal(0, 0.5, 40)) for i in range(60)], ignore_index=True)
    people = pd.DataFrame({'pid': [f'n{i}' for i in range(60)] + ['A'], 'converter': [False] * 60 + [True]})
    wk2 = weekly(pd.concat([noise, person('A', [1.0] * 40)], ignore_index=True))
    thr = tune_threshold(wk2, people, budget=0.5)
    nc = wk2[wk2.pid != 'A']
    rate = lambda t: persistence(nc, t).groupby('pid').episodes.max().sum() / (nc.evaluable.sum() / WEEKS_PER_YEAR)
    assert rate(thr) <= 0.5 and (thr == 0 or rate(thr - 0.05) > 0.5), (thr, rate(thr))
    print('detect OK, thr =', thr)

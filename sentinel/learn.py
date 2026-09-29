"""LEARN: quality gate, context adjustment, population prior, personal hierarchical baseline."""
import numpy as np
import pandas as pd

from . import CHANNELS, RISK_SIGN

MASKED = ['night_rhr', 'night_rmssd', 'still_hr']   # channels blanked on acute-context days


def quality_gate(daily, sqi_min=0.6, exercise_max=45):
    """Add `valid` and `ctx_masked`; blank channels on invalid days, night/still channels on acute days."""
    d = daily.copy()
    d['valid'] = (d['sqi'] >= sqi_min) & (d['rhythm_irregular'] == 0) & d[CHANNELS].notna().any(axis=1)
    d.loc[~d['valid'], CHANNELS] = np.nan
    acute = (d['exercise_min'] > exercise_max) | (d['alcohol'] == 1) | (d['illness'] == 1)
    d.loc[acute, MASKED] = np.nan
    d['ctx_masked'] = acute.astype(int)
    return d


def _design(d):
    """[1, ambient_temp, sin, cos, menses]; missing context values are left NaN except menses -> 0."""
    a = 2 * np.pi * d['month'].to_numpy(float) / 12
    return np.column_stack([np.ones(len(d)), d['ambient_temp'].to_numpy(float), np.sin(a), np.cos(a),
                            d['menses'].fillna(0).to_numpy(float)])


def fit_context(daily):
    """Pooled OLS of each channel on the slow context; returns {channel: 5 coefficients}."""
    X = _design(daily)
    okx = np.isfinite(X).all(axis=1)
    ctx = {}
    for ch in CHANNELS:
        y = daily[ch].to_numpy(float)
        ok = okx & np.isfinite(y)
        ctx[ch] = np.linalg.lstsq(X[ok], y[ok], rcond=None)[0] if ok.sum() >= X.shape[1] else np.zeros(X.shape[1])
    return ctx


def apply_context(daily, ctx):
    """Add `<ch>_adj` = value minus the context effect (intercept excluded; missing context = no effect)."""
    d = daily.copy()
    X = np.nan_to_num(_design(d)[:, 1:])
    for ch in CHANNELS:
        d[ch + '_adj'] = d[ch] - X @ ctx[ch][1:]
    return d


def fit_prior(daily, warmup_days=56):
    """Population prior per channel from each person's first `warmup_days` of `<ch>_adj`."""
    w = daily[daily['day'] < warmup_days]
    prior = {}
    for ch in CHANNELS:
        g = w.groupby('pid')[ch + '_adj']
        n, mu, s2 = g.count(), g.mean(), g.var()
        df = (n - 1).clip(lower=0)
        sigma2 = (df * s2.fillna(0)).sum() / max(df.sum(), 1)
        mu, n = mu[n > 0], n[n > 0]
        vm = mu.var()
        tau2 = max(vm - (sigma2 / n).mean(), 0.01 * vm)   # remove sampling noise from the spread of means
        prior[ch] = {'mu0': float(mu.mean()), 'tau': float(np.sqrt(tau2)), 'sigma': float(np.sqrt(sigma2))}
    return prior


def personal_baseline(daily, prior, warmup_valid=28, personal=True):
    """Signed, robust z per channel against a normal-normal posterior personal baseline.

    Needs `<ch>_adj`, `valid`, `ctx_masked`. Warm-up (first `warmup_valid` valid days, restarted at every
    firmware change) gives baseline_ready=False and NaN z. personal=False uses the population prior only.
    """
    d = daily.sort_values(['pid', 'day']).reset_index(drop=True)
    fw = d['firmware'].fillna(0)
    seg = fw.ne(fw.groupby(d['pid']).shift()).groupby(d['pid']).cumsum().rename('seg')
    key = [d['pid'], seg]
    val = d['valid'].astype(int)
    ready = (val.groupby(key).cumsum() - val) >= warmup_valid    # valid days strictly before this row
    out = d[['pid', 'day']].copy()
    for ch, sign in RISK_SIGN.items():
        p, x = prior[ch], d[ch + '_adj']
        if personal:
            xw = x.where(~ready)
            n = xw.notna().astype(int).groupby(key).transform('sum')
            t = xw.groupby(key).transform('sum')
            v = 1 / (1 / p['tau'] ** 2 + n / p['sigma'] ** 2)
            m = v * (p['mu0'] / p['tau'] ** 2 + t / p['sigma'] ** 2)
        else:
            m, v = p['mu0'], p['tau'] ** 2
        out[ch + '_z'] = (sign * (x - m) / np.sqrt(p['sigma'] ** 2 + v)).where(ready).clip(-6, 6)
    out['valid'], out['ctx_masked'], out['baseline_ready'] = d['valid'], d['ctx_masked'], ready
    return out


if __name__ == '__main__':
    rng = np.random.default_rng(0)
    P, D = 20, 120
    day = np.tile(np.arange(D), P)
    pid = np.repeat([f'p{i}' for i in range(P)], D)
    month = (day // 30) % 12 + 1
    temp = 15 + 8 * np.sin(2 * np.pi * month / 12) + rng.normal(0, 3, P * D)
    off = np.repeat(rng.normal(0, 3, P), D)
    d = pd.DataFrame({'pid': pid, 'day': day, 'month': month, 'ambient_temp': temp, 'menses': np.nan,
                      'exercise_min': 0.0, 'alcohol': 0.0, 'illness': 0.0, 'firmware': 0, 'sqi': 1.0,
                      'rhythm_irregular': 0})
    d['night_rhr'] = 55 + off + 0.3 * temp + rng.normal(0, 1, P * D) + 5 * ((pid == 'p0') & (day >= 60))
    for ch in CHANNELS[1:]:
        d[ch] = 50 + off + rng.normal(0, 1, P * D)
    d.loc[(d.pid == 'p0') & d.day.between(70, 72), 'alcohol'] = 1.0        # acute confounder
    d.loc[(d.pid == 'p1') & (d.day >= 80), 'firmware'] = 1                  # firmware change restarts warm-up

    g = quality_gate(d)
    ctx = fit_context(g)
    assert abs(ctx['night_rhr'][1] - 0.3) < 0.1, ctx['night_rhr']
    a = apply_context(g, ctx)
    prior = fit_prior(a)
    r = personal_baseline(a, prior)
    r0 = personal_baseline(a, prior, personal=False)

    p0 = r[r.pid == 'p0'].set_index('day')
    assert p0.loc[70:72, 'night_rhr_z'].isna().all() and (p0.loc[70:72, 'ctx_masked'] == 1).all()
    assert p0.loc[70:72, 'steps_z'].notna().all()                          # steps not masked
    assert p0.loc[[27, 28], 'baseline_ready'].tolist() == [False, True]
    assert p0.loc[73:119, 'night_rhr_z'].mean() > 1.5, p0.loc[73:119, 'night_rhr_z'].mean()
    assert abs(p0.loc[30:59, 'night_rhr_z'].mean()) < 1.0
    p1 = r[r.pid == 'p1'].set_index('day')
    assert not p1.loc[85, 'baseline_ready'] and p1.loc[115, 'baseline_ready']  # firmware restart
    assert not np.allclose(r.night_rhr_z.dropna(), r0.night_rhr_z.dropna())
    print('learn OK', {k: round(v, 2) for k, v in prior['night_rhr'].items()})

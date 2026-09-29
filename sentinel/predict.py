"""PREDICT — landmark discrete-time hazard: L2 logistic regression, person-bootstrap band, Platt calibration."""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.special import expit, logit

LEVEL = ['age', 'sex_m', 'bmi', 'rhr_level', 'cuff_sbp_last', 'cuff_dbp_last', 'cuff_days_since']
CHANGE = ['dev', 'dev_slope12', 'cusum', 'n_exceed', 'n_eval', 'persist', 'trend', 'trend_z']
QUALITY_COLS = ['valid_days_30']
FEATURE_SETS = {
    'full': LEVEL + CHANGE + QUALITY_COLS,
    'level_only': list(LEVEL),
    'cuff_only': ['age', 'cuff_sbp_last', 'cuff_dbp_last', 'cuff_days_since'],
    'change_only': list(CHANGE),
}  # 'onset' is synthetic ground truth and must never appear here.


def _roll(a, n):
    """Trailing-window sum over axis 1 (window n, inclusive of the current column)."""
    c = a.cumsum(axis=1)
    r = c.copy()
    r[:, n:] = c[:, n:] - c[:, :-n]
    return r


def local_trend(y, obs, q_level=0.03 ** 2, q_slope=0.003 ** 2, r=0.2 ** 2, p_slope0=0.01 ** 2):
    """Causal Kalman filter, local linear trend (level + slope/week), one person per row of y (person x week).

    Unobserved weeks are prediction steps only. Column t uses y[:, :t+1] only. Returns (slope, slope SD)."""
    P, W = y.shape
    lv, b = np.zeros(P), np.zeros(P)
    p11, p12, p22 = np.ones(P), np.zeros(P), np.full(P, p_slope0)
    slope, sd = np.empty((P, W)), np.empty((P, W))
    for t in range(W):
        lv, p11, p12, p22 = lv + b, p11 + 2 * p12 + p22 + q_level, p12 + p22, p22 + q_slope   # predict
        o = obs[:, t]
        k1, k2 = p11 / (p11 + r), p12 / (p11 + r)
        v = np.where(o, y[:, t] - lv, 0.0)
        lv, b = lv + k1 * v, b + k2 * v
        p22 = np.where(o, p22 - k2 * p12, p22)
        p11, p12 = np.where(o, (1 - k1) * p11, p11), np.where(o, (1 - k1) * p12, p12)
        slope[:, t], sd[:, t] = b, np.sqrt(p22)
    return slope, sd


def make_landmarks(wk, daily, people, horizon_weeks=26):
    """One row per pid-week from baseline-ready until the t_ref week (exclusive); uses only data up to day 7*week+6."""
    wk = wk.sort_values(['pid', 'week']).reset_index(drop=True)
    pe = people.set_index('pid')
    tr, ed = wk.pid.map(pe.t_ref), wk.pid.map(pe.end_day)
    last = np.where(tr.notna(), np.floor(tr / 7) - 1, ed // 7)
    # baseline ready = from the first evaluable week on (wk carries no explicit flag)
    ready = wk.evaluable.astype(int).groupby(wk.pid).cummax().astype(bool)
    lm = wk.loc[ready & (wk.week <= last), ['pid', 'week', 'dev', 'cusum', 'n_exceed', 'n_eval', 'persist']].copy()
    t = lm.pid.map(pe.t_ref)
    lm['y'] = ((t > 7 * lm.week) & (t <= 7 * (lm.week + horizon_weeks))).astype(int)
    lm['age'] = lm.pid.map(pe.age)
    lm['sex_m'] = (lm.pid.map(pe.sex) == 'M').astype(int)
    lm['bmi'] = lm.pid.map(pe.bmi)
    lm['lday'] = 7 * lm.week + 6

    # last cuff reading on or before the landmark day
    cuff = daily.loc[daily.sbp.notna() | daily.dbp.notna(), ['pid', 'day', 'sbp', 'dbp']]
    cuff = cuff.rename(columns={'day': 'cday', 'sbp': 'cuff_sbp_last', 'dbp': 'cuff_dbp_last'}).sort_values('cday')
    lm = pd.merge_asof(lm.sort_values('lday'), cuff, left_on='lday', right_on='cday', by='pid')
    lm['cuff_days_since'] = lm.lday - lm.cday
    lm = lm.sort_values(['pid', 'week']).reset_index(drop=True)

    # trailing-window features from dense (person x day) and (person x week) grids
    pids = pd.Index(pd.unique(pd.concat([daily.pid, wk.pid])))
    P, D, W = len(pids), int(max(daily.day.max(), lm.lday.max())) + 1, int(wk.week.max()) + 1
    pi, di = pids.get_indexer(daily.pid), daily.day.to_numpy()
    ok = (daily.valid.astype(bool) & daily.night_rhr_adj.notna()).to_numpy()
    S, C, V = (np.zeros((P, D)) for _ in range(3))
    S[pi, di] = np.where(ok, daily.night_rhr_adj.fillna(0), 0)
    C[pi, di] = ok
    V[pi, di] = daily.valid.astype(bool).to_numpy()
    li, ld, lw = pids.get_indexer(lm.pid), lm.lday.to_numpy(), lm.week.to_numpy()
    rc = _roll(C, 28)[li, ld]
    with np.errstate(invalid='ignore', divide='ignore'):
        lm['rhr_level'] = np.where(rc > 0, _roll(S, 28)[li, ld] / rc, np.nan)
    lm['valid_days_30'] = _roll(V, 30)[li, ld]

    # OLS slope of dev over the last 12 weeks (>= 3 evaluated points)
    wi = pids.get_indexer(wk.pid)
    y0 = np.zeros((P, W)); m = np.zeros((P, W))
    y0[wi, wk.week] = wk.dev.fillna(0); m[wi, wk.week] = wk.dev.notna()
    x = np.arange(W, dtype=float)[None, :]
    n, sx, sy = _roll(m, 12), _roll(m * x, 12), _roll(y0, 12)
    sxy, sxx = _roll(y0 * x, 12), _roll(m * x * x, 12)
    den = n * sxx - sx ** 2
    with np.errstate(invalid='ignore', divide='ignore'):
        slope = np.where((n >= 3) & (den > 0), (n * sxy - sx * sy) / den, np.nan)
    lm['dev_slope12'] = slope[li, lw]
    # Kalman local linear trend of dev over evaluable weeks: posterior slope and slope/SD ("trend z")
    ev = np.zeros((P, W), bool)
    ev[wi, wk.week] = wk.evaluable.astype(bool)
    tr, tsd = local_trend(y0, ev)
    lm['trend'], lm['trend_z'] = tr[li, lw], tr[li, lw] / tsd[li, lw]

    mo = daily.assign(week=daily.day // 7).groupby(['pid', 'week']).month.first().rename('month').reset_index()
    lm = lm.merge(mo, on=['pid', 'week'], how='left')
    cols = ['pid', 'week', 'y', *LEVEL, *CHANGE, *QUALITY_COLS, 'month']
    return lm[cols]


def _design(model, lm):
    """Impute (training median) + missing indicators, then standardise with the training mean/SD."""
    X = lm[model['cols']].astype(float).to_numpy()
    nan = np.isnan(X)
    X = np.where(nan, model['med'], X)
    X = np.hstack([X, nan[:, model['miss_ix']].astype(float)])
    return (X - model['mu']) / model['sd']


def _logit_fit(X, y, l2, w0):
    """Penalised logistic regression (intercept unpenalised), L-BFGS-B with analytic gradient."""
    X1 = np.hstack([np.ones((len(X), 1)), X])

    def f(w):
        z = X1 @ w
        r = np.r_[0.0, w[1:]]
        return (np.logaddexp(0, z) - y * z).sum() + 0.5 * l2 * r @ r, X1.T @ (expit(z) - y) + l2 * r

    return minimize(f, w0, jac=True, method='L-BFGS-B').x


def _score(w, X):
    return expit(w[0] + X @ w[1:])


def _calibrate(model, s):
    a0, a1 = model['cal']
    return expit(a0 + a1 * logit(np.clip(s, 1e-9, 1 - 1e-9)))


def fit(lm_fit, lm_cal, cols, l2=1.0, n_boot=20, seed=0):
    """Fit on lm_fit, bootstrap people for a band, Platt-calibrate on lm_cal."""
    X0 = lm_fit[cols].astype(float).to_numpy()
    med = np.nan_to_num(np.nanmedian(X0, axis=0))
    miss_ix = np.flatnonzero(np.isnan(X0).any(axis=0))
    model = {'cols': list(cols), 'med': med, 'miss_ix': miss_ix}
    Z = np.hstack([np.where(np.isnan(X0), med, X0), np.isnan(X0)[:, miss_ix].astype(float)])
    model['mu'], sd = Z.mean(axis=0), Z.std(axis=0)
    model['sd'] = np.where(sd > 0, sd, 1.0)
    X, y = (Z - model['mu']) / model['sd'], lm_fit.y.to_numpy(float)
    w = _logit_fit(X, y, l2, np.zeros(X.shape[1] + 1))
    # ponytail: bootstrap refits reuse the full-fit standardisation/imputation; re-estimate per draw if it matters
    codes = pd.factorize(lm_fit.pid)[0]
    order = np.argsort(codes, kind='stable')
    bnd = np.searchsorted(codes[order], np.arange(codes.max() + 2))
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        pick = rng.integers(0, codes.max() + 1, codes.max() + 1)
        ix = np.concatenate([order[bnd[k]:bnd[k + 1]] for k in pick])
        boots.append(_logit_fit(X[ix], y[ix], l2, w))
    model.update(w=w, boots=np.array(boots).reshape(n_boot, len(w)))
    # ponytail: Platt, not isotonic — isotonic ties scores at 0 with few calibration events (kills ranking);
    # switch to isotonic once the calibration set has ~50+ events
    s = _score(w, _design(model, lm_cal))
    model['cal'] = _logit_fit(logit(np.clip(s, 1e-9, 1 - 1e-9))[:, None], lm_cal.y.to_numpy(float), 1e-6, np.zeros(2))
    return model


def predict(model, lm):
    """Add calibrated p and the bootstrap 10th/90th percentile band p_lo/p_hi (band widened to contain p)."""
    X = _design(model, lm)
    p = _calibrate(model, _score(model['w'], X))
    B = _calibrate(model, expit(model['boots'][:, :1].T + X @ model['boots'][:, 1:].T))
    out = lm.copy()
    out['p'] = p
    out['p_lo'] = np.minimum(np.percentile(B, 10, axis=1), p) if len(B.T) else p
    out['p_hi'] = np.maximum(np.percentile(B, 90, axis=1), p) if len(B.T) else p
    return out


def _auroc(y, s):
    r = pd.Series(s).rank().to_numpy()
    n1 = y.sum()
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))


if __name__ == '__main__':
    rng = np.random.default_rng(1)
    assert all('onset' not in c for c in FEATURE_SETS.values())
    assert set(FEATURE_SETS) == {'full', 'level_only', 'cuff_only', 'change_only'}

    def synth(n):  # easy signal: y ~ Bernoulli(sigmoid(2*x1 - 1)), some NaNs in x2
        d = pd.DataFrame({'pid': np.repeat([f'p{i}' for i in range(n)], 10), 'x1': rng.normal(size=n * 10),
                          'x2': rng.normal(size=n * 10)})
        d['y'] = (rng.random(len(d)) < expit(2 * d.x1 - 1)).astype(int)
        d.loc[rng.random(len(d)) < 0.1, 'x2'] = np.nan
        return d
    tr, ca, te = synth(150), synth(60), synth(60)
    m = fit(tr, ca, ['x1', 'x2'], n_boot=10)
    out = predict(m, te)
    auc = _auroc(te.y.to_numpy(), out.p.to_numpy())
    assert auc > 0.8, auc
    assert (out.p_lo <= out.p).all() and (out.p <= out.p_hi).all() and out.p.between(0, 1).all()
    assert (out.p_hi - out.p_lo).mean() > 0  # bootstrap band is not degenerate

    # make_landmarks: tiny cohort; converter c1 (t_ref=100), non-converter n1 (end_day=139)
    days = np.arange(140)
    daily = pd.concat([pd.DataFrame({'pid': p, 'day': days, 'month': 1 + days // 30 % 12, 'valid': True,
                                     'night_rhr_adj': 60 + rng.normal(size=140),
                                     'sbp': np.where(days % 10 == 0, 100 + days, np.nan),
                                     'dbp': np.where(days % 10 == 0, 60.0, np.nan)}) for p in ('c1', 'n1')])
    wk = pd.DataFrame([(p, w) for p in ('c1', 'n1') for w in range(20)], columns=['pid', 'week'])
    wk['dev'] = 0.1 * wk.week
    wk['cusum'], wk['n_exceed'], wk['n_eval'], wk['persist'], wk['evaluable'] = 0.0, 0, 6, False, True
    people = pd.DataFrame({'pid': ['c1', 'n1'], 'age': [50, 60], 'sex': ['M', 'F'], 'bmi': [25., 30.],
                           'converter': [True, False], 't_ref': [100., np.nan], 'onset': [50., np.nan],
                           'end_day': [139, 139]})
    lm = make_landmarks(wk, daily, people)
    c = lm[lm.pid == 'c1']
    assert c.week.max() == 100 // 7 - 1 and (c.week < 100 // 7).all()   # t_ref week excluded
    assert lm[lm.pid == 'n1'].week.max() == 139 // 7 and lm[lm.pid == 'n1'].y.eq(0).all()
    assert c.y.eq(1).all()                                              # t_ref within 26 weeks of every row
    assert (lm.cuff_days_since >= 0).all()
    assert ((lm.cuff_sbp_last - 100) == (7 * lm.week + 6 - lm.cuff_days_since)).all()  # no future cuff reads
    assert np.allclose(lm.dev_slope12[lm.week >= 5], 0.1) and lm.valid_days_30.max() == 30
    assert 'onset' not in lm.columns
    print('predict OK  auroc=%.3f' % auc)

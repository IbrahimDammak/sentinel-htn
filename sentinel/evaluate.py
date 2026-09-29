"""EVALUATE — challenge metrics A-F on decision tables (dec = warn.decide output). Self-check: python -m sentinel.evaluate"""
import numpy as np
import pandas as pd
from scipy.stats import rankdata

from .warn import first_warnings

NAN = float('nan')


def auroc(y, p):
    """AUROC by the rank formula; NaN if a class is missing."""
    y = np.asarray(y) == 1
    n1, n0 = y.sum(), (~y).sum()
    if n1 == 0 or n0 == 0:
        return NAN
    return float((rankdata(p)[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def auprc(y, p):
    """Average precision: sum over distinct thresholds of recall step x precision."""
    y, p = np.asarray(y) == 1, np.asarray(p, float)
    if y.sum() == 0:
        return NAN
    o = np.argsort(-p, kind='mergesort')
    y, p = y[o], p[o]
    last = np.r_[p[1:] != p[:-1], True]            # last row of each tie group
    tp = np.cumsum(y)[last]
    k = np.arange(1, len(y) + 1)[last]
    return float(np.sum(np.diff(np.r_[0, tp / y.sum()]) * tp / k))


def calibration_bins(y, p, nbins=10):
    """(mean p, mean y, count) per non-empty equal-width bin."""
    y, p = np.asarray(y, float), np.clip(np.asarray(p, float), 0, 1)
    b = np.minimum((p * nbins).astype(int), nbins - 1)
    rows = [(p[b == i].mean(), y[b == i].mean(), (b == i).sum()) for i in range(nbins) if (b == i).any()]
    return np.array(rows).reshape(-1, 3).T


def risk_coverage(dec):
    """Coverage and running Brier risk when weeks are kept from most to least confident (narrow p_hi-p_lo)."""
    d = dec.dropna(subset=['p', 'p_lo', 'p_hi', 'y'])
    loss = ((d.p - d.y) ** 2).to_numpy()[np.argsort((d.p_hi - d.p_lo).to_numpy(), kind='mergesort')]
    k = np.arange(1, len(loss) + 1)
    return k / max(len(loss), 1), np.cumsum(loss) / np.maximum(k, 1)


def lead_days(dec, people):
    """Per converter t_ref - first warning day (warnings before t_ref only); NaN = miss."""
    conv = people[people.converter.astype(bool) & people.t_ref.notna()].set_index('pid')
    fw = first_warnings(dec).set_index('pid').first_warning_day.reindex(conv.index)
    lead = conv.t_ref - fw
    return lead.where(lead > 0)


def metrics(dec, people, horizon_weeks=26):
    """Metrics A-F over the people given (converters without any warning count as misses)."""
    people = people.reset_index(drop=True)
    dec = dec[dec.pid.isin(people.pid)].sort_values(['pid', 'week'])
    d = dec.dropna(subset=['p', 'y'])
    y, p = d.y.to_numpy(float), d.p.to_numpy(float)
    out = {'auroc': auroc(y, p), 'auprc': auprc(y, p)}                                      # A
    lead = lead_days(dec, people)                                                           # B
    for k in (0, 30, 90, 180):
        out[f'sens_lead_{k}'] = float((lead >= k).mean()) if len(lead) else NAN
    out['median_lead'] = float(lead.median()) if lead.notna().any() else NAN
    warned = dec.state == 'WARNING'                                                         # C
    start = warned & ~warned.groupby(dec.pid).shift(fill_value=False).astype(bool)
    nc = people[~people.converter.astype(bool) & people.pid.isin(dec.pid)]                  # same exposure as warn.tune_warning
    years = (nc.end_day + 1).sum() / 365.25
    out['alarms_per_nonconv_py'] = float(start[dec.pid.isin(nc.pid)].sum() / years) if years else NAN
    fw = first_warnings(dec).dropna(subset=['first_warning_day']).merge(people[['pid', 'converter', 't_ref']], on='pid')
    gap = fw.t_ref - fw.first_warning_day
    out['warning_precision'] = float((fw.converter.astype(bool) & (gap > 0) & (gap <= 7 * horizon_weeks)).mean()) if len(fw) else NAN
    out['brier'] = float(np.mean((p - y) ** 2)) if len(y) else NAN                          # D
    mp, my, n = calibration_bins(y, p)
    out['ece'] = float((n * np.abs(mp - my)).sum() / n.sum()) if n.size else NAN
    out['aurc'] = float(risk_coverage(dec)[1].mean()) if len(y) else NAN                    # F
    rest = dec[~warned]
    out['abstention_rate'] = float((rest.state == 'POOR_QUALITY').mean()) if len(rest) else NAN
    out['n_people'], out['n_converters'] = len(people), int(people.converter.astype(bool).sum())
    return out


def by_group(dec, people, col, bins=3):
    """Metrics per group of people[col]; bins = int (quantile groups, 3 = terciles) or list of edges."""
    g = pd.qcut(people[col], bins, duplicates='drop', precision=1) if isinstance(bins, int) else pd.cut(people[col], bins)
    return pd.DataFrame({str(k): metrics(dec, s) for k, s in people.groupby(g, observed=True)}).T


if __name__ == '__main__':
    W, P, I = 'WARNING', 'POOR_QUALITY', 'INSUFFICIENT'
    people = pd.DataFrame({'pid': list('ABCD'), 'converter': [True, True, False, False],
                           't_ref': [100., 300., np.nan, np.nan], 'end_day': [100, 300, 200, 200]})
    rows = [  # pid, week, y, p, width, state (p_lo/p_hi = p -/+ width/2)
        ('A', 0, 1, .85, .10, I), ('A', 1, 1, .65, .40, W), ('A', 2, 1, .95, .05, W),
        ('B', 0, 0, .25, .20, I), ('B', 1, 1, .45, .25, P),
        ('C', 0, 0, .15, .15, I), ('C', 1, 0, .35, .35, W), ('C', 2, 0, .75, .30, I), ('C', 3, 0, .55, .45, W),
        ('D', 0, 0, .05, .50, P), ('D', 1, 0, .12, .55, I)]
    dec = pd.DataFrame(rows, columns=['pid', 'week', 'y', 'p', 'w', 'state'])
    dec['p_lo'], dec['p_hi'] = dec.p - dec.w / 2, dec.p + dec.w / 2
    m = metrics(dec, people)
    hand = {'auroc': 25 / 28, 'auprc': 41 / 48,          # 25 of 28 pos-neg pairs; AP = (1+1+3/4+2/3)/4
            'sens_lead_0': .5, 'sens_lead_30': .5, 'sens_lead_90': 0., 'sens_lead_180': 0.,  # A first warned day 7*1+6=13 -> lead 87; B missed
            'median_lead': 87.,
            'alarms_per_nonconv_py': 2 / (402 / 365.25),    # C has 2 episodes; C+D exposure = 201+201 days
            'warning_precision': .5,                        # warned A (converts in 87d) and C
            'brier': 1.5394 / 11,
            'ece': 3.32 / 11,                               # 9 singleton bins sum|p-y| = 3.05, one bin (.135 gap x 2)
            'aurc': 1.0742312 / 11,                         # mean of running Brier risk, most confident first
            'abstention_rate': 2 / 7}                       # 2 POOR_QUALITY among 7 non-WARNING weeks
    for k, v in hand.items():
        assert abs(m[k] - v) < 1e-6, (k, m[k], v)
    g = by_group(dec, people.assign(g=[0, 0, 1, 1]), 'g', 2)
    assert len(g) == 2 and g.n_converters.tolist() == [2, 0]
    print('evaluate self-check OK')

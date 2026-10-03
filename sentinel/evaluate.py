"""EVALUATE — challenge metrics A-F on decision tables (dec = warn.decide output). Self-check: python -m sentinel.evaluate"""
import numpy as np
import pandas as pd
from scipy.stats import rankdata

from .warn import first_warnings, prompts

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


def km_incidence(t, event, at):
    """Kaplan-Meier cumulative incidence 1 - S(a) for each a in `at`; t = event or censoring time, event = bool."""
    t, event = np.asarray(t, float), np.asarray(event, bool)
    u = np.unique(t[event])
    S = np.cumprod(1 - np.array([(event & (t == x)).sum() / (t >= x).sum() for x in u]))
    return [float(1 - (S[u <= a][-1] if (u <= a).any() else 1.0)) for a in at]


def sens_at_spec(cal, d, spec=0.92):
    """Landmark-level sensitivity at a fixed specificity; the threshold comes from the CALIBRATION set, never the test.

    thr = the `spec` quantile (method 'higher', an observed value) of calibrated p over the calibration people's y=0
    landmark weeks, so >= spec of them have p <= thr; a test week is positive if p > thr. Rows unweighted, as for
    AUROC. Returns test sensitivity (y=1 weeks), the test specificity actually reached (y=0 weeks) and thr."""
    c = cal.dropna(subset=['p', 'y'])
    thr = float(np.quantile(c.p[c.y == 0], spec, method='higher'))
    y, p = d.y.to_numpy() == 1, d.p.to_numpy(float)
    return {'sens_spec92': float((p[y] > thr).mean()) if y.any() else NAN,
            'spec_spec92_test': float((p[~y] <= thr).mean()) if (~y).any() else NAN, 'thr_spec92': thr}


def metrics(dec, people, horizon_weeks=26, cal=None):
    """Metrics A-F over the people given (converters without any warning count as misses).

    Person-level confusion at the system's operating point (the WARNING state: p_lo >= thr_p tuned on the calibration
    people to 0.5 alarms/non-converter person-year, AND persistence): TP = converter with a WARNING before t_ref
    (= sens_lead_0), FN = converter without one (abstention = miss), FP = non-converter (with landmarks) ever
    warned, TN = non-converter never warned. specificity = TN/(TN+FP); f1 = 2TP/(2TP+FP+FN): CUMULATIVE over the whole
    follow-up (followup_median_days), not a single-window specificity; ppv_person = TP/(TP+FP) at this cohort's
    conversion rate; lr_pos = sens_lead_0 / (FP share). cal = calibration-set predictions (pipeline
    models['pred_cal']) -> sens_at_spec keys (per landmark WEEK, not the operating point), else NaN.
    False prompts over time (non-converters; day 0 = start of the first landmark week, i.e. after the warm-up; a warning
    counts at the end of its week): Kaplan-Meier probability of >= 1 prompt by 6 / 12 months, censored at the last
    landmark week; false_prompts_per_nonconv = episodes per non-converter. alarms_per_nonconv_py divides by calendar
    time (end_day + 1, warm-up included); alarms_per_nonconv_monitored_py by landmark weeks only.
    prompts_per_nonconv_py_r26 = alarms_per_nonconv_py after warn.prompts' 26-week refractory period (burden only).
    sens_post_onset_30/90 (simulator, people.onset): as sens_lead_30/90, but a converter whose first warning came
    before the simulated drift onset counts as a miss; n_pre_onset_first_warnings = how many did."""
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
    tp, fn, fp = int(lead.notna().sum()), int(lead.isna().sum()), int(nc.pid.isin(dec.pid[warned]).sum())
    out['specificity'] = (len(nc) - fp) / len(nc) if len(nc) else NAN
    out['f1'] = 2 * tp / (2 * tp + fp + fn) if tp + fp + fn else NAN
    out['ppv_person'] = tp / (tp + fp) if tp + fp else NAN
    out['lr_pos'] = out['sens_lead_0'] / (fp / len(nc)) if fp else NAN
    dn = dec[dec.pid.isin(nc.pid)]                                                          # false prompts over time
    w0, w1 = dn.groupby('pid').week.min(), dn.groupby('pid').week.max()
    fwd = first_warnings(dn).set_index('pid').first_warning_day.reindex(w0.index)
    t = np.where(fwd.notna(), fwd + 1 - 7 * w0, 7 * (w1 - w0 + 1))
    out['false_prompt_6mo'], out['false_prompt_12mo'] = km_incidence(t, fwd.notna(), (365.25 / 2, 365.25)) if len(dn) else (NAN, NAN)
    out['followup_median_days'] = float(np.median(7 * (w1 - w0 + 1))) if len(dn) else NAN
    n_alarm = start[dec.pid.isin(nc.pid)].sum()
    out['false_prompts_per_nonconv'] = float(n_alarm / len(nc)) if len(nc) else NAN
    out['alarms_per_nonconv_monitored_py'] = float(n_alarm / (len(dn) * 7 / 365.25)) if len(dn) else NAN
    pr = prompts(dec)
    assert dec[pr].groupby('pid').week.min().equals(dec[start].groupby('pid').week.min())   # first warnings unchanged
    out['prompts_per_nonconv_py_r26'] = float(pr[dec.pid.isin(nc.pid)].sum() / years) if years else NAN
    onset = people[people.converter.astype(bool)].set_index('pid').onset.reindex(lead.index)
    pre = first_warnings(dec).set_index('pid').first_warning_day.reindex(lead.index) < onset
    for k in (30, 90):
        out[f'sens_post_onset_{k}'] = float(((lead >= k) & ~pre).mean()) if onset.notna().any() else NAN
    out['n_pre_onset_first_warnings'] = int(pre.sum()) if onset.notna().any() else NAN
    out.update(sens_at_spec(cal, d) if cal is not None else dict.fromkeys(['sens_spec92', 'spec_spec92_test', 'thr_spec92'], NAN))
    out['brier'] = float(np.mean((p - y) ** 2)) if len(y) else NAN                          # D
    mp, my, n = calibration_bins(y, p)
    out['ece'] = float((n * np.abs(mp - my)).sum() / n.sum()) if n.size else NAN
    out['aurc'] = float(risk_coverage(dec)[1].mean()) if len(y) else NAN                    # F
    rest = dec[~warned]
    out['abstention_rate'] = float((rest.state == 'POOR_QUALITY').mean()) if len(rest) else NAN
    out['n_people'], out['n_converters'] = len(people), int(people.converter.astype(bool).sum())
    return out


def by_group(dec, people, col, bins=3, cal=None):
    """Metrics per group of people[col]; bins = int (quantile groups, 3 = terciles) or list of edges."""
    g = pd.qcut(people[col], bins, duplicates='drop', precision=1) if isinstance(bins, int) else pd.cut(people[col], bins)
    return pd.DataFrame({str(k): metrics(dec, s, cal=cal) for k, s in people.groupby(g, observed=True)}).T


if __name__ == '__main__':
    W, P, I = 'WARNING', 'POOR_QUALITY', 'INSUFFICIENT'
    people = pd.DataFrame({'pid': list('ABCD'), 'converter': [True, True, False, False], 't_ref': [100., 300., np.nan, np.nan],
                           'onset': [10., 200., np.nan, np.nan], 'end_day': [100, 300, 200, 200]})
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
            'abstention_rate': 2 / 7,                       # 2 POOR_QUALITY among 7 non-WARNING weeks
            'specificity': .5, 'f1': .5,                    # TP A, FN B, FP C, TN D -> 1/2 and 2/(2+1+1)
            'ppv_person': .5, 'lr_pos': 1.,                 # 1/(1+1); sens .5 / FP share .5
            'false_prompt_6mo': .5, 'false_prompt_12mo': .5,  # C warned at day 14 of monitoring, D censored at 14: KM 1/2
            'followup_median_days': 21., 'false_prompts_per_nonconv': 1.,   # C 4 weeks, D 2 weeks; 2 episodes / 2
            'alarms_per_nonconv_monitored_py': 2 / (42 / 365.25),          # 6 non-converter landmark weeks
            'prompts_per_nonconv_py_r26': 1 / (402 / 365.25),               # C's 2nd start (wk 3) within 26 wk of wk 1
            'sens_post_onset_30': .5, 'sens_post_onset_90': 0., 'n_pre_onset_first_warnings': 0}  # A warned day 13 >= onset 10
    assert np.allclose(km_incidence([1, 2, 2, 3, 4], [1, 0, 1, 1, 0], [.5, 2.5, 10]), [0, .4, .7])  # S: .8, .8*3/4, .6/2
    for k, v in hand.items():
        assert abs(m[k] - v) < 1e-6, (k, m[k], v)
    assert np.isnan(m['sens_spec92'])                       # no calibration set given
    m2 = metrics(dec, people.assign(onset=[50., 200., np.nan, np.nan]))   # A's first warning (day 13) now pre-onset
    assert m2['n_pre_onset_first_warnings'] == 1 and m2['sens_post_onset_30'] == 0 and m2['sens_lead_30'] == .5
    assert np.isnan(metrics(dec, people.assign(onset=np.nan))['sens_post_onset_30'])   # real data: no onset
    cal = pd.DataFrame({'y': 0, 'p': 0.02 * np.arange(1, 26)})   # 0.92 quantile ('higher') of .02...50 -> .48
    s = metrics(dec, people, cal=pd.concat([cal, pd.DataFrame({'y': [1], 'p': [.01]})]))  # cal positives ignored
    assert s['thr_spec92'] == .48 and (cal.p <= .48).mean() >= .92
    assert s['sens_spec92'] == 3 / 4 and s['spec_spec92_test'] == 5 / 7  # y=1 p .85 .65 .95 > .48, .45 not; y=0: 5/7 <= .48
    g = by_group(dec, people.assign(g=[0, 0, 1, 1]), 'g', 2)
    assert len(g) == 2 and g.n_converters.tolist() == [2, 0]
    print('evaluate self-check OK')

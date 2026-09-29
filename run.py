"""SENTINEL-HTN CLI: Learn -> Detect -> Predict -> Warn -> Evaluate.

  python run.py --synthetic [--n 600 --days 540 --seed 0 --quick] --out results/
  python run.py --daily d.csv --people p.csv --out results/
"""
import argparse
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sentinel import CHANNELS
from sentinel import data, detect, learn, predict, warn
from sentinel.evaluate import by_group, calibration_bins, lead_days, metrics, risk_coverage

BASE = dict(personal=True, context=True, features='full', n_boot=20, seed=0)
ABLATIONS = {'level_only': {'features': 'level_only'}, 'cuff_only': {'features': 'cuff_only'},
             'change_only': {'features': 'change_only'}, 'no_personalisation': {'personal': False},
             'no_context': {'context': False}}
ROBUSTNESS = {'mcar_0.3': ('mcar', 0.3, {}), 'mcar_0.6': ('mcar', 0.6, {}), 'noise_1.0': ('noise', 1.0, {}),
              'drop_night_rmssd': ('drop_channel', 1.0, {'channel': 'night_rmssd'}), 'mnar_0.4': ('mnar', 0.4, {}),
              'sensor_fail_0.3': ('sensor_fail', 0.3, {})}
KEY = ['auroc', 'auprc', 'sens_lead_90', 'median_lead', 'alarms_per_nonconv_py', 'warning_precision',
       'brier', 'ece', 'aurc', 'abstention_rate']


def make_split(people, seed=0):
    """Subject-grouped 60/20/20 fit/cal/test split of pids, stratified by converter."""
    rng = np.random.default_rng(seed)
    out = {'fit': [], 'cal': [], 'test': []}
    for _, g in people.groupby(people.converter.astype(bool)):
        pid = rng.permutation(g.pid.to_numpy())
        a, b = int(.6 * len(pid)), int(.8 * len(pid))
        out['fit'] += list(pid[:a])
        out['cal'] += list(pid[a:b])
        out['test'] += list(pid[b:])
    return out


def _adjust(d, ctx):
    """Context-adjust gated days; ctx=None is the no-context ablation (adj = raw)."""
    if ctx is not None:
        return learn.apply_context(d, ctx)
    d = d.copy()
    for ch in CHANNELS:
        d[ch + '_adj'] = d[ch]
    return d


def _weeks(d, prior, cfg, thr=None):
    """Personal baseline -> weekly deviation -> CUSUM (-> persistence if thr given)."""
    wk = detect.cusum(detect.weekly(learn.personal_baseline(d, prior, personal=cfg['personal'])))
    return wk if thr is None else detect.persistence(wk, thr)


def _landmarks(wk, d, people):
    return predict.make_landmarks(wk, d, people[people.pid.isin(wk.pid.unique())])


def pipeline(daily, people, split, cfg, fitted=None, perturb=None):
    """Fit on clean fit/cal people, then score the test people -> (dec_test, wk_test, models, thresholds).

    split = {'fit','cal','test'} pid lists; cfg = BASE-like dict. fitted=(models, thresholds) skips fitting;
    perturb=(kind, level, kwargs) degrades the TEST daily only (models stay fitted on clean data)."""
    inn = lambda df, k: df[df.pid.isin(split[k])]
    if fitted is None:
        d = learn.quality_gate(daily[daily.pid.isin(split['fit'] + split['cal'])])
        ctx = learn.fit_context(inn(d, 'fit')) if cfg['context'] else None
        d = _adjust(d, ctx)
        prior = learn.fit_prior(inn(d, 'fit'))
        wk = _weeks(d, prior, cfg)
        # two tiers: persistence = loose "watch" tier (2 episodes/py); the risk gate then confirms to 0.5/py
        thr = detect.tune_threshold(inn(wk, 'fit'), inn(people, 'fit'), budget=2.0)
        wk = detect.persistence(wk, thr)
        lm = _landmarks(wk, d, people)
        model = predict.fit(inn(lm, 'fit'), inn(lm, 'cal'), predict.FEATURE_SETS[cfg['features']],
                            n_boot=cfg['n_boot'], seed=cfg['seed'])
        thr_p = warn.tune_warning(predict.predict(model, inn(lm, 'cal')), inn(people, 'cal'))
        fitted = ({'ctx': ctx, 'prior': prior, 'model': model}, {'thr': thr, 'thr_p': thr_p})
    models, th = fitted
    dt = inn(daily, 'test')
    if perturb:
        kind, level, kw = perturb
        dt = data.perturb(dt, kind, level, seed=cfg['seed'], people=inn(people, 'test'), **kw)
    d = _adjust(learn.quality_gate(dt), models['ctx'])
    wk = _weeks(d, models['prior'], cfg, th['thr'])
    dec = warn.decide(predict.predict(models['model'], _landmarks(wk, d, people)), th['thr_p'])
    return dec, wk, models, th


def _clean(o):
    """JSON-safe copy: numpy -> python, NaN -> None."""
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (float, np.floating)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def _f(v):
    return 'n/a' if v is None or pd.isna(v) else f'{v:.3f}'


def table(rows, cols, ref=None):
    """Markdown table of {run: metrics}; if ref (a run name) is given, other rows show (delta vs ref)."""
    out = ['| run | ' + ' | '.join(cols) + ' |', '|---' * (len(cols) + 1) + '|']
    for name, m in rows.items():
        cells = []
        for c in cols:
            s = str(int(m[c])) if c.startswith('n_') else _f(m[c])
            if ref and name != ref and not (pd.isna(m[c]) or pd.isna(rows[ref][c])):
                s += f' ({m[c] - rows[ref][c]:+.3f})'
            cells.append(s)
        out.append(f'| {name} | ' + ' | '.join(cells) + ' |')
    return '\n'.join(out)


def example_ledger(dec, wk, tp):
    """Evidence ledger at the first warning of the warned converter with median lead."""
    lead = lead_days(dec, tp).dropna()
    if lead.empty:
        return None
    pid = (lead - lead.median()).abs().idxmin()
    fw = warn.first_warnings(dec).set_index('pid').loc[pid]
    week = int(fw.first_warning_week)
    return {'pid': pid, 'week': week, 'first_warning_day': fw.first_warning_day, 'lead_days': lead[pid],
            **warn.ledger(dec, wk, pid, week)}


def figures(out, dec, decs, tp):
    d = dec.dropna(subset=['p', 'y'])
    mp, my, n = calibration_bins(d.y, d.p)
    fig, ax = plt.subplots(figsize=(4.5, 4.5))
    ax.plot([0, 1], [0, 1], 'k--', lw=1)
    ax.plot(mp, my, 'o-')
    ax.set(xlabel='predicted risk', ylabel='observed conversion within horizon', title='Calibration (test)')
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'calibration.png'), dpi=120)
    lead = lead_days(dec, tp)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.hist(lead.dropna(), bins=12)
    ax.set(xlabel='lead time before clinical reference (days)', ylabel='converters',
           title=f'Lead time: {lead.notna().sum()}/{len(lead)} converters warned')
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'lead_time.png'), dpi=120)
    fig, ax = plt.subplots(figsize=(5, 3.5))
    for name, dd in decs.items():
        ax.plot(*risk_coverage(dd), label=name, lw=2 if name == 'full' else 1)
    ax.set(xlabel='coverage (most confident weeks first)', ylabel='Brier risk', title='Risk-coverage')
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'risk_coverage.png'), dpi=120)
    plt.close('all')


def write_report(path, res, args_str):
    groups = [('A', ['auroc', 'auprc']), ('B', ['sens_lead_0', 'sens_lead_30', 'sens_lead_90', 'sens_lead_180', 'median_lead']),
              ('C', ['alarms_per_nonconv_py', 'warning_precision']), ('D', ['brier', 'ece']),
              ('F', ['aurc', 'abstention_rate'])]
    main = res['main']
    L = ['# SENTINEL-HTN results', '', f'Run: {args_str}. Test people: {main["n_people"]} ({main["n_converters"]} converters). '
         f'Thresholds: persistence dev > {res["thresholds"]["thr"]:.3f}, warning p_lo >= {res["thresholds"]["thr_p"]:.3f}. '
         'Synthetic data unless stated; research prototype, not a diagnostic; no blood-pressure value is output.', '',
         '## Main model (metrics A-F, held-out test people)', '', '| set | metric | value |', '|---|---|---|']
    L += [f'| {g} | {k} | {_f(main[k])} |' for g, ks in groups for k in ks]
    L += ['', '## Ablations vs full (delta vs full in parentheses)', '',
          table({'full': main, **res['ablations']}, KEY, ref='full'), '',
          '## Robustness (E): test people perturbed, models fitted on clean data', '',
          table({'clean': main, **res['robustness']}, KEY, ref='clean'), '',
          '## Fairness (E8): by skin_ita tercile', '',
          table({k: v for k, v in res['fairness'].items()}, ['n_people', 'n_converters', *KEY]), '',
          '## Example evidence ledger (first warning of a warned converter)', '']
    L += ['```json', json.dumps(_clean(res['ledger']), indent=2), '```'] if res['ledger'] else ['No converter was warned before t_ref in the test set.']
    L += ['', 'Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`.', '']
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--synthetic', action='store_true')
    ap.add_argument('--daily')
    ap.add_argument('--people')
    ap.add_argument('--n', type=int, default=600)
    ap.add_argument('--days', type=int, default=540)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--quick', action='store_true', help='n=150, days=360, n_boot=5')
    ap.add_argument('--out', default='results')
    a = ap.parse_args()
    if not a.synthetic and not (a.daily and a.people):
        ap.error('give --synthetic or both --daily and --people')
    n, days, n_boot = (150, 360, 5) if a.quick else (a.n, a.days, BASE['n_boot'])
    daily, people = data.make_cohort(n, days, a.seed) if a.synthetic else data.load_csv(a.daily, a.people)
    split = make_split(people, a.seed)
    tp = people[people.pid.isin(split['test'])]
    cfg = {**BASE, 'n_boot': n_boot, 'seed': a.seed}
    os.makedirs(a.out, exist_ok=True)

    dec, wk, models, th = pipeline(daily, people, split, cfg)
    res = {'main': metrics(dec, tp), 'thresholds': th, 'ablations': {}, 'robustness': {}}
    decs = {'full': dec}
    for name, over in ABLATIONS.items():
        decs[name] = pipeline(daily, people, split, {**cfg, **over})[0]
        res['ablations'][name] = metrics(decs[name], tp)
    for name, pt in ROBUSTNESS.items():
        res['robustness'][name] = metrics(pipeline(daily, people, split, cfg, (models, th), pt)[0], tp)
    res['fairness'] = by_group(dec, tp, 'skin_ita', 3).to_dict('index')
    res['ledger'] = example_ledger(dec, wk, tp)

    with open(os.path.join(a.out, 'metrics.json'), 'w') as f:
        json.dump(_clean(res), f, indent=2)
    write_report(os.path.join(a.out, 'report.md'), res, f'n={n}, days={days}, seed={a.seed}, n_boot={n_boot}')
    figures(a.out, dec, decs, tp)

    m = res['main']
    print(f'SENTINEL-HTN ({n} people, {days} days; test {m["n_people"]} people, {m["n_converters"]} converters)')
    print(f'  AUROC {_f(m["auroc"])}  AUPRC {_f(m["auprc"])}  Brier {_f(m["brier"])}  ECE {_f(m["ece"])}')
    print(f'  sens@lead 30/90/180d {_f(m["sens_lead_30"])}/{_f(m["sens_lead_90"])}/{_f(m["sens_lead_180"])}  '
          f'median lead {_f(m["median_lead"])} d')
    print(f'  alarms/non-converter-yr {_f(m["alarms_per_nonconv_py"])}  warning precision {_f(m["warning_precision"])}  '
          f'AURC {_f(m["aurc"])}  abstention {_f(m["abstention_rate"])}')
    print(f'  wrote {a.out}/metrics.json, report.md, calibration.png, lead_time.png, risk_coverage.png')


if __name__ == '__main__':
    main()

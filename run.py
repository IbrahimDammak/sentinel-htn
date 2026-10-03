"""SENTINEL-HTN CLI: Learn -> Detect -> Predict -> Warn -> Evaluate.

  python run.py --synthetic [--n 600 --days 540 --seed 0 --quick] --out results/
  python run.py --daily d.csv --people p.csv --out results/
  python run.py --summary results/pulse [--ref results/weighted]   # mean +- SD over results/pulse/seed*/metrics.json
  python run.py --sweep results/pulse/coupling_0 results/pulse results/pulse/coupling_2x --out results/pulse
"""
import argparse
import glob
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sentinel import CHANNELS, EVIDENCE, PULSE, channels
from sentinel import data, detect, learn, predict, warn
from sentinel.evaluate import by_group, calibration_bins, lead_days, metrics, risk_coverage

# pulse OFF by default: unvalidated channels have to earn their way in (CONTRACT.md); with_pulse is a variant.
BASE = dict(personal=True, context=True, features='full', weights='evidence', pulse=False, n_boot=20, seed=0)
ABLATIONS = {'level_only': {'features': 'level_only'}, 'cuff_only': {'features': 'cuff_only'},
             'change_only': {'features': 'change_only'}, 'no_personalisation': {'personal': False},
             'no_context': {'context': False}, 'equal_weights': {'weights': 'equal'},
             'reliability_only': {'weights': 'reliability'}, 'with_pulse': {'pulse': True}}
ROBUSTNESS = {'mcar_0.3': ('mcar', 0.3, {}), 'mcar_0.6': ('mcar', 0.6, {}), 'noise_1.0': ('noise', 1.0, {}),
              'drop_night_rmssd': ('drop_channel', 1.0, {'channel': 'night_rmssd'}), 'mnar_0.4': ('mnar', 0.4, {}),
              'sensor_fail_0.3': ('sensor_fail', 0.3, {})}
BUDGETS = (0.25, 0.5, 1.0, 2.0)   # warning episodes per non-converter person-year (operating curve)
KEY = ['auroc', 'auprc', 'sens_spec92', 'sens_lead_0', 'sens_lead_30', 'sens_lead_90', 'median_lead', 'alarms_per_nonconv_py', 'warning_precision',
       'specificity', 'f1', 'brier', 'ece', 'aurc', 'abstention_rate']


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
    for ch in channels(d):
        d[ch + '_adj'] = d[ch]
    return d


def _weeks(d, prior, cfg, thr=None, weights=None):
    """Personal baseline -> weekly (weighted) deviation -> CUSUM (-> persistence if thr given)."""
    wk = detect.cusum(detect.weekly(learn.personal_baseline(d, prior, personal=cfg['personal']), weights))
    return wk if thr is None else detect.persistence(wk, thr)


def _weights(d, prior, cfg):
    """Label-free channel weights on d (training or unlabelled real data); None = equal weights."""
    if cfg['weights'] == 'equal':
        return None
    ev = EVIDENCE if cfg['weights'] == 'evidence' else dict.fromkeys(CHANNELS + PULSE, 1.0)
    return detect.channel_weights(detect.weekly(learn.personal_baseline(d, prior, personal=cfg['personal'])), ev)


def _trend_r(wk):
    """Kalman observation variance = variance of the weekly deviation on evaluable weeks (label-free)."""
    return float(wk.loc[wk.evaluable, 'dev'].var())


def _landmarks(wk, d, people, trend_r=None):
    return predict.make_landmarks(wk, d, people[people.pid.isin(wk.pid.unique())], trend_r=trend_r)


def pipeline(daily, people, split, cfg, fitted=None, perturb=None):
    """Fit on clean fit/cal people, then score the test people -> (dec_test, wk_test, models, thresholds).

    split = {'fit','cal','test'} pid lists; cfg = BASE-like dict. fitted=(models, thresholds) skips fitting;
    perturb=(kind, level, kwargs) degrades the TEST daily only (models stay fitted on clean data).
    cfg['pulse'] False (the default) drops the optional PULSE columns everywhere; True = the with_pulse variant."""
    inn = lambda df, k: df[df.pid.isin(split[k])]
    if not cfg['pulse']:
        daily = daily.drop(columns=PULSE, errors='ignore')
    if fitted is None:
        d = learn.quality_gate(daily[daily.pid.isin(split['fit'] + split['cal'])])
        ctx = learn.fit_context(inn(d, 'fit')) if cfg['context'] else None
        d = _adjust(d, ctx)
        prior = learn.fit_prior(inn(d, 'fit'))
        weights = _weights(inn(d, 'fit'), prior, cfg)
        wk = _weeks(d, prior, cfg, weights=weights)
        trend_r = _trend_r(inn(wk, 'fit'))
        # two tiers: persistence = loose "watch" tier (2 episodes/py); the risk gate then confirms to 0.5/py
        thr = detect.tune_threshold(inn(wk, 'fit'), inn(people, 'fit'), budget=2.0)
        wk = detect.persistence(wk, thr)
        lm = _landmarks(wk, d, people, trend_r)
        model = predict.fit(inn(lm, 'fit'), inn(lm, 'cal'), predict.FEATURE_SETS[cfg['features']],
                            n_boot=cfg['n_boot'], seed=cfg['seed'])
        pred_cal = predict.predict(model, inn(lm, 'cal'))
        thr_p = warn.tune_warning(pred_cal, inn(people, 'cal'))
        fitted = ({'ctx': ctx, 'prior': prior, 'weights': weights, 'trend_r': trend_r, 'model': model,
                   'pred_cal': pred_cal}, {'thr': thr, 'thr_p': thr_p})
    models, th = fitted
    dt = inn(daily, 'test')
    if perturb:
        kind, level, kw = perturb
        dt = data.perturb(dt, kind, level, seed=cfg['seed'], people=inn(people, 'test'), **kw)
    d = _adjust(learn.quality_gate(dt), models['ctx'])
    wk = _weeks(d, models['prior'], cfg, th['thr'], models['weights'])
    dec = warn.decide(predict.predict(models['model'], _landmarks(wk, d, people, models['trend_r'])), th['thr_p'])
    return dec, wk, models, th


def usage(dec, wk, d, people):
    """Label-free deployment metrics; every person is treated as a non-converter."""
    srt = dec.sort_values(['pid', 'week'])
    py = len(srt) / detect.WEEKS_PER_YEAR
    warned = warn._episodes((srt.state == 'WARNING').to_numpy(), srt.pid.to_numpy())
    days = (people.set_index('pid').end_day.reindex(srt.pid.unique()) + 1).sum()
    ok = d[d.valid]
    return {'people': int(srt.pid.nunique()), 'person_years': py,
            'valid_day_share': float(d.valid.sum() / days),
            **{f'cover_{c}': float(ok[c].notna().mean()) for c in CHANNELS},
            'evaluable_week_share': float(wk.evaluable.mean()),
            'dev_sd': float(wk.loc[wk.evaluable, 'dev'].std()),
            'abstention_rate': float((srt.state == 'POOR_QUALITY').mean()),
            'watch_episodes_py': float(wk.groupby('pid').episodes.max().sum() / py),
            'warning_episodes_py': warned / py,
            'people_warned': float(srt[srt.state == 'WARNING'].pid.nunique() / srt.pid.nunique())}


def real_world(daily, people, cfg, fitted):
    """Transfer test on an unlabelled real cohort: risk model and thresholds come from synthetic training;
    only the label-free parts (context coefficients, population prior, channel weights, trend noise) are refitted."""
    models, th = fitted
    d = learn.quality_gate(daily)
    d = _adjust(d, learn.fit_context(d) if cfg['context'] else None)
    prior = learn.fit_prior(d)
    wk = _weeks(d, prior, cfg, th['thr'], _weights(d, prior, cfg))
    dec = warn.decide(predict.predict(models['model'], _landmarks(wk, d, people, _trend_r(wk))), th['thr_p'])
    return usage(dec, wk, d, people)


def operating_curve(fits, people, split, budgets=BUDGETS):
    """Early-warning operating curve: for each warning budget, re-tune thr_p on the calibration people and
    re-decide the test weeks -> {model: {budget: sens_lead_90, alarms, precision}}. fits = {name: (dec, models)}.
    'chance' = no-skill floor: warnings at random times at rate = budget, from baseline-ready to t_ref - 90 d."""
    cal, tp = people[people.pid.isin(split['cal'])], people[people.pid.isin(split['test'])]
    out = {}
    for name, (dec, models) in fits.items():
        out[name] = {}
        for b in budgets:
            m = metrics(warn.decide(dec, warn.tune_warning(models['pred_cal'], cal, budget=b)), tp)
            out[name][b] = {k: m[k] for k in ('sens_lead_0', 'sens_lead_30', 'sens_lead_90', 'alarms_per_nonconv_py',
                                              'warning_precision')}
    out['chance'] = {b: {**chance_floor(fits['full'][0], tp, b), 'alarms_per_nonconv_py': b,
                         'warning_precision': float('nan')} for b in budgets}
    return out


def chance_floor(dec, tp, b):
    """No-skill floor: random warnings at rate b per person-year from baseline-ready on. sens_lead_L = P(>= 1 warning
    in [start, t_ref - L]); sens_post_onset_L scores like evaluate's sens_post_onset (a first warning before the
    simulated drift onset = miss): P(none in [start, onset)) * P(>= 1 in [max(onset, start), t_ref - L])."""
    conv = tp[tp.converter.astype(bool)]
    yr = lambda s: s.clip(lower=0).fillna(0).to_numpy() / 365.25
    start = conv.pid.map(7 * dec.groupby('pid').week.min())
    out = {f'sens_lead_{L}': float(np.mean(1 - np.exp(-b * yr(conv.t_ref - L - start)))) for L in (0, 30, 90)}
    if 'onset' in conv and conv.onset.notna().any():
        on = conv.onset.fillna(-np.inf)                                  # converter without latent onset: never pre-onset
        for L in (30, 90):
            pre, post = yr(np.minimum(on, conv.t_ref - L) - start), yr(conv.t_ref - L - np.maximum(on, start))
            out[f'sens_post_onset_{L}'] = float(np.mean(np.exp(-b * pre) * (1 - np.exp(-b * post))))
    return out


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


def figures(out, dec, decs, tp, curve):
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
    fig, ax = plt.subplots(figsize=(5, 3.5))
    for name, rows in curve.items():
        r = list(rows.values())
        ax.plot([v['alarms_per_nonconv_py'] for v in r], [v['sens_lead_90'] for v in r],
                'k--' if name == 'chance' else 'o-', label=name, lw=2 if name == 'full' else 1)
    ax.set(xlabel='warning alarms per non-converter person-year (test)', ylabel='sensitivity at >= 90 d lead',
           title='Early-warning operating curve')
    ax.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(out, 'lead_vs_budget.png'), dpi=120)
    plt.close('all')


DEFS = ('sens_spec92 = per-WEEK sensitivity at 92% per-WEEK specificity: landmark weeks, p threshold from the y=0 weeks of '
        "the CALIBRATION people (spec_spec92_test = per-week specificity reached on test); not the system's operating "
        'point. specificity = non-converters never prompted during follow-up (median {fu:.1f} months of monitoring after '
        'the warm-up): CUMULATIVE over follow-up, not a single-window specificity; f1 and ppv_person (person-level PPV of '
        'a prompt) at this test conversion rate of {prev:.0%}; lr_pos = Se0 / share of non-converters prompted. '
        'false_prompt_6mo / 12mo = Kaplan-Meier probability that a non-converter has >= 1 false prompt by 6 / 12 months '
        'of monitoring (day 0 = first landmark week, censored at end of follow-up). alarms_per_nonconv_py: per calendar '
        'person-year (warm-up included); alarms_per_nonconv_monitored_py: per monitored (post-warm-up) person-year. '
        'prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year after '
        'a 26-week refractory period (chosen to equal the 26-week prediction horizon; not the clinical panel rule of 13 weeks after a normal cuff series). It is a '
        'burden metric only: first warnings, every other metric, the tuned thresholds and the chance floor use the '
        'unsuppressed episodes. sens_post_onset_30/90 = Se30/Se90 counting a first warning before the simulated drift '
        'onset as a miss (n_pre_onset_first_warnings = how many); sens_lead_* count every warning before t_ref.')


def write_report(path, res, args_str):
    groups = [('A', ['auroc', 'auprc', 'sens_spec92', 'spec_spec92_test', 'thr_spec92']),
              ('B', ['sens_lead_0', 'sens_lead_30', 'sens_lead_90', 'sens_lead_180', 'median_lead',
                     'sens_post_onset_30', 'sens_post_onset_90', 'n_pre_onset_first_warnings']),
              ('C', ['alarms_per_nonconv_py', 'alarms_per_nonconv_monitored_py', 'prompts_per_nonconv_py_r26',
                     'warning_precision', 'specificity', 'f1', 'ppv_person', 'lr_pos', 'false_prompt_6mo',
                     'false_prompt_12mo', 'followup_median_days', 'false_prompts_per_nonconv']),
              ('D', ['brier', 'ece']), ('F', ['aurc', 'abstention_rate'])]
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
          table(res['fairness'], ['n_people', 'n_converters', *KEY]), '',
          '## By age tercile (years): model behaviour by age; age has no causal role in the simulator', '',
          table(res['by_age'], ['n_people', 'n_converters', *KEY]), '', DEFS.format(
              fu=main['followup_median_days'] / 30.44, prev=main['n_converters'] / main['n_people']), '',
          '## Early-warning operating curve: sensitivity at >= 90 d lead (alarms/non-converter-yr) per warning budget', '',
          '| budget | ' + ' | '.join(res['operating_curve']) + ' |', '|---' * (len(res['operating_curve']) + 1) + '|']
    L += [f'| {b} | ' + ' | '.join(f"{_f(c[b]['sens_lead_90'])} ({_f(c[b]['alarms_per_nonconv_py'])})"
                                    for c in res['operating_curve'].values()) + ' |' for b in BUDGETS]
    L += ['', '## Example evidence ledger (first warning of a warned converter)', '']
    L += ['```json', json.dumps(_clean(res['ledger']), indent=2), '```'] if res['ledger'] else ['No converter was warned before t_ref in the test set.']
    L += ['', 'Figures: `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`.', '']
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


def _ms(xs):
    return 'n/a' if any(x is None for x in xs) else f'{np.mean(xs):.3f} ± {np.std(xs, ddof=1):.3f}'


def _leaves(o, path=()):
    """(path, value) for every leaf of a nested dict."""
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _leaves(v, path + (k,))
    else:
        yield path, o


def _at_rate(curve, k, rate):
    """Sensitivity k along an operating curve ({budget: metrics}) at a realised test alarm rate: linear interpolation
    (0 alarms = 0 sensitivity; clamped beyond the curve's largest realised rate)."""
    x, y = zip(*sorted([(0.0, 0.0)] + [(v['alarms_per_nonconv_py'], v[k]) for v in curve.values()]))
    return float(np.interp(rate, x, y))


def _matched(r, b, k):
    """(main, with_pulse) sensitivity k at main's realised test alarm rate for warning budget b (metrics.json)."""
    oc = r['operating_curve']
    return oc['full'][b][k], _at_rate(oc['with_pulse'], k, oc['full'][b]['alarms_per_nonconv_py'])


def _row(label, pairs):
    """'| label | main | with_pulse | per-seed diff | mean ± SD | seeds with_pulse > main |' from per-seed (main, wp)."""
    m, w = zip(*pairs)
    if None in m + w:
        return f'| {label} | n/a | n/a | | | |'
    diff = [b - a for a, b in pairs]
    return (f'| {label} | {_ms(m)} | {_ms(w)} | ' + ' '.join(f'{x:+.3f}' for x in diff)
            + f' | {_ms(diff)} | {sum(x > 0 for x in diff)}/{len(diff)} |')


ARM_HEAD = ['| metric | main (no pulse) | with_pulse | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |',
            '|---|---|---|---|---|---|']
BURDEN = ['false_prompt_6mo', 'false_prompt_12mo', 'followup_median_days', 'specificity', 'false_prompts_per_nonconv',
          'ppv_person', 'lr_pos', 'alarms_per_nonconv_py', 'alarms_per_nonconv_monitored_py', 'prompts_per_nonconv_py_r26']
ONSET = ['sens_lead_30', 'sens_post_onset_30', 'sens_lead_90', 'sens_post_onset_90', 'n_pre_onset_first_warnings']


def summarise(root, ref=None):
    """root/summary.md: mean ± SD (ddof=1) over root/seed*/metrics.json; main = pulse OFF, with_pulse = the variant.
    ref = directory of earlier runs with the same seed folders: every value they share with this run must be equal
    (with pulse off by default, main == results/weighted)."""
    files = sorted(glob.glob(os.path.join(root, 'seed*', 'metrics.json')))
    runs = {os.path.basename(os.path.dirname(f)): json.load(open(f)) for f in files}
    R = list(runs.values())
    arms = lambda k: [(r['main'][k], r['ablations']['with_pulse'][k]) for r in R]

    def tab(rows, cols):
        out = ['| run | ' + ' | '.join(cols) + ' |', '|---' * (len(cols) + 1) + '|']
        return out + [f'| {name} | ' + ' | '.join(_ms([g(r)[c] for r in R]) for c in cols) + ' |' for name, g in rows]
    # decision rule (written after the own-operating-point results were known; the effect sizes carry the verdict): a gain needs with_pulse > main in every seed for AUROC and matched Se30 and Se90 at budget 0.5
    gain = all(w > m for k in ('sens_lead_30', 'sens_lead_90') for m, w in (_matched(r, '0.5', k) for r in R)) \
        and all(w > m for m, w in arms('auroc'))
    L = [f'# SENTINEL-HTN: main model (pulse OFF) and the with_pulse variant: {len(R)} seeds '
         f'({", ".join(runs)}), mean ± SD over seeds', '',
         'Synthetic cohort (calibrated simulator). with_pulse adds the optional pulse_htn channel (the embedding-drift '
         'channel pulse_drift was removed after the audit: non-directional, near-zero simulated signal). Its '
         f'within-person BP coupling ({R[0].get("pulse_coupling")} night SD per mmHg here, the cross-sectional slope, an '
         'UPPER bound) and night-to-night noise are ASSUMPTIONS (CONTRACT.md). The zero-coupling arm is in '
         'coupling_sweep.md and must be read with every with_pulse number.', '',
         f'**Result: {"a consistent gain" if gain else "no improvement"} from the pulse channel** (decision rule, set after the own-operating-point results were known: '
         "with_pulse above main in every seed for AUROC and for Se30 and Se90 at main's realised alarm rate, budget 0.5). "
         'Separately tuned thresholds put the two arms at different alarm rates, so a lower alarm rate or a higher '
         'cumulative specificity for with_pulse at its own operating point is an operating-point shift, not better '
         'separation; compare the arms at matched alarm rates below.', '',
         '## with_pulse vs main at matched alarm rates (operating curve)', '',
         "For each warning budget (thresholds tuned on calibration people), main's realised test alarm rate is the "
         "reference; with_pulse's sensitivity is read off its own operating curve at that rate (linear interpolation, "
         '0 alarms = 0). Se0 = warned before t_ref; Se30 / Se90 = warned >= 30 / 90 days before t_ref.', '',
         "| budget | realised alarms/py: main; with_pulse | metric | main | with_pulse at main's rate | with_pulse - main "
         'per seed | mean ± SD | seeds with_pulse > main |', '|---|---|---|---|---|---|---|---|']
    for b in R[0]['operating_curve']['full']:
        al = '; '.join(_ms([r['operating_curve'][a][b]['alarms_per_nonconv_py'] for r in R]) for a in ('full', 'with_pulse'))
        L += [f'| {b} | {al} ' + _row(k, [_matched(r, b, k) for r in R]) for k in ('sens_lead_0', 'sens_lead_30', 'sens_lead_90')]
    L += ['', '## Main model and ablations (with_pulse = main + pulse_htn), each at its own operating point', '']
    L += tab([('main (no pulse)', lambda r: r['main'])] + [(k, lambda r, k=k: r['ablations'][k]) for k in R[0]['ablations']], KEY)
    L += ['', '## with_pulse minus main at their own operating points (NOT alarm-matched), per seed', '', *ARM_HEAD]
    L += [_row(k, arms(k)) for k in KEY]
    L += ['', '## False prompts over time (non-converters, test people)', '',
          'Day 0 = first landmark week (after the personal-baseline warm-up). false_prompt_6mo / 12mo = Kaplan-Meier '
          'probability of >= 1 false prompt by 6 / 12 months of monitoring, censored at end of follow-up. specificity = '
          'non-converters never prompted, CUMULATIVE over the median follow-up (followup_median_days), not a '
          'single-window specificity. ppv_person = person-level PPV of a prompt at the test conversion rate '
          f'({_ms([r["main"]["n_converters"] / r["main"]["n_people"] for r in R])}); lr_pos = Se0 / share of '
          'non-converters prompted. alarms_per_nonconv_py divides by calendar time (warm-up included), '
          'alarms_per_nonconv_monitored_py by monitored, post-warm-up time.', '',
          'prompts_per_nonconv_py_r26 = prompts (confirmatory home-BP weeks) per non-converter calendar person-year with '
          "repeat suppression: a 26-week refractory period after each prompt (not the clinical panel's rule, which was 13 weeks after a normal cuff series), because "
          '26 weeks is the prediction horizon. It is a BURDEN metric only: first warnings are unchanged (asserted in '
          "evaluate.metrics), and every other metric, the tuned thresholds and the operating curve's chance floor use "
          'the unsuppressed episodes.', '', *ARM_HEAD]
    L += [_row(k, arms(k)) for k in BURDEN]
    L += ['', '## Pre-onset warnings (simulator: drift onset known)', '',
          'sens_post_onset_30/90 = Se30/Se90 counting a converter whose first warning came BEFORE the simulated drift onset '
          'as a miss (an added sensitivity analysis; sens_lead_* are unchanged and count every warning before t_ref). '
          'n_pre_onset_first_warnings = converters whose first warning preceded onset.', '', *ARM_HEAD]
    L += [_row(k, arms(k)) for k in ONSET]
    L += ['', '## Robustness (test people perturbed; with_pulse_drop_pulse = with_pulse model, pulse removed at test time)', '']
    L += tab([('clean', lambda r: r['main'])] + [(k, lambda r, k=k: r['robustness'][k]) for k in R[0]['robustness']], KEY)
    for key, title, note in (('fairness', 'skin_ita', ''),
                             ('by_age', 'age', ': model behaviour by age; age has no causal role in the simulator')):
        L += ['', f'## By {title} tercile, main model (T1 = lowest; edges differ per seed){note}', '']
        L += tab([(f'T{i + 1}', lambda r, i=i: list(r[key].values())[i]) for i in range(3)], ['n_people', 'n_converters', *KEY])
    for key in ('weights', 'weights_with_pulse'):
        L += ['', f'## Normalised channel weights ({key}), per seed', '']
        L += ['- ' + ', '.join(f'{c} {w / sum(r[key].values()):.2f}' for c, w in r[key].items()) for r in R]
    led = R[0].get('ledger_with_pulse')
    if led:
        L += ['', f'Example with_pulse ledger ({list(runs)[0]}, {led["pid"]} week {led["week"]}): channel_contrib (mean '
              'weekly z, last 6 weeks) ' + ', '.join(f'{c} {_f(v)}' for c, v in led['channel_contrib'].items())]
    if ref:
        L += ['', f'## Default-off invariant: every value shared with {ref}/<seed>/metrics.json', '']
        for s, r in runs.items():
            mine = dict(_leaves(r))
            shared = [(p, v) for p, v in _leaves(json.load(open(os.path.join(ref, s, 'metrics.json')))) if p in mine]
            diff = ['/'.join(map(str, p)) for p, v in shared if mine[p] != v]
            main_ok = all(mine[p] == v for p, v in shared if p[0] == 'main')
            L.append(f'- {s}: main {"identical" if main_ok else "DIFFERS"}; {len(shared)} shared values, '
                     + ('all identical' if not diff else f'{len(diff)} differ: {diff[:5]}'))
    open(os.path.join(root, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


def coupling_sweep(dirs, out):
    """out/coupling_sweep.md: with_pulse vs main (pulse off) for each assumed pulse coupling; dirs = run roots holding
    seed*/metrics.json, each run with its own --pulse-coupling."""
    L = ['# Pulse coupling sweep (assumed within-person coupling; mean ± SD over seeds)', '',
         'coupling = within-person shift of pulse_htn, night-to-night SD per mmHg of latent SBP. 0 = the pulse channel '
         'carries no BP signal (a pure-noise channel: with_pulse must gain nothing and raise no extra alarms); the middle '
         'value equals the age-adjusted BETWEEN-person slope from PPG-BP (results/ppg_bp, an upper bound for within-person '
         'coupling per the audit); 2x is a stress test beyond it. main = pulse OFF (identical at every coupling). Rows '
         "\"at main's rate\" compare the arms at matched alarm rates (with_pulse read off its operating curve at main's "
         'realised test alarm rate); the other rows put each arm at its own operating point (budget 0.5).', '',
         '| coupling | metric | main (no pulse) | with_pulse | with_pulse - main per seed | mean ± SD | seeds with_pulse > main |',
         '|---|---|---|---|---|---|---|']
    for d in dirs:
        R = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(d, 'seed*', 'metrics.json')))]
        c = f"| {R[0]['pulse_coupling']:g} "
        arms = lambda k: [(r['main'][k], r['ablations']['with_pulse'][k]) for r in R]
        L += [c + _row(k, arms(k)) for k in ('auroc', 'auprc', 'sens_lead_0', 'sens_lead_30', 'sens_lead_90')]
        L += [c + _row(f"{k} at main's rate, budget 0.5", [_matched(r, '0.5', k) for r in R])
              for k in ('sens_lead_0', 'sens_lead_30', 'sens_lead_90')]
        L += [c + _row(f"{k} at main's rate, mean over budgets",
                       [tuple(np.mean([_matched(r, b, k) for b in r['operating_curve']['full']], 0)) for r in R])
              for k in ('sens_lead_30', 'sens_lead_90')]
        L += [c + _row(k, arms(k)) for k in ('alarms_per_nonconv_py', 'prompts_per_nonconv_py_r26', 'false_prompt_12mo',
                                             'specificity', 'sens_spec92')]
    open(os.path.join(out, 'coupling_sweep.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


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
    ap.add_argument('--lifesnaps', help='LifeSnaps daily_fitbit_sema_df_unprocessed.csv: real-world transfer test')
    ap.add_argument('--summary', help='directory with seed*/metrics.json: write its summary.md and exit')
    ap.add_argument('--ref', help='with --summary: earlier runs whose shared values must be identical')
    ap.add_argument('--sweep', nargs='+', help='run roots (one per pulse coupling): write --out/coupling_sweep.md and exit')
    ap.add_argument('--pulse-coupling', type=float, default=data.PULSE_COUPLING,
                    help='synthetic: assumed within-person pulse coupling, night SD per mmHg (0 = no BP signal)')
    ap.add_argument('--noise-csv', help='synthetic: LifeSnaps daily csv whose real residual blocks replace the AR(1) '
                                        'noise (noise transplant, sentinel/realnoise.py)')
    a = ap.parse_args()
    if a.summary:
        return summarise(a.summary, a.ref)
    if a.sweep:
        return coupling_sweep(a.sweep, a.out)
    if not a.synthetic and not (a.daily and a.people) and not a.lifesnaps:
        ap.error('give --synthetic, both --daily and --people, --lifesnaps, --summary or --sweep')
    n, days, n_boot = (150, 360, 5) if a.quick else (a.n, a.days, BASE['n_boot'])
    bank = None
    if a.noise_csv:
        from sentinel.lifesnaps import load_lifesnaps
        from sentinel.realnoise import Bank
        bank = Bank(load_lifesnaps(a.noise_csv)[0])
    daily, people = (data.load_csv(a.daily, a.people) if a.daily else
                     data.make_cohort(n, days, a.seed, pulse_coupling=a.pulse_coupling, noise_bank=bank))
    split = make_split(people, a.seed)
    tp = people[people.pid.isin(split['test'])]
    cfg = {**BASE, 'n_boot': n_boot, 'seed': a.seed}
    if a.lifesnaps:   # the target has no pulse channels: train the transfer model on the channels it has
        daily = daily.drop(columns=PULSE, errors='ignore')
    os.makedirs(a.out, exist_ok=True)

    dec, wk, models, th = pipeline(daily, people, split, cfg)
    if a.lifesnaps:
        from sentinel.lifesnaps import load_lifesnaps
        nc = tp[~tp.converter.astype(bool)]
        d_nc = learn.quality_gate(daily[daily.pid.isin(nc.pid)])
        res = {'synthetic_nonconverters': usage(dec[dec.pid.isin(nc.pid)], wk[wk.pid.isin(nc.pid)], d_nc, nc),
               'lifesnaps': real_world(*load_lifesnaps(a.lifesnaps), cfg, (models, th)), 'thresholds': th}
        with open(os.path.join(a.out, 'real_world.json'), 'w') as f:
            json.dump(_clean(res), f, indent=2)
        cols = list(res['lifesnaps'])
        md = ['# Real-world transfer test: LifeSnaps vs synthetic non-converters', '',
              f'Model and thresholds trained on synthetic data (n={n}, days={days}, seed={a.seed}); context and population',
              'prior refitted on LifeSnaps (label-free). LifeSnaps has no BP labels: all participants count as non-converters.', '',
              '| metric | synthetic non-converters | LifeSnaps |', '|---|---|---|']
        md += [f'| {k} | {_f(res["synthetic_nonconverters"][k])} | {_f(res["lifesnaps"][k])} |' for k in cols]
        open(os.path.join(a.out, 'real_world.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
        print('\n'.join(md))
        return
    res = {'main': metrics(dec, tp, cal=models['pred_cal']), 'thresholds': th, 'weights': models['weights'], 'trend_r': models['trend_r'],
           'ablations': {}, 'robustness': {}, 'pulse_coupling': None if a.daily else a.pulse_coupling}
    abl = {name: pipeline(daily, people, split, {**cfg, **over}) for name, over in ABLATIONS.items()}
    decs = {'full': dec, **{k: v[0] for k, v in abl.items()}}
    res['ablations'] = {k: metrics(v[0], tp, cal=v[2]['pred_cal']) for k, v in abl.items()}
    fits = {'full': (dec, models), **{k: (abl[k][0], abl[k][2]) for k in ('level_only', 'cuff_only', 'with_pulse')}}
    res['operating_curve'] = operating_curve(fits, people, split)
    res['chance'] = chance_floor(dec, tp, res['main']['alarms_per_nonconv_py'])   # at the model's realised alarm rate
    for name, pt in ROBUSTNESS.items():
        res['robustness'][name] = metrics(pipeline(daily, people, split, cfg, (models, th), pt)[0], tp, cal=models['pred_cal'])
    wp = abl['with_pulse']                         # RQ5: the with_pulse model when the pulse channels vanish at test time
    res['robustness']['with_pulse_drop_pulse'] = metrics(pipeline(daily, people, split, {**cfg, 'pulse': True}, wp[2:],
                                                                  ('drop_channel', 1.0, {'channel': PULSE}))[0], tp, cal=wp[2]['pred_cal'])
    res['weights_with_pulse'] = wp[2]['weights']
    res['fairness'] = by_group(dec, tp, 'skin_ita', 3, models['pred_cal']).to_dict('index')
    res['by_age'] = by_group(dec, tp, 'age', 3, models['pred_cal']).to_dict('index')
    res['ledger'] = example_ledger(dec, wk, tp)
    res['ledger_with_pulse'] = example_ledger(wp[0], wp[1], tp)

    with open(os.path.join(a.out, 'metrics.json'), 'w') as f:
        json.dump(_clean(res), f, indent=2)
    write_report(os.path.join(a.out, 'report.md'), res, f'n={n}, days={days}, seed={a.seed}, n_boot={n_boot}')
    figures(a.out, dec, decs, tp, res['operating_curve'])

    m = res['main']
    print(f'SENTINEL-HTN ({n} people, {days} days; test {m["n_people"]} people, {m["n_converters"]} converters)')
    print(f'  AUROC {_f(m["auroc"])}  AUPRC {_f(m["auprc"])}  Brier {_f(m["brier"])}  ECE {_f(m["ece"])}')
    print(f'  sens@lead 30/90/180d {_f(m["sens_lead_30"])}/{_f(m["sens_lead_90"])}/{_f(m["sens_lead_180"])}  '
          f'median lead {_f(m["median_lead"])} d')
    print(f'  alarms/non-converter-yr {_f(m["alarms_per_nonconv_py"])}  warning precision {_f(m["warning_precision"])}  '
          f'AURC {_f(m["aurc"])}  abstention {_f(m["abstention_rate"])}')
    print('  Se@90 by warning budget ' + '  '.join(f'{k}: ' + '/'.join(_f(v['sens_lead_90']) for v in c.values())
                                               for k, c in res['operating_curve'].items()) + f'  (budgets {BUDGETS})')
    print(f'  wrote {a.out}/metrics.json, report.md, calibration.png, lead_time.png, risk_coverage.png, lead_vs_budget.png')


if __name__ == '__main__':
    main()

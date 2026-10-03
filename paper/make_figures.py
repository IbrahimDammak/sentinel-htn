"""Regenerate the paper figures from the pipeline (3 seeds, n=1200 x 540 d) and results/seed*/metrics.json.
Run from the repo root: python paper/make_figures.py   (~1 min)
"""
import json
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import run  # noqa: E402
from sentinel import data, warn  # noqa: E402

OUT = os.path.join(ROOT, 'paper', 'figures')
SEEDS = (0, 1, 2)
plt.rcParams.update({'font.size': 7.5, 'font.family': 'serif', 'axes.linewidth': 0.6,
                     'axes.spines.top': False, 'axes.spines.right': False})


def architecture():
    """Fig. 1 — Learn -> Detect -> Predict -> Warn pipeline with optional frozen foundation-model encoders (full width)."""
    fig, ax = plt.subplots(figsize=(7.16, 2.45))
    ax.set(xlim=(0, 100), ylim=(0, 32)); ax.axis('off')
    Y = 11.5  # main row sits above the encoder row
    boxes = [  # x, title, subtitle, lines, face
        (0.5, 'Inputs', '', 'wrist PPG + IMU\nsleep, steps,\ncontext, sparse\nhome cuff', '#eeeeee'),
        (15.5, 'Quality gate', '(RQ5)', 'SQI threshold\nrhythm gate\nacute-context\nmasks', '#eeeeee'),
        (30.5, '1 Learn', '(RQ1, RQ4)', 'context\nregression,\nhierarchical\npersonal baseline', '#dcd8f5'),
        (45.5, '2 Detect', '(RQ2)', 'weekly joint\ndeviation, Kalman\ntrend, CUSUM,\n"watch" tier', '#dcd8f5'),
        (60.5, '3 Predict', '(RQ3)', 'landmark hazard\n(level + change),\nbootstrap band,\nPlatt calibration', '#dcd8f5'),
        (75.5, '4 Warn', '(RQ6)', 'three states,\nalarm budget,\nevidence\nledger', '#dcd8f5'),
    ]
    for x, t, sub, body, fc in boxes:
        ax.add_patch(FancyBboxPatch((x, 3.5 + Y), 13.5, 16, boxstyle='round,pad=0.3,rounding_size=0.8', fc=fc, ec='#555', lw=0.6))
        ax.text(x + 6.75, 17.6 + Y, t, ha='center', va='center', weight='bold', fontsize=6.4)
        ax.text(x + 6.75, 15.4 + Y, sub, ha='center', va='center', fontsize=5.4, color='#444')
        ax.text(x + 6.75, 9.0 + Y, body, ha='center', va='center', fontsize=5.4, linespacing=1.2)
    for x in (14.2, 29.2, 44.2, 59.2, 74.2):
        ax.annotate('', (x + 1.1, 12 + Y), (x - 0.2, 12 + Y), arrowprops=dict(arrowstyle='->', lw=0.7))
    for i, (s, c) in enumerate([('WARNING', '#c7e9dc'), ('INSUFFICIENT', '#f2f2f2'), ('POOR_QUALITY', '#f2f2f2')]):
        y = 16 - 5.2 * i + Y
        ax.add_patch(FancyBboxPatch((90.9, y - 1.7), 8.9, 3.4, boxstyle='round,pad=0.2,rounding_size=0.5', fc=c, ec='#555', lw=0.5))
        ax.text(95.35, y, s, ha='center', va='center', fontsize=4.9)
        ax.annotate('', (91.0, y), (89.5, 12 + Y), arrowprops=dict(arrowstyle='->', lw=0.5))
    ax.text(95.35, 1.8 + Y, 'warning -> 7-day\nhome-cuff series', ha='center', va='center', fontsize=5.4, style='italic')
    # optional frozen encoders (dashed): their outputs enter Learn as extra channels
    for x, t, body in [(0.5, 'PaPaGei-S (frozen)', 'PPG clip -> 512-d -> hypertension\nhead logit = nightly pulse channel'),
                       (30.5, 'WBM (frozen)', 'hourly week 168 x 38 -> 256-d\nembedding = behaviour channel')]:
        ax.add_patch(FancyBboxPatch((x, 0.6), 27.5, 8.4, boxstyle='round,pad=0.3,rounding_size=0.8', fc='#fbeee8',
                                    ec='#555', lw=0.6, ls='--'))
        ax.text(x + 13.75, 7.0, t, ha='center', va='center', weight='bold', fontsize=6.0)
        ax.text(x + 13.75, 3.4, body, ha='center', va='center', fontsize=5.2, linespacing=1.2)
    ax.annotate('', (33.5, 3.0 + Y), (28.4, 6.5), arrowprops=dict(arrowstyle='->', lw=0.6, ls='--'))
    ax.annotate('', (37.25, 3.0 + Y), (37.25, 9.4), arrowprops=dict(arrowstyle='->', lw=0.6, ls='--'))
    ax.text(61.0, 4.8, 'optional, frozen, never trained here;\nreal-label probes in Results', ha='left', va='center',
            fontsize=5.4, style='italic', color='#444')
    fig.savefig(os.path.join(OUT, 'fig_architecture.pdf'), bbox_inches='tight')


def outcomes():
    """Fig. 2 — pooled reliability diagram and lead-time distribution (main model, 3 seeds)."""
    ys, ps, leads, n_conv = [], [], [], 0
    for s in SEEDS:
        daily, people = data.make_cohort(1200, 540, seed=s)
        split = run.make_split(people, s)
        dec = run.pipeline(daily, people, split, {**run.BASE, 'seed': s})[0]
        ys.append(dec.y.to_numpy()); ps.append(dec.p.to_numpy())
        tp = people[people.pid.isin(split['test']) & people.converter]
        n_conv += len(tp)
        fw = warn.first_warnings(dec).set_index('pid').first_warning_day
        lead = tp.set_index('pid').t_ref - fw.reindex(tp.pid).to_numpy()
        leads += list(lead[lead > 0])
    y, p = np.concatenate(ys), np.concatenate(ps)
    q = np.quantile(p, np.linspace(0, 1, 11))
    b = np.clip(np.searchsorted(q, p, side='right') - 1, 0, 9)
    px = [p[b == k].mean() for k in range(10)]; py = [y[b == k].mean() for k in range(10)]
    fig, (a, c) = plt.subplots(1, 2, figsize=(3.5, 1.6))
    lim = max(max(px), max(py)) * 1.1
    a.plot([0, lim], [0, lim], ls='--', lw=0.6, c='#888'); a.plot(px, py, 'o-', ms=2.5, lw=0.8, c='#534AB7')
    a.set(xlabel='predicted risk (26 wk)', ylabel='observed rate', xlim=(0, lim), ylim=(0, lim))
    a.set_title('(a) calibration, decile bins', fontsize=7)
    c.hist(leads, bins=np.arange(0, 400, 30), color='#1D9E75', ec='white', lw=0.4)
    c.set(xlabel='lead time before $t_{ref}$ (days)', ylabel='converters')
    c.set_title(f'(b) {len(leads)}/{n_conv} warned before $t_{{ref}}$', fontsize=7)
    fig.tight_layout(pad=0.3)
    fig.savefig(os.path.join(OUT, 'fig_outcomes.pdf'), bbox_inches='tight')


def robustness():
    """Fig. 3 — abstention vs alarm burden under degradation, and by skin-tone tercile (mean ± SD, 3 seeds)."""
    ms = [json.load(open(os.path.join(ROOT, 'results', 'weighted', f'seed{s}', 'metrics.json'))) for s in SEEDS]
    runs = ['clean'] + list(ms[0]['robustness'])
    get = lambda m, r: m['main'] if r == 'clean' else m['robustness'][r]
    lab = {'clean': 'clean', 'mcar_0.3': 'MCAR 30%', 'mcar_0.6': 'MCAR 60%', 'noise_1.0': 'noise 1 SD',
           'drop_night_rmssd': 'no RMSSD', 'mnar_0.4': 'MNAR 40%', 'sensor_fail_0.3': 'sensor fail 30%'}
    fig, (a, c) = plt.subplots(1, 2, figsize=(3.5, 1.75), gridspec_kw={'width_ratios': [1.5, 1]})
    yy = np.arange(len(runs))[::-1]
    for key, col, off in (('abstention_rate', '#888780', 0.18), ('alarms_per_nonconv_py', '#D85A30', -0.18)):
        v = np.array([[get(m, r)[key] for m in ms] for r in runs])
        a.barh(yy + off, v.mean(1), 0.34, xerr=v.std(1), color=col, error_kw={'lw': 0.5, 'capsize': 1},
               label={'abstention_rate': 'abstention rate', 'alarms_per_nonconv_py': 'alarms / non-conv. p-y'}[key])
    a.set_yticks(yy, [lab.get(r, r) for r in runs])
    a.set_title('(a) degraded test data', fontsize=7)
    t = [list(m['fairness'].values()) for m in ms]
    for key, col, off in (('sens_lead_30', '#534AB7', -0.18), ('abstention_rate', '#888780', 0.18)):
        v = np.array([[t[s][k][key] for s in range(len(ms))] for k in range(3)])
        c.bar(np.arange(3) + off, v.mean(1), 0.34, yerr=v.std(1), color=col, error_kw={'lw': 0.5, 'capsize': 1},
              label='Se, lead ≥ 30 d' if key == 'sens_lead_30' else None)
    c.set_xticks(range(3), ['T1\n(darkest)', 'T2', 'T3\n(lightest)'], fontsize=6)
    c.set_ylim(0, 0.7); c.set_title('(b) skin-tone (ITA) tercile', fontsize=7)
    fig.tight_layout(pad=0.3, rect=(0, 0.1, 1, 1))
    fig.legend(*[sum(x, []) for x in zip(a.get_legend_handles_labels(), c.get_legend_handles_labels())],
               loc='lower center', ncol=3, frameon=False, fontsize=5.8, bbox_to_anchor=(0.5, -0.02))
    fig.savefig(os.path.join(OUT, 'fig_robustness.pdf'), bbox_inches='tight')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    architecture(); robustness(); outcomes()
    print('figures written to', OUT)

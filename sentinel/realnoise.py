"""REALNOISE: put real LifeSnaps noise into the evaluation, two ways (RQ5; replaces the AR(1) noise assumption).

1. Noise transplant: the simulator's AR(1) day-to-day noise is replaced by moving blocks of REAL within-person residuals
   (LifeSnaps, standardised per person-channel, rescaled to the calibrated SD). Variance is unchanged by design; what
   becomes real is the noise SHAPE: autocorrelation inside a block, heavy tails and cross-channel correlation (all six
   channels are drawn jointly from the same person-days; a channel missing anywhere in that block falls back to its own
   complete block). Used by make_cohort(noise_bank=...) and `run.py --noise-csv`.
2. Plasmode injection: real LifeSnaps series (real noise AND real missingness) get a simulated BP drift added at a
   known onset; each person is scored twice, injected and untouched, so every person is their own control. Detect-level
   only (LifeSnaps has no cuff readings, so no t_ref): detected = the persistence ("watch") tier fires after onset.
   The same injection on simulated people (AR(1) or transplanted noise, cut to LifeSnaps follow-up lengths) shows how
   optimistic the simulator is.

  .venv/Scripts/python.exe -m sentinel.realnoise LIFESNAPS_DAILY_CSV   # self-check, then plasmode -> results/plasmode/
"""
import json
import os
import sys

import numpy as np
import pandas as pd

from . import CHANNELS

BLOCK = 14          # days per transplanted block: keeps within-fortnight autocorrelation; longer memory is cut
MIN_OBS = 14        # a person-channel enters the bank only with >= 14 observed days
DRIFT = (12, 22)    # mmHg of latent dSBP, as the simulator's converters
RAMP = 28           # days to full drift: compressed (simulator 120-200) because LifeSnaps follows people ~4 months
AFTER_READY = 14    # onset = 14 days after the personal baseline is ready
MIN_AFTER = 42      # need >= 6 weeks after onset (one persistence window)
REPS = 20           # random drift sizes per person


def residual_bank(daily):
    """Per person: (days x 6) array of standardised within-person residuals (NaN where missing or too sparse)."""
    bank = []
    for _, g in daily.sort_values('day').groupby('pid'):
        g = g.set_index('day').reindex(np.arange(g.day.max() + 1))
        x = g[CHANNELS].to_numpy(float)
        n = np.isfinite(x).sum(0)
        z = (x - np.nanmean(x, 0)) / np.nanstd(x, 0)
        z[:, n < MIN_OBS] = np.nan
        if np.isfinite(z).any() and len(z) >= BLOCK:
            bank.append(z)
    return bank


def _pools(bank):
    """Per channel: start indices (person, day) of complete BLOCK-day windows; joint windows with >= 1 channel."""
    pools = {c: [] for c in range(len(CHANNELS))}
    joint = []
    for i, z in enumerate(bank):
        ok = np.isfinite(z)
        cs = np.vstack([np.zeros((1, ok.shape[1]), int), np.cumsum(ok, 0)])
        full = (cs[BLOCK:] - cs[:-BLOCK]) == BLOCK                     # (n windows, channels)
        for c in range(ok.shape[1]):
            pools[c] += [(i, s) for s in np.flatnonzero(full[:, c])]
        joint += [(i, s) for s in np.flatnonzero(full.any(1))]
    return pools, joint


class Bank:
    def __init__(self, daily):
        self.z = residual_bank(daily)
        self.pools, self.joint = _pools(self.z)
        assert all(self.pools.values()), 'a channel has no complete window'

    def draw(self, rng, days):
        """(days x 6) standardised noise from consecutive BLOCK-day windows."""
        out = np.empty((days + BLOCK, len(CHANNELS)))
        for s in range(0, days, BLOCK):
            i, t = self.joint[rng.integers(len(self.joint))]
            blk = self.z[i][t:t + BLOCK].copy()
            gap = ~np.isfinite(blk).all(0)
            for _ in range(50):                                     # refill the missing channels jointly if possible
                if not gap.any():
                    break
                j, u = self.joint[rng.integers(len(self.joint))]
                alt = self.z[j][u:u + BLOCK]
                if np.isfinite(alt[:, gap]).all():
                    blk[:, gap] = alt[:, gap]
                    gap[:] = False
            for c in np.flatnonzero(gap):                           # else each channel from its own complete window
                j, u = self.pools[c][rng.integers(len(self.pools[c]))]
                blk[:, c] = self.z[j][u:u + BLOCK, c]
            out[s:s + BLOCK] = blk
        return out[:days]


# ---------------------------------------------------------------- plasmode
def inject(daily, onset, size):
    """Add size[pid] mmHg of ramped latent drift from onset[pid] to every observed value (simulator couplings)."""
    from .data import _CH
    d = daily.copy()
    on, sz = d.pid.map(onset).to_numpy(float), d.pid.map(size).to_numpy(float)
    ramp = np.nan_to_num(np.clip((d.day.to_numpy() - on) / RAMP, 0, 1) * sz)
    for c in CHANNELS:
        d[c] = d[c] + _CH[c][4] * ramp
    d['steps'] = d['steps'].clip(lower=0)
    d['night_rmssd'] = d['night_rmssd'].clip(lower=5)
    return d


def _watch(daily, cfg, thr):
    """Label-free refit on this cohort (as run.real_world), then the persistence tier at the synthetic threshold.
    -> (weekly table, per-person first ready day)."""
    import run
    from . import learn
    d = learn.quality_gate(daily)
    d = run._adjust(d, learn.fit_context(d))
    prior = learn.fit_prior(d)
    pb = learn.personal_baseline(d, prior)
    ready = pb[pb.baseline_ready].groupby('pid').day.min()
    return run._weeks(d, prior, cfg, thr, run._weights(d, prior, cfg)), ready


def _rates(wk0, wk1, onset, end):
    """Detected = persist in a week starting >= onset; false = the same on the untouched copy. Lag in days."""
    out = {}
    for name, wk in (('false', wk0), ('detected', wk1)):
        w = wk[wk.pid.isin(onset.index)]
        hit = w[w.persist & (w.week * 7 >= w.pid.map(onset))]
        out[name] = float(hit.pid.nunique() / len(onset))
        if name == 'detected':
            first = hit.groupby('pid').week.min() * 7 + 6 - onset.reindex(hit.pid.unique())
            out['median_lag_days'] = float(first.median()) if len(first) else np.nan
    # monitored post-onset weeks per person, for scale
    out['post_onset_weeks'] = float(((end - onset) / 7).median())
    return out


def plasmode(daily, cfg, thr, seed=0):
    """Inject drifts into `daily` (no BP, all untouched) REPS times; mean rates over reps."""
    rng = np.random.default_rng(seed)
    wk0, ready = _watch(daily, cfg, thr)
    end = daily.groupby('pid').day.max()
    onset = ready + AFTER_READY
    onset = onset[end.reindex(onset.index) - onset >= MIN_AFTER]
    reps = []
    for _ in range(REPS):
        size = pd.Series(rng.uniform(*DRIFT, len(onset)), onset.index)
        wk1, _ = _watch(inject(daily, onset, size), cfg, thr)
        reps.append(_rates(wk0, wk1, onset, end.reindex(onset.index)))
    r = pd.DataFrame(reps)
    return {'people': int(len(onset)), **{k: float(r[k].mean()) for k in r}, 'detected_sd_over_reps': float(r.detected.std())}


def cut_to(daily, people, lengths, seed=0):
    """Simulated non-converters cut to real follow-up lengths (drawn from `lengths`)."""
    rng = np.random.default_rng(seed)
    nc = people.loc[~people.converter.astype(bool), 'pid']
    keep = pd.Series(rng.choice(lengths, len(nc)), nc.to_numpy())
    d = daily[daily.pid.isin(nc)]
    return d[d.day <= d.pid.map(keep)]


def main(csv, out=os.path.join('results', 'plasmode'), n=600, seed=0):
    import run
    from . import data
    from .lifesnaps import load_lifesnaps
    real, _ = load_lifesnaps(csv)
    bank = Bank(real)
    # synthetic training -> persistence threshold (as in the paper's main run)
    sd, sp = data.make_cohort(1200, 540, seed)
    cfg = {**run.BASE, 'seed': seed}
    thr = run.pipeline(sd, sp, run.make_split(sp, seed), cfg)[3]['thr']
    lengths = real.groupby('pid').day.max().to_numpy()
    res = {'threshold': thr, 'block_days': BLOCK, 'ramp_days': RAMP, 'drift_mmHg': DRIFT, 'reps': REPS}
    res['real (plasmode)'] = plasmode(real, cfg, thr, seed)
    for name, kw in (('simulated, AR(1) noise', {}), ('simulated, transplanted noise', {'noise_bank': bank})):
        d, p = data.make_cohort(n, 540, seed + 100, converter_rate=0.0, **kw)
        res[name] = plasmode(cut_to(d.drop(columns=['pulse_htn']), p, lengths, seed), cfg, thr, seed)
        print(name, res[name], flush=True)
    print('real', res['real (plasmode)'])
    os.makedirs(out, exist_ok=True)
    json.dump(res, open(os.path.join(out, 'metrics.json'), 'w'), indent=1)
    rows = [k for k in res if isinstance(res[k], dict)]
    md = ['# Plasmode injection: the same drift in real vs simulated noise (Detect level)', '',
          f'Each person is scored twice: untouched, and with a latent SBP drift of U{DRIFT} mmHg ramped over {RAMP} days '
          f'from {AFTER_READY} days after their baseline is ready (simulator couplings, e.g. +0.15 bpm night HR per mmHg; '
          f'{REPS} random drift sizes per person). Detected = the persistence ("watch") tier fires after onset at the '
          f'synthetic-trained threshold {thr:.2f}; false = it fires after the same day without drift. Label-free parts '
          '(context, prior, channel weights) are refitted on each cohort. Simulated people are non-converters cut to '
          'LifeSnaps follow-up lengths. People need >= 6 weeks after onset. The ramp is compressed because LifeSnaps '
          'covers ~4 months: absolute rates are not comparable to the paper\'s 26-week task, only the rows to each other.',
          '', '| noise | people | detected after onset | false (no drift) | median lag (days) | post-onset weeks |',
          '|---|---|---|---|---|---|']
    md += [f"| {k} | {res[k]['people']} | {res[k]['detected']:.2f} ± {res[k]['detected_sd_over_reps']:.2f} | "
           f"{res[k]['false']:.2f} | {res[k]['median_lag_days']:.0f} | {res[k]['post_onset_weeks']:.1f} |" for k in rows]
    md += ['', '± = SD over the random drift sizes (same people), not a confidence interval.']
    open(os.path.join(out, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print('\n'.join(md))


if __name__ == '__main__':
    # self-check: blocks are standardised real values, jointly drawn, and the right length
    rng = np.random.default_rng(0)
    days = 60
    fake = pd.DataFrame({'pid': np.repeat(['a', 'b'], days), 'day': np.tile(np.arange(days), 2),
                         **{c: rng.normal(50, 5, 2 * days) for c in CHANNELS}})
    fake.loc[(fake.pid == 'a') & (fake.day.between(20, 30)), 'night_rhr'] = np.nan
    b = Bank(fake)
    z = b.draw(rng, 100)
    assert z.shape == (100, len(CHANNELS)) and np.isfinite(z).all()
    assert abs(z.std() - 1) < 0.15 and abs(z.mean()) < 0.15
    d = inject(fake, pd.Series({'a': 10.0}), pd.Series({'a': 20.0}))
    a0, a1 = fake[fake.pid == 'a'].set_index('day'), d[d.pid == 'a'].set_index('day')
    assert (a1.night_rhr - a0.night_rhr).loc[50] == 0.15 * 20 and (a1.night_rhr - a0.night_rhr).loc[5] == 0
    assert d[d.pid == 'b'][CHANNELS].equals(fake[fake.pid == 'b'][CHANNELS])
    print('realnoise self-check OK')
    if len(sys.argv) > 1:
        main(sys.argv[1])

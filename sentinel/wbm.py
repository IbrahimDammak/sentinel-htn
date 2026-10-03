"""WBM (optional; needs the WSL GPU env with torch, mamba-ssm, openmhc[hf]): frozen OpenMHC wearable behaviour model on
LifeSnaps hourly Fitbit data -> 256-d weekly embeddings -> linear probe on the labels LifeSnaps has (age, sex, BMI).
No BP labels exist here, so this tests only whether the frozen features carry person-level information on our data.
The core pipeline never imports this module.

  wsl -d UbuntuRestored -- bash -lc "cd /mnt/e/bureau/cardiacAttackDetectionHakathon && /root/sentinel-gpu/bin/python -m sentinel.wbm"
"""
import json
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOURLY = os.path.join(ROOT, 'data', 'lifesnaps', 'rais_anonymized', 'csv_rais_anonymized',
                      'hourly_fitbit_sema_df_unprocessed.csv')
# --no-energy: Fitbit computes calories from the user's typed profile (sex, weight, height), so the energy channel can
# leak sex/BMI directly; this variant flags it missing everywhere and drops it from the baseline.
NO_ENERGY = '--no-energy' in sys.argv
TAG = '_no_energy' if NO_ENERGY else ''
EMB = os.path.join(ROOT, 'data', 'lifesnaps', f'wbm_embeddings{TAG}.npz')    # cache; delete to recompute
OUT = os.path.join(ROOT, 'results', 'wbm_lifesnaps' + TAG)
REPO = 'MyHeartCounts/openmhc-wbm-dp'
MIN_WORN_HOURS = 84            # keep a week only if the watch was worn >= half its hours (HR present)
REPEATS, FOLDS, N_PERM = 20, 5, 200
# Fitbit -> WBM channel index. Everything else (iPhone, sleep, workouts) is flagged missing.
STEPS, DIST, HR, ENERGY = 3, 4, 5, 6
TASKS = {'age_ge30': 'age >= 30 (LifeSnaps band)', 'male': 'sex = male', 'bmi_ge25': 'BMI >= 25'}


def load_stats():
    from huggingface_hub import hf_hub_download
    s = json.load(open(hf_hub_download(REPO, 'normalization_stats.json')))
    return np.asarray(s['means'], np.float32), np.asarray(s['stds'], np.float32)


def build_weeks(means):
    """Person-weeks in WBM format. Units: steps/h, metres/h, HR in beats/s (WBM mean 1.24 = 75 bpm), active energy.
    Fitbit calories include basal burn, so active = calories - the person's 5th-percentile hourly calories, then one
    pooled scale factor matches WBM's channel mean (unit harmonisation; Apple's energy unit is not documented).
    Hours without HR = watch not worn -> all four watch channels flagged missing (Fitbit logs 0 steps when off-wrist)."""
    h = pd.read_csv(HOURLY, index_col=0, low_memory=False)
    h['t'] = pd.to_datetime(h['date']) + pd.to_timedelta(h['hour'], unit='h')
    h['active'] = (h['calories'] - h.groupby('id')['calories'].transform(lambda c: c.quantile(0.05))).clip(lower=0)
    worn = h['bpm'].notna()
    scale = float(means[ENERGY] / h.loc[worn, 'active'].mean())
    weeks, owners, hand = [], [], []
    for pid, g in h.groupby('id'):
        g = g.set_index('t').sort_index()
        g = g[~g.index.duplicated()]
        start = g.index.min().normalize()
        grid = g.reindex(pd.date_range(start, g.index.max().normalize() + pd.Timedelta(hours=23), freq='h'))
        on = grid['bpm'].notna().to_numpy()
        vals = np.zeros((len(grid), 19), np.float32)
        vals[:, STEPS] = grid['steps'].fillna(0).to_numpy()
        vals[:, DIST] = grid['distance'].fillna(0).to_numpy()
        vals[:, HR] = grid['bpm'].fillna(0).to_numpy() / 60
        vals[:, ENERGY] = grid['active'].fillna(0).to_numpy() * scale
        miss = np.ones_like(vals)
        miss[on, STEPS:ENERGY + 1] = 0
        if NO_ENERGY:
            vals[:, ENERGY], miss[:, ENERGY] = 0, 1
        for w in range(len(grid) // 168):
            sl = slice(w * 168, (w + 1) * 168)
            if on[sl].sum() >= MIN_WORN_HOURS:
                weeks.append((vals[sl], miss[sl]))
                owners.append(pid)
        # hand-crafted baseline from the same worn hours
        x = vals[on]
        f = [x[:, STEPS].mean(), x[:, DIST].mean(), x[:, HR].mean() * 60, np.percentile(x[:, HR], 5) * 60,
             x[:, HR].std() * 60] + ([] if NO_ENERGY else [x[:, ENERGY].mean()])
        hand.append((pid, f))
    return weeks, np.array(owners), dict(hand), scale


def embed(weeks, means, stds):
    import torch
    from huggingface_hub import hf_hub_download
    from downstream_evaluation.models.wbm.model import _load_wbm_encoder, _process_example
    enc = _load_wbm_encoder(hf_hub_download(REPO, 'model.ckpt'), 'cuda')
    x = np.stack([_process_example({'values': v, 'mask': m}, means, stds) for v, m in weeks])
    assert x.shape[1:] == (168, 38) and np.isfinite(x).all()
    out = []
    with torch.no_grad():
        for i in range(0, len(x), 64):
            out.append(enc(torch.from_numpy(x[i:i + 64]).cuda())[1].float().cpu().numpy())
    r = np.concatenate(out)
    assert r.shape == (len(weeks), 256) and np.isfinite(r).all()
    return r


def labels(pids):
    h = pd.read_csv(HOURLY, index_col=0, usecols=['Unnamed: 0', 'id', 'age', 'gender', 'bmi'], low_memory=False)
    p = h.groupby('id')[['age', 'gender', 'bmi']].first().reindex(pids)
    bmi = p['bmi'].map(lambda b: np.nan if pd.isna(b) else 1.0 if str(b).startswith('>=') else
                       0.0 if str(b).startswith('<') else float(float(b) >= 25))
    return pd.DataFrame({'age_ge30': p['age'].map({'<30': 0.0, '>=30': 1.0}),
                         'male': p['gender'].map({'FEMALE': 0.0, 'MALE': 1.0}), 'bmi_ge25': bmi}, index=pids)


def cv_auroc(X, y, seeds):
    """Repeated stratified 5-fold over people; standardise + L2 logistic with C picked by inner 3-fold CV."""
    from sklearn.linear_model import LogisticRegressionCV
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    aucs = []
    for s in seeds:
        p = np.zeros(len(y))
        for tr, te in StratifiedKFold(FOLDS, shuffle=True, random_state=s).split(X, y):
            m = make_pipeline(StandardScaler(), LogisticRegressionCV(Cs=np.logspace(-4, 1, 8), cv=3, max_iter=2000))
            p[te] = m.fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
        aucs.append(roc_auc_score(y, p))
    return np.array(aucs)


def main():
    means, stds = load_stats()
    weeks, owners, hand, scale = build_weeks(means)
    if os.path.exists(EMB):
        z = np.load(EMB, allow_pickle=True)
        r, owners = z['r'], z['owners']
    else:
        r = embed(weeks, means, stds)
        np.savez(EMB, r=r, owners=owners)
    pids = sorted(set(owners))
    wbm = np.stack([r[owners == p].mean(0) for p in pids])
    base = np.array([hand[p] for p in pids])
    lab = labels(pids)
    rng = np.random.default_rng(0)
    res = {'people': len(pids), 'weeks': int(len(owners)), 'energy_scale': scale, 'tasks': {}}
    for t, desc in TASKS.items():
        ok = lab[t].notna().to_numpy()
        y = lab[t].to_numpy()[ok].astype(int)
        row = {'label': desc, 'n': int(ok.sum()), 'positives': int(y.sum())}
        for name, X in (('hand6', base[ok]), ('wbm256', wbm[ok])):
            a = cv_auroc(X, y, range(REPEATS))
            null = np.array([cv_auroc(X, rng.permutation(y), [k]).item() for k in range(N_PERM)])
            row[name] = {'auroc': float(a.mean()), 'sd_over_repeats': float(a.std()),
                         'perm_p': float((1 + (null >= a.mean()).sum()) / (1 + N_PERM))}
        res['tasks'][t] = row
        print(t, row, flush=True)
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'metrics.json'), 'w'), indent=1)
    lines = ['# Frozen WBM on LifeSnaps: linear probe', '',
             f"{res['people']} people, {res['weeks']} person-weeks (>= {MIN_WORN_HOURS} worn hours). 4 of 19 WBM (3 with --no-energy) "
             'channels filled (watch steps, distance, HR, active energy); iPhone, sleep and workout channels flagged '
             'missing. No BP labels: this checks only whether frozen WBM features carry person-level information on '
             'Fitbit data. Person = mean of their weekly 256-d embeddings.', '',
             f'Probe: standardise + L2 logistic (C by inner 3-fold CV), {REPEATS}x repeated stratified {FOLDS}-fold '
             f'over people. AUROC = mean over repeats (SD over repeats is not a CI). p = label-permutation test, '
             f'{N_PERM} permutations. Baseline = mean steps, distance, active energy (not with --no-energy), HR, HR 5th pct, HR SD.', '',
             *(['**Variant --no-energy:** energy channel flagged missing (3 of 19 filled); baseline = hand features '
                'without energy (5).', ''] if NO_ENERGY else []),
             '| Label | n (pos) | hand AUROC | p | WBM-256 AUROC | p |', '|---|---|---|---|---|---|']
    for t, row in res['tasks'].items():
        h6, w = row['hand6'], row['wbm256']
        lines.append(f"| {row['label']} | {row['n']} ({row['positives']}) | {h6['auroc']:.2f} ± {h6['sd_over_repeats']:.2f}"
                     f" | {h6['perm_p']:.3f} | {w['auroc']:.2f} ± {w['sd_over_repeats']:.2f} | {w['perm_p']:.3f} |")
    lines += ['', 'Domain shift: WBM was pretrained on Apple Watch + iPhone data with 19 channels; here it sees Fitbit '
              'data with 15 channels missing and harmonised units (energy scaled by one pooled factor, '
              f'{scale:.2f}). Weak results would be expected and are not evidence against WBM.']
    open(os.path.join(OUT, 'summary.md'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()

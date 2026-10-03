"""MATCHED (exploratory; needs sklearn, openpyxl): statistically matched LifeSnaps x PPG-BP cohort.
LifeSnaps has wearables but no BP; PPG-BP has BP but no wearables, and they are different people. Each LifeSnaps person
gets a BP label from a random PPG-BP donor of the same sex and age band with similar BMI (hot-deck, k nearest BMI),
repeated M times (multiple imputation). By construction, wearables and BP are linked ONLY through sex, age band and
BMI, so the honest test is whether wearables add anything beyond those: expected gain ~ 0. A wearable-only AUROC
above 0.5 is the trap this run exposes (it is demographics in disguise), not evidence that wearables predict BP.

  .venv/Scripts/python.exe -m sentinel.matched      # needs data/lifesnaps/wbm_embeddings_no_energy.npz (sentinel.wbm)
"""
import json
import os

import numpy as np
import pandas as pd

from .pulse import ppg_bp_table
from .wbm import ROOT, build_weeks, labels

EMB = os.path.join(ROOT, 'data', 'lifesnaps', 'wbm_embeddings_no_energy.npz')
OUT = os.path.join(ROOT, 'results', 'matched')
M, K, REPEATS, FOLDS = 20, 5, 4, 5
BMI_BAND = {'<19': 18.0, '>=25': 26.5, '>=30': 32.0}     # LifeSnaps reports some BMIs only as bands
LABEL = 'SBP >= 130 or DBP >= 80 mmHg on one PPG-BP cuff reading (ACC/AHA stage 1)'


def lifesnaps_people():
    """Per person: demographics, 5 wearable summaries (no profile-derived energy), mean WBM embedding."""
    _, _, hand, _ = build_weeks(np.ones(19, np.float32))
    z = np.load(EMB, allow_pickle=True)
    pids = sorted(set(z['owners']))
    lab = labels(pids)
    h = pd.read_csv(os.path.join(ROOT, 'data', 'lifesnaps', 'rais_anonymized', 'csv_rais_anonymized',
                                 'hourly_fitbit_sema_df_unprocessed.csv'), usecols=['id', 'bmi'], low_memory=False)
    bmi = h.groupby('id')['bmi'].first().reindex(pids).map(lambda b: BMI_BAND.get(b, b)).astype(float)
    ok = (lab[['age_ge30', 'male']].notna().all(1) & bmi.notna()).to_numpy()
    demo = np.c_[lab['age_ge30'], lab['male'], bmi][ok]
    hand5 = np.array([hand[p][:5] for p in pids])[ok]       # steps, distance, HR, HR 5th pct, HR SD
    wbm = np.stack([z['r'][z['owners'] == p].mean(0) for p in pids])[ok]
    return demo, hand5, wbm


def impute(demo, donors, rng):
    """One hot-deck draw: same sex and age band, one of the K nearest-BMI donors at random."""
    y = np.empty(len(demo))
    for i, (old, male, bmi) in enumerate(demo):
        pool = donors[(donors.sex_m == male) & ((donors.age >= 30) == bool(old))]
        near = pool.iloc[np.argsort(np.abs(pool.bmi.to_numpy() - bmi))[:K]]
        y[i] = near.htn.to_numpy()[rng.integers(len(near))]
    return y.astype(int)


def cv_auroc(X, y, seed):
    from sklearn.linear_model import LogisticRegressionCV
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import StratifiedKFold
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    out = []
    for r in range(REPEATS):
        p = np.zeros(len(y))
        for tr, te in StratifiedKFold(FOLDS, shuffle=True, random_state=seed * 100 + r).split(X, y):
            m = make_pipeline(StandardScaler(), LogisticRegressionCV(Cs=np.logspace(-4, 1, 8), cv=3, max_iter=2000))
            p[te] = m.fit(X[tr], y[tr]).predict_proba(X[te])[:, 1]
        out.append(roc_auc_score(y, p))
    return float(np.mean(out))


def main():
    demo, hand5, wbm = lifesnaps_people()
    t = ppg_bp_table()
    t['htn'] = ((t.sbp >= 130) | (t.dbp >= 80)).astype(int)
    sets = {'demographics (age band, sex, BMI)': demo, 'wearable: hand5': hand5, 'wearable: WBM-256': wbm,
            'demographics + hand5': np.c_[demo, hand5], 'demographics + WBM-256': np.c_[demo, wbm]}
    rng = np.random.default_rng(0)
    runs, prev = {k: [] for k in sets}, []
    for m in range(M):
        y = impute(demo, t, rng)
        prev.append(y.mean())
        for k, X in sets.items():
            runs[k].append(cv_auroc(X, y, m))
        print(m, {k: round(v[-1], 2) for k, v in runs.items()}, flush=True)
    a = {k: np.array(v) for k, v in runs.items()}
    gain = {w: a[f'demographics + {w}'] - a['demographics (age band, sex, BMI)'] for w in ('hand5', 'WBM-256')}
    res = {'people': len(demo), 'imputations': M, 'label': LABEL, 'prevalence': float(np.mean(prev)),
           'auroc': {k: {'mean': float(v.mean()), 'sd_over_imputations': float(v.std())} for k, v in a.items()},
           'gain_over_demographics': {k: {'mean': float(v.mean()), 'sd_over_imputations': float(v.std())}
                                      for k, v in gain.items()}}
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, 'metrics.json'), 'w'), indent=1)
    lines = ['# Statistically matched LifeSnaps x PPG-BP cohort (exploratory, NOT validation)', '',
             f"{res['people']} LifeSnaps people; BP label ({LABEL}) borrowed from a random PPG-BP donor of the same sex "
             f'and age band among the {K} nearest in BMI; {M} imputations (prevalence {res["prevalence"]:.2f}). '
             'Different people: by construction wearables relate to BP only through sex, age band and BMI.', '',
             f'Probe: standardise + L2 logistic (C by inner 3-fold CV), {REPEATS}x {FOLDS}-fold per imputation. '
             'Wearables exclude the profile-derived energy channel (see results/wbm_lifesnaps_no_energy).', '',
             '| Features | AUROC (mean ± SD over imputations) |', '|---|---|']
    lines += [f"| {k} | {v['mean']:.2f} ± {v['sd_over_imputations']:.2f} |" for k, v in res['auroc'].items()]
    lines += ['', '| Added to demographics | AUROC gain |', '|---|---|']
    lines += [f"| {k} | {v['mean']:+.3f} ± {v['sd_over_imputations']:.3f} |"
              for k, v in res['gain_over_demographics'].items()]
    lines += ['', 'Reading: a wearable-only AUROC above 0.5 comes from wearables encoding sex/age/BMI (the matching '
              'variables), not from BP. The only meaningful number is the gain over demographics, which this design '
              'forces toward zero; it cannot show that wearables predict BP. Real paired data (OpenMHC) is required.']
    open(os.path.join(OUT, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()

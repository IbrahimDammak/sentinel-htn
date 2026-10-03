"""PULSE (optional; needs torch, pyPPG, dotmap, openpyxl): frozen PaPaGei-S PPG embeddings -> hypertension head,
tested on real PPG-BP data. The core pipeline never imports this module; torch/sklearn are imported inside functions.

  .venv/Scripts/python.exe -m sentinel.pulse              # self-check, then the PPG-BP experiment -> results/ppg_bp/
  .venv/Scripts/python.exe -m sentinel.pulse --selfcheck  # asserts only
"""
import json
import os
import sys
import time
import warnings

import numpy as np
import pandas as pd
from scipy.signal import resample_poly

from .evaluate import auroc
from .predict import _logit_fit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPAGEI = os.path.join(ROOT, 'external', 'papagei')
PPGBP = os.path.join(ROOT, 'data', 'ppg_bp', 'Data File')
EMB = os.path.join(ROOT, 'data', 'ppg_bp', 'embeddings.npz')    # cache; delete to recompute
OUT = os.path.join(ROOT, 'results', 'ppg_bp')
DEMO = ['age', 'sex_m', 'bmi']
L2_DEMO = 1.0                                 # fixed a priori: 3 features, ~175 training people (weak shrinkage)
L2_GRID = 10.0 ** np.arange(4, -1.01, -0.5)   # embedding-block penalty, chosen by inner CV (descending: warm starts)
REPEATS, FOLDS = 20, 5
N_PERM, PERM_REPEATS = 100, 3                 # stratified permutation test of c - a (as in the audit)
# Labels by their actual definition (PPG-BP classes = JNC7 SBP bands in 219/219; ONE seated upper-arm cuff reading;
# antihypertensive treatment is not recorded, so a treated, controlled hypertensive counts as < 120).
LABELS = {'sbp120': "SBP >= 120 mmHg on a single cuff reading (PPG-BP non-'Normal'; PaPaGei's label)",
          'stage12_vs_normal': 'Stage 1-2 vs Normal (middle band excluded) = SBP >= 140 vs < 120 mmHg; extreme-groups '
                               'design, so AUROC is inflated by spectrum bias (not a screening-population figure)',
          'sbp130_dbp80': 'EXPLORATORY: SBP >= 130 or DBP >= 80 mmHg (ACC/AHA 2025 stage 1 = the t_ref threshold); '
                          'added after the audit, NOT pre-specified'}
DOMAIN = ('PPG-BP: transmissive fingertip PPG at rest (seated, hospital cohort in China), 2.1-s clips; NOT validated on '
          'wrist reflectance PPG at night')

# PaPaGei's hard-coded PPG-BP split (external/papagei/example_papagei.ipynb cell 12); their probe tests on test + val.
PG_TRAIN = [2, 6, 8, 10, 12, 15, 16, 17, 18, 19, 22, 23, 26, 31, 32, 34, 35, 38, 40, 45, 48, 50, 53, 55, 56, 58, 60, 61,
            63, 65, 66, 83, 85, 87, 89, 92, 93, 97, 98, 99, 100, 104, 105, 106, 107, 112, 113, 114, 116, 120, 122, 126,
            128, 131, 134, 135, 137, 138, 139, 140, 141, 146, 148, 149, 152, 153, 154, 158, 160, 162, 164, 165, 167, 169,
            170, 175, 176, 179, 183, 184, 186, 188, 189, 190, 191, 193, 196, 197, 199, 205, 206, 207, 209, 210, 212, 216,
            217, 218, 223, 226, 227, 230, 231, 233, 234, 240, 242, 243, 244, 246, 247, 248, 256, 257, 404, 407, 409, 412,
            414, 415, 416, 417, 419]
PG_TEST = [14, 21, 25, 51, 52, 62, 67, 86, 90, 96, 103, 108, 110, 119, 123, 124, 130, 142, 144, 157, 172, 173, 174, 180,
           182, 185, 192, 195, 200, 201, 211, 214, 219, 221, 228, 239, 250, 403, 405, 406, 410]
PG_VAL = [3, 11, 24, 27, 29, 30, 41, 43, 47, 64, 88, 91, 95, 115, 125, 127, 136, 145, 155, 156, 161, 163, 166, 178, 198,
          203, 208, 213, 215, 222, 229, 232, 235, 237, 241, 245, 252, 254, 259, 411, 418]


# ---------------------------------------------------------------- embedding (authors' recipe)
def load_model():
    """PaPaGei-S: ResNet1DMoE, 512-d output, CPU, eval mode (strict state-dict load, 'module.' prefix stripped)."""
    import torch
    sys.path.insert(0, PAPAGEI)
    from models.resnet import ResNet1DMoE
    m = ResNet1DMoE(in_channels=1, base_filters=32, kernel_size=3, stride=2, groups=1, n_block=18, n_classes=512,
                    n_experts=3)
    sd = torch.load(os.path.join(PAPAGEI, 'weights', 'papagei_s.pt'), map_location='cpu', weights_only=True)
    m.load_state_dict({k.removeprefix('module.'): v for k, v in sd.items()})
    return m.eval()


def prep(x, fs):
    """z-score -> pyPPG Chebyshev band-pass 0.5-12 Hz + 50 ms smoothing -> 125 Hz -> centre zero-pad to 1250 (10 s)."""
    import pyPPG.preproc as PP
    from dotmap import DotMap
    x = (x - x.mean()) / x.std()
    x = PP.Preprocess(fL=0.5, fH=12, order=4, sm_wins={'ppg': 50, 'vpg': 10, 'apg': 10, 'jpg': 10}).get_signals(
        DotMap(v=x, fs=fs, filtering=True))[0]
    x = resample_poly(x, 125, fs)                                    # scipy reduces 125/1000 to 1/8
    pad = 1250 - len(x)
    return np.pad(x, (pad // 2, pad - pad // 2))


def embed(segs, model, batch=64):
    """(n, 1250) preprocessed clips -> (n, 512) embeddings (model output 0)."""
    import torch
    with torch.inference_mode():
        return np.vstack([model(torch.tensor(segs[i:i + batch], dtype=torch.float32)[:, None])[0].numpy()
                          for i in range(0, len(segs), batch)])


def read_clip(sid, c):
    """Raw 1000 Hz finger PPG; files end with a tab, so the last field is dropped (as the authors do)."""
    return pd.read_csv(os.path.join(PPGBP, '0_subject', f'{sid}_{c}.txt'), sep='\t', header=None).to_numpy(float).ravel()[:-1]


def ppg_bp_table():
    """One row per PPG-BP subject: sid, age, sex_m, bmi, sbp, dbp, cls (the dataset's 'Hypertension' class)."""
    df = pd.read_excel(os.path.join(PPGBP, 'PPG-BP dataset.xlsx'), header=1)
    return pd.DataFrame({'sid': df.subject_ID, 'age': df['Age(year)'].astype(float),
                         'sex_m': (df['Sex(M/F)'] == 'Male').astype(float), 'bmi': df['BMI(kg/m^2)'].astype(float),
                         'sbp': df['Systolic Blood Pressure(mmHg)'].astype(float),
                         'dbp': df['Diastolic Blood Pressure(mmHg)'].astype(float), 'cls': df['Hypertension']})


def ppg_bp_embeddings(t):
    """(sid, clip, emb) for the 3 clips of every subject in t; cached in data/ppg_bp/embeddings.npz."""
    if not os.path.exists(EMB):
        sid, clip = np.repeat(t.sid.to_numpy(), 3), np.tile([1, 2, 3], len(t))
        segs = np.vstack([prep(read_clip(s, c), 1000) for s, c in zip(sid, clip)])
        np.savez(EMB, sid=sid, clip=clip, emb=embed(segs, load_model()))
    z = np.load(EMB)
    return z['sid'], z['clip'], z['emb']


def labels(t, kind):
    """See LABELS. sbp120: class != Normal. stage12_vs_normal: Stage 1-2 1, Normal 0, middle band NaN (excluded).
    sbp130_dbp80: from the raw cuff values."""
    if kind == 'sbp120':
        return (t.cls != 'Normal').to_numpy(float)
    if kind == 'sbp130_dbp80':
        return ((t.sbp >= 130) | (t.dbp >= 80)).to_numpy(float)
    return np.where(t.cls == 'Normal', 0.0, np.where(t.cls.str.startswith('Stage'), 1.0, np.nan))


# ---------------------------------------------------------------- probe (numpy/scipy; _logit_fit)
def strat_folds(y, k, seed):
    """Stratified fold id per row (= subject): shuffle within each class, deal round-robin."""
    rng = np.random.default_rng(seed)
    f = np.empty(len(y), int)
    for c in np.unique(y):
        ix = rng.permutation(np.flatnonzero(y == c))
        f[ix] = np.arange(len(ix)) % k
    return f


def fit_head(X, y, nd, l2, w0=None):
    """Standardise on these rows, then L2 logistic: the first nd columns (demographics) get L2_DEMO, the rest l2.
    Returns (mu, sd, w); score = w0 + standardised X @ w."""
    mu, sd = X.mean(0), X.std(0)
    sd = np.where(sd > 0, sd, 1.0)
    pen = np.r_[0.0, np.full(nd, L2_DEMO), np.full(X.shape[1] - nd, l2)]
    return mu, sd, _logit_fit((X - mu) / sd, y, pen, np.zeros(X.shape[1] + 1) if w0 is None else w0)


def score(head, X):
    """Linear predictor (logit) of a head."""
    mu, sd, w = head
    return w[0] + ((X - mu) / sd) @ w[1:]


def tune_l2(X, y, nd, seed):
    """Embedding L2 by inner stratified 5-fold CV on these (training) rows only: mean fold AUROC over L2_GRID."""
    if X.shape[1] == nd:
        return None
    f, auc = strat_folds(y, FOLDS, seed), np.zeros(len(L2_GRID))
    for k in range(FOLDS):
        tr, w = f != k, None
        for j, l2 in enumerate(L2_GRID):                             # strong -> weak penalty, warm-started
            h = fit_head(X[tr], y[tr], nd, l2, w)
            w = h[2]
            auc[j] += auroc(y[~tr], score(h, X[~tr])) / FOLDS
    return float(L2_GRID[np.argmax(auc)])


def cv(X, y, nd, repeats=REPEATS, l2=None):
    """Repeated stratified 5-fold subject-level CV. Per repeat r: folds from seed r, inner-CV seed 1000*r + k
    (l2 given = fixed embedding penalty, no tuning). Returns the (repeats x 5) outer-fold AUROCs and the fitted folds
    [(repeat, test index, head, l2)]; a repeat's AUROC is the mean over its 5 folds."""
    aucs, folds = [], []
    for r in range(repeats):
        f, a = strat_folds(y, FOLDS, r), []
        for k in range(FOLDS):
            tr, te = np.flatnonzero(f != k), np.flatnonzero(f == k)
            lk = tune_l2(X[tr], y[tr], nd, 1000 * r + k) if l2 is None else l2
            h = fit_head(X[tr], y[tr], nd, lk)
            a.append(auroc(y[te], score(h, X[te])))
            folds.append((r, te, h, lk))
        aucs.append(a)
    return np.array(aucs), folds


def nb_corrected(d, n_tr, n_te):
    """Nadeau-Bengio (Mach Learn 2003) corrected resampled t-test on fold-level differences d (repeats x folds):
    variance inflated by n_te/n_tr for the overlap of training sets. Returns (mean, [95% CI], two-sided p)."""
    from scipy import stats
    d = np.ravel(d)
    m, se = d.mean(), np.sqrt((1 / len(d) + n_te / n_tr) * d.var(ddof=1))
    tc = stats.t.ppf(0.975, len(d) - 1)
    return float(m), [float(m - tc * se), float(m + tc * se)], float(2 * stats.t.sf(abs(m / se), len(d) - 1))


def strata(t):
    """Age-decile x sex strata for the permutation test."""
    return pd.qcut(t.age, 10, labels=False, duplicates='drop').to_numpy() * 2 + t.sex_m.to_numpy().astype(int)


def _perm_gain(args):
    """c - a (mean over PERM_REPEATS CV repeats) with the embeddings permuted within age x sex strata by `seed`
    (None = observed). Keeps the embedding-age/sex link, breaks any further link to the label."""
    kind, seed = args
    t = ppg_bp_table()
    Xe = ppg_bp_embeddings(t)[2].reshape(len(t), 3, -1).mean(1)
    if seed is not None:
        rng, s, Xp = np.random.default_rng(seed), strata(t), Xe.copy()
        for g in np.unique(s):
            ix = np.flatnonzero(s == g)
            Xp[ix] = Xe[rng.permutation(ix)]
        Xe = Xp
    y, D = labels(t, kind), t[DEMO].to_numpy()
    keep = ~np.isnan(y)
    return float(cv(np.hstack([D, Xe])[keep], y[keep], 3, PERM_REPEATS)[0].mean() - cv(D[keep], y[keep], 3, PERM_REPEATS)[0].mean())


def perm_test(kind, n_perm=N_PERM):
    """Stratified permutation test of the c - a gain: p = (1 + #null >= observed) / (1 + n_perm). Parallel."""
    from concurrent.futures import ProcessPoolExecutor
    from sentinel.pulse import _perm_gain as f                     # importable name, also under python -m
    with ProcessPoolExecutor(min(6, os.cpu_count() or 1)) as ex:
        obs, *null = ex.map(f, [(kind, None)] + [(kind, s) for s in range(n_perm)])
    null = np.array(null)
    return {'observed': obs, 'null_mean': float(null.mean()), 'null_max': float(null.max()), 'n_perm': n_perm,
            'repeats': PERM_REPEATS, 'p': float((1 + (null >= obs).sum()) / (1 + n_perm))}


def oof_mean(folds, X, n):
    """Repeat-mean out-of-fold logit per row (fold heads differ in scale: descriptive use only)."""
    S = np.zeros(n)
    for _, te, h, _ in folds:
        S[te] += score(h, X[te])
    return S / (folds[-1][0] + 1)


def vcomp(S):
    """One-way random-effects ANOVA on a (subjects x clips) matrix -> (between-person var, within-person var)."""
    w = S.var(axis=1, ddof=1).mean()
    return max(S.mean(axis=1).var(ddof=1) - w / S.shape[1], 0.0), w


def noise(folds, t, sid, E):
    """Per outer fold: clip-level scores of the held-out people from the fold's head -> variance components and the
    cross-sectional slope of the person-mean score per mmHg SBP (raw and age-adjusted). Averaged over the folds of
    each repeat; returns per-repeat arrays. Clips are seconds apart: night-to-night variability is NOT measured."""
    C = E.reshape(len(t), 3, -1)                                     # rows of t, 3 clips each
    assert (sid.reshape(len(t), 3) == t.sid.to_numpy()[:, None]).all()
    rows = []
    for r, te, h, _ in folds:
        S = np.stack([score(h, C[te, c]) for c in range(3)], axis=1)
        b, w = vcomp(S)
        m, sbp, age = S.mean(1), t.sbp.to_numpy()[te], t.age.to_numpy()[te]
        sl = np.polyfit(sbp, m, 1)[0]
        sla = np.linalg.lstsq(np.c_[np.ones(len(te)), sbp, age], m, rcond=None)[0][1]
        rows.append((r, b, w, b / (b + w), sl, sla, sl / np.sqrt(w), sla / np.sqrt(w)))
    g = pd.DataFrame(rows, columns=['r', 'b', 'w', 'icc', 'slope', 'slope_adj', 'slope_wsd', 'slope_adj_wsd'])
    g = g.groupby('r').mean()
    return {'between_sd': np.sqrt(g.b).to_numpy(), 'within_sd': np.sqrt(g.w).to_numpy(), 'icc': g.icc.to_numpy(),
            'slope_per_mmHg': g.slope.to_numpy(), 'slope_per_mmHg_age_adj': g.slope_adj.to_numpy(),
            'slope_per_mmHg_in_within_sd': g.slope_wsd.to_numpy(),
            'slope_per_mmHg_age_adj_in_within_sd': g.slope_adj_wsd.to_numpy()}


# ---------------------------------------------------------------- PaPaGei reproduction (sklearn, this check only)
def reproduce(t, X, n_boot=500, seed=0):
    """PaPaGei's PPG-BP hypertension probe: their split (train -> test + val), patient-level mean embedding,
    StandardScaler + LogisticRegression GridSearchCV(cv=4, accuracy) with their grid; 500-bootstrap 95% CI.
    The same probe on demographics (age, sex, BMI) with the same bootstrap draws gives a paired comparator; the
    embedding AUROC per C is reported as a sensitivity check only (never used for any choice)."""
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV
    from sklearn.preprocessing import StandardScaler
    y = labels(t, 'sbp120')
    tr, te = t.sid.isin(PG_TRAIN).to_numpy(), t.sid.isin(PG_TEST + PG_VAL).to_numpy()
    yt = y[te]
    grid = {'penalty': ['l1', 'l2'], 'C': [0.01, 0.1, 1, 10, 100], 'solver': ['lbfgs'], 'max_iter': [100, 200]}
    rng = np.random.default_rng(seed)
    boot = [rng.integers(0, len(yt), len(yt)) for _ in range(n_boot)]
    out, ps = {'n_train': int(tr.sum()), 'n_test': int(te.sum()), 'n_test_pos': int(yt.sum())}, {}
    with warnings.catch_warnings():                                  # l1+lbfgs fits fail (as in theirs); max_iter=100
        warnings.simplefilter('ignore')
        for name, Z in (('embeddings', X), ('demographics', t[DEMO].to_numpy())):
            sc = StandardScaler().fit(Z[tr])
            gs = GridSearchCV(LogisticRegression(), grid, cv=4, scoring='accuracy', n_jobs=1).fit(sc.transform(Z[tr]), y[tr])
            ps[name] = p = gs.predict_proba(sc.transform(Z[te]))[:, 1]
            out[name] = {'auroc': auroc(yt, p), 'ci95': list(np.percentile([auroc(yt[i], p[i]) for i in boot], [2.5, 97.5])),
                         'best_params': gs.best_params_}
        sc = StandardScaler().fit(X[tr])
        out['embeddings']['auroc_by_C'] = {C: auroc(yt, LogisticRegression(C=C).fit(sc.transform(X[tr]), y[tr]).predict_proba(
            sc.transform(X[te]))[:, 1]) for C in grid['C']}
    d = [auroc(yt[i], ps['embeddings'][i]) - auroc(yt[i], ps['demographics'][i]) for i in boot]
    out['diff_emb_minus_demo'] = {'mean': out['embeddings']['auroc'] - out['demographics']['auroc'],
                                  'ci95': list(np.percentile(d, [2.5, 97.5]))}
    return out


# ---------------------------------------------------------------- experiment
def _q(a):
    """Mean and 2.5/97.5 percentiles over CV repeats of the same people: split-to-split variability, NOT a CI."""
    return {'mean': float(np.mean(a)), 'split_p2.5': float(np.percentile(a, 2.5)),
            'split_p97.5': float(np.percentile(a, 97.5))}


def run_ppg_bp():
    """Reproduction; repeated-CV comparison (demographics / embeddings / both) for the LABELS with a resampling-corrected
    and a stratified-permutation test of the gain; age bands; noise decomposition on fold scales and on the final
    head's scale; final head -> results/ppg_bp/{summary.md, metrics.json, head.npz}."""
    t0 = time.time()
    os.makedirs(OUT, exist_ok=True)
    t = ppg_bp_table()
    sid, _, E = ppg_bp_embeddings(t)
    Xe = E.reshape(len(t), 3, -1).mean(1)                            # patient level = mean of the 3 clip embeddings
    Xd = t[DEMO].to_numpy()
    res = {'note': 'split_p2.5/split_p97.5 = percentiles over CV repeats of the same people (split-to-split '
                   'variability), NOT confidence intervals; use diff_c_minus_a.nb_corrected for uncertainty',
           'labels': LABELS, 'domain': DOMAIN, 'reproduction': reproduce(t, Xe), 'cv': {}, 'n_subjects': len(t)}
    print('reproduction', json.dumps(res['reproduction']), f'{time.time() - t0:.0f}s')
    models = {'a_demographics': (Xd, 3), 'b_embeddings': (Xe, 0), 'c_demo_plus_emb': (np.hstack([Xd, Xe]), 3)}
    oof = {}
    for kind in LABELS:
        y = labels(t, kind)
        keep = ~np.isnan(y)
        n = int(keep.sum())
        out, fa = {'definition': LABELS[kind], 'n': n, 'n_pos': int(y[keep].sum())}, {}
        for name, (X, nd) in models.items():
            fa[name], folds = cv(X[keep], y[keep], nd)
            out[name] = {'auroc_per_repeat': fa[name].mean(1).tolist(), **_q(fa[name].mean(1)),
                         'l2_chosen': pd.Series([f[3] for f in folds]).value_counts().to_dict() if nd < X.shape[1] else None}
            if kind == 'sbp120':                                     # keep is all True here
                oof[name] = oof_mean(folds, X, n)
                if name == 'b_embeddings':
                    res['noise'] = {k: {**_q(v), 'per_repeat': v.tolist()} for k, v in noise(folds, t, sid, E).items()}
            print(kind, name, f"{out[name]['mean']:.3f}", f'{time.time() - t0:.0f}s')
        d = fa['c_demo_plus_emb'] - fa['a_demographics']
        m, ci, p = nb_corrected(d, 0.8 * n, 0.2 * n)
        out['diff_c_minus_a'] = {**_q(d.mean(1)), 'per_repeat': d.mean(1).tolist(),
                                 'nb_corrected': {'mean': m, 'ci95': ci, 'p': p, 'n_train': 0.8 * n, 'n_test': 0.2 * n}}
        if kind != 'sbp130_dbp80':                                   # pre-specified labels only, as in the audit
            out['diff_c_minus_a']['perm_within_age_sex'] = perm_test(kind)
        print(kind, 'c - a', json.dumps(out['diff_c_minus_a']['nb_corrected']),
              json.dumps(out['diff_c_minus_a'].get('perm_within_age_sex')), f'{time.time() - t0:.0f}s')
        res['cv'][kind] = out
    y, age = labels(t, 'sbp120'), t.age.to_numpy()                  # post hoc, descriptive, small samples
    bands = {'<50': age < 50, '50-64': (age >= 50) & (age < 65), '>=65': age >= 65,
             '30-65 (target ages)': (age >= 30) & (age <= 65)}
    res['age_bands_sbp120'] = {k: {'n': int(b.sum()), 'n_pos': int(y[b].sum()), 'age_only': auroc(y[b], age[b]),
                                   **{name: auroc(y[b], s[b]) for name, s in oof.items()}} for k, b in bands.items()}
    # final head: embeddings only, sbp120, all subjects; L2 by 5-fold CV on all subjects
    l2 = tune_l2(Xe, y, 0, 7)
    mu, sd, w = fit_head(Xe, y, 0, l2)
    np.savez(os.path.join(OUT, 'head.npz'), mu=mu, sd=sd, w=w, l2=l2, label=LABELS['sbp120'], domain=DOMAIN,
             score='logit of single-clip PaPaGei-S embeddings; cross-sectional, between-person evidence only')
    res['final_head'] = {'l2': l2, 'n': len(t), 'model': 'b_embeddings', 'label': 'sbp120', 'domain': DOMAIN}
    # noise on the final head's scale (fixed L2, same out-of-fold splits): the scale-free simulator inputs
    nz = noise(cv(Xe, y, 0, l2=l2)[1], t, sid, E)
    res['noise_final_head'] = {k: {**_q(v), 'per_repeat': v.tolist()} for k, v in nz.items()}
    res['simulator_inputs'] = {'icc': float(nz['icc'].mean()),
                               'coupling_sd_per_mmHg': float(nz['slope_per_mmHg_age_adj_in_within_sd'].mean()),
                               'note': 'between-person and clip-to-clip quantities only: the within-person coupling '
                                       'and night-to-night noise used in the simulator are ASSUMPTIONS'}
    res['runtime_s'] = time.time() - t0
    with open(os.path.join(OUT, 'metrics.json'), 'w') as f:
        json.dump(res, f, indent=2)
    write_summary(res)
    print(f'wrote {OUT} in {res["runtime_s"]:.0f}s')
    return res


def write_summary(res):
    rp, nz, nf, si = res['reproduction'], res['noise'], res['noise_final_head'], res['simulator_inputs']
    f3 = lambda q: f"{q['mean']:.3f} [{q['split_p2.5']:.3f}, {q['split_p97.5']:.3f}]"
    ci = lambda q: f"{q['auroc']:.3f} [{q['ci95'][0]:.3f}, {q['ci95'][1]:.3f}]"
    L = ['# PPG-BP: frozen PaPaGei-S embeddings vs demographics for cuff SBP level (real data, cross-sectional)', '',
         'Data: PPG-BP (Liang 2018, CC0): 219 hospital participants in China; ONE seated upper-arm cuff reading and three '
         '2.1-s fingertip PPG clips each. Antihypertensive treatment is NOT recorded (a treated, controlled hypertensive '
         'counts as < 120); the cohort includes 38 people with diabetes, 20 with cerebral infarction and 25 with '
         'cerebrovascular disease, so the embeddings may encode a vascular-disease or vascular-age phenotype that '
         "chronological-age adjustment does not remove. Embeddings: PaPaGei-S (frozen), the authors' preprocessing; "
         'subject = mean of the 3 clip embeddings. This tests whether pulse shape carries information about BP level '
         'BETWEEN people; tracking of BP change WITHIN a person is not tested.', '',
         'Labels (by definition): ' + '; '.join(f'**{k}** = {v}' for k, v in res['labels'].items()) + '.', '',
         "## 1. Reproduction of PaPaGei's benchmark (their split, recipe and sklearn probe)", '',
         f"Train {rp['n_train']}, test = their test + val {rp['n_test']} ({rp['n_test_pos']} positive); label sbp120; "
         'AUROC [500-bootstrap 95% CI].', '',
         '| probe input | AUROC [95% CI] | GridSearchCV choice |', '|---|---|---|',
         f"| PaPaGei-S embeddings | {ci(rp['embeddings'])} | {rp['embeddings']['best_params']} |",
         f"| demographics (age, sex, BMI), same probe | {ci(rp['demographics'])} | {rp['demographics']['best_params']} |",
         '', f"Paired bootstrap difference embeddings - demographics: {rp['diff_emb_minus_demo']['mean']:+.3f} "
         f"[{rp['diff_emb_minus_demo']['ci95'][0]:+.3f}, {rp['diff_emb_minus_demo']['ci95'][1]:+.3f}]. "
         'Sensitivity of the embedding AUROC to C (shown only; never used for a choice): '
         + ', '.join(f'C={c}: {v:.3f}' for c, v in rp['embeddings']['auroc_by_C'].items()) + '. '
         "Consistent with the authors' own Table 15 (PaPaGei, ICLR 2025, Appendix E: demographics 0.77 [0.65-0.88], "
         'PaPaGei-S 0.77 [0.68-0.87], PaPaGei-S + demographics 0.80): age alone reaches the published embedding '
         'figure, and our embedding estimate lies within the published CI.', '',
         f'## 2. Repeated stratified 5-fold subject-level CV ({REPEATS} repeats, seeds 0-{REPEATS - 1})', '',
         "a: demographics, b: embeddings, c: demographics + embeddings. A repeat's AUROC is the mean over its 5 outer "
         'folds; cells show the mean over repeats [2.5-97.5 percentiles over repeats = **split-to-split variability, not a '
         'confidence interval**: the repeats reuse the same people]. Uncertainty of the gain c - a: Nadeau-Bengio '
         'corrected resampled t-test on the fold-level differences (n_test/n_train = 0.25), and a permutation test '
         f'that shuffles the embeddings within age-decile x sex strata ({N_PERM} permutations, {PERM_REPEATS} CV repeats '
         'each). Standardisation on training folds only; no PCA; '
         f'demographics L2 = {L2_DEMO} fixed a priori; embedding-block L2 by inner stratified 5-fold CV on the training '
         'fold only (grid 10^-1..10^4); logistic fit sentinel.predict._logit_fit.', '',
         '| label | n (pos) | a | b | c | c - a (split variability) | c - a: corrected 95% CI, p | stratified permutation p |',
         '|---|---|---|---|---|---|---|---|']
    for kind, o in res['cv'].items():
        g = o['diff_c_minus_a']
        nb, pm = g['nb_corrected'], g.get('perm_within_age_sex')
        L.append(f"| {kind} | {o['n']} ({o['n_pos']}) | {f3(o['a_demographics'])} | {f3(o['b_embeddings'])} | "
                 f"{f3(o['c_demo_plus_emb'])} | {f3(g)} | {nb['mean']:+.3f} [{nb['ci95'][0]:+.3f}, {nb['ci95'][1]:+.3f}], "
                 f"p = {nb['p']:.3f} | " + (f"{pm['p']:.3f} (null mean {pm['null_mean']:+.3f}, max {pm['null_max']:+.3f})"
                                             if pm else 'not run') + ' |')
    L += ['', 'Reading: the permutation test asks whether the embeddings carry information beyond age and sex in THIS '
          'sample; the corrected CI asks how precisely the gain would carry to a new sample. Where the corrected CI '
          'includes 0 the gain is **suggestive**, not established. sbp130_dbp80 is EXPLORATORY (added after the audit, '
          'not pre-specified). stage12_vs_normal excludes the middle band, so its AUROCs are inflated by spectrum bias.', '',
          '## 3. Gain by age band (sbp120; post hoc, descriptive, SMALL SAMPLES)', '',
          'AUROC of the repeat-mean out-of-fold logit within each band (fold heads differ in scale; no CI).', '',
          '| age band | n (pos) | age only | a | b | c |', '|---|---|---|---|---|---|']
    L += [f"| {k} | {v['n']} ({v['n_pos']}) | {v['age_only']:.3f} | {v['a_demographics']:.3f} | {v['b_embeddings']:.3f} | "
          f"{v['c_demo_plus_emb']:.3f} |" for k, v in res['age_bands_sbp120'].items()]
    L += ['', '## 4. Noise decomposition of the clip-level head score', '',
          "Model b, label sbp120; out-of-fold logits of each held-out subject's 3 single clips, computed within each "
          'outer fold and averaged over folds; mean over repeats [split variability]. **What this measures:** '
          'between-person spread and clip-to-clip noise of clips taken seconds apart (each 2.1-s clip is zero-padded to '
          "10 s). **What it does not measure:** night-to-night variability, and how the score moves when one person's "
          'BP changes. The slope is a between-person, cross-sectional slope (it partly reflects structural vascular '
          'ageing); the raw slope contains age and is never used.', '',
          "| quantity | fold-tuned heads (scales differ, L2 31..10^4) | final head's scale (fixed L2) |", '|---|---|---|']
    L += [f'| {k} | {f3(v)} | {f3(nf[k])} |' for k, v in nz.items()]
    L += ['', f"Scale-free simulator inputs (final head's scale): clip-level ICC {si['icc']:.3f}; age-adjusted between-person "
          f"slope {si['coupling_sd_per_mmHg']:.4f} within-clip SD per mmHg. {si['note']}.", '',
          f"Final head (results/ppg_bp/head.npz): model b, label sbp120, all {res['n_subjects']} subjects, "
          f"L2 = {res['final_head']['l2']:g} (5-fold CV on all subjects). Domain: {res['domain']}.", '',
          f"Runtime {res['runtime_s']:.0f} s. Command: `.venv/Scripts/python.exe -m sentinel.pulse` (embeddings cached in "
          'data/ppg_bp/embeddings.npz).', '']
    with open(os.path.join(OUT, 'summary.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L))


# ---------------------------------------------------------------- nightly pulse channels (pipeline columns)
HEAD = os.path.join(OUT, 'head.npz')


def load_head(path=HEAD):
    """(mu, sd, w) of the PPG-BP head (embeddings only, label sbp120: SBP >= 120 on one cuff reading; trained on
    fingertip PPG at rest, NOT validated on wrist PPG at night; see head.npz 'label'/'domain' and run_ppg_bp)."""
    z = np.load(path)
    return z['mu'], z['sd'], z['w']


def night_htn(nights, head):
    """pulse_htn per night: median head logit over the night's clean-clip embeddings. nights = list of (n_i, 512)
    arrays, one per night in order; n_i = 0 -> NaN."""
    return np.array([np.median(score(head, e)) if len(e) else np.nan for e in nights])


def pulse_channels(nights, fs, model, head):
    """One person's daily pulse_htn from raw clean night clips: nights = list (one per night, in order) of lists of
    1-D PPG arrays at fs Hz, each <= 10 s (empty list = no clean clip). Clip selection (SQI) is upstream.
    (An embedding-drift channel was removed after the audit: non-directional, it rises with any change including a
    BP fall; future work needs real longitudinal data.)"""
    E = [embed(np.vstack([prep(x, fs) for x in n]), model) if len(n) else np.empty((0, 512)) for n in nights]
    return night_htn(E, head)


def selfcheck_nightly():
    rng = np.random.default_rng(0)
    head = (np.zeros(512), np.ones(512), np.r_[0.5, np.ones(512)])      # logit = 0.5 + sum of the embedding
    e = rng.normal(size=(5, 512))
    h = night_htn([e, np.empty((0, 512))], head)
    assert np.isclose(h[0], np.median(0.5 + e.sum(1))) and np.isnan(h[1])
    t = ppg_bp_table()                                                # end to end on real clips (one subject a "night")
    ht = pulse_channels([[read_clip(s, 1)] for s in t.sid[:31]] + [[]], 1000, load_model(), load_head())
    assert np.isfinite(ht[:31]).all() and np.isnan(ht[31])
    print('pulse nightly self-check OK')


def selfcheck():
    t = ppg_bp_table()
    yp, ys, ye = labels(t, 'sbp120'), labels(t, 'stage12_vs_normal'), labels(t, 'sbp130_dbp80')
    assert len(t) == 219 and (yp == 0).sum() == 80 and (yp == 1).sum() == 139, np.bincount(yp.astype(int))
    assert (ys == 0).sum() == 80 and (ys == 1).sum() == 54 and np.isnan(ys).sum() == 85 and ye.sum() == 100
    assert (yp == (t.sbp >= 120)).all() and (ys[t.sbp >= 140] == 1).all() and (ys[t.sbp < 120] == 0).all()  # names
    assert np.isnan(ys[(t.sbp >= 120) & (t.sbp < 140)]).all()
    m, ci, p = nb_corrected(np.array([[.1, .2], [.3, .4]]), 4, 1)   # hand: se = sqrt((1/4 + 1/4) * var) = 0.0913
    assert np.allclose([m, *ci, p], [.25, -0.0405163, 0.5405163, 0.0714215], atol=1e-6), (m, ci, p)
    assert len(set(PG_TRAIN + PG_TEST + PG_VAL)) == 205 and t.sid.isin(PG_TRAIN + PG_TEST + PG_VAL).sum() == 205  # 123/41/41, disjoint
    f = strat_folds(yp, FOLDS, 0)                                    # every subject in one fold, classes balanced
    for c in (0, 1):
        n = np.bincount(f[yp == c], minlength=FOLDS)
        assert n.max() - n.min() <= 1 and n.sum() == (yp == c).sum()
    rng = np.random.default_rng(0)                                   # vcomp recovers between var 4, within var 1
    b, w = vcomp(rng.normal(0, 2, (4000, 1)) + rng.normal(0, 1, (4000, 3)))
    assert abs(b - 4) < 0.3 and abs(w - 1) < 0.05, (b, w)
    X = rng.normal(size=(300, 20))                                   # fit_head/score: easy signal on column 0
    y = (rng.random(300) < 1 / (1 + np.exp(-2 * X[:, 0]))).astype(float)
    assert auroc(y, score(fit_head(X, y, 0, 1.0), X)) > 0.8
    e = embed(np.vstack([prep(read_clip(100, c), 1000) for c in (1, 2, 3)]), load_model())
    assert e.shape == (3, 512) and np.isfinite(e).all()
    if os.path.exists(EMB):                                          # cache matches a fresh embedding
        z = np.load(EMB)
        assert np.allclose(e, z['emb'][z['sid'] == 100], atol=1e-4), np.abs(e - z['emb'][z['sid'] == 100]).max()
    print('pulse self-check OK')


if __name__ == '__main__':
    selfcheck()
    selfcheck_nightly()
    if '--selfcheck' not in sys.argv:
        run_ppg_bp()

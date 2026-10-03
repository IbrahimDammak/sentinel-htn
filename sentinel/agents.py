"""AGENTS — optional three-agent audit layer after Warn (main model only; run.py --agents). Not imported by the core.

  Profiler  (Learn + Detect): how one person's recent weeks deviate from their personal baseline. Facts only.
  Predictor (Predict):        the pipeline's risk, copied, and a proposed state.
  Auditor   (Warn gate):      checks the proposal against the evidence and the pipeline's gates; approve or veto.

Purpose: traceability and a conservative second check, NOT better discrimination. The pipeline is the source of
truth: agents call existing functions (warn.ledger, warn.prompts, learn.personal_baseline moments) and copy their
numbers; no maths is added except the usual range m_i +/- 2 sqrt(sigma^2 + v_i). Safety is enforced in code:
  - the only change is WARNING -> INSUFFICIENT; never an upgrade; POOR_QUALITY is never created or removed;
  - a veto downgrades the WHOLE WARNING episode (contiguous WARNING rows from its start), so it can never split an
    episode or add an episode start (check_invariants, run on every audit);
  - no agent text may carry a blood-pressure number or diagnostic wording (no_bp_number). A warning means
    "measure with a home cuff for 7 days".
A backend writes only the narrative parts (claims, rationale); code copies every number, computes every check and
the verdict, and takes the stricter of its own verdict and the backend's. Only the deterministic template backend
exists; llm_backend is a documented stub. Records are plain dicts checked by validate().

Which weeks are audited: rows where warn.prompts(dec) is True. Vetoed prompts no longer start a 26-week refractory
period, so prompts() is recomputed on the audited states and new prompts are audited until none appear.

Self-check: python -m sentinel.agents.  Summary over seeds: python -m sentinel.agents --summary results/agents
"""
import glob
import inspect
import json
import os
import re
import sys

import numpy as np
import pandas as pd

from . import detect, warn
from .predict import FEATURE_SETS

# Pipeline gates, read from the pipeline's own defaults so they cannot drift apart.
MIN_VALID_30 = inspect.signature(warn.decide).parameters['min_valid_30'].default
_P = inspect.signature(detect.persistence).parameters
PERSIST_M, PERSIST_N = _P['m'].default, _P['n'].default
# context_confound: fails if >= CTX_WEEKS of the last PERSIST_N weeks each have >= CTX_DAYS acute-context masked days.
# Fixed before any result was seen; must never be tuned.
CTX_DAYS, CTX_WEEKS = 3, 3
MARGINAL_VALID_30 = 21   # Profiler's descriptive quality verdict only; no check or decision uses it
ACTION = 'Take home-cuff readings for 7 days.'
CHECKS = ('quality_gate', 'risk_gate', 'persistence', 'refs_resolve', 'no_bp_number', 'context_confound')
# A failure of any of these vetoes; a refs_resolve failure alone returns the record once.
VETO_CHECKS = ('quality_gate', 'risk_gate', 'persistence', 'no_bp_number', 'context_confound')
VERDICTS = ('approve', 'return_once', 'veto')   # ordered by strictness
# BP numbers or diagnostic wording in free text. Applies to claims, summary, action and rationale; the Predictor's
# `cuff` field (the person's own past readings, input only) is not free text.
BP_TEXT = re.compile(r'mm\s*hg|\d{2,3}\s*/\s*\d{2,3}|(sbp|dbp|systolic|diastolic|pressure|\bbp)\w*\W{0,4}\d'
                     r'|diagnos|hypertensi', re.I)


def _j(v, kind=float):
    """JSON-safe scalar: NaN / inf / None -> None."""
    if v is None or pd.isna(v) or (kind is float and not np.isfinite(float(v))):
        return None
    return kind(v)


# ---------------------------------------------------------------- validator (hand-written, no dependencies)
NUM, STR, BOOL, INT = 'num', 'str', 'bool', 'int'
CLAIMS = [{'claim': STR, 'ref': STR}]
PROFILE_SPEC = {
    'pid': STR, 'week': INT,
    'quality': {'valid_days_30': NUM, 'n_eval': NUM, 'ctx_masked_6w': NUM, 'ctx_masked_weekly': [INT],
                'verdict': ('adequate', 'marginal')},
    'deviation': {'dev': NUM, 'cusum': NUM, 'weeks_exceeded': [INT], 'dev_slope12': NUM, 'trend_z': NUM,
                  'persist': BOOL},
    'drivers': [{'channel': STR, 'mean_z_6w': NUM, 'toward_risk': BOOL}],
    'usual_range': ({STR: [NUM]},),
    'concerns': CLAIMS, 'summary': STR}
PREDICTOR_SPEC = {
    'pid': STR, 'week': INT, 'p': NUM, 'p_lo': NUM, 'p_hi': NUM, 'thr_p': NUM,
    'cuff': {'sbp_last': NUM, 'dbp_last': NUM, 'days_since': NUM},
    'pipeline_state': ('POOR_QUALITY', 'INSUFFICIENT', 'WARNING'), 'imputed_inputs': [STR],
    'proposed_state': ('POOR_QUALITY', 'INSUFFICIENT', 'WARNING'), 'agrees_with_pipeline': BOOL,
    'reasons': CLAIMS, 'band_drivers': CLAIMS, 'action': STR}
AUDITOR_SPEC = {'pid': STR, 'week': INT, 'checks': [{'name': CHECKS, 'pass': BOOL, 'detail': STR}],
                'verdict': VERDICTS, 'final_state': ('POOR_QUALITY', 'INSUFFICIENT', 'WARNING'), 'rationale': STR}


def validate(rec, spec, path=''):
    """List of schema errors (empty = valid). spec: dict = exact keys; [s] = list of s; tuple of str = enum;
    ({STR: s},) = free-keyed dict; NUM accepts int/float/None; INT, STR, BOOL strict."""
    err = lambda m: [f'{path or "<root>"}: {m}']
    if isinstance(spec, dict):
        if not isinstance(rec, dict):
            return err('not a dict')
        out = err(f'keys {sorted(set(rec) ^ set(spec))} missing or unexpected') if set(rec) != set(spec) else []
        return out + [e for k in spec if k in rec for e in validate(rec[k], spec[k], f'{path}.{k}'.lstrip('.'))]
    if isinstance(spec, list):
        if not isinstance(rec, list):
            return err('not a list')
        return [e for i, v in enumerate(rec) for e in validate(v, spec[0], f'{path}.{i}')]
    if isinstance(spec, tuple) and len(spec) == 1 and isinstance(spec[0], dict):
        if not isinstance(rec, dict):
            return err('not a dict')
        (ks, vs), = spec[0].items()
        return [e for k, v in rec.items() for e in validate(k, ks, path) + validate(v, vs, f'{path}.{k}')]
    if isinstance(spec, tuple):
        return [] if rec in spec else err(f'{rec!r} not in {spec}')
    ok = {NUM: lambda v: v is None or (isinstance(v, (int, float)) and not isinstance(v, bool)),
          INT: lambda v: isinstance(v, int) and not isinstance(v, bool),
          STR: lambda v: isinstance(v, str), BOOL: lambda v: isinstance(v, bool)}[spec]
    return [] if ok(rec) else err(f'{rec!r} is not {spec}')


def resolve(ns, ref):
    """True if the dotted path `ref` (list items by index) names an existing field of ns."""
    o = ns
    for part in ref.split('.'):
        if isinstance(o, dict) and part in o:
            o = o[part]
        elif isinstance(o, list) and part.isdigit() and int(part) < len(o):
            o = o[int(part)]
        else:
            return False
    return True


def _claims(profile, pred):
    return [*profile.get('concerns', []), *pred.get('reasons', []), *pred.get('band_drivers', [])]


def _texts(profile, pred):
    return [c.get('claim', '') for c in _claims(profile, pred)] + [profile.get('summary', ''), pred.get('action', '')]


def bp_hits(texts):
    """Free-text fragments that look like a BP number or diagnostic wording."""
    return [m.group(0) for t in texts if isinstance(t, str) for m in BP_TEXT.finditer(t)]


# ---------------------------------------------------------------- facts (copied from the pipeline, never recomputed)
def profile_facts(dec_p, wk_p, resid_p, prior, week):
    """Profiler facts for one pid-week. dec_p, wk_p, resid_p = that person's rows of dec, wk and the
    personal_baseline(moments=True) output. Every value is copied from an existing pipeline field."""
    r = dec_p[dec_p.week == week].iloc[0]
    led = warn.ledger(dec_p, wk_p, r.pid, week)              # tool: the pipeline's own evidence ledger
    w6 = wk_p[wk_p.week.between(week - PERSIST_N + 1, week)]
    vd, ne = _j(r.valid_days_30, int), _j(r.n_eval, int)
    marginal = vd is None or ne is None or vd < MARGINAL_VALID_30 or ne < PERSIST_N
    rows = resid_p[resid_p.day <= 7 * week + 6]
    last = rows.iloc[-1] if len(rows) else None
    usual = {}
    for ch in led['channel_contrib']:
        if last is not None and ch in prior and ch + '_m' in rows and bool(last.baseline_ready):
            m, sd = float(last[ch + '_m']), float(np.sqrt(prior[ch]['sigma'] ** 2 + last[ch + '_v']))
            usual[ch] = [m - 2 * sd, m + 2 * sd]           # the one allowed exposure; context-adjusted scale
    return {
        'pid': str(r.pid), 'week': int(week),
        'quality': {'valid_days_30': vd, 'n_eval': ne, 'ctx_masked_6w': led['ctx_masked_6w'],
                    'ctx_masked_weekly': [int(c) for c in w6.ctx_masked],
                    'verdict': 'marginal' if marginal else 'adequate'},
        'deviation': {'dev': _j(r.dev), 'cusum': _j(r.cusum), 'weeks_exceeded': [int(r.n_exceed), int(r.n_eval)],
                      'dev_slope12': _j(r.dev_slope12), 'trend_z': _j(r.trend_z),
                      'persist': bool(r.persist) if pd.notna(r.persist) else False},
        'drivers': [{'channel': c, 'mean_z_6w': _j(z), 'toward_risk': bool(z is not None and z > 0)}
                    for c, z in led['channel_contrib'].items()],      # z is already risk-signed (RISK_SIGN)
        'usual_range': usual}


def predictor_facts(dec_p, week, thr_p, cols):
    """Predictor facts: p, p_lo, p_hi, thr_p copied; cuff = the person's own past readings (input only)."""
    r = dec_p[dec_p.week == week].iloc[0]
    return {'pid': str(r.pid), 'week': int(week), 'p': _j(r.p), 'p_lo': _j(r.p_lo), 'p_hi': _j(r.p_hi),
            'thr_p': float(thr_p),
            'cuff': {'sbp_last': _j(r.cuff_sbp_last), 'dbp_last': _j(r.cuff_dbp_last),
                     'days_since': _j(r.cuff_days_since)},
            'pipeline_state': str(r.state), 'imputed_inputs': [c for c in cols if c in r and pd.isna(r[c])]}


# ---------------------------------------------------------------- backends (narrative only)
def _template_profile(f):
    q, dv = f['quality'], f['deviation']
    out = []
    if q['verdict'] == 'marginal':
        out.append((f"Data quality is marginal: {q['valid_days_30']} valid days in the last 30 and {q['n_eval']} of "
                    f"the last {PERSIST_N} weeks evaluable.", 'profile.quality.verdict'))
    out.append((f"The weekly deviation exceeded the personal threshold in {dv['weeks_exceeded'][0]} of "
                f"{dv['weeks_exceeded'][1]} evaluable weeks.", 'profile.deviation.weeks_exceeded'))
    for i, d in enumerate(f['drivers']):
        if d['toward_risk']:
            out.append((f"{d['channel']} averaged {d['mean_z_6w']:+.2f} personal SD from baseline over the last "
                        f"{PERSIST_N} weeks, in the risk direction.", f'profile.drivers.{i}.mean_z_6w'))
    if dv['trend_z'] is not None:
        out.append((f"The Kalman trend of the deviation has z = {dv['trend_z']:.2f}.", 'profile.deviation.trend_z'))
    if q['ctx_masked_6w']:
        out.append((f"Acute context (exercise, alcohol, illness) masked the night channels on {q['ctx_masked_6w']} "
                    f"days in the last {PERSIST_N} weeks.", 'profile.quality.ctx_masked_6w'))
    concerns = [{'claim': c, 'ref': r} for c, r in out]
    return {'concerns': concerns, 'summary': ' '.join(c['claim'] for c in concerns)}


def _template_predict(ns):
    pr, pf = ns['predictor'], ns['profile']
    reasons = []
    if pr['p_lo'] is not None and pr['p_lo'] >= pr['thr_p']:
        reasons.append((f"The calibrated risk lower bound ({pr['p_lo']:.3f}) is at or above the warning threshold "
                        f"({pr['thr_p']:.3f}).", 'predictor.p_lo'))
    if pf['deviation']['persist']:
        n, m = pf['deviation']['weeks_exceeded']
        reasons.append((f"The deviation is persistent: {n} of {m} evaluable weeks above threshold.",
                        'profile.deviation.persist'))
    reasons.append((f"{pf['quality']['valid_days_30']} valid days in the last 30.", 'profile.quality.valid_days_30'))
    if pr['cuff']['days_since'] is not None:
        reasons.append((f"The last home-cuff reading was {pr['cuff']['days_since']:.0f} days before this week.",
                        'predictor.cuff.days_since'))
    band = [(f"Risk band {pr['p_lo']:.3f} to {pr['p_hi']:.3f} (bootstrap 10th-90th percentile).", 'predictor.p_hi')]
    if pr['imputed_inputs']:
        band.append(('Inputs missing this week and imputed with the training median (they carry no person-specific '
                     'information into the band): ' + ', '.join(pr['imputed_inputs']) + '.', 'predictor.imputed_inputs'))
    band.append((f"Evaluable weeks in the window: {pf['quality']['n_eval']} of {PERSIST_N}.", 'profile.quality.n_eval'))
    state = pr['pipeline_state']
    return {'proposed_state': state, 'reasons': [{'claim': c, 'ref': r} for c, r in reasons],
            'band_drivers': [{'claim': c, 'ref': r} for c, r in band],
            'action': ACTION if state == 'WARNING' else 'Keep monitoring.'}


def _template_audit(checks, verdict):
    failed = [c for c in checks if not c['pass']]
    if verdict == 'approve':
        return {'verdict': verdict, 'rationale': f'Approved: all {len(checks)} checks pass.'}
    names = '; '.join(f"{c['name']} ({c['detail']})" for c in failed)
    word = 'Returned once' if verdict == 'return_once' else 'Vetoed; the warning episode is downgraded to INSUFFICIENT'
    return {'verdict': verdict, 'rationale': f'{word}. Failed: {names}.'}


def template_backend():
    """Deterministic, template-based backend: reproducible, no API key."""
    return {'profile': _template_profile, 'predict': _template_predict, 'audit': _template_audit}


def llm_backend(model=None):
    """PLANNED, not implemented. Same three text functions backed by an LLM: each would get only the facts dict
    (profile: profile_facts; predict: {'profile', 'predictor'}; audit: the code-computed checks) and return JSON
    with the same keys as the template functions. Nothing else changes: code still copies every number, validate()
    rejects malformed output (-> veto), refs must resolve, no_bp_number scans the text, the verdict is the stricter
    of the code's and the backend's, and the only state change remains WARNING -> INSUFFICIENT."""
    raise NotImplementedError('only the deterministic template backend is implemented (reproducible, no API key)')


# ---------------------------------------------------------------- agents
def profiler(facts, backend):
    return {**facts, **{k: backend['profile'](facts)[k] for k in ('concerns', 'summary')}}


def predictor(facts, profile, backend):
    out = backend['predict']({'profile': profile, 'predictor': facts})
    rec = {**facts, 'proposed_state': out['proposed_state'], 'reasons': out['reasons'],
           'band_drivers': out['band_drivers'], 'action': out['action']}
    rec['agrees_with_pipeline'] = rec['proposed_state'] == rec['pipeline_state']
    return {k: rec[k] for k in PREDICTOR_SPEC}


def run_checks(profile, pred, thr_p):
    """The six Auditor checks, computed in code. For WARNING rows quality_gate, risk_gate and persistence pass by
    construction (warn.decide guarantees them) and the template backend cannot produce broken refs or BP numbers:
    they are invariant checks. On synthetic data context_confound is the only check that can veto, and the
    simulator's illness/alcohol effects sit only on days quality_gate already masks, so its vetoes there are
    expected to be pure cost."""
    ge = lambda a, b: a is not None and b is not None and a >= b
    q, dv = profile.get('quality', {}), profile.get('deviation', {})
    schema = validate(profile, PROFILE_SPEC) + validate(pred, PREDICTOR_SPEC)
    ns = {'profile': profile, 'predictor': pred}
    refs = [c.get('ref') for c in _claims(profile, pred) if isinstance(c, dict)]
    bad = [r for r in refs if not isinstance(r, str) or not resolve(ns, r)]
    hits = bp_hits(_texts(profile, pred))
    ctxw = q.get('ctx_masked_weekly', [])
    n_ctx = sum(c >= CTX_DAYS for c in ctxw)
    nx, nev = (dv.get('weeks_exceeded') or [None, None])[:2]
    rows = [
        ('quality_gate', ge(q.get('valid_days_30'), MIN_VALID_30), f"valid_days_30 {q.get('valid_days_30')} >= {MIN_VALID_30}"),
        ('risk_gate', ge(pred.get('p_lo'), thr_p), f"p_lo {pred.get('p_lo')} >= thr_p {thr_p}"),
        ('persistence', ge(nx, PERSIST_M), f'{nx} of {nev} evaluable weeks in the last {PERSIST_N} above threshold; need >= {PERSIST_M}'),
        ('refs_resolve', not schema and not bad and len(pred.get('reasons', [])) > 0,
         f'{len(refs) - len(bad)} of {len(refs)} refs resolve, {len(pred.get("reasons", []))} reasons'
         + (f'; unresolved {bad}' if bad else '') + (f'; schema errors {schema[:3]}' if schema else '')),
        ('no_bp_number', not hits, f'BP-like or diagnostic text: {hits}' if hits else 'no BP number or diagnostic wording'),
        ('context_confound', n_ctx < CTX_WEEKS,
         f'{n_ctx} of the last {len(ctxw)} weeks had >= {CTX_DAYS} acute-context masked days (fails at >= {CTX_WEEKS})')]
    return [{'name': n, 'pass': bool(p), 'detail': d} for n, p, d in rows], schema


def auditor(profile, pred, thr_p, backend, returned=False):
    checks, schema = run_checks(profile, pred, thr_p)
    failed = {c['name'] for c in checks if not c['pass']}
    if schema or failed & set(VETO_CHECKS) or (failed and returned):
        verdict = 'veto'
    elif failed:                                              # refs_resolve alone, first time
        verdict = 'return_once'
    else:
        verdict = 'approve'
    out = backend['audit'](checks, verdict)
    if VERDICTS.index(out.get('verdict', 'veto')) > VERDICTS.index(verdict):   # backend may only be stricter
        verdict = out['verdict'] if not (returned and out['verdict'] == 'return_once') else 'veto'
    rationale = out.get('rationale', '')
    if bp_hits([rationale]) or not isinstance(rationale, str):
        verdict, rationale = 'veto', 'Vetoed: the auditor rationale failed the no-BP-number rule.'
    base = pred.get('pipeline_state', 'WARNING')
    down = verdict == 'veto' or pred.get('proposed_state') == 'INSUFFICIENT'
    final = 'INSUFFICIENT' if base == 'WARNING' and down else base   # only WARNING -> INSUFFICIENT
    return {'pid': pred.get('pid'), 'week': pred.get('week'), 'checks': checks, 'verdict': verdict,
            'final_state': final, 'rationale': rationale}


def audit_case(prof_facts, pred_facts, thr_p, backend):
    """Profiler -> Predictor -> Auditor, with at most one return to the Predictor, which must drop every reason whose
    ref failed (enforced here, not left to the backend)."""
    profile = profiler(prof_facts, backend)
    pred = predictor(pred_facts, profile, backend)
    first = auditor(profile, pred, thr_p, backend)
    case = {'profiler': profile, 'predictor': pred, 'auditor': first, 'returned': None}
    if first['verdict'] == 'return_once':
        ns = {'profile': profile, 'predictor': pred}
        keep = lambda cs: [c for c in cs if isinstance(c.get('ref'), str) and resolve(ns, c['ref'])]
        pred2 = {**pred, 'reasons': keep(pred['reasons']), 'band_drivers': keep(pred['band_drivers'])}
        profile2 = {**profile, 'concerns': keep(profile['concerns'])}
        case.update(profiler=profile2, predictor=pred2, auditor=auditor(profile2, pred2, thr_p, backend, returned=True),
                    returned={'predictor': pred, 'profiler': profile, 'auditor': first})
    return case


# ---------------------------------------------------------------- episodes and the audit loop
def _sorted(dec):
    d = dec.sort_values(['pid', 'week'])
    return d.index, d.pid.to_numpy(), d.state.to_numpy().astype(object)


def episode_ids(state, pid):
    """Per row: id (1, 2, ...) of the WARNING episode it belongs to (0 = not WARNING); rows sorted by pid, week."""
    w = state == 'WARNING'
    start = w & ~(np.r_[False, w[:-1]] & np.r_[False, pid[1:] == pid[:-1]])
    return np.where(w, np.cumsum(start), 0)


def apply_vetoes(dec, starts):
    """Downgrade every WARNING episode that starts at one of `starts` [(pid, week)] to INSUFFICIENT, whole."""
    idx, pid, st = _sorted(dec)
    week = dec.loc[idx, 'week'].to_numpy()
    ep = episode_ids(st, pid)
    pos = {(p, w): i for i, (p, w) in enumerate(zip(pid, week))}
    for s in starts:
        i = pos[s]
        assert ep[i] and (i == 0 or ep[i - 1] != ep[i]), f'{s} is not a WARNING episode start'
        st[ep == ep[i]] = 'INSUFFICIENT'
    out = dec.copy()
    out.loc[idx, 'state'] = st
    return out


def check_invariants(before, after):
    """Raises unless after = before with whole WARNING episodes downgraded to INSUFFICIENT and nothing else."""
    assert before.index.equals(after.index)
    b, a = before.state.to_numpy(), after.state.loc[before.index].to_numpy()
    ch = b != a
    assert (b[ch] == 'WARNING').all() and (a[ch] == 'INSUFFICIENT').all(), 'only WARNING -> INSUFFICIENT allowed'
    assert ((b == 'POOR_QUALITY') == (a == 'POOR_QUALITY')).all(), 'POOR_QUALITY created or removed'
    idx, pid, st = _sorted(before)
    pos = before.index.get_indexer(idx)
    ep, chs = episode_ids(st, pid), ch[pos]
    for e in np.unique(ep[ep > 0]):
        assert chs[ep == e].all() or not chs[ep == e].any(), 'a veto split a WARNING episode'
    sa = after.state.loc[idx].to_numpy()
    st_b = (ep > 0) & ~(np.r_[False, ep[:-1]] == ep)
    ea = episode_ids(sa, pid)
    st_a = (ea > 0) & ~(np.r_[False, ea[:-1]] == ea)
    assert not (st_a & ~st_b).any(), 'a veto created an episode start'


def audit_loop(dec, case_fn):
    """Audit every prompt; vetoes downgrade whole episodes; recompute prompts on the audited states and audit any new
    prompt, until none appear. case_fn(cur, pid, week) -> case with case['auditor']['final_state'].
    Returns (audited dec, {(pid, week): case})."""
    cur, cases = dec, {}
    while True:
        pr = warn.prompts(cur)
        new = [k for k in zip(cur.pid[pr], cur.week[pr]) if k not in cases]
        if not new:
            break
        for k in new:
            cases[k] = case_fn(cur, *k)
        cur = apply_vetoes(cur, [k for k in new if cases[k]['auditor']['final_state'] != 'WARNING'])
    check_invariants(dec, cur)
    return cur, cases


def run(dec, wk, resid, prior, thr_p, backend=None, cols=None):
    """The layer on one decision table. resid = learn.personal_baseline(..., moments=True) for the same people.
    Returns (audited dec, cases sorted by pid, week)."""
    backend = template_backend() if backend is None else backend
    cols = FEATURE_SETS['full'] if cols is None else cols
    wk_by, res_by = dict(tuple(wk.groupby('pid'))), dict(tuple(resid.sort_values(['pid', 'day']).groupby('pid')))

    def case_fn(cur, pid, week):
        dp = cur[cur.pid == pid]
        return audit_case(profile_facts(dp, wk_by[pid], res_by.get(pid, resid.iloc[:0]), prior, week),
                          predictor_facts(dp, week, thr_p, cols), thr_p, backend)
    out, cases = audit_loop(dec, case_fn)
    return out, [cases[k] for k in sorted(cases)]


# ---------------------------------------------------------------- metrics, before vs after
COMPARE = ['alarms_per_nonconv_py', 'prompts_per_nonconv_py_r26', 'sens_lead_0', 'sens_lead_30', 'sens_lead_90',
           'sens_post_onset_30', 'median_lead', 'warning_precision', 'specificity']


def compare(dec0, dec1, cases, tp, cal, chance):
    """Before vs after audit on the test people. chance(dec, tp, rate) = run.chance_floor (recomputed at each
    table's own realised alarm rate). No agreement rate: with the template backend it is 100% by construction."""
    from .evaluate import lead_days, metrics
    m0, m1 = metrics(dec0, tp, cal=cal), metrics(dec1, tp, cal=cal)
    side = lambda m, d: {**{k: m[k] for k in COMPARE},
                         **{f'chance_{k}': v for k, v in chance(d, tp, m['alarms_per_nonconv_py']).items()
                            if k in ('sens_lead_30', 'sens_lead_90', 'sens_post_onset_30')}}
    l0, l1 = lead_days(dec0, tp), lead_days(dec1, tp)
    conv = tp[tp.converter.astype(bool)].set_index('pid')
    fw0 = warn.first_warnings(dec0).set_index('pid').first_warning_week
    veto = {(c['auditor']['pid'], c['auditor']['week']) for c in cases if c['auditor']['final_state'] != 'WARNING'}
    lost = [{'pid': p, 'lead_before': _j(l0[p]), 'lead_after': _j(l1[p]),
             'se30_before': bool(l0[p] >= 30), 'se30_after': bool(l1[p] >= 30),
             'se90_before': bool(l0[p] >= 90), 'se90_after': bool(l1[p] >= 90),
             'onset_day': _j(conv.onset.get(p)), 't_ref': _j(conv.t_ref.get(p))}
            for p in l0.index if pd.notna(l0[p]) and not (l1[p] == l0[p])]
    warned = lambda d: set(d.pid[d.state == 'WARNING'])
    nc = set(tp.pid[~tp.converter.astype(bool)])
    g = pd.qcut(tp.skin_ita, 3, duplicates='drop', precision=1)
    terc = dict(zip(tp.pid, g.astype(str)))
    by_skin = {str(t): {'audited': sum(terc.get(c['auditor']['pid']) == str(t) for c in cases),
                        'vetoes': sum(terc.get(p) == str(t) for p, _ in veto)} for t in g.cat.categories}
    first = lambda c: (c['returned'] or c)['auditor']
    failed = {n: sum(not ch['pass'] for c in cases for ch in first(c)['checks'] if ch['name'] == n) for n in CHECKS}
    return {
        'before': side(m0, dec0), 'after': side(m1, dec1),
        'counts': {'prompts_audited': len(cases), 'vetoes': len(veto),
                   'returned_once': sum(c['returned'] is not None for c in cases),
                   'converters_first_warning_vetoed': sum((p, int(fw0[p])) in veto for p in l0.dropna().index),
                   'converters_warned_before': int(l0.notna().sum()), 'converters_warned_after': int(l1.notna().sum()),
                   'converters_losing_all_warnings': sum(pd.isna(l1[p]) for p in l0.dropna().index),
                   'nonconverters_warned_before': len(warned(dec0) & nc), 'nonconverters_warned_after': len(warned(dec1) & nc),
                   'nonconverters_spared': len((warned(dec0) - warned(dec1)) & nc),
                   'converter_vetoes': sum(p in conv.index for p, _ in veto),
                   'nonconverter_vetoes': sum(p in nc for p, _ in veto)},
        'lost_early_detections': lost, 'vetoes_by_skin_ita': by_skin, 'failed_checks': failed}


def report_lines(ag):
    """Markdown section for run.py's report.md (only with --agents)."""
    f = lambda v: 'n/a' if v is None or pd.isna(v) else f'{v:.3f}'
    b, a = ag['before'], ag['after']
    L = ['## Agent audit layer (--agents, template backend, main model only)', '',
         'Profiler -> Predictor -> Auditor on every prompt (warn.prompts), re-run until no new prompt appears. The only '
         'allowed change is WARNING -> INSUFFICIENT for a whole episode. Purpose: traceability and a conservative '
         'second check, NOT better discrimination. For WARNING rows quality_gate, risk_gate and persistence pass by '
         'construction and the template backend cannot produce broken refs or BP numbers (invariant checks); on '
         'synthetic data context_confound (fixed rule: >= 3 of the last 6 weeks with >= 3 acute-context masked days) '
         'is the only check that can veto, and since the simulator puts illness/alcohol effects only on days the '
         'quality gate already masks, its vetoes are expected to be pure cost. The main tables above are pre-audit.', '',
         '| metric | before audit | after audit | after - before |', '|---|---|---|---|']
    L += [f'| {k} | {f(b[k])} | {f(a[k])} | ' + ('n/a' if b[k] is None or a[k] is None or pd.isna(b[k]) or pd.isna(a[k])
                                                 else f'{a[k] - b[k]:+.3f}') + ' |' for k in b]
    L += ['', '| count | value |', '|---|---|'] + [f'| {k} | {v} |' for k, v in ag['counts'].items()]
    L += ['', 'Failed checks (first audit round): ' + ', '.join(f'{k} {v}' for k, v in ag['failed_checks'].items()),
          '', 'Vetoes by skin_ita tercile: ' + ', '.join(f"{k}: {v['vetoes']}/{v['audited']}"
                                                         for k, v in ag['vetoes_by_skin_ita'].items()), '',
          'Converters whose first warning moved or vanished (lead days before -> after):', '']
    L += [f"- {d['pid']}: {f(d['lead_before'])} -> {f(d['lead_after'])} (Se30 {d['se30_before']}->{d['se30_after']}, "
          f"Se90 {d['se90_before']}->{d['se90_after']})" for d in ag['lost_early_detections']] or ['- none']
    return L + ['']


def summarise(root):
    """root/summary.md: before vs after audit, mean ± SD (ddof=1) over root/seed*/metrics.json, raw counts per seed
    and every lost early detection."""
    files = sorted(glob.glob(os.path.join(root, 'seed*', 'metrics.json')))
    runs = {os.path.basename(os.path.dirname(f)): json.load(open(f))['agents'] for f in files}
    R = list(runs.values())
    ms = lambda xs: 'n/a' if any(x is None for x in xs) else (f'{np.mean(xs):.3f} ± {np.std(xs, ddof=1):.3f}'
                                                              if len(xs) > 1 else f'{xs[0]:.3f}')
    L = [f'# Agent audit layer: before vs after audit, {len(R)} seeds ({", ".join(runs)}), mean ± SD over seeds', '',
         'Template backend, main model, held-out test people. The layer can only downgrade whole WARNING episodes to '
         'INSUFFICIENT; it is a traceability layer and a conservative second check, not a better classifier. '
         'chance_* = random warnings at that column\'s own realised alarm rate. Nothing was tuned: thresholds, the '
         'warning budget and the context_confound rule are as fixed before the runs.', '',
         '| metric | before | after | after - before per seed | mean ± SD |', '|---|---|---|---|---|']
    for k in R[0]['before']:
        b, a = [r['before'][k] for r in R], [r['after'][k] for r in R]
        dd = [None if x is None or y is None else y - x for x, y in zip(b, a)]
        L.append(f'| {k} | {ms(b)} | {ms(a)} | ' + ' '.join('n/a' if d is None else f'{d:+.3f}' for d in dd)
                 + f' | {ms(dd)} |')
    L += ['', '## Raw counts per seed', '', '| count | ' + ' | '.join(runs) + ' | total |', '|---' * (len(R) + 2) + '|']
    L += [f'| {k} | ' + ' | '.join(str(r['counts'][k]) for r in R) + f" | {sum(r['counts'][k] for r in R)} |"
          for k in R[0]['counts']]
    L += ['', '## Failed checks (first audit round) per seed', '', '| check | ' + ' | '.join(runs) + ' |',
          '|---' * (len(R) + 1) + '|']
    L += [f'| {k} | ' + ' | '.join(str(r['failed_checks'][k]) for r in R) + ' |' for k in R[0]['failed_checks']]
    L += ['', '## Vetoes / audited prompts by skin_ita tercile (T1 = darkest; edges differ per seed)', '',
          '| seed | T1 | T2 | T3 |', '|---|---|---|---|']
    L += [f'| {s} | ' + ' | '.join(f"{v['vetoes']}/{v['audited']}" for v in r['vetoes_by_skin_ita'].values()) + ' |'
          for s, r in runs.items()]
    L += ['', '## Every converter whose first pre-t_ref warning moved or vanished', '',
          '| seed | pid | lead before (d) | lead after (d) | Se30 before -> after | Se90 before -> after |',
          '|---|---|---|---|---|---|']
    f = lambda v: 'none' if v is None else f'{v:.0f}'
    L += [f"| {s} | {d['pid']} | {f(d['lead_before'])} | {f(d['lead_after'])} | {d['se30_before']} -> "
          f"{d['se30_after']} | {d['se90_before']} -> {d['se90_after']} |" for s, r in runs.items()
          for d in r['lost_early_detections']]
    open(os.path.join(root, 'summary.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--summary':
        summarise(sys.argv[2])
        sys.exit()
    W, I, P = 'WARNING', 'INSUFFICIENT', 'POOR_QUALITY'
    # episodes: a has two (weeks 1-2, 5); b has one cut by POOR_QUALITY
    dec = pd.DataFrame({'pid': list('aaaaaaa') + list('bbbb'), 'week': list(range(7)) + list(range(4)),
                        'state': [I, W, W, I, I, W, I, W, P, W, W]})
    out = apply_vetoes(dec, [('a', 1), ('b', 2)])
    assert out.state.tolist() == [I, I, I, I, I, W, I, W, P, I, I]
    check_invariants(dec, out)
    for bad in (dec.assign(state=dec.state.where(dec.index != 2, I)),     # splits episode a/1
                dec.assign(state=dec.state.where(dec.index != 0, W)),     # upgrade
                dec.assign(state=dec.state.where(dec.index != 8, I))):    # removes POOR_QUALITY
        try:
            check_invariants(dec, bad)
            raise SystemExit('invariant check missed a violation')
        except AssertionError:
            pass
    try:
        apply_vetoes(dec, [('a', 2)])                                     # not an episode start
        raise SystemExit('apply_vetoes accepted a non-start')
    except AssertionError:
        pass
    assert bp_hits(['SBP 142', 'reading 128/84', '5 mmHg', 'cuff_sbp_last = 131', 'a diagnosis']) and \
        len(bp_hits(['SBP 142', 'reading 128/84', '5 mmHg', 'cuff_sbp_last = 131', 'a diagnosis'])) == 5
    assert not bp_hits([ACTION, 'The weekly deviation exceeded the personal threshold in 4 of 6 evaluable weeks.',
                        'The last home-cuff reading was 37 days before this week.', 'Inputs imputed: cuff_sbp_last.'])
    ns = {'profile': {'drivers': [{'mean_z_6w': 1.0}], 'quality': {'n_eval': 6}}}
    assert resolve(ns, 'profile.drivers.0.mean_z_6w') and not resolve(ns, 'profile.drivers.1.mean_z_6w')
    assert not resolve(ns, 'profile.quality.nope') and validate({'a': 1}, {'a': STR}) and not validate(None, NUM)
    print('agents self-check OK')

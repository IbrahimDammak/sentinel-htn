"""WARN — three-state decision (POOR_QUALITY / INSUFFICIENT / WARNING) and the evidence ledger."""
import numpy as np
import pandas as pd

from . import CHANNELS, PULSE, STATES


def _state(pred, thr_p, min_valid_30):
    poor = ~(pred.valid_days_30 >= min_valid_30).to_numpy()   # NaN counts as poor quality
    warn = (pred.p_lo >= thr_p).to_numpy() & pred.persist.fillna(False).astype(bool).to_numpy()
    return np.where(poor, 'POOR_QUALITY', np.where(warn, 'WARNING', 'INSUFFICIENT'))


def decide(pred, thr_p, min_valid_30=15):
    """POOR_QUALITY if valid_days_30 is low; WARNING if p_lo >= thr_p AND persist; else INSUFFICIENT."""
    dec = pred.copy()
    dec['state'] = _state(pred, thr_p, min_valid_30)
    assert set(dec.state) <= set(STATES)
    return dec


def _episodes(is_warn, pid):
    """Count False->True transitions per person on rows sorted by (pid, week)."""
    prev = np.r_[False, is_warn[:-1]] & np.r_[False, pid[1:] == pid[:-1]]
    return int((is_warn & ~prev).sum())


def tune_warning(pred, people, budget=0.5, grid=None):
    """Smallest thr_p whose WARNING episodes per non-converter person-year are <= budget."""
    if grid is None:
        grid = np.r_[np.linspace(0, 1, 201), 1.01]   # 1.01 = never warn, always within budget
    pred = pred.sort_values(['pid', 'week'])
    nc = people.loc[~people.converter.astype(bool) & people.pid.isin(pred.pid)]
    years = (nc.end_day + 1).sum() / 365.25
    keep = pred.pid.isin(nc.pid).to_numpy()
    pid = pred.pid.to_numpy()[keep]
    for thr in np.sort(grid):
        is_warn = _state(pred, thr, 15)[keep] == 'WARNING'
        if _episodes(is_warn, pid) <= budget * years:
            return float(thr)
    return float(np.max(grid))


# Repeat suppression: 26 weeks, chosen to equal the 26-week prediction horizon (not the clinical panel's rule,
# which was 13 weeks after a normal cuff series; 13 weeks gives 0.28 vs 0.25 prompts/py), so a person is
# asked for at most one confirmatory home-BP week per horizon. A burden metric only: states, first warnings, tuned
# thresholds and the chance floor are untouched.
REFRACTORY_WEEKS = 26


def prompts(dec, refractory=REFRACTORY_WEEKS):
    """Boolean Series (dec's index): WARNING episode starts that become prompts once any start within `refractory`
    weeks after the person's previous prompt is suppressed. Every person's first start is always a prompt."""
    d = dec.sort_values(['pid', 'week'])
    w, pid, week = (d.state == 'WARNING').to_numpy(), d.pid.to_numpy(), d.week.to_numpy()
    out = w & ~(np.r_[False, w[:-1]] & np.r_[False, pid[1:] == pid[:-1]])
    last = {}
    for i in np.flatnonzero(out):
        if week[i] - last.get(pid[i], -np.inf) <= refractory:
            out[i] = False
        else:
            last[pid[i]] = week[i]
    return pd.Series(out, d.index).reindex(dec.index)


def first_warnings(dec):
    """Per person: first WARNING week and its day (end of that landmark week, 7*week+6; NaN if never)."""
    out = pd.DataFrame({'pid': dec.pid.unique()})
    fw = dec.loc[dec.state == 'WARNING'].groupby('pid').week.min()
    out['first_warning_week'] = out.pid.map(fw).astype(float)
    out['first_warning_day'] = 7 * out.first_warning_week + 6
    return out


def _num(v, kind=float):
    return None if v is None or pd.isna(v) else kind(v)


def ledger(dec, wk, pid, week):
    """Evidence behind one decision as a JSON-serialisable dict."""
    r = dec[(dec.pid == pid) & (dec.week == week)].iloc[0]
    w6 = wk[(wk.pid == pid) & wk.week.between(week - 5, week)]
    last = w6[w6.week == week]
    return {
        'state': str(r.state),
        'p': _num(r.p), 'p_lo': _num(r.p_lo), 'p_hi': _num(r.p_hi),
        'weeks_exceeded': '%d/%d' % (r.n_exceed, r.n_eval),   # n_exceed / n_eval
        'episodes': _num(last.episodes.iloc[0], int) if len(last) and 'episodes' in last else None,
        'dev_slope12': _num(r.dev_slope12),
        'channel_contrib': {c: _num(w6[c + '_w'].mean()) for c in CHANNELS + PULSE if c + '_w' in w6},
        'valid_days_30': _num(r.valid_days_30, int),
        'ctx_masked_6w': _num(w6.ctx_masked.sum(), int) if 'ctx_masked' in w6 else None,
        'month': _num(r.month, int) if 'month' in r else None,
    }


if __name__ == '__main__':
    import json
    rows = []   # (pid, week, p_lo, persist, valid_days_30)
    rows += [('a', w, 0.6 if w in (2, 3, 6) else 0.1, w in (2, 3, 6), 30) for w in range(8)]   # 2 episodes, first at wk 2
    rows += [('b', w, 0.9, True, 5) for w in range(8)]                                          # poor quality wins
    rows += [('c', w, 0.9, False, 30) for w in range(8)]                                        # no persistence
    rows += [('d', w, 0.6, True, 30) for w in range(8)]                                         # non-converter, always warned
    pred = pd.DataFrame(rows, columns=['pid', 'week', 'p_lo', 'persist', 'valid_days_30'])
    pred['p'], pred['p_hi'] = pred.p_lo + 0.05, pred.p_lo + 0.1
    pred['n_exceed'], pred['n_eval'], pred['dev_slope12'], pred['month'] = 4, 6, 0.02, 3
    dec = decide(pred, 0.5)
    assert set(dec.state) <= set(STATES) and 'STABLE' not in STATES
    assert (dec[dec.pid == 'b'].state == 'POOR_QUALITY').all()
    assert (dec[dec.pid == 'c'].state == 'INSUFFICIENT').all()
    assert list(dec[dec.pid == 'a'].state.iloc[[1, 2, 3, 4, 6]]) == ['INSUFFICIENT', 'WARNING', 'WARNING', 'INSUFFICIENT', 'WARNING']
    fw = first_warnings(dec).set_index('pid')
    assert fw.loc['a', 'first_warning_week'] == 2 and fw.loc['a', 'first_warning_day'] == 20
    assert fw.loc['d', 'first_warning_week'] == 0 and fw.loc['d', 'first_warning_day'] == 6
    assert fw.loc[['b', 'c']].first_warning_day.isna().all()
    people = pd.DataFrame({'pid': list('abcd'), 'converter': [True, True, False, False], 'end_day': 364})
    assert _episodes(np.array([1, 1, 0, 1, 0, 0, 1], bool), np.array(list('aaabbbb'))) == 3
    thr = tune_warning(pred, people, budget=0.5)   # d alone would give 1 episode/yr > 0.5 at thr <= 0.6
    assert thr > 0.6 and 0 <= thr <= 1.01, thr
    assert tune_warning(pred, people, budget=5) == 0.0
    pr = prompts(dec, refractory=4)   # a: starts at weeks 2 and 6 (6 - 2 <= 4 suppressed); d: one start
    assert prompts(dec, 3).sum() == 3 and pr.sum() == 2 and dec[pr].groupby('pid').week.min().to_dict() == {'a': 2, 'd': 0}
    sp = pd.DataFrame({'pid': 'e', 'week': range(40), 'state': ['WARNING' if w in (1, 5, 6, 30, 33) else 'INSUFFICIENT'
                                                              for w in range(40)]})
    assert sp.week[prompts(sp)].tolist() == [1, 30] and sp.week[prompts(sp, 0)].tolist() == [1, 5, 30, 33]   # 5, 33 within 26 wk
    wk = pd.DataFrame({'pid': 'a', 'week': range(8), 'ctx_masked': 1, 'episodes': 1, 'night_rhr_w': 0.8, 'steps_w': np.nan})
    led = ledger(dec, wk, 'a', 6)
    assert led['state'] == 'WARNING' and abs(led['channel_contrib']['night_rhr'] - 0.8) < 1e-9 and led['ctx_masked_6w'] == 6
    json.dumps(led)
    print('warn OK', led['weeks_exceeded'], thr)

"""End-to-end test: python tests/test_pipeline.py (~15 s). Uses a strong-signal cohort (effect=4): at the calibrated
realistic effect a single small cohort can sit at chance by luck, so it could not tell a bug from noise."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import subprocess
import tempfile

import numpy as np
import pandas as pd

import run
from sentinel import PULSE, STATES, agents, data, learn
from sentinel.lifesnaps import load_lifesnaps
from sentinel.evaluate import metrics
from sentinel.predict import FEATURE_SETS, local_trend

KEYS = ['auroc', 'auprc', 'sens_lead_0', 'sens_lead_30', 'sens_lead_90', 'sens_lead_180', 'median_lead',
        'alarms_per_nonconv_py', 'warning_precision', 'brier', 'ece', 'aurc', 'abstention_rate']

if __name__ == '__main__':
    assert 'STABLE' not in STATES and len(STATES) == 3
    assert all('onset' not in cols for cols in FEATURE_SETS.values())
    curve = {'0.5': {'alarms_per_nonconv_py': .4, 's': .3}, '0.25': {'alarms_per_nonconv_py': .2, 's': .1}}
    assert np.allclose([run._at_rate(curve, 's', a) for a in (.1, .3, 1.)], [.05, .2, .3])   # 0 alarms = 0; clamped
    y = np.random.default_rng(0).normal(0, .2, (5, 40))
    ok = y > -.3
    s1 = local_trend(y, ok)[0]
    y[:, 25:] += 3
    assert np.allclose(s1[:, :25], local_trend(y, ok)[0][:, :25])   # Kalman trend at week t ignores weeks > t
    daily, people = data.make_cohort(600, 450, seed=0, effect=4.0)   # strong-signal sanity cohort: catches broken/inverted pipelines
    split = run.make_split(people, 0)
    tp = people[people.pid.isin(split['test'])]
    cfg = {**run.BASE, 'n_boot': 5}
    dec, wk, models, th = run.pipeline(daily, people, split, cfg)
    assert set(dec.state) <= set(STATES)
    m = metrics(dec, tp)
    assert all(k in m for k in KEYS), [k for k in KEYS if k not in m]
    assert m['auroc'] > 0.6, m['auroc']
    dec6 = run.pipeline(daily, people, split, cfg, (models, th), ('mcar', 0.6, {}))[0]
    m6 = metrics(dec6, tp)
    assert m6['abstention_rate'] > m['abstention_rate'], (m['abstention_rate'], m6['abstention_rate'])
    # optional pulse channels: off by default; used when switched on; all-NaN columns with pulse on behave exactly like
    # the default (dropped) run
    assert set(models['weights']) == set(run.CHANNELS) and not {c + '_w' for c in PULSE} & set(wk)
    d_on = run.pipeline(daily, people, split, {**cfg, 'pulse': True})
    assert all(d_on[2]['weights'][c] > 0 for c in PULSE) and {c + '_w' for c in PULSE} <= set(d_on[1])
    d_nan = run.pipeline(daily.assign(**dict.fromkeys(PULSE, np.nan)), people, split, {**cfg, 'pulse': True})
    pd.testing.assert_frame_equal(d_nan[0], dec)
    assert d_nan[1].columns.equals(wk.columns) and set(d_nan[2]['weights']) == set(run.CHANNELS)
    # real-world path: test people rewritten in LifeSnaps CSV format -> adapter -> label-free transfer metrics
    t = daily[daily.pid.isin(tp.pid)]
    csv = os.path.join(tempfile.mkdtemp(), 'lifesnaps.csv')
    pd.DataFrame({'id': t.pid, 'date': pd.Timestamp('2021-05-24') + pd.to_timedelta(t.day, unit='D'),
                  'nremhr': t.night_rhr, 'rmssd': t.night_rmssd, 'resting_hr': t.still_hr, 'steps': t.steps,
                  'minutesAsleep': t.sleep_dur * 60, 'very_active_minutes': t.exercise_min,
                  'age': '<30', 'gender': 'MALE', 'bmi': '23.0'}).to_csv(csv)
    rw = run.real_world(*load_lifesnaps(csv), cfg, (models, th))
    assert rw['people'] == tp.pid.nunique() and 0 <= rw['abstention_rate'] <= 1 and rw['warning_episodes_py'] >= 0, rw

    # ---- agent audit layer (sentinel/agents.py)
    # personal_baseline moments leave every z value unchanged
    g = run._adjust(learn.quality_gate(daily[daily.pid.isin(split['test'])].drop(columns=PULSE)), models['ctx'])
    r0, r1 = learn.personal_baseline(g, models['prior']), learn.personal_baseline(g, models['prior'], moments=True)
    pd.testing.assert_frame_equal(r0, r1[r0.columns])
    assert {c + s for c in run.CHANNELS for s in ('_m', '_v')} == set(r1.columns) - set(r0.columns)

    # seeded random loop: the audit never upgrades, never touches POOR_QUALITY, every veto removes a whole episode
    rng = np.random.default_rng(0)
    n_cases = n_vetoes = 0
    for case in range(1000):
        rows = []
        for i in range(rng.integers(1, 5)):
            st = rng.choice(STATES)
            for w in range(rng.integers(3, 80)):
                st = st if rng.random() < .8 else rng.choice(STATES)
                rows.append((f'p{i}', w, st))
        dec_r = pd.DataFrame(rows, columns=['pid', 'week', 'state']).sample(frac=1, random_state=case)
        pv = rng.random()
        out, cs = agents.audit_loop(dec_r, lambda cur, p, w: {'auditor': {'final_state': 'INSUFFICIENT' if rng.random() < pv else 'WARNING'}})
        b, a = dec_r.sort_values(['pid', 'week']), out.sort_values(['pid', 'week'])
        ch = b.state.to_numpy() != a.state.to_numpy()
        assert ((b.state[ch] == 'WARNING') & (a.state[ch] == 'INSUFFICIENT')).all()          # never upgrades
        assert ((b.state == 'POOR_QUALITY') == (a.state == 'POOR_QUALITY')).all()            # POOR_QUALITY untouched
        isw = b.state.eq('WARNING')
        ep = (isw & ~(isw.shift(fill_value=False) & b.pid.eq(b.pid.shift()))).cumsum().where(isw, 0)
        assert pd.Series(ch, b.index)[isw].groupby(ep[isw]).nunique().max() <= 1 if isw.any() else True  # whole episodes
        for (p, w), c in cs.items():                                                         # each veto = its episode gone
            e = ep[(b.pid == p) & (b.week == w)].iloc[0]
            assert e > 0 and (a.state[ep == e] == ('WARNING' if c['auditor']['final_state'] == 'WARNING' else 'INSUFFICIENT')).all()
        assert all(k in cs for k in zip(out.pid[run.warn.prompts(out)], out.week[run.warn.prompts(out)]))  # all prompts audited
        n_cases += len(cs)
        n_vetoes += sum(c['auditor']['final_state'] != 'WARNING' for c in cs.values())
    assert n_cases > 1000 and 0 < n_vetoes < n_cases, (n_cases, n_vetoes)

    # the layer on the real pipeline output; same input -> identical records
    ag, dec_a, cases = run.agent_layer(daily, people, split, cfg, dec, wk, models, th)
    assert cases and json.dumps(run._clean(cases)) == json.dumps(run._clean(run.agent_layer(daily, people, split, cfg, dec, wk, models, th)[2]))
    agents.check_invariants(dec, dec_a)
    for c in cases:
        assert not agents.validate(c['profiler'], agents.PROFILE_SPEC) and not agents.validate(c['predictor'], agents.PREDICTOR_SPEC)
        assert not agents.validate(c['auditor'], agents.AUDITOR_SPEC) and c['predictor']['agrees_with_pipeline']
        assert c['predictor']['p_lo'] == dec_a.set_index(['pid', 'week']).p_lo[(c['predictor']['pid'], c['predictor']['week'])]
    assert ag['counts']['prompts_audited'] == len(cases) and set(ag['failed_checks']) == set(agents.CHECKS)

    # broken ref -> rejected (returned once, the reason dropped); BP number -> rejected (veto)
    c0 = cases[0]
    pf = {k: v for k, v in c0['profiler'].items() if k not in ('concerns', 'summary')}
    pf['quality'] = {**pf['quality'], 'ctx_masked_weekly': [0] * len(pf['quality']['ctx_masked_weekly'])}
    qf = {k: v for k, v in c0['predictor'].items() if k in ('pid', 'week', 'p', 'p_lo', 'p_hi', 'thr_p', 'cuff', 'pipeline_state', 'imputed_inputs')}
    tb = agents.template_backend()
    def with_reason(claim, ref, only=False):
        def predict(ns):
            o = tb['predict'](ns)
            return {**o, 'reasons': ([] if only else o['reasons']) + [{'claim': claim, 'ref': ref}]}
        return {**tb, 'predict': predict}
    ok = agents.audit_case(pf, qf, th['thr_p'], tb)
    assert ok['auditor']['verdict'] == 'approve' and ok['auditor']['final_state'] == 'WARNING' and ok['returned'] is None
    br = agents.audit_case(pf, qf, th['thr_p'], with_reason('Made-up field.', 'predictor.no_such_field'))
    first = {x['name']: x['pass'] for x in br['returned']['auditor']['checks']}
    assert not first['refs_resolve'] and br['returned']['auditor']['verdict'] == 'return_once'
    assert br['auditor']['verdict'] == 'approve' and all(r['ref'] != 'predictor.no_such_field' for r in br['predictor']['reasons'])
    only = agents.audit_case(pf, qf, th['thr_p'], with_reason('Made-up field.', 'predictor.no_such_field', only=True))
    assert only['auditor']['verdict'] == 'veto' and only['auditor']['final_state'] == 'INSUFFICIENT'
    bp = agents.audit_case(pf, qf, th['thr_p'], with_reason('Estimated SBP 142 mmHg.', 'predictor.p'))
    assert bp['auditor']['verdict'] == 'veto' and not {x['name']: x['pass'] for x in bp['auditor']['checks']}['no_bp_number']
    try:
        agents.llm_backend()
        raise AssertionError('llm_backend must be a stub')
    except NotImplementedError:
        pass

    # CLI: with --agents off, outputs are those of the agents run minus every agent key / section
    tmp = tempfile.mkdtemp()
    for flag in ([], ['--agents']):
        subprocess.run([sys.executable, 'run.py', '--synthetic', '--quick', '--seed', '0', '--out', os.path.join(tmp, str(len(flag))), *flag],
                       check=True, capture_output=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    off, on = (json.load(open(os.path.join(tmp, k, 'metrics.json'))) for k in '01')
    assert 'agents' not in off and not os.path.exists(os.path.join(tmp, '0', 'agent_records.json'))
    on.pop('agents')
    if on['ledger']:
        on['ledger'].pop('agents')
    assert on == off
    rep_off, rep_on = (open(os.path.join(tmp, k, 'report.md')).read() for k in '01')
    assert '## Agent audit layer' in rep_on and '## Agent audit layer' not in rep_off
    head, rest = rep_on.split('\n\n## Agent audit layer')
    assert head + '\n\nFigures:' + rest.split('\n\nFigures:')[1] == rep_off
    print('agents test OK', ag['counts'])

    print('pipeline test OK', {k: round(m[k], 3) for k in ('auroc', 'abstention_rate')}, 'mcar0.6 abstention', round(m6['abstention_rate'], 3))

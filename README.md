# SENTINEL-HTN

Personalised, uncertainty-aware early warning of emerging hypertension from a single wrist strap (AIoT), with
pluggable frozen wearable foundation models. Built for the BioVance AIoT Challenge (IEEE EMBS Tunisia).

## The problem

The challenge asks whether longitudinal multimodal wearable data can show a person drifting from their own baseline
toward hypertension **before clinical detection**. The signals are noisy, individual, context-dependent and often
missing, and an early but unreliable warning is not useful. So the system must follow

`X(1:t) -> personal baseline -> change -> trajectory -> early warning`

and report a risk estimate, an early-warning time, its uncertainty, the evidence behind it and a data-quality
assessment. The clinical reference `t_ref` is the first of two consecutive home-cuff (HBPM) occasions averaging
>= 130 systolic or >= 80 diastolic. The system never outputs a blood-pressure number: a warning means "measure with a
cuff for a week".

## Architecture

![SENTINEL-HTN architecture](paper/figures/fig_architecture.png)

### Full system overview

Solid arrows run on every person-week. Dashed parts are optional and off by default: the core never imports them.

```mermaid
flowchart LR
    subgraph IN["Inputs"]
        S["Wrist strap<br/>night HR, night RMSSD, resting HR,<br/>steps, sleep duration and regularity,<br/>SQI, irregular-rhythm flag, firmware"]
        P["Phone context<br/>temperature, month, menses,<br/>exercise minutes, alcohol, illness"]
        C["Sparse home cuff<br/>SBP / DBP readings"]
        PPG["Nightly raw PPG clips<br/>(optional)"]
        HW["Hourly phone and watch data<br/>(optional)"]
    end
    subgraph FM["Optional frozen foundation-model encoders"]
        PG["PaPaGei-S encoder<br/>PPG clip to 512-d"]
        PH["Hypertension head<br/>trained on PPG-BP"]
        WB["WBM encoder<br/>hourly week 168x38 to 256-d"]
        WD["Behaviour drift channel<br/>(planned)"]
    end
    subgraph CORE["Core pipeline: NumPy, pandas, SciPy only"]
        Q["Quality gate<br/>valid days, acute masks<br/>RQ5"]
        L["1 Learn<br/>context adjustment,<br/>personal baseline, z-scores<br/>RQ1 RQ4"]
        D["2 Detect<br/>weighted weekly deviation,<br/>CUSUM, 4-of-6 persistence,<br/>Kalman trend<br/>RQ2"]
        PR["3 Predict<br/>26-week landmark risk,<br/>bootstrap band, Platt calibration<br/>RQ3"]
        W["4 Warn<br/>three states, alarm budget,<br/>evidence ledger<br/>RQ6"]
    end
    subgraph OUT["Output per person-week"]
        WA["WARNING<br/>measure with a home cuff for 7 days"]
        IS["INSUFFICIENT<br/>keep monitoring"]
        PQ["POOR_QUALITY<br/>abstain"]
        LED["Evidence ledger<br/>weeks exceeded, channels,<br/>risk band, data quality"]
    end
    subgraph AG["Optional agent audit layer: run.py --agents"]
        A1["Profiler"] --> A2["Predictor"] --> A3["Auditor"]
    end
    S --> Q
    P --> Q
    Q --> L --> D --> PR --> W
    C --> PR
    PPG -.-> PG -.-> PH -. "pulse_htn channel" .-> L
    HW -.-> WB -.-> WD -.-> L
    W --> WA
    W --> IS
    W --> PQ
    W --> LED
    W -. "each prompt" .-> A1
    A3 -. "approve" .-> WA
    A3 -. "veto: whole episode" .-> IS
```

| Stage | File | Research question | What it does |
|---|---|---|---|
| Learn | `sentinel/learn.py` | RQ1 personalisation, RQ4 context | quality gate; regress out slow context (temperature, season, menses); mask acute context (exercise, alcohol, illness); normal-normal shrinkage baseline per person, restarted on a firmware change; clipped z-scores |
| Detect | `sentinel/detect.py` | RQ2 temporal reasoning, RQ4 | weekly joint deviation weighted by evidence prior x label-free reliability; CUSUM; persistence rule (4 of the last 6 evaluable weeks); Kalman local-linear trend. Missing weeks are "not evaluable", never negative |
| Predict | `sentinel/predict.py` | RQ3 early detection | landmark-week ridge logistic risk of conversion within 26 weeks (each person weighs one), 20 person-level bootstrap refits for the band, Platt calibration with a non-negative slope; null comparators `level_only`, `cuff_only` |
| Warn | `sentinel/warn.py` | RQ6 uncertainty, evidence | three-state decision with abstention; persistence "watch" tier (2 episodes/person-year) confirmed by the risk gate tuned to 0.5 alarms per non-converter person-year; per-decision evidence ledger |
| Evaluate | `sentinel/evaluate.py`, `run.py` | RQ5 reliability | metrics A-F, chance floor at the model's own alarm rate, ablations, robustness, fairness by skin tone |

`sentinel/data.py` holds the synthetic cohort (calibrated to LifeSnaps), the CSV loader and the perturbations. The
interfaces are fixed in `CONTRACT.md`.

### Training and deployment

```mermaid
flowchart LR
    COH["Cohort<br/>synthetic, or organiser CSV"] --> SP{"Subject-grouped split<br/>stratified by converter"}
    SP -- "60%" --> FIT["Fit people<br/>context coefficients, population prior,<br/>channel weights, persistence threshold,<br/>trend noise, risk model"]
    SP -- "20%" --> CAL["Calibration people<br/>Platt calibration, warning threshold,<br/>sensitivity-at-specificity threshold"]
    SP -- "20%" --> TEST["Test people<br/>scored only, clean and perturbed"]
    FIT --> LOCK["Locked model<br/>plus per-user state"]
    CAL --> LOCK
    LOCK --> TEST
    LOCK --> DEP["Deployment<br/>phone updates each person's state,<br/>a few vector operations per night"]
```

### Inside the core pipeline

```mermaid
flowchart TB
    subgraph QG["Quality gate: learn.quality_gate"]
        q1["valid day: SQI at least 0.6, no irregular rhythm,<br/>at least one channel present"]
        q2["acute context: exercise over 45 min, alcohol or illness<br/>masks night HR, RMSSD, resting HR and pulse that night"]
        q1 --> q2
    end
    subgraph LE["1 Learn: learn.py"]
        l1["fit_context: pooled least squares on temperature,<br/>sin and cos of month, menses, giving x_adj"]
        l2["fit_prior: population mean mu0, between-person tau,<br/>within-person sigma, from fit people's first 56 days"]
        l3["personal_baseline: normal-normal posterior m_i, v_i<br/>from the first 28 valid days, restarted on a firmware change"]
        l4["z = sign x (x_adj - m_i) / sqrt(sigma^2 + v_i), clipped to +-6"]
        l1 --> l2 --> l3 --> l4
    end
    subgraph DE["2 Detect: detect.py"]
        d1["weekly mean z per channel, at least 3 days<br/>evaluable week: at least 4 valid days"]
        d2["joint deviation: weighted mean of channel z<br/>weight = literature prior / variance, never fitted to labels"]
        d3["CUSUM: S = max(0, S + dev - 0.25)"]
        d4["persistence: dev over theta in 4 of the last 6 evaluable weeks<br/>theta set to 2 episodes per non-converter year (watch tier)"]
        d5["Kalman local linear trend<br/>slope and slope z, causal"]
        d1 --> d2
        d2 --> d3
        d2 --> d4
        d2 --> d5
    end
    subgraph PRE["3 Predict: predict.py"]
        p1["one landmark row per person-week until t_ref<br/>label: t_ref within the next 26 weeks"]
        p2["features: level (age, sex, BMI, resting HR, last cuff and its age)<br/>change (deviation, 12-week slope, CUSUM, persistence, trend)<br/>quality (valid days in 30)"]
        p3["ridge logistic regression, each person weighs 1, L2 = 10"]
        p4["20 person-level bootstrap refits<br/>band p_lo, p_hi = 10th and 90th percentiles"]
        p5["Platt calibration on out-of-fold and calibration scores<br/>slope kept non-negative"]
        p1 --> p2 --> p3 --> p4 --> p5
    end
    subgraph WR["4 Warn: warn.py"]
        w1{"at least 15 valid days<br/>in the last 30?"}
        w2{"p_lo at least theta_p<br/>AND persistence?"}
        w1 -- no --> wq["POOR_QUALITY"]
        w1 -- yes --> w2
        w2 -- yes --> ww["WARNING<br/>theta_p set to 0.5 episodes<br/>per non-converter year"]
        w2 -- no --> wi["INSUFFICIENT"]
        ww --> w3["evidence ledger, prompts with a<br/>26-week refractory (burden metric)"]
    end
    CUFF["home cuff readings"] --> p2
    q2 --> l1
    l4 --> d1
    d3 --> p2
    d4 --> p2
    d5 --> p2
    d4 --> w2
    p5 --> w1
```

### The three states

| State | Meaning |
|---|---|
| `WARNING` | sufficient evidence: the calibrated risk lower bound clears the threshold **and** the deviation is persistent |
| `INSUFFICIENT` | no reliable conclusion; keep monitoring |
| `POOR_QUALITY` | too few valid days in the last 30; any warning is suppressed |

There is no "stable" state: absence of a warning is not a claim of health.

```mermaid
flowchart TD
    A["Week w for person i"] --> B{">= 15 valid days<br/>in the last 30?"}
    B -- no --> PQ["POOR_QUALITY"]
    B -- yes --> C{"Persistence:<br/>dev > theta in >= 4 of<br/>last 6 evaluable weeks?"}
    C -- no --> IS["INSUFFICIENT"]
    C -- yes --> D{"Risk lower bound<br/>p_lo >= theta_p?"}
    D -- no --> IS
    D -- yes --> WA["WARNING + evidence ledger"]
```

### Optional foundation-model encoders

Both are frozen (never trained here), enter Learn as ordinary channels, and are **off by default**: the core runs
unchanged without them and never imports torch.

- **PaPaGei-S** (`sentinel/pulse.py`): PPG clip -> 512-d embedding -> hypertension head -> nightly `pulse_htn` channel
  (evidence prior 0.5: cross-sectional evidence only).
- **WBM** from OpenMHC (`sentinel/wbm.py`): hourly week of 19 phone/watch channels plus missingness flags (168 x 38)
  -> 256-d. Probed on real LifeSnaps data; its drift channel is planned, not yet in the pipeline.

Both are encoder-only: a frozen pretrained encoder turns a signal into an embedding, and a small head trained here
reads it. Nothing is decoded and no encoder weight is changed.

**PaPaGei-S: pulse shape** (`python -m sentinel.pulse`, separate CPU environment)

```mermaid
flowchart LR
    subgraph TEST["Real-label test: PPG-BP, 219 people, one cuff reading each"]
        c1["3 fingertip PPG clips<br/>2.1 s at 1 kHz"] --> c2["preprocessing: z-score,<br/>band-pass 0.5-12 Hz, 50 ms smoothing,<br/>resample to 125 Hz, pad to 10 s"]
        c2 --> c3["PaPaGei-S encoder, frozen<br/>1D ResNet mixture-of-experts, 18 blocks"]
        c3 --> c4["512-d embedding per clip<br/>mean of the 3 clips per person"]
        c4 --> c5["L2 logistic head<br/>label: SBP at least 120"]
        DEMO["age, sex, BMI"] --> c5
        c5 --> c6["20 x 5-fold subject-level CV<br/>demographics 0.70, embeddings 0.70,<br/>both 0.75 (gain +0.05, CI -0.01 to +0.10)"]
    end
    subgraph CH["As a pipeline channel: with_pulse variant"]
        n1["clean nightly wrist clips, up to 10 s"] --> n2["same preprocessing<br/>and frozen encoder"] --> n3["head logit per clip"] --> n4["nightly median = pulse_htn<br/>risk sign +1, evidence prior 0.5"] --> n5["enters Learn<br/>like any other channel"]
    end
    c5 -. "saved head" .-> n3
    n5 --> R["simulator: no early-warning gain<br/>at matched alarm rates, so off by default"]
```

**WBM: behaviour** (`python -m sentinel.wbm [--no-energy]`, CUDA GPU environment)

```mermaid
flowchart LR
    subgraph PROBE["Real-data probe: LifeSnaps, 68 Fitbit users, 606 person-weeks"]
        h1["hourly Fitbit export"] --> h2["map to WBM channels: steps, distance,<br/>heart rate, active energy<br/>the other 15 channels flagged missing"]
        h2 --> h3["keep weeks with at least 84 worn hours<br/>168 hours x (19 values + 19 missing flags)"]
        h3 --> h4["normalise with WBM's own statistics"]
        h4 --> h5["WBM encoder, frozen<br/>Mamba-2, 6.4M parameters, OpenMHC weights"]
        h5 --> h6["256-d embedding per week<br/>mean per person"]
        h6 --> h7["L2 logistic probe vs 6 hand-made features<br/>20 x 5-fold CV, 200 permutations"]
        h7 --> h8["sex 0.76 vs 0.66, no age signal<br/>BMI only through the calorie channel: a leak, removed"]
    end
    h6 -. "planned" .-> PL["drift channel: weekly distance<br/>from the person's baseline embedding, into Learn"]
    h6 -.-> NC["matched-cohort negative control<br/>LifeSnaps x PPG-BP borrowed labels (matched.py)"]
```

### Optional agent audit layer

`sentinel/agents.py` (`run.py --agents`, main model only) mirrors the stages with three agents: a **Profiler**
(Learn + Detect facts about one person's recent weeks), a **Predictor** (the pipeline's risk, copied, and a proposed
state) and an **Auditor** that checks each prompt against the evidence and the gates and approves or vetoes it. Its
purpose is traceability (every claim cites a field of the record) and a conservative second check, **not** better
discrimination: the only allowed change is downgrading a whole WARNING episode to INSUFFICIENT, enforced in code.
Only a deterministic template backend exists (no API key). On the simulator its one live check (acute-context
confounding) vetoes many prompts at a real cost in early detections; see `results/agents/summary.md`.

```mermaid
flowchart TB
    DEC["Warn output: decision table"] --> PRM["warn.prompts: WARNING episode starts outside<br/>the 26-week refractory, not yet audited"]
    TOOLS["pipeline tools: warn.ledger, weekly table,<br/>personal_baseline(moments=True)"] -.-> PF
    PRM --> PF
    subgraph CASE["One audit case: records are plain dicts, every claim cites a field"]
        PF["Profiler: Learn + Detect<br/>facts only: data quality, deviation, persistence,<br/>channel z, usual range m_i +- 2 sqrt(sigma^2 + v_i)"]
        PD["Predictor: Predict<br/>copies p, p_lo, p_hi, theta_p and past cuff readings,<br/>proposes a state, gives cited reasons"]
        AU["Auditor: Warn gate<br/>6 checks computed in code"]
        PF --> PD --> AU
        AU -- "only refs_resolve failed" --> RET["return once: drop reasons<br/>whose reference does not resolve"]
        RET --> AU
    end
    BK["backend: deterministic templates<br/>LLM backend is a stub"] -.-> CASE
    AU -- approve --> KEEP["WARNING kept"]
    AU -- veto --> VETO["apply_vetoes: the whole episode<br/>WARNING to INSUFFICIENT"]
    VETO --> INV["check_invariants: no upgrade, POOR_QUALITY untouched,<br/>no split episode, no new episode start"]
    INV -- "recompute prompts, audit new ones until none" --> PRM
    KEEP --> OUTS["outputs: metrics.json agents block,<br/>agent_records.json, ledger agents key, report.md section"]
    INV --> OUTS
```

| Auditor check | Rule | On a WARNING row | If it fails |
|---|---|---|---|
| `quality_gate` | at least 15 valid days in the last 30 | passes by construction | veto |
| `risk_gate` | p_lo at least theta_p | passes by construction | veto |
| `persistence` | at least 4 of the last 6 evaluable weeks above threshold | passes by construction | veto |
| `refs_resolve` | record well formed, every reference resolves, at least one reason | template cannot break it | return once, then approve or veto |
| `no_bp_number` | no mmHg, "128/84", "SBP 140" or diagnostic wording in any text | template cannot break it | veto |
| `context_confound` | fails if 3 of the last 6 weeks each have at least 3 acute-context masked days (fixed, never tuned) | the only check that can fail | veto |

## Data and validation

No public dataset follows the same people with wearables until a hypertension diagnosis, so each dataset answers
only the question it can answer honestly:

```mermaid
flowchart LR
    SIM["Calibrated simulator<br/>1,200 people x 540 days<br/>labels known"]
    LS["LifeSnaps<br/>71 Fitbit users, ~4 months<br/>no BP"]
    PB["PPG-BP<br/>219 people, one cuff reading<br/>fingertip PPG"]
    OM["OpenMHC<br/>wearables + hypertension labels<br/>access pending"]
    SIM --> R1["Full pipeline:<br/>discrimination, lead time,<br/>calibration, alarm burden"]
    LS --> R2["Simulator calibration<br/>noise and missingness"]
    LS --> R3["Real-world transfer:<br/>coverage, abstention, false alarms"]
    LS --> R4["Noise transplant and<br/>plasmode stress tests"]
    LS --> R5["WBM probe on real data"]
    PB --> R6["PaPaGei pulse-shape test<br/>on real cuff labels"]
    OM -.-> R7["Real test of early warning"]
```

## Results

Held-out results on the calibrated simulator (3 seeds x 1,200 people x 540 days, mean ± SD):

| Model | AUROC | AUPRC | Se30 | Se90 | Alarms/py |
|---|---|---|---|---|---|
| **Full** | **0.621 ± 0.014** | **0.120 ± 0.020** | **0.322 ± 0.051** | 0.161 ± 0.072 | 0.405 |
| Equal channel weights | 0.605 | 0.104 | 0.248 | 0.105 | 0.360 |
| Level-only (null) | 0.537 | 0.070 | 0.124 | 0.083 | 0.174 |
| Cuff-only (null) | 0.545 | 0.074 | 0.149 | 0.099 | 0.236 |
| No personalisation | 0.567 | 0.083 | 0.190 | 0.120 | 0.372 |
| No context | 0.550 | 0.078 | 0.193 | 0.138 | 0.357 |
| Chance (random alarms at the model's rate) | | | 0.257 | 0.206 | 0.405 |

Se30/Se90 = converters first warned >= 30/90 days before `t_ref`; alarms per non-converter person-year.

- **Early detection:** beats chance at 30 days in every seed; **not** at 90 days. Median lead 61 days.
- **Calibration:** Brier 0.059, ECE 0.006.
- **False-alarm burden:** 23% of non-converters get a first false prompt within a year (Kaplan-Meier); precision
  0.21; a 26-week pause after each prompt lowers the burden to 0.25 prompts/py without losing any first warning.
- **Real-world transfer (LifeSnaps, no labels):** no warnings over 8.3 person-years (95% upper bound 0.36/py),
  abstained in 23% of weeks.
- **Equity:** the darkest skin-tone tercile abstains five times more and is detected less often (Se30 0.21 vs 0.41).

Stress tests and foundation-model probes (all on real data):

| Test | Result | Files |
|---|---|---|
| Noise transplant: AR(1) noise replaced by real LifeSnaps residual blocks | results hold: AUROC 0.623, Se30 0.315 (chance 0.250, above in 3/3 seeds), 0.39 alarms/py, ECE 0.003 | `results/noise_transplant/comparison.md` |
| Plasmode: known drift injected into real LifeSnaps series | detected 0.31 on real series vs 0.77 simulated; the gap comes from real missingness (sparse evaluable weeks), not noise shape. 18 people, indicative | `results/plasmode/summary.md` |
| PaPaGei-S on PPG-BP | over age/sex/BMI: AUROC 0.70 -> 0.75 (corrected 95% CI -0.01 to +0.10): suggestive. As a simulated nightly channel: no early-warning gain, so it stays off | `results/ppg_bp/`, `results/pulse/` |
| WBM on LifeSnaps hourly data | calorie channel leaked BMI via the Fitbit profile and was removed; then sex AUROC 0.76 vs 0.66 for activity summaries; no age signal; says nothing about BP | `results/wbm_lifesnaps*/` |
| Matched LifeSnaps x PPG-BP cohort (negative control) | borrowed labels carry only the matching variables: wearables add nothing over age/sex/BMI | `results/matched/` |

![Calibration](results/pulse/seed0/calibration.png) ![Lead time](results/pulse/seed0/lead_time.png)

Paper results: `results/pulse/summary.md` (main model = `results/weighted`). `results/rq3_trend/` is the earlier,
uncalibrated simulator, kept because the paper cites its optimistic lead time.

## Run

```
pip install -r requirements.txt
python run.py --synthetic --quick --out results_quick      # ~15 s smoke run (too few converters for stable metrics)
python run.py --synthetic --n 1200 --seed 0 --out results/pulse/seed0   # paper setting (seeds 0-2): main + with_pulse
python run.py --summary results/pulse --ref results/weighted              # mean +- SD; main must equal results/weighted
python run.py --daily daily.csv --people people.csv --out results   # organiser data (schema in CONTRACT.md)
python run.py --lifesnaps data/lifesnaps/rais_anonymized/csv_rais_anonymized/daily_fitbit_sema_df_unprocessed.csv --n 1200 --out results/lifesnaps
python run.py --synthetic --n 1200 --seed 0 --agents --out results/agents/seed0   # + agent audit layer
python -m sentinel.agents --summary results/agents          # before vs after audit, mean +- SD over seeds
python tests/test_pipeline.py                               # end-to-end test (~10 s)
python -m sentinel.evaluate                                 # metric self-check against hand-computed values
```

Stress tests and experiments:

```
LS=data/lifesnaps/rais_anonymized/csv_rais_anonymized/daily_fitbit_sema_df_unprocessed.csv
python run.py --synthetic --n 1200 --seed 0 --noise-csv $LS --out results/noise_transplant/seed0   # noise transplant
python -m sentinel.realnoise $LS                            # plasmode -> results/plasmode/
python run.py --synthetic --n 1200 --seed 0 --pulse-coupling 0 --out results/pulse/coupling_0/seed0   # coupling sweep
python run.py --sweep results/pulse/coupling_0 results/pulse results/pulse/coupling_2x --out results/pulse
python -m sentinel.pulse                                    # PaPaGei on PPG-BP (needs the optional environment below)
python -m sentinel.matched                                  # matched-cohort negative control (needs WBM embeddings)
```

Options: `--n`, `--days`, `--seed`, `--quick` (n=150, days=360, 5 bootstrap resamples). The split is subject-grouped
60/20/20 (fit / calibration / test), stratified by converter. Every model, threshold and calibrator is fitted on clean
fit/calibration people; robustness runs perturb only the test people's data.

### Optional environments

PaPaGei (`sentinel/pulse.py`), in a separate virtualenv:

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install pyPPG==1.0.41 --no-deps
pip install dotmap openpyxl scikit-learn
```

It also needs PaPaGei (Nokia Bell Labs, BSD-3-Clause-Clear) cloned to `external/papagei/` with `weights/papagei_s.pt`,
and PPG-BP (Liang et al. 2018, CC0, figshare 5459299) unpacked to `data/ppg_bp/Data File/`. Then
`python -m sentinel.pulse` runs the self-checks and the experiment (~15 min on a 6-core CPU).

WBM (`sentinel/wbm.py`) needs a CUDA GPU with `torch`, `mamba-ssm`, `causal-conv1d` and `openmhc[hf]`
(weights `MyHeartCounts/openmhc-wbm-dp` from Hugging Face, OpenRAIL). We ran it in WSL2 on a 4 GB laptop GPU:

```
python -m sentinel.wbm [--no-energy]       # LifeSnaps hourly -> 256-d weekly embeddings -> linear probe
```

## Outputs (in `--out`)

- `metrics.json`: main model, ablations, robustness, fairness, thresholds, operating curve, chance floor and an example ledger
- `report.md`: tables for metrics A-F, ablations with deltas vs the full model, robustness, fairness by skin_ita tercile, and one evidence ledger for a warned converter
- `calibration.png`, `lead_time.png`, `risk_coverage.png`, `lead_vs_budget.png`

Metrics: A predictive (AUROC, AUPRC), B early detection (lead time, sensitivity at 0/30/90/180 days lead; in
simulation also with pre-onset first warnings counted as misses), C false-alarm burden (alarms per non-converter
person-year, warning precision, Kaplan-Meier probability of a first false prompt by 6 and 12 months, person-level PPV,
prompts under a 26-week repeat-suppression rule, reported as a burden figure only), D calibration (Brier, ECE),
E robustness, F uncertainty quality (AURC, abstention rate). "specificity" is cumulative over the whole follow-up
(non-converters never prompted), not a single-window specificity.

## Repository layout

```mermaid
flowchart LR
    RUN["run.py<br/>CLI: main model, ablations, robustness,<br/>fairness, operating curve, report"]
    INIT["sentinel/__init__.py<br/>channels, risk signs, evidence priors, states"]
    DATA["data.py<br/>simulator, CSV loader, perturbations"]
    LEARN["learn.py"] --> DET["detect.py"] --> PRED["predict.py"] --> WARN["warn.py"]
    EVAL["evaluate.py<br/>metrics A-F"]
    LS["lifesnaps.py<br/>real-data adapter"]
    RN["realnoise.py<br/>noise transplant, plasmode"]
    AGT["agents.py<br/>audit layer"]
    PUL["pulse.py<br/>PaPaGei, torch, CPU env"]
    WBMm["wbm.py<br/>WBM, GPU env"]
    MAT["matched.py<br/>negative control"]
    RES[("results/")]
    PAP["paper/<br/>main.tex, make_figures.py"]
    RUN --> DATA
    RUN --> LEARN
    RUN --> EVAL
    RUN --> LS
    RUN -. "--noise-csv" .-> RN
    RUN -. "--agents" .-> AGT
    INIT --- LEARN
    RUN --> RES
    PUL -. "own entry point" .-> RES
    WBMm -. "own entry point" .-> RES
    MAT -.-> RES
    RES --> PAP
```

| Path | Contents |
|---|---|
| `sentinel/` | the four pipeline stages (`learn`, `detect`, `predict`, `warn`), metrics (`evaluate`), simulator and loaders (`data`, `lifesnaps`) |
| `sentinel/pulse.py`, `wbm.py` | optional frozen foundation-model encoders (PaPaGei-S, WBM) |
| `sentinel/agents.py` | optional agent audit layer (`--agents`): Profiler, Predictor, Auditor; template backend |
| `sentinel/realnoise.py`, `matched.py` | real-noise stress tests (noise transplant, plasmode) and the matched-cohort negative control |
| `run.py`, `tests/` | CLI and end-to-end test |
| `CONTRACT.md` | data schema and module APIs (use it to plug in the organiser dataset) |
| `results/` | all reported results; paper numbers in `results/pulse/` and `results/weighted/` |
| `paper/` | IEEE paper (`main.tex`) and `make_figures.py` |
| `panel/`, `review/` | expert-panel audits and mock reviews behind the design (`panel/pulse_audit_doctor.md`) |

Raw data (`data/`), third-party code and weights (`external/`) and virtualenvs are never committed.

## Limitations

- **Early-warning results are simulated.** Noise and missingness are calibrated to real wearables and stress-tested
  with real noise, but the physiology-to-BP couplings, drift time course and labels are assumptions. Only labelled
  longitudinal data (the organisers' or OpenMHC) can establish performance.
- **Real-world data gaps are the main risk.** Plasmode injection shows detection drops on real series because few
  weeks are evaluable; wear time matters more than noise.
- **90-day warning does not beat chance;** the honest claim is about a month of lead.
- **Pulse channels are validated cross-sectionally only and are off by default;** WBM was pretrained on Apple data and
  sees only 3-4 of its 19 channels on Fitbit.
- **Equity gap** in darker skin, a known limit of optical sensing; the cuff fallback mitigates but does not remove it.
- **EM sensing is not in this code** beyond a rhythm gate, and the system makes no claim about acute events.
- **No mmHg output and not a diagnostic.** It is a research prototype: a warning means "get a proper cuff measurement".

## Data credits

LifeSnaps (Yfantidou et al., Sci. Data 2022, CC BY 4.0); PPG-BP (Liang et al., Sci. Data 2018, CC0); PaPaGei
(Pillai et al., ICLR 2025); WBM (Erturk et al., ICML 2025) via OpenMHC (Schuetz et al., 2026).

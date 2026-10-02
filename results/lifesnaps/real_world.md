# Real-world transfer test: LifeSnaps vs synthetic non-converters

Model and thresholds trained on synthetic data (n=1200, days=540, seed=0); context and population
prior refitted on LifeSnaps (label-free). LifeSnaps has no BP labels: all participants count as non-converters.

| metric | synthetic non-converters | LifeSnaps |
|---|---|---|
| people | 199.000 | 49.000 |
| person_years | 273.388 | 8.318 |
| valid_day_share | 0.682 | 0.665 |
| cover_night_rhr | 0.646 | 0.576 |
| cover_night_rmssd | 0.646 | 0.576 |
| cover_still_hr | 0.646 | 0.822 |
| cover_steps | 1.000 | 0.996 |
| cover_sleep_dur | 1.000 | 1.000 |
| cover_sleep_reg | 1.000 | 0.889 |
| evaluable_week_share | 0.724 | 0.246 |
| dev_sd | 0.249 | 0.522 |
| abstention_rate | 0.113 | 0.233 |
| watch_episodes_py | 1.317 | 0.962 |
| warning_episodes_py | 0.497 | 0.000 |
| people_warned | 0.387 | 0.000 |

## Day-to-day variability: real (LifeSnaps) vs simulator

Median within-person SD of each daily channel on valid days (synthetic: 300 people, seed 0).

| channel | LifeSnaps | simulator | real / simulator |
|---|---|---|---|
| night_rhr (bpm) | 4.29 | 2.77 | 1.55 |
| night_rmssd (ms) | 6.54 | 6.28 | 1.04 |
| still_hr (bpm, Fitbit resting HR) | 2.14 | 4.07 | 0.53 |
| steps | 4106 | 2000 | 2.05 |
| sleep_dur (h) | 1.41 | 0.80 | 1.76 |
| sleep_reg (index) | 14.47 | 7.94 | 1.82 |

## Findings
- Only 49 of 71 people reached a ready personal baseline (28 valid nights) within their follow-up (median 87 days); 48% of nights have a recorded main sleep and nocturnal HR/HRV exist on 33% of days.
- Real weekly deviation is about twice as noisy as simulated (dev SD 0.52 vs 0.25), mainly because real day-to-day variability is 1.5-2x higher for night HR, steps and sleep.
- Evaluable weeks: 25% (real) vs 72% (simulated); abstention 23% vs 11%.
- Zero warnings over 8.3 person-years (95% upper bound on the false-alarm rate: 3.0/8.3 = 0.36 per person-year), but mostly because sparse data kept the persistence rule from firing: the system abstained rather than alarmed. This is the designed behaviour, not proof of specificity.

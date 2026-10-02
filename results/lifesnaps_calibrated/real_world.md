# Real-world transfer test: LifeSnaps vs synthetic non-converters

Model and thresholds trained on synthetic data (n=1200, days=540, seed=0); context and population
prior refitted on LifeSnaps (label-free). LifeSnaps has no BP labels: all participants count as non-converters.

| metric | synthetic non-converters | LifeSnaps |
|---|---|---|
| people | 200.000 | 49.000 |
| person_years | 273.522 | 8.318 |
| valid_day_share | 0.674 | 0.665 |
| cover_night_rhr | 0.642 | 0.576 |
| cover_night_rmssd | 0.642 | 0.576 |
| cover_still_hr | 0.642 | 0.822 |
| cover_steps | 1.000 | 0.996 |
| cover_sleep_dur | 1.000 | 1.000 |
| cover_sleep_reg | 1.000 | 0.889 |
| evaluable_week_share | 0.708 | 0.246 |
| dev_sd | 0.368 | 0.522 |
| abstention_rate | 0.114 | 0.233 |
| watch_episodes_py | 1.492 | 0.842 |
| warning_episodes_py | 0.508 | 0.000 |
| people_warned | 0.380 | 0.000 |

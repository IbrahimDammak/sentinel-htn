# Plasmode injection: the same drift in real vs simulated noise (Detect level)

Each person is scored twice: untouched, and with a latent SBP drift of U(12, 22) mmHg ramped over 28 days from 14 days after their baseline is ready (simulator couplings, e.g. +0.15 bpm night HR per mmHg; 20 random drift sizes per person). Detected = the persistence ("watch") tier fires after onset at the synthetic-trained threshold 0.15; false = it fires after the same day without drift. Label-free parts (context, prior, channel weights) are refitted on each cohort. Simulated people are non-converters cut to LifeSnaps follow-up lengths. People need >= 6 weeks after onset. The ramp is compressed because LifeSnaps covers ~4 months: absolute rates are not comparable to the paper's 26-week task, only the rows to each other.

| noise | people | detected after onset | false (no drift) | median lag (days) | post-onset weeks |
|---|---|---|---|---|---|
| real (plasmode) | 18 | 0.31 ± 0.03 | 0.06 | 26 | 9.4 |
| simulated, AR(1) noise | 276 | 0.77 ± 0.01 | 0.24 | 39 | 11.1 |
| simulated, transplanted noise | 276 | 0.73 ± 0.01 | 0.31 | 42 | 11.1 |

± = SD over the random drift sizes (same people), not a confidence interval.

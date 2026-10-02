# Panel: hardware engineer, one wrist strap for SENTINEL-HTN

**IC** = INDUSTRY-CLAIM (vendor/distributor figure, URL given, checked 2026-09-29). **EST** = my estimate, unmeasured.

**Bottom line.** MAX86176 + nRF52840 holds. The 151–301 µA budget assumed an always-on 50–100 µA MCU. With no inference on the strap and windowed PPG: **~42 µA typical, ~91 µA worst (EST)**. Claim 30 days until measured. New supply risk: DigiKey lists the MAX86176ENX+ as **discontinued, 0 stock**.

## 1. Block diagram

```
 skin side                                   top side
 green LED x2 + PD x2 ──┐                    ECG E2 (316L, finger touch)
 ECG E1 (316L back) ─R+TVS─┤                     │ R+TVS
                        ▼                        ▼
             MAX86176  PPG + 1-lead ECG AFE ◄────┘
                        │ SPI
 LIS2DH12 ──SPI──► nRF52840 module ◄──I2C── TMP117 (bonded under E1)
                        ├─QSPI─ MX25R6435F 8 MB (raw log, optional)
                        └─BLE──► phone app ──► cloud model
 pogo 5 V ─ BQ25120A (charger, 1.8 V buck, NTC) ─ LiPo 100–150 mAh + PCM ─ VBAT ─► AFE LED supply
```

## 2. BOM (custom PCB v1)

| Part | Function | @1 | @1k | Source |
|---|---|---|---|---|
| MAX86176ENX+ | PPG + ECG AFE | $14.36 (team figure; 0 stock) | $9.88 (@100) | IC: https://www.digikey.com/en/products/detail/analog-devices-inc-maxim-integrated/MAX86176ENX/19530761 |
| nRF52840 | MCU + BLE | bare chip $7.28; certified module (e.g. Raytac MDBT50Q) $12 EST | module $8 EST | IC: https://www.digikey.com/en/products/result?keywords=NRF52840-QIAA-R |
| BQ25120A | charger, buck, LDO (Iq 700 nA, ship <50 nA) | $2.60 EST | $1.30 EST | specs IC: https://www.ti.com/product/BQ25120A |
| LIS2DH12TR | accelerometer | $1.90 | $0.90 | EST |
| TMP117 | skin temperature | $3.50 | $1.60 | EST |
| MX25R6435F | 8 MB flash | $1.70 | $1.00 | EST |
| 2 green LEDs, 2 PDs, barrier | optics | $5 | $2 | EST |
| 2× 316L electrodes | ECG and thermal contact | $3 | $0.60 | EST |
| Passives, TVS, button, pogo pins | misc | $5 | $1.50 | EST |
| 4-layer PCB + assembly | board | $40 | $4 | EST |
| LiPo 100–150 mAh + PCM, IEC 62133-2 | battery | $6 | $2 | EST |
| Enclosure (SLA print / moulded PC) | housing | $20 | $3 + ~$8 tooling | EST |
| Silicone strap + pogo cradle | wear, charging | $13 | $3 | EST |
| **Total** | | **~$128** | **~$39 (~$47 with tooling)** | |

Certification testing (tens of thousands of dollars) outweighs the BOM at 1k. Confirm the MAX86176 lifecycle with ADI before layout (analog.com was unreachable) and qualify a second source.

## 3. Power budget (24-h average at battery)

Assumptions: 8 h night, 3.7 V LiPo, LEDs on VBAT, 80% of nominal capacity usable. Worst = dark skin/high BMI (LED ×3), 1 s advertising, untuned firmware.

| Consumer | Duty cycle | Typ µA | Worst µA |
|---|---|---|---|
| nRF52840 idle (RTC, RAM kept) + BQ25120A | 100% | 4 | 6 |
| LIS2DH12, 25 Hz, FIFO | 100% | 6 | 6 |
| MCU: FIFO reads, steps, activity counts | 0.3 ms per 1.2 s | 1.5 | 3 |
| Night PPG, 64 Hz, 20 mA LED (60 worst), AFE; **feature extraction** (beats, window SQI, HR, RMSSD) | 5 min every 15 min = 11% | 17 | 50 |
| Day still-HR, 60 s at 25 Hz | ~16 min/day | 1 | 2 |
| ECG spot, 30 s | 1/day | 0.3 | 0.5 |
| Nightly aggregates + actigraphy sleep | ~10 ms/day | <0.1 | <0.1 |
| **ML inference** | **not on strap** | **0** | **0** |
| TMP117 one-shot, flash writes | 1/min | 0.8 | 1.3 |
| **BLE sync**: advertising at 2 s (1 s worst), ~5 KB/day (+15 KB per ECG) | | 6 | 12 |
| Leakage, dividers, firmware slack | | 5 | 10 |
| **Total** | | **~42** | **~91** |

| Nominal (usable) | 42 µA | 91 µA |
|---|---|---|
| 100 mAh (80) | 79 d | 37 d |
| 150 mAh (120) | 119 d | 55 d |

- **Not on the strap:** ML inference, BP estimates, baseline/CUSUM/risk, ECG rhythm classification, multi-day sleep regularity, frequency-domain HRV, continuous daytime HR. The audited inference (47.65 mJ/min) alone is 215 µA, five times this budget.
- Continuous night PPG instead of windows adds +34 µA typical, +92 µA worst.
- **Choose 100 mAh:** thinner strap, still more than a month.

## 4. Firmware duties

**Sampling:**
- Accel at 25 Hz, always on.
- Night: in the sleep period (21:00–09:00), a 5-min PPG window at 64 Hz every 15 min. A window that starts with motion is retried once. LED AGC runs at window start, and the LED current is logged as a skin/fit proxy.
- Day: a 60-s still-HR spot after 3 min without motion, at most one every 30 min.
- ECG: 30 s at ~250 sps, started from the app or the button.

**SQI per window (rule-based):**
1. Accel SD below 0.02 g.
2. DC in range (not saturated, not off-wrist).
3. Perfusion index above a floor.
4. Beat-to-template correlation of at least 0.8.
5. RR within 35–120 bpm, with successive change below 20%.

The window is good if at least 80% of its beats are valid.

**CONTRACT mapping:**

| Column | Computed by |
|---|---|
| `night_rhr`, `night_rmssd` | strap: median over good windows (RR from interpolated peaks, ectopics removed) |
| `still_hr`, `steps` | strap: median of spots; daily count |
| `sleep_dur` | strap: actigraphy (van Hees-style) |
| `sleep_reg` | phone: multi-day, from strap onset/offset |
| `sqi` | strap: good ÷ scheduled windows in the sleep period |
| `rhythm_irregular` | phone: ECG spot irregular OR strap PPG-irregularity flag (a false positive only costs a valid day) |
| `exercise_min` | strap: vigorous minutes, 17:00 to sleep onset |
| `firmware` | strap: **DSP-algorithm version** only; build ID separate, so bug-fix builds don't force re-baselining |
| `ambient_temp`, context, `sbp`/`dbp` | phone: weather API, self-report, BLE cuff |

**Sync:**
- After waking: advertise at 1 s for 2 h; retry 19:00–22:00; otherwise every 2 s (ECG checks, signed MCUboot DFU).
- The phone pulls records after its last acknowledged sequence number, acknowledges them and sets the clock.

**Storage:**
- Per day: ~3.5 KB (minute counts, 32 window records, summary), plus 15 KB per ECG.
- CRC'd ring buffer, deleted only after acknowledgement; internal flash holds more than 30 days offline.
- Validation builds keep raw PPG (~1.8 MB/night) on external flash.

## 5. Build plan

**4-week demo (own firmware):**
- Per strap:
  - Seeed XIAO nRF52840 Sense (nRF52840, IMU, charger, 2 MB flash) ~$16
  - MAX30101 PPG breakout ~$20
  - AD8232 ECG breakout ~$20 (touch electrodes)
  - LiPo $6
  - Strap and printed case $10
  - Subtotal ≈ $72 (all EST)
- Shared:
  - Nordic PPK2 ~$99
  - Polar H10 ~$90 (RR reference)
  - USB isolator ~$35
- Two straps come to **≈$370**.

Optional: one MAX86176EVSYS# (₹11,787.59 ≈ $134, my conversion; IC: https://www.digikey.hu/en/products/detail/analog-devices-inc-maxim-integrated/MAX86176EVSYS/17878678) to run the same C feature code on target-AFE data. The ProtoCentral MAX86150 PPG+ECG breakout is retired (IC: https://protocentral.com/product/protocentral-max86150-ppg-and-ecg-breakout-with-qwiic-v2/); the MAXREFDES104# wrist platform (~$400, IC: https://embeddedcomputing.com/application/consumer/smartphones-and-wearables/product-of-the-week-maxim-integrateds-health-sensor-platform-3-0-maxrefdes104) is too expensive.

**Weekly plan:**
- Week 1: accel, steps, sleep, flash, BLE to a laptop (Python `bleak`, no phone app).
- Week 2: PPG windows, SQI, RMSSD; replay recorded raw PPG through the C code and compare it with the Python reference.
- Week 3: ECG spot check; 3–5 nights per member against the H10; PPK2 current.
- Week 4: daily CSV into `run.py`.

**What the demo can show:**
- The strap → CSV → SENTINEL chain.
- Bland–Altman RHR/RMSSD against the H10 on a few people.
- The measured µA.
- An ECG strip.

**What it cannot show:** a hypertension prediction (that needs months and a cohort), accuracy across skin tones, or regulatory readiness.

**Custom PCB (8–12 weeks later):** the BOM above with a pre-certified module.

## 6. Wearability risks

| Risk | Mitigation |
|---|---|
| Motion | Sample at night and when still; motion gate and retry; bad windows become POOR_QUALITY, never values |
| Skin tone | Wide LED AGC, two PDs, IR at night; log LED current and PI; budget ×3 LED; recruit across ITA and report SQI per tercile |
| Strap fit | 0.3–0.5 mm domed window; fine-pitch holes; wear above the ulnar styloid; fit coaching from DC/PI |
| Sweat | Sealed housing; 316L/Ti electrodes (EN 1811 nickel); no ENIG pads touching skin |
| Charging gaps | Monthly daytime charging; reminder below 20%; offline buffer; charge nights logged as missing (MNAR) |

## 7. Regulatory and safety

- **IEC 60601-1:** internally powered, type BF applied parts; DC patient leakage ≤10 µA normal condition (ECG electrodes); contact surfaces ≤43 °C beyond 10 min. **No measurement while charging** (mechanical interlock + firmware VBUS inhibit). Home use adds IEC 60601-1-11.
- **IEC 60601-1-2 (EMC):** ESD ±8 kV contact and ±15 kV air, plus home RF immunity. Use TVS on the electrodes and a pre-certified radio module.
- **ISO 10993:** intact skin, long-term: cytotoxicity (-5), sensitisation (-10), irritation (-23); use medical silicone and 316L.
- **IEC 62133-2 + UN 38.3:** certified cells, PCM, NTC/JEITA, charge ≤0.5C.

**A student prototype must still keep:**
- No mains path to a wearer: use a laptop on battery or a USB isolator while the electrodes are touched.
- Only protected cells, charged in a LiPo bag.
- Known skin-contact materials.
- Consent and INPDP data protection.
- No diagnostic claims.

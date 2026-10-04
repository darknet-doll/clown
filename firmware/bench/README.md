# Bench rig — full rewire

One breadboard layout for every bench test: trigger, LED strip through the
74AHCT125, and the motor. Follow [bench-wiring.png](bench-wiring.png) — every
numbered wire or part there is one step below, in the same order.

- **Rows 1–30 only.** Long breadboards often split their rails partway down
- **Match rails by colour**, not position: **red +** and **blue −**
- **XIAO rows:** the drawing assumes the XIAO's pins land in columns c and h.
  If yours land elsewhere, use any free hole *in the same row, outside the XIAO*
- Regenerate the drawing with `python3 firmware/bench/bench_wiring.py`

## What's different from last time

- **Motor current stays in its own rows.** Cell −, Q1 source and R5 all meet in
  row 22. One jumper (#25) is that row's only link to the ground rail, so motor
  current never flows through the chip's ground
- **Both ground rails go straight to the XIAO's GND pin** (#2, #3). No rail-to-rail
  bridge
- **Left red rail is unused.** Nothing goes in it
- **C2, the 0.1 µF ceramic, is in.** The electrolytic stand-in comes out
- **The pin-5 pulldown** goes into the chip's own ground row (#15), not to a rail

## Strip the board

Everything out: XIAO, chip, every jumper and part. USB and cell unplugged.

## Steps

Nothing is powered until the **Power-up** section.

### Place the two chips
- **XIAO (U3):** rows 1–7, straddling the gap, USB-C off the top
- **74AHCT125 (U2):** rows 10–16, legs in e and f, **notch toward row 10**

### Power and ground — straight from the XIAO's own pins
| # | From | To |
|---|---|---|
| 1 | XIAO **5V** row (i1) | **red +** rail, right |
| 2 | XIAO **GND** row (i2) | **blue −** rail, right |
| 3 | XIAO **GND** row (j2) | **blue −** rail, left — arc it over the XIAO |

### Chip tie-offs
| # | From | To | Chip pin |
|---|---|---|---|
| 4 | a10 | blue − left | 1 (1OE) |
| 5 | a13 | blue − left | 4 (2OE) |
| 6 | a16 | blue − left | 7 (GND) |
| 7 | i10 | red + right | 14 (Vcc) |
| 8 | **C2 0.1 µF**: j10 | blue − right, beside it | 14 → ground. Short legs |
| 9 | j11 | red + right | 13 (4OE) |
| 10 | j12 | blue − right | 12 (4A) |
| 11 | j14 | red + right | 10 (3OE) |
| 12 | j15 | blue − right | 9 (3A) |

**Chip pins 8 and 11 stay empty.**

### Signals from the XIAO
| # | From | To | |
|---|---|---|---|
| 13 | XIAO **D10** row (j4) | d11 | chip pin 2 (1A) |
| 14 | XIAO **D2** row (a3) | a14 | chip pin 5 (2A) |
| 15 | **10 kΩ**: d14 | d16 | pin 5 → pin 7's ground row |

### Trigger
| # | From | To |
|---|---|---|
| 16 | switch **NO** | a2 (XIAO **D1** row) |
| 17 | switch **COM** | blue − left |

### Strip
| # | From | To | |
|---|---|---|---|
| 18 | **R3 330 Ω**: b12 | b18 | chip pin 3 → DIN row |
| 19 | jumper d18 | g18 | across the gap |
| 20 | strip **DIN** | j18 | input end — arrows point away |
| 21 | strip **5V** | red + right | |
| 22 | strip **GND** | blue − right | |

### Motor side (cell still disconnected)
| # | From | To | |
|---|---|---|---|
| — | **Q1 RFP30N06LE** | d20 / d21 / d22 | printed face toward the **left** edge → G in row 20 |
| 23 | **R4 100 Ω**: c15 | c20 | chip pin 6 → gate |
| 24 | **R5 10 kΩ**: b20 | b22 | gate → source |
| 25 | jumper a22 | blue − left | **row 22's only link to ground** |
| 26 | **CR1 1N5819**: c21 | c25 | **band (stripe) in row 25** |
| 27 | **F1 GBX-185**: b25 | b27 | |
| 28 | motor **−** | a21 | |
| 29 | motor **+** | a25 | |

### Cell — not yet. Steps 30–31 are in Power-up.

## Check before any power (meter, ohms / continuity)

| Between | Expect |
|---|---|
| Chip **leg 7** ↔ XIAO **GND pin** | beep, and **< 1 Ω** on the ohms range |
| Chip **leg 14** ↔ XIAO **5V pin** | beep |
| Chip **leg 1**, **leg 4** ↔ XIAO GND pin | beep |
| Row 27 or row 25 ↔ either red rail | **no** beep |
| Row 25 ↔ any blue rail | **no** beep |
| d20 (gate) ↔ d22 (source) | ~10 kΩ |
| d20 (gate) ↔ d21 (drain) | open |

## Power-up, one stage at a time

### Stage 1 — USB only, `pin_probe`
Black probe on the **XIAO's GND pin**, D10 set to `1`:

| Red probe on | Expect |
|---|---|
| Chip leg 7 | **< 20 mV** — this is the fault from last time |
| Chip leg 14 | ~5 V |
| Chip leg 2 | ~3.3 V |
| Chip leg 3 | ~5 V |

Type `0`: leg 3 drops to ~0 V. **Don't continue until leg 7 is under 20 mV.**

### Stage 2 — USB only, `strip_test`
- Boot flash red → green → blue; squeeze → comets
- Re-check leg 7 against the XIAO GND pin while comets run: still < 20 mV

### Stage 3 — cell connected, `motor_test`
1. Upload `motor_test` with the cell still off. Strip should boot normally
2. **30:** cell **−** → e22
3. **31:** cell **+** → a27
4. Squeeze: blower spins, comets run. Release: both stop
5. Hold the trigger and re-check leg 7 against XIAO GND: **< 50 mV** with the
   motor running

**Off:** cell **+** first, then cell −, then USB.

## If something's wrong

| Symptom | Look at |
|---|---|
| Leg 7 more than 20 mV from XIAO GND | jumpers 3 and 6, and their rail holes. Swap the jumper, try fresh holes |
| Strip dark, leg 3 follows `0`/`1` | R3 seating, jumper 19, strip end |
| Leg 3 doesn't follow | chip pin 1 tie (#4), chip power (#7), C2 not shorting 5V |
| Blower never runs | D2 jumper (#14), Q1 orientation, F1 seated, cell charged |
| Blower runs constantly | Q1 legs swapped, or 2A not reaching pin 5 |
| Chip warm | unplug. An output (pin 3, 6, 8, 11) is tied to something it shouldn't be |
| XIAO resets when the motor starts | jumper 25 / row 22, then cell charge |

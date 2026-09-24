# Schematic

The electrical drawing for **one arm**. The other arm is identical — same parts,
same pinout, same firmware.

Two sheets, both generated from [docs/schematic/schematic.py](docs/schematic/schematic.py):

- **Sheet 1 — schematic.** The pod electronics, the motor drive, the trigger
- **Sheet 2 — harness.** Which net rides which pin, and where each module unplugs

Prose for the same information lives in [BUILD.md](BUILD.md) step 4 (pod) and
[PARTS.md](PARTS.md) (why each part is there). This file is the reference drawing —
if the two ever disagree, the drawing is what got reviewed.

---

## Sheet 1 — schematic

![One-arm schematic](docs/schematic/clown-arm-schematic.svg)

How to read it:

- **Pink flags** are net labels. A wire ending in `GATE` continues at the other
  flag marked `GATE`. It is the same wire; it is drawn twice so the sheet stays
  readable
- **Ground symbols** are all one net. There is exactly one ground in this design
- Rails are labelled on the line: `VBATT` is the cell after the disconnect and the
  fuse, `+5 V` is the boost output

### The four things on this sheet that the earlier docs did not have

| # | What | Why |
|---|---|---|
| **SW1** | Master disconnect in the cell positive, ahead of the fuse | Kills the pack in one motion, without fishing a plug out of a sealed pod |
| **D2** | 1N5819 between the boost output and the XIAO 5V pad | The XIAO's 5V pad is tied straight to USB VBUS. Without D2, a connected pack backfeeds the host port the moment you plug in to reflash |
| **R5** | 10 kΩ gate-to-source pulldown on Q1 | Between reset and `setup()`, `D2` floats. R5 is the only thing holding the blower off. If you bought a module, confirm it has one; most do not |
| **R4** | 100 Ω gate series resistor | Limits the gate-charging current spike out of the level shifter |

`D2` costs about 0.3 V, so the XIAO sees ~4.7 V — comfortably inside its regulator.
**The strip is fed from the boost directly, not through D2.** Only the MCU sits
behind the diode, so the strip keeps a full 5 V.

### The unused half of U2

The build uses two of the 74AHCT125's four gates. **The other two are not "spare",
they are inputs that must not float.** A floating CMOS input drifts around the
switching threshold, so the gate oscillates, and the chip draws far more current
than its datasheet promises — tens of milliamps instead of microamps, as heat,
forever, off a battery you are wearing.

| Pin | Tie to | Why |
|---|---|---|
| `3A`, `4A` | **GND** | Inputs. A defined level, either rail would do; ground is the convention |
| `3OE`, `4OE` | **Vcc** | Also inputs, and OE is active-low — high disables the output |
| `3Y`, `4Y` | **nothing** | Outputs. Leave them open. Never tie an output to a rail |

- `1OE` and `2OE` go to **GND**, which is what enables the two gates we do use
- Disabling the unused outputs rather than enabling them into open air is the
  conventional choice, and it means a stray probe on `3Y`/`4Y` can't fight anything

On the DIP-14 part the pins are `1OE` 1, `1A` 2, `1Y` 3, `2OE` 4, `2A` 5, `2Y` 6,
`GND` 7, `3Y` 8, `3A` 9, `3OE` 10, `4Y` 11, `4A` 12, `4OE` 13, `Vcc` 14 — **check
it against the datasheet for the package you actually bought**; a breakout board
renumbers everything.

---

## Sheet 2 — harness

![One-arm harness](docs/schematic/clown-arm-harness.svg)

- The four module boundaries are the dashed boxes. Every one of them unplugs
- `J2-6` (the second ground) terminates in the sleeve, on the strip's ground. It
  exists to halve the drop on the longest run in the costume, not to reach the hand
- The motor pair crosses the sleeve untouched — it is deliberately not bundled with
  the data line

---

<!-- generated:nets -->

### Nets

| Net | What it is | Everything on it |
|---|---|---|
| `VBATT` | Cell positive, after SW1 and F1 | BT1+ · J1-1 · SW1 · F1 · U1 IN+ · R1 · J3-1 (motor +) |
| `GND` | The one common ground. Everything returns here | BT1− · J1-2 · U1 IN−/OUT− · U3 GND · U2 GND · U2 1OE · U2 2OE · U2 3A · U2 4A · Q1 source · C1− · R2 · J2-2 · J2-6 · SW2 COM |
| `+5V` | Boost output. Strip, level shifter, and D2's anode | U1 OUT+ · U2 Vcc · U2 3OE · U2 4OE · C1+ · D2 anode · J2-1 (strip +5V) |
| `+5V_MCU` | Same 5 V, one Schottky drop down, MCU only | D2 cathode · U3 5V pad |
| `VSENSE` | Half of VBATT, for the ADC | R1 · R2 · U3 D0 (GPIO2) |
| `LED_DATA_3V3` | MCU-level data, level shifter input | U3 D10 (GPIO10) · U2 1A |
| `LED_DATA` | 5 V data, through the series resistor | U2 1Y · R3 · J2-3 · LD1 DIN |
| `GATE_3V3` | MCU-level motor PWM, level shifter input | U3 D2 (GPIO4) · U2 2A |
| `GATE` | 5 V gate drive. R5 holds it down while the MCU boots | U2 2Y · R4 · R5 · Q1 gate |
| `TRIG` | Trigger, idle high on the MCU's internal pull-up | U3 D1 (GPIO3) · J2-4 · J4-4 · J6-1 · SW2 NO |
| `MOTOR+` | Blower positive, straight off the cell | VBATT · J3-1 · J5-1 · D1 cathode · M1+ |
| `MOTOR-` | Blower negative, switched by the MOSFET | Q1 drain · J3-2 · J5-2 · D1 anode · M1− |

### Designators

| Ref | Part |
|---|---|
| `BT1` | Protected 18650, on its factory PH2.0 lead |
| `J1` | JST-PH 2.0 2-pin — cell to pod, and cell to charger |
| `SW1` | Master disconnect, in the cell positive |
| `F1` | 2 A PPTC resettable fuse |
| `U1` | MT3608 boost module, trimmed to 5.00 V |
| `D2` | 1N5819 — USB isolation, cathode to the XIAO 5V pad |
| `C1` | 1000 uF electrolytic, at the elbow connector |
| `R1, R2` | 100 k / 100 k battery-sense divider |
| `U3` | Seeed XIAO ESP32-C3 |
| `U2` | 74AHCT125 — gate 1 for LED data, gate 2 for the MOSFET gate, gates 3 and 4 tied off |
| `R3` | 330-470 R series resistor on the LED data line |
| `R4` | 100 R gate series resistor |
| `R5` | 10 k gate-to-source pulldown |
| `Q1` | N-channel logic-level MOSFET (AO3400 / IRLZ44N / RFP30N06LE) |
| `D1` | 1N5819 flyback, across the motor, at the blower end |
| `M1` | Bubble kit blower motor |
| `SW2` | Lever microswitch, in the palm |
| `J2` | JST-SM 6-pin — elbow |
| `J3` | JST-SM 2-pin — elbow, motor |
| `J4` | JST-SM 5-pin — wrist |
| `J5` | JST-SM 2-pin — wrist, motor |
| `J6` | JST-ZH 1.5 mm 2-pin — at the microswitch |
| `LD1` | WS2812B, 21 px: forearm 15 + hand 6 |

<!-- /generated:nets -->

---

## Regenerating

Both SVGs and the net table above are generated. Edit the script, never the SVGs:

```
python3 docs/schematic/schematic.py
```

No dependencies — it writes SVG text directly. The net table is rewritten in place
between the `generated:nets` markers, so the drawing and the table cannot drift.

---

## What is deliberately not here

- **Mechanical.** Enclosure, gasketing, strap and sealing detail are
  [BUILD.md](BUILD.md) step 11
- **Firmware thresholds.** The low-battery warning and the low-voltage shutoff are
  in `firmware/clown_arm/clown_arm.ino`, in the tunables block
- **Layout.** There is no PCB. The pod is protoboard; sheet 1 is the circuit, not a
  placement

## Review checklist

If you are the engineer reading this, these are the things worth checking hardest:

- [ ] `D2` orientation — cathode to the XIAO. Backwards, the board never powers
- [ ] `D1` orientation — banded end to motor **+**. Backwards it is a dead short
      across the cell through the MOSFET
- [ ] `C1` polarity — stripe to ground
- [ ] `R5` present, and actually across gate–source rather than gate–ground on a
      module with a separate source pin
- [ ] `F1` ahead of everything, including `U1` and the motor tap
- [ ] The boost trimpot set to 5.00 V **before** the XIAO is connected
- [ ] `U2` `1OE`/`2OE` tied to ground, not left floating
- [ ] `U2` `3A`/`4A` to ground and `3OE`/`4OE` to Vcc — no unused input floating,
      and `3Y`/`4Y` left open rather than tied

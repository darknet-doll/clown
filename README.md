# clown

A bubble-shooting clown costume. Make a gun shape with either hand, squeeze your
remaining fingers into your palm, and a comet of light runs from your elbow down
to your fingertips — arriving exactly as a stream of bubbles starts firing out of
your fingers.

Two arms, two identical rigs.

---

## Sequence

1. **Squeeze.** Microswitch in the palm closes.
2. **Motor kicks.** Blower gets a brief over-drive pulse to break static friction,
   then settles to its run speed.
3. **Comet launches** from the elbow pixel and travels toward the fingertips.
4. **~250 ms later** the comet lands at the fingertips and the blower has reached
   full speed — bubbles start. The light travel *is* the spin-up delay, so it
   reads as causal instead of as lag.
5. **Hold** to keep streaming; comets keep launching on a loop.
6. **Release.** Motor cuts, fingertips flare white and fade out.

---

## Why two independent arms

Each arm is a self-contained module: its own controller, power bank, strip,
blower, and trigger. Nothing crosses the torso.

- No wire harness over the shoulders or back — nothing to snag, nothing to
  unplug when you take the costume off one sleeve at a time.
- If one arm dies mid-event, the other keeps working.
- **The firmware is byte-identical on both.** As long as pixel 0 is at the elbow
  on each arm, there's no handedness in the code — flash the same binary twice.

The tradeoff is buying two of everything, including two bubble maker kits. That's
unavoidable regardless: you need one blower per hand.

*Later option:* the XIAO ESP32-C3 has ESP-NOW, so a single trigger could fire both
arms in sync. Not in v1 — get one arm working end to end first.

---

## Bill of materials

Quantities below are **per arm**. Double everything.

| Part | Qty | Notes |
|---|---|---|
| Bambu Lab Electric Bubble Maker Kit 01 (P6M) | 1 | Blower + one-way-valve cap |
| WS2812B strip, 60 LED/m, 5V, black FPC, IP65 | ~0.4 m | IP65 is not optional — you are spraying soap down your own arm |
| Seeed XIAO ESP32-C3 | 1 | 5V in via USB-C, 3.3V logic |
| 74AHCT125 level shifter | 1 | 3.3V data -> 5V strip. **Do not skip this** |
| N-channel logic-level MOSFET module (AO3400 / IRLZ44N) | 1 | Switches the blower |
| 1N5819 flyback diode | 1 | Across the motor — it's inductive |
| 1000 µF electrolytic capacitor | 1 | Across the strip's 5V/GND |
| 330–470 Ω resistor | 1 | In series on the strip data line |
| Snap-action microswitch (lever type) | 1 | The palm trigger |
| USB power bank, 5V 2A+ | 1 | Powers everything |
| Silicone hookup wire, 22–26 AWG | — | Flexible. Not solid-core |

Printed parts: palm trigger plate, forearm strip channel, upper-arm controller
and power bank pod. The bubble kit itself has a pile of MakerWorld mounts to
start from.

---

## Power

Everything runs from one 5V bus per arm, fed by the power bank.

### The blower is a 3.7V motor

The "5V 2A" on the kit's spec sheet is the **USB charger**, not the motor. The P6M
blower runs off a single 18650 at 3.7 V nominal. Wiring it straight to 5 V is ~35%
over-voltage — loud, hot, and short-lived.

Instead it's driven through the MOSFET with **PWM capped at ~72% duty**, which
averages to roughly 3.7 V. PWM frequency is set to 20 kHz so the motor doesn't
whine in the audible band. Brief kickstart pulses above the cap are fine and
intentional.

The 18650 and its charger that ship with the kit are unused in this build.

### Power bank auto-shutoff

Many power banks cut out when draw falls below ~50–100 mA. Two defenses:

- Buy one with an "always on" / low-current / trickle mode, **or**
- The idle breathing animation is tuned to keep draw above the threshold. Don't
  turn `IDLE_BRIGHTNESS` down to zero to save battery — that's what kills the bank.

### Budget per arm

| Load | Draw |
|---|---|
| 21 px WS2812B, full white, 100% | ~1.26 A (never happens) |
| Comet at 50% brightness cap, ~8 px lit | ~0.25 A |
| Blower at run duty | ~0.5–1.0 A |
| **Realistic peak** | **~1.3 A** |

A 2 A bank is comfortable. A 3 A bank gives headroom for the kickstart pulse.

---

## Strip layout

**Split the strip at the wrist.** A continuous strip across a flexing wrist will
crack its traces within a few hours of wear.

```
  elbow                          wrist                fingertips
   |------- forearm, 15 px -------|  gap  |-- hand, 6 px --|
   px 0                        px 14      px 15         px 20
                              ~4 cm flexible silicone jumper
```

- Forearm segment: ~25 cm, 15 pixels, pixel 0 at the elbow.
- Wrist jumper: ~4 cm of flexible silicone wire, three conductors, with a service
  loop so it isn't under tension at full wrist extension.
- Hand segment: ~10 cm, 6 pixels, across the back of the hand to the knuckles.

Data chains straight through, so it's one logical 21-pixel strip in code.

The firmware knows about the physical gap and treats it as ~2 pixels of *virtual*
distance, so the comet's apparent speed stays constant as it crosses the wrist
instead of appearing to jump.

Measure your own arm and adjust `FOREARM_PX` / `HAND_PX` / `GAP_PX` to match.

---

## Wiring

Per arm, XIAO ESP32-C3:

| Signal | XIAO pin | GPIO | To |
|---|---|---|---|
| LED data | D10 | 10 | 74AHCT125 input, then 330–470 Ω, then strip DIN |
| Trigger | D1 | 3 | Microswitch to GND (internal pull-up, active low) |
| Motor PWM | D2 | 4 | MOSFET module gate input |
| 5V | 5V pad | — | Power bank, strip 5V, 74AHCT125 Vcc, motor + |
| GND | GND | — | Common ground for everything |

Avoid D8 / D9 (GPIO8 / GPIO9) — they're boot strapping pins.

Notes:

- The 1000 µF cap goes across the strip's 5V/GND, physically close to the strip.
- The 330–470 Ω resistor goes in series on the data line, close to the first pixel.
- The 1N5819 goes across the motor terminals, cathode to +.
- Common ground is mandatory — the level shifter, strip, MOSFET, and MCU all share it.

---

## Firmware

`firmware/clown_arm/clown_arm.ino` — Arduino sketch, FastLED, ESP32 Arduino core 3.x.

Flash the same sketch to both arms, unchanged.

Tunables live in one block at the top:

| Constant | Default | What it does |
|---|---|---|
| `FOREARM_PX` / `HAND_PX` / `GAP_PX` | 15 / 6 / 2 | Physical layout |
| `COMET_TRAVEL_MS` | 250 | Elbow to fingertip, must match blower spin-up |
| `COMET_REPEAT_MS` | 320 | Gap between comets while held |
| `MAX_BRIGHTNESS` | 128 | Global cap, protects the power budget |
| `MOTOR_RUN_DUTY` | 184 | ~72% of 255 — the 3.7 V average |
| `MOTOR_KICK_DUTY` | 235 | Kickstart pulse |
| `MOTOR_KICK_MS` | 80 | Kickstart duration |
| `THEME_HUE` | 192 | Comet color |
| `IDLE_BRIGHTNESS` | 24 | Also the power bank keepalive — don't zero it |

Tune `COMET_TRAVEL_MS` last, on the assembled arm: film it in slow motion and
adjust until the first bubble leaves your fingers on the same frame the comet
lands.

---

## Field notes

- **Soap gets everywhere.** IP65 strip, sealed strip ends, and keep the controller
  pod on the *upper* arm, above the spray.
- **Test the trigger in the gun pose, not on the bench.** The lever needs to sit
  under your middle and ring finger pads so the squeeze lands every time without
  aiming.
- **Carry spares:** a pre-soldered wrist jumper and a spare microswitch. Those are
  the two parts that will fail during an event.
- Bubble solution consumption is the real runtime limit, not battery.

---

## Status

- [x] Design, BOM, power plan
- [x] Firmware v1
- [ ] Parts ordered
- [ ] One arm assembled and timed
- [ ] Second arm
- [ ] Printed enclosures
- [ ] Optional: ESP-NOW sync between arms

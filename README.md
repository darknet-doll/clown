# clown

A bubble-shooting clown costume. Make a gun shape with either hand, squeeze your
remaining fingers into your palm, and a comet of light runs from your elbow down
to your fingertips — arriving exactly as a stream of bubbles starts firing out of
your fingers.

Two arms, two identical rigs. LED strips hidden under gloves and sleeves, so the
light reads as a glow coming from inside the costume rather than a strip taped to
your arm.

**New here?** → [PARTS.md](PARTS.md) explains every component in plain English.
→ [BUILD.md](BUILD.md) is the step-by-step assembly manual.

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

Each arm is a self-contained module: its own controller, battery, strip, blower,
and trigger. Nothing crosses the torso.

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

## Power

Each arm runs off **one swappable protected 18650**, on a split rail:

```
18650 ─┬─> MOSFET ──> blower motor        (3.7V native)
       └─> 5V boost ──> LED strip + XIAO  (~0.3A)
```

The blower is fed straight from the cell at its native voltage — which is exactly
how Bambu designed the kit. Only the strip and the brain need boosting to 5V, and
that's a light enough load (~0.3 A) that a small inexpensive boost module is
genuinely adequate.

This is simpler than running everything from a single 5 V bus, not harder. On a
5 V rail the motor would need its PWM duty capped to ~72% to fake 3.7 V; fed
direct, it just runs, and PWM becomes purely a bubble-rate control.

Each bubble kit ships with a protected 18650 and a USB charger, so buying two kits
already covers both arms. Buy spare cells to hot-swap.

### Budget per arm

| Load | Draw |
|---|---|
| Comet at default brightness, ~8 px lit | ~0.3 A at 5V |
| Blower at run duty | ~0.5–1.0 A at 3.7V |
| **Realistic peak from the cell** | **~1.3 A** |

A 2600 mAh cell comfortably outlasts a bottle of bubble solution at any realistic
duty cycle. Swappable cells are for convenience, not because runtime is tight —
**you'll be refilling solution long before the battery matters.**

The firmware reads cell voltage through a divider and pulses the elbow pixel red
when it drops below 3.4 V, so you get warning rather than a sudden death.

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

- Forearm segment: ~25 cm, 15 pixels, pixel 0 at the elbow, under a sleeve.
- Wrist jumper: ~4 cm of flexible silicone wire, three conductors, with a service
  loop so it isn't under tension at full wrist extension.
- Hand segment: ~10 cm, 6 pixels, across the back of the hand to the knuckles,
  under the glove.

Data chains straight through, so it's one logical 21-pixel strip in code.

The firmware knows about the physical gap and treats it as ~2 pixels of *virtual*
distance, so the comet's apparent speed stays constant as it crosses the wrist
instead of appearing to jump.

Measure your own arm and adjust `FOREARM_PX` / `HAND_PX` / `GAP_PX` to match.

### Under the glove

Hiding the strip under fabric is a genuine upgrade, not a compromise — the fabric
diffuses the pixels into one smooth continuous streak instead of visible dots.

But it only works if the fabric cooperates:

- **Thin, pale, stretchy** fabric glows beautifully.
- **Thick or dark** fabric, especially leather, swallows almost all of it.

Test a powered strip section under your actual glove in a dark room *before*
committing to it. No firmware setting rescues a glove that eats the light.

`MAX_BRIGHTNESS` is set high (180) to punch through fabric. Route the strip over
the **back** of the hand, never the palm, and sew a fabric channel rather than
gluing the strip down taut — the channel lets it slide as your hand flexes.

Full detail in [BUILD.md](BUILD.md) step 10.

---

## Wiring

Per arm, XIAO ESP32-C3:

| Signal | XIAO pin | GPIO | To |
|---|---|---|---|
| LED data | D10 | 10 | 74AHCT125 input, then 330–470 Ω, then strip DIN |
| Trigger | D1 | 3 | Microswitch to GND (internal pull-up, active low) |
| Motor PWM | D2 | 4 | MOSFET module gate input |
| Battery sense | D0 | 2 | Midpoint of a 100 kΩ / 100 kΩ divider across the cell |
| 5V | 5V pad | — | Boost output, strip 5V, 74AHCT125 Vcc |
| GND | GND | — | Common ground for everything |

Avoid D8 / D9 (GPIO8 / GPIO9) — they're boot strapping pins.

Notes:

- A 2 A polyfuse goes inline at the battery positive, before anything else.
- The 1000 µF cap goes across the strip's 5V/GND, physically close to the strip.
- The 330–470 Ω resistor goes in series on the data line, close to the first pixel.
- The 1N5819 goes across the motor terminals, cathode to +.
- Common ground is mandatory — the level shifter, strip, MOSFET, boost, and MCU
  all share it.

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
| `MAX_BRIGHTNESS` | 180 | Global cap — raised to punch through glove fabric |
| `IDLE_BRIGHTNESS` | 20 | Resting glow; 0 for fully dark |
| `MOTOR_RUN_DUTY` | 230 | Bubble rate |
| `MOTOR_KICK_DUTY` / `MOTOR_KICK_MS` | 255 / 80 | Kickstart pulse |
| `THEME_HUE` | 192 | Comet color |
| `VBAT_WARN_MV` | 3400 | Low-cell warning threshold |

Tune `COMET_TRAVEL_MS` last, on the assembled arm: film it in slow motion and
adjust until the first bubble leaves your fingers on the same frame the comet
lands. See [BUILD.md](BUILD.md) step 9.

---

## Field notes

- **Soap gets everywhere.** IP65 strip, sealed strip ends, and keep the controller
  pod on the *upper* arm, above the spray.
- **Test the trigger in the gun pose, not on the bench.** The lever needs to sit
  under your middle and ring finger pads so the squeeze lands every time without
  aiming.
- **Carry spares:** a charged cell per arm, a pre-soldered wrist jumper, and a
  spare microswitch. Those are what fail during an event.
- **Keep the USB-C port accessible** in the printed pod. You will reflash this
  more often than you expect.

---

## Status

- [x] Design, power plan, wiring
- [x] Parts list with explanations — [PARTS.md](PARTS.md)
- [x] Build manual — [BUILD.md](BUILD.md)
- [x] Firmware v1, incl. low-battery warning
- [ ] Parts ordered
- [ ] Glove fabric light test
- [ ] One arm assembled and timed
- [ ] Second arm
- [ ] Printed enclosures (trigger plate, battery sled, controller pod)
- [ ] Optional: ESP-NOW sync between arms

# clown

A bubble-shooting clown costume. Make a gun shape with either hand, squeeze your
remaining fingers into your palm, and a comet of light runs from your upper arm
down to your fingertips — arriving exactly as a stream of bubbles starts firing out of
your fingers.

Two arms, two identical rigs — **one trigger per hand, each firing its own arm.**
LED strips hidden under gloves and sleeves, so the light reads as a glow coming
from inside the costume rather than a strip taped to your arm.

Each arm comes apart into four modules that unplug from each other, so you can get
out of the costume alone without turning into a pretzel.

**Start here:** [Clown-Build-Manual.pdf](Clown-Build-Manual.pdf) — the printable
manual. Page 1 is every part, numbered, with a plain-English note under each one;
every page after that is assembly steps referring back to those numbers.

Markdown equivalents, if you'd rather read them here:
[PARTS.md](PARTS.md) (parts and what they do) and
[BUILD.md](BUILD.md) (step-by-step assembly).

**Circuit:** [SCHEMATIC.md](SCHEMATIC.md) — two generated sheets, one for the
electronics and one for the harness. That's the drawing to review, and the one to
check your wiring against.

**Costume direction:** [DESIGN.md](DESIGN.md) — the concept board, and the three
places where it changes the build.

---

## Sequence

1. **Squeeze.** Microswitch in the palm closes.
2. **Motor kicks.** Blower gets a brief over-drive pulse to break static friction,
   then settles to its run speed.
3. **Comet launches** from pixel 0 at the pod, high on the upper arm, and travels
   toward the fingertips.
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
- **Each hand has its own trigger**, wired only to its own arm. There is no
  cross-arm wiring anywhere in v1.
- If one arm dies mid-event, the other keeps working.
- **The firmware is byte-identical on both.** As long as pixel 0 is at the pod
  on each arm, there's no handedness in the code — flash the same binary twice.

The tradeoff is buying two of everything, including two bubble maker kits and two
triggers. That's unavoidable regardless: you need one blower per hand.

*Later option:* the XIAO ESP32-C3 has ESP-NOW, so either trigger could **also** fire
the other arm for a two-handed blast. That's **additive** — each hand keeps its own
trigger and its own arm. It is a second way to fire, not a replacement for the
second trigger. Not in v1 — get one arm working end to end first.

---

## Modules and connectors

Nothing is soldered end to end across a joint. Each arm is four modules:

| Module | Holds | Unplugs at |
|---|---|---|
| **Pod** — upper arm | brain, boost, level shifter, MOSFET, fuse, disconnect, cell cradle, upper-arm strip 6 px | `SW1` + battery plug + straps |
| **Sleeve** — forearm | forearm strip, 15 px | elbow: SM 4-pin + SM 3-pin |
| **Glove** — hand | hand strip 6 px, this hand's trigger | wrist: SM 5-pin |
| **Bubbler** | bottle, cap, hose, blower head | wrist: SM 2-pin + its strap |

### The connectors

| Boundary | Carries | Connector |
|---|---|---|
| Cell ↔ pod, cell ↔ charger | 2 | **JST-PH 2.0, 2-pin** *(factory, on the cell)* |
| Pod → upper-arm strip | strip 3 | **JST-SM 3-pin** |
| Strip across the elbow | strip 3 | **JST-SM 3-pin** |
| Pod → sleeve, at the elbow | motor 2 + trigger 2 | **JST-SM 4-pin** |
| Sleeve → glove, at the wrist | strip 3 + trigger 2 | **JST-SM 5-pin** |
| Motor run, at the wrist | motor 2 | **JST-SM 2-pin** |
| Microswitch pigtail | switch 2 | **JST-ZH 1.5 mm, 2-pin** |

The trigger and the motor both have to reach the pod from the hand, so they cross
*both* joints. At the elbow they share one 4-pin lead, while the strip crosses on
its own 3-pin.

### Two rules that keep it safe

**No two connectors on one arm share both family and pin count** — with one
deliberate exception. PH-2 · ZH-2 · SM-2 · SM-3 (×2) · SM-4 · SM-5. The three
2-pin plugs are three different pitches — 2.0, 1.5 and 2.5 mm — so none will mate
with the others.

- **The trigger pigtail is ZH, not PH,** because every cell ships on a PH2.0 lead.
  One wrong plug would put 3.7 V onto GPIO3.
- **The kit's motor lead gets reworked off PH2.0 to SM-2,** because as shipped the
  cell mates straight to the motor, bypassing the MOSFET entirely.
- The two SM-3 strip plugs — at the pod and at the elbow — are identical to each
  other, which is safe *by construction*: same strip nets, same pin order.
  Cross-mating the pod plug onto the forearm input just skips the upper-arm
  segment; nothing is damaged.

**Battery out before you mate or unmate anything.** Feeding data into an unpowered
WS2812 pushes current through its input protection diodes — the classic way to kill
pixel 0.

Full detail in [PARTS.md](PARTS.md) and [BUILD.md](BUILD.md) step 13.

---

## Power

Each arm runs off **one swappable protected 18650**, on a split rail:

```
18650 ─> SW1 ─> 2A fuse ─┬─> MOSFET ──> blower motor          (3.7V native)
                         └─> 5V boost ─┬─> LED strip + shifter (~0.3A)
                                       └─> CR2 ─> XIAO 5V pad
```

**`SW1` is a master disconnect** in the cell positive — one motion, through the
costume, kills the arm without opening the pod. The cell still comes out for
storage and charging; the switch is what makes the pod safe to open and the arm
safe to unplug in a hurry.

**`CR2` is an isolation Schottky.** The XIAO's 5V pad is tied straight to its USB-C
VBUS, so without it, plugging in to reflash with the cell connected puts the boost
output on the host port. The strip and the level shifter stay on the boost
directly at a full 5 V; only the MCU sits behind the diode.

The blower is fed straight from the cell at its native voltage — which is exactly
how Bambu designed the kit. Only the strip and the brain need boosting to 5V, and
that's a light enough load (~0.3 A) that a small inexpensive boost module is
genuinely adequate.

This is simpler than running everything from a single 5 V bus, not harder. On a
5 V rail the motor would need its PWM duty capped to ~72% to fake 3.7 V; fed
direct, it just runs, and PWM becomes purely a bubble-rate control.

Each bubble kit ships with a protected 18650 **already on a PH2.0 pigtail** and a
USB charger that mates to the same plug. Fit the matching half at the pod and a
flat cell goes pod → charger with no adapter.

That pigtail is also why the pod has **no battery sled** — the cell already carries
its own connector, so the pod only needs a printed **cradle** that holds it still
and a lid that opens without a tool. Retention and conduction stay separate jobs.

**Two cells exist, one per arm, and no spares were bought.** A flat cell ends that
arm for the night; recharging between sets is the extension plan.

The kit does **not** include a bottle — the cap fits a 24T/30T neck and you supply
the rest. That's useful: bottle size is your main lever on arm weight.

### Budget per arm

| Load | Draw |
|---|---|
| Comet at default brightness, ~8 px lit | ~0.3 A at 5V |
| Blower at run duty | ~0.5–1.0 A at 3.7V |
| **Realistic peak from the cell** | **~1.3 A** |

A 2600 mAh cell comfortably outlasts a bottle of bubble solution at any realistic
duty cycle. Swappable cells are for convenience, not because runtime is tight —
**you'll be refilling solution long before the battery matters.**

The firmware reads cell voltage through a divider and does two things with it:

- **3.4 V → warning.** The elbow pixel pulses red, slowly, once per beat. There's a
  150 mV band before it clears again, so it doesn't strobe on and off every time
  the motor loads the cell.
- **3.0 V sustained → shutoff.** The motor cuts, the trigger stops working, and
  the elbow pixel double-blinks. It latches until a charged cell turns up.

The cell's own protection board is the backstop, not the plan — repeatedly hauling
an 18650 down to its protection cutoff is what kills it. Both thresholds are
tunable at the top of the sketch.

---

## Strip layout

**Split the strip at the elbow and the wrist.** A continuous strip across a
flexing joint will crack its traces within a few hours of wear.

```
  pod              elbow                         wrist                  fingertips
   |-- upper, 6 px --|  gap  |------ forearm, 15 px ------|   gap   |-- hand, 6 px --|
   px 0          px 5        px 6                     px 20        px 21         px 26
                  ~12 cm umbilical + SM 3-pin    ~8 cm umbilical + SM 5-pin plug
```

- Upper-arm segment: ~10 cm, 6 pixels, pixel 0 at the pod, running down the upper
  arm to just above the elbow. Plugs into the pod on a **JST-SM 3-pin**.
- Elbow umbilical: ~12 cm spanning the joint, three conductors — the strip's 5V,
  GND and data — through a **JST-SM 3-pin** mated a few cm above the elbow. Service
  loop across the joint, same reasoning as the wrist.
- Forearm segment: ~21 cm, 15 pixels, just below the elbow to the wrist, under a
  sleeve.
- Wrist umbilical: ~8 cm spanning the joint, five conductors — the strip's 5V, GND
  and data, plus this hand's two trigger wires — through a **JST-SM 5-pin** plug
  mated 3–4 cm above the wrist crease, where the skin barely moves. Service loop on
  the glove side so it isn't under tension at full extension.
- Hand segment: ~10 cm, 6 pixels, across the back of the hand to the knuckles,
  under the glove.

Data chains straight through, so it's one logical 27-pixel strip in code.

The firmware knows about both physical gaps and treats them as *virtual* distance
— `ELBOW_GAP_PX` ~7 at the elbow, `GAP_PX` ~5 at the wrist — so the comet's
apparent speed stays constant as it crosses each joint instead of appearing to jump.

**Keep the umbilicals short.** Every centimetre between the last pixel on one side
of a joint and the first pixel on the other is dark arm the comet has to cross. At
the wrist ~8 cm is fine and 15 cm reads as a gap; the elbow needs more slack, but
keep it near ~12 cm.

Measure your own arm and adjust `UPPER_PX` / `FOREARM_PX` / `HAND_PX` /
`ELBOW_GAP_PX` / `GAP_PX` to match. Each gap constant is the measured
pixel-to-pixel distance across that finished umbilical — connector body included,
which is most of it — divided by 1.67 cm.

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

Full drawing: [SCHEMATIC.md](SCHEMATIC.md).

| Signal | XIAO pin | Silkscreen | To |
|---|---|---|---|
| LED data | `U3 GPIO10` | silk `D10` | 74AHCT125 input, then 330–470 Ω, then `J2` (SM-3) pin 3 |
| Trigger | `U3 GPIO3` | silk `D1` | `J3` (SM-4) pin 3 (internal pull-up, active low) |
| Motor PWM | `U3 GPIO4` | silk `D2` | MOSFET module gate input |
| Battery sense | `U3 GPIO2` | silk `D0` | Midpoint of a 100 kΩ / 100 kΩ divider across the cell |
| 5V | `U3 5V` | silk `5V` | Boost output **through `CR2`** (cathode to the XIAO) |
| GND | `U3 GND` | silk `GND` | Common ground for everything |

**Pins are named by GPIO number, parts by designator, and the two never collide.**
The diodes are `CR1` and `CR2` precisely because the XIAO's silkscreen already owns
`D0`–`D10`; the silkscreen column above is the only place those D-numbers appear.
The rule, and why it matters, is in [SCHEMATIC.md](SCHEMATIC.md#naming-rules).

Everything the pod sends down the arm leaves through two plugs:

| Plug | Pins |
|---|---|
| **`J2`, SM 3-pin** — to the upper-arm strip | 1 strip 5V · 2 strip GND · 3 strip data |
| **`J3`, SM 4-pin** — the elbow lead | 1 motor + (battery, after fuse) · 2 motor − (MOSFET output) · 3 trigger · 4 trigger return (GND) |

The strip leaves on `J2` and goes straight into pixel 0. `J3` is a 4-conductor lead
down the upper arm to the elbow, where its SM-4 plug mates the sleeve. The strip
crosses the elbow separately, on its own SM-3 umbilical (`J6`).

Avoid `GPIO8` / `GPIO9` (silk `D8` / `D9`) — they're boot strapping pins.

Notes:

- `SW1`, a 3 A-rated DC disconnect, goes in the battery positive first, then the
  2 A polyfuse, then everything else.
- `CR2`, a 1N5819, goes between the boost output and the XIAO's 5V pad only — the
  strip and the shifter stay on the boost directly.
- A 10 kΩ gate-to-source pulldown holds the blower off while the XIAO boots. If
  your MOSFET module already has one, meter it and skip; most don't.
- The 1000 µF cap goes across the strip's 5V/GND, close to the strip connector on the pod.
- A 0.1 µF ceramic goes across the 74AHCT125's `Vcc` and `GND` pins, legs short,
  right at the chip. Different job from the 1000 µF — fit both.
- The 330–470 Ω resistor goes in series on the data line, at the connector end.
- The 1N5819 goes across the motor terminals, cathode to +, at the blower end.
- The motor is deliberately not bundled with the strip data. At the elbow it shares
  the SM-4 with the trigger, and the data crosses on its own SM-3; at the wrist the
  motor has its own SM-2. Twist the motor pair.
- Common ground is mandatory — the level shifter, strip, MOSFET, boost, and MCU
  all share it.

---

## Firmware

`firmware/clown_arm/clown_arm.ino` — Arduino sketch, FastLED, ESP32 Arduino core 3.x.

Flash the same sketch to both arms, unchanged.

Tunables live in one block at the top:

| Constant | Default | What it does |
|---|---|---|
| `UPPER_PX` / `FOREARM_PX` / `HAND_PX` | 6 / 15 / 6 | Physical layout |
| `ELBOW_GAP_PX` / `GAP_PX` | 7 / 5 | Virtual distance across the elbow and wrist umbilicals |
| `COMET_TRAVEL_MS` | 250 | Pod to fingertip, must match blower spin-up |
| `COMET_REPEAT_MS` | 320 | Gap between comets while held |
| `MAX_BRIGHTNESS` | 180 | Global cap — raised to punch through glove fabric |
| `IDLE_BRIGHTNESS` | 20 | Resting glow; 0 for fully dark |
| `MOTOR_RUN_DUTY` | 230 | Bubble rate |
| `MOTOR_KICK_DUTY` / `MOTOR_KICK_MS` | 255 / 80 | Kickstart pulse |
| `THEME_HUE` | 192 | Comet color |
| `VBAT_WARN_MV` / `VBAT_WARN_CLEAR_MV` | 3400 / 3550 | Low-cell warning, with hysteresis |
| `VBAT_CUTOFF_MV` | 3000 | Sustained → shut the arm down |

Tune `COMET_TRAVEL_MS` last, on the assembled arm: film it in slow motion and
adjust until the first bubble leaves your fingers on the same frame the comet
lands. See [BUILD.md](BUILD.md) step 9.

---

## Field notes

- **Soap gets everywhere, and "above the spray" is a lie at a rave.** Your arms go
  up; the pod is then under the runoff, not above it. Sealed, drained, downward-
  facing openings, drip loops on every wire — [BUILD.md](BUILD.md) step 11.
- **`SW1` off, then cell out.** In that order, every time you stop.
- **Test the trigger in the gun pose, not on the bench.** The lever needs to sit
  under your middle and ring finger pads so the squeeze lands every time without
  aiming.
- **Cell out before you mate or unmate any connector.** Every time. It is the one
  habit that protects pixel 0.
- **Carry spares:** pre-made wrist and elbow umbilicals, and one SM pigtail pair of
  each size. Those swap without a soldering iron.
- **Know the two you can't fix:** a flat cell and a dead trigger. One of each per
  arm, both in use, no spares bought — see [BUILD.md](BUILD.md)'s field kit.
- **Any cell that ever travels loose gets a plastic case**, never a bag with keys
  or coins. The whole can of an 18650 is its negative terminal and the wrap is all
  that covers it.
- **Check every latch before you walk out.** A half-seated SM plug looks mated and
  works until you move.
- **Keep the USB-C port accessible** in the printed pod. You will reflash this
  more often than you expect.

---

## Status

- [x] Design, power plan, wiring
- [x] Parts list with explanations — [PARTS.md](PARTS.md)
- [x] Build manual — [BUILD.md](BUILD.md)
- [x] Printable PDF manual — [Clown-Build-Manual.pdf](Clown-Build-Manual.pdf)
- [x] Firmware v1, incl. low-battery warning with hysteresis and a 3.0 V shutoff
- [x] Schematic and harness drawing — [SCHEMATIC.md](SCHEMATIC.md)
- [x] Concept direction — [DESIGN.md](DESIGN.md)
- [x] Connector architecture — four modules per arm, no soldered joints across a joint
- [ ] **Pull the kit's technical drawings from the Bambu site** — needed for the
      bubbler mount and the blower sleeve
- [ ] **Find the IR / thermal camera** — wanted for bench test, [BUILD.md](BUILD.md) step 6
- [ ] **Hose test** — does a 150 mm feed hose still lift solution? Decides Mount C
      vs Mount A ([BUILD.md](BUILD.md) step 7)
- [ ] Pick a multimeter — spec and three suggestions in [PARTS.md](PARTS.md)
- [ ] Decide leaded vs lead-free solder (tradeoff in [PARTS.md](PARTS.md))
- [ ] Source a **logic-level** MOSFET — *not* an IRF520 module, see [PARTS.md](PARTS.md)
- [x] Kits, passives, protoboards and triggers on hand — see
      [PARTS.md](PARTS.md), *What's already on hand*
- [ ] Remaining parts ordered — the `buy` rows in [PARTS.md](PARTS.md); **stock,
      price and delivery are unverified**, confirm in cart
- [ ] Costume layer decided — glove, sleeve, diffuser, ribbon. Buy one, test it
      lit, then buy the rest
- [ ] Bottles sourced — 24T/30T neck, not included in the kit
- [ ] Lace diffusion test (see DESIGN.md — lace reveals, it doesn't diffuse)
- [ ] Decide where the controller pod hides
- [ ] One arm assembled and timed
- [ ] Second arm
- [ ] Both-arms checkout and doffing drill ([BUILD.md](BUILD.md) step 13)
- [ ] **Engineering review of [SCHEMATIC.md](SCHEMATIC.md)** — checklist at the
      bottom of that file
- [ ] Printed enclosures (trigger plate, cell cradle, controller pod, bubbler
      mount) — sealed to [BUILD.md](BUILD.md) step 11, not just printed
- [ ] **Soak test** — powered arm, overhead, sprayed for a minute, then opened and
      inspected ([BUILD.md](BUILD.md) step 11)
- [ ] Source the disconnect switches — **check the DC rating**, not the AC one
- [ ] Optional: ESP-NOW sync between arms

---

## Regenerating the PDF

The manual is generated, not hand-edited. Edit
[docs/manual/build_manual.py](docs/manual/build_manual.py) and run:

```
pip3 install reportlab
python3 docs/manual/build_manual.py
```

Part numbers live in the `PARTS` list at the top of that script; the assembly
steps reference them through `ref(n)`, so renumbering a part updates every
cross-reference automatically.

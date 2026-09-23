# clown

A bubble-shooting clown costume. Make a gun shape with either hand, squeeze your
remaining fingers into your palm, and a comet of light runs from your elbow down
to your fingertips — arriving exactly as a stream of bubbles starts firing out of
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

**Costume direction:** [DESIGN.md](DESIGN.md) — the concept board, and the three
places where it changes the build.

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
- **Each hand has its own trigger**, wired only to its own arm. There is no
  cross-arm wiring anywhere in v1.
- If one arm dies mid-event, the other keeps working.
- **The firmware is byte-identical on both.** As long as pixel 0 is at the elbow
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
| **Pod** — upper arm | brain, boost, level shifter, MOSFET, fuse, battery sled | battery plug + straps |
| **Sleeve** — forearm | forearm strip, 15 px | elbow: SM 6-pin + SM 2-pin |
| **Glove** — hand | hand strip 6 px, this hand's trigger | wrist: SM 5-pin |
| **Bubbler** | bottle, cap, hose, blower head | wrist: SM 2-pin + its strap |

### The connectors

| Boundary | Carries | Connector |
|---|---|---|
| Cell ↔ pod, cell ↔ charger | 2 | **JST-PH 2.0, 2-pin** *(factory, on the cell)* |
| Pod → sleeve, at the elbow | strip 3 + trigger 2 + second GND | **JST-SM 6-pin** |
| Motor run, at the elbow | motor 2 | **JST-SM 2-pin** |
| Sleeve → glove, at the wrist | strip 3 + trigger 2 | **JST-SM 5-pin** |
| Motor run, at the wrist | motor 2 | **JST-SM 2-pin** |
| Microswitch pigtail | switch 2 | **JST-ZH 1.5 mm, 2-pin** |

Both the trigger and the motor have to reach the pod from the hand, so both cross
*both* joints — which is why the elbow plug is 6-pin rather than 3.

### Two rules that keep it safe

**No two connectors on one arm share both family and pin count.** PH-2 · ZH-2 ·
SM-2 · SM-5 · SM-6. The three 2-pin plugs are three different pitches — 2.0, 1.5
and 2.5 mm — so none will mate with the others.

- **The trigger pigtail is ZH, not PH,** because every cell ships on a PH2.0 lead.
  One wrong plug would put 3.7 V onto GPIO3.
- **The kit's motor lead gets reworked off PH2.0 to SM-2,** because as shipped the
  cell mates straight to the motor, bypassing the MOSFET entirely.
- The motor's two SM-2 plugs are identical to each other, which is safe *by
  construction*: they're on the same net, so cross-mating them only shortens the run.

**Battery out before you mate or unmate anything.** Feeding data into an unpowered
WS2812 pushes current through its input protection diodes — the classic way to kill
pixel 0.

Full detail in [PARTS.md](PARTS.md) and [BUILD.md](BUILD.md) step 12.

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

Each bubble kit ships with a protected 18650 **already on a PH2.0 pigtail** and a
USB charger that mates to the same plug. Fit the matching half at the pod and a
flat cell goes pod → charger with no adapter. Buy spare cells to hot-swap.

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

The firmware reads cell voltage through a divider and pulses the elbow pixel red
when it drops below 3.4 V, so you get warning rather than a sudden death.

---

## Strip layout

**Split the strip at the wrist.** A continuous strip across a flexing wrist will
crack its traces within a few hours of wear.

```
  elbow                        wrist                  fingertips
   |------ forearm, 15 px ------|   gap   |-- hand, 6 px --|
   px 0                      px 14        px 15         px 20
                            ~8 cm umbilical + SM 5-pin plug
```

- Forearm segment: ~21 cm, 15 pixels, pixel 0 at the elbow, under a sleeve.
- Wrist umbilical: ~8 cm spanning the joint, five conductors — the strip's 5V, GND
  and data, plus this hand's two trigger wires — through a **JST-SM 5-pin** plug
  mated 3–4 cm above the wrist crease, where the skin barely moves. Service loop on
  the glove side so it isn't under tension at full extension.
- Hand segment: ~10 cm, 6 pixels, across the back of the hand to the knuckles,
  under the glove.

Data chains straight through, so it's one logical 21-pixel strip in code.

The firmware knows about the physical gap and treats it as ~5 pixels of *virtual*
distance, so the comet's apparent speed stays constant as it crosses the wrist
instead of appearing to jump.

**Keep the umbilical short.** Every centimetre between the last forearm pixel and
the first hand pixel is dark arm the comet has to cross. ~8 cm is fine; 15 cm reads
as a gap.

Measure your own arm and adjust `FOREARM_PX` / `HAND_PX` / `GAP_PX` to match.
`GAP_PX` is the measured pixel-to-pixel distance across the finished umbilical —
connector body included, which is most of it — divided by 1.67 cm.

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
| LED data | D10 | 10 | 74AHCT125 input, then 330–470 Ω, then elbow SM-6 pin 3 |
| Trigger | D1 | 3 | Elbow SM-6 pin 4 (internal pull-up, active low) |
| Motor PWM | D2 | 4 | MOSFET module gate input |
| Battery sense | D0 | 2 | Midpoint of a 100 kΩ / 100 kΩ divider across the cell |
| 5V | 5V pad | — | Boost output, elbow SM-6 pin 1, 74AHCT125 Vcc |
| GND | GND | — | Common ground for everything |

Everything the pod sends down the arm leaves through two plugs:

| Plug | Pins |
|---|---|
| **SM 6-pin** | 1 strip 5V · 2 strip GND · 3 strip data · 4 trigger · 5 trigger return · 6 second ground |
| **SM 2-pin** | 1 motor + (battery, after fuse) · 2 motor − (MOSFET output) |

Pin 6 is not spare. The elbow run is the longest in the costume and carries the
whole strip's current; a second ground conductor cuts the drop and gives the data
line a better return path.

Avoid D8 / D9 (GPIO8 / GPIO9) — they're boot strapping pins.

Notes:

- A 2 A polyfuse goes inline at the battery positive, before anything else.
- The 1000 µF cap goes across the strip's 5V/GND, close to the elbow connector.
- The 330–470 Ω resistor goes in series on the data line, at the connector end.
- The 1N5819 goes across the motor terminals, cathode to +, at the blower end.
- The motor gets its own plug, deliberately not bundled with the data line. Twist
  the pair.
- Common ground is mandatory — the level shifter, strip, MOSFET, boost, and MCU
  all share it.

---

## Firmware

`firmware/clown_arm/clown_arm.ino` — Arduino sketch, FastLED, ESP32 Arduino core 3.x.

Flash the same sketch to both arms, unchanged.

Tunables live in one block at the top:

| Constant | Default | What it does |
|---|---|---|
| `FOREARM_PX` / `HAND_PX` / `GAP_PX` | 15 / 6 / 5 | Physical layout |
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
- **Cell out before you mate or unmate any connector.** Every time. It is the one
  habit that protects pixel 0.
- **Carry spares:** a charged cell per arm, a pre-made wrist umbilical, a spare
  microswitch on its ZH-2 pigtail, and one SM pigtail pair of each size. Those are
  what fail during an event — and now all of them swap without a soldering iron.
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
- [x] Firmware v1, incl. low-battery warning
- [x] Concept direction — [DESIGN.md](DESIGN.md)
- [x] Connector architecture — four modules per arm, no soldered joints across a joint
- [ ] **Pull the kit's technical drawings from the Bambu site** — needed for the
      bubbler mount and the blower sleeve
- [ ] **Find the IR / thermal camera** — wanted for bench test, [BUILD.md](BUILD.md) step 6
- [ ] **Hose test** — does a 150 mm feed hose still lift solution? Decides Mount C
      vs Mount A ([BUILD.md](BUILD.md) step 7)
- [ ] Pick a multimeter (spec is in [PARTS.md](PARTS.md); model not chosen)
- [ ] Decide leaded vs lead-free solder (tradeoff in [PARTS.md](PARTS.md))
- [ ] Parts ordered
- [ ] Bottles sourced — 24T/30T neck, not included in the kit
- [ ] Lace diffusion test (see DESIGN.md — lace reveals, it doesn't diffuse)
- [ ] Decide where the controller pod hides
- [ ] One arm assembled and timed
- [ ] Second arm
- [ ] Both-arms checkout and doffing drill ([BUILD.md](BUILD.md) step 12)
- [ ] Printed enclosures (trigger plate, battery sled, controller pod, bubbler mount)
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

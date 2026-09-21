# Build Manual

How to assemble one arm, start to finish. Then you do it again for the other arm.

Read [PARTS.md](PARTS.md) first if you haven't — it explains what each component
actually does, which makes these steps make a lot more sense.

**Estimated time:** a full afternoon for the first arm. The second one takes about
half that, because you'll already know what you're doing.

---

## Before you start

**Read this whole page once before picking up the soldering iron.** Several steps
are much easier if you know what's coming (notably: heat-shrink goes on *before*
you solder, and you bench-test *before* anything goes into the glove).

### Safety, briefly but seriously

- **Lithium battery.** Use the protected cells that came with the bubble kits.
  Never short the terminals, never charge an obviously damaged or puffy cell, and
  don't leave it charging unattended. It's strapped to your arm — treat it with
  respect.
- **Check polarity with a multimeter before connecting the battery the first
  time.** Reversed power will destroy the brain and the LED strip instantly and
  permanently. Two minutes with a meter saves you re-ordering parts.
- **Soap and electronics.** Everything that can get wet is sealed or lives on
  your upper arm, above the spray. This is a design constraint, not a suggestion.
- Solder in a ventilated space. Flux fumes are unpleasant.

---

## Step 1 — Measure your arm

Put on the glove you'll be using and hold your arm out in the "finger gun" pose.

Measure and write down:

1. **Elbow to wrist crease** — typically around 25 cm.
2. **Wrist crease to knuckles**, across the back of the hand — typically around
   10 cm.
3. Where your middle and ring finger pads land on your palm when you squeeze.
   That's where the trigger goes. Mark it with a fabric pen.

Convert the first two to pixel counts. At 60 LED/m each pixel is **1.67 cm**:

```
forearm pixels = forearm cm / 1.67
hand pixels    = hand cm / 1.67
```

For typical measurements that's about **15 pixels** on the forearm and **6** on
the hand. Round down — a slightly short strip is fine, a strip that doesn't fit
is not.

Keep these numbers. You'll type them into the firmware in Step 8.

---

## Step 2 — Cut the strip

The strip has marked cut lines between every pixel, usually with copper pads
either side. **Cut in the middle of the copper pads**, not next to them — you
need pad left on both pieces to solder to.

Cut two pieces:

- Forearm piece: your forearm pixel count (≈15)
- Hand piece: your hand pixel count (≈6)

**Check the arrows.** The strip has small arrows printed on it showing which way
data flows. Data goes **elbow → fingertips**, so both pieces must have their
arrows pointing the same way, toward your fingers. Getting this backwards is the
single most common build mistake, and the fix is unsoldering everything.

Mark the elbow end of the forearm piece with tape. That end is pixel 0.

### Why the strip is in two pieces

Your wrist bends constantly. A single continuous strip across that joint will
crack its internal copper traces within a few hours of wearing it, and then
everything past the crack goes dark. The flexible jumper wire in the next step
absorbs that movement instead.

---

## Step 3 — Solder the wrist jumper

You're joining the two strip pieces with about 4 cm of flexible silicone wire,
three conductors: **5V, GND, and data**.

1. Slide heat-shrink onto each wire **now**, before soldering.
2. Peel back a little of the silicone sleeve at the ends of each strip piece to
   expose the copper pads.
3. Tin the pads and the wire ends (melt a little solder onto each separately).
4. Join: forearm piece's **output** end → hand piece's **input** end. 5V to 5V,
   GND to GND, and **DO** (data out) to **DI** (data in).
5. Shrink the heat-shrink down over each joint.
6. Seal the exposed strip ends with a blob of hot glue or clear silicone. This is
   the soap-proofing.

Make the jumper slightly longer than the gap needs, so there's a small service
loop. It should never be pulled tight when you extend your wrist fully.

**Test the joint now:** gently tug each wire. Better to find a weak joint on the
bench than inside a glove.

---

## Step 4 — Build the controller pod

This all lives on a small piece of protoboard that will sit on your **upper arm**,
above the soap spray.

Wire it up as follows.

### Connections

| From | To | Notes |
|---|---|---|
| Battery + | Polyfuse → everything's + | Fuse goes first, right at the battery |
| Battery − | Common ground | Everything shares this ground |
| Battery + (after fuse) | Boost module IN+ | |
| Battery − | Boost module IN− | |
| Boost OUT+ (5V) | XIAO 5V pad, 74AHCT125 Vcc, strip 5V | |
| Boost OUT− | Common ground | |
| Battery + (after fuse) | Motor + | Motor runs direct from battery, not 5V |
| Motor − | MOSFET module output | |
| MOSFET module ground | Common ground | |
| XIAO D2 (GPIO4) | MOSFET gate input | |
| XIAO D10 (GPIO10) | 74AHCT125 input pin | |
| 74AHCT125 output pin | 330–470 Ω resistor → strip DIN | Resistor close to the strip |
| XIAO D1 (GPIO3) | Microswitch, other side to ground | |
| XIAO D0 (GPIO2) | Junction of the two 100 kΩ resistors | Battery monitor |

### The battery monitor divider

Three connections:

```
Battery + (after fuse) ──[100 kΩ]──┬──[100 kΩ]── Ground
                                   │
                              XIAO D0
```

The midpoint sits at exactly half the battery voltage, which is safely within
what the brain can measure.

### Also fit

- **1000 µF capacitor** across the strip's 5V and ground, physically close to the
  strip end. **Watch polarity** — the marked stripe is the negative leg.
- **1N5819 diode** directly across the motor's two terminals. The banded end goes
  to the **positive** side. Backwards it's a dead short, so check this one twice.

### Rules that matter

- **Everything shares one common ground.** The brain, strip, level shifter,
  MOSFET, boost, and battery all connect to the same ground. Skipping this causes
  bizarre, hard-to-diagnose behavior.
- **Don't use D8 or D9** (GPIO8/GPIO9) for anything. They're boot pins — the
  board won't start reliably if something's attached to them.
- Keep the wire run from the level shifter to the first pixel short.

### Leave the USB-C port accessible

Design the printed pod so you can plug a USB-C cable into the XIAO **without
disassembling anything**. You will reflash this more times than you expect —
every timing tweak, every color change. A cutout in the pod wall is enough.

---

## Step 5 — Wire the trigger

1. Solder two lengths of thin silicone wire to the microswitch's **COM** and
   **NO** (normally open) terminals.
2. Run them up your forearm to the pod. One goes to D1, the other to ground.
3. Mount the switch on a small printed plate, positioned so the **lever** sits
   under your middle and ring finger pads at the spot you marked in Step 1.

Orient the lever so a natural squeeze presses it across its length. You should be
able to trigger it with your eyes closed, in one motion, every time. If you find
yourself having to aim, rotate or reposition the plate until you don't.

---

## Step 6 — Bench test before anything goes in the glove

**Do not skip this.** Sewing everything into a glove and *then* discovering a
reversed data arrow is genuinely miserable.

Lay the whole thing out flat on the table, fully wired but not mounted.

1. **Check polarity with the multimeter.** Battery + and − where you expect.
   Boost output reading close to 5.0V. Only then connect the brain.
2. Power it up. You should get the dim breathing idle glow.
3. Press the microswitch by hand. The comet should launch from the **elbow end**
   and travel to the **fingertip end**, and the motor should spin.
4. If the comet runs backwards, your strip pieces are reversed — fix it in the
   wiring, **not** in the code. (Both arms run identical firmware. Keeping that
   true is worth the resolder.)
5. Let it run for five minutes. Touch the boost module and MOSFET. Warm is fine,
   too-hot-to-touch is not — power down and check for a short.

---

## Step 7 — Fit the bubble maker

Mount the blower unit so its nozzle points **past your fingertips**, in the
direction the comet travels. The bottle of solution sits on the back of your hand
or forearm — check MakerWorld for existing mounts from the kit's collection as a
starting point.

Wire the motor back to the MOSFET in the pod. Use silicone wire; this run flexes.

The one-way valve in the supplied cap means the bottle won't dump solution when
you move your arm around, which is the entire reason to use the kit's cap rather
than improvising.

---

## Step 8 — Flash the firmware

1. Install the Arduino IDE, then add ESP32 board support (Boards Manager → search
   "esp32" → install the Espressif package).
2. Install the **FastLED** library (Library Manager → search "FastLED").
3. Select board: **XIAO_ESP32C3**.
4. Open `firmware/clown_arm/clown_arm.ino`.
5. **Edit the layout constants at the top** to match your Step 1 measurements:

```cpp
constexpr int FOREARM_PX = 15;   // your forearm pixel count
constexpr int HAND_PX    = 6;    // your hand pixel count
constexpr int GAP_PX     = 2;    // jumper length / 1.67 cm, rounded
```

6. Plug in USB-C and upload.

If upload fails, hold the BOOT button while plugging in the cable to force
bootloader mode.

**Flash the identical sketch to both arms.** There's deliberately no left/right
setting — as long as pixel 0 is at the elbow on each arm, the mirroring is
physical only.

---

## Step 9 — Tune the timing

This is the step that makes the whole effect work, and it can only be done on the
finished arm.

The goal: **the comet reaches your fingertips at the exact moment the first bubble
appears.** When it's right, the light looks like it's *causing* the bubbles. When
it's wrong by even 100 ms, it looks like lag.

1. Film yourself firing it in slow motion (any modern phone does 120 or 240 fps).
2. Watch back frame by frame. Does the comet arrive early or late?
3. Adjust `COMET_TRAVEL_MS`:
   - Comet arrives **before** the bubbles → increase it (slower comet)
   - Comet arrives **after** the bubbles → decrease it (faster comet)
4. Reflash, film again. Expect three or four rounds.

Default is 250 ms. Your actual number depends on how fast your specific blower
spins up, which is why it's guesswork until you measure it.

While you're here, `COMET_REPEAT_MS` sets how often a new comet launches while
you hold the trigger. Lower = a denser, more frantic stream.

---

## Step 10 — Mount into the glove

Now the strip goes in.

### Choosing and testing the glove

The fabric spreads the light into a smooth continuous glow instead of visible
dots — which is a genuine upgrade over an exposed strip, **if** the fabric
cooperates.

- **Thin, pale, stretchy fabric** glows beautifully.
- **Thick or dark fabric**, especially leather, swallows almost all of it.

Before committing, hold a powered section of strip under a scrap or under the
glove itself in a dark room. If you can't see it clearly, no amount of firmware
will fix it — get a different glove.

### Brightness

The default `MAX_BRIGHTNESS` is raised to punch through fabric. If yours is
thicker you can push it higher, but watch two things:

- Current draw climbs with brightness, so battery life drops.
- Under fabric with no airflow, a very bright strip gets warm. At these levels,
  with only a handful of pixels lit at a time, it's a non-issue — but don't set
  everything to full white and leave it on for an hour.

### Routing

- The strip runs across the **back of the hand**, over the knuckles. Never the
  palm — that's where the trigger is and where you grip things.
- Stop short of the fingertips. The bubble nozzle needs that space, and finger
  joints flex too much for strip to survive.
- Sew a **fabric channel or sleeve** for the strip to sit in, rather than gluing
  it down flat. The channel lets it slide a little as your hand flexes. Glued-taut
  strip tears itself off, or tears the glove.
- Run the forearm section under a sleeve or an arm warmer, same principle.
- Add **strain relief** where wires cross the elbow and wrist — a small loop of
  wire tacked down on each side of the joint, so movement pulls on the tack rather
  than the solder joint.

---

## Step 11 — Build the second arm

Repeat Steps 1–10.

The only thing to be careful about: **pixel 0 goes at the elbow on this arm too.**
It's tempting to mirror the wiring along with the physical build. Don't. Identical
wiring means identical firmware means one thing to maintain.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Nothing lights at all | Check common ground. Check boost output is ~5V. Check strip DIN is on the *input* end (follow the arrows) |
| First pixel wrong color, rest fine | Missing or wrong-value data resistor |
| Random flickering, especially when moving | Missing 74AHCT125, or a loose ground |
| Comet runs fingertips → elbow | Strip is reversed. Fix the wiring, not the code |
| Comet "jumps" at the wrist | `GAP_PX` doesn't match your actual jumper length |
| Colors wrong (red/green swapped) | Change `GRB` to `RGB` in the `addLeds` line |
| Motor whines audibly | PWM frequency dropped below 20 kHz — check `MOTOR_PWM_HZ` |
| Motor doesn't spin | MOSFET gate not on D2, or a non-logic-level MOSFET |
| Everything dies when the motor starts | Battery sagging, or the polyfuse tripping. Check the cell's charge |
| Lights work, then die after a few minutes | Battery protection circuit cutting out — recharge or swap the cell |
| Board won't accept uploads | Hold BOOT while plugging in USB |
| Strip goes dark past the wrist | Cracked trace or failed jumper joint — this is the failure mode the jumper exists to prevent |

---

## Programming and customization

The whole point of the WS2812B strip is that **every pixel takes orders
individually** — that's what "addressable" means, and it's why a comet is possible
at all.

### Quick tweaks

Everything you'd normally want to change is in one clearly-marked block at the top
of `clown_arm.ino`. Edit, reflash over USB-C, done:

| Constant | Changes |
|---|---|
| `THEME_HUE` | The comet's color (0–255 around the color wheel) |
| `COMET_TRAVEL_MS` | Comet speed / sync with the bubbles |
| `COMET_REPEAT_MS` | How rapid-fire the stream is |
| `COMET_FADE` | Tail length — higher is shorter |
| `MAX_BRIGHTNESS` | Overall brightness, for your glove's fabric |
| `IDLE_BRIGHTNESS` | Resting glow. Set to 0 for fully dark when idle |
| `MOTOR_RUN_DUTY` | Bubble rate |

### Going further

The XIAO ESP32-C3 has Wi-Fi and Bluetooth sitting unused. Natural next steps, in
rough order of effort:

- **More patterns** — a second animation, and a long-press to cycle between them.
- **ESP-NOW sync** — let one arm's trigger fire both arms simultaneously, for a
  two-handed blast.
- **Phone control** — a small web page served by the board to change color and
  speed live, without a laptop.

None of these need extra hardware. They're already paid for.

---

## Field kit

Things to have with you when you actually wear this:

- Spare charged 18650 per arm
- A pre-soldered spare wrist jumper
- A spare microswitch
- Extra bubble solution — **this runs out long before the battery does**
- A small screwdriver and some electrical tape

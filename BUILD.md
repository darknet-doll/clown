# Build Manual

## What you are building

**Two arms.** Each arm is four modules that unplug from each other:

| Module | Holds | Unplugs at |
|---|---|---|
| **Pod** — upper arm | brain, boost, level shifter, MOSFET, fuse, disconnect, battery sled | `SW1` + battery plug + straps |
| **Sleeve** — forearm | forearm strip, 15 px | elbow: SM 6-pin + SM 2-pin |
| **Glove** — hand | hand strip 6 px, this hand's trigger | wrist: SM 5-pin |
| **Bubbler** | bottle, cap, hose, blower head | wrist: SM 2-pin + its strap |

Nothing is soldered end to end across a joint. That is what lets you get out of
the costume alone, with soapy hands, without dislocating a shoulder.

Steps 1–11 build **one arm**. Step 12 is the second arm. **Step 13 is the costume**
— the two arms together, and how you get in and out of it.

Read [PARTS.md](PARTS.md) first if you haven't — it explains what each component
actually does, which makes these steps make a lot more sense.
[SCHEMATIC.md](SCHEMATIC.md) is the same circuit as a drawing; keep it open
alongside step 4.

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
- **You must be able to kill and remove the cell in seconds, one-handed.** That is
  what `SW1` (step 4) and a tool-free sled lid (step 11) are for. If getting the
  battery out of this costume needs two hands, a screwdriver, or taking a sleeve
  off first, it is not finished.
- **Carry and store spare cells in a plastic case**, never loose in a bag with
  keys or coins. A bare 18650's whole can is the negative terminal — the wrap is
  the only insulation it has.
- **Protected cells are the backstop, not the plan.** The firmware shuts the arm
  down at 3.0 V so the cell's own protection board never has to act. Don't remove
  either layer.
- **Check polarity with a multimeter before connecting the battery the first
  time.** Reversed power will destroy the brain and the LED strip instantly and
  permanently. Two minutes with a meter saves you re-ordering parts.
- **Soap and electronics.** Assume every surface of this costume gets wet, from
  every angle, all night — arms go up, and "above the spray" stops meaning
  anything the moment they do. Sealing is step 11, and it is a design constraint,
  not a suggestion.
- Solder in a ventilated space. The fumes are flux, not lead — they're unpleasant
  whichever solder you bought. A cheap fan pulling air away from your face fixes it.

### The connector rule you will use constantly

> **Battery out before you mate or unmate anything.**

Feeding data into an unpowered WS2812 strip pushes current through its input
protection diodes. That is the classic way to kill pixel 0, and it's exactly what
happens if you plug the glove in while the pod is live. Unplug the cell first,
every time. It takes one second and it becomes automatic quickly.

---

## Step 1 — Measure your arm

Put on the glove and sleeve you'll be using and hold your arm out in the "finger
gun" pose.

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

**Then subtract about 4 cm from the forearm figure.** The wrist umbilical and its
connector need to live somewhere, and that somewhere is the last few centimetres
of forearm, just above the wrist crease where the skin barely flexes.

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
everything past the crack goes dark. The flexible umbilical in the next step
absorbs that movement instead.

---

## Step 3 — Build the wrist umbilical

This is the plug that lets the glove come off on its own. It carries **five
conductors**: the strip's 5V, GND and data, plus this hand's two trigger wires.

Use a **JST-SM 5-pin pigtail pair**. Decide a convention now and keep it on both
arms:

| SM-5 pin | Carries |
|---|---|
| 1 | Strip 5V |
| 2 | Strip GND |
| 3 | Strip data |
| 4 | Trigger |
| 5 | Trigger return (to ground at the pod) |

### Sleeve side

1. Slide heat-shrink onto every wire **now**, before soldering.
2. Solder short silicone leads to the forearm piece's **output** end — 5V, GND and
   **DO** (data out).
3. Solder those three to pins 1–3 of one half of the SM-5 pigtail.
4. Pins 4–5 get two lengths of thin silicone wire long enough to run all the way
   **up the forearm to the elbow**. They're the trigger's path to the pod.
5. Shrink everything down. Seal the exposed strip end with a blob of hot glue or
   clear silicone — this is the soap-proofing.

### Glove side

1. Solder pins 1–3 of the other pigtail half to the hand piece's **input** end —
   5V to 5V, GND to GND, and pin 3 to **DI** (data in).
2. Pins 4–5 get two lengths of thin silicone wire long enough to reach the palm,
   ending in the **female half of a JST-ZH 2-pin** pigtail. That's where the
   microswitch will plug in at Step 5.
3. Shrink, and seal the strip end the same way.

### Where the connector sits, and why

- **Mate the pair about 3–4 cm above the wrist crease**, on the forearm. That skin
  barely moves. The wrist crease itself is the worst possible place for a rigid
  20 mm plastic body.
- The **glove-side wire is the flex element** — leave it long enough to cross the
  wrist with a **service loop**, so it's never under tension at full extension.
- **Keep the whole umbilical as short as the connector allows.** Every centimetre
  between the last forearm pixel and the first hand pixel is a centimetre of dark
  arm the comet has to cross. Around 8 cm total is realistic and fine; 15 cm will
  look like a gap.
- **Measure the finished pixel-to-pixel distance** and write it down. You'll turn
  it into `GAP_PX` in Step 8.

**Test the joints now:** gently tug each wire. Better to find a weak joint on the
bench than inside a glove.

---

## Step 4 — Build the controller pod

This all lives on a small piece of protoboard that will sit on your **upper arm**.
It used to say "above the soap spray" — step 11 explains why that is no longer the
plan, and what the enclosure has to do instead.

**Work from [SCHEMATIC.md](SCHEMATIC.md) sheet 1.** The table below is the same
circuit in words; the drawing is what to check your work against.

### Connections

| From | To | Notes |
|---|---|---|
| Battery **PH2.0** + | `SW1` master disconnect | Disconnect first, right at the cell |
| `SW1` out | Polyfuse → everything's + | Fuse next, before anything else |
| Battery **PH2.0** − | Common ground | Everything shares this ground |
| Battery + (after fuse) | Boost module IN+ | |
| Battery − | Boost module IN− | |
| Boost OUT+ (5V) | 74AHCT125 Vcc, elbow SM-6 pin 1 | Strip and shifter, direct |
| Boost OUT+ (5V) | `D2` anode; `D2` cathode → XIAO 5V pad | **Isolation diode — see below** |
| Boost OUT− | Common ground | |
| Battery + (after fuse) | Motor +, via elbow SM-2 | Motor runs direct from battery, not 5V |
| Motor − (via elbow SM-2) | MOSFET module output | |
| MOSFET module ground | Common ground | |
| XIAO D2 (GPIO4) | 74AHCT125 **second** gate input | Gate drive — see below |
| 74AHCT125 second gate output | 100 Ω → MOSFET gate | With a 10 kΩ gate-to-source pulldown — see below |
| 74AHCT125 `1OE`, `2OE` | Common ground | Enables the two gates you use |
| 74AHCT125 `3A`, `4A` | Common ground | Unused inputs — must not float |
| 74AHCT125 `3OE`, `4OE` | 5V | Unused outputs disabled. `3Y`/`4Y` stay open |
| XIAO D10 (GPIO10) | 74AHCT125 input pin | |
| 74AHCT125 output pin | 330–470 Ω resistor → elbow SM-6 pin 3 | Resistor close to the connector |
| XIAO D1 (GPIO3) | Elbow SM-6 pin 4 | Trigger, arriving from the hand |
| Elbow SM-6 pin 5 | Common ground | Trigger return |
| XIAO D0 (GPIO2) | Midpoint of the two 100 kΩ resistors | Battery monitor |

### Fit the master disconnect

`SW1` goes in the **cell positive**, between the battery plug and the polyfuse —
so it kills everything downstream, including the motor tap and the boost.

- **Rated for at least 3 A DC.** Most small rocker and toggle switches are rated
  for mains AC and much less for DC. Check the DC number, not the AC one
- **Mounted so you can reach it through the costume, one-handed**, without
  opening the pod. A rubber-booted toggle keeps its own seal and gives you a
  positive click you can find by feel
- **Label which way is off**, or fit a guard. Standing in the dark unsure whether
  you just switched it off is the failure this part exists to prevent
- It does **not** replace pulling the cell. It makes the pod safe to open and the
  arm safe to unplug in one motion; the cell still comes out for storage, for
  charging, and any time something is actually wrong

Together with a sled lid that opens without a tool (step 11), this is the answer to
"get the battery out of this costume, now."

### Isolate the XIAO's 5 V pad

**The XIAO's `5V` pad is wired straight to its USB-C VBUS.** There is no diode on
the board. So with the pack connected and a USB cable plugged in, the boost output
is sitting on the host's USB port — feeding a laptop, a phone charger, or whatever
else you reflash from.

Fit a **1N5819 Schottky, `D2`, between the boost output and the XIAO's 5V pad,
banded end (cathode) to the XIAO.**

- Current flows boost → XIAO. Nothing flows back into a host port
- Costs about 0.3 V: the XIAO sees ~4.7 V, comfortably inside its regulator
- **Only the XIAO goes behind the diode.** The strip and the 74AHCT125 stay on the
  boost output directly, at a full 5 V — they're the load that cares
- You bought these for the motor flyback anyway. Buy a couple more

> Without `D2`, the safe habit is "never plug in USB with the cell connected" — and
> you will break that habit at 2 a.m. with one hand full. The diode is 20¢.

### Drive the MOSFET gate at 5V, not 3.3V

The XIAO's GPIO swings to **3.3 V**. Most "logic-level" MOSFETs are specified fully
on at **Vgs = 5 V** — at 3.3 V they only partly open, dissipate the difference as
heat, and the blower runs slow and inconsistent.

**The 74AHCT125 has four gates and the strip only uses one.** Route `D2` through a
second gate exactly the way you route the LED data through the first. The MOSFET
then sees a clean 5 V gate signal.

- Costs nothing — the chip is already in the pod
- Add a **100 Ω** resistor in series with the gate
- **If you bought an AO3400-based part** it will work at 3.3 V directly, since AO3400
  is specified down to 2.5 V. Doing it through the shifter anyway costs nothing and
  removes the question

### Tie off the two gates you aren't using

The 74AHCT125 has four gates. You use two. **The other two are not spare parts,
they are inputs, and a CMOS input must never be left floating.**

A floating input sits wherever stray charge leaves it, usually somewhere near the
switching threshold. The gate then oscillates, and the chip dissipates real power
doing it — tens of milliamps instead of microamps, as heat, continuously, out of a
battery strapped to your arm. It also couples noise into the two gates you do care
about, which is the last thing you want on the LED data line.

| Pin | Goes to |
|---|---|
| `1OE`, `2OE` | **GND** — this is what turns the two gates you use *on* |
| `3A`, `4A` | **GND** — unused inputs, parked at a defined level |
| `3OE`, `4OE` | **Vcc** — unused outputs disabled (OE is active low) |
| `3Y`, `4Y` | **nothing at all** — outputs. Leave them open |

- **Never tie an output to a rail.** `3Y` and `4Y` stay unconnected; the `OE` pins
  are what switch them off
- On the DIP-14 part: `1OE` 1, `1A` 2, `1Y` 3, `2OE` 4, `2A` 5, `2Y` 6, `GND` 7,
  `3Y` 8, `3A` 9, `3OE` 10, `4Y` 11, `4A` 12, `4OE` 13, `Vcc` 14.
  **Check the datasheet for the package you bought** — a breakout board renumbers
  everything
- Four short wires on the protoboard. Do it while the chip is going in, not later

### The gate pulldown is not optional

Between the moment the XIAO resets and the moment `setup()` runs, `D2`/GPIO4 is an
**input, floating**. A floating gate on a MOSFET holds whatever charge it last
had. The failure looks like the blower twitching, or briefly running, every time
you power up or reflash — with the firmware doing nothing at all.

**A 10 kΩ resistor from gate to source fixes it permanently.** It is the only thing
holding the blower off during boot.

- **Bare transistor (RFP30N06LE, IRLZ44N):** fit one. It is not included
- **Module:** check, don't assume. Most "MOSFET module" boards do **not** have a
  gate pulldown. With the module unpowered and nothing else connected, measure
  **gate to source**:
  - reads around 10 kΩ (or anything from ~1 kΩ to ~100 kΩ) → it has one, you're done
  - reads open / megohms → add your own 10 kΩ across those two pins
- The firmware also drives the pin low as the very first thing in `setup()`, but
  that is belt to the resistor's braces — it cannot act before it runs

> **Do not use an IRF520 module.** It is the top search result for "Arduino MOSFET
> module" and it is not logic-level — its gate threshold runs to 4 V and it wants
> ~10 V to open properly. It half-works, which is harder to diagnose than not working.

### The pod's two outward plugs

Everything the pod sends down the arm leaves through exactly two connectors:

| Connector | Pin | Carries |
|---|---|---|
| **SM 6-pin** | 1 | Strip 5V |
| | 2 | Strip GND |
| | 3 | Strip data (after the resistor) |
| | 4 | Trigger |
| | 5 | Trigger return / ground |
| | 6 | **Second ground** — tie to common ground |
| **SM 2-pin** | 1 | Motor + (battery, after fuse) |
| | 2 | Motor − (MOSFET output) |

- **Pin 6 is not spare, it's a job.** The elbow run is the longest in the costume
  and carries the whole strip's current. A second ground conductor cuts the voltage
  drop and gives the data line a better return path. Tie it to common ground at
  both ends.
- **The motor gets its own plug on purpose.** Roughly an amp of switched PWM
  bundled against a WS2812 data line is asking for flicker. Twist the motor pair.

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
  elbow connector. **Watch polarity** — the marked stripe is the negative leg.
- **1N5819 diode** directly across the motor's two terminals, at the blower end.
  The banded end goes to the **positive** side. Backwards it's a dead short, so
  check this one twice.

### Keep the cell on its factory plug

The 18650 arrives on a **PH2.0 pigtail**, and the kit's USB charger mates to the
same connector. Fit the matching half at the pod and you get a clean swap: pull
the flat cell out of the pod, plug it straight into the charger, plug a fresh one
in. No adapters, no rework.

**PH2.0 must be the only PH connector in the whole build.** See Step 5.

The cell plug is also your last-resort disconnect. `SW1` is the one you reach for;
`J1` is the one that makes the arm genuinely inert. Design the pod so you can get
to both — the sled lid and the plug on the underside, the switch on the outside.

### Rules that matter

- **Everything shares one common ground.** The brain, strip, level shifter,
  MOSFET, boost, and battery all connect to the same ground. Skipping this causes
  bizarre, hard-to-diagnose behavior.
- **Don't use D8 or D9** (GPIO8/GPIO9) for anything. They're boot pins — the
  board won't start reliably if something's attached to them.
- Keep the wire run from the level shifter to the elbow connector short, and put
  the data resistor at the connector end.

### Leave the USB-C port accessible

Design the printed pod so you can plug a USB-C cable into the XIAO **without
disassembling anything**. You will reflash this more times than you expect —
every timing tweak, every color change. A cutout in the pod wall is enough.

Use a **data-capable** USB-C cable. A charge-only cable looks identical and will
cost you half an hour of confusion.

---

## Step 5 — Wire this hand's trigger

**Each hand has its own trigger, firing its own arm.** Nothing crosses the torso.
You are wiring one of two identical, independent triggers.

1. Solder two lengths of thin silicone wire to the microswitch's **COM** and
   **NO** (normally open) terminals.
2. Terminate them in the **male half of a JST-ZH 2-pin** pigtail — the mate to the
   one you left on the glove side of the umbilical in Step 3.
3. Mount the switch on a small printed plate, positioned so the **lever** sits
   under your middle and ring finger pads at the spot you marked in Step 1.

Orient the lever so a natural squeeze presses it across its length. You should be
able to trigger it with your eyes closed, in one motion, every time. If you find
yourself having to aim, rotate or reposition the plate until you don't.

### Why the switch gets its own tiny plug

The field kit carries a spare microswitch. Without this pigtail, "spare" means
"spare, if you also brought a soldering iron and somewhere to plug it in." With
it, swapping a dead trigger mid-event is a ten-second job.

### Why ZH and not PH

> **The trigger pigtail must not be PH2.0.**

Every cell in this build ships on a PH2.0 lead. If the trigger used the same
connector, one wrong plug in a dark room puts **3.7 V directly onto GPIO3** — a
dead pin, quite possibly a dead XIAO.

**JST-ZH is 1.5 mm pitch; PH is 2.0 mm.** They physically will not mate. That
incompatibility is the entire reason for the choice, so don't "simplify" it later
by standardising on one connector.

---

## Step 6 — Bench test before anything goes in the glove

**Do not skip this.** Sewing everything into a glove and *then* discovering a
reversed data arrow is genuinely miserable.

Lay the whole thing out flat on the table, fully wired but not mounted, with every
connector mated.

**Before any power at all:**

1. **Measure gate to source on the MOSFET.** You want a few kΩ, not open. Open
   means the pulldown is missing and the blower will twitch at every boot — go
   back to step 4.
2. **Check `D1` and `D2` orientation** against [SCHEMATIC.md](SCHEMATIC.md).
   `D1` banded end to motor **+**; `D2` banded end to the **XIAO**. `D1` backwards
   is a dead short across the cell through the MOSFET.
3. **Check continuity through every connector**, pin by pin, with the beeper. A
   pigtail with a crimp that didn't seat looks perfect and works intermittently.
   Find that now, not at the venue.

**Then, cell in, `SW1` on:**

4. **Check polarity with the multimeter.** Battery + and − where you expect.
   **Set the boost to 5.00 V on its trimpot before the XIAO is ever connected.**
5. **Check the isolation diode did its job.** Boost output ~5.0 V, XIAO 5V pad
   ~4.7 V. A ~0.3 V step across `D2` means it is in series and the right way
   round. Same reading on both sides means you shorted past it, and the pack is
   still able to backfeed a USB host.
6. Power it up. You should get the dim breathing idle glow.
7. **Watch the blower as it powers up. It must not twitch.** If it kicks, stop:
   floating gate.
8. Press the microswitch by hand. The comet should launch from the **elbow end**
   and travel to the **fingertip end**, and the motor should spin.
9. If the comet runs backwards, your strip pieces are reversed — fix it in the
   wiring, **not** in the code. (Both arms run identical firmware. Keeping that
   true is worth the resolder.)
10. Let it run for five minutes, then check for heat.

### Test the low-voltage shutoff, once

Worth doing on the bench exactly once per arm, so you recognise it in the field and
know it works:

- **With a bench supply:** feed the pod 2.95 V in place of the cell. Within about
  six seconds the elbow pixel starts a slow **double** blink, the motor stops, and
  the trigger does nothing. Wind up to 3.7 V and it comes back.
- **Without one:** run an arm until it gets there. Tedious, but it also tells you
  your real runtime.
- **Single slow pulse = warning** (swap soon). **Double blink = shut down** (swap
  now). They're deliberately different at a glance.

The thresholds are `VBAT_WARN_MV` and `VBAT_CUTOFF_MV` in the firmware. Don't lower
the cutoff to squeeze out more runtime — under 3.0 V you are trading cell life for
a couple of minutes of bubbles.

### Checking for heat

Touch the boost module and MOSFET. Warm is fine, too-hot-to-touch is not — power
down and check for a short.

**If you can borrow a thermal camera, use it here instead.** It turns this step
from a fingertip guess into a measurement, and it shows you things a fingertip
misses:

- a boost module running hot because something downstream is shorted
- a MOSFET that turned out not to be logic-level, only half-opening and dissipating
  the difference
- a strip section drawing more than its neighbours

One borrowed session during bench test is plenty. You don't need to own one.

---

## Step 7 — Fit the bubbler

### First, understand what you actually have

The kit is not one object. It's a **bottle**, a **cap with a one-way valve**, and a
**blower head**, joined by silicone hose:

- **~50 mm of hose inside the bottle**, ending in the blue **gravity ball**. The
  ball sinks, so the pickup stays in solution at any arm angle — even inverted.
- **~50–70 mm of hose outside the cap**, feeding the blower head.

So the heavy thing (bottle) and the thing that must point past your fingertips
(blower head) **do not have to be in the same place.** That opens up a much better
mount — if the blower can pull solution far enough.

### The hose test — do this before you commit to a mount

Twenty minutes, one length of 3 × 5 mm silicone tube, and it decides the whole
mount design. Do it the day the kit arrives, before any of the soldering above.

1. Assemble the kit as supplied. Confirm it makes bubbles.
2. Replace the **outside** hose with about **150 mm** of 3 × 5 tube.
3. Run it again, held roughly the way your arm will hold it.

**Does it still make bubbles at the same rate?**

### If it passes → Mount C, bottle on the forearm

- **Bottle strapped to the forearm**, blower head at the knuckles pointing past
  your fingertips.
- Bubbles still appear to come from your fingers, so the comet illusion is intact.
- The heaviest item on the arm moves off the end of the lever, where it was costing
  you the most. This is the better build if you can get it.

### If it fails → Mount A, both on the back of the hand

- **Bottle and blower head both on the back of the hand**, exactly as the kit
  intends, nozzle past the fingertips.
- Works as shipped, no modification, no risk.
- Manage the weight instead:
  - **run the bottle half-full** — the field kit carries refills anyway
  - mount the bottle body **back toward the wrist**, cap forward, to shorten the
    lever arm
  - anchor to a **wrist strap**, not to glove fabric. A glove will not hold 200 g
    swinging for an evening

### Either way

- Check MakerWorld for existing mounts from the kit's collection as a starting
  point. Community CAD for the cap thread and the blower sleeve already exists.
- **The bubbler is its own module.** Give it a quick-release strap and make sure
  nothing about its mount bridges the wrist — if a rigid bottle spans that joint,
  the glove can't come off without removing the bottle first.
- **Rework the motor lead.** The kit ships the motor on a **PH2.0 female** plug
  that mates straight to the cell. Cut it off and fit a **JST-SM 2-pin** instead.
  This is not cosmetic: leave it PH2.0 and the cell can be plugged directly into
  the motor, bypassing the MOSFET, and the trigger does nothing.
- Use silicone wire for the motor run; it flexes constantly.
- A longer hose holds more solution, so dribble on shutdown gets slightly worse.
  The silicone sleeve over the cap's protrusion — the one-way valve — is what stops
  it emptying into your glove in a bag.

---

## Step 8 — Flash the firmware

1. Install the Arduino IDE, then add ESP32 board support (Boards Manager → search
   "esp32" → install the Espressif package).
2. Install the **FastLED** library (Library Manager → search "FastLED").
3. Select board: **XIAO_ESP32C3**.
4. Open `firmware/clown_arm/clown_arm.ino`.
5. **Edit the layout constants at the top** to match your measurements:

```cpp
constexpr int FOREARM_PX = 15;   // your forearm pixel count
constexpr int HAND_PX    = 6;    // your hand pixel count
constexpr int GAP_PX     = 5;    // umbilical length / 1.67 cm, rounded
```

`GAP_PX` is the **measured pixel-to-pixel distance across the umbilical**, from the
last forearm pixel to the first hand pixel, divided by 1.67 cm. Measure the finished
assembly from Step 3 — including the connector body, which is most of it. Around 8 cm
of umbilical gives `GAP_PX = 5`. Guessing here is what makes the comet look like it
stumbles at the wrist.

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

**If you built Mount C**, expect a slightly longer number. A 150 mm feed hose takes
marginally longer to prime than a 60 mm one, and that delay lands between the
trigger and the first bubble.

While you're here, `COMET_REPEAT_MS` sets how often a new comet launches while
you hold the trigger. Lower = a denser, more frantic stream.

---

## Step 10 — Mount into the glove and sleeve

Now the strip goes in.

### Choosing and testing the fabric

The fabric spreads the light into a smooth continuous glow instead of visible
dots — which is a genuine upgrade over an exposed strip, **if** the fabric
cooperates.

- **Thin, pale, stretchy fabric** glows beautifully.
- **Thick or dark fabric**, especially leather, swallows almost all of it.

Before committing, hold a powered section of strip under a scrap or under the
glove itself in a dark room. If you can't see it clearly, no amount of firmware
will fix it — get a different glove. **Test the sleeve at the same time**; there's
no point in a glove that glows and a sleeve that doesn't.

**Building the lace concept?** [DESIGN.md](DESIGN.md) overrides this section. Lace
is open mesh — light goes straight through the holes and the strip stays visibly a
strip. You either lean into that or add a diffuser layer underneath. Decide before
you cut into the gloves.

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
- Run the forearm section under the sleeve or arm warmer, same principle.

### Connectors and strain relief

- **The connector is never the anchor.** Tack the cable to the garment on *both*
  sides of every plug, so a snag pulls the tack rather than the latch.
- Leave a **service loop** either side of every connector.
- Add strain relief where wires cross the elbow and wrist — a small loop of wire
  tacked down on each side of the joint, so movement pulls on the tack rather than
  the solder joint.
- **A smear of dielectric grease** in each connector shell keeps soap residue from
  corroding the contacts over a season. Intermittent faults from green contacts are
  miserable to diagnose.
- Position the mated plugs where they **won't be pressed against your skin** by a
  tight sleeve. A 20 mm plastic body under a cuff for six hours is uncomfortable.
- **Sealing comes next.** Step 11 covers wrapping the mated plugs, which way they
  should face, and why the wrist plug sits above the cuff rather than under it.

---

## Step 11 — Seal it against the soap

The build used to assume the pod sits on your upper arm, **above** the spray. That
assumption holds on a bench and fails at a rave, where your arms go up. Point a
bubble gun at the ceiling for four hours and the pod is no longer above anything.

So: assume every surface of this costume gets wet, from every angle, all night.

### What actually gets in

- **Arms overhead.** Solution runs *down* the arm, straight at the pod and into
  any opening that faces up.
- **Blowback.** The blower atomises solution. A fine soapy mist settles on
  everything within a metre, including the inside of any vent you left open.
- **Wicking.** This is the one people miss. Soap film creeps *along wire
  insulation*, into a connector shell, and out the other end, hours after the
  splash that started it. Sealing the box is not enough if the wires are a wick.
- **Other people.** Hands go up, drinks get waved, and someone will absolutely
  grab your forearm.
- **Condensation.** Warm arm, cold night, sealed box. Water forms *inside* a
  perfectly sealed enclosure with no help from the outside.

Dried bubble solution is also mildly conductive and hygroscopic — it pulls
moisture back out of the air, so a "dry" residue across two pins is a leakage path
that comes back every humid night until you clean it off.

### The rule: drain it, don't hermetically seal it

Chasing a watertight box is the wrong target. You cannot get there with an FDM
print, a USB port and six wires leaving the case, and if you *did*, condensation
would defeat you from the inside.

Aim for this instead:

- Nothing that gets in can **pool** on a board
- Everything that gets in has a **way out at the bottom**
- Everything that gets in **dries** between events

### The pod enclosure

- **PETG, not PLA.** PLA goes soft in a hot car and is brittle where this part
  wants to flex under a strap.
- **Four perimeters, 1.6 mm walls minimum.** Thin FDM walls leak through the layer
  lines themselves, gasket or no gasket.
- **A lid with a gasket groove**, closed with four M3 screws into heat-set inserts.
  2 mm silicone O-ring cord in the groove, or closed-cell foam tape if you'd rather
  not model a groove. Both are fine; nothing sticky, because you will open this.
- **Every opening faces down or aft.** Nothing on the top surface. Nothing on the
  fingertip-facing end.
- **A 2 mm drain hole at the lowest corner**, as the box sits on your arm, plus a
  second small hole at the opposite high corner so it can breathe. Yes, this is a
  hole in your waterproof box. It is the difference between a box that drains and a
  box that holds a puddle against your protoboard.
- **Cable entry through a grommet**, on the underside, and **a drip loop on every
  wire leaving the pod** — a downward loop below the entry point, so water running
  along the insulation reaches the bottom of the loop and drips off instead of
  tracking into the case.
- **A silicone plug or a hinged flap over the USB-C port.** It has to stay
  reachable (you will reflash this constantly) and it has to be shut by default.

### Conformal coat the board

The enclosure is the first line, not the only one. A thin coat of clear acrylic
conformal spray over the assembled protoboard turns a soaked board into one you
rinse, dry and keep using.

- **Mask before you spray:** the USB-C connector, the boost module's trimpot, the
  MOSFET tab, every connector housing, and the microswitch.
- Two thin coats beat one thick one.
- **Do it after the bench test passes**, not before. Coating a board you then have
  to rework is miserable.
- Clear RTV dabbed over the solder joints on the strip's cut ends does the same job
  at the wet end of the arm.

### The battery gets its own sealed compartment

The cell is the part that hurts you if this goes wrong, so it gets treated
separately from everything else:

- **A wall between the cell and the electronics**, so a vented or leaking cell
  doesn't take the board with it, and so soap that gets into the sled compartment
  during a swap doesn't reach the XIAO.
- **The sled's tabs get heat-shrink** over the solder joints. A bare tab and a
  stray strand of wire is a dead short across a lithium cell, an inch from your
  skin.
- **Nothing metal in the compartment.** No stray screws, no washers, no snipped
  lead ends. Check it every time you close it.
- **Check the cell's own wrap** before every event. A nicked 18650 shrink-wrap
  exposes the can, which is the negative terminal over the whole body of the cell —
  that's how a cell shorts against something it's only *resting* on. Re-wrap any
  cell whose sleeve is torn; they cost almost nothing.
- **The sled lid closes positively** — a click, a screw, or a strap — and opens
  without a tool.

### The trigger is the leakiest part of the build

A bare lever microswitch in your palm, under a glove, in soapy water, is not a
sealed part. Options, cheapest first:

- **A printed pocket with a silicone or nitrile membrane** over the lever. A scrap
  of a nitrile glove, stretched and glued around the rim, passes the press through
  and keeps the liquid out.
- **A sealed (IP67) microswitch**, if you can get one with the same lever.
- **Either way, the ZH-2 pigtail joint gets sealed** — heat-shrink over the solder,
  and a smear of dielectric grease in the shell.

### The connectors

- **Grease every shell** — you were doing this anyway for corrosion; it also keeps
  water out of the contacts.
- **Wrap each mated plug** in a turn of self-amalgamating silicone tape. It fuses
  to itself, takes no adhesive with it when you unwrap it, and comes off in one
  piece when you need to unplug.
- **Point the plug down**, or at worst sideways. A shell facing up is a cup.
- The wrist SM-5 sits **above the cuff**, not under it — a cuff channels solution
  straight into the plug.

### Test it before you trust it

With the arm assembled, sealed, and **powered** (this is the point — an unpowered
box tells you nothing about tracking or shorts):

1. Hold it overhead, the way you'd actually fire it.
2. Spray it all over with a spray bottle of the real bubble solution for a full
   minute, from above, from the sides, and at the connectors.
3. Fire the trigger a dozen times through the wetting.
4. Leave it for ten minutes, still powered, still wet.
5. Open it. **Look for water inside, and for water *tracking* along the inside of
   the wire entry.** Both mean you move the entry point or add a drip loop.

### After every event

- **Cell out. SW1 off first, then the cell.**
- Open the pod and leave it open overnight. A sealed damp box is worse than an open
  damp box.
- Rinse the blower head and cap in warm water — dried solution glues the one-way
  valve shut.
- Wipe soap residue off every connector that got sprayed, and re-grease it. Dried
  residue is conductive when the humidity comes back.

---

## Step 12 — Build the second arm

Repeat Steps 1–11.

Two things to be careful about:

- **Pixel 0 goes at the elbow on this arm too.** It's tempting to mirror the wiring
  along with the physical build. Don't. Identical wiring means identical firmware
  means one thing to maintain.
- **Keep the same SM-5 and SM-6 pin conventions.** If arm A puts the trigger on
  pins 4–5 and arm B puts it on pins 1–2, then spares aren't spares, and one
  wrong plug at an event costs you a board. Write the pinout on a bit of tape
  inside each pod.

---

## Step 13 — Assemble the costume

Both arms exist. This step is about the thing you actually wear.

### Both-arms checkout

With both arms built, before any event:

1. **Cells out of both pods.**
2. Mate every connector on both arms. Count them: 4 per arm — elbow SM-6, elbow
   SM-2, wrist SM-5, wrist SM-2 — plus the ZH-2 at each microswitch.
3. Cells in. Both arms should show the idle glow.
4. **Fire each hand separately.** Left trigger drives left arm only; right drives
   right only. If one trigger fires the other arm, you have crossed something —
   there is no cross-arm wiring in this design.
5. Fire both at once. Watch for either arm dimming or glitching. They're
   electrically independent, so they shouldn't interact at all; if they do, suspect
   a shared ground you didn't intend.
6. Run both for the length of a bottle of solution. That's your real duty cycle.

### Getting into it

**Order matters. Cells go in last, always.**

1. Pods on the upper arms, strapped, cells **out**, `SW1` **off** on both.
2. Sleeves on. Mate the elbow SM-6 and SM-2 on each side.
3. Gloves on. Mate the wrist SM-5 on each side.
4. Bubblers strapped on, mate the wrist SM-2, bottles filled.
5. **Cells in, then `SW1` on.** Check both idle glows before you walk out.

### Getting out of it

Reverse. The whole point of the build:

1. **`SW1` off, then cells out.** Both arms are now dead and safe to unplug.
2. Wrist SM-2 + bubbler strap → bubblers off, bottles go somewhere upright.
3. Wrist SM-5 → gloves peel off.
4. Elbow SM-6 + SM-2 → sleeves come off.
5. Pod straps.

Four releases per arm, none of them needing a second person or a flat surface.

### If something goes wrong mid-event

In order, fastest first:

1. **`SW1` off.** One motion, through the costume, no looking. The arm is dead.
2. **Cell out.** Sled lid, plug, done. Now it's inert and you can carry it.
3. Only then work out what happened.

Practise both. If either takes more than a few seconds with one hand, fix the pod
before the event — that's step 11's job, not the night's.

### The test that matters

> Can you get out of it alone, in a bathroom, with soapy hands, in under a minute?
> And can you kill and remove either battery, one-handed, in under ten seconds?

If not, something is still soldered that shouldn't be, or a strap is fighting a
connector. Fix it before the event, not at it.

### Care afterwards

- **Cells out** for storage. Never store the costume with cells connected. `SW1`
  off is not storage — a switch can be knocked on in a bag.
- **Open the pods and let them dry** before they go away. See step 11.
- Rinse the blower head and cap in warm water; dried bubble solution glues the
  one-way valve shut.
- Leave the silicone sleeve on the cap protrusion so the bottle doesn't empty into
  your bag.
- Wipe soap residue off any connector that got sprayed, and re-grease it.

---

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Nothing lights at all | Check common ground. Check boost output is ~5V. Check strip DIN is on the *input* end (follow the arrows) |
| Nothing lights, and it worked yesterday | Check every connector is fully latched. A half-seated SM plug looks mated |
| Works until you move your arm | Unseated connector, or a crimp that didn't take. Beep through each pin while wiggling |
| First pixel wrong color, rest fine | Missing or wrong-value data resistor |
| Pixel 0 died after a reconnect | Strip was plugged in live. Cell out before mating, every time |
| Random flickering, especially when moving | Missing 74AHCT125, or a loose ground. Check SM-6 pin 6 is actually tied to ground at both ends |
| 74AHCT125 runs warm with nothing obviously wrong | Unused inputs floating. `3A`/`4A` to ground, `3OE`/`4OE` to Vcc (Step 4) |
| Comet runs fingertips → elbow | Strip is reversed. Fix the wiring, not the code |
| Comet "jumps" or stalls at the wrist | `GAP_PX` doesn't match your measured umbilical length |
| Colors wrong (red/green swapped) | Change `GRB` to `RGB` in the `addLeds` line |
| Motor whines audibly | PWM frequency dropped below 20 kHz — check `MOTOR_PWM_HZ` |
| Motor doesn't spin | MOSFET gate not driven, or a non-logic-level MOSFET |
| Motor spins weakly, MOSFET gets hot | Gate driven at 3.3V instead of through the 74AHCT125, or it's an IRF520 — not a logic-level part |
| Motor runs constantly, trigger does nothing | Motor still on its factory PH2.0 lead, plugged straight to the cell. Rework it to SM-2 (Step 7) |
| Everything dies when the motor starts | Battery sagging, or the polyfuse tripping. Check the cell's charge |
| Lights work, then die after a few minutes | Battery protection circuit cutting out — recharge or swap the cell |
| Elbow pixel pulsing red, slow single pulse | Low-battery warning. Swap the cell soon |
| Elbow pixel double-blinking red, motor dead, trigger does nothing | Low-voltage shutoff latched at 3.0 V. Swap the cell; it clears itself |
| Blower twitches or kicks every time you power up or reflash | Missing gate pulldown. Measure gate to source — it should not read open (Step 4) |
| Laptop warns about a USB device drawing power, or the pod stays alive with the cell out and USB in | Missing or reversed `D2`. The pack is backfeeding the host port (Step 4) |
| Arm completely dead, cell freshly charged | `SW1` off, or its DC rating gave out. Check the switch before you suspect the board |
| It worked, got sprayed, now behaves oddly | Soap tracking across pins. Kill `SW1`, open it, rinse with isopropyl, dry fully. Then step 11 |
| One trigger fires the other arm | Not possible by design — you've cross-plugged two arms. Check each arm is self-contained |
| Board won't accept uploads | Hold BOOT while plugging in USB. If the port isn't recognised at all, suspect a charge-only USB-C cable |
| Strip goes dark past the wrist | Cracked trace or failed umbilical joint — this is the failure mode the umbilical exists to prevent |
| Bubbles weak or intermittent | Gravity ball not in solution, or the feed hose is too long. See the Step 7 hose test |
| Bubbles stop but motor runs | Bottle empty, or dried solution in the one-way valve. Rinse the cap |

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
| `VBAT_WARN_MV` / `VBAT_WARN_CLEAR_MV` | When the low-cell warning starts and stops. Keep them apart — that gap is the hysteresis that stops the warning strobing |
| `VBAT_CUTOFF_MV` | Where the arm shuts itself down. Raising it is fine; lowering it costs cell life |

### Going further

The XIAO ESP32-C3 has Wi-Fi and Bluetooth sitting unused. Natural next steps, in
rough order of effort:

- **More patterns** — a second animation, and a long-press to cycle between them.
- **ESP-NOW sync** — let either arm's trigger *also* fire the other, for a
  two-handed blast. Note this is **additive**: each hand keeps its own trigger and
  its own arm. It's a second way to fire, not a replacement for the second trigger.
- **Phone control** — a small web page served by the board to change color and
  speed live, without a laptop.

None of these need extra hardware. They're already paid for.

---

## Field kit

Things to have with you when you actually wear this:

- Spare charged 18650 per arm, on its PH2.0 pigtail, **each in its own plastic
  case** — never loose in the bag
- **A pre-made spare wrist umbilical** — now genuinely swappable, since both ends
  are connectors
- A spare microswitch, already on its ZH-2 pigtail
- One spare SM pigtail pair of each size
- Extra bubble solution — **this runs out long before the battery does**
- Spare 3 × 5 silicone tube, in case a feed hose splits
- A solder pen, for repairs you can't connector your way out of
- A small screwdriver and some electrical tape
- **Self-amalgamating silicone tape**, for re-wrapping a plug you had to open
- A few **cable ties or a spare strap** — a pod that works loose ends up pointing
  its openings upward
- **Isopropyl and a cloth.** Wiping dried solution off a connector at the venue is
  the difference between one dead arm and two

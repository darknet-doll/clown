# Parts List

## How to read the quantities

Every part below carries **two numbers**:

- **Per arm** — what one arm needs
- **Buy** — what to actually put in the basket for the whole costume

They are different, and confusing them is the single easiest way to end up
halfway through a build with one glove. **The costume is two arms.** Tools are
marked `buy 1` because you only need one soldering iron, not one per arm.

Format for each part:

- **Is** — what the object actually is
- **Does** — its job in the circuit
- **Skip it →** the exact way it breaks

Read order if you're new:

1. This file — what the parts are
2. [BUILD.md](BUILD.md) — how they go together
3. [README.md](README.md) — why the design is shaped this way

---

## About the buy links

Each part below has a **Suggested product** line pointing at a real Amazon listing.

- **What I checked:** the listing exists and its spec matches what this build needs
- **What I could not check:** price, current stock, and whether it ships to Bothell
  - Amazon serves automated requests a page with no price, stock or delivery data,
    and a delivery estimate needs a signed-in session with your address set
  - **Confirm all three in your cart before ordering.** Treat these as "this is the
    right part," not "this is in stock today"
- Where the part is a pure commodity and brand genuinely doesn't matter, the link is
  a search rather than one listing
- The bubble kit is **not on Amazon** — it comes from Bambu's own store

---

## Shopping list

Everything, in one table. Details and reasoning are in the sections below.

| Part | Per arm | **Buy** |
|---|---|---|
| Bambu Electric Bubble Maker Kit 01 | 1 | **2** |
| Bottle, 24T or 30T neck | 1 | **2** + a spare |
| Silicone tube, 3 × 5 mm | — | **1 m** |
| Bubble solution | — | **as much as you can carry** |
| WS2812B strip, 60/m, 5V, IP65, black PCB | 0.4 m | **1 m roll** |
| Thin pale stretchy glove | 1 | **a pair** |
| Sleeve or arm warmer | 1 | **a pair** |
| Seeed XIAO ESP32-C3 | 1 | **2** |
| 74AHCT125 level shifter | 1 | **2** (buy 5, they're cheap) |
| MOSFET module (AO3400 / IRLZ44N) | 1 | **2** |
| 1N5819 diode | 1 | **2** (buy 10) |
| Protected 18650 cell | 1 | **2 in use + 2 spares** (2 come free in the kits) |
| 18650 sled with leads | 1 | **2** |
| 5V boost module | 1 | **2** |
| 2A polyfuse | 1 | **2** (buy 5) |
| 100 kΩ resistor | 2 | **4** |
| 1000 µF capacitor | 1 | **2** |
| 330–470 Ω resistor | 1 | **2** |
| Lever microswitch | 1 | **2 + 2 spares** |
| JST-SM pigtail pair, 6-pin | 1 | **2 + 1 spare** |
| JST-SM pigtail pair, 5-pin | 1 | **2 + 1 spare** |
| JST-SM pigtail pair, 2-pin | 2 | **4 + 2 spares** |
| JST-ZH pigtail pair, 2-pin, 1.5 mm | 1 | **2 + 2 spares** |
| Protoboard, small | 1 | **2** |
| Silicone hookup wire 22–26 AWG | — | **one assortment covers both** |
| Heat-shrink, assorted | — | **one assortment covers both** |
| Hot glue sticks or clear RTV silicone | — | **1** |
| Dielectric grease | — | **1 small tube** |
| Needle and thread, or fabric glue | — | **1** |
| Fabric marker pen | — | **1** |
| USB-C cable, **data capable** | — | **1** |

Tools, one of each: soldering iron, flux-core solder, flux pen, wire strippers,
side cutters, heat gun, multimeter, 3D printer. Thermal camera optional but very
useful — see [Tools](#tools).

---

## The bubbles

### Bambu Lab Electric Bubble Maker Kit 01 (P6M) — 1 per arm · **buy 2**

- **Is:** blower head + one-way-valve bottle cap + silicone hose + gravity ball
- **Does:** draws solution up the hose and blows air across it → bubbles
- **You modify:** only the motor's connector
  - Kit ships the motor on a **PH2.0 female** plug, which mates straight to the cell
  - You cut that off and fit a **JST-SM 2-pin** instead, so the MOSFET sits in between
  - See [Connectors](#connectors) for why that swap is not optional
- **Also in the box, and you use both:**
  - one protected 18650 cell, on a PH2.0 pigtail
  - a USB charger with a matching PH2.0 lead
- **Not in the box:** the bottle. See below
- Two kits → two blower heads + two cells. One per arm
- **Suggested product:** not sold on Amazon —
  [Bambu Lab US store](https://us.store.bambulab.com/products/electric-bubble-maker-kit-01)

### How the kit actually works

Worth understanding before you design a mount, because it isn't what you'd guess:

- A **50 mm hose inside the bottle** ends in the blue **gravity ball**
  - the ball sinks, so the pickup finds solution at any arm angle, even inverted
  - this is why an arm-mounted bottle works at all
- A **50–70 mm hose outside the cap** feeds the blower head
  - so the **blower head is already a separate object from the bottle**, joined by tube
  - the bubbles form at the head, not at the cap
- **This is the key fact for mounting.** The heavy thing (bottle) and the thing that
  must point past your fingertips (head) do not have to be in the same place
- [BUILD.md](BUILD.md) step 7 has a twenty-minute test that decides your mount

### Bottle, 24T or 30T neck — 1 per arm · **buy 2 + a spare**

- **Is:** the solution reservoir the kit's cap screws onto
- **Not included in the kit.** Bambu says explicitly: do not use a drinking bottle
- **Pick deliberately** — this is your main lever on arm weight
  - full bottle + solution is the heaviest single item on the arm
  - a small bottle refilled often beats a big bottle carried all night
- Community CAD for the thread and blower sleeve exists on MakerWorld if you want
  to print a custom one
- **Suggested product:** measure your cap first, then
  [search 24/410 or 30/410 PET bottles](https://www.amazon.com/s?k=24-410+30-410+plastic+bottle+with+cap)
  — 24T/30T is the thread callout, and bottle listings usually say 24/410 or 30/410

### Silicone tube, 3 × 5 mm — **buy 1 m**

- **Is:** 3 mm inside, 5 mm outside — same as the hose in the kit
- **Does:** lets you extend the feed hose so the bottle can sit on your forearm
- Also a field spare. Stock aquarium/lab tubing, costs almost nothing
- Used in the step 7 mount test
- **Suggested product:**
  [search 3mm ID x 5mm OD silicone tubing](https://www.amazon.com/s?k=silicone+tubing+3mm+ID+5mm+OD)
  — any food-grade roll; you need about a metre

### Bubble solution — **buy as much as you can carry**

- This runs out long before the battery does. It is the actual limit on your night

---

## The lights

### WS2812B LED strip, 60 LED/m, 5V, black PCB, IP65 — 0.4 m per arm · **buy a 1 m roll**

- **Is:** ribbon of lights, each with its own tiny chip inside
- **Does:** lets you set every light separately, down one single data wire
  - That's what "addressable" / "programmable" means
  - Normal strips = one colour all at once → no travelling comet possible

Why these exact specs:

- **60 LED/m** → 1.67 cm apart
  - dense enough to blur into a smooth streak under fabric
  - not visible dots
- **5V** → same supply as everything else
  - avoid 12V strips (WS2815) — needs a second power system
- **Black PCB** → invisible against dark fabric when off
- **IP65** (clear silicone sleeve) → waterproofing
  - you are spraying soapy water down your own arm

**Suggested product:**
[Luopan WS2812B, configurable](https://www.amazon.com/WS2812B-pixels-WS2812-Decorative-Lighting/dp/B0CG5V735Q)
— select **1 m / 60 LEDs / black PCB / IP65**. Read the option dropdown carefully;
this listing also sells 30 and 144 LED/m and IP30, which are the wrong parts.

**Alternative:** SK6812 RGBW

- drop-in swap
- adds a real white LED per pixel → better "charging up" glow
- slightly more forgiving on data timing
- costs a bit more

---

## The brain

### Seeed XIAO ESP32-C3 — 1 per arm · **buy 2**

- **Is:** a whole computer, 21 × 17.5 mm
- **Does:** ~60×/second, decides
  - the colour of all 21 pixels
  - whether the motor runs
- **Watches:** the palm trigger on its own arm
- **Why this board:**
  - tiny → hides on your upper arm
  - takes 5V in directly
  - Wi-Fi + Bluetooth built in (unused in v1, free for later)
- **Reprogram:** USB-C cable — a **data** cable, not a charge-only one
  - **keep that port reachable** in the printed pod → see [BUILD.md](BUILD.md)
- **Suggested product:**
  [Seeed XIAO ESP32C3, 3-pack](https://www.amazon.com/XIAO-ESP32C3-3PCS-Pack-Bluetooth5-0/dp/B0DGX3LSC7)
  — two arms plus a spare, which you will want the first time you kill a pin

### 74AHCT125 level shifter chip — 1 per arm · **buy 2** (get 5, they're cheap)

- **Is:** a translator that also shouts
- **Problem it fixes:**
  - brain speaks at 3.3V
  - strip listens for 5V
  - strip *sort of* hears 3.3V — which is the trap
- **Does:** repeats the brain's 3.3V signal at a confident 5V
- **Skip it →** lights flicker, glitch, wrong colours, at random
  - worse with longer wire runs
  - fine on your bench, haunted at the party
  - #1 cause of "my LED strip is possessed"
- **Suggested product:**
  [Juried Engineering SN74AHCT125N, DIP-14, 5-pack](https://www.amazon.com/Juried-Engineering-SN74AHCT125N-SN74AHCT125-Breadboard-Friendly/dp/B08FHD994N)
  - or [Adafruit ADA1787, single](https://www.amazon.com/Adafruit-Accessories-Quad-Level-Shifter-piece/dp/B00XW2L39K)
    if you would rather buy the known-good one twice
- **You use one of its four gates for the strip.** Keep the chip in mind — the
  MOSFET section below has a use for a second gate

---

## The motor control

### N-channel logic-level MOSFET — 1 per arm · **buy 2**

- **Is:** an electrical switch, no moving parts
- **Problem it fixes:** brain can decide, but can't push enough current to spin a motor
  - like asking someone to lift a car
- **Does:** brain flicks this switch → switch lets big current through from battery

#### Do not buy the obvious module

Search "MOSFET module Arduino" and the top result is almost always an **IRF520
driver module**. It is the wrong part and it will half-work, which is worse than
not working:

- IRF520 is **not logic-level** — its gate threshold runs as high as 4 V and it
  wants ~10 V to open fully
- Your XIAO drives the gate at **3.3 V**. The FET partly opens, dissipates the
  difference as heat, and the blower runs slow and inconsistently
- This is exactly the failure the old wording ("non-logic-level → only half-opens,
  gets hot") warned about — and the default purchase walks straight into it

#### Gate voltage is the real constraint

Even genuine logic-level parts are usually specified at **Vgs = 5 V**, not 3.3 V:

| Part | Rated on at | At 3.3 V gate |
|---|---|---|
| IRF520 | ~10 V | **barely on. Don't.** |
| IRLZ44N | 5 V | marginal — works, runs warmer than it should |
| RFP30N06LE | 5 V | marginal, same story |
| AO3400 | **2.5 V** | fully on. Correct for direct 3.3 V drive |

#### The fix that costs nothing

**Drive the gate from 5 V using a spare gate on the 74AHCT125 you already have.**

- The level shifter has **four** gates and the strip uses one
- Route `D2` through a second gate, exactly as you route the LED data through the first
- The MOSFET then sees a clean 5 V gate signal, and IRLZ44N or RFP30N06LE become
  fully-on parts instead of marginal ones
- No new components, no extra cost. See [BUILD.md](BUILD.md) step 4

**Suggested product**, pick one path:

- **Direct 3.3 V drive** — get an **AO3400**-based module and check the listing
  actually names AO3400, not IRF520
- **5 V gate drive** (recommended) —
  [Cylewet RFP30N06LE logic-level TO-220, 6-pack](https://www.amazon.com/Cylewet-RFP30N06LE-N-Channel-Control-Arduino/dp/B073D399M1).
  Bare transistors, so add a **100 Ω** gate series resistor and a **10 kΩ**
  gate-to-source pulldown — both come from the resistor kit below

> Note this supersedes the older "buy a module, not a bare chip" advice. That was
> sound in principle, but the modules actually on sale are the wrong transistor.

### 1N5819 flyback diode — 1 per arm · **buy 2** (get 10)

- **Is:** a one-way valve for electricity
- **Problem it fixes:** a motor is a big coil
  - cut power to a coil → it kicks back a high-voltage spike into your circuit
- **Does:** gives that spike a safe loop to run around until it dies out
- **Skip it →** MOSFET eventually dies, maybe takes the brain with it
- Costs ~20¢. Fit it
- **Suggested product:** [search 1N5819 Schottky diodes](https://www.amazon.com/s?k=1N5819+schottky+diode)
  — any bag of 10 or more; they're pennies each

---

## Power

### Protected 18650 battery — 1 per arm · **buy 2 in use + 2 spares**

- **Is:** rechargeable cell, same kind as in a laptop pack or a vape
- One comes free with each bubble kit, already on a **PH2.0 pigtail**
- **Keep that pigtail.** It's how the cell plugs into both the pod and the charger
- **"Protected" =** tiny guardian circuit in the end of the cell
  - cuts off if drained too far or charged too hard
  - over-drained lithium can be damaged or genuinely unsafe
- Cells in the bubble kit are protected ones
- **Do not substitute unprotected cells** to save money
  - this is strapped to your arm
- **Suggested product:** two arrive free with the kits. For spares,
  [search protected 18650 button-top cells](https://www.amazon.com/s?k=protected+18650+battery+button+top)
  — the listing must say **protected**; most cheap 18650s are not

### 18650 battery sled / holder with wire leads — 1 per arm · **buy 2**

- **Is:** the slot the cell sits in
- **Does:** lets you swap a flat cell for a fresh one, no soldering iron
- Print an enclosure with a lid that clicks shut
  - you don't want it ejecting mid-performance
- **Suggested product:**
  [search single-slot 18650 holder with wire leads](https://www.amazon.com/s?k=18650+battery+holder+single+slot+wire+leads)

### 5V boost converter module — 1 per arm · **buy 2**

- **Is:** a pump, but for voltage
- **Problem it fixes:** cell makes ~3.7V, brain + LEDs need 5V
- **Does:** pumps 3.7V up to a steady 5V
- **Only feeds lights + brain (~0.3 A)**
  - motor runs straight off the battery instead
  - so a small cheap module is genuinely fine here
- **Suggested product:**
  [Dorhea MT3608 step-up, 10-pack](https://www.amazon.com/MT3608-Converter-Adjustable-Voltage-Regulator/dp/B0BGLGL9RV)
  — **it is adjustable, so set it to 5.0 V with the trimpot and verify on the meter
  before you connect the XIAO.** Out of the bag it can be anything

### 2A resettable fuse (polyfuse / PPTC) — 1 per arm · **buy 2** (get 5)

- **Is:** a safety valve that resets itself
- **Does:** on a current spike, suddenly becomes very resistant → chokes the flow
  - before anything catches fire
- Let it cool → back to normal by itself
- Cheap insurance for a lithium cell worn against your body
- **Suggested product:** [search 2A PPTC resettable fuse](https://www.amazon.com/s?k=PPTC+resettable+fuse+2A+radial)

### Two 100 kΩ resistors (battery monitor) — 2 per arm · **buy 4**

- **Is:** two resistors forming a "divider"
- **Problem it fixes:**
  - brain can only safely measure up to ~3.3V
  - full cell is 4.2V
- **Does:** shrinks battery voltage neatly in half → safe to read
- **Gets you:** costume pulses red when the battery is nearly flat
  - instead of dying with no warning
- **Suggested product:** buy an assortment, not singles —
  [search 1/4W metal film resistor kit](https://www.amazon.com/s?k=metal+film+resistor+assortment+kit+1%2F4W)
  — one kit covers the 100 kΩ pair, the 330–470 Ω data resistor, and the 100 Ω / 10 kΩ
  the MOSFET gate wants

---

## Signal conditioning

### 1000 µF electrolytic capacitor — 1 per arm · **buy 2**

- **Is:** a tiny water tank for electricity
- **Problem it fixes:** many LEDs switching on at once all gulp power at the same instant
- **Does:** holds a reserve, smooths the gulp → voltage doesn't dip and confuse the brain
- **Watch out:** polarised
  - one leg marked negative → must go to ground
  - backwards, electrolytics pop
- **Suggested product:**
  [search 1000uF 16V electrolytic capacitors](https://www.amazon.com/s?k=1000uF+16V+electrolytic+capacitor)
  — 10 V would technically do, but 16 V or 25 V costs the same

### 330–470 Ω resistor — 1 per arm · **buy 2**

- **Is:** a speed bump on the data wire
- **Does:** softens the signal's sharp edge
  - so it doesn't bounce back down the wire and garble the message to the first LED
- **Skip it →** the *first* pixel misbehaves — wrong colour or flickering
  - every pixel behind it stays fine

---

## The trigger

### Snap-action microswitch, lever type — 1 per arm · **buy 2 + 2 spares**

- **Is:** clicky button with a small metal arm sticking off it
- **One per hand.** Each hand fires its own arm — nothing crosses the torso
- **The arm is the point:**
  - wide press area
  - squeeze fingers into your palm mid-performance and hit it every time
  - **no looking, no aiming**
  - a plain round button = hunting for a 12 mm target by feel
- **Bonus:** crisp physical click → you feel that it fired
- **Suggested product:**
  [Saim long hinge lever microswitch, 10-pack](https://www.amazon.com/Saim-Momentary-Switch-Roller-Action/dp/B01NBK00FD)
  — wire **COM** and **NO**; ignore the NC terminal
- **Prefer the plain lever over the roller version.** A roller is a hard point that
  presses into your palm for hours. If the only listing you can get has rollers, the
  roller pops off most of these

---

## Connectors

The costume comes apart into **four modules per arm**, so you can get out of it
alone, with soapy hands, without turning into a pretzel. Nothing is soldered end
to end across a joint.

| Module | Holds | Unplugs at |
|---|---|---|
| **Pod** (upper arm) | brain, boost, shifter, MOSFET, fuse, sled | battery plug + straps |
| **Sleeve** (forearm) | forearm strip, 15 px | elbow, SM 6-pin + SM 2-pin |
| **Glove** (hand) | hand strip 6 px, trigger | wrist, SM 5-pin |
| **Bubbler** | bottle, cap, hose, blower head | wrist, SM 2-pin + its strap |

### The connectors themselves

| Boundary | Carries | Connector | Per arm · **buy** |
|---|---|---|---|
| Cell ↔ pod, cell ↔ charger | 2 | **JST-PH 2.0, 2-pin** *(already on the cell)* | — |
| Pod → sleeve, at the **elbow** | strip 3 + trigger 2 + spare GND | **JST-SM 6-pin** | 1 · **2 + 1** |
| Motor run, at the **elbow** | motor 2 | **JST-SM 2-pin** | 1 · **4 + 2** |
| Sleeve → glove, at the **wrist** | strip 3 + trigger 2 | **JST-SM 5-pin** | 1 · **2 + 1** |
| Motor run, at the **wrist** | motor 2 | **JST-SM 2-pin** | *(same bag as above)* |
| Microswitch pigtail | switch 2 | **JST-ZH 1.5 mm, 2-pin** | 1 · **2 + 2** |

**Both the trigger and the motor have to reach the pod from the hand**, so both
cross *both* joints. That's why the elbow plug is 6-pin, not 3-pin — it carries
the strip, the trigger, and a second ground.

- Buy them as **pre-wired pigtail pairs**. No crimp tool, no housings to assemble
- All of them latch. None of them is friction-only

**Suggested products:**

| Need | Listing |
|---|---|
| SM 6-pin | [ACTOO 6-pin JST-SM, 10 pairs](https://www.amazon.com/ACTOO-Connector-Female-Terminal-Adapter/dp/B07YWHCPW5) |
| SM 5-pin | [BTF-LIGHTING 5-pin JST-SM, 10 pairs](https://www.amazon.com/BTF-LIGHTING-Pairs-Female-Connector-Flexible/dp/B01DC0KNY2) |
| SM 2-pin | [VANDESAIL 2-pin JST-SM, 20 pairs](https://www.amazon.com/VANDESAIL-Connector-Adapter-Electrical-Female/dp/B0CQX8D3QR) |
| ZH 2-pin, 1.5 mm | [XUGERIP JST-ZH 1.5 mm 2-pin, 20 pairs](https://www.amazon.com/XUGERIP-1-5mm-Male-Female-Connector/dp/B0D9SN5BTP) |

- These are sold in bulk packs because that's how they come. You'll use the spares
- **Check the ZH listing says 1.5 mm.** ZH, SH and PH all get called "JST micro" by
  sellers, and the whole point of this part is that it cannot mate with PH

### Why these specific ones

- **JST-SM** is the LED-strip inline connector. It has a real clicking latch, it's
  sold as male/female pigtail pairs by the bag, and it's flat enough to hide under
  a cuff (~20 × 7 × 5 mm)
- The **wrist 5-pin carries the strip's 3 conductors plus the trigger's 2**, so the
  whole glove comes off with one pull
- The **elbow 6-pin** carries the same five plus a **second ground**. The elbow run is
  the longest in the costume and carries the whole strip's current; doubling the
  ground conductor cuts the voltage drop and gives the data line a better return
- The **motor gets its own 2-pin**, deliberately not bundled with the data line.
  ~1 A of PWM alongside a WS2812 data wire is asking for trouble. Twist the motor
  pair anyway
- The **cell keeps its factory PH2.0**. That's what the kit's charger mates to, so
  a flat cell goes pod → charger with no adapter and no rework. PH2.0 is rated 2 A
  and your peak is about 1.3 A — and the kit already runs the blower's own
  0.5–1.0 A through that same connector

### The rule that prevents the expensive mistake

> **No two connectors on one arm may share both family and pin count.**

- Check it against the table: PH-2 · ZH-2 · SM-2 · SM-5 · SM-6
- The three 2-pin plugs are **different families** — PH is 2.0 mm pitch, ZH is 1.5 mm,
  SM is 2.5 mm. None of them will mate with either of the others
- **The one deliberate exception:** the motor's two SM-2 plugs, at the elbow and at
  the wrist, are identical. That's safe *by construction* — they sit on the same net,
  so cross-mating them just shortens the motor run. Nothing else in the build has
  that property
- **This is why the trigger pigtail is ZH and not PH.** Plug a PH-2 trigger lead
  into the PH-2 battery lead and you put 3.7 V straight onto GPIO3 — dead pin, very
  possibly dead XIAO
- **This is also why you rework the kit's motor plug off PH2.0.** Leave it and the
  cell mates directly to the motor, bypassing the MOSFET entirely

### Three rules that come with connectors

- **Battery out before you mate or unmate anything.** Feeding data into an
  unpowered WS2812 pushes current through its input protection diodes, which is the
  classic way to kill pixel 0. Unplugging the cell first makes this a habit rather
  than a chore
- **The connector is never the anchor.** Tack the cable to the garment on *both*
  sides of every plug, so a snag pulls the tack, not the latch
- **Service loop either side of every plug.** Same reasoning as the wrist umbilical

### Dielectric grease — **buy 1 small tube**

- **Is:** non-conductive waterproof goo
- **Does:** a smear in each connector shell keeps soap residue from corroding the
  contacts over a season
- Cheap, and the alternative is intermittent faults you'll chase for hours
- **Suggested product:** [search dielectric grease](https://www.amazon.com/s?k=dielectric+grease+small+tube)

---

## Wire and materials

### Silicone-insulated hookup wire, 22–26 AWG — **one assortment covers both arms**

- **Is:** wire with soft rubbery insulation, not stiff plastic
- **Does:** bends thousands of times without the copper snapping
- **Use:**
  - 22 AWG (thicker) → power
  - 26 AWG (thinner) → data + trigger
- **Wrong wire →** works loose and breaks at elbow and wrist within hours of wear
  - solid-core is the worst offender
- **Suggested product:**
  [search silicone stranded wire kit 22-26 AWG](https://www.amazon.com/s?k=silicone+wire+kit+22+24+26+AWG+stranded)
  — a multi-colour spool set; colour-coding pays for itself at the connectors

### Heat-shrink tubing, assorted — **one assortment covers both arms**

- **Is:** plastic sleeve that shrinks tight when heated
- **Does:** seals and insulates each solder joint
- **Slide it on *before* you solder** — everyone forgets exactly once
- **Suggested product:** [search heat shrink tubing assortment](https://www.amazon.com/s?k=heat+shrink+tubing+assortment+kit)

### Hot glue or clear RTV silicone — **buy 1**

- **Does:** seals the cut ends of the strip against soap
- Used in [BUILD.md](BUILD.md) step 3. Easy to forget when ordering, annoying to lack
- **Suggested product:** [search clear RTV silicone](https://www.amazon.com/s?k=clear+RTV+silicone+sealant+small+tube)
  — or any hot glue gun you already own

### Protoboard, small — 1 per arm · **buy 2**

- **Is:** the perforated board the pod's components sit on
- Nothing exotic. A 4 × 6 cm piece per arm is plenty
- **Suggested product:** [search double-sided perfboard assortment](https://www.amazon.com/s?k=double+sided+perfboard+prototype+PCB+assorted)

### A light-coloured, thin, stretchy glove — 1 per arm · **buy a pair**

- **Does:** hides the strip, spreads light into a soft even glow instead of dots
- **Fabric matters a lot:**
  - thin / white / pale / stretchy → glows beautifully
  - thick / dark / leather → swallows the light almost entirely
- Test a scrap in a dark room before you buy
- **Suggested product:** none — this one you buy by hand, in person, holding a lit
  strip section under it. Fabric is the single most build-critical thing you cannot
  judge from a listing photo
- Full detail → glove section in [BUILD.md](BUILD.md)
- **If you're building the lace concept, read [DESIGN.md](DESIGN.md) first.** Lace is
  pale but it is *not* a diffuser — it's open mesh, and it overrides this guidance

### Sleeve or arm warmer — 1 per arm · **buy a pair**

- **Does:** same job as the glove, for the forearm segment
- Same fabric rules apply. Buy it at the same time as the glove and test both together

### Needle and thread, or fabric glue — **buy 1**

- For sewing the strip channels into the glove and sleeve
- A channel, not glue-down-flat — see [BUILD.md](BUILD.md) step 10

### Fabric marker pen — **buy 1**

- For marking the trigger position on your palm in step 1

---

## Tools

One of each — these are not per arm.

- **Soldering iron**
- **Flux-core solder, 0.8 mm** — see the note below, it's not a throwaway choice
- **Flux pen** — separate from the solder. The IP65 strip pads are the grubbiest
  joints in this build and they want extra flux
- Wire strippers, small side cutters
- **Multimeter** — not optional. Spec below
- Heat gun or lighter — for heat-shrink
- **Thermal camera** — optional, genuinely useful. See below
- 3D printer — trigger plate, battery sled, controller pod, bubbler mount
- **USB-C data cable** — a charge-only cable will waste you half an hour.
  [Search USB-C data sync cable](https://www.amazon.com/s?k=USB+C+data+sync+cable)

### Solder: leaded or lead-free?

Worth thirty seconds of thought, because the usual reasoning is slightly off.

- **The fumes that make you feel ill are the rosin flux, not the lead.** Lead does
  not vaporise at soldering temperatures. Ventilate regardless — a cheap fan
  pulling air away from your face is the fix, whichever solder you buy
- **The actual lead risk is ingestion** — lead on your hands, then your food. Wash
  your hands, don't eat at the bench, and that's the exposure closed
- **Lead-free (SAC305)** needs a hotter iron (~350 °C) and wets noticeably worse.
  That matters here, because the hardest joints in this build are the tiny copper
  pads on IP65 strip
- **Leaded 63/37** is much more forgiving on those pads

**Either is defensible.** Pick lead-free if you'd rather not have lead in the house;
just expect the strip joints to fight you a little and turn the iron up. Pick 63/37
if you want the strip work to go smoothly and you're happy washing your hands.

- **Buy flux-core either way.** Solid wire with no flux is miserable
- The **pen-style dispenser** is a nice thing to own, but buy a **spool for the
  build** and keep the pen in the field kit — it's for repairs, not for 40 joints
  in an afternoon
- **Suggested products:**
  [search 63/37 rosin-core 0.8 mm](https://www.amazon.com/s?k=63%2F37+rosin+core+solder+0.8mm) ·
  [search lead-free rosin-core 0.8 mm](https://www.amazon.com/s?k=lead+free+rosin+core+solder+0.8mm) ·
  [search rosin flux pen](https://www.amazon.com/s?k=rosin+flux+pen+no+clean)

### Multimeter spec

You'll use it for polarity checks before every first power-up, for continuity
tracing, and for measuring actual current draw. Minimum useful spec:

- **DC voltage** — the one you'll use most
- **AC voltage** — not needed for this build, but you own a multimeter for life
- **DC current to at least 2 A**, on a **fused** input
- **Continuity with an audible beeper** — and a *fast* one. This is what you'll
  actually live in while tracing a dead strip segment
- **Resistance**
- **Capacitance** — nice to have, useful for checking the 1000 µF is what it claims

Also worth having: auto-ranging, a backlight, and a hold button. You will be under
a table in bad light.

**Suggested products:**

- **Good enough, cheap:**
  [Neoteck auto-ranging DMM](https://www.amazon.com/Neoteck-Multimeter-Multimeters-Resistance-Transistor/dp/B01NAVAT9S)
  — hits every line of the spec above, dual-fused, CAT II 600 V
- **Also fine:**
  [Proster PSTTL334](https://www.amazon.com/Proster-PSTTL334-Multimeter-Temperature-Capacitance/dp/B0194VGLFS)
  — same class, adds temperature and comes with alligator clips
- **Buy once, cry once:**
  [Fluke 115](https://www.amazon.com/Fluke-115-Compact-True-RMS-Multimeter/dp/B000OCFFMW)
  — overkill for this build, correct for the next twenty years. Only worth it if you
  expect to keep doing electronics

For *this* build any of the three is sufficient — nothing here is a hard measurement.
The continuity beeper is what you'll actually live in.

### Thermal camera

- **Does:** shows you the hot component before it becomes a dead component
- Turns [BUILD.md](BUILD.md) step 6's "touch it and see if it's warm" from a
  fingertip guess into an actual measurement
- Best at finding: a shorted boost module, a MOSFET that turned out not to be
  logic-level, a strip section drawing more than it should
- A borrowed one used once during bench test is plenty. You don't need to own it
- **No link** — you already own one; it's on the README checklist to dig out

---

## The five parts people skip

Ordered by how much pain skipping them causes:

1. **74AHCT125** → random flicker, only in the field, impossible to reproduce
2. **1N5819 diode** → dead MOSFET, later, for no visible reason
3. **Common ground** (not a part — a rule) → bizarre unrepeatable behaviour
4. **330–470 Ω resistor** → first pixel only, wrong colour
5. **1000 µF capacitor** → voltage dips when pixels light, brain gets confused

## The one connector mistake that costs a board

**The trigger pigtail must not be PH2.0.** It shares a shell with the battery lead
that ships on every cell. See [Connectors](#connectors).

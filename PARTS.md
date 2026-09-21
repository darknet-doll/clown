# Parts List

- Everything below is **per arm**
- Building two arms → double every quantity
- Format for each part:
  - **Is** — what the object actually is
  - **Does** — its job in the circuit
  - **Skip it →** the exact way it breaks

Read order if you're new:

1. This file — what the parts are
2. [BUILD.md](BUILD.md) — how they go together
3. [README.md](README.md) — why the design is shaped this way

---

## The bubbles

### Bambu Lab Electric Bubble Maker Kit 01 (P6M) — ×1

- **Is:** small blower fan + bottle cap with one-way valve + battery
- **Does:** blows air across a soap film → bubbles
- **You modify:** nothing
  - You only take over *when* it switches on
- **Also in the box, and you use both:**
  - one 18650 cell
  - a USB charger
- Two kits → two blowers + two cells. One per arm

---

## The lights

### WS2812B LED strip, 60 LED/m, 5V, black PCB, IP65 — ~0.4 m

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

**Alternative:** SK6812 RGBW

- drop-in swap
- adds a real white LED per pixel → better "charging up" glow
- slightly more forgiving on data timing
- costs a bit more

---

## The brain

### Seeed XIAO ESP32-C3 — ×1

- **Is:** a whole computer, 21 × 17.5 mm
- **Does:** ~60×/second, decides
  - the colour of all 21 pixels
  - whether the motor runs
- **Watches:** the palm trigger
- **Why this board:**
  - tiny → hides on your upper arm
  - takes 5V in directly
  - Wi-Fi + Bluetooth built in (unused in v1, free for later)
- **Reprogram:** USB-C cable
  - **keep that port reachable** in the printed pod → see [BUILD.md](BUILD.md)

### 74AHCT125 level shifter chip — ×1

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

---

## The motor control

### N-channel logic-level MOSFET module (AO3400 or IRLZ44N) — ×1

- **Is:** an electrical switch, no moving parts
- **Problem it fixes:** brain can decide, but can't push enough current to spin a motor
  - like asking someone to lift a car
- **Does:** brain flicks this switch → switch lets big current through from battery
- **Buy as a module, not a bare chip:**
  - no soldering
  - resistors already included
- **"Logic-level" matters:**
  - opens *fully* from the brain's low voltage
  - non-logic-level → only half-opens, gets hot

### 1N5819 flyback diode — ×1

- **Is:** a one-way valve for electricity
- **Problem it fixes:** a motor is a big coil
  - cut power to a coil → it kicks back a high-voltage spike into your circuit
- **Does:** gives that spike a safe loop to run around until it dies out
- **Skip it →** MOSFET eventually dies, maybe takes the brain with it
- Costs ~20¢. Fit it

---

## Power

### Protected 18650 battery — ×1 in use, plus spares

- **Is:** rechargeable cell, same kind as in a laptop pack or a vape
- One comes free with each bubble kit
- **"Protected" =** tiny guardian circuit in the end of the cell
  - cuts off if drained too far or charged too hard
  - over-drained lithium can be damaged or genuinely unsafe
- Cells in the bubble kit are protected ones
- **Do not substitute unprotected cells** to save money
  - this is strapped to your arm

### 18650 battery sled / holder with wire leads — ×1

- **Is:** the slot the cell sits in
- **Does:** lets you swap a flat cell for a fresh one, no soldering iron
- Print an enclosure with a lid that clicks shut
  - you don't want it ejecting mid-performance

### 5V boost converter module — ×1

- **Is:** a pump, but for voltage
- **Problem it fixes:** cell makes ~3.7V, brain + LEDs need 5V
- **Does:** pumps 3.7V up to a steady 5V
- **Only feeds lights + brain (~0.3 A)**
  - motor runs straight off the battery instead
  - so a small cheap module is genuinely fine here

### 2A resettable fuse (polyfuse / PPTC) — ×1

- **Is:** a safety valve that resets itself
- **Does:** on a current spike, suddenly becomes very resistant → chokes the flow
  - before anything catches fire
- Let it cool → back to normal by itself
- Cheap insurance for a lithium cell worn against your body

### Two 100 kΩ resistors (battery monitor) — ×2

- **Is:** two resistors forming a "divider"
- **Problem it fixes:**
  - brain can only safely measure up to ~3.3V
  - full cell is 4.2V
- **Does:** shrinks battery voltage neatly in half → safe to read
- **Gets you:** costume pulses red when the battery is nearly flat
  - instead of dying with no warning

---

## Signal conditioning

### 1000 µF electrolytic capacitor — ×1

- **Is:** a tiny water tank for electricity
- **Problem it fixes:** many LEDs switching on at once all gulp power at the same instant
- **Does:** holds a reserve, smooths the gulp → voltage doesn't dip and confuse the brain
- **Watch out:** polarised
  - one leg marked negative → must go to ground
  - backwards, electrolytics pop

### 330–470 Ω resistor — ×1

- **Is:** a speed bump on the data wire
- **Does:** softens the signal's sharp edge
  - so it doesn't bounce back down the wire and garble the message to the first LED
- **Skip it →** the *first* pixel misbehaves — wrong colour or flickering
  - every pixel behind it stays fine

---

## The trigger

### Snap-action microswitch, lever type — ×1

- **Is:** clicky button with a small metal arm sticking off it
- **The arm is the point:**
  - wide press area
  - squeeze fingers into your palm mid-performance and hit it every time
  - **no looking, no aiming**
  - a plain round button = hunting for a 12 mm target by feel
- **Bonus:** crisp physical click → you feel that it fired

---

## Wire and materials

### Silicone-insulated hookup wire, 22–26 AWG

- **Is:** wire with soft rubbery insulation, not stiff plastic
- **Does:** bends thousands of times without the copper snapping
- **Use:**
  - 22 AWG (thicker) → power
  - 26 AWG (thinner) → data + trigger
- **Wrong wire →** works loose and breaks at elbow and wrist within hours of wear
  - solid-core is the worst offender

### Heat-shrink tubing, assorted

- **Is:** plastic sleeve that shrinks tight when heated
- **Does:** seals and insulates each solder joint
- **Slide it on *before* you solder** — everyone forgets exactly once

### A light-coloured, thin, stretchy glove — ×1

- **Does:** hides the strip, spreads light into a soft even glow instead of dots
- **Fabric matters a lot:**
  - thin / white / pale / stretchy → glows beautifully
  - thick / dark / leather → swallows the light almost entirely
- Test a scrap in a dark room before you buy
- Full detail → glove section in [BUILD.md](BUILD.md)

---

## Tools you'll need

- Soldering iron, solder, flux
- Wire strippers, small side cutters
- **Multimeter** — for checking polarity before connecting the battery
  - not optional
- Heat gun or lighter — for heat-shrink
- 3D printer — trigger plate, battery sled, controller pod
- Needle and thread, or fabric glue — glove channel

---

## Rough quantities summary

| Part | Per arm | Buy for two arms |
|---|---|---|
| Bubble Maker Kit 01 | 1 | 2 |
| WS2812B strip 60/m IP65 | 0.4 m | 1 m roll |
| XIAO ESP32-C3 | 1 | 2 |
| 74AHCT125 | 1 | 2 (buy 5, they're cheap) |
| MOSFET module | 1 | 2 |
| 1N5819 diode | 1 | 2 (buy 10) |
| Protected 18650 | 1 | 2 in use + 2 spares |
| 18650 sled | 1 | 2 |
| 5V boost module | 1 | 2 |
| 2A polyfuse | 1 | 2 (buy 5) |
| 100 kΩ resistor | 2 | 4 |
| 1000 µF capacitor | 1 | 2 |
| 330–470 Ω resistor | 1 | 2 |
| Lever microswitch | 1 | 2 + 2 spares |
| Silicone wire | — | one small assortment covers both |
| Thin light glove | 1 | a pair |

---

## The five parts people skip

Ordered by how much pain skipping them causes:

1. **74AHCT125** → random flicker, only in the field, impossible to reproduce
2. **1N5819 diode** → dead MOSFET, later, for no visible reason
3. **Common ground** (not a part — a rule) → bizarre unrepeatable behaviour
4. **330–470 Ω resistor** → first pixel only, wrong colour
5. **1000 µF capacitor** → voltage dips when pixels light, brain gets confused

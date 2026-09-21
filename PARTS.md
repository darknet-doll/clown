# Parts List

Everything below is **per arm**. You're building two, so double every quantity.

Plain-English explanation of what each thing actually does, and why it's in the
list, is under each part. If a part has a "skip this and it breaks like *this*"
note, that's the part people leave out and then spend a weekend debugging.

---

## The bubbles

### Bambu Lab Electric Bubble Maker Kit 01 (P6M) — ×1

The bubble machine itself: a small blower motor, a bottle cap with a one-way
valve, and a rechargeable battery.

**ELI5:** It's a tiny fan that blows air across a film of soap to make bubbles.
You're not modifying it — you're just taking over the job of deciding *when* it
turns on, instead of it being a simple on/off switch.

The kit also includes an 18650 battery and a USB charger. **You will use those.**
Buying two kits gets you two blowers *and* two batteries, one per arm.

---

## The lights

### WS2812B LED strip, 60 LED/m, 5V, black circuit board, IP65 — ~0.4 m

**ELI5:** A ribbon of tiny lights where every single light has its own miniature
chip inside it. That's the important part. It means you can tell light #7 to be
bright white and light #8 to be dark, all through **one** data wire. That's what
makes a comet possible — a normal LED strip can only be one color all at once,
so the light couldn't "travel" anywhere.

"Addressable" and "programmable" mean exactly this: each pixel takes orders
individually.

Why these specific numbers:

- **60 LED/m** — about 1.7 cm between lights. Dense enough that under a glove
  they blur into one smooth streak instead of visible dots.
- **5V** — runs off the same low voltage as everything else. (Avoid 12V strips
  like the WS2815 here; they'd need a whole second power system.)
- **Black circuit board** — disappears against dark fabric when it's off.
- **IP65** (clear silicone sleeve over the top) — you are spraying soapy water
  down your own arm. This is the waterproofing.

**Alternative:** SK6812 RGBW strip is a drop-in swap. It adds a dedicated white
LED to each pixel, which looks better for a "charging up" glow, and it's slightly
more forgiving about data timing. Costs a bit more.

---

## The brain

### Seeed XIAO ESP32-C3 — ×1

**ELI5:** A complete computer the size of a postage stamp. It watches your palm
trigger, and about 60 times a second it decides what color every single LED
should be and whether the motor should be running. Everything clever in this
costume happens here.

It's this board specifically because it's tiny (21 × 17.5 mm, so it hides on your
upper arm), it takes 5V in directly, and it has Wi-Fi and Bluetooth built in if
you ever want to control the costume from your phone.

You reprogram it by plugging a USB-C cable into it. **Keep that port reachable**
when you build the enclosure — see [BUILD.md](BUILD.md).

### 74AHCT125 level shifter chip — ×1

**ELI5:** A translator that also shouts. The brain speaks at 3.3 volts. The LED
strip is listening for 5 volts. Usually the strip *sort of* hears the brain
anyway, which is exactly the problem — it works on your bench and then flickers
randomly at the party.

This chip listens to the brain's quiet 3.3V signal and repeats it at a confident
5V, so the strip hears it perfectly every time.

**Skip this and:** your lights flicker, glitch, or show wrong colors
intermittently — especially as wire runs get longer. This is the single most
common cause of "my LED strip is haunted."

---

## The motor control

### N-channel logic-level MOSFET module (AO3400 or IRLZ44N) — ×1

**ELI5:** An electrically-operated switch with no moving parts. The brain can
think, but it can't push enough electricity to actually spin a motor — it'd be
like asking someone to lift a car. So instead the brain flicks this switch, and
the switch lets the big current through from the battery.

Buying it as a little pre-made module (rather than a bare chip) saves you
soldering and usually includes the resistors it needs.

"Logic-level" matters: it means the switch fully opens from the brain's low
voltage. A non-logic-level MOSFET would only half-open and get hot.

### 1N5819 flyback diode — ×1

**ELI5:** A motor is really just a big coil of wire. When you suddenly cut power
to a coil, it *kicks back* — it dumps a nasty high-voltage spike backwards into
your circuit. This part is a one-way valve that gives that spike a safe little
loop to run around in until it burns itself out.

**Skip this and:** your MOSFET eventually dies, and possibly takes the brain with
it. It costs about 20 cents. Fit it.

---

## Power

### Protected 18650 battery — ×1 in use, plus spares

**ELI5:** A rechargeable battery, the same kind inside a laptop battery pack or a
vape. One comes free with each bubble kit.

"**Protected**" means it has a tiny guardian circuit built into the end of it
that cuts the battery off if you drain it too far or charge it too hard. Lithium
batteries that get over-drained can be damaged or become genuinely unsafe. The
cells included with the bubble kit are protected ones.

**Do not substitute unprotected cells** because they were cheaper. This is
strapped to your arm.

### 18650 battery sled / holder with wire leads — ×1

**ELI5:** The slot the battery sits in, so you can pop a flat one out and a fresh
one in without a soldering iron. Print an enclosure with a lid that clicks shut —
you don't want it ejecting mid-performance.

### 5V boost converter module — ×1

**ELI5:** A pump, but for voltage. The battery only produces about 3.7 volts, and
the LEDs and brain need 5. This little board pumps it up to a steady 5V.

In this build it only has to supply the lights and the brain (roughly 0.3 A)
because the motor is fed straight from the battery. That's a gentle job, so a
small inexpensive module is genuinely fine here.

### 2A resettable fuse (polyfuse / PPTC) — ×1

**ELI5:** A safety valve that resets itself. If something shorts out and the
current spikes, this part suddenly becomes very resistant and chokes the flow off
before anything catches fire. Let it cool down and it goes back to normal by
itself.

Cheap insurance for a lithium battery worn against your body.

### Two 100 kΩ resistors (battery monitor) — ×2

**ELI5:** The brain can only safely measure voltages up to about 3.3V, and a full
battery is 4.2V. These two resistors form a "divider" that shrinks the battery
voltage neatly in half, so the brain can read it without being hurt.

This is what lets the costume pulse red at you when the battery is nearly flat,
instead of just dying without warning.

---

## Signal conditioning

### 1000 µF electrolytic capacitor — ×1

**ELI5:** A tiny water tank for electricity. When a bunch of LEDs switch on at
the same instant, they all gulp power at once. The tank holds a reserve and
smooths out that gulp, so the voltage doesn't dip and confuse the brain.

Note it's polarized — one leg is marked negative and must go to ground. Backwards
electrolytic capacitors pop.

### 330–470 Ω resistor — ×1

**ELI5:** A speed bump on the data wire. It softens the sharp edge of the signal
so it doesn't bounce back down the wire and garble the message to the first LED.

**Skip this and:** the first pixel in the strip behaves strangely — wrong color,
or flickering while the rest are fine.

---

## The trigger

### Snap-action microswitch, lever type — ×1

**ELI5:** A clicky button with a little metal arm sticking off it. The arm is the
point: it gives you a wide area to press, so you can squeeze your fingers into
your palm in the middle of a performance and hit it every time **without looking
or aiming**. A plain round button means hunting for a 12 mm target by feel.

It also gives a crisp physical click, so you can feel that it fired.

---

## Wire and materials

### Silicone-insulated hookup wire, 22–26 AWG

**ELI5:** Wire with soft rubbery insulation instead of stiff plastic. It bends
thousands of times without the copper inside snapping. Normal hookup wire (and
especially solid-core wire) will work loose and break at the elbow and wrist
within a few hours of wearing it.

22 AWG (thicker) for power, 26 AWG (thinner) for the data and trigger signals.

### Heat-shrink tubing, assorted

**ELI5:** Plastic sleeve that shrinks tight when you heat it, sealing and
insulating your solder joints. Slide it on *before* you solder — everyone forgets
once.

### A light-colored, thin, stretchy glove — ×1

**ELI5:** The strip hides underneath this, and the fabric spreads the light out
into a soft even glow instead of visible dots.

Material matters a lot here. Thin white or pale stretchy fabric glows beautifully.
Thick black leather will swallow the light almost entirely. See the glove section
in [BUILD.md](BUILD.md) before you buy — test a scrap first if you can.

---

## Tools you'll need

- Soldering iron, solder, flux
- Wire strippers, small side cutters
- Multimeter (for checking polarity before you connect the battery — not optional)
- Heat gun or lighter for the heat-shrink
- 3D printer for the trigger plate, battery sled, and controller pod
- Needle and thread, or fabric glue, for the glove channel

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

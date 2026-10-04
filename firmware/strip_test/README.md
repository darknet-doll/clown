# strip_test

Bench test: squeeze the trigger → a comet runs down the LED strip, through the
74AHCT125.

- No motor, battery or boost — USB powers everything
- Same pins and the same shifter gate as `clown_arm.ino` → the wiring carries over
- Run [`trigger_test`](../trigger_test/README.md) first; this assumes the trigger works

## About the 0.1 µF cap

- **Fine to run without it on the bench.** Short wires, 10 pixels, no motor
- **But a glitch here proves nothing.** If the strip flickers, fit the cap before
  you go hunting
- **Stand-in until the ceramics land:** a small electrolytic (1–10 µF) from the kit
  across pins 14 and 7, stripe side to pin 7. Swap it for the 0.1 µF when it arrives

## You need

- The XIAO, data USB-C cable and kit microswitch from `trigger_test`
- 1× 74AHCT125 (DIP-14)
- 10 pixels cut from the WS2812B strip (cut on the copper pads)
- 1× 330–470 Ω resistor
- Jumper wires / breadboard

## The chip

Notch (or dot) at the top = pin 1 is top-left. Straddle the breadboard's centre gap.

```
            ┌───U───┐
  1OE   1 ──┤       ├── 14  Vcc
  1A    2 ──┤       ├── 13  4OE
  1Y    3 ──┤       ├── 12  4A
  2OE   4 ──┤       ├── 11  4Y
  2A    5 ──┤       ├── 10  3OE
  2Y    6 ──┤       ├──  9  3A
  GND   7 ──┤       ├──  8  3Y
            └───────┘
```

## Wiring

Rails: red **+** = XIAO **5V**, blue **−** = XIAO **GND**.

| From | To | Notes |
|---|---|---|
| XIAO **5V** | red + rail | **new** — the chip and strip need 5 V |
| XIAO **GND** | blue − rail | |
| Switch NO / COM | D1 / blue − rail | unchanged from `trigger_test` |
| Chip pin **14** (Vcc) | red + rail | |
| Chip pin **7** (GND) | blue − rail | |
| XIAO **D10** | chip pin **2** (1A) | |
| Chip pin **3** (1Y) | 330–470 Ω → strip **DIN** | arrow on the strip points *away* from DIN |
| Chip pin **1** (1OE) | blue − rail | turns gate 1 on |
| Chip pins **4, 5** (2OE, 2A) | blue − rail | gate 2 is the motor drive later; parked for now |
| Chip pins **9, 12** (3A, 4A) | blue − rail | unused inputs — must not float |
| Chip pins **10, 13** (3OE, 4OE) | red + rail | unused outputs off |
| Chip pins **6, 8, 11** (2Y, 3Y, 4Y) | **nothing** | outputs — never tie to a rail |
| Strip **5V** / **GND** | red + / blue − rail | |

- **Take the plain LED off D10** before you plug in
- **Battery unplugged.** USB only

## Load it

Same as `trigger_test`, plus FastLED:

1. **Library Manager** → search `FastLED` → install
2. **File → Open** → `firmware/strip_test/strip_test.ino`
3. Board **XIAO_ESP32C3**, **USB CDC On Boot: Enabled**, pick the port, **Upload**

## What you should see

- **Power-up:** whole strip red → green → blue, then a dim purple glow
- **Squeeze and hold:** comets run from the first pixel to the last, over and over
- **Release:** back to dim purple
- **Serial Monitor** (115200): `trigger: PRESSED` / `trigger: released`

## If it doesn't

| Symptom | Likely cause |
|---|---|
| Strip dark, Serial works | chip not powered (pins 14/7), pin 1 not grounded, or strip wired at DOUT end |
| Chip warm | an unused input floating, or a Y output tied to a rail — recheck the table |
| Flicker / random colours | fit the cap (or stand-in) first; then shorten the 1Y → DIN wire, check grounds |
| Boot flash is green → red → blue | change `GRB` to `RGB` |
| First pixel wrong, rest fine | resistor missing or wrong value |
| XIAO resets when the comet runs | too many pixels on USB — cut the offcut shorter |

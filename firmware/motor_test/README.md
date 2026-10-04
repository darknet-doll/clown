# motor_test

Bench test: squeeze the trigger → the blower runs and a comet runs down the strip.

- Builds on [`strip_test`](../strip_test/README.md) — start from that breadboard
- XIAO, chip and strip stay on USB. **The motor runs off the kit's 18650**, never USB
- Same pins, shifter gate and motor timing as `clown_arm.ino`

## Before the 0.1 µF ceramic arrives

- Keep the stand-in electrolytic across the rails by the chip
- **A glitch here proves nothing** — strip flicker or a XIAO reset when the motor
  kicks are exactly what a missing decoupling cap looks like. Refit and retest
- **Not optional, even on the bench:** the flyback diode `CR1` and the 10 kΩ gate
  pulldown `R5`. Those protect hardware; the cap only protects signal quality

## You add

- RFP30N06LE MOSFET
- 100 Ω (`R4`), 10 kΩ ×2 (`R5` + a pin-5 pulldown)
- 1N5819 diode (`CR1`)
- GBX-185 polyfuse (`F1`)
- The kit's motor and charged 18650

## Steps (from the strip_test board)

**USB unplugged, cell not connected.**

### Gate 2 (chip pin 5 → motor)
1. **Remove** the jumper from chip pin 5 to the blue rail. Pin 4 stays on blue
2. **Jumper** XIAO **D2**'s row (left side, 3rd pin from USB) → chip pin 5's row
3. **10 kΩ** from chip pin 5's row → blue rail. Holds the motor off while the XIAO boots

### MOSFET
4. **Seat the MOSFET** in empty rows, each leg in its own row. Printed face toward
   you, legs down: **G, D, S** left to right
5. **100 Ω** from chip pin 6's row (2Y) → **G** row
6. **10 kΩ** from **G** row → **S** row
7. **Jumper** **S** row → blue rail

### Motor, diode, fuse
Battery + gets its **own rows** — never the red rail.

8. Pick two empty rows away from everything: **CELL** and **BAT+**
9. **Polyfuse** GBX-185: one leg in **CELL**, one in **BAT+**
10. **Motor +** → **BAT+**. **Motor −** → **D** row
11. **1N5819**: banded end in **BAT+**, other end in **D** row

### Check with the meter (still no power)
- **BAT+ row ↔ red rail:** continuity → must **not** beep
- **G ↔ S:** ohms → ~10 kΩ
- **Diode band** in BAT+, not in D

### Power, in this order
12. **USB in.** Strip boots red → green → blue
13. **Cell − → blue rail.** Then **cell + → CELL row**. Meter the cell leads first if
    the colours aren't obvious
14. **Aim the bubble head away** from the board and laptop — it can run dry

**Disconnecting:** cell + first, then USB.

## What you should see

- **Squeeze:** blower spins up, comets run
- **Release:** blower stops, strip back to dim purple
- **Serial Monitor:** `trigger: PRESSED, motor on` / `trigger: released, motor off`

## If it doesn't

| Symptom | Likely cause |
|---|---|
| Blower never runs, Serial fine | D2 jumper not on pin 5; MOSFET legs swapped; cell not reaching BAT+; fuse not seated |
| Blower runs all the time | MOSFET G/D/S wrong; pin 5 still tied to blue *and* D2 |
| Blower twitches at power-up | missing 10 kΩ on G→S or on pin 5 |
| XIAO resets when the motor starts | stand-in cap / no ceramic yet, or a flat cell. Don't chase until the 0.1 µF is in |
| MOSFET hot | gate not getting 5 V — check chip pin 14 has 5 V and the 100 Ω goes to G |
| Polyfuse trips (motor stops, fuse warm) | motor stalled, or a short from BAT+ to ground |

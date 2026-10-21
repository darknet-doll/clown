# Build progress

Where each arm stands, newest first. Steps refer to [BUILD.md](BUILD.md) and the
[Pod PCB Build](https://claude.ai/artifact/EFubpZgKECGwYLr3vCSfxH) walkthrough.

## Arm 1 — updated 2026-10-18

### Done

- **Pod PCB: all 40 walkthrough steps finished**
  - Resistors, C2, C3, CR2, F1, Q1, J1, SW1, U1, U2, C1, XIAO, J2, J3 fitted
  - First power, chip, rail and XIAO power checks done
- **Readings at the end**
  - U2 supply (pin 14 → 7): **5.10 V** — a touch over 5.05, safe; retrim pending
  - XIAO 5V pin: **4.85 V**, the expected drop across CR2
- **J1 cell lead** = the PH2.0 plug cut off the kit's motor lead
- **SW1** = DaierTek KCD1 rocker on two red leads
- **U1 (MT3608) on this module: clockwise lowers the voltage**, counter-clockwise raises it
- **J2** (strip, SM-3): socket half on the board
  - red = J2-1 +5V · white = J2-2 GND · green = J2-3 DATA
- **J3** (motor + trigger, SM-4): socket half on the board
  - blue = J3-1 M+ · red = J3-2 M− · green = J3-3 TRIG · black = J3-4 GND
- **XIAO is flashed with `firmware/motor_test`** — same pins as the board, so it
  runs the bench test as-is
  - **2026-10-21:** found running a sketch that isn't in the repo (serial printed
    `up … frames … reset_reason`), strip dark. Reflashed `motor_test`, upload verified
  - Board MAC `ac:27:6e:7c:d7:2c` (ESP32-C3 rev v0.4) — check it with esptool before
    flashing, to be sure which XIAO is on the cable
- **Kit blower separated from its switch** for the bench test
  - motor red → blue, motor black → red
  - microswitch's two wires → green and black

### In progress

- **Bench test with `motor_test`** — fit CR1, tape joins, then power up
  - CR1 (1N5819) across the two motor joins, **band on the motor-red / blue join**

### Next

- Bench test passes → flash `firmware/clown_arm` with the real pixel counts (BUILD step 8)
- Full BUILD step 6 bench test with the strip lit
  - retrim U1 to **5.00 V under load**, then lock the trimpot with nail polish
- Long runs (BUILD step 3): splice reel wire between the pigtails
  - motor pair 22 AWG twisted, trigger pair 26 AWG
  - still to make: wrist SM-4, trigger JST-ZH 2-pin, blower JST-SM 2-pin
- Arm 2

### Open questions — check before going on

- **C2 / C3:** confirm both are printed **"104"**. A loose cap marked "33" turned up
  (33 pF); if either fitted cap isn't 104, swap it
- **Cell splice:** the cell's own pigtail was cut by mistake and spliced back.
  Meter the plug (+ on the expected pin) before it goes on the kit charger
- **J1 joints:** had stray strands; confirm they were reflowed and J1 + to − reads OL with the cell out

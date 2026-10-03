# trigger_test

Bench test: squeeze the bubble kit's trigger → an LED lights.

- No motor, battery, boost, strip or level shifter needed
- Trigger is on the same pin as `clown_arm.ino` → that wiring carries over unchanged
- The XIAO ESP32-C3 has **no user LED** of its own (only the charge LED), so this
  uses one plain external LED

## You need

- 1× XIAO ESP32-C3 (the pre-soldered one is easiest)
- 1× USB-C cable that **carries data** (charge-only cables are the #1 upload failure)
- 1× kit lever microswitch
- 1× plain LED (any colour, two legs)
- 1× 330–470 Ω resistor — **not optional**, without it the LED and the pin get hurt
- Jumper wires / breadboard

## Wiring

| From | To | Notes |
|---|---|---|
| Switch **COM** | XIAO **GND** | ignore the NC terminal |
| Switch **NO** | XIAO **D1** | internal pull-up, no resistor needed |
| XIAO **D10** | 330–470 Ω → LED **long leg** (+) | resistor can go on either leg |
| LED **short leg** (−, flat side of the rim) | XIAO **GND** | |

- **Battery unplugged.** Bench test is USB only
- **Don't plug the kit's trigger lead into anything with a battery on it.** If it
  came on a PH2.0 plug, it mates with the battery lead too — clip straight onto the
  switch terminals or bare wires instead

## Load it

1. Install **Arduino IDE 2**
2. **Boards Manager** → search `esp32` → install **esp32 by Espressif Systems**
3. **File → Open** → `firmware/trigger_test/trigger_test.ino`
4. **Tools → Board** → `esp32` → **XIAO_ESP32C3**
5. **Tools → USB CDC On Boot** → **Enabled** (otherwise Serial Monitor is blank)
6. Plug in the XIAO → **Tools → Port** → pick the new `/dev/cu.usbmodem…` entry
7. Click **Upload** (→ arrow)

Upload fails / no port shows up:

- Unplug → **hold BOOT** (the button marked B) → plug in → release → upload again
- After a BOOT-mode upload, press **RESET** (R) once to start the sketch
- Still no port → swap the USB-C cable

## What you should see

- **Power-up:** LED blinks 3 times, then goes off
- **Squeeze:** LED on
- **Release:** LED off
- **Serial Monitor** (115200 baud): prints `trigger: PRESSED` / `trigger: released`

## If it doesn't

| Symptom | Likely cause |
|---|---|
| No boot blinks | LED in backwards (flip it), or not on D10 / GND |
| Boot blinks, nothing on squeeze, no Serial lines | switch on NC instead of NO, or COM not reaching GND |
| Serial says PRESSED/released, LED stays dark | LED came loose after boot — reseat it |
| LED always on, Serial shows PRESSED at rest | switch wired COM↔NC — move to NO |

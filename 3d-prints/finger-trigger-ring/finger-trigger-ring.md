# Finger trigger ring

Ring at the base of the middle finger that carries the lever microswitch (the bubble
trigger). The switch sits on the palm side with its lever toward the palm. Curling the
finger at the knuckle folds the palm onto the lever.

## Switch

Amazon listing drawing (`m.media-amazon.com/images/I/71BXJrdZ7tL._SL1500_.jpg`):

- Body 20 × 15.6 × 6.4. Lever on one 20 mm edge, 14.1 long, tip 8 above the body
- Mounting holes Ø2.3, 9.5 apart
- Hole height isn't on the drawing. Measured off the image (25.6 px/mm): centres
  **7.2 below the lever edge**, 8.4 above the bottom edge, about 5.1 in from each end

## v3 (test fit) — current

Same as v2 except:

- **Split edges:** the four long edges of the gap are rounded R0.6, so they don't pinch.
  The same rounding takes the saddle's lower corners where they meet the finger's sides
- **Finger-side edges:** flared R1.0 at both ends of the ring
  - all round at the knuckle end
  - on the back half at the end of the band
  - under the saddle at its far end
- **Screw holes:** Ø1.7, right through into the bore. Nothing to bridge when printing
  - The plate is 4.6 thick at the holes. An M2×10 tip stops about 1.0 short of the
    bore. **Nothing longer than M2×10**, or it reaches the finger
- **Files:** `versions/finger-trigger-ring-v3-c65.stl` (`export_v3.py`)

## v2 (test fit) — archived, not printed

Same as v1 except:

- **No lip** behind the switch. The final switch may be a different one, so only the
  two pilots are sized to it
- **Split:** 1.0 gap through the band on the back of the finger. The band can open or
  squeeze to suit other hands
- **One size: 65** mm circumference. The production hands aren't available to measure yet
- **Pilot depth:** 3.8. Still M2×10
- **Files:** `versions/archive/finger-trigger-ring-v2-c65.stl` (`export_v2.py`)

## v1 (test fit) — archived, not printed

- **Bore:** finger circumference / π + 0.2. Two sizes: **50** and **65** mm circumference
- **Band:** 2.0 wall, 7 long, at the knuckle end
- **Saddle:** flat plate 21 × 15.9 on the palm side, 3.5 thick at the centre line, sides
  cut off at the finger's sides so it doesn't push into the neighbouring fingers
- **Lip:** 1.5 × 3 tall behind the switch's bottom edge. It takes the lever push off the screws
- **Screws:** M2 self-tapping into blind Ø1.7 pilots, 0.8 floor above the bore
  - Pilot depth 4.2 (c50) / 3.8 (c65)
  - **Use M2×10** (about 3.6 of thread). M2×8 bites only about 1.6
- **Print:** knuckle end on the bed, no supports
- **Files:** `versions/archive/finger-trigger-ring-v1-c50.stl`, `versions/archive/finger-trigger-ring-v1-c65.stl`
  (`export_v1.py`)

## Print log

| Date | Version | Result |
|---|---|---|

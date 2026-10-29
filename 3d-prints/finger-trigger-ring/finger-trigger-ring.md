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

## v4 (sizing set) — current

v3 geometry in nine sizes, each in two plate lengths. Print the ones that bracket the
hand, then pick a size and a plate.

- **Sizes:** 45, 47.5, 50, 52.5, 55, 57.5, 60, 62.5, 65 mm finger circumference
- **full:** plate as v3. It runs 8.7 past the screw-hole centres, to 15.9 from the knuckle end
- **short:** plate runs half that past the holes, 4.35, to 11.55. The switch overhangs its
  end by about 4. There is 3.5 of plate between each hole and the end
- **Screws:** M2×10 at every size. The tip stops 1.0 (c65) to 1.7 (c45) short of the bore
- **Files:** `versions/finger-trigger-ring-v4-c<size>-full.stl` and `-short.stl` (`export_v4.py`)

| Size | Bore Ø | Plate at holes | M2×10 tip to bore |
|---|---|---|---|
| 45 | 14.52 | 5.27 | 1.67 |
| 47.5 | 15.32 | 5.15 | 1.55 |
| 50 | 16.12 | 5.05 | 1.45 |
| 52.5 | 16.91 | 4.96 | 1.36 |
| 55 | 17.71 | 4.88 | 1.28 |
| 57.5 | 18.50 | 4.81 | 1.21 |
| 60 | 19.30 | 4.75 | 1.15 |
| 62.5 | 20.09 | 4.69 | 1.09 |
| 65 | 20.89 | 4.64 | 1.04 |

## v3 (test fit) — archived

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
- **Files:** `versions/archive/finger-trigger-ring-v3-c65.stl` (`export_v3.py`)

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

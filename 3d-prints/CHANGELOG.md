# 3D print changelog

Every change to a printed part, newest first per part. One line of what changed and
one line of why. Each part's full spec, settings and per-print log are in its own
`<part>.md`.

- **Current files:** `<part>/versions/`
- **Replaced files and finished test pieces:** `<part>/versions/archive/`. Never edited
  or overwritten; each `export_vN.py` still regenerates its own files there
- **Units:** mm

---

## Pod housing

Sealed PETG box with TPU seals for the controller pod: board, cell, MT3608, rocker and
the leads to both arm plugs.
Spec and log: [pod-housing/pod-housing.md](pod-housing/pod-housing.md)

| Version | Date | Status | Files |
|---|---|---|---|
| v5 | 2026-10-30 | Not yet printed. Current. Print the seal tray (with the lid, gasket and seals) and the wall coupon first | `versions/pod-housing-v5-{bottom,lid,deck,gasket,seals,wall-coupon,seal-tray}.stl` |
| v4 | 2026-10-29 | Archived. Wall and snap coupons printed 2026-10-30 | `versions/archive/pod-housing-v4-*.stl` |
| v3 | 2026-10-29 | Archived, never printed | `versions/archive/pod-housing-v3-*.stl` |
| v2 | 2026-10-29 | Archived, never printed | `versions/archive/pod-housing-v2-*.stl` |
| v1 | 2026-10-29 | Archived, never printed | `versions/archive/pod-housing-v1-*.stl` |

### v5 — 2026-10-30

- **Change:**
  - **Material:** the bottom and lid are PETG. TPU is used only for the seals and the
    module deck
  - **Lid:** screwed down with 4 × M3×8 button heads into heat-set inserts. The inserts
    sit in bosses that hang from the long walls on 45° corbels. The heads sit flush in
    counterbores over TPU washers
  - **Lid seal:** a TPU lip gasket in a groove in the wall top, squashed 0.6 by a
    pocket in the lid. Ribs under the lid run between the bosses. The lid seats PETG
    to PETG on hard stops
  - **J2, J3:** leave on their leads through split TPU grommets in the front wall. J2
    is 10 × 15 with a 2.5 bore, J3 8 × 20 with a 3.0 bore. The JST panel cutouts are
    gone
  - **Rocker:** a Ø20.6 hole, thinned to 1.2 behind the clips, with a TPU washer
    under the bezel (0.6 or 1.0)
  - **Deck:** moves about 9 forward to clear a screw boss
  - **Coupons:** a seal tray, the real wall top on a 15 deep tray, replaces the snap
    coupon. The wall coupon is PETG
  - 82.8 × 57.6 × 41.6
- **Why:** darknetdoll, after the v4 coupons:
  - An all-TPU box makes the circuit boards structural
  - The rocker stretched the 19.8 TPU hole and stayed that way, so rigid PETG needs a
    bigger hole
  - The pod's J2 is the male SM-3 half. Its latch release is at the wire end, so it
    can't panel-mount, and JST makes no panel version. Grommets at darknetdoll's
    sizes let both plugs pass through without re-soldering
  - A lip, not a squeezed cord, because 95A is too stiff for four screws to squeeze
    evenly
- **Files:** `versions/pod-housing-v5-*.stl` (`export_v5.py`)

### v4 — 2026-10-29

- **Change:** v3 resized to the parts as measured with calipers:
  - **MT3608:** pocket 37.4 long for the 36.8 module, and lips set for its 0.95 board.
    The rails have 6 gaps where the trimpot screw stands 1.1 past the edge, on both
    rails at both ends
  - **Rocker:** the wall is thinned out to 26 at the sides for the 23 snap clips
  - **XIAO:** its socket stands 1.6 proud, so the back wall moves back 0.1
  - 82.8 × 57.6 × 42.4
- **Why:** v3 used listing sizes and guesses. The real module is longer and much
  lower (7.9), its trimpot screw sticks out past the edge, and the rocker's clips are
  wider than allowed for
- **Files:** `versions/archive/pod-housing-v4-*.stl` (`export_v4.py`)

### v3 — 2026-10-29

- **Change:**
  - The rocker points out of the back end, behind the XIAO, with its body lying over
    the XIAO
  - J2 and J3 sit side by side in a 1.8 front wall
  - The straps go over the top, in two channels across the lid. The base loops are gone
  - No USB-C opening and no plug
  - The MT3608 deck now lies on the cell, held down by the lid
  - Bottom and lid edges get a 1.2 chamfer
  - 82.7 × 57.6 × 42.3
- **Why:** darknetdoll: v2 misread the brief. The straps go over the top. The rocker
  points out of the back, so its wires have room, and it can sit over the board. The
  plugs belong together on one side. The case is there to protect the board, so USB-C
  needs no opening. Clearing the XIAO sets the height; putting the module on the cell
  keeps the length short
- **Files:** `versions/archive/pod-housing-v3-*.stl` (`export_v3.py`)

### v2 — 2026-10-29

- **Change:**
  - The lid snaps on with no screws and the corner ears are gone
  - The rocker moves into the lid, which makes the box 3.6 taller (36.4)
  - The MT3608 moves onto a TPU deck over the XIAO, so the box is 12 shorter (104.0)
  - The USB end wall is 5.4 thick and flush, in place of v1's collar
  - Four loops at the base take 12 mm Velcro straps
  - The cell bay is sized to the measured cell, Ø18.5 × 69
  - New snap coupon: a small box and lid with the real snap and the rocker hole
- **Why:** darknetdoll: the external screw mounts were ugly, the outside should be
  smooth, and the pod needs strap loops to hold it to the arm. The rocker should sit on
  top so the parts pack tighter. The ~30 deep rocker sets the height, and that height
  leaves room for the module above the XIAO
- **Files:** `versions/archive/pod-housing-v2-*.stl` (`export_v2.py`)

### v1 — 2026-10-29

- **Change:** first model. The board is on four M2 standoffs and the cell sits beside it
  in its own compartment. The MT3608 pocket and the rocker are past the plug end, with
  J2/J3 snapping into the end wall. The lid seals with a TPU skirt and wall-top bead,
  screwed at four corner ears. Also a wall coupon with every opening, and a USB-C plug
- **Why:** the pod needs one sealed box with the cell inside. Printing it in TPU makes
  the gaskets part of the print. The plug cutouts are JST's own SMP panel spec, so the
  connectors snap in after the board is screwed down
- **Files:** `versions/archive/pod-housing-v1-*.stl` (`export_v1.py`)

---

## Finger trigger ring

Lever microswitch on a ring at the base of the middle finger, lever toward the palm.
Spec and log: [finger-trigger-ring/finger-trigger-ring.md](finger-trigger-ring/finger-trigger-ring.md)

| Version | Date | Status | Files |
|---|---|---|---|
| v4 | 2026-10-29 | Not yet printed. Current | `versions/finger-trigger-ring-v4-c*-full.stl`, `versions/finger-trigger-ring-v4-c*-short.stl` (18 files) |
| v3 | 2026-10-27 | Archived. Same geometry as v4 c65 full | `versions/archive/finger-trigger-ring-v3-c65.stl` |
| v2 | 2026-10-27 | Archived, never printed | `versions/archive/finger-trigger-ring-v2-c65.stl` |
| v1 | 2026-10-27 | Archived, never printed | `versions/archive/finger-trigger-ring-v1-*.stl` |

### v4 — 2026-10-29

- **Change:** v3 in nine sizes, 45 to 65 mm circumference in 2.5 steps. Each comes
  with the full plate and a short one that reaches half as far past the screw holes
  (4.35 instead of 8.7)
- **Why:** bracket the production hands without measuring them, and test whether less
  plate along the finger still holds the switch
- **Files:** `versions/finger-trigger-ring-v4-c<size>-full.stl`, `-short.stl` (`export_v4.py`)

### v3 — 2026-10-27

- **Change:** rounded the split's edges R0.6 and flared the finger-side edges R1.0.
  The screw holes now go right through
- **Why:** sharp edges at the gap and bore pinch the finger. Through holes print without bridging
- **Files:** `versions/archive/finger-trigger-ring-v3-c65.stl` (`export_v3.py`)

### v2 — 2026-10-27

- **Change:** removed the lip behind the switch. Added a 1.0 split through the band
  on the back of the finger. 65 mm bore only
- **Why:** the switch may change, so nothing should be sized to its body. The split
  lets one ring fit a range of hands. Only the 65 test finger is available for now
- **Files:** `versions/archive/finger-trigger-ring-v2-c65.stl` (`export_v2.py`)

### v1 — 2026-10-27

- **Change:** first model. 7 mm band plus a flat saddle on the palm side. The switch
  lies flat, held by two M2 screws into 1.7 pilots, with a lip behind it. Two bores: 50 and 65 mm circumference
- **Why:** test fit and actuation. Curling the finger should fold the palm onto the lever
- **Files:** `versions/archive/finger-trigger-ring-v1-c50.stl`, `versions/archive/finger-trigger-ring-v1-c65.stl` (`export_v1.py`)

---

## Bubble housing

Saddle mount for the Bubble Maker Kit 01 blower head, back of the left hand.
Spec and log: [bubble-housing/bubble-housing.md](bubble-housing/bubble-housing.md)

| Version | Date | Status | Files |
|---|---|---|---|
| v4 | — | Waiting on body measurements (M1–M6, R1–R4) | — |
| gun front print + Velcro slots | 2026-10-21 | Not yet printed | `reference/bubble-gun-toy/front-housing/front-housing-velcro-*.stl` (gitignored, `velcro_slots.py`) |
| gun front print | 2026-10-13 | **Adopted as the new housing direction.** Full halves to print, no coupon | `reference/bubble-gun-toy/front-housing/` (gitignored, regenerate with `cut_front_housing.py`) |
| v3 | 2026-10-11 | **Printed 2026-10-12, does not fit.** Current until v4 | `versions/bubble-housing-v3-base.stl`, `versions/bubble-housing-v3-shroud.stl` |
| v2 | 2026-10-08 | Base archived. Slot coupon current, result not logged yet | `versions/archive/bubble-housing-v2-base.stl`, `versions/bubble-housing-v2-slot-coupon.stl` |
| v1 | 2026-10-07 | Archived. Clip coupons printed and done | `versions/archive/bubble-housing-v1-*.stl` |
| reference | 2026-10-05 | Measurements only, no print | `reference/` (gun model files are gitignored) |

### Gun front print, Velcro slots — 2026-10-21

- **Change:** on both halves, the single slot at 12:00 / 6:00 is filled and replaced by
  two 13 x 2.5 strap slots with a 4 mm bar between them (`velcro_slots.py`)
- **Why:** the strap needs to go down, under a bar and back up to grip the housing;
  one slot gives it nothing to wrap round
- **Files:** `front-housing-velcro-*.stl`, local only (gitignored)

### Gun front print — 2026-10-13

- **Change:** cut the gun's own front housing (both body halves) at the front face of
  the bottle-bay bottom opening (61.0 behind the ring face) and re-clocked it −90°
  about the barrel axis: front screw seats 12/6 → 3/9, clamshell split vertical →
  horizontal (02 = top lid, 01 = cradle), feed-nipple groove kept in the top half
- **Why:** print the proven pocket as-is for the wrist-splint mount while v4 waits on
  the body measurements. Horizontal split lets the head drop into the cradle; screws
  at 3/9 keep the seats off the hand side
- **Files:** stay local (derived from the no-redistribution model); script committed
- **Adopted as the new housing direction** (darknetdoll, 2026-10-13). First print is
  the full halves (`front-housing-bottom-01.stl` + `front-housing-top-02.stl`)
- **No fit coupon** (darknetdoll, 2026-10-13): a 30 mm front coupon was cut and then
  dropped the same day — print the full halves directly

### v4 — planned

- **Change:** rebuild the inside from the blower's real body, section by section:
  - clip moves forward so it grips only the ring section
  - shroud opens up behind the ring
  - add the side-tab slots and a full-length top recess
  - keep v3's nipple groove
- **Why:** v3 failed because the whole head was bored at front-lip size
- **Source:** the "Gun features to borrow" table in
  [bubble-housing/bubble-housing.md](bubble-housing/bubble-housing.md): two-step bore,
  nipple groove, top recess, side slots, air-slot pattern, split shroud with BT2×8 screws
- **Blocked on:** the "Measure for v4" table in the fit-measurements doc

### v3 — 2026-10-11

- **Change:** base C-clip bore 37.8 → 37.6
  - **Why:** clip coupon 1 (37.6) held the ring best. Printed bores run looser than the
    gun's injection-molded 37.8
- **Change:** shroud gains a feed-nipple groove: 6.5 wide, top centre, 12 back from the
  mouth, cut right through the wall
  - **Why:** the 2026-10-08 test found a feed nipple on top of the head. The gun's
    pocket has a matching groove. The slot doubles as the feed-line exit
- **Result, printed 2026-10-12: fail.** The blower head does not go in
  - **Cause:** clip and shroud used the gun's front-lip bore (37.8, then 37.6) along the
    whole head. The gun uses that size only for the first 13.5 (the ring), then opens
    to 39.4 for 38 more
  - **Also missing:** the gun's side slots (3.8 × 30.5) and its top recess (3 deeper,
    26 long)
  - **Also:** the clip sat 8–16 behind the ring face, across the ring-to-body step

### v2 — 2026-10-08

- **Change:** belt-loop openings 27 × 3 → 13 × 2.5 (loops 30 → 19 long)
  - **Why:** Velcro measured 11 wide × 1.1 thick, not the 25 v1 assumed. 13 = 11 + 2
    clearance; 2.5 fits the strap doubled back (2 × 1.1)
- **Change:** new slot coupon: 13 × 2.0, 13 × 2.5, 13 × 3.0
  - **Why:** check the opening width before committing the base
- **Unchanged:** shroud and clip coupons (v1 files)

### v1 — 2026-10-07

- **First fit-test set**, Concept 1 rev B, plain (no clown details):
  - **base:** curved saddle plate (48 × 62, 2.4 thick) + wrist tongue (28 × 36) + four
    belt loops (27 × 3 openings) + C-clip (37.8 bore, 110° opening on top) +
    pedestal + two rear rails
  - **shroud:** separate rear hood. 37.8 bore, closed back, five top vent slots,
    10 × 9 wire exit
  - **clip coupons:** four rings at 37.6 / 37.8 / 38.0 / 38.2, marked by 1–4 bumps
  - **slot coupon:** 22 × 3, 27 × 3, 27 × 4
- **Why these numbers:**
  - clip bore from the gun's front lip (37.8) and the measured ring (37.5)
  - slots assumed 25 mm Velcro
  - plate curve, shroud interior and rails were guesses (stand-in hand, unmeasured bracket)
- **Result, clip coupons printed 2026-10-08:**
  - coupon 1 (37.6) held the ring best → v3
  - test also found the feed nipple → v3

### Reference — 2026-10-05

- Measured the blower pocket of a third-party gun built on the same kit ("Bubble Gun
  Toy" REV1, MakerWorld):
  - front lip 37.8 for 13.5
  - main bore 39.4 for 38
  - 51.6 deep
  - side slots and top recess
- Model files kept local only (no-redistribution license); measurements and scripts
  are committed

---

## Cuff ruffle

Printed lace-look ruffle that straps to the housing's wrist tongue.
Spec and log: [cuff-ruffle/cuff-ruffle.md](cuff-ruffle/cuff-ruffle.md)

| Version | Date | Status |
|---|---|---|
| v0 | 2026-10-08 | Concepts only, nothing printed. r1 = three small tiers; r2 = one big ruffle sleeve, the chosen direction |

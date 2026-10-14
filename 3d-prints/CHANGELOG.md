# 3D print changelog

Every change to a printed part, newest first per part. One line of what changed and
one line of why. Each part's full spec, settings and per-print log are in its own
`<part>.md`.

- **Current files:** `<part>/versions/`
- **Replaced files and finished test pieces:** `<part>/versions/archive/`. Never edited
  or overwritten; each `export_vN.py` still regenerates its own files there
- **Units:** mm

---

## Bubble housing

Saddle mount for the Bubble Maker Kit 01 blower head, back of the left hand.
Spec and log: [bubble-housing/bubble-housing.md](bubble-housing/bubble-housing.md)

| Version | Date | Status | Files |
|---|---|---|---|
| v4 | — | Waiting on body measurements (M1–M6, R1–R4) | — |
| gun front print | 2026-10-13 | **Adopted as the new housing direction.** Full halves to print, no coupon | `reference/bubble-gun-toy/front-housing/` (gitignored, regenerate with `cut_front_housing.py`) |
| v3 | 2026-10-11 | **Printed 2026-10-12, does not fit.** Current until v4 | `versions/bubble-housing-v3-base.stl`, `versions/bubble-housing-v3-shroud.stl` |
| v2 | 2026-10-08 | Base archived. Slot coupon current, result not logged yet | `versions/archive/bubble-housing-v2-base.stl`, `versions/bubble-housing-v2-slot-coupon.stl` |
| v1 | 2026-10-07 | Archived. Clip coupons printed and done | `versions/archive/bubble-housing-v1-*.stl` |
| reference | 2026-10-05 | Measurements only, no print | `reference/` (gun model files are gitignored) |

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

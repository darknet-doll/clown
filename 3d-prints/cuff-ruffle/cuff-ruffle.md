# Cuff Ruffle — v0 (not yet designed)

A printed ruffle that mounts to the bubble housing and gives the wrist end the
lace-cuff look ([DESIGN.md](../../DESIGN.md) "The wrist cuff", reference image
below). It plays the part of the cuff's **lower ruffle** — the one that drapes
over the housing tongue. The fabric cuff keeps the band and the upper ruffle;
this part replaces only the fabric nearest the spinning ring, where floppy lace
is a snag risk and rigid print is actually safer.

Concept renders: `concepts/` (r1 — look only; hand and all hem positions are
stand-ins from the bubble-housing concept, nothing is measured). Knobs to
iterate in `concepts/model.py`: flute count `K`, per-tier flare/amplitude,
scallop depth, hole rows.

## Ground Truth

- `reference/lace-cuff-look.png` — the look being copied (same image as
  `design/wrist-cuff-reference.png`). **Look only — no dimensions come off it**
- Mating interface, from [bubble-housing.md](../bubble-housing/bubble-housing.md):
  - Wrist tongue: 28 wide × 36 long, plate 2.4 thick (design values of the
    mating part, not re-measured)
  - Strap opening: 13 × 2.5, belt-loop bar 3, loop 4 tall (pending the v2 slot
    coupon result)
  - Velcro strap: 11 wide × 1.1 thick (measured 2026-10-08)
- Hand: H3 = 29.21 (width at the wrist end of the back of the hand, from photos,
  still to confirm)
- Distance from the tongue's wrist end to the wrist crease, hand flat and hand
  fully extended: UNKNOWN — this sets the ruffle's maximum length

## Constraints

- **No rigid part touches the wrist crease at full extension.** The glove must
  still come off past it, and a rigid edge at a flexing joint digs in
- Shroud top vent slots and the head's intake stay uncovered
- Nothing enters the ring/wand-wheel sweep, fingers curled or straight
- The tongue's Velcro strap must still thread and tighten with this part fitted
- Hem must drain — no upward-facing cup anywhere on it (openwork doubles as
  drain holes)
- Must not block the feed-line route out of the shroud nipple groove

## Spec

- Mount: flat tab sandwiched under the tongue, held by the tongue's own Velcro
  strap through a matching slot   <- no new fasteners; the strap already clamps
  that exact spot
- Tab width: 28   <- matches the tongue
- Tab slot: 13 × 2.5   <- matches the housing's strap opening; revisit if the v2
  slot coupon picks 2.0 or 3.0
- Everything else: UNKNOWN (form, flare, hem length, wall, pattern, material —
  see Open)

## Print Settings

(none yet — no version exported)

Candidates, undecided: translucent white PETG (stiff, matches the floral-shell
plan, must stop well short of the crease) vs TPU 95A (flexes with the wrist,
kinder edge on skin, prints the ruffle lobes without supports less cleanly).

## Log

(none)

## Open

- Measure: tongue wrist-end → wrist crease, hand flat AND fully extended. Sets
  max hem length; keep ≥ 10 clear at full extension if the part is rigid
- Material: PETG (stiff, translucent, matches floral shell) or TPU 95A (flexes)?
- Form: wavy bell skirt vs overlapping petal scallops? True lace mesh on a
  doubly-curved ruffle is heavy modeling — scalloped openwork (broderie look)
  gets the read at arm's length for far less effort
- Wall: single-wall wavy shell (~0.8–1.2) is the usual trick for printed fabric
  — test a hem coupon before committing to the full skirt
- Does it fully replace the fabric lower ruffle, or sit under a shorter fabric
  one as a stiffener/guard?
- Openwork density: enough holes to drain and read as lace, few enough to hide
  the tongue strap underneath
- Clearance check at the housing fit test: ring sweep, vent slots, strap
  threading, knuckle interference with fingers curled
- Does the strap-sandwich mount rock? If the tab under the tongue lifts the
  housing, recess the tab 1.1 for the strap instead

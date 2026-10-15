# Wrist Splint Mount — v0 (not yet designed)

A TPU remix of a third-party wrist splint that becomes the mount base for the
bubble housing: the splint straps to the wrist/hand with velcro, and the
housing attaches on top of it with velcro (darknetdoll, 2026-10-12). Replaces
the heat-molding plan and possibly the housing's own tongue + hand straps
(see Open).

## Ground Truth

### Reference: "Wrist Splint (Custom Moldable)" by JordanBurghoff

- **Source:** Printables model 1238124, updated 2025-03-21
  (printables.com/model/1238124-wrist-splint-custom-moldable)
- **License:** **CC BY-NC-SA 4.0** — redistribution and remix allowed with
  attribution; derivatives must carry the same license; non-commercial only.
  OK to commit to this public repo with credit; our remixed splint files
  inherit BY-NC-SA
- **Files on the page:** `wrist-splint.stl` (model files, 2 MB) + a 0.2 mm PLA
  MK3S gcode (print files)
- **In `reference/wrist-splint-custom-moldable-print_files/`** (the print-files
  bundle, found 2026-10-12 in the Desktop 3D prints folder): the model PDF and
  `wrist-splint_02mm_pla_mk3s_4h53m.gcode` (gitignored — MK3S-only, 7.8 MB).
  Author's slice: PLA, 0.4 nozzle, 0.2 layers, 48 g, 4.88 h
- From the PDF photos (look only, no dimensions): the splint body is
  honeycomb openwork — already close to the build's lace aesthetic

### wrist-splint.stl, measured (mesh bounds, binary STL, mm; 2026-10-12)

In `reference/wrist-splint-custom-moldable-model_files/`. 32,972 triangles,
units mm, z up from the plate.

| What | Value |
|---|---|
| Flat footprint (x × y) | 229.35 × 197.79 — fits the X1C 256 bed at 100% |
| Thickness (z, printed flat) | 3.50 |
| Secondary z plateau | ~2.5 — likely velcro-channel relief depth; confirm when the channels are mapped |

From the listing (author's text, not measured):

- Prints **flat**; designed to be heat-molded at 80–90 °C (PLA design intent)
- Sized to the max of a 210 × 250 bed; fits wrist circumference ~16–21 cm,
  **18 cm = 100% scale**; adjust by slicer scaling
- Properly scaled, it ends ~1 cm above/below the base of the pinky
- **Velcro channels along both sides**, fit straps up to 20 mm wide; channel
  supports can be cut out to widen them
- Immobilizes the wrist (ulnar/radial), optionally the thumb; fingers free

### From this project (design values of mating parts, not re-measured)

- Velcro strap: 11 wide × 1.1 thick (measured 2026-10-08,
  [bubble-housing.md](../bubble-housing/bubble-housing.md)) — fits the ≤20 channels
- Housing plate: 48 × 62, 2.4 thick; wrist tongue 28 × 36
- Hand: H3 = 29.21 (wrist end of back of hand, from photos, unconfirmed)
- **Wrist circumference: 139.7 (5.5 in)** — darknetdoll, 2026-10-12. Well under
  the author's 160–210 as-provided range, so the scale-down path applies

## Constraints

- **License:** any published remix credits JordanBurghoff and stays
  CC BY-NC-SA 4.0, non-commercial
- The mount patch must resist the blower ring's spin-up torque and vibration.
  Velcro is strong in shear, weak in peel — geometry must take the peel
- Splint + velcro stack raises the drum axis; knuckle and ring-sweep
  clearances from bubble-housing.md still apply on top of the stack
- Blower intake and shroud vent slots stay uncovered
- Left hand. Glove must still go on/off over or under the splint

Openwork pattern concepts:

- `concepts/openwork-swatches-r1.png` — 8 patterns, clown + floral spread
- `concepts/openwork-swatches-r2.png` — circuit direction (darknetdoll
  2026-10-14): CIRCUIT grammar as cutouts, resistors as punctuation,
  harlequin diamonds replacing the house heart signature. 4 layouts
- **r3, the chosen direction: trace bus on the real splint outline** —
  review artifact: claude.ai/artifact/UmpUhLbJdErYzgjE1Fy6Fb.
  `concepts/splint_outline.py` extracts the true outline from the STL
  (`splint-outline.json`); `concepts/trace_bus_r3.py` places the pattern
  with clearance checks (`trace-bus-r3.json` / `.png`);
  `concepts/make_r3_artifact.py` builds the artifact page

## Spec

- Base: the JordanBurghoff splint geometry at **77.6% slicer scale**   <- wrist 139.7 / 180 reference (18 cm = 100%), measured 2026-10-12
- At 77.6%, derived from the measured mesh: footprint 178.0 × 153.5; thickness
  2.72 if scaled uniformly; velcro channels take straps ≤ 15.5, so the 11 mm
  strap still fits
- Z scale: UNKNOWN — uniform 77.6% (2.72 thick) vs holding Z at 100% (3.5
  thick, stiffer in TPU, slightly distorts chamfers). Decide with the TPU
  flop test (see Open)
- Material: TPU 95A (or softer), **never "TPU for AMS"**   <- darknetdoll
  2026-10-12 (flex replaces heat-molding); 2026-10-15: TPU for AMS is Shore
  68D semi-rigid and printed rock-stiff — soft TPU feeds from the external
  spool only
- Wrist attachment: the splint's own side velcro channels, with the 11 mm strap
- Housing attachment: velcro field on the splint's dorsal face, mating velcro
  under the housing   <- darknetdoll 2026-10-12
- Openwork: **trace bus** (CIRCUIT grammar, harlequin accents, no hearts)
  <- darknetdoll 2026-10-14, picked from r2 tile 1; r3 places it. Cutout
  floors: slots 3.0 / webs 3.0 at 100% (2.3 each at print scale)
- Housing velcro patch: solid, 53 × 44 at 100% on the dorsal band (x 25–78,
  y 42–86 in the model frame), doubles as the trace bus's "chip"   <- position
  assumed from thumb-opening adjacency, confirm at first wrap fit
- Everything else: UNKNOWN (see Open)

## Print Settings

v1 (suggested, not yet printed): TPU 95A, **external spool** (AMS bypass),
0.4 nozzle, 0.2 layers, 2 walls, 25% gyroid, slow (~40 mm/s outer). Files
from `export_v1.py`, **pre-scaled to 77.6%** — print at 100%, no further
scaling. Dorsal coupon pair answers the Z-scale question (see Open).

| File | Orientation | Supports |
|---|---|---|
| `versions/wrist-splint-mount-v1-dorsal-coupon-27.stl` | Flat | None. 2.72 thick = uniform-scale candidate |
| `versions/wrist-splint-mount-v1-dorsal-coupon-35.stl` | Flat | None. 3.50 thick = Z-held candidate |

Coupon is 60.5 × 49.7: the velcro patch zone with its die diamond, the pin
comb, and bundle A's trace ends, for wrap-stiffness + patch-stability feel
and TPU cut fidelity. Preview: `versions/wrist-splint-mount-v1-coupon-preview.png`.

v2 (suggested, not yet printed) — **the full splint test print** (darknetdoll
approved the r3 design 2026-10-15). Same settings as v1. From `export_v2.py`,
pre-scaled: **178.0 × 153.5 × 2.72**, print at 100%.

| File | Orientation | Supports |
|---|---|---|
| `versions/wrist-splint-mount-v2-full.stl` | Flat | None |

v2 geometry decisions (also in `export_v2.py`):
- Plate rebuilt as a flat extrusion of the z=1.75 section, not a boolean on
  the original mesh   <- keeps every outline/slot exactly; loses the
  original's edge chamfers, and the channel bridges become full height
  (slightly stronger, threading unchanged)
- Thickness 2.72 = uniform 77.6%   <- keeps all proportions matched to the
  wrist; if the patch is too soft under the housing, re-export at 3.5 (Z held)
- Preview: `versions/wrist-splint-mount-v2-preview.png`

## Log

### 2026-10-15 | v2 | first full print | too stiff | printed in the wrong TPU

- Printed in **Bambu "TPU for AMS" — Shore 68D semi-rigid**, not the spec'd
  TPU 95A. 68D is deliberately stiff so the AMS can feed it; the stiffness is
  the material, not the geometry or settings
- Heat-forming is not a fix (TPU springs back; flat plate warps)
- Keep the print as the rigidity reference for the patch zone
- Reprint plan: true TPU 95A (or 85A for extra comfort) on the external
  spool; 2 walls, 2+2 top/bottom shells, ~15% gyroid, slow

## Open

- Mesh map (outline, channels, thumb opening: done 2026-10-14 via
  `concepts/splint_outline.py`). Still open: confirm which side is dorsal
  when wrapped on the LEFT hand, and whether the whole model needs a mirror
  — decide before any export (a transform: flag it first)
- ~~r3 → full export~~ done 2026-10-15 (`export_v2.py`, extrusion rebuild —
  see Print Settings v2). Still open from it: velcro sew-through holes in the
  patch corners (v2 relies on the pin-comb slots + die diamond as sew points —
  confirm that's enough when attaching the hook field), and the 3.5 Z-held
  re-export if the patch proves too soft
- Handedness may be a non-issue: a flat TPU sheet can simply be flipped over
  when wrapping — confirm on the printed coupon before bothering with mirrors
- Sanity-check the 139.7 circumference once before printing: tape snug (not
  tight) around the wrist crease. 5.5 in is petite; a re-measure costs nothing,
  a wrong scale costs a print
- Handedness: does the thumb cutout make it side-specific? If so, mirror in
  the slicer for the left hand (a transform — flag before doing it)
- TPU flop test: at 77.6% uniform the wall is 2.72 — is the dorsal face
  stable enough under the housing in 95A, or hold Z at 100% (3.5), add a
  stiffer/thicker zone, or a rigid insert under the housing footprint?
  Prefer a dorsal ~40 mm coupon over a full splint print
- Velcro peel under ring torque: locating ridge/pocket on the splint that the
  housing nests into, so velcro only holds down? Or keep one strap over the
  housing tongue as belt-and-braces?
- How does velcro attach to a TPU face? Adhesive-backed hook sticks poorly to
  TPU — printed holes to sew/rivet through, or a printed-in hook-channel strap
  pass instead of a glued field?
- Stack height: splint wall + hook-and-loop (~2–3) + plate 2.4 — re-check
  knuckle clearance and ring sweep with fingers curled
- Does the housing keep its tongue and belt loops (worn over the splint as
  backup) or lose them in a v4? Decide after the first stack fit test
- **Pick an openwork pattern** from `concepts/openwork-swatches-r1.png`
  (or a mix — e.g. one pattern on the forearm, another on the dorsal band).
  Then r2 places the pick on the real splint outline, respecting the velcro
  channels, the solid housing-mount zone, and web ≥ 1.7 after scale
- Cuff-ruffle interaction: the splint now occupies the wrist the fabric cuff
  was covering; where does the printed ruffle tab mount if the tongue goes
  away? (see [cuff-ruffle.md](../cuff-ruffle/cuff-ruffle.md))
- The splint spans the wrist crease by design; in TPU it flexes, but confirm
  full wrist extension is comfortable with the housing mounted

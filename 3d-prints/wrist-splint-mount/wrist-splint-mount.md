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

Openwork pattern concepts: `concepts/openwork-swatches-r1.png` (from
`concepts/openwork_swatches.py`) — 8 swatches, look only, not yet placed on
the splint outline. Awaiting darknetdoll's pick (see Open).

## Spec

- Base: the JordanBurghoff splint geometry at **77.6% slicer scale**   <- wrist 139.7 / 180 reference (18 cm = 100%), measured 2026-10-12
- At 77.6%, derived from the measured mesh: footprint 178.0 × 153.5; thickness
  2.72 if scaled uniformly; velcro channels take straps ≤ 15.5, so the 11 mm
  strap still fits
- Z scale: UNKNOWN — uniform 77.6% (2.72 thick) vs holding Z at 100% (3.5
  thick, stiffer in TPU, slightly distorts chamfers). Decide with the TPU
  flop test (see Open)
- Material: TPU   <- darknetdoll 2026-10-12; flex replaces heat-molding, no wrap needed
- Wrist attachment: the splint's own side velcro channels, with the 11 mm strap
- Housing attachment: velcro field on the splint's dorsal face, mating velcro
  under the housing   <- darknetdoll 2026-10-12
- Everything else: UNKNOWN (see Open)

## Print Settings

(none yet — no version exported)

Candidate: TPU 95A, external spool (AMS bypass on the X1C), 0.4 nozzle.
Hardness and wall/infill undecided — see Open.

## Log

(none)

## Open

- Map the mesh in detail (footprint and thickness done 2026-10-12): outline of
  the dorsal region and whether it reaches the housing's position on the back
  of the hand, velcro channel positions/widths, honeycomb cell size (candidate
  sew-through points for the velcro field), thumb-hole position/handedness
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

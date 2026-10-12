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
- **Files on the page:** `Wrist Splint` STL (2 MB) + a 0.2 mm PLA MK3S gcode.
  **Not yet downloaded — nothing below is measured; it is all listing text**

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

## Constraints

- **License:** any published remix credits JordanBurghoff and stays
  CC BY-NC-SA 4.0, non-commercial
- The mount patch must resist the blower ring's spin-up torque and vibration.
  Velcro is strong in shear, weak in peel — geometry must take the peel
- Splint + velcro stack raises the drum axis; knuckle and ring-sweep
  clearances from bubble-housing.md still apply on top of the stack
- Blower intake and shroud vent slots stay uncovered
- Left hand. Glove must still go on/off over or under the splint

## Spec

- Base: the JordanBurghoff splint geometry, scaled to darknetdoll's wrist   <- scale % UNKNOWN until circumference is measured
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

- **Download the STL** into `reference/` (needs a Printables login; permission
  pending). Then measure off the mesh: dorsal flat area and whether it reaches
  the housing's position on the back of the hand, wall thickness, velcro
  channel positions and widths, overall flat footprint
- Write `reference/ATTRIBUTION.md` (author, link, license) when the file lands
- **Measure darknetdoll's wrist circumference** → scale % (18 cm = 100%)
- Handedness: does the thumb cutout make it side-specific? If so, mirror in
  the slicer for the left hand (a transform — flag before doing it)
- TPU hardness: 95A flops — is the dorsal face stable enough under the
  housing, or does it need a stiffer/thicker zone (or a rigid insert) under
  the housing footprint?
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
- Scaling the splint in the slicer is uniform — does scaling down for a
  smaller wrist thin the velcro channels below the 11 mm strap? Check at the
  chosen %
- Cuff-ruffle interaction: the splint now occupies the wrist the fabric cuff
  was covering; where does the printed ruffle tab mount if the tongue goes
  away? (see [cuff-ruffle.md](../cuff-ruffle/cuff-ruffle.md))
- The splint spans the wrist crease by design; in TPU it flexes, but confirm
  full wrist extension is comfortable with the housing mounted

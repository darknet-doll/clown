# Pod housing

Sealed box for the controller pod. It holds the pod PCB, the 18650 on its PH2.0
pigtail, the MT3608 module (U1), the KCD1 rocker (SW1), and the leads to both arm plugs,
J2 (SM-3) and J3 (SM-4). The box is PETG, so it carries the load and the boards don't.
The seals are printed TPU parts. The case is there to protect the board, so the
XIAO's USB-C has no opening. Flash it with the lid off.

## v8 — current

![preview](versions/pod-housing-v8-preview.png)

v4's layout in PETG, with TPU seals and a lid held by self-tapping screws. J2 and J3
leave on their leads through split grommets. v8 changes only the deck, so that it
prints flat.

**Outside:** 82.8 × 57.6 × 42.2, with 1.2 chamfers on the bottom and lid edges. The
outside is smooth apart from these:

- the rocker's bezel on the back end
- the J2 and J3 grommets in the front end
- four screw heads, flush in the lid
- two strap channels across the lid
- a fingernail notch under the lid edge at the back end, on the cell side

### Ends and wearing

- **Back end (-X):** the end behind the XIAO. The rocker points out of it
- **Front end (+X):** past the board's J2/J3 pads. J2 and J3 leave side by side here,
  each on its lead through a grommet
- **Straps:** two 12 mm Velcro straps go over the top, in 13.5 × 1.0 channels across
  the lid. They sit between the screw heads, 29.4 apart

### Layout

- **Board:** on four standoffs, 3.5 above the floor, with an M2×6 self-tapping screw in
  each corner hole. Its back edge is 2.1 off the back wall, so the XIAO's USB-C socket
  clears the wall by 0.5
- **Rocker:** comes through the back wall at the XIAO's centre line
  - **Fit it with the snap clips at the sides.** Across the clips it's 23. With the
    clips top and bottom, the lower clip hits the XIAO's socket
  - Its 20 body lies over the XIAO, 1.0 clear of the socket
  - Its 30 depth (body 14.5, then terminals and spade lugs) ends near X 25, short of
    C2 at 27
  - The lug wires come off over U2, with room to turn, and run to SW1
- **Cell:** beside the board in its own compartment
  - It rides on three saddles, 1.0 off the floor
  - The lead comes out of the front end, where there's 8.5 to turn it back over the
    cell. The mated PH2.0 pair lies on the cell's front end, past the deck (15.8 of room)
  - The J1 lead crosses the divider through a notch near the J1 pads
- **MT3608:** on a TPU deck on top of the cell, components and leads up. The deck
  starts 9.3 in from the back wall, to clear the screw boss in that corner
  - A lip on the middle of each rail snaps over its 0.95 board
  - **Rail gaps:** the trimpot's brass screw stands 1.1 past the module's long edge.
    The rails have a 6 gap where it sits, on both rails at both ends, so the module
    goes in either way round. The trimpot can't be reached from outside
  - The deck's flat underside presses the cell 0.2 along its top. The wall and the
    divider hold it sideways, 0.15 clear of each
  - Two ribs on the lid press the deck down 0.2
  - U1's wires cross the divider through a notch near the U1 pads
- **J2, J3:** the plugs stay on their leads outside the box. Each lead goes through a
  split TPU grommet in the front wall (darknetdoll's sizes)
  - **J2 (SM-3):** a 10 × 15 opening, long side up, and a 5.0 × 2.5 slot for the wires
  - **J3 (SM-4):** an 8 × 20 opening, long side up, and a 6.0 × 3.0 slot
  - Each plug goes out through its opening first. The grommet's two halves then
    close round the lead, so nothing is re-soldered
  - The slots run across, along the split between the halves, so the wires lie side
    by side between them
  - A panel mount wasn't possible for J2. The pod's SM-3 is the male half, whose
    latch release is at its wire end. In the wall, that release would be inside the
    box, and JST only makes the barbed female half for panels

### Why it's 42.2 tall

The rocker's body is 20 across and has to clear the XIAO's socket, which tops out
12.1 above the floor. That puts the top of its Ø20.6 hole 33.4 above the floor. The
gasket groove and the ledge under it need 2.4 above that, so the wall top is at 35.8.
Add the 2.4 floor and the 4.0 lid. Lifting the module onto the cell makes use of the
height and keeps the length to 82.8.

### Seals and fixings

- **Lid screws:** four M3×8 self-tapping pan heads, straight into the PETG. No inserts
  (darknetdoll: M3 × 6, 8, 10 and 12 on hand)
  - **Bosses:** Ø8.5, centred 5.0 in from the long walls, two on each. They hang from
    the wall top on 45° corbels, so they print without support and leave the floor
    clear
    - Board side: at X 15, past the rocker's body, and X 66, short of the plug leads
    - Cell side: near both corners
  - **Pilot holes:** Ø2.6 × 9.0 deep, with 2.95 of PETG round each
    - An M3×8 bites 6.4, over twice its diameter, with 2.6 spare below its tip
    - If a thread wears out, an M3×10 cuts 2 of fresh thread below it
  - **Lid:** 4.0 thick. Each head sits flush in a Ø6.6 × 2.9 counterbore on a TPU washer
    (6.4 × 2.8 × 0.8). That fits a pan head up to 6.0 × 2.4. The screws are inside
    the gasket line, so the washers seal the screw holes
  - **Hard stops:** the lid seats PETG to PETG on the outer 1.05 of the wall top and
    on the boss tops. Tighten until it seats and no further. The stops take the load
    and the lip does the sealing
  - **Ribs:** 1.6 × 4.5 ribs under the lid run along both long walls between the bosses.
    They keep the lid flat on the lip between the screws
- **Lid gasket:** TPU, a base and a lip
  - The base is 1.3 wide and presses into a 1.2 × 1.0 groove in the wall top. The wall
    top has a 1.0 ledge inside, which carries the groove's inner side
  - The lip leans 45° inward and stands 1.2 proud. A 0.6 pocket in the lid's
    underside squashes it 0.6, and the squashed tip slides about 0.4 inward, inside
    the pocket
  - **Why a lip and not a cord:** 95A is too stiff to squeeze. A solid TPU cord would
    take more force than four M3s can give, and the lid would bow up between them. The
    lip bends instead, with little force and 0.6 of travel to spare
- **Rocker:** a Ø20.6 hole. The v4 coupon's 19.8 TPU hole stayed stretched round the
  body, and PETG won't stretch
  - The wall is thinned from inside to 1.2 across a 26 × 8 band at the sides, where
    the clips catch
  - A TPU washer (Ø23.4 × Ø20.6) goes under the bezel. It seals the gap, and its
    thickness makes up the panel for the clips. There are two, 0.6 and 1.0; use
    whichever lets the clips catch firmly
- **Grommets:** each neck is 0.1 a side smaller than its opening. v6's necks were
  0.15 a side bigger and too tight to push in
  - A flange sits on the outside face, 1.4 past the opening all round
  - A chamfered ridge, 0.5 past the opening, snaps past the inside face
  - The halves split across the long side
  - The wire slot is twice its width long, across the grommet. In J3 that leaves 0.9
    of TPU each side of the slot through the wall
  - darknetdoll meant the slot to run along the long side. Across fits, so it stays

### Measured

darknetdoll, calipers, 2026-10-29. Every value is a constant at the top of
`export_v8.py`.

| What | Measured | Drives |
|---|---|---|
| Pod board thickness | 1.65 | board stack |
| Pod board underside to the top of the XIAO's USB-C socket | 8.6 (socket top 6.95 above the board) | rocker height, so the box height |
| USB-C socket face to the board's far edge | 71.6 (socket stands 1.6 past the edge) | back wall position |
| C3, the 0.1 µF disc, above the board | 5.0 (C2 taken as the same) | clearance under the rocker's lugs |
| MT3608 board, L × W × thickness | 36.8 × 17.2 × 0.95 | deck pocket and lips |
| MT3608 overall height, flat underside to the trimpot screw | 7.9 | room under the lid |
| MT3608 width over the trimpot screw | 18.3 (screw stands 1.1 past the edge) | rail gaps |
| Trimpot screw, centre from the VOUT end, and Ø | 8.9, 2.3 | rail gap position |
| Rocker across the snap clips | 23 | clip band, clips at the sides |
| Rocker body, bezel seat to the terminals | 14.5 | rocker stand-in |
| Rocker depth with the spade lugs on | 30 (20 if soldered direct) | rocker stand-in |
| Spade lug boots: both side by side, one boot | 10, 6.7 | rocker stand-in |
| Cell | Ø18.5 × 69, lead on the end | cell bay |
| Grommets, 2026-10-30: opening and wire slot | J2 10 × 15, 5.0 × 2.5. J3 8 × 20, 6.0 × 3.0 | front wall openings, grommets |

Still not measured:

- **Rocker bezel Ø:** 23 is assumed. It sets the washer's outside
- **Rocker body Ø under the bezel, and the clips' panel range:** these set the
  Ø20.6 hole and the 1.2 panel. The wall coupon tests both
- **C1:** the board needs 28 inside if C1 is 22 tall, and the box has 35.8
- **Screw heads:** pan heads up to 6.0 × 2.4 are assumed

The export's clash check puts stand-ins for all of these in the box and finds no
overlap. The exceptions are deliberate: the deck's and the lid ribs' 0.2 squeezes,
and the gasket's fit and lip squeeze.

### Sources

- **Board:** outline, holes and part positions from [pod_pcb.py](../../docs/pcb/pod_pcb.py).
  Part heights from the [PCB README](../../docs/pcb/README.md): C1 17–22, Q1 ~20,
  F1 ~18
- **JST SM:** catalogue (`jst-mfg.com/product/pdf/eng/eSM.pdf`). Only the SMP plug
  housing (female contacts) has panel barbs. The SMR receptacle (male pins) carries
  the latch arm, with its release at the wire end
- **From darknetdoll, 2026-10-29:**
  - Rocker: out of the back over the board, behind the XIAO, no boot
  - Velcro: 12 wide, over the top
  - J2/J3: on one side, the front end
  - USB-C: no opening
  - Trimpot: must not be reachable from outside
- **From darknetdoll, 2026-10-30:**
  - PETG housing, TPU only for gaskets, and a screwed lid
  - Self-tapping M3 screws, no heat-set inserts
  - The pod's J2 is the male SM-3 half
  - J2 and J3 leave through split grommets, at the sizes above
- **From darknetdoll, 2026-10-30, after the v6 coupons:**
  - The grommets were too tight: 0.5 smaller where they meet the PETG
  - The wire hole was too small: twice as long across
- **From darknetdoll, 2026-10-30, after the v7 grommets:** they fit. The slot runs
  across the short side, not the long side as meant, but it stays

### Print

- **PETG:** bottom, lid, seal tray, wall coupon
  - Use 6 or more wall loops so the 2.4 walls print solid; thin FDM walls leak
    through the layer lines (BUILD step 11)
  - Use 0.2 layers
- **TPU 95A from the external spool:** gasket, seals, deck. Not "TPU for AMS": that's
  68D and too stiff to seal (see
  [wrist-splint-mount.md](../wrist-splint-mount/wrist-splint-mount.md))
- **Bridges:** print them slowly. In the bottom, they're the tops of the grommet
  openings (10 and 8) and of the rocker hole (~7). In the lid, they're the strap
  channel floors (13.5) and the counterbore floors, because the lid prints top face
  down

| File | Material | Orientation | Supports |
|---|---|---|---|
| `versions/pod-housing-v8-bottom.stl` | PETG | Floor down | None. **Print next** |
| `versions/pod-housing-v8-deck.stl` | TPU | Underside down (as exported) | None. **Print next** |
| `versions/pod-housing-v8-lid.stl` | PETG | Top face down (as exported) | None. Same as v6's |
| `versions/pod-housing-v8-gasket.stl` | TPU | Base down (as exported) | None. Same as v6's |
| `versions/pod-housing-v8-seals.stl` | TPU | Flat (as exported) | None. Same as v7's |
| `versions/pod-housing-v8-seal-tray.stl` | PETG | Floor down | None. Same as v6's |
| `versions/pod-housing-v8-wall-coupon.stl` | PETG | On its foot | None. Same as v6's |

Only the bottom and the deck are left to print. The lid, gasket and washers printed
as v6 and the grommets printed as v7 are the same parts in v8.

The seals file holds:

- five screw washers (one spare)
- the two rocker washers, 0.6 and 1.0
- both grommets, as four halves lying on their split faces

### Coupon tests

Test the seal tray first, then the wall coupon.

**Seal tray:** the real wall top, groove and bosses on a tray 15 deep. Test it with
the lid, gasket, screw washers and four M3×8s. The lid and gasket are the real parts,
so keep them if they pass.

1. **The tray alone:** fill it open, 10 deep (about 40 mL), and stand it on a dry
   paper towel for 30 minutes. A wet towel means water is getting through the layer
   lines. That's a print setting (more wall loops, hotter), not the seal. Dry the
   tray before going on
2. **Threads:** with no lid, run an M3×8 straight down into each boss by hand, as far
   as it goes, then back it out
   - Good: it cuts in firmly by hand
   - Pilot too tight: it needs forcing, or the boss cracks
   - Pilot too loose: it spins without biting, or strips
3. **Gasket:** press the base into the groove all round, lip leaning inward. Start at
   the corners and don't stretch it. It should stay in on its own
4. **Lid:** a washer in each counterbore, then the screws. Tighten them diagonally, a
   little at a time, until the lid lands on its stops: the screw suddenly gets much
   harder to turn. Stop there. Check:
   - no gap between the lid and the wall top anywhere, the middle of the long sides
     included. A slip of paper shouldn't go in
   - the heads sit flush with the lid's top, or just below
5. **Lip:** take the lid off and look at the gasket. The lip should be bent evenly all
   round, with the base still down in the groove and the tip not folded outward or
   caught under the lid's edge. Put the lid back, turning each screw backwards until
   it drops into its thread before tightening it
6. **Leak, upside down:** fill 10 deep (a drop of food colouring shows leaks better),
   screw the lid down and turn the tray over onto a dry paper towel. Leave it an
   hour, or overnight. If the towel is wet, note where: which side, the middle or a
   corner, or under a screw head
7. **Leak, on its side:** stand it on each long side for 30 minutes. That puts the
   water on the middle of the side, where the lid would bow between the screws
8. **Reopening (optional):** open and close it 5 to 10 times, backing each screw into
   its thread, then repeat step 6. This shows how fast the bosses wear

**Wall coupon:** the back wall round the rocker hole, and the front wall round both
grommet openings, at their real heights and printed the same way as the bottom. Test
it with the rocker, both rocker washers, J2 and J3 on their leads, and the four
grommet halves.

1. **Rocker hole:** measure it with calipers. It's drawn at Ø20.6. FDM holes usually
   print a little small, so this separates a printer error from a design one
2. **Rocker:** push it in from the outside face, clips at the sides. Try it with no
   washer, then on the 0.6 washer, then on the 1.0. For each, note:
   - whether the body goes in without forcing
   - whether the clips catch firmly, or it wobbles
   - whether the bezel squashes the washer flat all round
   - whether the rocker still clicks freely
3. **Plugs:** push J2's plug through the 10 × 15 opening and J3's through the 8 × 20.
   They should pass without forcing
4. **Grommets:** close the two halves round the lead outside the wall, flange
   outward, and push the grommet in until the ridge snaps past the inside face.
   Check:
   - the flange lies flat on the outside face all round
   - no light shows through the split or round the lead
   - a firm tug on the lead doesn't pull the grommet out
5. **Spray:** spray the outside face for a minute, then wipe the inside face round the
   rocker and each grommet with a dry paper towel. Keep the pod board away from the
   water: an offcut of the same wire through the grommet tests it just as well

Record in the print log:

- **Tray alone:** dry or wet
- **Threads:** how each cut in, and any cracks
- **Lid:** seated with no gap or not, heads flush or proud
- **Lip:** how it looked after the squeeze
- **Leaks:** dry or wet, and where
- **Rocker:** the hole as printed, and which washer, if any, holds it firmly
- **Plugs and grommets:** whether each plug passes, any gaps, and the spray result

### Assembly

1. Run an M3×8 into each boss once, before anything else goes in, to cut the thread
2. Press the gasket's base into the groove all round, lip leaning inward
3. Fit the board onto the standoffs, 4 × M2×6 self-tapping
4. Slip a rocker washer over the rocker's body, then push it in from outside the back
   wall, clips at the sides. Its body lies over the XIAO. Run the lug wires to SW1
5. Push each plug out through its opening: J2 through the 10 × 15, J3 through the
   8 × 20
   - Lay the wires side by side in one grommet half's slot, outside the box, and close
     the other half over them, flange outward
   - Push the grommet in until the ridge snaps past the inside face
   - Put a cable tie on the lead inside, against the grommet, so a tug on the plug
     doesn't reach the solder joints
   - Leave a drip loop outside
6. Lay the cell on the saddles, lead toward the front. Mate PH2.0 and lay the pair
   on the cell's front end
7. Set the deck on the cell behind the pair, rails up. Feed U1's wires over the
   divider notch, then press the MT3608 into its pocket, leads up, until the lips
   click over its board. The trimpot screw goes in a rail gap
8. Lid on, with a TPU washer under each screw head. Tighten the four screws in turn
   until the lid seats
   - Each time, turn each screw backwards until it drops into its thread, then
     tighten. A self-tapper started crooked cuts a new thread and wears the boss out
9. Straps over the top, in the channels

### Decided

- **Seal, no drain** (darknetdoll, 2026-10-29). This overrides BUILD step 11's "drain
  it, don't seal it": no drain hole and no breather
  - Opening the pod to dry it after every event (BUILD step 11) matters more now
- **MT3608 in the cell compartment is fine** (darknetdoll, 2026-10-29). This overrides
  BUILD step 11's rule of nothing soldered in with the cell. The TPU deck keeps the
  module off the cell
- **PETG housing, TPU seals, screwed lid** (darknetdoll, 2026-10-30). An all-TPU box
  leaves the circuit boards to carry the load
- **J2 and J3 on leads through split grommets** (darknetdoll, 2026-10-30), at their
  sizes. No re-soldering
- **Self-tapping M3 screws, no heat-set inserts** (darknetdoll, 2026-10-30)

### Open

- **Thread wear:** the pod is opened after every event to dry it, and self-tapped
  PETG threads wear. Start each screw in its own thread (Assembly 8), and keep
  M3×10s as the fix for a worn boss
- **Lip squeeze:** untested. The seal tray tests it. If it weeps mid-side, the pocket
  can be made shallower, for more squeeze
- **Rocker:** the 20.6 hole, the 1.2 panel and the 23.4 washer rest on unmeasured
  sizes (see Measured). The wall coupon tests them
- **Grommet seal:** the necks are now loose in their openings, so the wall no longer
  squeezes the halves together or onto the wires. The flange on the outside face
  does the sealing. The wall coupon's spray test shows whether that's enough
- **Plugs outside:** unmated, an SM plug is open to the weather. Dielectric grease in
  the shells (BUILD) still applies
- **Arm fit:** the bottom is flat and 57.6 wide, so it will rock on a round upper arm

## v7 — archived, grommets printed

v8, but the deck stood on two pads that pressed the cell 0.2 over two saddles. Its
2.0 plate printed 5.5 off the bed with nothing under it, so it needed supports.

- **Grommets, 2026-10-30:** printed, and they fit. See the print log
- **Files:** `versions/archive/pod-housing-v7-*.stl` (`export_v7.py`)

## v6 — archived, coupons printed

v7, but with tighter grommets and round bores:

- **Grommets:** each neck 0.15 a side bigger than its opening, so the wall squeezed
  the halves together. Flange 1.65 and ridge 0.75 past the opening
- **Bores:** round, Ø2.5 for J2 and Ø3.0 for J3
- **Coupons, 2026-10-30:** see the print log. Everything fitted except the grommets
- **Files:** `versions/archive/pod-housing-v6-*.stl` (`export_v6.py`)

## v5 — archived, never printed

v6, but with heat-set inserts:

- **Lid screws:** four M3×8 button heads into M3 × 4.6 × 5.0 heat-set inserts, in
  4.0 × 7.0 holes
- **Lid:** 3.4 thick, with Ø7.2 × 2.2 counterbores and 7.0 washers
- 82.8 × 57.6 × 41.6
- **Files:** `versions/archive/pod-housing-v5-*.stl` (`export_v5.py`)

## v4 — archived, coupons printed

v6's layout, all in TPU 95A, with a snap lid and J2/J3 panel-mounted in a 1.8 front
wall:

- **Lid:** snapped on with no screws. It had a skirt 0.25 oversize inside the walls, a
  45° snap bead and a wall-top bead
- **Rocker:** a Ø19.8 hole, meant to grip the body, with the wall thinned to 2.0
  round the clips
- **J2, J3:** JST's panel cutout for the SMP plug housing, from the 1.5–2.0 column
- 82.8 × 57.6 × 42.4
- **Coupons, 2026-10-30:** see the print log. Then the housing moved to PETG, because
  an all-TPU box makes the boards structural
- **Files:** `versions/archive/pod-housing-v4-*.stl` (`export_v4.py`)

## v3 — archived, never printed

v4's layout, with estimated part sizes in place of measured ones:

- The MT3608 was assumed to be 36 × 17 × 14 tall, against the measured 36.8 × 17.2 ×
  7.9, so its deck pocket was too short. Its rails had no gaps for the trimpot screw
- The rocker's clips were assumed to stay inside Ø21, against the measured 23
- The XIAO's socket was assumed to stand 1.5 proud, against the measured 1.6
- 82.7 × 57.6 × 42.3
- **Files:** `versions/archive/pod-housing-v3-*.stl` (`export_v3.py`)

## v2 — archived, never printed

Snap lid and module deck as v4. Differences from v4:

- The rocker hung from the lid
- The MT3608 deck sat over the XIAO
- J2 and J3 were on either side of the rocker in the front end
- The USB-C port came through a 5.4 back wall, with a plug
- Four Velcro loops at the base
- 104.0 × 57.3 × 36.4
- **Files:** `versions/archive/pod-housing-v2-*.stl` (`export_v2.py`)

## v1 — archived, never printed

Same board, cell compartment and plug cutouts as v4. Differences from v4:

- The rocker went through the cell-side wall
- The MT3608 had its own bay past the board
- The lid was screwed down with 4 × M3 into corner ears outside the walls
- The USB-C port had a collar standing 3 proud of the end wall
- 116.0 × 57.6 × 32.8, ears to 126 × 68
- **Files:** `versions/archive/pod-housing-v1-*.stl` (`export_v1.py`)

## Print log

| Date | Version | Result |
|---|---|---|
| 2026-10-30 | v4 wall coupon, TPU 95A | **Rocker:** went through the Ø19.8 hole, but the TPU stayed stretched round it, so a rigid wall needs a bigger hole. **SM-3 cutout:** fits the female half, but the pod's J2 is the male half |
| 2026-10-30 | v4 snap coupon, TPU 95A | The lid fits well |
| 2026-10-30 | v6 seal tray and wall coupon (PETG), with the lid (PETG), gasket and seals (TPU 95A) | Everything generally fits. **Grommets:** too tight where they meet the PETG, and the wire hole too small |
| 2026-10-30 | v7 grommets, TPU 95A | Fit. The wire slot runs across the short side, where the long side was meant |

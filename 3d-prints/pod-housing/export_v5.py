# v5: the housing in PETG, sealed with TPU parts, and a screwed lid (darknetdoll,
# 2026-10-30: an all-TPU box leaves the circuit boards as the structure). v4's layout,
# except:
#   lid    four M3x8 button heads into heat-set inserts, in bosses hanging from the
#          long walls, heads flush in counterbores over TPU washers. A TPU lip gasket
#          sits in a groove in the wall top and seals against a pocket in the lid's
#          underside. A lip, not a squeezed cord: 95A is too stiff to squeeze evenly
#          with four screws, so the lid would bow between them
#   plugs  J2 and J3 leave on their leads through split TPU grommets in the front
#          wall. The plugs go through the openings first, so nothing is re-soldered
#          (darknetdoll: J2 10 x 15 with a 2.5 bore, J3 8 x 20 with a 3.0 bore)
#   rocker a 20.6 hole in rigid PETG, thinned to 1.2 behind the clips, with a TPU
#          washer under the bezel. v4's 19.8 TPU hole stayed stretched round the body
# Run from this folder:
#   uv run --with trimesh --with manifold3d --with shapely --with scipy --with pyvista python export_v5.py
#   ->  versions/pod-housing-v5-{bottom,lid,deck,gasket,seals,wall-coupon,seal-tray}.stl + -preview.png
#
# Frame as v1: the PCB's own coordinates with y flipped, so the board is X 0..70,
# Y -30..0. Z up, floor top at Z = 0. -X is the back end (rocker), +X the front
# end (J2, J3). Lid-joint profiles are (d, z): d is the offset from the inner wall
# face, outward positive.
import numpy as np, trimesh
from shapely.geometry import Point, Polygon, box as sbox
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

WALL, FLOOR, LID = 2.4, 2.4, 3.4
EDGE_CH = 1.2                    # 45 degree chamfer on the bottom and lid top edges

# --- board (docs/pcb/pod_pcb.py, README) ---
PCB_L, PCB_W, PCB_T = 70.0, 30.0, 1.65  # thickness measured
HOLES = [(2.5, -2.5), (67.5, -2.5), (2.5, -27.5), (67.5, -27.5)]
STANDOFF = 3.5
BOSS_D = 4.6
PILOT_D, PILOT_DEEP = 1.6, 4.5   # M2x6 self-tapping
PART_MAX = 22.0                  # C1 is 17-22, Q1 ~20, F1 ~18
PCB_TOP = STANDOFF + PCB_T
XIAO_TOP = PCB_TOP + 8.6 - PCB_T       # measured: board underside to socket top, 8.6
USB_MOUTH_X = 70.0 - 71.6              # measured: socket face to the board's far edge, 71.6
C2_C3_H = 5.0                          # measured: the 0.1 uF discs stand 5.0 above the board

# --- KCD1 round rocker, through the back wall ---
ROCKER_DEPTH = 30.0      # measured: bezel seat to the end of the spade lug boots
SW_BODY_D, SW_BODY_DEEP = 20.0, 14.5   # measured: round body, bezel seat to the terminals
SW_LUGS = (10.0, 6.7)                  # measured: both boots side by side, one boot
SW_CLIPS_D = 23.0        # measured across the snap clips. Fit with the clips at the sides
SW_HOLE_D = 20.6         # 20.0 cutout + 0.6. PETG won't stretch; the bezel covers the gap
SW_BEZEL_D = 23.0        # not measured
SW_PANEL = 1.2           # PETG behind the clips. The TPU washer under the bezel adds the rest
SW_WASHERS = (0.6, 1.0)  # two thicknesses: use whichever lets the clips catch
SW_Y = -14.0             # over the XIAO's centre line
SW_Z = XIAO_TOP + SW_BODY_D / 2 + 1.0  # body clears the XIAO by 1.0

# --- lid joint ---
LEDGE, LEDGE_DROP = 1.0, 1.0     # wall top widened inward to carry the groove's inner side
GROOVE_D0, GROOVE_D1, GROOVE_DEEP = 0.0, 1.2, 1.0
RECESS_D0, RECESS_D1, RECESS_DEEP = -2.0, 1.35, 0.6   # pocket in the lid's underside; the
# squashed lip slides ~0.4 inward, to about -1.45
# TPU gasket: a base pressed into the groove (0.05 a side), and a lip leaning 45
# degrees inward whose tip stands 1.2 proud. The pocket squeezes it 0.6
LIP = [(-0.05, -0.95), (1.25, -0.95), (1.25, 0.0), (0.05, 1.2), (-1.05, 1.2), (0.15, 0.0), (-0.05, 0.0)]
# Floor to lid underside: the rocker hole, with the ledge and groove 0.4 above it
H_IN = SW_Z + SW_HOLE_D / 2 + 0.4 + LEDGE + LEDGE_DROP     # 35.8

# --- lid screws: M3x8 button head into M3 x 4.6 x 5.0 heat-set inserts (PARTS.md) ---
INSERT_D, INSERT_DEEP = 4.0, 7.0      # 7.0 not 6.0: the counterbore puts 6.3 of the screw below the lid
SCREW_CLEAR, CB_D, CB_DEEP = 3.4, 7.2, 2.2   # 5.7 head on a TPU washer, flush with the top
SCREW_WASHER = (7.0, 2.8, 0.8)        # OD, ID, thickness
BOSS_R, BOSS_IN, BOSS_H = 4.25, 5.0, 8.0     # in 5.0, so the counterbore barely meets the pocket
STIFF_IN, STIFF_T, STIFF_H = 2.4, 1.6, 4.5   # ribs under the lid, between the bosses

# --- inner outline ---
X_IN0 = USB_MOUTH_X - 0.5            # the XIAO's socket clears the back wall by 0.5
X_IN1 = PCB_L + 5.9
Y_IN1, R_IN = 0.6, 1.6
DIV_Y1, DIV_T = -30.6, 1.6
DIV_Y0 = DIV_Y1 - DIV_T

# --- cell: protected 18650, lead out of one end (darknetdoll: 18.5 x 69) ---
CELL_D, CELL_L = 18.5, 69.0
CELL_BAY = 20.0                    # cell + 1.5, and the deck with the module's rails
Y_IN0 = DIV_Y0 - CELL_BAY
CELL_YC = DIV_Y0 - CELL_BAY / 2
CELL_LIFT = 1.0
CELL_ZC = CELL_LIFT + CELL_D / 2
CELL_TOP = CELL_LIFT + CELL_D
CELL_X0 = X_IN0 + 0.5              # lead end toward the front, room to turn back
SADDLES_X = (9.0, 47.0, 63.0)
SADDLE_T = 2.0

# --- lid screws: two on each long wall. (X, wall's inner face Y, +1/-1 toward the box)
# Board side: clear of the rocker body (ends at X 10) and the plugs' leads.
# Cell side: near the corners, the deck starts past the back one
SCREWS = [(15.0, Y_IN1, -1), (66.0, Y_IN1, -1),
          (X_IN0 + 0.3 + BOSS_R, Y_IN0, 1), (X_IN1 - 0.3 - BOSS_R, Y_IN0, 1)]

# --- front end: J2 and J3 leave on their leads, through split TPU grommets ---
J2_OPEN, J2_BORE = (10.0, 15.0), 2.5   # darknetdoll: opening (across, up) and bore
J3_OPEN, J3_BORE = (8.0, 20.0), 3.0
OPEN_R = 1.0
GROM_FIT, GROM_FLANGE, GROM_RIDGE = 0.15, 1.5, 0.6   # neck interference a side, flange, ridge
GROM_FLANGE_T, GROM_RIDGE_T = 1.2, 1.0
J_Z = 15.0
J2_Y = Y_IN1 - R_IN - 0.5 - GROM_FLANGE - J2_OPEN[0] / 2    # flange clear of the corner
J3_Y = J2_Y - J2_OPEN[0] / 2 - 2 * GROM_FLANGE - 1.5 - J3_OPEN[0] / 2

# --- MT3608 module, on the deck ---
MOD_L, MOD_W, MOD_H, MOD_PCB = 36.8, 17.2, 7.9, 0.95   # measured; leads soldered on top
MOD_FIT = 0.6
TRIM_SCREW = (8.9, 2.3, 1.1)   # measured: centre from the VOUT end, diameter, standing past the edge
RAIL_GAP = 6.0                 # gap in the rails for the screw
DECK_Z0, DECK_T = CELL_TOP + 0.3, 2.0
DECK_TOP = DECK_Z0 + DECK_T
DECK_X0 = SCREWS[2][0] + BOSS_R + 0.5   # past the cell-side back boss
DECK_LAND = 3.5                    # flat deck at each end for the lid's ribs, clear of the rails
MOD_X0 = DECK_X0 + DECK_LAND
MOD_X1 = MOD_X0 + MOD_L + MOD_FIT
DECK_X1 = MOD_X1 + DECK_LAND
DECK_Y0, DECK_Y1 = Y_IN0 + 0.15, DIV_Y0 - 0.15
RAIL_T, RAIL_LIP = 1.0, 0.5
PAD_X = (SADDLES_X[0], SADDLES_X[1])   # deck presses the cell right over two saddles
TRIM_X = (MOD_X0 + MOD_FIT / 2 + TRIM_SCREW[0], MOD_X1 - MOD_FIT / 2 - TRIM_SCREW[0])
RIB_T = 2.0

# --- straps: 12 mm Velcro over the lid, in the gap between the screw heads ---
STRAP_W, STRAP_DEEP = 13.5, 1.0
NOTCH_W = 12.0
_CLEAR = CB_D / 2 + 0.75 + STRAP_W / 2
STRAPS_X = (max(x for x, _, _ in SCREWS if x < 40) + _CLEAR, min(x for x, _, _ in SCREWS if x > 40) - _CLEAR)
TRAY_DEEP = 15.0                   # seal tray: deep enough for the lid's deck ribs

X_OUT0, X_OUT1 = X_IN0 - WALL, X_IN1 + WALL
Y_OUT0, Y_OUT1 = Y_IN0 - WALL, Y_IN1 + WALL
R_OUT = R_IN + WALL
INNER = (X_IN0, Y_IN0, X_IN1, Y_IN1, R_IN)
OUTER = (X_OUT0, Y_OUT0, X_OUT1, Y_OUT1, R_OUT)

U = lambda meshes: trimesh.boolean.union(meshes, engine='manifold')
D = lambda a, bs: trimesh.boolean.difference([a] + list(bs), engine='manifold')
I = lambda a, b: trimesh.boolean.intersection([a, b], engine='manifold')


def rrect(x0, y0, x1, y1, r):
    return sbox(x0, y0, x1, y1).buffer(-r, 32).buffer(r, 32)


def prism(poly, z0, z1, M=None):
    """Extrude a shapely (multi)polygon from z0 to z1, then place it with M."""
    polys = list(getattr(poly, 'geoms', [poly]))
    ms = [trimesh.creation.extrude_polygon(orient(p, 1.0), z1 - z0) for p in polys]
    m = U(ms) if len(ms) > 1 else ms[0]
    m.apply_translation([0, 0, z0])
    if M is not None:
        m.apply_transform(M)
    return m


def wall(origin, u, n):
    """Frame for a wall: local x along u, local y = global Z, local z = outward
    normal n, from the wall's inner face (w = 0) outward."""
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = u, (0, 0, 1), n, origin
    assert np.isclose(np.linalg.det(M[:3, :3]), 1)
    return M


def prism_yz(poly, x0, x1):
    """Profile drawn in (Y, Z), extruded along +X from x0 to x1."""
    return prism(poly, x0, x1, wall((0, 0, 0), (0, 1, 0), (1, 0, 0)))


def box(x0, x1, y0, y1, z0, z1):
    return prism(sbox(x0, y0, x1, y1), z0, z1)


def cyl(r, p0, p1, sections=96):
    return trimesh.creation.cylinder(radius=r, segment=[p0, p1], sections=sections)


def ring(od, id_, t):
    return prism(Point(0, 0).buffer(od / 2, 96).difference(Point(0, 0).buffer(id_ / 2, 96)), 0, t)


def rings(outline, profile, n=24):
    """Rounded-rectangle outline offset by each profile d, as fixed-count rings,
    so consecutive rings stay in step for lofting."""
    x0, y0, x1, y1, r = outline
    corners = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    t = np.radians(np.linspace(0, 90, n))
    out = []
    for d, z in profile:
        assert r + d > 0
        ring_ = []
        for cx, cy, a0 in corners:
            a = np.radians(a0) + t
            ring_ += list(zip(cx + (r + d) * np.cos(a), cy + (r + d) * np.sin(a), np.full(n, z)))
        out.append(ring_)
    return np.array(out)


def loft(R, closed):
    """Faces joining rings R[i] to R[i+1]; closed joins the last back to the first."""
    M, K = R.shape[:2]
    F = []
    for i in range(M if closed else M - 1):
        j = (i + 1) % M
        for k in range(K):
            k2 = (k + 1) % K
            a, b, c, e = i * K + k, i * K + k2, j * K + k2, j * K + k
            F += [(a, b, c), (a, c, e)]
    return F


def finish(V, F):
    m = trimesh.Trimesh(np.array(V), np.array(F))
    if m.volume < 0:
        m.invert()
    assert m.is_watertight and m.is_winding_consistent
    return m


def sweep(outline, profile):
    """Closed (d, z) profile swept round the outline: a ring-shaped solid."""
    R = rings(outline, profile)
    return finish(R.reshape(-1, 3), loft(R, True))


def rr_solid(outline, profile):
    """Solid rounded-rectangle block whose side follows an open (d, z) profile,
    bottom to top, capped flat at both ends (the outline is convex)."""
    R = rings(outline, profile)
    M, K = R.shape[:2]
    V = list(R.reshape(-1, 3))
    F = loft(R, False)
    for ring_i, flip in ((0, True), (M - 1, False)):
        c = len(V)
        V.append(R[ring_i].mean(0))
        for k in range(K):
            a, b = ring_i * K + k, ring_i * K + (k + 1) % K
            F.append((c, b, a) if flip else (c, a, b))
    return finish(V, F)


# ---------------------------------------------------------------------------
# Wall features, in a wall's own (u, v=Z, w) frame
# ---------------------------------------------------------------------------

def rocker_cuts(M, uc, vc):
    """Round hole, and the wall thinned to SW_PANEL from inside across a band at the
    sides where the snap clips catch. The top of the hole prints as a ~7 bridge."""
    band = sbox(uc - SW_CLIPS_D / 2 - 1.5, vc - 4.0, uc + SW_CLIPS_D / 2 + 1.5, vc + 4.0)
    return [prism(Point(uc, vc).buffer(SW_HOLE_D / 2, 128), -1, WALL + 1, M),
            prism(band, -1, WALL - SW_PANEL, M)]


def plug_cuts(M, u2, u3):
    """The two grommet openings. Each plug goes through its own opening on its lead."""
    return [prism(rrect(u - w / 2, J_Z - h / 2, u + w / 2, J_Z + h / 2, OPEN_R), -1, WALL + 1, M)
            for u, (w, h) in ((u2, J2_OPEN), (u3, J3_OPEN))]


def build_grommet(size, bore):
    """TPU grommet in its wall's (u, v, w) frame, centred on the opening: flange
    outside, neck through the wall 0.15 a side oversize, and a chamfered ridge that
    snaps past the inner face. Split across its long side, so the halves close
    round a lead whose plug is already through. Returns the two halves."""
    w, h = size
    outline = (-w / 2, -h / 2, w / 2, h / 2, OPEN_R)
    g = U([rr_solid(outline, [(GROM_FIT + GROM_FLANGE, WALL), (GROM_FIT + GROM_FLANGE, WALL + GROM_FLANGE_T)]),
           rr_solid(outline, [(GROM_FIT, -0.01), (GROM_FIT, WALL + 0.01)]),
           rr_solid(outline, [(GROM_FIT, -GROM_RIDGE_T), (GROM_FIT + GROM_RIDGE, 0.0)])])
    g = D(g, [cyl(bore / 2, (0, 0, -5), (0, 0, 10), 48)])
    return [I(g, box(-50, 50, 0, 50, -50, 50)), I(g, box(-50, 50, -50, 0, -50, 50))]


M_BACK = wall((X_IN0, 0, 0), (0, -1, 0), (-1, 0, 0))    # u = -Y
M_FRONT = wall((X_IN1, 0, 0), (0, 1, 0), (1, 0, 0))     # u = Y


def placed(m, M, uc, vc):
    m = m.copy()
    m.apply_translation([uc, vc, 0])
    m.apply_transform(M)
    return m


# ---------------------------------------------------------------------------
# Bottom
# ---------------------------------------------------------------------------

def hanging_boss(xb, yw, s):
    """Screw boss hanging from the top of a long wall (inner face at Y = yw, box
    toward s), on a 45 degree corbel so it prints without support."""
    yc = yw + s * BOSS_IN
    reach = BOSS_IN + BOSS_R
    zb = H_IN - BOSS_H
    plan = unary_union([Point(xb, yc).buffer(BOSS_R, 64),
                        sbox(xb - BOSS_R, min(yw - s, yc), xb + BOSS_R, max(yw - s, yc))])
    col = prism(plan, zb - reach - 1.0, H_IN)
    # z >= zb - reach + y, with y measured into the box from the wall face
    wedge = Polygon([(yw + s * y, z) for y, z in ((-1.0, zb - reach - 1.0), (reach + 1.0, zb + 1.0),
                                                  (reach + 1.0, H_IN + 1.0), (-1.0, H_IN + 1.0))])
    return I(col, prism_yz(wedge, xb - BOSS_R - 1, xb + BOSS_R + 1))


def shell(z0):
    """Walls and floor (floor top at z0), the ledge and gasket groove round the wall
    top, and the screw bosses with their insert holes."""
    outer = rr_solid(OUTER, [(-EDGE_CH, z0 - FLOOR), (0, z0 - FLOOR + EDGE_CH), (0, H_IN)])
    body = D(outer, [prism(rrect(*INNER), z0, H_IN + 1)])
    ledge = sweep(INNER, [(0.3, H_IN - LEDGE_DROP - LEDGE - 0.3), (-LEDGE, H_IN - LEDGE_DROP),
                          (-LEDGE, H_IN), (0.3, H_IN)])
    body = U([body, ledge] + [hanging_boss(x, yw, s) for x, yw, s in SCREWS])
    body = I(body, box(X_OUT0 - 1, X_OUT1 + 1, Y_OUT0 - 1, Y_OUT1 + 1, z0 - FLOOR, H_IN))
    cuts = [sweep(INNER, [(GROOVE_D0, H_IN - GROOVE_DEEP), (GROOVE_D1, H_IN - GROOVE_DEEP),
                          (GROOVE_D1, H_IN + 1), (GROOVE_D0, H_IN + 1)])]
    cuts += [cyl(INSERT_D / 2, (x, yw + s * BOSS_IN, H_IN - INSERT_DEEP), (x, yw + s * BOSS_IN, H_IN + 1), 48)
             for x, yw, s in SCREWS]
    return D(body, cuts)


def build_bottom():
    inner = [cyl(BOSS_D / 2, (x, y, -0.01), (x, y, STANDOFF)) for x, y in HOLES]
    divider = box(X_IN0 - 0.1, X_IN1 + 0.1, DIV_Y0, DIV_Y1, -0.01, H_IN - 0.4)
    divider = D(divider, [box(4.0, 20.0, DIV_Y0 - 1, DIV_Y1 + 1, DECK_TOP + MOD_PCB + 0.5, H_IN),  # U1 wires
                          box(55.0, 66.0, DIV_Y0 - 1, DIV_Y1 + 1, 21.0, H_IN)])                    # J1 lead
    inner.append(divider)
    for x in SADDLES_X:
        s = sbox(Y_IN0 - 0.1, -0.01, DIV_Y0 + 0.1, CELL_ZC - 2.0).difference(
            Point(CELL_YC, CELL_ZC).buffer(CELL_D / 2 + 0.2, 96))
        inner.append(prism_yz(s, x - SADDLE_T / 2, x + SADDLE_T / 2))
    body = U([shell(0.0)] + inner)
    cuts = rocker_cuts(M_BACK, -SW_Y, SW_Z) + plug_cuts(M_FRONT, J2_Y, J3_Y)
    cuts += [cyl(PILOT_D / 2, (x, y, STANDOFF - PILOT_DEEP), (x, y, STANDOFF + 1), 32) for x, y in HOLES]
    return D(body, cuts)


# ---------------------------------------------------------------------------
# Lid: printed upside down, top face on the bed
# ---------------------------------------------------------------------------

def lid_notch(x_out0, yc, zt):
    """Fingernail notch under the lid's edge, outside the gasket pocket."""
    return box(x_out0 - 1, x_out0 + WALL - 1.6, yc - NOTCH_W / 2, yc + NOTCH_W / 2, zt - 1, zt + 1.0)


def build_lid():
    plate = rr_solid(OUTER, [(0, H_IN), (0, H_IN + LID - EDGE_CH), (-EDGE_CH, H_IN + LID)])
    parts = [plate]
    # ribs along the long walls, between the bosses, so the lid stays flat on the lip
    for (xa, yw, s), (xb, _, _) in ((SCREWS[0], SCREWS[1]), (SCREWS[2], SCREWS[3])):
        y0, y1 = sorted((yw + s * STIFF_IN, yw + s * (STIFF_IN + STIFF_T)))
        parts.append(box(xa + BOSS_R + 0.5, xb - BOSS_R - 0.5, y0, y1, H_IN - STIFF_H, H_IN + 0.01))
    # ribs that hold the deck down at both ends, 0.2 squeeze, stopped short of the lip
    for x in (DECK_X0 + DECK_LAND / 2, DECK_X1 - DECK_LAND / 2):
        parts.append(box(x - RIB_T / 2, x + RIB_T / 2, Y_IN0 + STIFF_IN, DECK_Y1 - 0.4, DECK_TOP - 0.2, H_IN + 0.01))
    top = H_IN + LID
    pocket = rrect(*INNER).buffer(RECESS_D1, 64).difference(rrect(*INNER).buffer(RECESS_D0, 64))
    cuts = [prism(pocket, H_IN - 1, H_IN + RECESS_DEEP)]
    for x, yw, s in SCREWS:
        y = yw + s * BOSS_IN
        cuts += [cyl(SCREW_CLEAR / 2, (x, y, H_IN - 1), (x, y, top + 1), 48),
                 cyl(CB_D / 2, (x, y, top - CB_DEEP), (x, y, top + 1), 64)]
    cuts += [box(x - STRAP_W / 2, x + STRAP_W / 2, Y_OUT0 - 1, Y_OUT1 + 1, top - STRAP_DEEP, top + 1)
             for x in STRAPS_X]
    cuts.append(lid_notch(X_OUT0, CELL_YC, H_IN))
    return D(U(parts), cuts)


# ---------------------------------------------------------------------------
# TPU: gasket, deck, small seals
# ---------------------------------------------------------------------------

def build_gasket():
    """Lid gasket in place in the wall-top groove. Prints base down, as exported."""
    return sweep(INNER, [(d, H_IN + z) for d, z in LIP])


def build_deck():
    """Carries the MT3608 on top of the cell. Printed flat, underside down."""
    plan = sbox(DECK_X0, DECK_Y0, DECK_X1, DECK_Y1).intersection(rrect(*INNER).buffer(-0.15, 32))
    parts = [prism(plan, DECK_Z0, DECK_TOP)]
    # pads under it press the cell 0.2, right over two saddles
    for x in PAD_X:
        p = sbox(DECK_Y0, CELL_ZC + 4.0, DECK_Y1, DECK_Z0 + 0.01).difference(
            Point(CELL_YC, CELL_ZC).buffer(CELL_D / 2 - 0.2, 96))
        parts.append(prism_yz(p, x - 2.0, x + 2.0))
    top = DECK_TOP
    rails = ((DECK_Y0, DECK_Y0 + RAIL_T), (DECK_Y1 - RAIL_T, DECK_Y1))
    rail_ms = U([box(MOD_X0 - 0.5, MOD_X1 + 0.5, y0, y1, top - 0.01, top + MOD_PCB + 2.6) for y0, y1 in rails])
    # The trimpot's screw stands past the module's long edge. Gap both rails at both
    # ends, so the module goes in either way round
    parts.append(D(rail_ms, [box(c - RAIL_GAP / 2, c + RAIL_GAP / 2, DECK_Y0 - 1, DECK_Y1 + 1, top - 0.1, top + 10)
                             for c in TRIM_X]))
    # One lip per rail, between the gaps. Its 45 degree underside clears the
    # module's top edge by 0.1
    lip_z = top + MOD_PCB + 0.35
    xa, xb = TRIM_X[0] + RAIL_GAP / 2 + 1.0, TRIM_X[1] - RAIL_GAP / 2 - 1.0
    for y_face, s in ((rails[0][1], 1), (rails[1][0], -1)):
        lip = Polygon([(y_face, lip_z - RAIL_LIP), (y_face, lip_z + 0.8),
                       (y_face + s * RAIL_LIP, lip_z + 0.8), (y_face + s * RAIL_LIP, lip_z)])
        parts.append(prism_yz(lip, xa, xb))
    for x0, x1 in ((MOD_X0 - 0.5, MOD_X0), (MOD_X1, MOD_X1 + 0.5)):
        parts.append(box(x0, x1, rails[0][1] + 4, rails[1][0] - 4, top - 0.01, top + 1.2))
    return U(parts)


def flat_half(h):
    """A grommet half turned onto its split face for printing."""
    h = h.copy()
    up = h.bounds[1][1] > 0.01
    h.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2 if up else -np.pi / 2, [1, 0, 0]))
    return h


def build_seals():
    """The small TPU seals, flat as printed, in one row: five screw washers (one
    spare), the two rocker washers, and both grommets as four halves."""
    od, id_, t = SCREW_WASHER
    items = [ring(od, id_, t) for _ in range(5)]
    items += [ring(SW_BEZEL_D + 0.4, SW_HOLE_D, t) for t in SW_WASHERS]
    for size, bore in ((J2_OPEN, J2_BORE), (J3_OPEN, J3_BORE)):
        items += [flat_half(h) for h in build_grommet(size, bore)]
    x, out = 0.0, []
    for m in items:
        m = m.copy()
        m.apply_translation([x - m.bounds[0][0], -m.bounds[0][1], -m.bounds[0][2]])
        x = m.bounds[1][0] + 3.0
        out.append(m)
    return U(out)


# ---------------------------------------------------------------------------
# Coupons
# ---------------------------------------------------------------------------

def build_wall_coupon():
    """The back wall round the rocker hole and the front wall round both grommet
    openings, at their real heights and in the bottom's print orientation. PETG,
    stands on a foot."""
    Mc = wall((0, 0, 0), (1, 0, 0), (0, -1, 0))      # inner face at Y = 0, outward -Y
    u2 = 28.0 + GROM_FLANGE + J2_OPEN[0] / 2 + 1.0
    u3 = u2 + (J2_Y - J3_Y)
    L = u3 + J3_OPEN[0] / 2 + GROM_FLANGE + 2.0
    plate = prism(sbox(0, -FLOOR, L, SW_Z + SW_HOLE_D / 2 + 2.5), 0, WALL, Mc)
    foot = box(0, L, 0, 12.0, -FLOOR, 0)
    return D(U([plate, foot]), rocker_cuts(Mc, 14.0, SW_Z) + plug_cuts(Mc, u2, u3))


def build_seal_tray():
    """The real wall top, groove, bosses and inserts on a shallow tray, for the real
    lid and gasket: screw down, fill with water, turn over."""
    return shell(H_IN - TRAY_DEEP)


# ---------------------------------------------------------------------------
# Stand-ins for the parts, for the clash check and the preview
# ---------------------------------------------------------------------------

def stand_ins():
    t = PCB_TOP
    seat = X_OUT0 - SW_WASHERS[0]                    # bezel seat, on the thin washer
    panel = X_IN0 - (WALL - SW_PANEL) + 0.01         # inside face of the thinned panel
    m0, my0 = MOD_X0 + MOD_FIT / 2, DECK_Y0 + RAIL_T + 0.25   # module, VOUT end at -X, screw at -Y
    return {
        'board': box(0, PCB_L, -PCB_W, 0, STANDOFF, t),
        'XIAO': box(-0.4, 20.85, -22.9, -5.1, t, t + 2.5 + 1.2 + 2.6),
        'USB-C': box(USB_MOUTH_X, 7.0, -14.0 - 4.47, -14.0 + 4.47, XIAO_TOP - 3.2, XIAO_TOP),
        'U2': box(25.9, 43.3, -21.0, -11.0, t, t + 5.3),
        'C2': box(27.0, 32.0, -9.65, -7.15, t, t + C2_C3_H),
        'C3': box(22.15, 24.65, -18.6, -13.6, t, t + C2_C3_H),
        'C1': cyl(5.0, (49.0, -9.0, t), (49.0, -9.0, t + PART_MAX)),
        'Q1': box(45.7, 55.8, -21.0, -16.0, t, t + 20.0),
        'F1': box(24.0, 39.0, -29.0, -24.6, t, t + 18.0),
        'cell': cyl(CELL_D / 2, (CELL_X0, CELL_YC, CELL_ZC), (CELL_X0 + CELL_L, CELL_YC, CELL_ZC)),
        'MT3608': U([box(m0, m0 + MOD_L, my0, my0 + MOD_W, DECK_TOP, DECK_TOP + MOD_PCB),
                     box(m0 + 2, m0 + 12, my0 + 1, my0 + 11, DECK_TOP + MOD_PCB, DECK_TOP + MOD_H),
                     box(m0 + TRIM_SCREW[0] - TRIM_SCREW[1] / 2, m0 + TRIM_SCREW[0] + TRIM_SCREW[1] / 2,
                         my0 - TRIM_SCREW[2], my0 + 1, DECK_TOP + MOD_PCB + 1.5,
                         DECK_TOP + MOD_PCB + 1.5 + TRIM_SCREW[1])]),
        'rocker': U([cyl(SW_BODY_D / 2, (panel, SW_Y, SW_Z), (seat + SW_BODY_DEEP, SW_Y, SW_Z)),
                     box(seat + SW_BODY_DEEP - 0.01, seat + ROCKER_DEPTH, SW_Y - SW_LUGS[0] / 2,
                         SW_Y + SW_LUGS[0] / 2, SW_Z - SW_LUGS[0] / 2, SW_Z + SW_LUGS[0] / 2)] +
                    [box(panel, panel + 4.0, min(SW_Y + s * 9.5, SW_Y + s * SW_CLIPS_D / 2),
                         max(SW_Y + s * 9.5, SW_Y + s * SW_CLIPS_D / 2), SW_Z - 3.0, SW_Z + 3.0)
                     for s in (-1, 1)]),
        'bezel': U([cyl(SW_BEZEL_D / 2, (seat, SW_Y, SW_Z), (seat - 2.0, SW_Y, SW_Z)),
                    cyl(SW_BEZEL_D / 2 + 0.2, (X_OUT0, SW_Y, SW_Z), (seat, SW_Y, SW_Z))]),
    }


def outside_parts():
    """Both grommets in their openings, and each plug hanging a little way out on
    its lead. For the preview only."""
    out = {}
    for name, u, size, bore, plug in (('J2', J2_Y, J2_OPEN, J2_BORE, (10.5, 7.5, 18.2)),
                                      ('J3', J3_Y, J3_OPEN, J3_BORE, (7.4, 10.5, 11.7))):
        out[name + ' grommet'] = U([placed(h, M_FRONT, u, J_Z) for h in build_grommet(size, bore)])
        x0 = X_OUT1 + GROM_FLANGE_T + 6.0
        lead = cyl(bore / 2, (X_IN1 - 3.0, u, J_Z), (x0 + 0.5, u, J_Z), 24)
        out[name + ' plug'] = U([lead, box(x0, x0 + plug[2], u - plug[0] / 2, u + plug[0] / 2,
                                           J_Z - plug[1] / 2, J_Z + plug[1] / 2)])
    return out


def straps():
    out = []
    top = H_IN + LID
    for xc in STRAPS_X:
        x0, x1 = xc - 6.0, xc + 6.0
        out.append(box(x0, x1, Y_OUT0 - 1.1, Y_OUT1 + 1.1, top - STRAP_DEEP + 0.05, top - STRAP_DEEP + 1.15))
        for y0, y1 in ((Y_OUT0 - 1.15, Y_OUT0 - 0.05), (Y_OUT1 + 0.05, Y_OUT1 + 1.15)):
            out.append(box(x0, x1, y0, y1, -FLOOR - 8, top - STRAP_DEEP + 1.15))
    return out


def preview(bottom, lid, deck, gasket, seals, wall_c, tray, parts, outside, out):
    import pyvista as pv
    pv.OFF_SCREEN = True
    colors = {'board': '#1f8a6e', 'XIAO': '#c0c3c9', 'USB-C': '#e8e8e8', 'U2': '#2a2a2e',
              'C2': '#e0a030', 'C3': '#e0a030', 'C1': '#3b4c9a', 'Q1': '#2a2a2e', 'F1': '#f0c832',
              'cell': '#d9584a', 'MT3608': '#3f72d9', 'rocker': '#202020', 'bezel': '#202020'}
    petg, tpu, strap_c, plug_c = '#dfe3ea', '#5a8fd0', '#f08a3c', '#111111'
    labels = {'board': (55, -25, PCB_TOP), 'cell': (CELL_X0 + 60, CELL_YC, CELL_TOP),
              'MT3608 on deck': (MOD_X0 + 18, CELL_YC, DECK_TOP + MOD_H),
              'rocker': (X_IN0 + 12, SW_Y, SW_Z + 10), 'J2': (X_OUT1, J2_Y, J_Z + 9),
              'J3': (X_OUT1, J3_Y, J_Z + 12)}
    strap_ms = straps()

    def mesh(p, m, color, opacity=1.0):
        p.add_mesh(pv.wrap(m).compute_normals(feature_angle=35, split_vertices=True),
                   color=color, opacity=opacity, smooth_shading=False)

    pl = pv.Plotter(off_screen=True, shape=(2, 2), window_size=(1800, 1300), border=False)
    c = np.array([(X_OUT0 + X_OUT1) / 2, (Y_OUT0 + Y_OUT1) / 2, 14])
    views = [((0, 0), tuple(c + (-150, -130, 150)), 'closed, from the back: rocker, flush screws, straps', True),
             ((0, 1), tuple(c + (150, 110, 150)), 'lid off, from the front: grommets, gasket, bosses', False),
             ((1, 0), tuple(c + (0, 0, 260)), 'from above, lid off', False)]
    for (r, k), pos, title, with_lid in views:
        pl.subplot(r, k)
        pl.set_background('white')
        mesh(pl, bottom, petg, 0.55 if r == 1 else 1.0)
        for name, m in outside.items():
            mesh(pl, m, tpu if 'grommet' in name else plug_c)
        if with_lid:
            mesh(pl, lid, petg)
            mesh(pl, parts['bezel'], colors['bezel'])
            for m in strap_ms:
                mesh(pl, m, strap_c)
        else:
            mesh(pl, gasket, tpu)
            mesh(pl, deck, tpu)
            for name, m in parts.items():
                mesh(pl, m, colors[name])
        if r == 1:
            pts = np.array(list(labels.values()), float)
            pl.add_point_labels(pts, list(labels), font_size=14, point_size=6, shape_opacity=0.8,
                                always_visible=True, text_color='black', shape_color='white')
            pl.enable_parallel_projection()
        pl.add_text(title, font_size=10, color='black')
        pl.camera_position = [pos, tuple(c), (0, 1, 0) if r == 1 else (0, 0, 1)]
        pl.reset_camera()
        pl.camera.zoom(1.3 if r == 1 else 1.15)
    pl.subplot(1, 1)
    pl.set_background('white')
    flip = lid.copy()
    flip.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    lay = [(flip, petg, (0, 0)), (tray.copy(), petg, (95, 0)), (wall_c.copy(), petg, (190, 0)),
           (gasket.copy(), tpu, (0, -75)), (deck.copy(), tpu, (95, -75)), (seals.copy(), tpu, (0, -100))]
    allb = []
    for m, col, (dx, dy) in lay:
        m.apply_translation([dx - m.bounds[0][0], dy - m.bounds[0][1], -m.bounds[0][2]])
        mesh(pl, m, col)
        allb.append(m.bounds)
    pl.add_text('as printed. PETG: lid (top down), seal tray, wall coupon\n'
                'TPU: gasket, deck, washers and grommet halves', font_size=10, color='black')
    allb = np.vstack(allb)
    cc = (allb.min(0) + allb.max(0)) / 2
    pl.camera_position = [tuple(cc + np.array([-60, -200, 260])), tuple(cc), (0, 0, 1)]
    pl.reset_camera()
    pl.camera.zoom(1.3)
    pl.enable_anti_aliasing('ssaa')
    pl.screenshot(out)
    pl.close()


if __name__ == '__main__':
    bottom, lid, deck, gasket = build_bottom(), build_lid(), build_deck(), build_gasket()
    seals, wall_c, tray = build_seals(), build_wall_coupon(), build_seal_tray()
    parts, outside = stand_ins(), outside_parts()

    print(f'H_IN {H_IN:.1f}  rocker centre Z {SW_Z:.1f}, hole top {SW_Z + SW_HOLE_D / 2:.1f}, '
          f'groove floor {H_IN - GROOVE_DEEP:.1f}, ledge toe {H_IN - LEDGE_DROP - LEDGE:.1f}')
    print(f'screws {[(round(x, 2), round(y + s * BOSS_IN, 2)) for x, y, s in SCREWS]}  '
          f'straps at X {STRAPS_X[0]:.1f}, {STRAPS_X[1]:.1f}  J2 Y {J2_Y:.2f}  J3 Y {J3_Y:.2f}  '
          f'deck X {DECK_X0:.1f}..{DECK_X1:.1f}')
    print('clash check (stand-in volume inside the housing or the deck, mm^3):')
    closed = U([bottom, lid, deck])
    for k, m in parts.items():
        if k == 'bezel':
            continue
        v = max(I(m, closed).volume, 0.0)
        print(f'  {k:7s} {v:8.2f}' + ('   <- deck pads squeeze the cell 0.2, by design' if k == 'cell' else ''))
    print(f'  deck vs bottom {max(I(deck, bottom).volume, 0):.2f}   deck vs lid {max(I(deck, lid).volume, 0):.2f}'
          '   <- lid ribs squeeze the deck 0.2, by design')
    print(f'  lid vs bottom {max(I(lid, bottom).volume, 0):.2f}   <- should be 0: PETG meets PETG on the hard stops')
    print(f'  gasket vs bottom {max(I(gasket, bottom).volume, 0):.2f}   <- base 0.05 a side in the groove')
    print(f'  gasket vs lid {max(I(gasket, lid).volume, 0):.2f}   <- lip squeezed 0.6 by the pocket')
    for name in ('J2', 'J3'):
        g = outside[name + ' grommet']
        print(f'  {name} grommet vs bottom {max(I(g, bottom).volume, 0):.2f}   <- neck 0.15 a side, ridge on the inner face'
              f'   vs lid/deck/gasket {max(I(g, U([lid, deck, gasket])).volume, 0):.2f}')

    out = {'bottom': bottom, 'lid': lid, 'deck': deck, 'gasket': gasket, 'seals': seals,
           'wall-coupon': wall_c, 'seal-tray': tray}
    for name, m in out.items():
        m = m.copy()
        if name == 'lid':                         # print orientation: top face down
            m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
        m.apply_translation([0, 0, -m.bounds[0][2]])
        m.export(f'versions/pod-housing-v5-{name}.stl')
        e = np.round(m.extents, 1)
        print(f'{name:12s} {e[0]} x {e[1]} x {e[2]}  volume {m.volume / 1000:.1f} cm^3  '
              f'watertight={m.is_watertight}  bodies={len(m.split(only_watertight=False))}')
    print(f'outer box {X_OUT1 - X_OUT0:.1f} x {Y_OUT1 - Y_OUT0:.1f} x {H_IN + FLOOR + LID:.1f}')
    preview(bottom, lid, deck, gasket, seals, wall_c, tray, parts, outside, 'versions/pod-housing-v5-preview.png')

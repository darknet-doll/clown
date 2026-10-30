# v3: the rocker points out of the back end, its body lying over the XIAO, and J2/J3
# sit side by side in the front end wall. The straps run over the lid in two
# shallow channels. No USB opening: the case protects the board, and the XIAO is
# flashed with the lid off. The MT3608 rides on a deck over the cell.
# Run from this folder:
#   uv run --with trimesh --with manifold3d --with shapely --with scipy --with pyvista python export_v3.py
#   ->  versions/pod-housing-v3-{bottom,lid,deck,wall-coupon,snap-coupon}.stl + -preview.png
#
# Frame as v1: the PCB's own coordinates with y flipped, so the board is X 0..70,
# Y -30..0. Z up, floor top at Z = 0. -X is the back end (rocker), +X the front
# end (J2, J3).
#
#   row A  board on four standoffs. The rocker comes through the back wall at the
#          XIAO end and lies over the XIAO
#   row B  the cell in its own compartment beside the board. The MT3608 lies on a
#          TPU deck on top of the cell, and the lid holds the deck down
#   front  J2 (SM-3) and J3 (SM-4) side by side, in line with the board
#
# Seals, all in the TPU itself:
#   lid    skirt 0.25 oversize inside the walls, a snap bead that drops into a
#          groove in the walls, and a bead on the wall top that the snap keeps
#          squashed. No screws, so no holes. The straps over the top hold it too
#   plugs  JST's own panel cutout for the SMP housing, in a 1.8 end wall
#   rocker hole 0.2 under the 20 mm cutout. The TPU grips the body all round, and
#          the bezel sits on the flat back wall
import numpy as np, trimesh
from shapely.geometry import Point, Polygon, LineString, box as sbox
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

WALL, FLOOR, LID = 2.4, 2.4, 2.4
EDGE_CH = 1.2                    # 45 degree chamfer on the bottom and lid top edges

# --- board (docs/pcb/pod_pcb.py, README) ---
PCB_L, PCB_W, PCB_T = 70.0, 30.0, 1.6
HOLES = [(2.5, -2.5), (67.5, -2.5), (2.5, -27.5), (67.5, -27.5)]
STANDOFF = 3.5
BOSS_D = 4.6
PILOT_D, PILOT_DEEP = 1.6, 4.5   # M2x6 self-tapping
PART_MAX = 22.0                  # C1 is 17-22, Q1 ~20, F1 ~18
PCB_TOP = STANDOFF + PCB_T
XIAO_TOP = PCB_TOP + 2.5 + 1.2 + 3.2   # header spacer, XIAO PCB, USB-C socket. NOT MEASURED
USB_MOUTH_X = -1.5                     # socket stands 1.5 past the board edge

# --- KCD1 round rocker, through the back wall ---
ROCKER_DEPTH = 30.0      # bezel seat to the end of the spade lugs (darknetdoll, about 30)
SW_BODY_D, SW_BODY_DEEP = 20.0, 18.0   # round body, then the terminals and lugs
SW_LUGS = (16.0, 9.0)                  # lug block, across x up
SW_CLIP_R = 10.5         # body plus snap clips, for clearance above
SW_HOLE_D = 19.8         # 20.0 cutout less 0.2 so the TPU grips the body
SW_BEZEL_D = 23.0
SW_PANEL, SW_SPOT_D = 2.0, 23.0
SW_Y = -14.0             # over the XIAO's centre line
SW_Z = XIAO_TOP + SW_BODY_D / 2 + 1.0  # body clears the XIAO by 1.0

# --- lid joint ---
SKIRT_H = 3.7
FACE_BEAD_W, FACE_BEAD_H = 1.0, 0.3
# Floor to lid underside: the rocker body and the skirt above it set this
H_IN = max(PCB_TOP + PART_MAX + 0.9, SW_Z + SW_CLIP_R + 0.3 + SKIRT_H)     # 37.5

# --- inner outline ---
X_IN0 = USB_MOUTH_X - 0.5            # the XIAO's socket clears the back wall by 0.5
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
SADDLES_X = (3.0, 33.0, 63.0)
SADDLE_T = 2.0

# --- front end: J2, J3. JST SM plug housing (SMP-0xV-BC) panel cutout, eSM.pdf ---
FRONT_WALL = 1.8                   # inside JST's 1.5-2.0 panel range, no spot faces
SMP = {3: dict(A=8.2, B=12.5), 4: dict(A=10.7, B=15.0)}   # the 1.5-2.0 panel column
SMP_HA, SMP_HB, KEY_W, KEY_H = 5.15, 4.15, 4.0, 1.6
X_IN1 = PCB_L + 6.5                # SMP bodies stand ~5 in; leads turn down to pads at 66.5
J2_Y = Y_IN1 - 1.0 - SMP[3]['B'] / 2
J3_Y = J2_Y - SMP[3]['B'] / 2 - 1.7 - SMP[4]['B'] / 2
J_Z = 13.5

# --- MT3608 module (Dorhea 36 x 17 x 14 listing size). NOT MEASURED. On the deck ---
MOD_L, MOD_W, MOD_H, MOD_PCB = 36.0, 17.0, 14.0, 1.6
MOD_FIT = 0.6
DECK_Z0, DECK_T = CELL_TOP + 0.3, 2.0
DECK_TOP = DECK_Z0 + DECK_T
DECK_X0 = X_IN0 + 0.15
DECK_LAND = 3.5                    # flat deck at each end for the lid's ribs, clear of the rails
MOD_X0 = DECK_X0 + DECK_LAND
MOD_X1 = MOD_X0 + MOD_L + MOD_FIT
DECK_X1 = MOD_X1 + DECK_LAND
DECK_Y0, DECK_Y1 = Y_IN0 + 0.15, DIV_Y0 - 0.15
RAIL_T, LIP = 1.0, 0.5
PAD_X = (SADDLES_X[0], SADDLES_X[1])   # deck presses the cell right over two saddles
RIB_T = 2.0

# --- straps: 12 mm Velcro over the lid ---
STRAP_W, STRAP_DEEP, STRAP_GAP = 13.5, 1.0, 40.0
NOTCH_W = 12.0

X_OUT0, X_OUT1 = X_IN0 - WALL, X_IN1 + FRONT_WALL
Y_OUT0, Y_OUT1 = Y_IN0 - WALL, Y_IN1 + WALL
R_OUT = R_IN + WALL
STRAPS_X = tuple((X_OUT0 + X_OUT1) / 2 + d for d in (-STRAP_GAP / 2, STRAP_GAP / 2))
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


def rings(outline, profile, n=24):
    """Rounded-rectangle outline offset by each profile d, as fixed-count rings,
    so consecutive rings stay in step for lofting."""
    x0, y0, x1, y1, r = outline
    corners = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    t = np.radians(np.linspace(0, 90, n))
    out = []
    for d, z in profile:
        assert r + d > 0
        ring = []
        for cx, cy, a0 in corners:
            a = np.radians(a0) + t
            ring += list(zip(cx + (r + d) * np.cos(a), cy + (r + d) * np.sin(a), np.full(n, z)))
        out.append(ring)
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
# Snap lid. zt = wall top. Bead and groove faces are 45 degrees, the steepest
# either half prints without support in its print orientation
# ---------------------------------------------------------------------------

def skirt_profile(zt):
    zb = zt - SKIRT_H
    return [(-1.2, zb), (-0.5, zb), (0.0, zb + 0.5),            # lead-in
            (0.45, zb + 0.95), (0.45, zb + 1.05), (0.0, zb + 1.5),  # snap bead
            (0.0, zb + 1.65), (0.25, zb + 1.9),                   # seal band, 0.25 oversize
            (0.25, zt + 0.01), (-1.2, zt + 0.01)]


def groove_profile(zt):
    zb = zt - SKIRT_H                                             # bead clears it by 0.05
    return [(-0.5, zb), (0.0, zb + 0.45), (0.5, zb + 0.95), (0.5, zb + 1.1),
            (0.0, zb + 1.6), (-0.5, zb + 2.1)]                   # lid lifts 0.1 before it catches


def chamfer_profile(zt):
    return [(-0.5, zt - 0.8), (0.0, zt - 0.3), (0.3, zt), (0.3, zt + 1.0), (-0.5, zt + 1.0)]


def face_bead(inner, zt):
    """Bead on the wall top, 0.5-1.5 out from the inner face on every wall."""
    ring = rrect(*inner).buffer(1.5, 64).difference(rrect(*inner).buffer(0.5, 64))
    return prism(ring, zt - 0.01, zt + FACE_BEAD_H)


def lid_notch(x_out0, yc, zt):
    """Fingernail notch under the lid's edge, stopping 0.1 short of the face bead."""
    return box(x_out0 - 1, x_out0 + WALL - 1.6, yc - NOTCH_W / 2, yc + NOTCH_W / 2, zt - 1, zt + 1.0)


# ---------------------------------------------------------------------------
# Wall features, in a wall's own (u, v=Z, w) frame
# ---------------------------------------------------------------------------

def smp_profile(uc, vc, n):
    A, B = SMP[n]['A'], SMP[n]['B']
    return unary_union([
        sbox(uc - B / 2, vc - SMP_HB / 2, uc + B / 2, vc + SMP_HB / 2),
        sbox(uc - A / 2, vc - SMP_HA / 2, uc + A / 2, vc + SMP_HA / 2),
        sbox(uc - KEY_W / 2, vc, uc + KEY_W / 2, vc + SMP_HA / 2 + KEY_H)])


def rocker_cuts(M, uc, vc, wall_t):
    """Round hole, and the wall thinned to SW_PANEL round it from inside. The top
    of the hole prints as a ~7 bridge."""
    return [prism(Point(uc, vc).buffer(SW_HOLE_D / 2, 128), -1, wall_t + 1, M),
            prism(Point(uc, vc).buffer(SW_SPOT_D / 2, 128), -1, wall_t - SW_PANEL, M)]


M_BACK = wall((X_IN0, 0, 0), (0, -1, 0), (-1, 0, 0))    # u = -Y
M_FRONT = wall((X_IN1, 0, 0), (0, 1, 0), (1, 0, 0))     # u = Y


# ---------------------------------------------------------------------------
# Bottom
# ---------------------------------------------------------------------------

def build_bottom():
    outer = rr_solid(OUTER, [(-EDGE_CH, -FLOOR), (0, -FLOOR + EDGE_CH), (0, H_IN)])
    shell = D(outer, [prism(rrect(*INNER), 0, H_IN + 1)])
    cuts = rocker_cuts(M_BACK, -SW_Y, SW_Z, WALL)
    cuts += [prism(smp_profile(J2_Y, J_Z, 3), -1, FRONT_WALL + 1, M_FRONT),
             prism(smp_profile(J3_Y, J_Z, 4), -1, FRONT_WALL + 1, M_FRONT)]
    cuts += [sweep(INNER, groove_profile(H_IN)), sweep(INNER, chamfer_profile(H_IN))]

    inner = [cyl(BOSS_D / 2, (x, y, -0.01), (x, y, STANDOFF)) for x, y in HOLES]
    divider = box(X_IN0 - 0.1, X_IN1 + 0.1, DIV_Y0, DIV_Y1, -0.01, H_IN - 0.4)
    divider = D(divider, [box(4.0, 20.0, DIV_Y0 - 1, DIV_Y1 + 1, DECK_TOP + MOD_PCB + 0.5, H_IN),  # U1 wires
                          box(55.0, 66.0, DIV_Y0 - 1, DIV_Y1 + 1, 21.0, H_IN)])                    # J1 lead
    inner.append(divider)
    for x in SADDLES_X:
        s = sbox(Y_IN0 - 0.1, -0.01, DIV_Y0 + 0.1, CELL_ZC - 2.0).difference(
            Point(CELL_YC, CELL_ZC).buffer(CELL_D / 2 + 0.2, 96))
        inner.append(prism_yz(s, x - SADDLE_T / 2, x + SADDLE_T / 2))
    keep_out = rrect(*INNER).difference(rrect(*INNER).buffer(-1.7))   # the lid's skirt
    inner = D(U(inner), [prism(keep_out, H_IN - SKIRT_H - 0.3, H_IN + 1)])

    body = U([shell, inner, face_bead(INNER, H_IN)])
    pilots = [cyl(PILOT_D / 2, (x, y, STANDOFF - PILOT_DEEP), (x, y, STANDOFF + 1), 32) for x, y in HOLES]
    return D(body, cuts + pilots)


# ---------------------------------------------------------------------------
# Lid: printed upside down, top face on the bed
# ---------------------------------------------------------------------------

def build_lid():
    plate = rr_solid(OUTER, [(0, H_IN), (0, H_IN + LID - EDGE_CH), (-EDGE_CH, H_IN + LID)])
    parts = [plate, sweep(INNER, skirt_profile(H_IN))]
    # ribs that hold the deck down at both ends, 0.2 squeeze
    for x in (DECK_X0 + DECK_LAND / 2, DECK_X1 - DECK_LAND / 2):
        parts.append(box(x - RIB_T / 2, x + RIB_T / 2, DECK_Y0 + 0.4, DECK_Y1 - 0.4, DECK_TOP - 0.2, H_IN + 0.01))
    top = H_IN + LID
    cuts = [box(x - STRAP_W / 2, x + STRAP_W / 2, Y_OUT0 - 1, Y_OUT1 + 1, top - STRAP_DEEP, top + 1)
            for x in STRAPS_X]
    cuts.append(lid_notch(X_OUT0, CELL_YC, H_IN))
    return D(U(parts), cuts)


# ---------------------------------------------------------------------------
# Deck: carries the MT3608 on top of the cell. Printed flat, underside down
# ---------------------------------------------------------------------------

def build_deck():
    plan = sbox(DECK_X0, DECK_Y0, DECK_X1, DECK_Y1).intersection(rrect(*INNER).buffer(-0.15, 32))
    parts = [prism(plan, DECK_Z0, DECK_TOP)]
    # pads under it press the cell 0.2, right over two saddles
    for x in PAD_X:
        p = sbox(DECK_Y0, CELL_ZC + 4.0, DECK_Y1, DECK_Z0 + 0.01).difference(
            Point(CELL_YC, CELL_ZC).buffer(CELL_D / 2 - 0.2, 96))
        parts.append(prism_yz(p, x - 2.0, x + 2.0))
    top = DECK_TOP
    rails = ((DECK_Y0, DECK_Y0 + RAIL_T), (DECK_Y1 - RAIL_T, DECK_Y1))
    for y0, y1 in rails:
        parts.append(box(MOD_X0 - 0.5, MOD_X1 + 0.5, y0, y1, top - 0.01, top + MOD_PCB + 2.6))
    lip_z = top + MOD_PCB + 0.2
    for xa, xb in ((MOD_X0 + 3, MOD_X0 + 11), (MOD_X1 - 11, MOD_X1 - 3)):
        for y_face, s in ((rails[0][1], 1), (rails[1][0], -1)):
            lip = Polygon([(y_face, lip_z - LIP), (y_face, lip_z + 0.8),
                           (y_face + s * LIP, lip_z + 0.8), (y_face + s * LIP, lip_z)])
            parts.append(prism_yz(lip, xa, xb))
    for x0, x1 in ((MOD_X0 - 0.5, MOD_X0), (MOD_X1, MOD_X1 + 0.5)):
        parts.append(box(x0, x1, rails[0][1] + 4, rails[1][0] - 4, top - 0.01, top + 1.2))
    return U(parts)


# ---------------------------------------------------------------------------
# Coupons
# ---------------------------------------------------------------------------

def build_wall_coupon():
    """The back wall round the rocker and the front wall round both plugs, at their
    real heights and in the bottom's print orientation. Stands on a foot."""
    L = 70.0
    Mc = wall((0, 0, 0), (1, 0, 0), (0, -1, 0))      # inner face at Y = 0, outward -Y
    plate = prism(sbox(0, -FLOOR, L, SW_Z + SW_SPOT_D / 2 + 2.0), 0, WALL, Mc)
    foot = box(0, L, 0, 12.0, -FLOOR, 0)
    thin = box(28.0, L, -0.01, WALL - FRONT_WALL, J_Z - 7.0, J_Z + 7.0)   # front wall is 1.8
    cuts = rocker_cuts(Mc, 14.0, SW_Z, WALL) + [thin,
            prism(smp_profile(38.5, J_Z, 3), -1, WALL + 1, Mc),
            prism(smp_profile(57.5, J_Z, 4), -1, WALL + 1, Mc)]
    return D(U([plate, foot]), cuts)


def build_snap_coupon():
    """Small box and lid with the real joint and a strap channel. Snap the lid on
    and off, fill the box with water and turn it over. The lid is laid out beside
    the box, top face down."""
    inner = (0.0, 0.0, 42.0, 34.0, R_IN)
    outer = (-WALL, -WALL, 42.0 + WALL, 34.0 + WALL, R_OUT)
    zt = 12.0
    bx = D(rr_solid(outer, [(-EDGE_CH, -FLOOR), (0, -FLOOR + EDGE_CH), (0, zt)]),
           [prism(rrect(*inner), 0, zt + 1)])
    bx = D(U([bx, face_bead(inner, zt)]), [sweep(inner, groove_profile(zt)),
                                           sweep(inner, chamfer_profile(zt))])
    lid = U([rr_solid(outer, [(0, zt), (0, zt + LID - EDGE_CH), (-EDGE_CH, zt + LID)]),
             sweep(inner, skirt_profile(zt))])
    lid = D(lid, [box(21.0 - STRAP_W / 2, 21.0 + STRAP_W / 2, -10, 50, zt + LID - STRAP_DEEP, zt + 10),
                  lid_notch(-WALL, 17.0, zt)])
    lid.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    lid.apply_translation([0, -lid.bounds[0][1] + 34.0 + WALL + 6.0, -lid.bounds[0][2] - FLOOR])
    return U([bx, lid])


# ---------------------------------------------------------------------------
# Stand-ins for the parts, for the clash check and the preview
# ---------------------------------------------------------------------------

def stand_ins():
    t = PCB_TOP
    seat = X_OUT0                                    # bezel seat, the back wall's outer face
    s = {
        'board': box(0, PCB_L, -PCB_W, 0, STANDOFF, t),
        'XIAO': box(-0.4, 20.85, -22.9, -5.1, t, t + 2.5 + 1.2 + 2.6),
        'USB-C': box(USB_MOUTH_X, 7.0, -14.0 - 4.47, -14.0 + 4.47, XIAO_TOP - 3.2, XIAO_TOP),
        'U2': box(25.9, 43.3, -21.0, -11.0, t, t + 5.3),
        'C2': box(27.0, 32.0, -9.65, -7.15, t, t + 9.0),
        'C3': box(22.15, 24.65, -18.6, -13.6, t, t + 9.0),
        'C1': cyl(5.0, (49.0, -9.0, t), (49.0, -9.0, t + PART_MAX)),
        'Q1': box(45.7, 55.8, -21.0, -16.0, t, t + 20.0),
        'F1': box(24.0, 39.0, -29.0, -24.6, t, t + 18.0),
        'cell': cyl(CELL_D / 2, (CELL_X0, CELL_YC, CELL_ZC), (CELL_X0 + CELL_L, CELL_YC, CELL_ZC)),
        'MT3608': U([box(MOD_X0 + 0.3, MOD_X0 + 0.3 + MOD_L, DECK_Y0 + RAIL_T + 0.35,
                         DECK_Y0 + RAIL_T + 0.35 + MOD_W, DECK_TOP, DECK_TOP + MOD_PCB),
                     box(MOD_X0 + 2, MOD_X0 + 12, CELL_YC - 5, CELL_YC + 5, DECK_TOP + MOD_PCB, DECK_TOP + MOD_H)]),
        'rocker': U([cyl(SW_BODY_D / 2, (X_IN0 - (WALL - SW_PANEL) + 0.01, SW_Y, SW_Z),
                         (seat + SW_BODY_DEEP, SW_Y, SW_Z)),
                     box(seat + SW_BODY_DEEP - 0.01, seat + ROCKER_DEPTH, SW_Y - SW_LUGS[0] / 2,
                         SW_Y + SW_LUGS[0] / 2, SW_Z - SW_LUGS[1] / 2, SW_Z + SW_LUGS[1] / 2)]),
        'bezel': cyl(SW_BEZEL_D / 2, (seat, SW_Y, SW_Z), (seat - 2.0, SW_Y, SW_Z)),
    }
    for name, y, n in (('J2', J2_Y, 3), ('J3', J3_Y, 4)):
        w = SMP[n]['A'] - 0.2
        s[name] = box(X_IN1 - 5.0, X_IN1 - 0.01, y - w / 2, y + w / 2, J_Z - 4.0, J_Z + 4.0)
    return s


def straps():
    out = []
    top = H_IN + LID
    for xc in STRAPS_X:
        x0, x1 = xc - 6.0, xc + 6.0
        out.append(box(x0, x1, Y_OUT0 - 1.1, Y_OUT1 + 1.1, top - STRAP_DEEP + 0.05, top - STRAP_DEEP + 1.15))
        for y0, y1 in ((Y_OUT0 - 1.15, Y_OUT0 - 0.05), (Y_OUT1 + 0.05, Y_OUT1 + 1.15)):
            out.append(box(x0, x1, y0, y1, -FLOOR - 8, top - STRAP_DEEP + 1.15))
    return out


def preview(bottom, lid, deck, wall_c, snap_c, parts, out):
    import pyvista as pv
    pv.OFF_SCREEN = True
    colors = {'board': '#1f8a6e', 'XIAO': '#c0c3c9', 'USB-C': '#e8e8e8', 'U2': '#2a2a2e',
              'C2': '#e0a030', 'C3': '#e0a030', 'C1': '#3b4c9a', 'Q1': '#2a2a2e', 'F1': '#f0c832',
              'cell': '#d9584a', 'MT3608': '#3f72d9', 'rocker': '#202020', 'bezel': '#202020',
              'J2': '#111111', 'J3': '#111111'}
    housing, deck_c, strap_c = '#dfe3ea', '#a9b4c8', '#f08a3c'
    labels = {'board': (55, -25, PCB_TOP), 'cell': (CELL_X0 + 55, CELL_YC, CELL_TOP),
              'MT3608 on deck': (MOD_X0 + 18, CELL_YC, DECK_TOP + MOD_H),
              'rocker': (X_IN0 + 12, SW_Y, SW_Z + 10),
              'J2': (X_IN1, J2_Y, J_Z + 5), 'J3': (X_IN1, J3_Y, J_Z + 5)}
    strap_ms = straps()

    def mesh(p, m, color, opacity=1.0):
        p.add_mesh(pv.wrap(m).compute_normals(feature_angle=35, split_vertices=True),
                   color=color, opacity=opacity, smooth_shading=False)

    pl = pv.Plotter(off_screen=True, shape=(2, 2), window_size=(1800, 1300), border=False)
    c = np.array([(X_OUT0 + X_OUT1) / 2, (Y_OUT0 + Y_OUT1) / 2, 14])
    views = [((0, 0), tuple(c + (-150, -130, 150)), 'closed, from the back: rocker, strap channels', True),
             ((0, 1), tuple(c + (150, 110, 150)), 'lid off, from the front: J2 and J3', False),
             ((1, 0), tuple(c + (0, 0, 260)), 'from above, lid off', False)]
    for (r, k), pos, title, with_lid in views:
        pl.subplot(r, k)
        pl.set_background('white')
        mesh(pl, bottom, housing, 0.55 if r == 1 else 1.0)
        if with_lid:
            mesh(pl, lid, housing)
            mesh(pl, parts['bezel'], colors['bezel'])
            for m in strap_ms:
                mesh(pl, m, strap_c)
        else:
            mesh(pl, deck, deck_c)
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
    lay = [(flip, housing, (0, 0)), (deck.copy(), deck_c, (95, 0)), (wall_c.copy(), housing, (0, -75)),
           (snap_c.copy(), housing, (90, -75))]
    allb = []
    for m, col, (dx, dy) in lay:
        m.apply_translation([dx - m.bounds[0][0], dy - m.bounds[0][1], -m.bounds[0][2]])
        mesh(pl, m, col)
        allb.append(m.bounds)
    pl.add_text('as printed: lid (top down), deck, wall coupon, snap coupon', font_size=10, color='black')
    allb = np.vstack(allb)
    cc = (allb.min(0) + allb.max(0)) / 2
    pl.camera_position = [tuple(cc + np.array([-60, -200, 230])), tuple(cc), (0, 0, 1)]
    pl.reset_camera()
    pl.camera.zoom(1.25)
    pl.enable_anti_aliasing('ssaa')
    pl.screenshot(out)
    pl.close()


if __name__ == '__main__':
    bottom, lid, deck = build_bottom(), build_lid(), build_deck()
    wall_c, snap_c = build_wall_coupon(), build_snap_coupon()
    parts = stand_ins()

    print(f'H_IN {H_IN:.1f}  rocker centre Z {SW_Z:.1f}, over the XIAO by '
          f'{SW_Z - SW_BODY_D / 2 - XIAO_TOP:.1f}  straps at X {STRAPS_X[0]:.1f}, {STRAPS_X[1]:.1f}')
    print('clash check (stand-in volume inside the housing or the deck, mm^3):')
    closed = U([bottom, lid, deck])
    for k, m in parts.items():
        if k == 'bezel':
            continue
        v = max(I(m, closed).volume, 0.0)
        print(f'  {k:7s} {v:8.2f}' + ('   <- deck pads squeeze the cell 0.2, by design' if k == 'cell' else ''))
    print(f'  deck vs bottom {max(I(deck, bottom).volume, 0):.2f}   deck vs lid {max(I(deck, lid).volume, 0):.2f}'
          '   <- lid ribs squeeze the deck 0.2, by design')
    print(f'  lid vs bottom {I(lid, bottom).volume:.1f}   <- skirt 0.25 oversize + face bead, by design')

    out = {'bottom': bottom, 'lid': lid, 'deck': deck, 'wall-coupon': wall_c, 'snap-coupon': snap_c}
    for name, m in out.items():
        m = m.copy()
        if name == 'lid':                         # print orientation: top face down
            m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
        m.apply_translation([0, 0, -m.bounds[0][2]])
        m.export(f'versions/pod-housing-v3-{name}.stl')
        e = np.round(m.extents, 1)
        print(f'{name:12s} {e[0]} x {e[1]} x {e[2]}  volume {m.volume / 1000:.1f} cm^3  '
              f'watertight={m.is_watertight}  bodies={len(m.split(only_watertight=False))}')
    print(f'outer box {X_OUT1 - X_OUT0:.1f} x {Y_OUT1 - Y_OUT0:.1f} x {H_IN + FLOOR + LID:.1f}')
    preview(bottom, lid, deck, wall_c, snap_c, parts, 'versions/pod-housing-v3-preview.png')

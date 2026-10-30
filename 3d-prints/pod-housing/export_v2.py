# v2: v1 with nothing on the outside but the rocker, the USB port, the plug
# cutouts and the strap loops. The lid snaps on with no screws, the rocker moves
# into the lid, and the MT3608 rides on a deck over the XIAO, so the box is 12
# shorter than v1.
# Run from this folder:
#   uv run --with trimesh --with manifold3d --with shapely --with scipy --with pyvista python export_v2.py
#   ->  versions/archive/pod-housing-v2-{bottom,lid,deck,usb-plug,wall-coupon,snap-coupon}.stl + -preview.png
#
# Frame as v1: the PCB's own coordinates with y flipped, so the board is X 0..70,
# Y -30..0. Z up, floor top at Z = 0.
#
#   row A  board on four standoffs, XIAO USB-C through the -X end wall. The MT3608
#          lies on a TPU deck that snaps onto ledges over the XIAO and U2
#   row B  the cell in its own compartment beside the board
#   end    past the board: the rocker hangs from the lid, with J2 (SM-3) and
#          J3 (SM-4) in the end wall on either side of it
#
# Seals, all in the TPU itself:
#   lid    skirt 0.25 oversize inside the walls, a snap bead that drops into a
#          groove in the walls, and a bead on the wall top that the snap keeps
#          squashed. No screws, so no holes
#   plugs  JST's own panel cutout for the SMP housing, as v1
#   rocker hole 0.2 under the 20 mm cutout. The TPU grips the body all round, and
#          the bezel sits on the lid's flat top
#   USB-C  bore in a thickened end wall, flush outside. The printed plug pushes in
import numpy as np, trimesh
from shapely.geometry import Point, Polygon, LineString, box as sbox
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

WALL, FLOOR, LID = 2.4, 2.4, 2.4

# --- board (docs/pcb/pod_pcb.py, README) ---
PCB_L, PCB_W, PCB_T = 70.0, 30.0, 1.6
HOLES = [(2.5, -2.5), (67.5, -2.5), (2.5, -27.5), (67.5, -27.5)]
STANDOFF = 3.5
BOSS_D = 4.6
PILOT_D, PILOT_DEEP = 1.6, 4.5   # M2x6 self-tapping
PART_MAX = 22.0                  # C1 is 17-22, Q1 ~20, F1 ~18
PCB_TOP = STANDOFF + PCB_T

# --- KCD1 round rocker, in the lid ---
ROCKER_DEPTH = 30.0      # bezel seat to the end of the spade lugs (darknetdoll, about 30)
WIRE_TURN = 4.0          # the lug wires come out downward and need room to turn
SW_HOLE_D = 19.8         # 20.0 cutout less 0.2 so the TPU grips the body
SW_BODY_R = 10.5         # body and snap clips, with clearance
SW_BEZEL_D = 23.0
SW_PANEL = 2.0
SW_SPOT_D = 23.0

# Floor to lid underside: the rocker sets it, not the board (that would be 28.0)
H_IN = max(PCB_TOP + PART_MAX + 0.9, ROCKER_DEPTH + WIRE_TURN - LID)   # 31.6

# --- inner outline ---
X_IN0, Y_IN1, R_IN = -0.7, 0.6, 1.6
DIV_Y1, DIV_T = -30.6, 1.6
DIV_Y0 = DIV_Y1 - DIV_T

# --- cell: protected 18650, lead out of one end (darknetdoll: 18.5 x 69) ---
CELL_D, CELL_L = 18.5, 69.0
CELL_BAY = CELL_D + 1.2
Y_IN0 = DIV_Y0 - CELL_BAY          # -51.9
CELL_YC = DIV_Y0 - CELL_BAY / 2
CELL_LIFT = 1.0
CELL_ZC = CELL_LIFT + CELL_D / 2
CELL_X0 = 0.5
LEAD_ROOM = 4.5                    # lead comes out of the +X end and turns back over the cell
BAY_X1, CROSS_T = CELL_X0 + CELL_L + LEAD_ROOM, 1.6
SADDLES_X = (5.0, 35.0, 65.0)
SADDLE_T = 2.0

# --- rocker position: past the board and the cell compartment's corner ---
SW_X, SW_Y = 82.5, -23.0
SW_TOP = H_IN + LID
X_IN1 = SW_X + SW_SPOT_D / 2 + 1.2 + 0.3     # spot face stays clear of the lid's skirt

# --- MT3608 module (Dorhea 36 x 17 x 14 listing size). NOT MEASURED ---
MOD_L, MOD_W, MOD_H, MOD_PCB = 36.0, 17.0, 14.0, 1.6
MOD_FIT = 0.6
DECK_Z0, DECK_T = 14.6, 2.0        # over the XIAO (~11.4) and the 0.1 uF discs (~14)
DECK_TOP = DECK_Z0 + DECK_T
DECK_X1, DECK_Y_F1 = 38.5, -21.0   # main deck stops short of F1 (Y -24.6, 18 tall)
DECK_EXT_X1 = 22.5                 # out to the divider where F1 isn't
MOD_X0, MOD_Y1 = 1.2, -1.3         # rail clears the deck lip, module clears the lid's skirt
MOD_X1 = MOD_X0 + MOD_L + MOD_FIT
MOD_Y0 = MOD_Y1 - (MOD_W + MOD_FIT)
RAIL_T, LIP = 1.2, 0.5
LEDGE_W, DECK_LIP = 1.8, 0.6
U1_SLOT = (5.5, 18.0, -28.5, -25.0)   # U1's wire pads sit at X 6.5-17, Y -26.8

# --- JST SM plug housing (SMP-0xV-BC) panel cutout, eSM.pdf, panel 1.0-1.5 ---
SMP = {3: dict(A=8.2, B=12.3), 4: dict(A=10.7, B=14.8)}
SMP_HA, SMP_HB, KEY_W, KEY_H = 5.15, 4.15, 4.0, 1.6
SMP_PANEL, SMP_SPOT_H = 1.5, 11.0
J2_Y = Y_IN1 - (SMP[3]['B'] / 2 + 1 + 0.3)
J3_Y = Y_IN0 + (SMP[4]['B'] / 2 + 1 + 0.3)
J_Z = 13.5

# --- XIAO USB-C ---
USB_Y = -14.0
USB_ABOVE_PCB = 2.5 + 1.2 + 1.6     # header spacer, XIAO PCB, half the socket. NOT MEASURED
USB_Z = PCB_TOP + USB_ABOVE_PCB
USB_MOUTH_X = -1.5
USB_WEB = X_IN0 - (USB_MOUTH_X - 0.1)
USB_HOLE = (9.8, 4.6)
USB_BORE = (13.0, 7.4)
END_WALL = WALL + 3.0               # deep enough for the plug to grip, flush outside
PLUG_FIT = 0.15

# --- lid snap and seals ---
SKIRT_H = 5.0
FACE_BEAD_W, FACE_BEAD_H = 1.0, 0.3
RIBS_X, RIB_T = (20.0, 50.0), 2.0
NOTCH_W = 12.0

# --- strap loops: 12 mm Velcro, doubled back ---
LOOP_W, LOOP_T, LOOP_BAR, LOOP_POST, LOOP_H = 14.0, 3.0, 2.6, 3.0, 5.0

X_OUT0, X_OUT1 = X_IN0 - END_WALL, X_IN1 + WALL
Y_OUT0, Y_OUT1 = Y_IN0 - WALL, Y_IN1 + WALL
R_OUT = R_IN + WALL
LOOPS_X = tuple((X_OUT0 + X_OUT1) / 2 + d for d in (-30.0, 30.0))
INNER = (X_IN0, Y_IN0, X_IN1, Y_IN1, R_IN)

U = lambda meshes: trimesh.boolean.union(meshes, engine='manifold')
D = lambda a, bs: trimesh.boolean.difference([a] + list(bs), engine='manifold')
I = lambda a, b: trimesh.boolean.intersection([a, b], engine='manifold')


def rrect(x0, y0, x1, y1, r):
    return sbox(x0, y0, x1, y1).buffer(-r, 32).buffer(r, 32)


def stadium(uc, vc, w, h):
    return LineString([(uc - (w - h) / 2, vc), (uc + (w - h) / 2, vc)]).buffer(h / 2, 32)


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


def sweep(outline, profile, n=24):
    """Solid swept round a rounded-rectangle outline (x0, y0, x1, y1, r). The
    profile is a closed list of (d, z): d is the outward offset from the outline.
    Each ring is the exact offset curve, so rings stay in step and the loft is
    watertight."""
    x0, y0, x1, y1, r = outline
    corners = [(x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)]
    t = np.radians(np.linspace(0, 90, n))
    K = 4 * n
    V = []
    for d, z in profile:
        assert r + d > 0
        for cx, cy, a0 in corners:
            a = np.radians(a0) + t
            V += list(zip(cx + (r + d) * np.cos(a), cy + (r + d) * np.sin(a), np.full(n, z)))
    F = []
    M = len(profile)
    for i in range(M):
        j = (i + 1) % M
        for k in range(K):
            k2 = (k + 1) % K
            a, b, c, e = i * K + k, i * K + k2, j * K + k2, j * K + k
            F += [(a, b, c), (a, c, e)]
    m = trimesh.Trimesh(np.array(V), np.array(F))
    if m.volume < 0:
        m.invert()
    assert m.is_watertight
    return m


# ---------------------------------------------------------------------------
# Snap lid. zt = wall top. Bead and groove faces are 45 degrees, the steepest
# either half prints without support in its print orientation
# ---------------------------------------------------------------------------

def skirt_profile(zt):
    zb = zt - SKIRT_H
    return [(-1.2, zb), (-0.6, zb), (0.0, zb + 0.6),          # lead-in
            (0.5, zb + 1.1), (0.5, zb + 1.4), (0.0, zb + 1.9),  # snap bead
            (0.0, zb + 2.4), (0.25, zb + 2.65),                 # seal band, 0.25 oversize
            (0.25, zt + 0.01), (-1.2, zt + 0.01)]


def groove_profile(zt):
    zb = zt - SKIRT_H                                           # bead clears it by 0.05
    return [(-0.5, zb), (0.0, zb + 0.5), (0.55, zb + 1.05), (0.55, zb + 1.45),
            (0.0, zb + 2.0), (-0.5, zb + 2.5)]                 # lid lifts 0.1 before it catches


def chamfer_profile(zt):
    return [(-0.5, zt - 0.9), (0.0, zt - 0.4), (0.4, zt), (0.4, zt + 1.0), (-0.5, zt + 1.0)]


def face_bead(outer, zt):
    mid = outer.buffer(-WALL / 2, 64)
    return prism(mid.buffer(FACE_BEAD_W / 2, 64).difference(mid.buffer(-FACE_BEAD_W / 2, 64)),
                 zt - 0.01, zt + FACE_BEAD_H)


def lid_notch(x_out0, yc, zt):
    """Fingernail notch under the lid's edge. Stops 0.1 short of the face bead."""
    return box(x_out0 - 1, x_out0 + WALL / 2 - FACE_BEAD_W / 2 - 0.1, yc - NOTCH_W / 2,
               yc + NOTCH_W / 2, zt - 1, zt + 1.0)


# ---------------------------------------------------------------------------
# Wall features, in a wall's own (u, v=Z, w) frame. Each returns (adds, cuts).
# ---------------------------------------------------------------------------

def smp_profile(uc, vc, n):
    A, B = SMP[n]['A'], SMP[n]['B']
    return unary_union([
        sbox(uc - B / 2, vc - SMP_HB / 2, uc + B / 2, vc + SMP_HB / 2),
        sbox(uc - A / 2, vc - SMP_HA / 2, uc + A / 2, vc + SMP_HA / 2),
        sbox(uc - KEY_W / 2, vc, uc + KEY_W / 2, vc + SMP_HA / 2 + KEY_H)])


def smp_features(M, uc, vc, n):
    B = SMP[n]['B']
    spot = sbox(uc - B / 2 - 1, vc - SMP_SPOT_H / 2, uc + B / 2 + 1, vc + SMP_SPOT_H / 2)
    return [], [prism(smp_profile(uc, vc, n), -1, WALL + 1, M),
                prism(spot, -1, WALL - SMP_PANEL, M)]


def usb_features(M, uc, vc, wall_t, floor_v=None):
    """Port through a wall_t-thick wall. On a thinner wall (the coupon), a block
    on the outside makes up END_WALL."""
    hole = sbox(uc - USB_HOLE[0] / 2, vc - USB_HOLE[1] / 2,
                uc + USB_HOLE[0] / 2, vc + USB_HOLE[1] / 2).buffer(-0.8).buffer(0.8, 16)
    adds = []
    if wall_t < END_WALL:
        block = sbox(uc - USB_BORE[0] / 2 - 2.2, floor_v, uc + USB_BORE[0] / 2 + 2.2,
                     vc + USB_BORE[1] / 2 + 2.2)
        adds.append(prism(block, wall_t - 0.01, END_WALL, M))
    cuts = [prism(hole, -1, END_WALL + 1, M),
            prism(stadium(uc, vc, *USB_BORE), USB_WEB, END_WALL + 1, M)]
    return adds, cuts


def rocker_cuts(xc, yc, ztop):
    """Through-hole in a lid whose outer face is at ztop, thinned to SW_PANEL inside."""
    return [cyl(SW_HOLE_D / 2, (xc, yc, ztop - LID - 1), (xc, yc, ztop + 1), 128),
            cyl(SW_SPOT_D / 2, (xc, yc, ztop - LID - 1), (xc, yc, ztop - SW_PANEL), 128)]


# ---------------------------------------------------------------------------
# Bottom
# ---------------------------------------------------------------------------

def outline_out():
    return rrect(X_OUT0, Y_OUT0, X_OUT1, Y_OUT1, R_OUT)


def outline_in():
    return rrect(*INNER)


M_POS_X = wall((X_IN1, 0, 0), (0, 1, 0), (1, 0, 0))      # u = Y
M_NEG_X = wall((X_IN0, 0, 0), (0, -1, 0), (-1, 0, 0))    # u = -Y


def strap_loops():
    """Belt loops at the bottom of both long sides. The strap comes up from round
    the arm, through the slot and back down over the bar."""
    out = []
    L = LOOP_W + 2 * LOOP_POST
    for s, y_face in ((-1, Y_OUT0), (1, Y_OUT1)):
        y_in, y_out = y_face - s * 1.0, y_face + s * (LOOP_T + LOOP_BAR)
        for xc in LOOPS_X:
            plan = unary_union([rrect(xc - L / 2, min(y_in, y_out), xc + L / 2, max(y_in, y_out), 2.0),
                                sbox(xc - L / 2, min(y_in, y_face + s * 2.5), xc + L / 2,
                                     max(y_in, y_face + s * 2.5))])
            z1 = -FLOOR + LOOP_H
            side = Polygon([(y_in, -FLOOR), (y_out, -FLOOR), (y_out, z1 - 1.5),
                            (y_out - s * 1.5, z1), (y_in, z1)])
            lug = I(prism(plan, -FLOOR, z1), prism_yz(side, xc - L / 2 - 1, xc + L / 2 + 1))
            slot = rrect(xc - LOOP_W / 2, min(y_face, y_face + s * LOOP_T), xc + LOOP_W / 2,
                         max(y_face, y_face + s * LOOP_T), 0.8)
            out.append(D(lug, [prism(slot, -FLOOR - 1, z1 + 1)]))
    return out


def ledge_frame(origin, along, into):
    """Frame with local x = -into (so negative x points into the room), local y = Z,
    local z = along the wall, from origin."""
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = -np.array(into, float), (0, 0, 1), along, origin
    if np.linalg.det(M[:3, :3]) < 0:
        M[:3, 0] = -M[:3, 0]
        return M, -1
    return M, 1


def ledges():
    out = []
    for origin, along, into, u0, u1 in [
            ((0, Y_IN1, 0), (1, 0, 0), (0, -1, 0), 5.0, DECK_X1 - 0.5),     # +Y wall
            ((0, DIV_Y1, 0), (1, 0, 0), (0, 1, 0), 5.0, DECK_EXT_X1 - 0.5),  # divider
            ((X_IN0, 0, 0), (0, -1, 0), (1, 0, 0), 5.0, 25.0)]:             # -X wall, Y -5..-25
        M, sgn = ledge_frame(origin, along, into)
        prof = [(0.1, DECK_Z0 - LEDGE_W), (-LEDGE_W, DECK_Z0), (0.1, DECK_Z0)]
        z = DECK_TOP + 0.1
        lip = [(0.1, z), (-DECK_LIP, z + DECK_LIP), (0.1, z + 2 * DECK_LIP)]
        for p in (prof, lip):
            out.append(prism(Polygon([(sgn * w, v) for w, v in p]), u0, u1, M))
    return out


def build_bottom():
    shell = D(prism(outline_out(), -FLOOR, H_IN), [prism(outline_in(), 0, H_IN + 1)])
    adds = [face_bead(outline_out(), H_IN)] + strap_loops()
    feats = [smp_features(M_POS_X, J2_Y, J_Z, 3), smp_features(M_POS_X, J3_Y, J_Z, 4),
             usb_features(M_NEG_X, -USB_Y, USB_Z, END_WALL)]
    adds += [a for f in feats for a in f[0]]
    cuts = [c for f in feats for c in f[1]]
    cuts += [sweep(INNER, groove_profile(H_IN)), sweep(INNER, chamfer_profile(H_IN))]

    inner = [cyl(BOSS_D / 2, (x, y, -0.01), (x, y, STANDOFF)) for x, y in HOLES]
    wall_top = H_IN - 0.4
    divider = box(X_IN0 - 0.1, BAY_X1 + CROSS_T, DIV_Y0, DIV_Y1, -0.01, wall_top)
    divider = D(divider, [box(55.0, 66.0, DIV_Y0 - 1, DIV_Y1 + 1, 21.0, H_IN)])   # J1 lead
    cross = box(BAY_X1, BAY_X1 + CROSS_T, Y_IN0 - 0.1, DIV_Y0 + 0.1, -0.01, wall_top)
    inner += [divider, cross]
    for x in SADDLES_X:
        s = sbox(Y_IN0 - 0.1, -0.01, DIV_Y0 + 0.1, CELL_ZC - 2.0).difference(
            Point(CELL_YC, CELL_ZC).buffer(CELL_D / 2 + 0.2, 96))
        inner.append(prism_yz(s, x - SADDLE_T / 2, x + SADDLE_T / 2))
    inner += ledges()
    keep_out = outline_in().difference(outline_in().buffer(-1.7))   # the lid's skirt
    inner = D(U(inner), [prism(keep_out, H_IN - SKIRT_H - 0.3, H_IN + 1)])

    body = U([shell, inner] + adds)
    pilots = [cyl(PILOT_D / 2, (x, y, STANDOFF - PILOT_DEEP), (x, y, STANDOFF + 1), 32) for x, y in HOLES]
    return D(body, cuts + pilots)


# ---------------------------------------------------------------------------
# Lid: printed upside down, top face on the bed
# ---------------------------------------------------------------------------

def build_lid():
    parts = [prism(outline_out(), H_IN, H_IN + LID), sweep(INNER, skirt_profile(H_IN))]
    # ribs that press the cell onto its saddles (0.2 squeeze)
    for x in RIBS_X:
        r = sbox(Y_IN0 + 1.6, CELL_ZC + 5.0, DIV_Y0 - 1.6, H_IN + 0.01).difference(
            Point(CELL_YC, CELL_ZC).buffer(CELL_D / 2 - 0.2, 96))
        parts.append(prism_yz(r, x - RIB_T / 2, x + RIB_T / 2))
    return D(U(parts), rocker_cuts(SW_X, SW_Y, SW_TOP) +
             [lid_notch(X_OUT0, (Y_OUT0 + Y_OUT1) / 2, H_IN)])


# ---------------------------------------------------------------------------
# Deck: carries the MT3608 over the XIAO. Printed flat, underside on the bed
# ---------------------------------------------------------------------------

def build_deck():
    g = 0.15                               # gap to the walls
    plan = unary_union([sbox(X_IN0 + g, DECK_Y_F1, DECK_X1, Y_IN1 - g),
                        sbox(X_IN0 + g, DIV_Y1 + g, DECK_EXT_X1, DECK_Y_F1 + 0.1)])
    plan = plan.intersection(outline_in().buffer(-g, 32))       # walls' inside corners are R1.6
    plan = plan.difference(sbox(U1_SLOT[0], U1_SLOT[2], U1_SLOT[1], U1_SLOT[3]).buffer(0.5))
    parts = [prism(plan, DECK_Z0, DECK_TOP)]
    top = DECK_TOP
    for y0, y1 in ((MOD_Y0 - RAIL_T, MOD_Y0), (MOD_Y1, MOD_Y1 + RAIL_T)):
        parts.append(box(MOD_X0 - 0.5, MOD_X1 + 0.5, y0, y1, top - 0.01, top + MOD_PCB + 2.6))
    lip_z = top + MOD_PCB + 0.2
    for xa, xb in ((MOD_X0 + 3, MOD_X0 + 11), (MOD_X1 - 11, MOD_X1 - 3)):
        for y_face, s in ((MOD_Y0, 1), (MOD_Y1, -1)):
            lip = Polygon([(y_face, lip_z - LIP), (y_face, lip_z + 0.8),
                           (y_face + s * LIP, lip_z + 0.8), (y_face + s * LIP, lip_z)])
            parts.append(prism_yz(lip, xa, xb))
    for x0, x1 in ((MOD_X0 - 0.5, MOD_X0), (MOD_X1, MOD_X1 + 0.5)):
        parts.append(box(x0, x1, MOD_Y0 + 4, MOD_Y1 - 4, top - 0.01, top + 1.2))
    return U(parts)


def build_usb_plug():
    """Pushes into the USB bore. Printed cap-down."""
    depth = END_WALL - USB_WEB - 0.2
    insert = prism(stadium(0, 0, USB_BORE[0] + 2 * PLUG_FIT, USB_BORE[1] + 2 * PLUG_FIT), 1.2, 1.2 + depth)
    insert = D(insert, [prism(stadium(0, 0, USB_BORE[0] - 3.2, USB_BORE[1] - 3.2), 2.4, 1.2 + depth + 1)])
    cap = prism(unary_union([stadium(0, 0, USB_BORE[0] + 4.4, USB_BORE[1] + 4.4),
                             sbox(0, -3.0, USB_BORE[0] / 2 + 9.0, 3.0).buffer(1.0)]), 0, 1.2)
    cap = D(cap, [cyl(1.25, (USB_BORE[0] / 2 + 7.0, 0, -1), (USB_BORE[0] / 2 + 7.0, 0, 3), 32)])
    return U([cap, insert])


# ---------------------------------------------------------------------------
# Coupons
# ---------------------------------------------------------------------------

def build_wall_coupon():
    """A stretch of wall with both plug cutouts and the USB port, at their real
    heights and in the bottom's print orientation. Stands on a foot."""
    L = 75.0
    Mc = wall((0, 0, 0), (1, 0, 0), (0, -1, 0))     # inner face at Y = 0, outward -Y
    plate = prism(sbox(0, -FLOOR, L, 22.0), 0, WALL, Mc)
    foot = box(0, L, 0, 12.0, -FLOOR, 0)
    feats = [smp_features(Mc, 12.0, J_Z, 3), smp_features(Mc, 31.0, J_Z, 4),
             usb_features(Mc, 56.0, USB_Z, WALL, -FLOOR)]
    body = U([plate, foot] + [a for f in feats for a in f[0]])
    return D(body, [c for f in feats for c in f[1]])


def build_snap_coupon():
    """Small box and lid with the real snap, seals and rocker hole. Snap the lid
    on and off, fill the box with water and turn it over, fit the rocker. The lid
    is laid out beside the box, top face down."""
    inner = (0.0, 0.0, 42.0, 34.0, R_IN)
    zt = 12.0
    o_out = rrect(-WALL, -WALL, 42.0 + WALL, 34.0 + WALL, R_OUT)
    bx = D(prism(o_out, -FLOOR, zt), [prism(rrect(*inner), 0, zt + 1)])
    bx = D(U([bx, face_bead(o_out, zt)]), [sweep(inner, groove_profile(zt)),
                                           sweep(inner, chamfer_profile(zt))])
    lid = U([prism(o_out, zt, zt + LID), sweep(inner, skirt_profile(zt))])
    lid = D(lid, rocker_cuts(21.0, 17.0, zt + LID) + [lid_notch(-WALL, 17.0, zt)])
    lid.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    lid.apply_translation([0, -lid.bounds[0][1] + 34.0 + WALL + 6.0, -lid.bounds[0][2] - FLOOR])
    return U([bx, lid])


# ---------------------------------------------------------------------------
# Stand-ins for the parts, for the clash check and the preview
# ---------------------------------------------------------------------------

def stand_ins():
    t = PCB_TOP
    s = {
        'board': box(0, PCB_L, -PCB_W, 0, STANDOFF, t),
        'XIAO': box(-0.4, 20.85, -22.9, -5.1, t, t + 2.5 + 1.2 + 2.6),
        'USB-C': box(USB_MOUTH_X, 7.0, USB_Y - 4.47, USB_Y + 4.47, USB_Z - 1.6, USB_Z + 1.6),
        'U2': box(25.9, 43.3, -21.0, -11.0, t, t + 5.3),
        'C2': box(27.0, 32.0, -9.65, -7.15, t, t + 9.0),
        'C3': box(22.15, 24.65, -18.6, -13.6, t, t + 9.0),
        'C1': cyl(5.0, (49.0, -9.0, t), (49.0, -9.0, t + PART_MAX)),
        'Q1': box(45.7, 55.8, -21.0, -16.0, t, t + 20.0),
        'F1': box(24.0, 39.0, -29.0, -24.6, t, t + 18.0),
        'cell': cyl(CELL_D / 2, (CELL_X0, CELL_YC, CELL_ZC), (CELL_X0 + CELL_L, CELL_YC, CELL_ZC)),
        'MT3608': U([box(MOD_X0 + 0.3, MOD_X0 + 0.3 + MOD_L, MOD_Y1 - 0.3 - MOD_W, MOD_Y1 - 0.3,
                         DECK_TOP, DECK_TOP + MOD_PCB),
                     box(MOD_X0 + 2, MOD_X0 + 12, MOD_Y1 - 13, MOD_Y1 - 3, DECK_TOP + MOD_PCB, DECK_TOP + MOD_H)]),
        'rocker': cyl(SW_BODY_R - 0.5, (SW_X, SW_Y, SW_TOP - ROCKER_DEPTH),
                      (SW_X, SW_Y, SW_TOP - SW_PANEL - 0.01)),
        'bezel': cyl(SW_BEZEL_D / 2, (SW_X, SW_Y, SW_TOP), (SW_X, SW_Y, SW_TOP + 2.0)),
    }
    for name, y, n in (('J2', J2_Y, 3), ('J3', J3_Y, 4)):
        w = SMP[n]['A'] - 0.2
        s[name] = box(X_IN1 + WALL - SMP_PANEL - 5.0, X_IN1 + WALL - SMP_PANEL - 0.01,
                      y - w / 2, y + w / 2, J_Z - 4.0, J_Z + 4.0)
    return s


def straps():
    out = []
    for s, y_face in ((-1, Y_OUT0), (1, Y_OUT1)):
        for xc in LOOPS_X:
            y0 = y_face + s * 0.3
            out.append(box(xc - 6, xc + 6, min(y0, y0 + s * 1.1), max(y0, y0 + s * 1.1), -14, 0.5))
            y1 = y_face + s * (LOOP_T + LOOP_BAR + 0.2)
            out.append(box(xc - 6, xc + 6, min(y1, y1 + s * 1.1), max(y1, y1 + s * 1.1), -10, 0.5))
            out.append(box(xc - 6, xc + 6, min(y0, y1 + s * 1.1), max(y0, y1 + s * 1.1), 0.5, 1.6))
    return out


def preview(bottom, lid, deck, plug, wall_c, snap_c, parts, out):
    import pyvista as pv
    pv.OFF_SCREEN = True
    colors = {'board': '#1f8a6e', 'XIAO': '#c0c3c9', 'USB-C': '#e8e8e8', 'U2': '#2a2a2e',
              'C2': '#e0a030', 'C3': '#e0a030', 'C1': '#3b4c9a', 'Q1': '#2a2a2e', 'F1': '#f0c832',
              'cell': '#d9584a', 'MT3608': '#3f72d9', 'rocker': '#202020', 'bezel': '#202020',
              'J2': '#111111', 'J3': '#111111'}
    housing, deck_c, strap_c = '#dfe3ea', '#a9b4c8', '#f08a3c'
    labels = {'board': (55, -25, PCB_TOP), 'cell': (CELL_X0 + 35, CELL_YC, CELL_ZC + CELL_D / 2),
              'MT3608 on deck': (MOD_X0 + 18, MOD_Y1 - 9, DECK_TOP + MOD_H),
              'rocker (in lid)': (SW_X, SW_Y, SW_TOP),
              'J2': (X_IN1, J2_Y, J_Z + 5), 'J3': (X_IN1, J3_Y, J_Z + 5), 'USB-C': (X_IN0, USB_Y, USB_Z + 4)}
    strap_ms = straps()

    def mesh(p, m, color, opacity=1.0):
        p.add_mesh(pv.wrap(m).compute_normals(feature_angle=35, split_vertices=True),
                   color=color, opacity=opacity, smooth_shading=False)

    pl = pv.Plotter(off_screen=True, shape=(2, 2), window_size=(1800, 1300), border=False)
    c = np.array([(X_OUT0 + X_OUT1) / 2, (Y_OUT0 + Y_OUT1) / 2, 12])
    closed = lid.copy()
    views = [((0, 0), tuple(c + (-110, -170, 150)), 'closed: smooth lid, rocker on top, strap loops at the base', True),
             ((0, 1), tuple(c + (150, 120, 170)), 'lid off, from the plug end', False),
             ((1, 0), tuple(c + (0, 0, 260)), 'from above, lid off', False)]
    for (r, k), pos, title, with_lid in views:
        pl.subplot(r, k)
        pl.set_background('white')
        mesh(pl, bottom, housing, 0.55 if r == 1 else 1.0)
        for m in strap_ms:
            mesh(pl, m, strap_c)
        if with_lid:
            mesh(pl, closed, housing)
            mesh(pl, parts['bezel'], colors['bezel'])
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
        pl.camera.zoom(1.3 if r == 1 else 1.1)
    pl.subplot(1, 1)
    pl.set_background('white')
    flip = lid.copy()
    flip.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    flip.apply_translation([0, 0, -flip.bounds[0][2]])
    lay = [(flip, housing, (0, 0)), (deck.copy(), deck_c, (0, -80)), (wall_c.copy(), housing, (55, -80)),
           (snap_c.copy(), housing, (140, -40)), (plug.copy(), '#f0a050', (110, 10))]
    allb = []
    for m, col, (dx, dy) in lay:
        m.apply_translation([dx - m.bounds[0][0], dy - m.bounds[0][1], -m.bounds[0][2]])
        mesh(pl, m, col)
        allb.append(m.bounds)
    pl.add_text('as printed: lid (top down), deck, wall coupon, snap coupon, USB plug', font_size=10, color='black')
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
    plug, wall_c, snap_c = build_usb_plug(), build_wall_coupon(), build_snap_coupon()
    parts = stand_ins()

    print(f'H_IN {H_IN:.1f}  rocker bottom {SW_TOP - ROCKER_DEPTH:.1f} above the floor  '
          f'strap loops at X {LOOPS_X[0]:.1f}, {LOOPS_X[1]:.1f}')
    print('clash check (stand-in volume inside the housing or the deck, mm^3):')
    closed = U([bottom, lid, deck])
    for k, m in parts.items():
        if k == 'bezel':
            continue
        v = I(m, closed).volume if I(m, closed).volume > 0 else 0.0
        print(f'  {k:7s} {v:8.2f}' + ('   <- lid ribs squeeze the cell 0.2, by design' if k == 'cell' else ''))
    print(f'  deck vs bottom + lid {I(deck, U([bottom, lid])).volume:.2f}')
    print(f'  lid vs bottom {I(lid, bottom).volume:.1f}   <- skirt 0.25 oversize + face bead, by design')

    out = {'bottom': bottom, 'lid': lid, 'deck': deck, 'usb-plug': plug,
           'wall-coupon': wall_c, 'snap-coupon': snap_c}
    for name, m in out.items():
        m = m.copy()
        if name == 'lid':                         # print orientation: top face down
            m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
        m.apply_translation([0, 0, -m.bounds[0][2]])
        m.export(f'versions/archive/pod-housing-v2-{name}.stl')
        e = np.round(m.extents, 1)
        print(f'{name:12s} {e[0]} x {e[1]} x {e[2]}  volume {m.volume / 1000:.1f} cm^3  '
              f'watertight={m.is_watertight}  bodies={len(m.split(only_watertight=False))}')
    print(f'outer box {X_OUT1 - X_OUT0:.1f} x {Y_OUT1 - Y_OUT0:.1f} x {H_IN + FLOOR + LID:.1f}')
    preview(bottom, lid, deck, plug, wall_c, snap_c, parts, 'versions/archive/pod-housing-v2-preview.png')

# v1: sealed TPU housing for the pod. Board, cell, boost module, rocker and the two
# arm plugs all go inside one box with a screwed lid.
# Run from this folder:
#   uv run --with trimesh --with manifold3d --with shapely --with scipy --with pyvista python export_v1.py
#   ->  versions/pod-housing-v1-{bottom,lid,usb-plug,wall-coupon}.stl + -preview.png
#
# Frame: the PCB's own coordinates from docs/pcb/pod_pcb.py with y flipped, so the
# board is X 0..70, Y -30..0 (model Y = -pcb y). Z up, floor top at Z = 0.
#
#   row A  board on four standoffs, XIAO USB-C through the -X wall
#   row B  the cell in its own compartment beside the board (-Y side)
#   end    past the board's +X end: MT3608 in a pocket, the KCD1 rocker through the
#          -Y wall, J2 (SM-3) and J3 (SM-4) snapped into the +X wall
#
# Seals, all in the TPU itself:
#   lid    skirt with 0.25 radial interference inside the walls, plus a bead on
#          the wall top that the lid squashes. Four M3 screws in corner ears,
#          outside the seal, so no screw hole opens into the box
#   plugs  JST's own panel cutout for the SMP housing (a 1.5 panel). The housing's
#          flange pulls tight on the inside face
#   rocker bead ring under the bezel. The snap clips pull the bezel onto it
#   USB-C  collar around the port. A printed plug pushes into it
import numpy as np, trimesh
from shapely.geometry import Point, Polygon, LineString, box as sbox
from shapely.geometry.polygon import orient
from shapely.ops import unary_union

WALL, FLOOR, LID = 2.4, 2.4, 2.4

# --- board (docs/pcb/pod_pcb.py, README) ---
PCB_L, PCB_W, PCB_T = 70.0, 30.0, 1.6
HOLES = [(2.5, -2.5), (67.5, -2.5), (2.5, -27.5), (67.5, -27.5)]
STANDOFF = 3.5           # under-board room for clipped leads and wire-pad tails
BOSS_D = 4.6             # copper keep-out is 2.4 radius round each hole
PILOT_D, PILOT_DEEP = 1.6, 4.5   # M2x6 self-tapping: 4.4 of thread in the boss
PART_MAX = 22.0          # tallest part above the PCB: C1 is 17-22, Q1 ~20, F1 ~18
PCB_TOP = STANDOFF + PCB_T
H_IN = PCB_TOP + PART_MAX + 0.9   # 28.0, floor top to lid underside

# --- inner outline ---
X_IN0 = -0.7             # board edge to wall; the XIAO's own board overhangs 0.4
Y_IN1 = 0.6
R_IN = 1.6               # board corners are R1, so the inner corner stays tight
DIV_Y1, DIV_T = -30.6, 1.6
DIV_Y0 = DIV_Y1 - DIV_T

# --- cell: protected 18650 on the kit's PH2.0 pigtail. NOT MEASURED ---
CELL_D, CELL_L = 18.8, 70.0
CELL_BAY = CELL_D + 1.2
Y_IN0 = DIV_Y0 - CELL_BAY          # -52.2
CELL_YC = DIV_Y0 - CELL_BAY / 2
CELL_LIFT = 1.0                    # cell rides on the saddles, clear of the floor
CELL_ZC = CELL_LIFT + CELL_D / 2
CELL_X0 = 2.0
BAY_X1, CROSS_T = 74.0, 1.6        # cell compartment ends here: room for the pigtail
SADDLES_X = (6.0, 37.0, 68.0)
SADDLE_T = 2.0

# --- MT3608 module (Dorhea 36 x 17 x 14 listing size). NOT MEASURED ---
MOD_L, MOD_W, MOD_H, MOD_PCB = 36.0, 17.0, 14.0, 1.6
MOD_FIT = 0.6
MOD_X0 = 71.6
MOD_X1 = MOD_X0 + MOD_L + MOD_FIT
MOD_Y1 = Y_IN1
MOD_Y0 = MOD_Y1 - (MOD_W + MOD_FIT)
RAIL_T = 1.4
X_IN1 = MOD_X1 + 2.3               # wire bend at the module's far end
LIP = 0.5

# --- KCD1 round rocker, 20 mm snap-in. Depth NOT MEASURED ---
SW_HOLE_D = 19.8         # 20.0 cutout less 0.2 so the TPU grips the body
SW_BEZEL_D = 23.0
SW_BODY_D, SW_DEPTH = 20.0, 33.0   # body + terminals + boxed spade lugs
SW_X, SW_Z = 87.0, 13.0
SW_PANEL = 2.0
SW_BEAD_R, SW_BEAD_W, SW_BEAD_H = 10.9, 0.8, 0.4

# --- JST SM plug housing (SMP-0xV-BC) panel cutout, eSM.pdf, panel 1.0-1.5 ---
SMP = {3: dict(A=8.2, B=12.3), 4: dict(A=10.7, B=14.8)}
SMP_HA, SMP_HB, KEY_W, KEY_H = 5.15, 4.15, 4.0, 1.6
SMP_PANEL = 1.5
SMP_SPOT_H = 11.0
J2_Y, J3_Y, J_Z = -25.5, -43.0, 13.5

# --- XIAO USB-C ---
USB_Y = -14.0                                   # XIAO body centre, pcb y 14.0
USB_ABOVE_PCB = 2.5 + 1.2 + 1.6                 # header spacer, XIAO PCB, half the socket. NOT MEASURED
USB_Z = PCB_TOP + USB_ABOVE_PCB
USB_MOUTH_X = -1.5                              # socket stands 1.5 proud of the board
USB_WEB = X_IN0 - (USB_MOUTH_X - 0.1)           # 0.9 of wall round the socket, stops 0.1 short of its mouth
USB_HOLE = (9.8, 4.6)
USB_BORE = (13.0, 7.4)                          # cable overmold
USB_COLLAR = 3.0
PLUG_FIT = 0.15

# --- lid ---
SKIRT_H, SKIRT_T, SKIRT_FIT = 4.0, 1.4, 0.25
BEAD_W, BEAD_H = 1.0, 0.4
EAR_OFF, EAR_R = 3.6, 3.8
EAR_PILOT_D, EAR_PILOT_DEEP, EAR_CLEAR_D = 2.6, 14.0, 3.4   # M3x16 self-tapping
RIBS_X, RIB_T = (22.0, 52.0), 2.0

X_OUT0, X_OUT1 = X_IN0 - WALL, X_IN1 + WALL
Y_OUT0, Y_OUT1 = Y_IN0 - WALL, Y_IN1 + WALL
EARS = [(X_IN0 - EAR_OFF, Y_IN1 + EAR_OFF), (X_IN1 + EAR_OFF, Y_IN1 + EAR_OFF),
        (X_IN0 - EAR_OFF, Y_IN0 - EAR_OFF), (X_IN1 + EAR_OFF, Y_IN0 - EAR_OFF)]

U = lambda meshes: trimesh.boolean.union(meshes, engine='manifold')
D = lambda a, bs: trimesh.boolean.difference([a] + list(bs), engine='manifold')
I = lambda a, b: trimesh.boolean.intersection([a, b], engine='manifold')


def rrect(x0, y0, x1, y1, r):
    return sbox(x0, y0, x1, y1).buffer(-r, 32).buffer(r, 32)


def stadium(uc, vc, w, h):
    return LineString([(uc - (w - h) / 2, vc), (uc + (w - h) / 2, vc)]).buffer(h / 2, 32)


def prism(poly, z0, z1, M=None):
    """Extrude a shapely (multi)polygon from z0 to z1, then place it with M."""
    polys = getattr(poly, 'geoms', [poly])
    m = U([trimesh.creation.extrude_polygon(orient(p, 1.0), z1 - z0) for p in polys]) \
        if len(polys) > 1 else trimesh.creation.extrude_polygon(orient(polys[0], 1.0), z1 - z0)
    m.apply_translation([0, 0, z0])
    if M is not None:
        m.apply_transform(M)
    return m


def wall(origin, u, n):
    """Frame for a wall: local x along u, local y = global Z, local z = outward
    normal n, from the wall's inner face (w = 0) to its outer face (w = WALL)."""
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


# ---------------------------------------------------------------------------
# Wall features, in a wall's own (u, v=Z, w) frame. Each returns (adds, cuts).
# ---------------------------------------------------------------------------

def switch_features(M, uc, vc):
    # Plain round: a teardrop tip would cut the bead ring and open a leak under
    # the bezel. The top of the hole prints as a ~7 mm bridge
    hole = Point(uc, vc).buffer(SW_HOLE_D / 2, 128)
    cuts = [prism(hole, -1, WALL + 1, M),
            prism(Point(uc, vc).buffer(13.5, 96), -1, WALL - SW_PANEL, M)]
    ring = Point(uc, vc).buffer(SW_BEAD_R + SW_BEAD_W / 2, 128).difference(
        Point(uc, vc).buffer(SW_BEAD_R - SW_BEAD_W / 2, 128))
    adds = [prism(ring, WALL - 0.01, WALL + SW_BEAD_H, M)]
    return adds, cuts


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


def usb_features(M, uc, vc, floor_v):
    hole = sbox(uc - USB_HOLE[0] / 2, vc - USB_HOLE[1] / 2,
                uc + USB_HOLE[0] / 2, vc + USB_HOLE[1] / 2).buffer(-0.8).buffer(0.8, 16)
    bore = stadium(uc, vc, *USB_BORE)
    block = sbox(uc - USB_BORE[0] / 2 - 2.2, floor_v, uc + USB_BORE[0] / 2 + 2.2,
                 vc + USB_BORE[1] / 2 + 2.2)
    adds = [prism(block, WALL - 0.01, WALL + USB_COLLAR, M)]
    cuts = [prism(hole, -1, WALL + 1, M), prism(bore, USB_WEB, WALL + USB_COLLAR + 1, M)]
    return adds, cuts


# ---------------------------------------------------------------------------
# Bottom
# ---------------------------------------------------------------------------

def outline_out():
    return unary_union([rrect(X_OUT0, Y_OUT0, X_OUT1, Y_OUT1, R_IN + WALL)] +
                       [Point(c).buffer(EAR_R, 64) for c in EARS])


def outline_in():
    return rrect(X_IN0, Y_IN0, X_IN1, Y_IN1, R_IN)


M_NEG_Y = wall((0, Y_IN0, 0), (1, 0, 0), (0, -1, 0))     # u = X
M_POS_X = wall((X_IN1, 0, 0), (0, 1, 0), (1, 0, 0))      # u = Y
M_NEG_X = wall((X_IN0, 0, 0), (0, -1, 0), (-1, 0, 0))    # u = -Y


def wall_features():
    feats = [switch_features(M_NEG_Y, SW_X, SW_Z),
             smp_features(M_POS_X, J2_Y, J_Z, 3),
             smp_features(M_POS_X, J3_Y, J_Z, 4),
             usb_features(M_NEG_X, -USB_Y, USB_Z, -FLOOR)]
    return [a for f in feats for a in f[0]], [c for f in feats for c in f[1]]


def skirt_keepout(z0):
    """Where the lid's skirt goes: internal walls are cut back out of it."""
    band = outline_in().difference(outline_in().buffer(-(SKIRT_T + 0.5)))
    return prism(band, z0, H_IN + 1)


def build_bottom():
    shell = D(prism(outline_out(), -FLOOR, H_IN), [prism(outline_in(), 0, H_IN + 1)])
    mid = rrect(X_OUT0, Y_OUT0, X_OUT1, Y_OUT1, R_IN + WALL).buffer(-WALL / 2, 64)
    bead = prism(mid.buffer(BEAD_W / 2, 64).difference(mid.buffer(-BEAD_W / 2, 64)),
                 H_IN - 0.01, H_IN + BEAD_H)
    adds, cuts = wall_features()

    inner = []
    for x, y in HOLES:
        inner.append(cyl(BOSS_D / 2, (x, y, -0.01), (x, y, STANDOFF)))
    # divider and cross wall close the cell compartment
    wall_top = H_IN - 0.4
    divider = box(X_IN0 - 0.1, BAY_X1 + CROSS_T, DIV_Y0, DIV_Y1, -0.01, wall_top)
    divider = D(divider, [box(55.0, 66.0, DIV_Y0 - 1, DIV_Y1 + 1, 21.0, H_IN)])   # J1 lead
    cross = box(BAY_X1, BAY_X1 + CROSS_T, Y_IN0 - 0.1, DIV_Y0 + 0.1, -0.01, wall_top)
    inner += [divider, cross]
    # cell saddles
    for x in SADDLES_X:
        s = sbox(Y_IN0 - 0.1, -0.01, DIV_Y0 + 0.1, CELL_ZC - 2.0).difference(
            Point(CELL_YC, CELL_ZC).buffer(CELL_D / 2 + 0.2, 96))
        inner.append(prism_yz(s, x - SADDLE_T / 2, x + SADDLE_T / 2))
    # module pocket: rail on the -Y side, the outer wall on the +Y side, snap lips
    inner.append(box(MOD_X0 - 0.5, MOD_X1 + 0.5, MOD_Y0 - RAIL_T, MOD_Y0, -0.01, MOD_PCB + 2.6))
    lip_z = MOD_PCB + 0.2
    for xa, xb in ((MOD_X0 + 3, MOD_X0 + 11), (MOD_X1 - 11, MOD_X1 - 3)):
        for y_face, s in ((MOD_Y0, 1), (MOD_Y1, -1)):
            # lip with a 45 degree underside, so it prints off the rail
            lip = Polygon([(y_face, lip_z - LIP), (y_face, lip_z + 0.8),
                           (y_face + s * LIP, lip_z + 0.8), (y_face + s * LIP, lip_z)])
            inner.append(prism_yz(lip, xa, xb))
    for x0, x1 in ((MOD_X0 - 1.2, MOD_X0), (MOD_X1, MOD_X1 + 1.2)):
        inner.append(box(x0, x1, MOD_Y0 + 4, MOD_Y1 - 4, -0.01, 1.2))
    inner = D(U(inner), [skirt_keepout(H_IN - SKIRT_H - 0.3)])

    body = U([shell, bead, inner] + adds)
    pilots = [cyl(PILOT_D / 2, (x, y, STANDOFF - PILOT_DEEP), (x, y, STANDOFF + 1), 32) for x, y in HOLES]
    ear_pilots = [cyl(EAR_PILOT_D / 2, (x, y, H_IN - EAR_PILOT_DEEP), (x, y, H_IN + 1), 32) for x, y in EARS]
    return D(body, cuts + pilots + ear_pilots)


# ---------------------------------------------------------------------------
# Lid: printed upside down, top face on the bed
# ---------------------------------------------------------------------------

def build_lid():
    plate = prism(outline_out(), H_IN, H_IN + LID)
    parts = [plate]
    # skirt, with a stepped lead-in at its tip
    steps = [(H_IN - SKIRT_H, H_IN - SKIRT_H + 0.6, -0.35),
             (H_IN - SKIRT_H + 0.6, H_IN - SKIRT_H + 1.2, -0.05),
             (H_IN - SKIRT_H + 1.2, H_IN + 0.01, SKIRT_FIT)]
    for z0, z1, off in steps:
        ring = outline_in().buffer(off, 64).difference(outline_in().buffer(SKIRT_FIT - SKIRT_T, 64))
        parts.append(prism(ring, z0, z1))
    # ribs that press the cell onto its saddles (0.2 squeeze)
    for x in RIBS_X:
        r = sbox(Y_IN0 + 1.6, CELL_ZC + 5.0, DIV_Y0 - 1.6, H_IN + 0.01).difference(
            Point(CELL_YC, CELL_ZC).buffer(CELL_D / 2 - 0.2, 96))
        parts.append(prism_yz(r, x - RIB_T / 2, x + RIB_T / 2))
    lid = U(parts)
    holes = [cyl(EAR_CLEAR_D / 2, (x, y, H_IN - 1), (x, y, H_IN + LID + 1), 32) for x, y in EARS]
    return D(lid, holes)


def build_usb_plug():
    """Pushes into the USB collar. Printed cap-down."""
    depth = WALL + USB_COLLAR - USB_WEB - 0.2       # stops 0.2 short of the bore floor
    insert = prism(stadium(0, 0, USB_BORE[0] + 2 * PLUG_FIT, USB_BORE[1] + 2 * PLUG_FIT), 1.2, 1.2 + depth)
    insert = D(insert, [prism(stadium(0, 0, USB_BORE[0] - 3.2, USB_BORE[1] - 3.2), 2.4, 1.2 + depth + 1)])
    cap = prism(unary_union([stadium(0, 0, USB_BORE[0] + 4.4, USB_BORE[1] + 4.4),
                             sbox(0, -3.0, USB_BORE[0] / 2 + 9.0, 3.0).buffer(1.0)]), 0, 1.2)
    cap = D(cap, [cyl(1.25, (USB_BORE[0] / 2 + 7.0, 0, -1), (USB_BORE[0] / 2 + 7.0, 0, 3), 32)])
    return U([cap, insert])


def build_coupon():
    """One stretch of wall with every opening in it, at the same heights and the
    same print orientation as the bottom. Stands on a foot."""
    L = 100.0
    Mc = wall((0, 0, 0), (1, 0, 0), (0, -1, 0))     # inner face at Y = 0, outward -Y
    plate = prism(sbox(0, -FLOOR, L, 26.0), 0, WALL, Mc)
    foot = box(0, L, 0, 12.0, -FLOOR, 0)
    feats = [switch_features(Mc, 16.0, SW_Z),
             smp_features(Mc, 40.0, J_Z, 3),
             smp_features(Mc, 59.0, J_Z, 4),
             usb_features(Mc, 84.0, USB_Z, -FLOOR)]
    body = U([plate, foot] + [a for f in feats for a in f[0]])
    return D(body, [c for f in feats for c in f[1]])


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
        'C1': cyl(5.0, (49.0, -9.0, t), (49.0, -9.0, t + 22.0)),
        'Q1': box(45.7, 55.8, -21.0, -16.0, t, t + 20.0),
        'F1': box(24.0, 39.0, -29.0, -24.6, t, t + 18.0),
        'cell': cyl(CELL_D / 2, (CELL_X0, CELL_YC, CELL_ZC), (CELL_X0 + CELL_L, CELL_YC, CELL_ZC)),
        'MT3608': U([box(MOD_X0 + 0.3, MOD_X0 + 0.3 + MOD_L, MOD_Y1 - 0.3 - MOD_W, MOD_Y1 - 0.3, 0, MOD_PCB),
                     box(MOD_X0 + 2, MOD_X0 + 12, MOD_Y1 - 13, MOD_Y1 - 3, MOD_PCB, MOD_H)]),
        'rocker': cyl(SW_BODY_D / 2, (SW_X, Y_IN0 + WALL - SW_PANEL - 0.01 + 0.4, SW_Z),
                      (SW_X, Y_IN0 + SW_DEPTH, SW_Z)),
        'bezel': cyl(SW_BEZEL_D / 2, (SW_X, Y_OUT0 - SW_BEAD_H, SW_Z), (SW_X, Y_OUT0 - SW_BEAD_H - 2.0, SW_Z)),
    }
    for name, y, n in (('J2', J2_Y, 3), ('J3', J3_Y, 4)):
        w = SMP[n]['A'] - 0.2
        s[name] = box(X_IN1 + WALL - SMP_PANEL - 5.0, X_IN1 + WALL - SMP_PANEL - 0.01,
                      y - w / 2, y + w / 2, J_Z - 4.0, J_Z + 4.0)
    return s


def preview(bottom, lid, plug, coupon, parts, out):
    import pyvista as pv
    pv.OFF_SCREEN = True
    colors = {'board': '#1f8a6e', 'XIAO': '#c0c3c9', 'USB-C': '#e8e8e8', 'U2': '#2a2a2e',
              'C1': '#3b4c9a', 'Q1': '#2a2a2e', 'F1': '#f0c832', 'cell': '#d9584a',
              'MT3608': '#3f72d9', 'rocker': '#202020', 'bezel': '#202020', 'J2': '#111111', 'J3': '#111111'}
    housing = '#dfe3ea'
    labels = {'board': (35, -15, PCB_TOP), 'cell': (CELL_X0 + 35, CELL_YC, CELL_ZC + CELL_D / 2),
              'MT3608': (MOD_X0 + 18, MOD_Y1 - 9, MOD_H), 'rocker': (SW_X, Y_IN0 + 20, SW_Z + 10),
              'J2': (X_IN1, J2_Y, J_Z + 5), 'J3': (X_IN1, J3_Y, J_Z + 5), 'USB-C': (X_IN0, USB_Y, USB_Z + 4)}

    def mesh(p, m, color, opacity=1.0):
        p.add_mesh(pv.wrap(m).compute_normals(feature_angle=35, split_vertices=True),
                   color=color, opacity=opacity, smooth_shading=False)

    pl = pv.Plotter(off_screen=True, shape=(2, 2), window_size=(1800, 1300), border=False)
    c = np.array([(X_OUT0 + X_OUT1) / 2, (Y_OUT0 + Y_OUT1) / 2, 10])
    views = [((0, 0), tuple(c + (-120, -170, 170)), 'bottom with the parts in, from the USB end and the rocker side'),
             ((0, 1), tuple(c + (170, 110, 190)), 'from the plug end'),
             ((1, 0), tuple(c + (0, 0, 260)), 'from above, housing see-through')]
    for (r, k), pos, title in views:
        pl.subplot(r, k)
        pl.set_background('white')
        mesh(pl, bottom, housing, 0.55 if r == 1 else 1.0)
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
    co = coupon.copy(); co.apply_translation([0, -85, -co.bounds[0][2]])
    pg = plug.copy(); pg.apply_translation([20, -110, -pg.bounds[0][2]])
    for m, col in ((flip, housing), (co, housing), (pg, '#f0a050')):
        mesh(pl, m, col)
    pl.add_text('as printed: lid (top face down), wall coupon, USB plug', font_size=10, color='black')
    allb = np.vstack([flip.bounds, co.bounds, pg.bounds])
    cc = (allb.min(0) + allb.max(0)) / 2
    pl.camera_position = [tuple(cc + np.array([-90, -230, 200])), tuple(cc), (0, 0, 1)]
    pl.reset_camera()
    pl.camera.zoom(1.2)
    pl.enable_anti_aliasing('ssaa')
    pl.screenshot(out)
    pl.close()


if __name__ == '__main__':
    bottom, lid = build_bottom(), build_lid()
    plug, coupon = build_usb_plug(), build_coupon()
    parts = stand_ins()

    print('clash check (stand-in volume inside the housing, mm^3):')
    closed = U([bottom, lid])
    for k, m in parts.items():
        if k == 'bezel':
            continue
        v = I(m, closed).volume
        print(f'  {k:7s} {v:8.2f}' + ('   <- lid ribs squeeze the cell 0.2, by design' if k == 'cell' else ''))

    out = {'bottom': bottom, 'lid': lid, 'usb-plug': plug, 'wall-coupon': coupon}
    for name, m in out.items():
        if name == 'lid':                         # print orientation: top face down
            m = m.copy()
            m.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
        m = m.copy(); m.apply_translation([0, 0, -m.bounds[0][2]])
        m.export(f'versions/pod-housing-v1-{name}.stl')
        e = np.round(m.extents, 1)
        print(f'{name:12s} {e[0]} x {e[1]} x {e[2]}  volume {m.volume / 1000:.1f} cm^3  '
              f'watertight={m.is_watertight}  bodies={len(m.split(only_watertight=False))}')
    preview(bottom, lid, plug, coupon, parts, 'versions/pod-housing-v1-preview.png')

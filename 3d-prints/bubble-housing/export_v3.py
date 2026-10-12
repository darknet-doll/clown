# v3 fit-test prints: the feed-nipple fixes from the 2026-10-08 fit test.
# Run from this folder: python3 export_v3.py  ->  versions/bubble-housing-v3-*.stl
#
#   base     v2 base with the C-clip bore at 37.6 (coupon 1 held the ring best;
#            the gun's 37.8 is an injection-molded fit, printed bores run looser)
#   shroud   v1 shroud + feed-nipple groove: 6.5 wide at top center, from the
#            mouth back 12. Spec depth is 3.2 radial, which is deeper than the
#            2.4 wall, so it comes out as a through-slot — that is intended, it
#            doubles as the feed-line exit
#
# Nipple (gun-groove envelope, bubble-housing.md Ground Truth): ~6 wide, ~3
# proud of the ring OD, from ~1.3 behind the ring face running ~20 back. With
# the head flush at the shroud back wall the nipple reaches ~9 into the shroud;
# 12 gives margin. Clock the head nipple-up: the clip's 110 deg opening and
# this groove are both top center.
# Slot coupon and clip coupons are unchanged: print the v2 / v1 files.
import sys
import numpy as np, trimesh
from trimesh.creation import box, annulus
sys.path.insert(0, 'concepts')
import model as M
from model import at, hand_top, T, axis_z, R_IN, R_OUT, X0, X1, cyl_x

# helpers copied from export_v1.py (importing it would re-export the v1 files)
def union(parts):
    return trimesh.boolean.union(parts, engine='manifold')

def on_bed(m):
    m = m.copy(); m.apply_translation([-m.bounds[0][0] - (m.extents[0] / 2), -m.bounds[0][1] - (m.extents[1] / 2), -m.bounds[0][2]])
    return m

def c_clip(bore, width=8.0, wall=2.4, gap_deg=110):
    ring = annulus(r_min=bore / 2, r_max=bore / 2 + wall, height=width, sections=192)
    half = np.radians(gap_deg / 2)
    r = bore + 10
    wedge = trimesh.creation.extrude_polygon(
        trimesh.path.polygons.Polygon([(0, 0), (r * np.sin(-half), r * np.cos(half)),
                                      (r * np.sin(half), r * np.cos(half))]), width + 2)
    wedge.apply_translation([0, 0, -width / 2 - 1])
    return ring.difference(wedge)

def report(name, m):
    e = np.round(m.extents, 1)
    print(f'{name:8s} watertight={m.is_watertight}  size {e[0]} x {e[1]} x {e[2]} mm  volume {m.volume / 1000:.1f} cm3')

STRAP_W, STRAP_T = 11.0, 1.1
SLOT_LEN = STRAP_W + 2.0          # 13
SLOT_W = 2.5
BAR = 3.0
LOOP_LEN = SLOT_LEN + 2 * BAR     # 19: end bars sit outside the opening

CLIP_BORE = 37.6                  # <- fit test 2026-10-08, coupon 1
GROOVE_W = 6.5
GROOVE_LEN = 12.0                 # from the mouth (X1) back

OUT = 'versions/bubble-housing-v3-{}.stl'

def loop(cx, y_edge, side, z0):
    return M.belt_loop(cx - LOOP_LEN / 2, cx + LOOP_LEN / 2, y_edge, side, z0, slot=SLOT_W, bar=BAR)

# --- base: v2 base, clip bore 37.6 ----------------------------------------------
parts = [M.curved_plate(10, 72, 24, T, ny=60), M.curved_plate(-26, 10, 14, T, ny=40)]
for s in (1, -1):
    parts += loop(58, 24 * s, s, hand_top(24))      # knuckle loops, same centre as v1
    parts += loop(-11, 14 * s, s, hand_top(14))     # wrist loops, same centre as v1
clip = c_clip(CLIP_BORE)
clip.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
clip.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
parts += [at(clip, 62, 0, axis_z), at(box([8, 22, 4.5]), 62, 0, T + 2.0)]
parts += [at(box([20, 4, 4.5]), 36, s * 9, T + 2.0) for s in (1, -1)]
base = on_bed(union(parts))
base.export(OUT.format('base')); report('base', base)

# --- shroud: v1 shroud + feed-nipple groove at the mouth -------------------------
outer = cyl_x(R_OUT, X0, X1).union(at(box([X1 - X0, 32, axis_z - 1.0]), (X0 + X1) / 2, 0, 1.0 + (axis_z - 1.0) / 2))
inner = cyl_x(R_IN, X0 + 2.4, X1 + 1).union(at(box([X1 - X0, 26, axis_z]), (X0 + X1) / 2 + 1.7, 0, T + axis_z / 2))
shroud = outer.difference(inner)
for x in (24, 30, 36, 42, 48):
    shroud = shroud.difference(at(box([2.4, 18, 14]), x, 0, axis_z + R_IN))
shroud = shroud.difference(at(box([8, 10, 9]), X0 + 1, 0, T + 4.5))
# feed-nipple groove: through-slot, top center, mouth back GROOVE_LEN. The cut
# floor sits 0.9 below R_IN so the slot stays full width where the bore surface
# curves up at y = +-GROOVE_W/2 (sqrt(R_IN^2 - 3.25^2) = R_IN - 0.28)
shroud = shroud.difference(at(box([GROOVE_LEN + 2, GROOVE_W, 8]),
                              X1 - GROOVE_LEN / 2 + 1, 0, axis_z + R_IN - 0.9 + 4))

# verify the groove before export: rays straight down at the mouth region
probe = trimesh.ray.ray_triangle.RayMeshIntersector(shroud)
def first_hit_z(x, y):
    loc, _, _ = probe.intersects_location([[x, y, axis_z + 50]], [[0, 0, -1]])
    return max(loc[:, 2]) - axis_z if len(loc) else None
checks = [
    ('groove open at top center (x 52, y 0)', first_hit_z(52, 0), lambda z: z is None or z < R_IN),
    ('wall intact beside groove (x 52, y 5)', first_hit_z(52, 5),
     lambda z: z is not None and z > np.sqrt(R_OUT ** 2 - 25) - 0.1),   # outer surface curves: top at y=5 is sqrt(R_OUT^2-5^2)
    ('wall intact behind groove (x 44.5, y 0)', first_hit_z(44.5, 0), lambda z: z is not None and z > R_OUT - 0.1),
]
ok = True
for label, z, test in checks:
    good = test(z)
    ok &= good
    print(f'  {"PASS" if good else "FAIL"}  {label}: first hit {"none" if z is None else f"{z:.2f} above axis"}')
if not ok:
    sys.exit('groove verification failed, not exporting the shroud')

shroud.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 1, 0]))  # back wall down
shroud = on_bed(shroud)
shroud.export(OUT.format('shroud')); report('shroud', shroud)

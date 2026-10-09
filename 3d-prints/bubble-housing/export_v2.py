# v2 fit-test prints: v1 base with belt loops resized for the real Velcro.
# Run from this folder: python3 export_v2.py  ->  versions/bubble-housing-v2-*.stl
#
#   base         v1 base, belt loops now 13 x 2.5 openings (was 27 x 3)
#   slot-coupon  13 x 2.0, 13 x 2.5, 13 x 3.0, left to right
#
# Velcro measured 2026-10-08: 11 wide, 1.1 thick.
#   opening length 13 = 11 + 2 clearance
#   opening width 2.5 = room for the strap doubled back through the loop (2 x 1.1)
# Shroud and clip coupons are unchanged: print the v1 files.
import sys
import numpy as np, trimesh
from trimesh.creation import box, annulus
sys.path.insert(0, 'concepts')
import model as M
from model import at, hand_top, T, axis_z

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

OUT = 'versions/bubble-housing-v2-{}.stl'

def loop(cx, y_edge, side, z0):
    return M.belt_loop(cx - LOOP_LEN / 2, cx + LOOP_LEN / 2, y_edge, side, z0, slot=SLOT_W, bar=BAR)

# --- base: same as v1 except the loops ------------------------------------------
parts = [M.curved_plate(10, 72, 24, T, ny=60), M.curved_plate(-26, 10, 14, T, ny=40)]
for s in (1, -1):
    parts += loop(58, 24 * s, s, hand_top(24))      # knuckle loops, same centre as v1
    parts += loop(-11, 14 * s, s, hand_top(14))     # wrist loops, same centre as v1
clip = c_clip(37.8)
clip.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
clip.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
parts += [at(clip, 62, 0, axis_z), at(box([8, 22, 4.5]), 62, 0, T + 2.0)]
parts += [at(box([20, 4, 4.5]), 36, s * 9, T + 2.0) for s in (1, -1)]
base = on_bed(union(parts))
base.export(OUT.format('base')); report('base', base)

# --- slot coupon ------------------------------------------------------------------
strip = box([80, 30, T]); strip.apply_translation([0, 0, T / 2])
for x, w in zip((-22, 0, 22), (2.0, 2.5, 3.0)):
    strip = strip.difference(at(box([w, SLOT_LEN, T + 2]), x, 0, T / 2))
strip = on_bed(strip)
strip.export(OUT.format('slot-coupon')); report('slots', strip)

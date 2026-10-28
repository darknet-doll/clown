# v2 fit-test ring: v1 without the lip, plus a split on the back of the finger.
# Run from this folder:
#   uv run --with trimesh --with manifold3d --with shapely python export_v2.py
#   ->  versions/archive/finger-trigger-ring-v2-c65.stl
#
#   lip      removed: the final switch may not be this one, so nothing is sized
#            to its body except the two pilots
#   split    1.0 gap through the band at 12:00 on the back of the finger, so the
#            band can open or squeeze to suit other hands
#   sizes    65 only for now; the production hands aren't available to measure
#
# Switch, layout and axes are as in export_v1.py.
import numpy as np, trimesh
from shapely.geometry import Point, box as sbox
from shapely.ops import unary_union

SW_W, SW_H, SW_T = 20.0, 15.6, 6.4
HOLE_X = 9.5 / 2
HOLE_FROM_LEVER = 7.2
FIT = 0.2
BAND_WALL = 2.0
BAND_LEN = 7.0
SADDLE_MIN = 3.5
SADDLE_W = SW_W + 1.0
SPLIT = 1.0               # gap on the back of the finger (-y)
PILOT_D, PILOT_FLOOR = 1.7, 0.8

def build(circ):
    r_in = circ / np.pi / 2 + FIT / 2
    r_out = r_in + BAND_WALL
    top = r_in + SADDLE_MIN
    sad_len = SW_H + 0.3
    sec = unary_union([Point(0, 0).buffer(r_out, 128), sbox(-SADDLE_W / 2, top - 2, SADDLE_W / 2, top)]).convex_hull
    sec = sec.intersection(sbox(-50, r_in * 0.35, 50, 50)).difference(Point(0, 0).buffer(r_in, 128))
    saddle = trimesh.creation.extrude_polygon(sec, sad_len)
    band = trimesh.creation.annulus(r_min=r_in, r_max=r_out, height=BAND_LEN, sections=160)
    band.apply_translation([0, 0, BAND_LEN / 2])
    ring = trimesh.boolean.union([saddle, band], engine='manifold')
    cut = trimesh.creation.box([SPLIT, BAND_WALL + 2, BAND_LEN + 2])
    cut.apply_translation([0, -(r_in + BAND_WALL / 2), BAND_LEN / 2])
    ring = trimesh.boolean.difference([ring, cut], engine='manifold')
    for sx in (-1, 1):
        x = sx * HOLE_X
        floor_y = np.sqrt(r_in ** 2 - x ** 2) + PILOT_FLOOR
        depth = top - floor_y
        p = trimesh.creation.cylinder(radius=PILOT_D / 2, height=depth + 1, sections=48)
        p.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
        p.apply_translation([x, floor_y + (depth + 1) / 2, HOLE_FROM_LEVER])
        ring = trimesh.boolean.difference([ring, p], engine='manifold')
    return ring, dict(r_in=r_in, top=top, pilot=depth)

if __name__ == '__main__':
    for c in (65,):
        m, info = build(c)
        m.export(f'versions/archive/finger-trigger-ring-v2-c{c}.stl')
        e = np.round(m.extents, 1)
        print(f'c{c}: bore {2 * info["r_in"]:.2f}  plate top {info["top"]:.2f} off axis  '
              f'pilot depth {info["pilot"]:.1f}  watertight={m.is_watertight}  bodies={len(m.split(only_watertight=False))}  '
              f'size {e[0]} x {e[1]} x {e[2]}')

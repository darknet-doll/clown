# v1 fit-test rings: lever microswitch on the palm side of the middle finger base.
# Run from this folder:
#   uv run --with trimesh --with manifold3d --with shapely python export_v1.py
#   ->  versions/finger-trigger-ring-v1-c50.stl, versions/finger-trigger-ring-v1-c65.stl
#
# Switch (Amazon listing drawing, 71BXJrdZ7tL): body 20 x 15.6 x 6.4, lever on one
# 20 mm edge, sweeps 8 above it. Holes 2.3, 9.5 apart. The drawing doesn't give the
# hole height; measured off its pixels (25.6 px/mm): centres 7.2 below the lever
# edge, 8.4 above the bottom edge, ~5.1 in from each end.
#
# Layout: the switch lies flat on a saddle on the palm side, broad face down, lever
# edge toward the palm. Curling the finger at the knuckle folds the palm onto the
# lever. Screws go down through the switch into blind 1.7 pilots (self-tap M2).
# M2x10 gives ~3.6 of thread; M2x8 only ~1.6.
#
# Axes: z = finger axis (z=0 is the knuckle end, which prints on the bed),
# +y = palm side, x = across the finger.
import numpy as np, trimesh
from shapely.geometry import Point, box as sbox
from shapely.ops import unary_union

SW_W, SW_H, SW_T = 20.0, 15.6, 6.4
HOLE_X = 9.5 / 2
HOLE_FROM_LEVER = 7.2
FIT = 0.2                 # added to the finger diameter
BAND_WALL = 2.0
BAND_LEN = 7.0            # band along the finger, at the knuckle end
SADDLE_MIN = 3.5          # saddle thickness at the palm centre line
SADDLE_W = SW_W + 1.0
LIP_T, LIP_H = 1.5, 3.0   # stop behind the switch's bottom edge: takes the lever push
PILOT_D, PILOT_FLOOR = 1.7, 0.8

def build(circ):
    r_in = circ / np.pi / 2 + FIT / 2
    r_out = r_in + BAND_WALL
    top = r_in + SADDLE_MIN
    sad_len = SW_H + 0.3
    # saddle section: hull of the band and the switch plate, cut off at the
    # finger's sides so it doesn't wing out at the neighbouring fingers
    sec = unary_union([Point(0, 0).buffer(r_out, 128), sbox(-SADDLE_W / 2, top - 2, SADDLE_W / 2, top)]).convex_hull
    sec = sec.intersection(sbox(-50, r_in * 0.35, 50, 50)).difference(Point(0, 0).buffer(r_in, 128))
    saddle = trimesh.creation.extrude_polygon(sec, sad_len)
    band = trimesh.creation.annulus(r_min=r_in, r_max=r_out, height=BAND_LEN, sections=160)
    band.apply_translation([0, 0, BAND_LEN / 2])
    lip = trimesh.creation.box([SADDLE_W, LIP_H, LIP_T])
    lip.apply_translation([0, top + LIP_H / 2, sad_len + LIP_T / 2])
    lip_foot = trimesh.creation.extrude_polygon(sec, LIP_T)   # lip stands on the saddle section
    lip_foot.apply_translation([0, 0, sad_len])
    ring = trimesh.boolean.union([saddle, band, lip, lip_foot], engine='manifold')
    # pilots: from the plate top down to PILOT_FLOOR above the bore
    hz = HOLE_FROM_LEVER
    for sx in (-1, 1):
        x = sx * HOLE_X
        floor_y = np.sqrt(r_in ** 2 - x ** 2) + PILOT_FLOOR
        depth = top - floor_y
        p = trimesh.creation.cylinder(radius=PILOT_D / 2, height=depth + 1, sections=48)
        p.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
        p.apply_translation([x, floor_y + (depth + 1) / 2, hz])
        ring = trimesh.boolean.difference([ring, p], engine='manifold')
    return ring, dict(r_in=r_in, top=top, pilot=depth)

def switch_dummy(top):
    # preview only: body, lever at rest, the two holes
    body = trimesh.creation.box([SW_W, SW_T, SW_H])
    body.apply_translation([0, top + SW_T / 2, SW_H / 2])
    return body

if __name__ == '__main__':
    import os
    os.makedirs('versions', exist_ok=True)
    for c in (50, 65):
        m, info = build(c)
        m.export(f'versions/finger-trigger-ring-v1-c{c}.stl')
        e = np.round(m.extents, 1)
        print(f'c{c}: bore {2 * info["r_in"]:.2f}  plate top {info["top"]:.2f} off axis  '
              f'pilot depth {info["pilot"]:.1f}  watertight={m.is_watertight}  size {e[0]} x {e[1]} x {e[2]}')

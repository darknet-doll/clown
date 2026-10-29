# v4 sizing set: v3 in nine sizes, each with the full saddle and a short one.
# Run from this folder:
#   uv run --with trimesh --with manifold3d --with shapely python export_v4.py
#   ->  versions/finger-trigger-ring-v4-c<size>-full.stl, ...-short.stl
#
#   sizes    45 to 65 mm finger circumference in 2.5 steps
#   full     saddle as v3: runs 8.7 past the screw-hole centres (to 15.9)
#   short    saddle runs half that past the holes, 4.35 (to 11.55); the switch
#            overhangs the end. Less plate along the finger
#
# Section, rounding, flares and through holes are as in export_v3.py; the far-end
# flare under the saddle moves with the shorter end.
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
SPLIT = 1.0
EDGE_R = 0.6
BORE_R = 1.0
PILOT_D = 1.7

SIZES = [45 + 2.5 * i for i in range(9)]
FULL_LEN = SW_H + 0.3
SADDLES = {'full': FULL_LEN, 'short': HOLE_FROM_LEVER + (FULL_LEN - HOLE_FROM_LEVER) / 2}

def rounded(poly, r):
    return poly.buffer(-r, 64).buffer(r, 64)

def flare_cutter(r_in, z0, z1, f, sections=160):
    n = 16
    t = np.linspace(0, np.pi / 2, n)
    lo = [(r_in + f - f * np.sin(a), z0 + f - f * np.cos(a)) for a in t]
    hi = [(r_in + f - f * np.cos(a), z1 - f + f * np.sin(a)) for a in t]
    prof = [(0, z0 - 1), (r_in + f, z0 - 1)] + lo + hi + [(r_in + f, z1 + 1), (0, z1 + 1)]
    return trimesh.creation.revolve(prof, sections=sections)

def build(circ, sad_len):
    r_in = circ / np.pi / 2 + FIT / 2
    r_out = r_in + BAND_WALL
    top = r_in + SADDLE_MIN
    y_cut = r_in * 0.35
    bore = Point(0, 0).buffer(r_in, 256)
    sad = unary_union([Point(0, 0).buffer(r_out, 256), sbox(-SADDLE_W / 2, top - 2, SADDLE_W / 2, top)]).convex_hull
    sad = sad.intersection(sbox(-50, y_cut, 50, 50)).difference(bore)
    band = Point(0, 0).buffer(r_out, 256).difference(bore)
    band = band.difference(sbox(-SPLIT / 2, -50, SPLIT / 2, 0))
    sec_a = rounded(unary_union([band, sad]), EDGE_R)
    sec_b = rounded(sad, EDGE_R)
    a = trimesh.creation.extrude_polygon(sec_a, BAND_LEN)
    b = trimesh.creation.extrude_polygon(sec_b, sad_len - BAND_LEN)
    b.apply_translation([0, 0, BAND_LEN])
    ring = trimesh.boolean.union([a, b], engine='manifold')
    back = trimesh.creation.box([60, 50, 60]); back.apply_translation([0, y_cut - 25, sad_len / 2])
    palm = trimesh.creation.box([60, 50, 60]); palm.apply_translation([0, y_cut + 25, sad_len / 2])
    cut_back = trimesh.boolean.intersection([flare_cutter(r_in, 0, BAND_LEN, BORE_R), back], engine='manifold')
    cut_palm = trimesh.boolean.intersection([flare_cutter(r_in, 0, sad_len, BORE_R), palm], engine='manifold')
    ring = trimesh.boolean.difference([ring, cut_back, cut_palm], engine='manifold')
    for sx in (-1, 1):
        p = trimesh.creation.cylinder(radius=PILOT_D / 2, height=top + 2, sections=48)
        p.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))
        p.apply_translation([sx * HOLE_X, top / 2 + 1, HOLE_FROM_LEVER])
        ring = trimesh.boolean.difference([ring, p], engine='manifold')
    plate = top - np.sqrt(r_in ** 2 - HOLE_X ** 2)
    return ring, dict(r_in=r_in, top=top, pilot=plate)

def name(c, kind):
    return f'finger-trigger-ring-v4-c{c:g}-{kind}'

if __name__ == '__main__':
    for c in SIZES:
        for kind, sad_len in SADDLES.items():
            m, info = build(c, sad_len)
            m.export(f'versions/{name(c, kind)}.stl')
            e = np.round(m.extents, 1)
            print(f'c{c:<4g} {kind:5s}: bore {2 * info["r_in"]:.2f}  plate at holes {info["pilot"]:.2f}  '
                  f'M2x10 clearance {info["pilot"] - (10 - SW_T):.2f}  watertight={m.is_watertight}  '
                  f'bodies={len(m.split(only_watertight=False))}  size {e[0]} x {e[1]} x {e[2]}')

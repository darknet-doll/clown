# v1 fit-test prints for Concept 1 rev B (plain, no clown details).
# Run from this folder: python3 export_v1.py  ->  versions/bubble-housing-v1-*.stl
#
#   base    saddle plate + wrist tongue + 4 belt loops + C-clip + rear rails
#   shroud  rear hood, separate so the base can be tested without it
#   clip    C-clip coupons at 4 bores, 1-4 bumps on the back = smallest to largest
#   slots   strap-slot coupon: 22x3 (20 mm Velcro), 27x3 and 27x4 (25 mm Velcro)
#
# Geometry and units come from concepts/model.py (mm). Every part is exported in
# its print orientation, sitting on z = 0.
import os, sys
import numpy as np, trimesh
from trimesh.creation import box, cylinder, annulus
sys.path.insert(0, 'concepts')
import model as M
from model import at, hand_top, T, axis_z, R_IN, R_OUT, X0, X1, cyl_x

os.makedirs('versions', exist_ok=True)
OUT = 'versions/bubble-housing-v1-{}.stl'

def union(parts):
    return trimesh.boolean.union([p for p in parts], engine='manifold')

def on_bed(m):
    m = m.copy(); m.apply_translation([-m.bounds[0][0] - (m.extents[0] / 2), -m.bounds[0][1] - (m.extents[1] / 2), -m.bounds[0][2]])
    return m

def c_clip(bore, width=8.0, wall=2.4, gap_deg=110):
    ring = annulus(r_min=bore / 2, r_max=bore / 2 + wall, height=width, sections=192)
    half = np.radians(gap_deg / 2)
    # cut the opening with a wedge pointing at +y (becomes "up" once placed)
    r = bore + 10
    wedge = trimesh.creation.extrude_polygon(
        trimesh.path.polygons.Polygon([(0, 0), (r * np.sin(-half) * 1.0, r * np.cos(half)),
                                      (r * np.sin(half), r * np.cos(half))]), width + 2)
    wedge.apply_translation([0, 0, -width / 2 - 1])
    return ring.difference(wedge)

def report(name, m):
    e = np.round(m.extents, 1)
    print(f'{name:8s} watertight={m.is_watertight}  size {e[0]} x {e[1]} x {e[2]} mm  volume {m.volume / 1000:.1f} cm3')

# --- base: plate, tongue, loops, clip, pedestal, rails --------------------------
parts = [M.curved_plate(10, 72, 24, T, ny=60), M.curved_plate(-26, 10, 14, T, ny=40)]
for s in (1, -1):
    parts += M.belt_loop(43, 73, 24 * s, s, hand_top(24)) + M.belt_loop(-26, 4, 14 * s, s, hand_top(14))
clip = c_clip(37.8)
clip.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))   # axis along x
clip.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]))   # opening up (+z)
parts += [at(clip, 62, 0, axis_z), at(box([8, 22, 4.5]), 62, 0, T + 2.0)]
parts += [at(box([20, 4, 4.5]), 36, s * 9, T + 2.0) for s in (1, -1)]
base = on_bed(union(parts))
base.export(OUT.format('base')); report('base', base)

# --- shroud: printed standing on its back wall ----------------------------------
outer = cyl_x(R_OUT, X0, X1).union(at(box([X1 - X0, 32, axis_z - 1.0]), (X0 + X1) / 2, 0, 1.0 + (axis_z - 1.0) / 2))
inner = cyl_x(R_IN, X0 + 2.4, X1 + 1).union(at(box([X1 - X0, 26, axis_z]), (X0 + X1) / 2 + 1.7, 0, T + axis_z / 2))
shroud = outer.difference(inner)
for x in (24, 30, 36, 42, 48):
    shroud = shroud.difference(at(box([2.4, 18, 14]), x, 0, axis_z + R_IN))
shroud = shroud.difference(at(box([8, 10, 9]), X0 + 1, 0, T + 4.5))
shroud.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 1, 0]))  # back wall down
shroud = on_bed(shroud)
shroud.export(OUT.format('shroud')); report('shroud', shroud)

# --- clip coupons: 37.6 / 37.8 / 38.0 / 38.2 bore, lying flat ------------------
coupons = []
for i, bore in enumerate((37.6, 37.8, 38.0, 38.2)):
    c = c_clip(bore)
    c.apply_translation([0, 0, 4.0])
    bumps = [at(cylinder(radius=1.2, height=8, sections=24), (k - i / 2) * 3.5, -(bore / 2 + 2.4 + 0.6), 4.0)
             for k in range(i + 1)]
    c = union([c] + bumps)
    coupons.append(at(c, i * 50.0, 0, 0))
clipset = on_bed(trimesh.util.concatenate(coupons))
clipset.export(OUT.format('clip-coupons')); report('clips', clipset)

# --- strap-slot coupon -----------------------------------------------------------
strip = box([110, 40, T]); strip.apply_translation([0, 0, T / 2])
for x, (length, width) in zip((-35, 0, 35), ((22, 3.0), (27, 3.0), (27, 4.0))):
    strip = strip.difference(at(box([width, length, T + 2]), x, 0, T / 2))
strip = on_bed(strip)
strip.export(OUT.format('slot-coupon')); report('slots', strip)

"""v1 export — dorsal coupon pair, PRE-SCALED to 77.6% (139.7 mm wrist).

Not the full splint. A strip of the dorsal zone (velcro patch + pin comb +
nearby trace-bus cuts from concepts/trace-bus-r3.json) at two candidate
thicknesses, to feel TPU wrap stiffness and patch stability and to check
cut fidelity before the full print:

  versions/wrist-splint-mount-v1-dorsal-coupon-27.stl   (2.72 = uniform Z)
  versions/wrist-splint-mount-v1-dorsal-coupon-35.stl   (3.50 = Z held)

Region in model frame: x 8..86, y 26..90 (100%), so 60.5 x 49.7 printed.
Flat on the plate, no supports. TPU 95A, external spool.
"""

import json

import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import trimesh

SCALE = 0.776
REGION = sg.box(8, 26, 86, 90)
SLOT = 3.0
PAD_R = 2.6

d = json.load(open("concepts/trace-bus-r3.json"))

cuts = []
for pts in d["slots"]:
    cuts.append(sg.LineString(pts).buffer(SLOT / 2, cap_style="round"))
for x, y in d["pads"]:
    cuts.append(sg.Point(x, y).buffer(PAD_R, quad_segs=16))
for x, y, w, h in d["diamonds"]:
    cuts.append(sg.Polygon([(x, y - h / 2), (x + w / 2, y),
                            (x, y + h / 2), (x - w / 2, y)]))
for x, y, ang in d["resistors"]:
    ca, sa = np.cos(ang), np.sin(ang)
    L = 12.0
    cuts.append(sg.LineString([(x - L * ca, y - L * sa),
                               (x + L * ca, y + L * sa)]).buffer(SLOT / 2))
    for s in (-1, 1):
        cuts.append(sg.Point(x + s * (L + 1) * ca,
                             y + s * (L + 1) * sa).buffer(PAD_R, quad_segs=16))
    t = np.linspace(0, 2 * np.pi, 48)
    bx, by = 7 * np.tanh(1.6 * np.cos(t)), 3.1 * np.tanh(1.6 * np.sin(t))
    cuts.append(sg.Polygon(np.c_[x + bx * ca - by * sa, y + bx * sa + by * ca]))

plate = REGION.buffer(-0.0)
# round the coupon corners a touch so TPU corners don't curl
plate = plate.buffer(-3, join_style="round").buffer(3, join_style="round")
coupon = plate.difference(so.unary_union(cuts))
coupon = so.transform(lambda x, y: (x * SCALE, y * SCALE), coupon)
if coupon.geom_type == "MultiPolygon":  # keep the big piece, drop slivers
    coupon = max(coupon.geoms, key=lambda g: g.area)
print(f"coupon footprint: {coupon.bounds[2]-coupon.bounds[0]:.1f} x "
      f"{coupon.bounds[3]-coupon.bounds[1]:.1f} mm, "
      f"{len(coupon.interiors)} interior cuts")

for t, tag in ((2.72, "27"), (3.50, "35")):
    m = trimesh.creation.extrude_polygon(coupon, height=t)
    m.apply_translation(-np.append(m.bounds[0], 0)[:3] * [1, 1, 0])
    path = f"versions/wrist-splint-mount-v1-dorsal-coupon-{tag}.stl"
    m.export(path)
    print(f"wrote {path}  ({len(m.faces)} tris, {t} thick, watertight={m.is_watertight})")

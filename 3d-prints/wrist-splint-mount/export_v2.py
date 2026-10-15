"""v2 export — the FULL remixed splint, pre-scaled to 77.6%.

The approved r3 design (concepts/trace-bus-r3.json) as a printable mesh:
outer boundary + velcro channel slots + label window kept exactly from the
reference STL's extracted section; honeycomb replaced by the trace bus;
solid velcro patch with die diamond.

Geometry decision (2026-10-15): the plate is REBUILT as a flat extrusion
of the z=1.75 section, not a boolean on the original mesh. Kept: every
outline and slot. Lost: the original's edge chamfers and the recessed
tops of the channel bridges (now full height — slightly stronger,
threading unchanged). Thickness 2.72 = uniform 77.6%; 3.5 Z-held variant
is the fallback if the patch is too soft under the housing.

Output: versions/wrist-splint-mount-v2-full.stl (flat, no supports, TPU).
"""

import json

import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import trimesh

SCALE = 0.776
THICK = 2.72
SLOT = 3.0
PAD_R = 2.6

d = json.load(open("concepts/trace-bus-r3.json"))

# chained section loops can carry micro-bowties; buffer(0) heals each ring
plate = sg.Polygon(d["outer"]).buffer(0)
for k in d["kept"]:
    plate = plate.difference(sg.Polygon(k).buffer(0))
assert plate.is_valid and plate.geom_type == "Polygon", plate.geom_type

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

splint = plate.difference(so.unary_union(cuts))
if splint.geom_type == "MultiPolygon":
    pieces = sorted(splint.geoms, key=lambda g: -g.area)
    print("WARNING: cuts severed the plate into", len(pieces),
          "pieces; keeping the largest, dropped areas:",
          [round(p.area, 1) for p in pieces[1:]])
    splint = pieces[0]

splint = so.transform(lambda x, y: (x * SCALE, y * SCALE), splint)
w = splint.bounds[2] - splint.bounds[0]
h = splint.bounds[3] - splint.bounds[1]
print(f"footprint {w:.1f} x {h:.1f} mm, {len(splint.interiors)} holes")

m = trimesh.creation.extrude_polygon(splint, height=THICK)
m.apply_translation([-m.bounds[0][0], -m.bounds[0][1], 0])
out = "versions/wrist-splint-mount-v2-full.stl"
m.export(out)
print(f"wrote {out}  ({len(m.faces)} tris, {THICK} thick, "
      f"watertight={m.is_watertight})")

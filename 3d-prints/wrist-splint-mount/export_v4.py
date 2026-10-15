"""v4 export — the TULLE test square (the real r4 workflow, small).

Disconnected element islands, printed scale, 1.8 tall. NO membrane:
the tulle is the structure, added at the mid-print pause. The STL can't
carry the pause — in Bambu Studio right-click the layer slider at
LAYER 2 (0.4 mm) -> Add Pause. Then: tulle over the plate, taut,
magnets outside the print area, resume.

Contents (45 x 58):
  - two 3-trace bundles: r3-inherited 1.4 hinge vs respaced 2.6 hinge
  - one harlequin diamond, one pad WITH punched centre (tulle shows)
  - one strap tab with a 13 x 2.5 slot — thread the 11 mm velcro strap
    and YANK: this is the fabric-bond test that gates the housing mount

Output: versions/wrist-splint-mount-v4-tulle-square.stl
"""

import shapely.geometry as sg
import shapely.ops as so
import trimesh

W, H = 45.0, 58.0
TRACE_W = 2.3
EL_TOP = 1.8

els = []
for i in range(3):  # bundle A: inherited pitch, hinge 1.4
    y = 6 + i * (TRACE_W + 1.4)
    els.append(sg.LineString([(4, y), (W - 4, y)]).buffer(
        TRACE_W / 2, cap_style="round"))
for i in range(3):  # bundle B: respaced, hinge 2.6
    y = 22 + i * (TRACE_W + 2.6)
    els.append(sg.LineString([(4, y), (W - 4, y)]).buffer(
        TRACE_W / 2, cap_style="round"))
x, y, dw, dh = 9, 42, 4.7, 8.5  # diamond
els.append(sg.Polygon([(x, y - dh / 2), (x + dw / 2, y),
                       (x, y + dh / 2), (x - dw / 2, y)]))
# pad with punched centre (open to tulle)
els.append(sg.Point(21, 42).buffer(2.0, quad_segs=16).difference(
    sg.Point(21, 42).buffer(0.8, quad_segs=12)))
# strap tab, 20 x 10 with the real 13 x 2.5 strap slot
tab = sg.box(28, 48, 48, 58).intersection(sg.box(0, 0, W, H)).buffer(
    -1.5, join_style="round").buffer(1.5, join_style="round")
slot = sg.LineString([(31.75, 53), (44.25, 53)]).buffer(1.25, cap_style="round")
els.append(tab.difference(slot))

merged = so.unary_union(els)
polys = [merged] if merged.geom_type == "Polygon" else list(merged.geoms)
print(f"{len(polys)} islands")
m = trimesh.util.concatenate(
    [trimesh.creation.extrude_polygon(p, height=EL_TOP) for p in polys])
out = "versions/wrist-splint-mount-v4-tulle-square.stl"
m.export(out)
print(f"wrote {out}  ({len(m.faces)} tris, {EL_TOP} tall, "
      f"pause at layer 2 + tulle + magnets)")

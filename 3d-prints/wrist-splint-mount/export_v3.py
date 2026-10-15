"""v3 export — membrane bend coupons: r4's question answered without tulle.

Elements can't print alone (they're disconnected islands; tulle is the
structure), so these coupons replace the fabric with a printed membrane
of the same 68D "TPU for AMS". Two coupons, membrane 0.4 and 0.6:

  versions/wrist-splint-mount-v3-membrane-coupon-04.stl
  versions/wrist-splint-mount-v3-membrane-coupon-06.stl

Each is 45 x 58 at PRINTED scale (no further scaling): membrane field
with two 3-trace bundles on top — pitch A = the r3-inherited spacing
(1.4 hinge, the suspected slab-welder) and pitch B = respaced (2.6
hinge) — plus one diamond and one pad. Curl across the traces over a
marker: pitch B should hinge cleanly, pitch A tells us how bad the
inherited spacing really is. Elements 1.8 tall total.
"""


import shapely.geometry as sg
import shapely.ops as so
import trimesh

W, H = 45.0, 58.0
TRACE_W = 2.3
EL_TOP = 1.8
PAD_R = 2.0

def coupon(membrane_t, tag):
    membrane = sg.box(0, 0, W, H).buffer(-2, join_style="round").buffer(
        2, join_style="round")

    els = []
    # bundle A: r3-inherited pitch (hinge 1.4) at y 8..19
    for i in range(3):
        y = 9 + i * (TRACE_W + 1.4)
        els.append(sg.LineString([(4, y), (W - 4, y)]).buffer(
            TRACE_W / 2, cap_style="round"))
    # bundle B: respaced (hinge 2.6) at y 24..38
    for i in range(3):
        y = 26 + i * (TRACE_W + 2.6)
        els.append(sg.LineString([(4, y), (W - 4, y)]).buffer(
            TRACE_W / 2, cap_style="round"))
    # a diamond and a pad in the top field
    x, y, dw, dh = 14, 48, 4.7, 8.5
    els.append(sg.Polygon([(x, y - dh / 2), (x + dw / 2, y),
                           (x, y + dh / 2), (x - dw / 2, y)]))
    els.append(sg.Point(32, 48).buffer(PAD_R, quad_segs=16))

    el_poly = so.unary_union(els).intersection(membrane)
    if el_poly.geom_type == "Polygon":
        el_poly = [el_poly]
    else:
        el_poly = list(el_poly.geoms)
    base = trimesh.creation.extrude_polygon(membrane, height=membrane_t)
    tops = [trimesh.creation.extrude_polygon(p, height=EL_TOP) for p in el_poly]
    m = trimesh.util.concatenate([base] + tops)
    path = f"versions/wrist-splint-mount-v3-membrane-coupon-{tag}.stl"
    m.export(path)
    print(f"wrote {path}  (membrane {membrane_t}, {len(m.faces)} tris)")

coupon(0.4, "04")
coupon(0.6, "06")

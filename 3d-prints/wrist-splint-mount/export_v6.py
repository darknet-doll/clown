"""v6 export — the full r4 splint on a PRINTED MEMBRANE (no tulle).

Same 61 elements as v5 fused to a 0.4 membrane of the same 68D in
place of fabric: one print, no pause, no magnets (tulle in delivery).
Channel slots, strap slots, eyelets, pad centres and the die diamond
pierce the membrane fully.

Decisions baked in (all recorded in wrist-splint-mount.md):
- MIRRORED IN X for the left hand: tulle side to skin, elements out
- Bundles respaced from r3's cutout pitch to 6.5 mm (100%) so the tulle
  hinges between traces are ~2.7 printed — the anti-slab fix
- Edge binding dashes 10/5 (100%), shortened to 6/4 on the forearm rim
  (x < -80) where they run along the curl direction
- Patch tile: 2 strap slots (13 x 2.5 printed), 4 eyelets, die diamond;
  bundle A traces land ON the tile (merged, structural)
- Annular pads (punched centres show tulle)
- Pre-scaled 77.6%; elements 1.8 tall; pause at LAYER 2 in Bambu

Output: versions/wrist-splint-mount-v6-membrane-full.stl + preview PNG.
"""

import json

import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import trimesh

SCALE = 0.776
EL_TOP = 1.8
TRACE_W = 3.0      # 100% frame -> 2.33 printed
PAD_R, PAD_HOLE = 2.6, 1.04
PITCH = 6.5        # respaced: hinge (6.5-3.0)*0.776 = 2.7 printed

d = json.load(open("concepts/splint-outline.json"))
loops = [np.array(l["pts"]) for l in d["loops"]]
areas = [l["area"] for l in d["loops"]]

def keep_slot(p, a):
    w, h = np.ptp(p[:, 0]), np.ptp(p[:, 1])
    aspect = max(w, h) / max(min(w, h), 1e-6)
    fill = abs(a) / (w * h)
    return (aspect >= 2.4 and abs(a) <= 130
            and (fill >= 0.60 or (fill >= 0.50 and abs(a) >= 60)))

outer = sg.Polygon(loops[0]).buffer(0)
kept = [sg.Polygon(p).buffer(0) for p, a in zip(loops[1:], areas[1:])
        if keep_slot(p, a)]
print(f"outline ok, {len(kept)} channel slots")

P = dict(x0=25, y0=42, x1=78, y1=86)
els = []

def hrun(y, x0, x1, jogs=()):
    pts, yy = [(x0, y)], y
    for xj, dy in jogs:
        pts += [(xj, yy), (xj + abs(dy), yy + dy)]
        yy += dy
    pts.append((x1, yy))
    return pts

def trace(pts, pad_start=True, pad_end=True):
    els.append(sg.LineString(pts).buffer(TRACE_W / 2, cap_style="round"))
    for flag, p in ((pad_start, pts[0]), (pad_end, pts[-1])):
        if flag:
            els.append(sg.Point(p).buffer(PAD_R, quad_segs=16).difference(
                sg.Point(p).buffer(PAD_HOLE, quad_segs=12)))

def diamond(x, y, w=6.0, h=11.0):
    els.append(sg.Polygon([(x, y - h / 2), (x + w / 2, y),
                           (x, y + h / 2), (x - w / 2, y)]))

# bundle A — lands ON the patch tile (pad only at the forearm end)
for i in range(4):
    trace(hrun(56 + i * PITCH, -84, P["x0"] + 2), pad_end=False)
# pin comb under the patch
for x in np.arange(32, P["x1"] - 3, 7):
    els.append(sg.LineString([(x, P["y0"] - 6.5), (x, P["y0"] - 1)]).buffer(
        TRACE_W / 2, cap_style="round"))
# bundles B, C, D (respaced; staggered free ends get pads)
for i in range(4):
    trace(hrun(1 + i * PITCH, -84, 8 - 3 * i))
for i in range(3):
    trace(hrun(-19 + i * PITCH, -84, -2 - 3 * i))
for i in range(3):
    trace(hrun(-51 + i * PITCH, -84, 16 + 6 * i))

# harlequin rows + resistors in the gap bands
for x in (-88, -72, -24, -8, 6):
    diamond(x, 33)
for x in (-85, -69, -16, 0):
    diamond(x, -27.5)

def resistor(x, y, ang=0.0):
    ca, sa = np.cos(ang), np.sin(ang)
    L = 12.0
    els.append(sg.LineString([(x - L * ca, y - L * sa),
                              (x + L * ca, y + L * sa)]).buffer(TRACE_W / 2))
    for s in (-1, 1):
        p = (x + s * (L + 1) * ca, y + s * (L + 1) * sa)
        els.append(sg.Point(p).buffer(PAD_R, quad_segs=16).difference(
            sg.Point(p).buffer(PAD_HOLE, quad_segs=12)))
    t = np.linspace(0, 2 * np.pi, 48)
    bx, by = 7 * np.tanh(1.6 * np.cos(t)), 3.1 * np.tanh(1.6 * np.sin(t))
    els.append(sg.Polygon(np.c_[x + bx * ca - by * sa, y + bx * sa + by * ca]))

resistor(-48, 33)
resistor(-40, -27.5)
resistor(-30, -68)

# patch tile: slots, eyelets, die diamond
tile = sg.box(P["x0"], P["y0"], P["x1"], P["y1"]).buffer(
    -3, join_style="round").buffer(3, join_style="round")
cxp, cyp = (P["x0"] + P["x1"]) / 2, (P["y0"] + P["y1"]) / 2
tile = tile.difference(sg.Polygon([(cxp, cyp - 7.7), (cxp + 4.5, cyp),
                                   (cxp, cyp + 7.7), (cxp - 4.5, cyp)]))
for sy in (P["y0"] + 9, P["y1"] - 9):
    tile = tile.difference(sg.LineString(
        [(cxp - 6.8, sy), (cxp + 6.8, sy)]).buffer(1.61, cap_style="round"))
for ex in (P["x0"] + 6, P["x1"] - 6):
    for ey in (P["y0"] + 6, P["y1"] - 6):
        tile = tile.difference(sg.Point(ex, ey).buffer(2.0, quad_segs=12))
els.append(tile)

# strap tabs around every kept channel slot
for k in kept:
    x0, y0, x1, y1 = k.bounds
    tab = sg.box(x0 - 2.5, y0 - 2.5, x1 + 2.5, y1 + 2.5).buffer(
        -1.5, join_style="round").buffer(1.5, join_style="round")
    els.append(tab.difference(k))

# edge binding: dashes on a 2.5 mm inset ring; short ticks on the forearm rim
inset = outer.buffer(-2.5)
rings = ([inset.exterior] if inset.geom_type == "Polygon"
         else [g.exterior for g in inset.geoms])
for ring in rings:
    L, s = ring.length, 0.0
    while s < ring.length - 2:
        x_here = ring.interpolate(s).x
        dash, gap = (6.0, 4.0) if x_here < -80 else (10.0, 5.0)
        pts = [ring.interpolate(min(s + t, L)) for t in
               np.linspace(0, dash, max(3, int(dash / 2)))]
        els.append(sg.LineString([(p.x, p.y) for p in pts]).buffer(
            2.0, cap_style="round"))
        s += dash + gap

# merge overlaps (binding meeting tabs etc.), clip to outline, despeckle
merged = so.unary_union(els).intersection(outer)
polys = [merged] if merged.geom_type == "Polygon" else list(merged.geoms)
polys = [p for p in polys if p.area >= 3.0]
print(f"{len(polys)} islands after union + despeckle")

# membrane: full outline minus channel slots minus every element hole
MEMBRANE_T = 0.4
holes = list(kept)
for p in polys:
    for ring in p.interiors:
        holes.append(sg.Polygon(ring))
membrane = outer.difference(so.unary_union(holes))
mem_polys = ([membrane] if membrane.geom_type == "Polygon"
             else list(membrane.geoms))

# MIRROR for the left hand, then scale to the wrist
def fix(p):
    if p.exterior.is_ccw is False:
        p = sg.Polygon(list(p.exterior.coords)[::-1],
                       [list(i.coords)[::-1] for i in p.interiors])
    return p

mir = lambda p: so.transform(lambda x, y: (-x * SCALE, y * SCALE), p)
meshes = [trimesh.creation.extrude_polygon(fix(mir(p)), height=MEMBRANE_T)
          for p in mem_polys if p.area > 3]
mirrored = [mir(p) for p in polys]
for p in mirrored:
    meshes.append(trimesh.creation.extrude_polygon(fix(p), height=EL_TOP))
m = trimesh.util.concatenate(meshes)
m.apply_translation([-m.bounds[0][0], -m.bounds[0][1], 0])
w, h = m.bounds[1][:2] - m.bounds[0][:2]
out = "versions/wrist-splint-mount-v6-membrane-full.stl"
m.export(out)
print(f"wrote {out}  {w:.1f} x {h:.1f} x {EL_TOP}, {len(m.faces)} tris")

# preview
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP

fig, ax = plt.subplots(figsize=(13, 11))
fig.patch.set_facecolor("#141416")
ax.set_facecolor("#141416")
for p in mem_polys:
    q = mir(p)
    ax.add_patch(MP(np.array(q.exterior.coords), fc="#3a3b42"))
    for hole in q.interiors:
        ax.add_patch(MP(np.array(hole.coords), fc="#141416"))
for q in mirrored:
    ax.add_patch(MP(np.array(q.exterior.coords), fc="#F2F2F2"))
    for hole in q.interiors:
        ax.add_patch(MP(np.array(hole.coords), fc="#3a3b42"))
ax.autoscale()
ax.set_aspect("equal")
ax.axis("off")
ax.set_title(f"v6 full membrane splint, MIRRORED (left hand), printed scale "
             f"{w:.0f} x {h:.0f}", color="#eee", family="monospace")
fig.savefig("versions/wrist-splint-mount-v6-preview.png", dpi=110,
            facecolor="#141416", bbox_inches="tight")
print("preview ok")

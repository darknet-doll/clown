"""v7 export — WRAP BAND: a full-circumference wrist band test, no tulle.

darknetdoll 2026-10-21: test a piece that forms all the way round the wrist
and closes with velcro threaded through it. Same construction as v6
(68D elements fused to a 0.4 printed membrane, one print, no pause), but a
straight band instead of the splint outline.

Dimensions are PRINTED mm (no further scaling):
- Band 120 long x 40 wide. Wrist 139.7, so the ends sit ~20 apart round the
  wrist and two 11 mm straps bridge the gap (adjustable)
- Each end: a solid tile 18 long with two slot pairs (one per strap, at
  y +-10). Slot 13 across x 2.5 along, bar 4 between: strap goes down one
  slot, under the bar, up the other — same as the housing's velcro slots
- Middle: flex zone. Elements run ACROSS the band (traces with pads, columns
  of harlequin diamonds) so the wrap bends at the membrane between them.
  Hinges >= 2.5 printed (v5/v6 anti-slab rule)
- Long edges: short dashed binding (4 on / 2 off) so the membrane edge
  can't tear but still bends

Output: versions/wrist-splint-mount-v7-wrap-band.stl + preview PNG.
"""

import numpy as np
import shapely.geometry as sg
import shapely.ops as so
import trimesh

L, W = 120.0, 40.0
EL_TOP, MEMBRANE_T = 1.8, 0.4
TILE = 18.0
SLOT_ACROSS, SLOT_ALONG, BAR = 13.0, 2.5, 4.0
STRAP_Y = (-10.0, 10.0)
TRACE_W, PAD_R, PAD_HOLE = 2.4, 2.0, 0.8
DIAMOND = (4.7, 8.5)          # along x, across y — v6's printed size
EDGE = 2.0                    # binding width

band = sg.box(0, -W / 2, L, W / 2).buffer(-4, join_style="round").buffer(4, join_style="round")
els, holes = [], []

# end tiles with slot pairs
for x_end, s in ((0.0, 1), (L, -1)):
    x0, x1 = sorted((x_end, x_end + s * TILE))
    tile = sg.box(x0, -W / 2, x1, W / 2)
    for sy in STRAP_Y:
        for off in (4.0, 4.0 + SLOT_ALONG + BAR):       # from the band end
            xs = x_end + s * (off + SLOT_ALONG / 2)
            slot = sg.box(xs - SLOT_ALONG / 2, sy - SLOT_ACROSS / 2,
                          xs + SLOT_ALONG / 2, sy + SLOT_ACROSS / 2)
            tile = tile.difference(slot)
            holes.append(slot)
    els.append(tile)

# flex zone: alternate a cross trace (pads both ends) and a diamond column
def pad(x, y):
    p = sg.Point(x, y)
    hole = p.buffer(PAD_HOLE, quad_segs=12)
    holes.append(hole)
    return p.buffer(PAD_R, quad_segs=16).difference(hole)

def diamond(x, y):
    w, h = DIAMOND
    return sg.Polygon([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)])

GAP = 3.0                                  # membrane hinge between elements
step = TRACE_W / 2 + GAP + DIAMOND[0] / 2  # trace centre -> diamond centre
x, kind = TILE + GAP + PAD_R, 0
y_in = W / 2 - EDGE - GAP - PAD_R          # pads stay clear of the binding
while x < L - TILE - GAP - PAD_R:
    if kind == 0:
        els.append(sg.LineString([(x, -y_in), (x, y_in)]).buffer(TRACE_W / 2, cap_style="flat"))
        els += [pad(x, -y_in), pad(x, y_in)]
        x += max(step, PAD_R + GAP + DIAMOND[0] / 2)
    else:
        for y in (-10.5, 0.0, 10.5):
            els.append(diamond(x, y))
        x += max(step, DIAMOND[0] / 2 + GAP + PAD_R)
    kind ^= 1

# edge binding: short dashes along both long edges, flex zone only
for ye in (-W / 2 + EDGE / 2, W / 2 - EDGE / 2):
    xd = TILE
    while xd < L - TILE:
        els.append(sg.box(xd, ye - EDGE / 2, min(xd + 4, L - TILE), ye + EDGE / 2))
        xd += 6.0

merged = so.unary_union(els).intersection(band)
polys = [merged] if merged.geom_type == "Polygon" else list(merged.geoms)
polys = [p for p in polys if p.area >= 3.0]
membrane = band.difference(so.unary_union(holes))
mem_polys = [membrane] if membrane.geom_type == "Polygon" else list(membrane.geoms)
print(f"{len(polys)} element islands")

def fix(p):
    return sg.polygon.orient(p, 1.0)

meshes = [trimesh.creation.extrude_polygon(fix(p), height=MEMBRANE_T) for p in mem_polys]
meshes += [trimesh.creation.extrude_polygon(fix(p), height=EL_TOP) for p in polys]
m = trimesh.util.concatenate(meshes)
m.apply_translation(-m.bounds[0])
out = "versions/wrist-splint-mount-v7-wrap-band.stl"
m.export(out)
w, h = m.bounds[1][:2]
print(f"wrote {out}  {w:.1f} x {h:.1f} x {EL_TOP}, {len(m.faces)} tris")

# preview: flat band, plus a section of it wrapped on the wrist
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MP, Circle

BG, MEM, EL, STRAP = "#141416", "#3a3b42", "#F2F2F2", "#f2a65a"
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(16, 6.5), gridspec_kw=dict(width_ratios=[2.2, 1]))
fig.patch.set_facecolor(BG)
for a in (ax, ax2):
    a.set_facecolor(BG)
    a.set_aspect("equal")
    a.axis("off")

for p in mem_polys:
    ax.add_patch(MP(np.array(p.exterior.coords), fc=MEM))
    for r in p.interiors:
        ax.add_patch(MP(np.array(r.coords), fc=BG))
for p in polys:
    ax.add_patch(MP(np.array(p.exterior.coords), fc=EL))
    for r in p.interiors:
        ax.add_patch(MP(np.array(r.coords), fc=MEM if r.length > 10 else BG))
for sy in STRAP_Y:          # straps drawn across the gap, beyond the band ends
    for x0, x1 in ((-14, 4), (L - 4, L + 14)):
        ax.add_patch(MP([(x0, sy - 5.5), (x1, sy - 5.5), (x1, sy + 5.5), (x0, sy + 5.5)],
                        fc=STRAP, alpha=0.85))
ax.set_xlim(-18, L + 18)
ax.set_ylim(-W / 2 - 8, W / 2 + 12)
ax.text(-16, W / 2 + 6, f"v7 wrap band — {L:.0f} x {W:.0f}, elements {EL_TOP} on a {MEMBRANE_T} membrane"
        "   (orange: the two 11 mm straps)", color=EL, fontsize=11)
ax.text(TILE / 2, -W / 2 - 5, "slot tile", color=EL, ha="center", fontsize=9)
ax.text(L / 2, -W / 2 - 5, "flex zone: bends at the membrane between elements",
        color=EL, ha="center", fontsize=9)

# wrapped view: wrist as an ellipse of the right circumference
a_, b_ = 25.0, 19.0          # semi-axes; perimeter ~139.7
t = np.linspace(0, 2 * np.pi, 400)
ax2.add_patch(MP(np.c_[a_ * np.cos(t), b_ * np.sin(t)], fc="#6b5a52"))
seg = np.hypot(np.diff(a_ * np.cos(t)), np.diff(b_ * np.sin(t)))
s = np.r_[0, np.cumsum(seg)]
gap = s[-1] + 2 * np.pi * 1.0 - L     # band rides ~1 out from the skin
start = np.pi / 2 + (gap / 2) / ((a_ + b_) / 2)
tt = np.linspace(start, start + 2 * np.pi - gap / ((a_ + b_) / 2), 300)
ax2.plot((a_ + 1.2) * np.cos(tt), (b_ + 1.2) * np.sin(tt), color=EL, lw=4, solid_capstyle="butt")
tg = np.linspace(start - gap / ((a_ + b_) / 2) - 0.05, start + 0.05, 30)
ax2.plot((a_ + 3.2) * np.cos(tg), (b_ + 3.2) * np.sin(tg), color=STRAP, lw=4)
ax2.set_xlim(-34, 34)
ax2.set_ylim(-30, 34)
ax2.text(0, 29, f"round the wrist: ~{gap:.0f} gap at the back, closed by the straps",
         color=EL, ha="center", fontsize=9)
ax2.text(0, 0, "wrist\n139.7 round", color=EL, ha="center", va="center", fontsize=9)

plt.savefig("versions/wrist-splint-mount-v7-preview.png", dpi=110, bbox_inches="tight", facecolor=BG)
print("versions/wrist-splint-mount-v7-preview.png")

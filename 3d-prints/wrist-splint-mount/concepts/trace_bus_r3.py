"""r3 — trace-bus openwork placed on the REAL splint outline.

Reads splint-outline.json (from splint_outline.py). Keeps the outer
boundary, the velcro-channel slots and the label window; drops the
honeycomb; authors the CIRCUIT trace bus in its place, harlequin accents,
resistors as punctuation. The solid dorsal mount patch (the housing's
velcro landing) plays the chip: bundle A terminates on it like pins and
it carries the punched diamond.

Cutout floors at 100% model scale: slots 3.0, webs >= 3.0, so 2.3 each
at the 77.6% print scale. All cutouts are auto-checked for >= 7 mm to the
outer boundary and >= 4 mm to kept slots; violations are dropped and
reported, then reviewed visually.

Outputs: trace-bus-r3.json (svg-ready geometry) + trace-bus-r3.png.
"""

import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon

VOID, PLATE, PINK = "#141416", "#BAD2DE", "#E49CB4"

SLOT = 3.0
PAD_R = 2.6
MARGIN_EDGE = 7.0
MARGIN_SLOT = 4.0

# the housing's velcro landing, solid (dorsal band between thumb + channels)
PATCH = dict(x0=25, y0=42, x1=78, y1=86)

data = json.load(open("splint-outline.json"))
loops = [np.array(l["pts"]) for l in data["loops"]]
areas = [l["area"] for l in data["loops"]]
outer = loops[0]

# keep channel slots / windows (elongated, rectangular-ish); drop
# honeycomb cells and low-fill partial-hex slivers
def keep_slot(p, a):
    w, h = np.ptp(p[:, 0]), np.ptp(p[:, 1])
    aspect = max(w, h) / max(min(w, h), 1e-6)
    fill = abs(a) / (w * h)
    return (aspect >= 2.4 and abs(a) <= 130
            and (fill >= 0.60 or (fill >= 0.50 and abs(a) >= 60)))

kept, dropped = [], 0
for p, a in zip(loops[1:], areas[1:]):
    if keep_slot(p, a):
        kept.append(p)
    else:
        dropped += 1
print(f"kept {len(kept)} slots, dropped {dropped} honeycomb loops")

# dense boundary samples for distance checks
def densify(p, step=1.0):
    out = []
    for i in range(len(p)):
        a, b = p[i], p[(i + 1) % len(p)]
        n = max(1, int(np.hypot(*(b - a)) / step))
        out.extend(a + (b - a) * t for t in np.linspace(0, 1, n, endpoint=False))
    return np.array(out)

bnd = densify(outer)
kept_pts = np.vstack([densify(k) for k in kept]) if kept else np.empty((0, 2))

def clear(x, y, extra=0.0):
    d_edge = np.hypot(*(bnd - (x, y)).T).min()
    d_slot = np.hypot(*(kept_pts - (x, y)).T).min() if len(kept_pts) else 99
    return d_edge >= MARGIN_EDGE + extra and d_slot >= MARGIN_SLOT + extra

# ------------------------------------------------------------- authoring
slots, pads, diamonds, resistors, rejected = [], [], [], [], []

def hrun(y, x0, x1, jogs=()):
    """Left-to-right run with 45-degree jogs: (x_at, dy)."""
    pts, x, yy = [(x0, y)], x0, y
    for xj, dy in jogs:
        pts += [(xj, yy), (xj + abs(dy), yy + dy)]
        yy += dy
    pts.append((x1, yy))
    return pts

def add_trace(pts, pad_start=True, pad_end=True):
    for px, py in pts:
        if not clear(px, py, SLOT / 2):
            rejected.append((px, py))
    slots.append(pts)
    if pad_start:
        pads.append(pts[0])
    if pad_end:
        pads.append(pts[-1])

def add_diamond(x, y, w=6.0, h=11.0):
    if clear(x, y, h / 2 - 2):
        diamonds.append((x, y, w, h))
    else:
        rejected.append((x, y))

# bundle A — four traces feed the mount patch like pins (no end pads)
for y in (58, 64, 70, 76):
    add_trace(hrun(y, -84, PATCH["x0"] - 4.5), pad_end=False)
# pin comb along the patch bottom edge
for x in np.arange(32, PATCH["x1"] - 3, 7):
    slots.append([(x, PATCH["y0"] - 6.5), (x, PATCH["y0"] - 1)])

# bundle B — four traces, staggered end pads short of the thumb opening
for i, y in enumerate((2, 8, 14, 20)):
    add_trace(hrun(y, -84, 8 - 3 * i))

# bundle C — three traces
for i, y in enumerate((-18, -12, -6)):
    add_trace(hrun(y, -84, -2 - 3 * i))

# bundle D — three traces with a 45 jog into the lower-right field
for i, y in enumerate((-50, -44, -38)):
    add_trace(hrun(y, -84, 16 + 6 * i))

# harlequin rows in the gap bands, resistor punctuation inline
for x in (-88, -72, -24, -8, 6):
    add_diamond(x, 34)
resistors.append((-48, 34, 0.0))
for x in (-85, -69, -16, 0):
    add_diamond(x, -28)
resistors.append((-40, -28, 0.0))
resistors.append((-30, -68, 0.0))

# punched diamond on the patch (the chip's die mark)
diamonds.append(((PATCH["x0"] + PATCH["x1"]) / 2,
                 (PATCH["y0"] + PATCH["y1"]) / 2, 7.0, 12.0))

for x, y, ang in resistors:
    for s in (-1, 0, 1):
        px, py = x + s * 13 * np.cos(ang), y + s * 13 * np.sin(ang)
        if not clear(px, py, 2.6):
            rejected.append((px, py))

print(f"{len(slots)} slots, {len(pads)} pads, {len(diamonds)} diamonds, "
      f"{len(resistors)} resistors; {len(rejected)} clearance rejects")
for r in rejected:
    print("  reject near", np.round(r, 1))

# ------------------------------------------------------------- outputs
out = dict(slot_w=SLOT, pad_r=PAD_R, patch=PATCH,
           outer=np.round(outer, 2).tolist(),
           kept=[np.round(k, 2).tolist() for k in kept],
           honeycomb=[np.round(p, 2).tolist()
                      for p, a in zip(loops[1:], areas[1:])
                      if not keep_slot(p, a)],
           slots=slots, pads=pads, diamonds=diamonds, resistors=resistors)
json.dump(out, open("trace-bus-r3.json", "w"), default=float)
print("wrote trace-bus-r3.json")

fig, ax = plt.subplots(figsize=(15, 13))
fig.patch.set_facecolor(VOID)
ax.set_facecolor(VOID)
ax.fill(outer[:, 0], outer[:, 1], color=PLATE, zorder=1)
for k in kept:
    ax.fill(k[:, 0], k[:, 1], color=VOID, zorder=2)

px_mm = lambda mm: mm * (ax.get_window_extent().width /
                         np.diff(ax.get_xlim())[0]) * 72 / 110
fig.canvas.draw()
for pts in slots:
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], color=VOID, lw=px_mm(SLOT),
            solid_capstyle="round", solid_joinstyle="round", zorder=3)
for x, y in pads:
    ax.add_patch(Circle((x, y), PAD_R, fc=VOID, zorder=3))
for x, y, w, h in diamonds:
    ax.add_patch(Polygon([(x, y - h / 2), (x + w / 2, y),
                          (x, y + h / 2), (x - w / 2, y)], fc=VOID, zorder=4))
for x, y, ang in resistors:
    ca, sa = np.cos(ang), np.sin(ang)
    L = 12.0
    ax.plot([x - L * ca, x + L * ca], [y - L * sa, y + L * sa],
            color=VOID, lw=px_mm(SLOT), solid_capstyle="round", zorder=3)
    for s in (-1, 1):
        ax.add_patch(Circle((x + s * (L + 1) * ca, y + s * (L + 1) * sa),
                            PAD_R, fc=VOID, zorder=3))
    t = np.linspace(0, 2 * np.pi, 24)
    bx, by = 7 * np.tanh(1.6 * np.cos(t)), 3.1 * np.tanh(1.6 * np.sin(t))
    ax.add_patch(Polygon(np.c_[x + bx * ca - by * sa, y + bx * sa + by * ca],
                         fc=VOID, zorder=3))
ax.add_patch(plt.Rectangle((PATCH["x0"], PATCH["y0"]),
                           PATCH["x1"] - PATCH["x0"], PATCH["y1"] - PATCH["y0"],
                           fill=False, ec=PINK, lw=1.6, ls="--", zorder=5))
ax.text(PATCH["x0"] + 2, PATCH["y1"] - 5, "housing velcro patch (solid)",
        color=PINK, fontsize=9, family="monospace", zorder=5)
ax.set_aspect("equal")
ax.axis("off")
ax.set_title("trace-bus r3 on the real splint outline (100% model mm)",
             color="#F2F2F2", family="monospace")
fig.savefig("trace-bus-r3.png", dpi=110, facecolor=VOID, bbox_inches="tight")
print("wrote trace-bus-r3.png")

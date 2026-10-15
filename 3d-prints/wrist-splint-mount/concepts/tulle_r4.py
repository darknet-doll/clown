"""r4 concept — the trace bus as POSITIVE elements printed on tulle.

The tulle-sandwich flip of r3: no plate at all. Rigid printed tiles
(traces, pads, diamonds, resistors, the velcro patch, edge binding,
strap tabs) sit on a tulle substrate that is trapped between the first
print layers and the rest mid-print. All flex is fabric, so the stiff
68D "TPU for AMS" (or PLA) becomes the RIGHT material, feeds through
the AMS, and the piece can be multicolour per the CIRCUIT palette:
tulle reads as the board ground, elements as traces.

Geometry is lifted straight from concepts/trace-bus-r3.json (same model
frame, 100%; printed at 77.6% like everything else).

Output: tulle-sandwich-r4.png — look only.
"""

import json

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyBboxPatch
from matplotlib.path import Path

GROUND = "#141416"   # page / what shows through bare tulle
TULLE = "#23242a"    # tulle field tint
MESH = "#3a3c45"     # tulle mesh lines
GREEN = "#F2F2F2"    # CIRCUIT primary (reads white)
PINK = "#F2B8CC"     # CIRCUIT secondary

d = json.load(open("trace-bus-r3.json"))
outer = np.array(d["outer"])

fig, ax = plt.subplots(figsize=(15, 13))
fig.patch.set_facecolor(GROUND)
ax.set_facecolor(GROUND)

# --- tulle substrate: tinted field + fine mesh, clipped to the outline
clip_path = Path(outer)
patch_clip = Polygon(outer, fc=TULLE, zorder=1)
ax.add_patch(patch_clip)
lo, hi = outer.min(axis=0) - 2, outer.max(axis=0) + 2
mesh_lines = []
for v in np.arange(lo[0], hi[0], 2.6):
    mesh_lines.append(ax.plot([v, v], [lo[1], hi[1]], color=MESH, lw=0.35,
                              zorder=1.5)[0])
for v in np.arange(lo[1], hi[1], 2.6):
    mesh_lines.append(ax.plot([lo[0], hi[0]], [v, v], color=MESH, lw=0.35,
                              zorder=1.5)[0])
for ln in mesh_lines:
    ln.set_clip_path(patch_clip)

def lw_mm(mm):
    fig.canvas.draw()
    px = ax.get_window_extent().width / np.diff(ax.get_xlim())[0]
    return mm * px * 72 / 110

ax.set_xlim(lo[0] - 4, hi[0] + 4)
ax.set_ylim(lo[1] - 10, hi[1] + 4)
ax.set_aspect("equal")
ax.axis("off")

# --- edge binding: printed dashes riding the boundary (and thumb rim)
def resample(p, step=1.0):
    seg = np.vstack([p, p[:1]])
    dl = np.hypot(*np.diff(seg, axis=0).T)
    s = np.concatenate([[0], np.cumsum(dl)])
    t = np.arange(0, s[-1], step)
    return np.c_[np.interp(t, s, seg[:, 0]), np.interp(t, s, seg[:, 1])]

rb = resample(outer)
W = lw_mm(4.0)
i = 0
while i < len(rb) - 12:
    ax.plot(rb[i:i + 12, 0], rb[i:i + 12, 1], color=GREEN, lw=W,
            solid_capstyle="round", zorder=3)
    i += 16

# --- strap tabs: a rigid tile around every kept channel slot, hole open
for k in d["kept"]:
    k = np.array(k)
    cx, cy = k.mean(axis=0)
    w, h = np.ptp(k[:, 0]) + 5, np.ptp(k[:, 1]) + 5
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=2",
                                fc=GREEN, ec="none", zorder=3))
    ax.add_patch(Polygon(k, fc=GROUND, zorder=4))  # tulle cut out of the slot

# --- the trace bus, positive
for pts in d["slots"]:
    p = np.array(pts)
    ax.plot(p[:, 0], p[:, 1], color=GREEN, lw=lw_mm(3.0),
            solid_capstyle="round", solid_joinstyle="round", zorder=5)
for x, y in d["pads"]:
    ax.add_patch(Circle((x, y), d["pad_r"], fc=GREEN, zorder=5))
    ax.add_patch(Circle((x, y), d["pad_r"] * 0.4, fc=TULLE, zorder=6))
for x, y, w, h in d["diamonds"][:-1]:
    ax.add_patch(Polygon([(x, y - h / 2), (x + w / 2, y),
                          (x, y + h / 2), (x - w / 2, y)], fc=PINK, zorder=5))
for x, y, ang in d["resistors"]:
    ca, sa = np.cos(ang), np.sin(ang)
    L = 12.0
    ax.plot([x - L * ca, x + L * ca], [y - L * sa, y + L * sa],
            color=GREEN, lw=lw_mm(3.0), solid_capstyle="round", zorder=5)
    t = np.linspace(0, 2 * np.pi, 24)
    bx, by = 7 * np.tanh(1.6 * np.cos(t)), 3.1 * np.tanh(1.6 * np.sin(t))
    ax.add_patch(Polygon(np.c_[x + bx * ca - by * sa, y + bx * sa + by * ca],
                         fc=PINK, zorder=6))

# --- velcro patch: one big rigid tile, pink frame, die diamond opens to tulle
P = d["patch"]
pw, ph = P["x1"] - P["x0"], P["y1"] - P["y0"]
ax.add_patch(FancyBboxPatch((P["x0"], P["y0"]), pw, ph,
                            boxstyle="round,pad=0,rounding_size=3",
                            fc=PINK, ec=GREEN, lw=2.2, zorder=5))
dx, dy = P["x0"] + pw / 2, P["y0"] + ph / 2
ax.add_patch(Polygon([(dx, dy - 6), (dx + 3.5, dy), (dx, dy + 6),
                      (dx - 3.5, dy)], fc=TULLE, zorder=6))
# pin comb as positive stubs
for x in np.arange(32, P["x1"] - 3, 7):
    ax.plot([x, x], [P["y0"] - 6.5, P["y0"] - 1], color=GREEN,
            lw=lw_mm(3.0), solid_capstyle="round", zorder=5)

ax.set_title("r4 tulle sandwich - trace bus as printed elements on fabric\n"
             "(100% frame; dark = bare tulle = all the flex; "
             "68D 'TPU for AMS' or PLA, AMS multicolour OK)",
             color=GREEN, family="monospace", fontsize=12)
fig.text(0.5, 0.04,
         "print 2 base layers - pause - tulle on, magnets to the steel plate - "
         "resume. elements ~1.8 total; velcro patch stays one rigid tile",
         color="#9aa3ad", fontsize=10, ha="center", family="monospace")
fig.savefig("tulle-sandwich-r4.png", dpi=110, facecolor=GROUND,
            bbox_inches="tight")
print("wrote tulle-sandwich-r4.png")

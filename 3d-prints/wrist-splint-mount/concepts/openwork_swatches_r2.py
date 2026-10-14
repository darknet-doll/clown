"""Openwork concepts r2 — CIRCUIT mode with harlequin accents (no hearts,
darknetdoll's call 2026-10-14: diamonds replace the signature heart).

Clone of openwork_swatches.py (r1 stays untouched, per the HEXCODE working
method). Four 88 x 88 mm swatches of circuit-grammar CUTOUTS for the TPU
splint: traces are slots, pads are plain holes (an annular pad would drop
its centre), chips are solid islands implied by pin combs, resistors are
compound pad-lead-body slots. 45-degree doglegs, bundles, edge combs per
references/circuit.md; bundle pitch widened 3.4 -> 4.8 because in aperture
form the house pitch leaves a 1.0 web, under the floor.

All slots >= 2.4 mm and webs >= 2.2 mm at 100%, so >= 1.8 / 1.7 after the
77.6% slicer scale. Plate drawn ice blue to compare against r1; in black
TPU the same geometry goes full CIRCUIT.

Output: openwork-swatches-r2.png. Look only.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, FancyBboxPatch

VOID = "#141416"
PLATE = "#BAD2DE"
PINK = "#E49CB4"
WHITE = "#F2F2F2"

TILE = 88.0
SLOT = 2.4          # trace slot width, mm at 100%
PITCH = 4.8         # bundle pitch (house 3.4 widened for aperture webs)
PAD_R = 2.2

FIG_DPI = 140


def lw_mm(ax, mm):
    """Line width in points for a stroke of `mm` data units on this axes."""
    px_per_mm = ax.get_window_extent().width / np.diff(ax.get_xlim())[0]
    return mm * px_per_mm * 72.0 / FIG_DPI


def tile_axes(ax, title, note):
    ax.set_xlim(-4, TILE + 4)
    ax.set_ylim(-15, TILE + 4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(FancyBboxPatch((0, 0), TILE, TILE,
                                boxstyle="round,pad=0,rounding_size=4",
                                fc=PLATE, ec="none", zorder=1))
    ax.set_title(title, color=WHITE, fontsize=13, pad=6, family="monospace")
    ax.text(TILE / 2, -10, note, color="#9aa3ad", fontsize=8.5,
            ha="center", family="monospace")


def slot(ax, pts, w=SLOT):
    pts = np.asarray(pts, float)
    ax.plot(pts[:, 0], pts[:, 1], color=VOID, lw=lw_mm(ax, w),
            solid_capstyle="round", solid_joinstyle="round", zorder=2)


def pad(ax, x, y, r=PAD_R):
    ax.add_patch(Circle((x, y), r, fc=VOID, zorder=2))


def diamond(ax, x, y, w=5.0, h=9.0):
    ax.add_patch(Polygon([(x, y - h / 2), (x + w / 2, y),
                          (x, y + h / 2), (x - w / 2, y)], fc=VOID, zorder=3))


def resistor(ax, x, y, ang=0.0, body=(12.0, 5.6), lead=4.0):
    """THT resistor as one compound cutout: pad-lead-body-lead-pad."""
    ca, sa = np.cos(ang), np.sin(ang)
    L = body[0] / 2 + lead

    def at(dx, dy=0.0):
        return x + dx * ca - dy * sa, y + dx * sa + dy * ca
    slot(ax, [at(-L - PAD_R * 0.4), at(L + PAD_R * 0.4)])
    pad(ax, *at(-L - PAD_R * 0.6))
    pad(ax, *at(L + PAD_R * 0.6))
    t = np.linspace(0, 2 * np.pi, 24)
    bx = body[0] / 2 * np.tanh(1.6 * np.cos(t))   # rounded-rect-ish
    by = body[1] / 2 * np.tanh(1.6 * np.sin(t))
    ax.add_patch(Polygon(np.c_[x + bx * ca - by * sa,
                               y + bx * sa + by * ca], fc=VOID, zorder=2))


def dogleg(x0, y0, y_jog, dx, y1):
    """Canonical fan move: vertical, 45-degree jog of dx, vertical.
    The diagonal advances toward y1, whichever direction that is."""
    d = 1.0 if y1 >= y0 else -1.0
    return [(x0, y0), (x0, y_jog), (x0 + dx, y_jog + abs(dx) * d), (x0 + dx, y1)]


def comb(ax, y, x0, x1, up=True, step=4.8, length=4.0):
    for x in np.arange(x0, x1, step):
        slot(ax, [(x, y), (x, y + (length if up else -length))])


def chip(ax, cx, cy, w=20.0, h=14.0, pins=4):
    """Solid island implied by pin combs top+bottom; punched diamond centre."""
    xs = np.linspace(cx - w / 2 + 3, cx + w / 2 - 3, pins)
    for x in xs:
        slot(ax, [(x, cy + h / 2), (x, cy + h / 2 + 4)])
        slot(ax, [(x, cy - h / 2), (x, cy - h / 2 - 4)])
    diamond(ax, cx, cy, 4.2, 7.4)
    return xs


# ---------------------------------------------------------------- tiles

def t_bus(ax):
    """Mirrored trace bus, diamonds at the jog corners, resistor punctuation."""
    for side in (0, 1):
        xs = 10 + np.arange(4) * PITCH
        for i, x0 in enumerate(xs):
            x = x0 if side == 0 else TILE - x0
            dx = (6 + 2 * i) * (1 if side == 0 else -1)
            p = dogleg(x, 8, 26 + 3 * i, dx, TILE - 8)
            slot(ax, p)
            pad(ax, x, 8)
            pad(ax, x + dx, TILE - 8)
    for y in (22, 52):
        diamond(ax, TILE / 2, y)
    resistor(ax, TILE / 2, 70, ang=np.pi / 2)


def t_chip(ax):
    """Chip anchor: pins fan to bottom pads, diamonds ride the open field."""
    xs = chip(ax, TILE / 2, TILE - 26)
    drops = [-16, -6, 6, 16]
    for x, dx in zip(xs, drops):
        p = dogleg(x, TILE - 36, TILE - 48, dx, 10)
        slot(ax, p)
        pad(ax, x + dx, 10)
    resistor(ax, 16, TILE - 14, ang=0)
    resistor(ax, TILE - 16, TILE - 14, ang=0)
    for x, y in [(14, 34), (TILE - 14, 34), (TILE / 2, 22)]:
        diamond(ax, x, y)
    comb(ax, 2.5, 14, TILE - 12, up=True)


def t_border(ax):
    """Overlay grammar: combs + corner pad clusters, harlequin interior."""
    comb(ax, 2.5, 20, TILE - 18, up=True)
    comb(ax, TILE - 2.5, 20, TILE - 18, up=False)
    for side in (0, 1):
        for cy in (14, TILE - 14):
            cx = 10 if side == 0 else TILE - 10
            sgn = 1 if side == 0 else -1
            pad(ax, cx, cy)
            slot(ax, [(cx, cy), (cx + sgn * 8, cy)])
            slot(ax, [(cx + sgn * 8, cy),
                      (cx + sgn * 13, cy + (5 if cy < TILE / 2 else -5))])
            pad(ax, cx + sgn * 13, cy + (5 if cy < TILE / 2 else -5))
    for j, y in enumerate(np.arange(24, TILE - 18, 13)):
        for x in np.arange(26 + (j % 2) * 9, TILE - 20, 18):
            diamond(ax, x, y, 6.0, 10.5)
    resistor(ax, TILE / 2, 12, ang=0)


def t_columns(ax):
    """Alternating columns: harlequin chains and 3-trace bundles."""
    cols = np.arange(11, TILE - 6, 16.5)
    for i, cx in enumerate(cols):
        if i % 2 == 0:
            for y in np.arange(12, TILE - 8, 13):
                if abs(cx - TILE / 2) < 1 and 28 < y < 60:
                    continue  # clearance for the centre resistor
                diamond(ax, cx, y, 5.6, 10.0)
        else:
            for k in (-1, 0, 1):
                x = cx + k * PITCH
                slot(ax, [(x, 8), (x, TILE - 8)])
                pad(ax, x, 8)
                pad(ax, x, TILE - 8)
    resistor(ax, TILE / 2, TILE / 2, ang=np.pi / 2)


TILES = [
    (t_bus, "1 trace bus", "mirrored bundles, 45 deg doglegs, pads both ends"),
    (t_chip, "2 chip anchor", "pin-comb chip island + punched diamond, fan to pads"),
    (t_border, "3 border + field", "edge combs & corner pads, harlequin interior - strongest core"),
    (t_columns, "4 harlequin bus", "diamond chains alternating with trace bundles"),
]

fig, axes = plt.subplots(2, 2, figsize=(13.2, 14.2))
fig.patch.set_facecolor(VOID)
fig.suptitle("wrist splint openwork - r2 circuit mode, harlequin accents\n"
             "(cutout grammar: slots 2.4 / webs 2.2 at 100% -> 1.8 / 1.7 at 77.6%; "
             "diamonds replace the house heart per darknetdoll)",
             color=PINK, fontsize=13.5, family="monospace", y=0.985)
fig.text(0.5, 0.008,
         "look only - ice blue stands in for the TPU colour; in black TPU this "
         "goes full CIRCUIT. velcro channels + housing mount zone stay solid",
         color="#9aa3ad", fontsize=10, ha="center", family="monospace")
fig.tight_layout(rect=(0, 0.02, 1, 0.94))
fig.canvas.draw()  # settle axes extents so lw_mm calibrates correctly
for (fn, title, note), ax in zip(TILES, axes.flat):
    ax.set_facecolor(VOID)
    tile_axes(ax, title, note)
    fn(ax)
out = __file__.replace("openwork_swatches_r2.py", "openwork-swatches-r2.png")
fig.savefig(out, dpi=FIG_DPI, facecolor=VOID)
print("wrote", out)

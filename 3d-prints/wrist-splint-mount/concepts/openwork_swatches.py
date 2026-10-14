"""Openwork pattern concepts for the wrist splint remix — r1 review sheet.

Each tile is an 80 x 80 mm swatch of plate-with-holes, drawn at 100% model
scale. Webs are kept >= 2.2 mm at 100% so they stay >= 1.7 mm after the
77.6% slicer scale (print floor 1.15 per the HEXCODE kit, plus margin for
TPU). Holes are capped around 12 mm so the splint keeps its strength.

Colors and the pixel heart map come from the HEXCODE palette
(hexcode_palette.py, sampled from shipped work — do not re-tune here).

Output: openwork-swatches-r1.png (this folder). Look only — nothing here
is placed on the real splint outline yet.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, RegularPolygon, FancyBboxPatch, Wedge

# HEXCODE FLORAL palette (stand-ins: plate = ice blue for translucent TPU)
VOID = "#141416"
PLATE = "#BAD2DE"
PINK = "#E49CB4"
GREEN = "#8FBE78"
WHITE = "#F2F2F2"

# House pixel heart, 7 x 6 — copied exactly from hexcode_palette.HEART
HEART = [
    ".XX.XX.",
    "XXXXXXX",
    "XXXXXXX",
    ".XXXXX.",
    "..XXX..",
    "...X...",
]

TILE = 80.0  # mm


def tile_axes(ax, title, note):
    ax.set_xlim(-4, TILE + 4)
    ax.set_ylim(-14, TILE + 4)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.add_patch(
        FancyBboxPatch((0, 0), TILE, TILE,
                       boxstyle="round,pad=0,rounding_size=4",
                       fc=PLATE, ec="none", zorder=1))
    ax.set_title(title, color=WHITE, fontsize=13, pad=6, family="monospace")
    ax.text(TILE / 2, -9, note, color="#9aa3ad", fontsize=8.5,
            ha="center", family="monospace")


def clip(ax, patch):
    patch.set_zorder(2)
    ax.add_patch(patch)


def inside(x, y, m=5.0):
    return m < x < TILE - m and m < y < TILE - m


# ---------------------------------------------------------------- patterns

def honeycomb(ax):
    """Reference: the original splint's pattern (approximate look)."""
    r, pitch = 4.6, 11.0
    for j, y in enumerate(np.arange(4, TILE, pitch * 0.87)):
        for x in np.arange(4 + (j % 2) * pitch / 2, TILE, pitch):
            if inside(x, y):
                clip(ax, RegularPolygon((x, y), 6, radius=r,
                                        orientation=np.pi / 6, fc=VOID))


def harlequin(ax):
    """Jester diamonds with dot holes at the nodes."""
    w, h = 7.0, 12.5
    gx, gy = w + 3.2, h + 3.2
    for j, y in enumerate(np.arange(6, TILE, gy)):
        for x in np.arange(6 + (j % 2) * gx / 2, TILE, gx):
            if inside(x, y, 7):
                clip(ax, Polygon([(x, y - h / 2), (x + w / 2, y),
                                  (x, y + h / 2), (x - w / 2, y)], fc=VOID))
    for j, y in enumerate(np.arange(6 + gy / 2, TILE - 4, gy)):
        for x in np.arange(6 + ((j + 1) % 2) * gx / 2, TILE - 4, gx):
            if inside(x, y):
                clip(ax, Circle((x, y), 1.6, fc=VOID))


def polka(ax):
    """Circus polka dots, three sizes, staggered."""
    rng = np.random.default_rng(4242)
    sizes = [5.2, 3.4, 2.0]
    pts = []
    for r in sizes:
        for _ in range(400):
            x, y = rng.uniform(6, TILE - 6, 2)
            if all(np.hypot(x - px, y - py) > r + pr + 2.6 for px, py, pr in pts):
                pts.append((x, y, r))
    for x, y, r in pts:
        clip(ax, Circle((x, y), r, fc=VOID))


def daisy(ax):
    """Six-petal daisy cutouts on the honeycomb's own grid."""
    pitch = 19.0
    for j, y in enumerate(np.arange(10, TILE, pitch * 0.87)):
        for x in np.arange(10 + (j % 2) * pitch / 2, TILE, pitch):
            if not inside(x, y, 8):
                continue
            clip(ax, Circle((x, y), 2.1, fc=VOID))
            for k in range(6):
                a = k * np.pi / 3
                px, py = x + 5.1 * np.cos(a), y + 5.1 * np.sin(a)
                t = np.linspace(0, 2 * np.pi, 24)
                ex = 2.9 * np.cos(t) * np.cos(a) - 1.75 * np.sin(t) * np.sin(a)
                ey = 2.9 * np.cos(t) * np.sin(a) + 1.75 * np.sin(t) * np.cos(a)
                clip(ax, Polygon(np.c_[px + ex, py + ey], fc=VOID))


def sakura_petal(x, y, a, L=6.2, W=4.6, notch=0.30):
    """Five-per-bloom notched petal polygon (notch at the outer tip)."""
    t_up = np.linspace(-np.pi / 2, np.pi / 2, 18)
    half = []
    for s in (1, -1):
        for t in t_up[:: s]:
            rr = 1 - notch * np.exp(-((t - 0) ** 2) / 0.035) * (t * s > 0)
            half.append((L / 2 * (np.sin(t) + 1) * rr, s * W / 2 * np.cos(t)))
    pts = np.array(half)
    # notch: pinch the outer tip into a V
    tip = pts[:, 0] > L * 0.82
    pts[tip, 1] *= 0.55
    ca, sa = np.cos(a), np.sin(a)
    return Polygon(np.c_[x + pts[:, 0] * ca - pts[:, 1] * sa,
                         y + pts[:, 0] * sa + pts[:, 1] * ca], fc=VOID)


def sakura(ax):
    """Sakura blooms (5 notched petal holes, solid open centre) + leaf holes."""
    rng = np.random.default_rng(90210)
    blooms = [(16, 62), (46, 70), (66, 44), (30, 36), (58, 16), (14, 14)]
    for x, y in blooms:
        rot = rng.uniform(0, 2 * np.pi)
        for k in range(5):
            a = rot + k * 2 * np.pi / 5
            clip(ax, sakura_petal(x + 2.6 * np.cos(a), y + 2.6 * np.sin(a), a))
    # leaf-shaped holes drifting between blooms
    for _ in range(10):
        x, y = rng.uniform(8, TILE - 8, 2)
        if any(np.hypot(x - bx, y - by) < 13 for bx, by in blooms):
            continue
        a = rng.uniform(0, np.pi)
        t = np.linspace(0, 2 * np.pi, 20)
        ex, ey = 3.4 * np.cos(t), 1.6 * np.sin(t)
        clip(ax, Polygon(np.c_[x + ex * np.cos(a) - ey * np.sin(a),
                               y + ex * np.sin(a) + ey * np.cos(a)], fc=VOID))


def vine_web(ax):
    """Inverted: the WEB is the vine lattice; air is everything between.

    Drawn as void field + plate-colored strands (few wide slow curves,
    per the FLORAL rule) + solid border ring.
    """
    frame = FancyBboxPatch((3, 3), TILE - 6, TILE - 6,
                           boxstyle="round,pad=0,rounding_size=3",
                           fc=VOID, ec=PLATE, lw=5, zorder=2)
    ax.add_patch(frame)
    rng = np.random.default_rng(31337)
    lines = []
    for i in range(6):
        x = rng.uniform(4, TILE * 0.45) if i % 2 else rng.uniform(TILE * 0.55, TILE - 4)
        y, a = -6.0, np.pi / 2 + rng.normal(0, 0.25)
        pts = [(x, y)]
        while y < TILE + 6:
            a = np.pi / 2 + (a - np.pi / 2) * 0.9 + rng.normal(0, 0.09)
            x, y = x + 5.0 * np.cos(a), y + abs(5.0 * np.sin(a))
            pts.append((x, y))
        pts = np.array(pts)
        lines.append(ax.plot(pts[:, 0], pts[:, 1], color=PLATE, lw=7.5,
                             solid_capstyle="round", zorder=3)[0])
        # cross ties: short branches that land on a neighbour strand
        for px, py in pts[2::3]:
            if inside(px, py, 9):
                b = rng.uniform(-0.5, 0.5) + (0 if rng.random() < 0.5 else np.pi)
                lines.append(ax.plot([px, px + 14 * np.cos(b)],
                                     [py, py + 14 * np.sin(b)],
                                     color=PLATE, lw=5.0,
                                     solid_capstyle="round", zorder=3)[0])
    for ln in lines:
        ln.set_clip_path(frame)


def scallop_lace(ax):
    """Lace bands: scallop arcs, picot dots, teardrops — the cuff look."""
    for row, y in enumerate(np.arange(8, TILE - 4, 15)):
        if row % 2 == 0:
            for x in np.arange(10, TILE - 6, 11):
                clip(ax, Wedge((x, y), 4.4, 180, 360, fc=VOID))
                clip(ax, Circle((x + 5.5, y + 2.6), 1.3, fc=VOID))
        else:
            for x in np.arange(7, TILE - 6, 8):
                t = np.linspace(0, 2 * np.pi, 20)
                clip(ax, Polygon(np.c_[x + 1.9 * np.sin(t) * (1 - np.cos(t)) * 0.8,
                                       y + 3.4 * np.cos(t)], fc=VOID))


def hearts(ax):
    """House pixel hearts as cutouts, two cell sizes, staggered."""
    cells = [(r, c) for r, row in enumerate(HEART)
             for c, ch in enumerate(row) if ch == "X"]

    def heart_at(x0, y0, cell):
        for r, c in cells:
            ax.add_patch(plt.Rectangle((x0 + c * cell, y0 + (5 - r) * cell),
                                       cell * 1.01, cell * 1.01, fc=VOID, zorder=2))

    big, small = 2.2, 1.5  # only big survives heart_cell_min 1.40 at 77.6%
    for j, y in enumerate(np.arange(5, TILE - 13, 16.5)):
        for i, x in enumerate(np.arange(5 + (j % 2) * 9.5, TILE - 15, 19)):
            heart_at(x, y, big if (i + j) % 2 == 0 else small)


# ---------------------------------------------------------------- sheet

TILES = [
    (honeycomb, "0 honeycomb (as-is)", "the original splint pattern, for reference"),
    (harlequin, "1 harlequin", "jester diamonds + node dots - the clown pick"),
    (polka, "2 polka dot", "circus dots, 3 sizes - easiest, drains best"),
    (hearts, "3 pixel hearts", "house 7x6 heart as cutout - cell 2.2 only (1.5 dies at 77.6%)"),
    (daisy, "4 daisy", "6-petal blooms on the honeycomb grid - keeps its density"),
    (sakura, "5 sakura + leaves", "FLORAL blossoms (notched petals, open centre) + leaf holes"),
    (vine_web, "6 vine web", "web IS the vine lattice - organic, strongest look-risk"),
    (scallop_lace, "7 scallop lace", "cuff-lace bands - rhymes with the cuff-ruffle"),
]

fig, axes = plt.subplots(2, 4, figsize=(19, 10.6))
fig.patch.set_facecolor(VOID)
for (fn, title, note), ax in zip(TILES, axes.flat):
    ax.set_facecolor(VOID)
    tile_axes(ax, title, note)
    fn(ax)
fig.suptitle("wrist splint openwork - pattern concepts r1  "
             "(80 mm swatches at 100%; webs sized to survive 77.6% scale)",
             color=PINK, fontsize=15, family="monospace", y=0.985)
fig.text(0.5, 0.012,
         "look only - nothing is placed on the real splint outline; velcro channels "
         "and the housing mount zone stay solid in every option",
         color="#9aa3ad", fontsize=10, ha="center", family="monospace")
fig.tight_layout(rect=(0, 0.02, 1, 0.96))
out = __file__.replace("openwork_swatches.py", "openwork-swatches-r1.png")
fig.savefig(out, dpi=140, facecolor=VOID)
print("wrote", out)

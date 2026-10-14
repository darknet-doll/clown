"""Extract the wrist-splint's true 2D silhouette from the reference STL.

The splint prints flat (z 0 -> 3.5), so a single cross-section at mid
thickness carries the whole plan view: outer boundary + every hole
(honeycomb cells, thumb opening, velcro channels if they pierce z=1.75).

Output: splint-outline.json {loops: [{pts: [[x,y],...], area: signed}]}
plus a quick-look PNG. Loops are closed; the largest |area| is the outer
boundary. Nothing is transformed — model units (mm at 100%), model frame.
"""

import json
import struct

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

STL = "../reference/wrist-splint-custom-moldable-model_files/wrist-splint.stl"
Z = 1.75


def load_tris(path):
    with open(path, "rb") as f:
        f.read(80)
        (n,) = struct.unpack("<I", f.read(4))
        raw = np.frombuffer(f.read(n * 50), dtype=np.uint8).reshape(n, 50)
    return raw[:, 12:48].copy().view("<f4").reshape(n, 3, 3).astype(np.float64)


def plane_segments(tris, z):
    """Intersection segments of each triangle with plane z=const."""
    segs = []
    d = tris[:, :, 2] - z
    cross = (np.sign(d).min(axis=1) < 0) & (np.sign(d).max(axis=1) > 0)
    for tri, dd in zip(tris[cross], d[cross]):
        pts = []
        for i in range(3):
            a, b = tri[i], tri[(i + 1) % 3]
            da, db = dd[i], dd[(i + 1) % 3]
            if da * db < 0:
                t = da / (da - db)
                pts.append((a + t * (b - a))[:2])
        if len(pts) == 2:
            segs.append((pts[0], pts[1]))
    return segs


def chain(segs, tol=0.015):
    """Chain segments into closed loops by endpoint proximity."""
    key = lambda p: (round(p[0] / tol), round(p[1] / tol))
    adj = {}
    for a, b in segs:
        adj.setdefault(key(a), []).append((tuple(a), tuple(b)))
        adj.setdefault(key(b), []).append((tuple(b), tuple(a)))
    used, loops = set(), []
    for a, b in segs:
        sid = (tuple(a), tuple(b))
        if sid in used or (tuple(b), tuple(a)) in used:
            continue
        loop = [tuple(a), tuple(b)]
        used.add(sid)
        while True:
            k = key(loop[-1])
            nxt = None
            for frm, to in adj.get(k, []):
                pid = (frm, to)
                if pid in used or (to, frm) in used:
                    continue
                nxt = (frm, to)
                break
            if nxt is None:
                break
            used.add(nxt)
            loop.append(nxt[1])
            if key(loop[-1]) == key(loop[0]):
                break
        if len(loop) > 3 and key(loop[-1]) == key(loop[0]):
            loops.append(np.array(loop[:-1]))
    return loops


def signed_area(p):
    x, y = p[:, 0], p[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


tris = load_tris(STL)
segs = plane_segments(tris, Z)
loops = chain(segs)
loops.sort(key=lambda p: -abs(signed_area(p)))
print(f"{len(segs)} segments -> {len(loops)} closed loops")
areas = [signed_area(p) for p in loops]
print("largest |areas|:", [round(abs(a)) for a in areas[:8]])

out = {"z": Z, "loops": [
    {"area": round(a, 2), "pts": np.round(p, 3).tolist()}
    for p, a in zip(loops, areas)]}
with open("splint-outline.json", "w") as f:
    json.dump(out, f)
print("wrote splint-outline.json")

fig, ax = plt.subplots(figsize=(14, 12))
fig.patch.set_facecolor("#141416")
ax.set_facecolor("#141416")
ax.fill(loops[0][:, 0], loops[0][:, 1], color="#BAD2DE", zorder=1)
for p in loops[1:]:
    ax.fill(p[:, 0], p[:, 1], color="#141416", zorder=2)
ax.set_aspect("equal")
ax.tick_params(colors="#9aa3ad", labelsize=8)
ax.set_title(f"wrist-splint.stl plan view at z={Z} (model mm, 100%)",
             color="#F2F2F2", family="monospace")
for s in ax.spines.values():
    s.set_color("#444")
ax.grid(color="#2a2a2e", lw=0.5)
fig.savefig("splint-plan.png", dpi=110, facecolor="#141416",
            bbox_inches="tight")
print("wrote splint-plan.png")

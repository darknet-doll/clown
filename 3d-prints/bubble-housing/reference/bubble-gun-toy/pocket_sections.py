# Gun blower pocket wall as r(angle, z): rays from the barrel axis every 1 deg, every 0.5 mm.
# Frame: z = barrel axis, z=-5 muzzle face (= ring face), +y = down, split plane x=0.
# Angle: 0 = +x (02 half side), 90 = +y (bottom), 180 = -x (01 half), 270 = -y (top).
# Run from this folder: python3 pocket_sections.py -> pocket-wall.npz + pocket-map.png (local only)
import trimesh, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
m = trimesh.util.concatenate([trimesh.load('stl/01_Body_REV1.stl'), trimesh.load('stl/02_Body_REV1.stl')])
ang = np.radians(np.arange(0, 360, 1.0)); zs = np.arange(-4.75, 46.6, 0.5)
R = np.full((len(zs), len(ang)), np.nan)
for i, z in enumerate(zs):
    O = np.c_[np.zeros(len(ang)), np.zeros(len(ang)), np.full(len(ang), z)]
    D = np.c_[np.cos(ang), np.sin(ang), np.zeros(len(ang))]
    loc, ri, _ = m.ray.intersects_location(O, D, multiple_hits=False)
    R[i, ri] = np.hypot(loc[:, 0], loc[:, 1])
np.savez('pocket-wall.npz', R=R, zs=zs, ang=np.degrees(ang))
fig, ax = plt.subplots(figsize=(14, 6))
im = ax.imshow(np.nan_to_num(R, nan=30), origin='lower', aspect='auto', cmap='viridis', vmin=8, vmax=24,
               extent=[0, 360, zs[0], zs[-1]])
ax.set_xticks(range(0, 361, 30)); ax.set_xlabel('angle (deg): 0 +x side, 90 bottom, 180 -x side, 270 top')
ax.set_ylabel('z (mm), -5 = muzzle face'); plt.colorbar(im, label='pocket wall radius (mm); yellow = no wall (opening)')
ax.set_title('Gun blower pocket, unrolled'); plt.tight_layout(); plt.savefig('pocket-map.png', dpi=90)

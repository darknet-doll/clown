# Cross-sections of the gun pocket from pocket-wall.npz (run pocket_sections.py first).
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = np.load('pocket-wall.npz'); R, zs, ang = d['R'], d['zs'], np.radians(d['ang'])
pick = [0.25, 12.25, 25.25, 33.25, 38.25, 44.25]
fig, axs = plt.subplots(1, 6, figsize=(21, 4.2))
for ax, z in zip(axs, pick):
    i = int(np.argmin(abs(zs - z))); r = np.nan_to_num(R[i], nan=24.5); r = np.minimum(r, 24.5)
    x, y = r*np.cos(ang), r*np.sin(ang)
    ax.fill(np.r_[x, x[0]], np.r_[y, y[0]], color='#ffd8a8', ec='#d9480f', lw=1)
    t = np.linspace(0, 2*np.pi, 200)
    ax.plot(18.75*np.cos(t), 18.75*np.sin(t), '--', color='#1c7ed6', lw=0.8)
    ax.set_xlim(-25, 25); ax.set_ylim(25, -25); ax.set_aspect('equal'); ax.grid(alpha=.3)
    ax.axhline(0, color='#999', lw=.5); ax.axvline(0, color='#999', lw=.5)
    ax.set_title(f'{zs[i]+5:.1f} mm behind muzzle face', fontsize=10)
    ax.text(-24, -21, 'top', fontsize=8); ax.text(14, -21, '02 half +x', fontsize=8); ax.text(-24, 23, '01 half -x', fontsize=8)
fig.suptitle('Gun pocket free space (orange) looking from the muzzle. Blue dashed = ring 37.5. Spikes to the edge = openings', fontsize=11)
plt.tight_layout(); plt.savefig('pocket-slices.png', dpi=80)
# envelope numbers behind z=29 (where the rear blocks start)
for z in (30.25, 35.25, 40.25, 45.25):
    i = int(np.argmin(abs(zs - z))); r = R[i]
    x, y = r*np.cos(ang), r*np.sin(ang)
    inner = r < 17
    print(f'{zs[i]+5:5.1f} behind face: blocks at r<17 over angles',
          [int(a) for a in np.degrees(ang)[inner][[0, -1]]] if inner.any() else '-',
          f' min r {np.nanmin(r):.1f}', f' free x {np.nanmin(x):.1f}..{np.nanmax(x):.1f} y {np.nanmin(y):.1f}..{np.nanmax(y):.1f}')

# Reference figure of the gun pocket, rotated so the feed nipple is at 12 o'clock and
# measured from the ring face (= gun muzzle face). Needs pocket-wall.npz. Local only.
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = np.load('pocket-wall.npz'); R, zs, ang = d['R'], d['zs'] + 5, np.radians(d['ang'])
NIP = np.radians(314)                       # nipple groove centre in gun angles
clock = ang - NIP                           # 0 = nipple, + = clockwise seen from the front
fig = plt.figure(figsize=(15, 9.5))
# --- top: features along the head ---------------------------------------------
ax = fig.add_axes([0.05, 0.60, 0.9, 0.33])
rows = [('Front lip  Ø37.8 (holds the ring)', 0, 13.55, '#4dabf7'),
        ('Main bore  Ø39.4 (body)', 13.55, 51.6, '#74c0fc'),
        ('Feed-nipple groove, +3.0 deep, ~6 wide, at 12:00', 1.3, 22.0, '#f783ac'),
        ('Air slots on top: 6 per row, 2 wide, 5 pitch', 8.0, 35.0, '#69db7c'),
        ('Top recess, +3.0 deep, ~120° wide', 21.75, 47.25, '#ffd43b'),
        ('Side slots, 3.8 wide, through the wall, 1:30 and 7:30', 14.25, 44.75, '#ff922b'),
        ('Rear blocks: motor end sits off-centre (see sections)', 33.5, 51.6, '#adb5bd'),
        ('Screw holes: Ø2.5 at 9.9 (top) and 13.5 (bottom); Ø1.8 x 8.6 at 22.5 and 47.4 (top)', 9.9, 47.4, '#868e96')]
for k, (label, a, b, c) in enumerate(rows):
    y = len(rows) - k
    ax.barh(y, b - a, left=a, height=0.62, color=c, edgecolor='#495057')
    ax.text(52.6, y, label, va='center', fontsize=10)
for zf in (0, 13.55, 51.6, 52.01):
    ax.axvline(zf, color='#495057', lw=0.8, ls=':')
ax.text(0, len(rows) + 0.9, 'ring face', fontsize=9, ha='center')
ax.text(51.6, len(rows) + 0.9, 'back wall 51.6\n(head is 52.01: 0.4 proud)', fontsize=9, ha='center')
ax.set_xlim(-2, 110); ax.set_ylim(0.3, len(rows) + 1.8); ax.set_yticks([])
ax.set_xticks(range(0, 56, 5)); ax.set_xlabel('mm behind the ring face')
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.set_title('Gun pocket features to borrow, along the head', loc='left', fontsize=13, fontweight='bold')
# --- bottom: three sections, nipple up -------------------------------------------
for k, zf in enumerate((5.25, 30.25, 45.25)):
    ax = fig.add_axes([0.05 + k * 0.31, 0.04, 0.28, 0.48])
    i = int(np.argmin(abs(zs - zf))); r = np.minimum(np.nan_to_num(R[i], nan=25), 25)
    x, y = r * np.sin(clock), r * np.cos(clock)          # clockwise from 12:00
    ax.fill(np.r_[x, x[0]], np.r_[y, y[0]], color='#ffd8a8', ec='#d9480f', lw=1.2)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(18.75 * np.cos(t), 18.75 * np.sin(t), '--', color='#1c7ed6', lw=0.9)
    ax.set_xlim(-26, 26); ax.set_ylim(-26, 26); ax.set_aspect('equal'); ax.grid(alpha=.25)
    ax.set_title(f'{zs[i]:.0f} mm behind the ring face', fontsize=11)
    ax.text(0, 23.5, 'nipple', ha='center', fontsize=9)
fig.text(0.05, 0.535, 'Looking at the ring face, nipple at 12:00. Orange = free space in the gun pocket, '
         'spikes to the edge = openings. Blue dashed = ring 37.5.', fontsize=10)
plt.savefig('gun-borrow-reference.png', dpi=110)

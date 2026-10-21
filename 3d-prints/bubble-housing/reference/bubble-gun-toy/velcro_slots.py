# Velcro strap slots for the gun front housing (2026-10-21, darknetdoll's ask).
#
# The cut halves (cut_front_housing.py) each have one 3.8 x 30.5 through-slot on the
# outer flat: 12:00 on the lid (02), 6:00 on the cradle (01). A single slot gives the
# strap nothing to wrap round. This replaces it with two strap slots and a bar
# between them: the strap goes down one slot, under the bar, and up the other.
#
#   - Old slot filled: x -1.95 -> 1.95, z 9.5 -> 40, from the bore (r 19.7) out to
#     the raised rim (|y| 22.4). The filled rim becomes the bar.
#   - Strap runs round the wrist (along x at these faces), so its 11 width lies
#     along the barrel axis (z). Each slot: 13 along z (11 strap + 2) x 2.5 across
#     (lets the strap double back, 2 x 1.1), same as the bubble-housing strap opening.
#   - Bar: 4 wide (x -2 -> 2). Slots at x 2 -> 4.5 and -4.5 -> -2
#   - Slot z 15 -> 28 (assembly frame) = 20 -> 33 behind the ring face. Stops short
#     of the cradle's internal ribs, which start at z 29.
#
# The strap passes under the bar inside the bore, between the bar and the blower
# head. Bore r 19.7; the head's body OD there is not measured yet (M2).
#
# Outputs stay in front-housing/ (gitignored, derived from the no-redistribution model).

import os

import numpy as np
import trimesh

Z_CUT = 56.0
OUT = 'front-housing'
ROT = trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 0, 1])
BED = {'bottom-01': trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]),
       'top-02': trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])}
SIGN = {'bottom-01': 1, 'top-02': -1}      # bottom half is +y, top half is -y

BORE_R = 19.7
FILL_X, FILL_Z, RIM_Y = 1.95, (9.5, 40.0), 22.4
BAR, SLOT_W, SLOT_Z = 4.0, 2.5, (15.0, 28.0)


def box(x0, x1, y0, y1, z0, z1):
    b = trimesh.creation.box(extents=[x1 - x0, y1 - y0, z1 - z0])
    b.apply_translation([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return b


def flip(m, s):
    """Mirror a +y feature onto the -y half."""
    if s < 0:
        m = m.copy()
        m.apply_transform(np.diag([1, -1, 1, 1]))
    return m


bore = trimesh.creation.cylinder(radius=BORE_R, height=60, sections=180)
bore.apply_translation([0, 0, (FILL_Z[0] + FILL_Z[1]) / 2])

halves = {}
for src, name in [('stl/01_Body_REV1.stl', 'bottom-01'), ('stl/02_Body_REV1.stl', 'top-02')]:
    s = SIGN[name]
    m = trimesh.load(src).slice_plane(plane_origin=[0, 0, Z_CUT], plane_normal=[0, 0, -1], cap=True)
    m.apply_transform(ROT)

    fill = box(-FILL_X, FILL_X, 15.0, RIM_Y, *FILL_Z).difference(bore)
    m = m.union(flip(fill, s))
    for x0 in (BAR / 2, -BAR / 2 - SLOT_W):
        m = m.difference(flip(box(x0, x0 + SLOT_W, 15.0, 26.0, *SLOT_Z), s))

    halves[name] = m
    out = m.copy()
    out.apply_transform(BED[name])
    out.apply_translation(-out.bounds[0])
    path = f'{OUT}/front-housing-velcro-{name}.stl'
    out.export(path)
    print(f'{path}: watertight={out.is_watertight} '
          f'bounds={np.round(out.bounds, 2).tolist()} vol={out.volume / 1000:.1f} cm3')

# --- view: both faces close up, plus a section showing the strap path ----------------
import pyvista as pv

pv.OFF_SCREEN = True
COL = {'bottom-01': '#a98be8', 'top-02': '#e9edf2'}
STRAP = '#f2a65a'


def strap(s):
    """11-wide strap threaded down one slot, under the bar, up the other (1.1 thick)."""
    t, yo, yi = 1.1, 21.5, BORE_R
    xa, xb = BAR / 2 + SLOT_W / 2, -(BAR / 2 + SLOT_W / 2)
    zc = sum(SLOT_Z) / 2
    parts = [box(xa, 16, yo, yo + t, zc - 5.5, zc + 5.5),                  # outside, right
             box(xa - t / 2, xa + t / 2, yi - t, yo + t, zc - 5.5, zc + 5.5),  # down slot
             box(xb, xa, yi - t, yi, zc - 5.5, zc + 5.5),                  # under the bar
             box(xb - t / 2, xb + t / 2, yi - t, yo + t, zc - 5.5, zc + 5.5),  # up slot
             box(-16, xb, yo, yo + t, zc - 5.5, zc + 5.5)]                 # outside, left
    return flip(trimesh.util.concatenate(parts), s)


def panel(p, meshes, pos, focal, up, zoom, title, with_strap=False, clip_z=None):
    p.set_background('white')
    for name, m in meshes.items():
        g = pv.wrap(m)
        if clip_z is not None:
            g = g.clip(normal=(0, 0, -1), origin=(0, 0, clip_z))
        p.add_mesh(g, color=COL[name], smooth_shading=False, show_edges=False)
        if with_strap:
            st = pv.wrap(strap(SIGN[name]))
            if clip_z is not None:
                st = st.clip(normal=(0, 0, -1), origin=(0, 0, clip_z))
            p.add_mesh(st, color=STRAP)
    p.camera_position = [pos, focal, up]
    p.enable_parallel_projection()
    p.camera.zoom(zoom)
    p.add_text(title, font_size=11, color='black')


p = pv.Plotter(off_screen=True, shape=(2, 2), window_size=(1800, 1500), border=False)
zc = sum(SLOT_Z) / 2

p.subplot(0, 0)
panel(p, {'top-02': halves['top-02']}, (0, -300, 25), (0, 0, 25), (0, 0, -1), 1.5,
      'Lid (top, 12:00): two strap slots + bar\nring face is at the top of the image')
p.subplot(0, 1)
panel(p, {'bottom-01': halves['bottom-01']}, (0, 300, 25), (0, 0, 25), (0, 0, -1), 1.5,
      'Cradle (bottom, 6:00): same slots\nring face is at the top of the image')
p.subplot(1, 0)
panel(p, halves, (-170, -170, -200), (0, 0, 25), (0, -1, 0), 1.25,
      'Three-quarter, strap shown in orange', with_strap=True)
p.subplot(1, 1)
panel(p, halves, (0, 0, -300), (0, 0, zc), (0, -1, 0), 1.6,
      f'Section through the slots ({zc + 5:.1f} behind ring face)\n'
      'strap: down one slot, under the bar, up the other', with_strap=True, clip_z=zc)

p.screenshot(f'{OUT}/velcro-slots.png')
p.close()
print(f'{OUT}/velcro-slots.png')

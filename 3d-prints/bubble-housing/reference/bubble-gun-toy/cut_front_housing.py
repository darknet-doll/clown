# Cut the gun's front housing (the blower pocket section) out of 01/02_Body so it
# can be printed on its own, re-clocked for the wrist-splint mount (2026-10-13):
#
#   - Cut plane: z = 56.0 in the assembly frame (= 61.0 behind the ring face), the
#     front face of the bottle-bay bottom opening, measured by ray scan (the wall
#     face returns z = 56.000 exactly). Everything behind it is dropped; the cap
#     closes the cut, so the old hatch front wall becomes the new back wall.
#   - Rotate -90 deg about the barrel (z) axis: +x -> -y. Looking at the ring face
#     (muzzle view, -y up, +x viewer-left), that turns the part clockwise 90 deg:
#       * clamshell split: x = 0 (seam at 12:00/6:00) -> y = 0 (seam at 3:00/9:00)
#       * front screw holes: 12:00 (y -28.1, z 4.9) -> 3:00; 6:00 (y +25.9, z 8.5) -> 9:00
#       * 02_Body (x > 0) becomes the TOP half (lid), 01_Body the BOTTOM (cradle)
#       * feed-nipple groove: 44 deg off top toward 02 -> ~46 deg off top, stays in
#         the top half. The other direction would have buried it against the hand.
#   - Exports are print-oriented: each half with its split face on the bed, +z up.
#
# Outputs stay in front-housing/ (gitignored): they are derived from the MakerWorld
# model, which must not be redistributed.

import numpy as np
import trimesh

Z_CUT = 56.0            # assembly frame; muzzle face is z = -5
OUT = 'front-housing'

ROT = trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 0, 1])  # +x -> -y

# print orientation: split face (y = 0 after ROT) on the bed, part growing +z
BED_BOTTOM = trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0])   # y -> z (01, y >= 0)
BED_TOP = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])     # -y -> z (02, y <= 0)

import os
os.makedirs(OUT, exist_ok=True)

halves = {}
for src, name, bed in [('stl/01_Body_REV1.stl', 'bottom-01', BED_BOTTOM),
                       ('stl/02_Body_REV1.stl', 'top-02', BED_TOP)]:
    m = trimesh.load(src)
    cut = m.slice_plane(plane_origin=[0, 0, Z_CUT], plane_normal=[0, 0, -1], cap=True)
    cut.apply_transform(ROT)
    assembly = cut.copy()                      # rotated assembly frame, kept for renders
    cut.apply_transform(bed)
    cut.apply_translation(-cut.bounds[0])      # bed corner at origin, split face at z = 0
    path = f'{OUT}/front-housing-{name}.stl'
    cut.export(path)
    halves[name] = assembly
    print(f'{path}: watertight={cut.is_watertight} '
          f'bounds={np.round(cut.bounds, 2).tolist()} vol={cut.volume / 1000:.1f} cm3')

# --- check views (muzzle view clock: screws must sit at 3:00 and 9:00) ---------------
try:
    import pyvista as pv
except ImportError:
    raise SystemExit('pyvista not found; STLs exported, views skipped')

pv.OFF_SCREEN = True
STY = {'bottom-01': dict(color='#a98be8', smooth_shading=True),
       'top-02': dict(color='#e9edf2', smooth_shading=True)}


def shot(fn, pos, focal=(0, 0, 25), up=(0, -1, 0), zoom=1.0, flat=True, explode=0.0):
    p = pv.Plotter(off_screen=True, window_size=(1400, 1050))
    p.set_background('white')
    for name, m in halves.items():
        g = m.copy()
        if explode:
            g.apply_translation([0, -explode if name == 'top-02' else explode, 0])
        p.add_mesh(pv.wrap(g), **STY[name])
    p.camera_position = [pos, focal, up]
    if flat:
        p.enable_parallel_projection()
    p.camera.zoom(zoom)
    p.enable_anti_aliasing('ssaa')
    p.screenshot(f'{OUT}/{fn}')
    p.close()
    print(f'{OUT}/{fn}')


shot('view-front.png', (0, 0, -300), zoom=1.6)                      # muzzle view, up = gun top
shot('view-back.png', (0, 0, 300), zoom=1.6)                        # cut face
shot('view-top.png', (0, -300, 25), up=(0, 0, -1), zoom=1.5)        # lid half from above
shot('view-three-quarter.png', (-170, -170, -200), zoom=1.3, flat=False)
shot('view-exploded.png', (-170, -170, -200), zoom=1.1, flat=False, explode=14)

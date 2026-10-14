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
# Also exports a fit COUPON (adopted as the new housing direction, 2026-10-13):
# the front 30 mm of both halves on one plate. That keeps the lip bore, the 0.8
# shoulder step at 13.55, the full nipple groove (1.3 -> 22), the front screw
# bosses and the start of the side slots. The cap only closes the wall
# cross-section, so the bore stays open and the head passes through until its
# ring seats on the step.
#
# Outputs stay in front-housing/ (gitignored): they are derived from the MakerWorld
# model, which must not be redistributed.

import os

import numpy as np
import trimesh

Z_CUT = 56.0            # assembly frame; muzzle face is z = -5
Z_COUPON = 25.0         # front 30 mm behind the ring face
COUPON_GAP = 10.0       # between the two halves on the plate
OUT = 'front-housing'

ROT = trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 0, 1])  # +x -> -y

# print orientation: split face (y = 0 after ROT) on the bed, part growing +z
BED = {'bottom-01': trimesh.transformations.rotation_matrix(np.pi / 2, [1, 0, 0]),   # y -> z
       'top-02': trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])}     # -y -> z

os.makedirs(OUT, exist_ok=True)


def cut_half(src, name, z_cut):
    """Front section of one body half: (assembly-frame mesh, bed-oriented mesh)."""
    m = trimesh.load(src)
    cut = m.slice_plane(plane_origin=[0, 0, z_cut], plane_normal=[0, 0, -1], cap=True)
    cut.apply_transform(ROT)
    assembly = cut.copy()
    cut.apply_transform(BED[name])
    cut.apply_translation(-cut.bounds[0])      # bed corner at origin, split face at z = 0
    return assembly, cut


SRC = [('stl/01_Body_REV1.stl', 'bottom-01'), ('stl/02_Body_REV1.stl', 'top-02')]

halves = {}
for src, name in SRC:
    assembly, cut = cut_half(src, name, Z_CUT)
    halves[name] = assembly
    path = f'{OUT}/front-housing-{name}.stl'
    cut.export(path)
    print(f'{path}: watertight={cut.is_watertight} '
          f'bounds={np.round(cut.bounds, 2).tolist()} vol={cut.volume / 1000:.1f} cm3')

# --- coupon: both shortened halves on one plate --------------------------------------
coupon_assembly = {}
plate = []
x_off = 0.0
for src, name in SRC:
    assembly, cut = cut_half(src, name, Z_COUPON)
    coupon_assembly[name] = assembly
    cut.apply_translation([x_off, 0, 0])
    plate.append(cut)
    x_off = cut.bounds[1][0] + COUPON_GAP
coupon = trimesh.util.concatenate(plate)
coupon.export(f'{OUT}/front-housing-coupon.stl')
print(f'{OUT}/front-housing-coupon.stl: '
      f'watertight={all(p.is_watertight for p in plate)} '
      f'bounds={np.round(coupon.bounds, 2).tolist()} vol={coupon.volume / 1000:.1f} cm3')

# --- check views (muzzle view clock: screws must sit at 3:00 and 9:00) ---------------
try:
    import pyvista as pv
except ImportError:
    raise SystemExit('pyvista not found; STLs exported, views skipped')

pv.OFF_SCREEN = True
STY = {'bottom-01': dict(color='#a98be8', smooth_shading=True),
       'top-02': dict(color='#e9edf2', smooth_shading=True)}


def shot(fn, meshes, pos, focal=(0, 0, 25), up=(0, -1, 0), zoom=1.0, flat=True, explode=0.0):
    p = pv.Plotter(off_screen=True, window_size=(1400, 1050))
    p.set_background('white')
    for name, m in meshes.items():
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


shot('view-front.png', halves, (0, 0, -300), zoom=1.6)                      # muzzle view
shot('view-back.png', halves, (0, 0, 300), zoom=1.6)                        # cut face
shot('view-top.png', halves, (0, -300, 25), up=(0, 0, -1), zoom=1.5)        # lid from above
shot('view-three-quarter.png', halves, (-170, -170, -200), zoom=1.3, flat=False)
shot('view-exploded.png', halves, (-170, -170, -200), zoom=1.1, flat=False, explode=14)
shot('view-coupon.png', coupon_assembly, (-170, -170, -200), focal=(0, 0, 10),
     zoom=1.3, flat=False, explode=14)

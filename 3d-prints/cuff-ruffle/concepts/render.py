# Renders r2-*.png next to this file. Run: python3 3d-prints/cuff-ruffle/concepts/render.py
import pathlib, sys
import numpy as np, pyvista as pv
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from model import scene
pv.OFF_SCREEN = True
HERE = pathlib.Path(__file__).resolve().parent

STY = dict(hand=dict(color='#f1d3c2', opacity=0.5, smooth_shading=True),
           straps=dict(color='#2b2b2b', opacity=0.85, smooth_shading=True),
           mount=dict(color='#b9a3ec', smooth_shading=False),
           bracket=dict(color='#e9edf2', smooth_shading=False),
           drum=dict(color='#f7f8fa', smooth_shading=True),
           tab=dict(color='#9d86d6', smooth_shading=False),
           ruffle=dict(color='#fbfaf7', smooth_shading=True, specular=0.35, opacity=0.97))

LABELS = [((-15, -48, 25), 'one big printed ruffle - openwork is the lace AND the drains'),
          ((8, 36, 16), 'hides the tongue + strap, hem still stops before the shroud'),
          ((-8, 0, -22), 'tab under the tongue, held by the tongue strap'),
          ((-50, -24, -8), 'fabric band + upper ruffle take over here')]

def shot(fn, pos, focal=(0, 0, 8), zoom=1.0, flat=False, labels=False):
    p = pv.Plotter(off_screen=True, window_size=(1400, 950)); p.set_background('white')
    for k in ('hand', 'straps', 'mount', 'bracket', 'drum', 'tab', 'ruffle'):
        p.add_mesh(pv.wrap(scene[k]).compute_normals(feature_angle=35, split_vertices=True,
                   auto_orient_normals=False), **STY[k], backface_params=None)
    if labels:
        pts = np.array([l[0] for l in LABELS], float)
        p.add_point_labels(pts, [l[1] for l in LABELS], font_size=19, point_size=9,
                           point_color='#333333', shape_opacity=0.85, always_visible=True,
                           text_color='black', shape_color='white')
    p.camera_position = [pos, focal, (0, 0, 1)]
    if flat: p.enable_parallel_projection()
    p.camera.zoom(zoom); p.enable_anti_aliasing('ssaa')
    p.screenshot(str(HERE / fn)); p.close()

shot('r2-three-quarter.png', (-150, -210, 150), zoom=1.35, labels=True)
shot('r2-side.png', (-5, -330, 10), focal=(-5, 0, 10), zoom=1.8, flat=True)
shot('r2-top.png', (-5, 0, 330), focal=(-5, 0, 0), zoom=1.7, flat=True)
shot('r2-from-wrist.png', (-300, -60, 70), focal=(-10, 0, 5), zoom=1.5)

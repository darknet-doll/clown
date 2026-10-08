import sys; sys.path.insert(0, 'concept')
import numpy as np, pyvista as pv
from model_whimsy import scene
STY = dict(hand=dict(color='#f1d3c2', opacity=0.5, smooth_shading=True),
           straps=dict(color='#2b2b2b', opacity=0.85, smooth_shading=True),
           drum=dict(color='#f7f8fa', smooth_shading=True),
           base=dict(color='#b9a3ec'),
           shell=dict(color='#fbfaf7', smooth_shading=True, specular=0.3),
           ruff=dict(color='#f4a6c6', smooth_shading=False),
           pompoms=dict(color='#b3122e', smooth_shading=True, specular=0.4),
           bow=dict(color='#b3122e', smooth_shading=True, specular=0.4))
def shot(fn, pos, focal=(30, 0, 12), zoom=1.0, flat=False):
    p = pv.Plotter(off_screen=True, window_size=(1400, 950)); p.set_background('white')
    for k in ('hand', 'straps', 'base', 'shell', 'ruff', 'drum', 'pompoms', 'bow'):
        p.add_mesh(pv.wrap(scene[k]).compute_normals(feature_angle=35, split_vertices=True, auto_orient_normals=False), **STY[k])
    p.camera_position = [pos, focal, (0, 0, 1)]
    if flat: p.enable_parallel_projection()
    p.camera.zoom(zoom); p.enable_anti_aliasing('ssaa'); p.screenshot(fn); p.close()
shot('concept/w1-three-quarter.png', (-110, -210, 160), zoom=1.45)
shot('concept/w2-front.png', (230, -170, 120), zoom=1.5)
shot('concept/w3-rear.png', (-150, 150, 120), zoom=1.5)
shot('concept/w4-side.png', (30, -320, 15), focal=(30, 0, 15), zoom=1.9, flat=True)

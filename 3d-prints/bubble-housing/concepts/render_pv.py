import sys; sys.path.insert(0,'concept')
import numpy as np, pyvista as pv
from model import scene
pv.OFF_SCREEN = True
def P(m): return pv.wrap(m)
STY = dict(hand=dict(color='#f1d3c2', opacity=0.55, smooth_shading=True),
           straps=dict(color='#e8743b', opacity=0.9, smooth_shading=True),
           mount=dict(color='#a98be8', smooth_shading=False),
           bracket=dict(color='#e9edf2', smooth_shading=False),
           drum=dict(color='#f7f8fa', smooth_shading=True))
LABELS = [((62, 0, 47), 'C-clip (37.8 bore, open on top)'),
          ((36, 0, 47), 'rear shroud, vent slots on top'),
          ((70, 12, 40), 'blower ring (37.5)'),
          ((58, -30, 3), 'knuckle belt loop'),
          ((-11, -20, 3), 'wrist belt loop'),
          ((58, -36, -24), 'Velcro under the 4 fingers'),
          ((-12, -36, -24), 'Velcro at the wrist')]
def shot(fn, pos, focal=(30,0,0), up=(0,0,1), labels=False, zoom=1.0, flat=False):
    p = pv.Plotter(off_screen=True, window_size=(1400, 950)); p.set_background('white')
    for k in ('hand','straps','mount','bracket','drum'): p.add_mesh(P(scene[k]), **STY[k])
    if labels:
        pts = np.array([l[0] for l in LABELS], float)
        p.add_point_labels(pts, [l[1] for l in LABELS], font_size=20, point_size=10, point_color='#333333',
                           shape_opacity=0.85, always_visible=True, text_color='black', shape_color='white')
    p.camera_position = [pos, focal, up]
    if flat: p.enable_parallel_projection()
    p.camera.zoom(zoom)
    p.enable_anti_aliasing('ssaa'); p.screenshot(fn); p.close()
shot('concept/v1-three-quarter.png', (-120, -230, 170), labels=True, zoom=1.25)
shot('concept/v2-side.png', (30, -320, 10), focal=(30,0,10), zoom=1.9, flat=True)
shot('concept/v3-top.png', (30, 0, 320), up=(0,1,0), zoom=1.9, flat=True)
shot('concept/v5-rear.png', (-150, 160, 130), focal=(30,0,10), zoom=1.5)
shot('concept/v4-from-fingers.png', (320, 0, 40), focal=(30,0,12), zoom=1.6, flat=True)

# Concept 1 rev C, "whimsy": same saddle + straps, clown details added.
#  - pleated ruff collar around the bubble ring (echoes the glove's ruffle cuff)
#  - polka-dot vent holes on the shroud sides (replace the top slots)
#  - three pom-pom buttons down the spine, a bow on the back wall
#  - scalloped lace edge on the saddle plate
import numpy as np, trimesh
from shapely.geometry import Polygon, Point
from trimesh.creation import box, cylinder, icosphere, extrude_polygon
import model as M
from model import at, along_x, hand_top, axis_z, T, R_IN, R_OUT, X0, X1, cyl_x

def rot(m, ang, axis): m=m.copy(); m.apply_transform(trimesh.transformations.rotation_matrix(ang, axis)); return m
def yz_disc(poly, x0, thick):
    """extrude a polygon drawn in (y, z-axis_z) into a plate facing +x"""
    m = extrude_polygon(poly, thick)                 # in xy, along +z
    m = rot(m, np.pi/2, [0,1,0])                     # extrusion now along -x ... fix orientation below
    m = rot(m, np.pi/2, [1,0,0])
    return at(m, x0, 0, axis_z)

below_plate = at(box([400, 400, 100]), 0, 0, T + 1.0 - 50)   # anything under the plate top is cut

# --- shroud with polka-dot vents ------------------------------------------------
outer = cyl_x(R_OUT, X0, X1).union(at(box([X1-X0, 32, axis_z-1.0]), (X0+X1)/2, 0, 1.0+(axis_z-1.0)/2))
inner = cyl_x(R_IN, X0+2.4, X1+1).union(at(box([X1-X0, 26, axis_z]), (X0+X1)/2+1.7, 0, T+axis_z/2))
shroud = outer.difference(inner)
dots = [(24, 6), (32, -3), (40, 6), (48, -3), (28, 15), (44, 15)]   # (x, z above axis)
for x, dz in dots:
    hole = rot(cylinder(radius=2.6, height=60, sections=32), np.pi/2, [1,0,0])
    shroud = shroud.difference(at(hole, x, 0, axis_z + dz))
shroud = shroud.difference(at(box([8, 10, 9]), X0+1, 0, T+4.5))     # wire exit

# --- ruff collar: two scalloped rings, offset half a pleat --------------------
def scallop(r_base, amp, n, phase):
    t = np.linspace(0, 2*np.pi, 720, endpoint=False)
    r = r_base + amp*np.abs(np.cos(n*t/2 + phase))
    return Polygon(np.c_[r*np.cos(t), r*np.sin(t)]).difference(Point(0,0).buffer(R_IN, 128))
ruff_back  = yz_disc(scallop(R_OUT+5, 4.5, 14, 0.0),      66, 2.4)
ruff_front = yz_disc(scallop(R_OUT+2, 4.0, 14, np.pi/14), 69, 2.4)
ruff = trimesh.util.concatenate([ruff_back, ruff_front]).difference(below_plate)

# --- pom-poms and bow ------------------------------------------------------------
pompoms = trimesh.util.concatenate([at(icosphere(3, radius=r), x, 0, axis_z + R_OUT + r*0.7)
                                    for x, r in ((24, 4.2), (36, 5.0), (48, 4.2))])
def lobe(sign):
    e = icosphere(3, radius=1.0); e.apply_scale([2.0, 9.0, 6.0])
    return at(rot(e, sign*0.35, [1,0,0]), X0 - 1.5, sign*9.5, axis_z + 4)
bow = trimesh.util.concatenate([lobe(1), lobe(-1), at(icosphere(3, radius=3.6), X0 - 2.0, 0, axis_z + 4)])

# --- lace scallops along the plate sides ----------------------------------------
lace = []
for x in np.arange(13, 42, 7.0):
    for s in (1, -1):
        y = s*24
        lace.append(at(cylinder(radius=3.6, height=T, sections=32), x, y, hand_top(abs(y)) + T/2))

# --- assemble: plate, loops, clip, cradle from rev A + new parts ---------------
base_parts = [M.curved_plate(10, 72, 24, T), M.curved_plate(-26, 10, 14, T)]
for s in (1, -1):
    base_parts += M.belt_loop(43, 73, 24*s, s, hand_top(24)) + M.belt_loop(-26, 4, 14*s, s, hand_top(14))
base_parts += lace
scene = dict(hand=M.scene['hand'], straps=M.scene['straps'], drum=M.drum,
             base=trimesh.util.concatenate(base_parts),
             shell=trimesh.util.concatenate([shroud, M.clip, M.pedestal] + M.cradle),
             ruff=ruff, pompoms=pompoms, bow=bow)

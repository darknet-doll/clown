# Concept 1: saddle mount. Units mm. x = wrist -> fingers, y = across hand, z = up.
# Hand/finger/forearm shapes are stand-ins (NOT measured); blower proxy uses B1/B2.
import numpy as np, trimesh
from trimesh.creation import box, cylinder, annulus
HA, HB = 40.0, 13.0                      # hand stand-in ellipse half-width / half-height
def hand_top(y): return -HB + HB*np.sqrt(np.clip(1-(y/HA)**2, 0, 1))

def curved_plate(x0, x1, hw, t, nx=2, ny=40):
    ys = np.linspace(-hw, hw, ny); xs = np.linspace(x0, x1, nx)
    V=[]; 
    for zoff in (0, t):
        for x in xs:
            for y in ys: V.append([x, y, hand_top(y)+zoff])
    V=np.array(V); idx=lambda l,i,j: l*nx*ny+i*ny+j; F=[]
    for i in range(nx-1):
        for j in range(ny-1):
            a,b,c,d=idx(1,i,j),idx(1,i,j+1),idx(1,i+1,j+1),idx(1,i+1,j); F+= [[a,b,c],[a,c,d]]
            a,b,c,d=idx(0,i,j),idx(0,i,j+1),idx(0,i+1,j+1),idx(0,i+1,j); F+= [[a,c,b],[a,d,c]]
    for i in range(nx-1):            # side walls
        for l0,j in ((0,0),(0,ny-1)):
            a,b,c,d=idx(0,i,j),idx(0,i+1,j),idx(1,i+1,j),idx(1,i,j); F+=[[a,b,c],[a,c,d]] if j==0 else [[a,c,b],[a,d,c]]
    for i,s in ((0,1),(nx-1,-1)):
        for j in range(ny-1):
            a,b,c,d=idx(0,i,j),idx(0,i,j+1),idx(1,i,j+1),idx(1,i,j); F+=[[a,c,b],[a,d,c]] if s==1 else [[a,b,c],[a,c,d]]
    m = trimesh.Trimesh(V,F); trimesh.repair.fix_normals(m); return m

def at(m, x, y, z): m=m.copy(); m.apply_translation([x,y,z]); return m
def along_x(m): m=m.copy(); m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0])); return m

def belt_loop(x0, x1, y_edge, side, z0, slot=3.0, bar=3.0, h=4.0):
    """Frame standing off the plate edge: strap passes between plate edge and outer bar."""
    yo = y_edge + side*(slot + bar/2); parts=[at(box([x1-x0, bar, h]), (x0+x1)/2, yo, z0+h/2)]
    for x in (x0+bar/2, x1-bar/2):
        parts.append(at(box([bar, slot+bar+1, h]), x, y_edge+side*(slot+bar)/2, z0+h/2))
    return parts

T = 2.4
mount = []
# saddle plate (front) and wrist tongue
mount.append(curved_plate(10, 72, 24, T))
mount.append(curved_plate(-26, 10, 14, T))
# belt loops: strap 25 wide -> 27 long slots, 3 wide
for s in (1,-1):
    mount += belt_loop(43, 73, 24*s, s, hand_top(24))
    mount += belt_loop(-26, 4, 14*s, s, hand_top(14))
# blower proxy: drum (B1 37.5) x 24 long + bracket, total B2 52
axis_z = T + 4 + 37.5/2
drum = at(along_x(cylinder(radius=37.5/2, height=24, sections=64)), 62, 0, axis_z)
bracket = at(box([28, 24, 30]), 36, 0, axis_z-37.5/2+15)
# C-clip around drum: 37.8 bore, 2.4 wall, 8 wide, open over the top 110 deg
ang0, ang1 = np.radians(90+55), np.radians(90-55+360)
ring = annulus(r_min=37.8/2, r_max=37.8/2+2.4, height=8, sections=96)
keep = []
for f in ring.faces:
    c = ring.vertices[f].mean(0); a = np.arctan2(c[1], c[0]) % (2*np.pi)
    keep.append(not (np.radians(35) < a < np.radians(145)))
clip = ring.submesh([np.where(keep)[0]], append=True)
clip.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]))
clip.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2,[1,0,0]))  # gap faces +z
clip = at(clip, 62, 0, axis_z)
pedestal = at(box([8, 22, 4.5]), 62, 0, T+2.0)
cradle = [at(box([20, 4, 4.5]), 36, s*9, T+2.0) for s in (1,-1)]
mount += [clip, pedestal] + cradle
# stand-ins
def ell_tube(x0, x1, a, b, zc, n=64):
    t = np.linspace(0, 2*np.pi, n, endpoint=False); ring2 = np.c_[a*np.cos(t), b*np.sin(t)+zc]
    V = np.vstack([np.c_[np.full(n,x), ring2] for x in (x0,x1)]); F=[]
    for i in range(n):
        j=(i+1)%n; F += [[i,j,n+j],[i,n+j,n+i]]
    V2 = np.vstack([V, [[x0,0,zc],[x1,0,zc]]]); c0,c1=2*n,2*n+1
    for i in range(n): j=(i+1)%n; F += [[c0,j,i],[c1,n+i,n+j]]
    return trimesh.Trimesh(V2, F)
hand = ell_tube(-40, 76, HA, HB, -HB)
forearm = ell_tube(-110, -40, 30, 20, -18)
fingers = [at(along_x(cylinder(radius=8, height=70, sections=24)), 76+35, y, -9) for y in (-27,-9,9,27)]
strap_k = ell_tube(46, 71, HA+1.6, HB+1.6, -HB); strap_w = ell_tube(-25, 2, HA+1.6, HB+1.6, -HB)
strap_k.faces = strap_k.faces[:128]; strap_w.faces = strap_w.faces[:128]   # band only, no end caps
scene = dict(mount=trimesh.util.concatenate(mount), drum=drum, bracket=bracket,
             hand=trimesh.util.concatenate([hand, forearm]+fingers), straps=trimesh.util.concatenate([strap_k, strap_w]))

# --- rev B: rear shroud closes the back of the blower head ---------------------
R_IN, WALL = 37.8/2, 2.4
R_OUT = R_IN + WALL
X0, X1 = 16, 58                      # shroud runs from the end cap to the C-clip
def cyl_x(r, x0, x1, sec=96): return at(along_x(cylinder(radius=r, height=x1-x0, sections=sec)), (x0+x1)/2, 0, axis_z)
outer = cyl_x(R_OUT, X0, X1).union(at(box([X1-X0, 2*16, axis_z-1.0]), (X0+X1)/2, 0, 1.0+(axis_z-1.0)/2))
inner = cyl_x(R_IN, X0+WALL, X1+1).union(at(box([X1-X0, 26, axis_z]), (X0+X1)/2+WALL/2+0.5, 0, T+axis_z/2))
shroud = outer.difference(inner)
for x in (24, 30, 36, 42, 48):                                   # vent slots on top
    shroud = shroud.difference(at(box([2.4, 18, 14]), x, 0, axis_z+R_IN))
shroud = shroud.difference(at(box([8, 10, 9]), X0+1, 0, T+4.5))  # wire exit, bottom of the end cap
mount.append(shroud)
scene['mount'] = trimesh.util.concatenate(mount)

# Screw holes on the gun's split face (x = 0): depth map of each half seen from the split
# plane, then small openings / sockets. Run from this folder; writes split-depth.npz (local).
import numpy as np, trimesh
from scipy import ndimage
st = 0.5; ys = np.arange(-40, 45, st); zs = np.arange(-8, 175, st)
Y, Z = np.meshgrid(ys, zs, indexing='ij')
out = {}
for name, x0, dx in (('01', 5.0, -1.0), ('02', -5.0, 1.0)):
    m = trimesh.load(f'stl/{name}_Body_REV1.stl')
    O = np.c_[np.full(Y.size, x0), Y.ravel(), Z.ravel()]; D = np.tile([dx, 0, 0], (Y.size, 1))
    loc, ri, _ = m.ray.intersects_location(O, D, multiple_hits=False)
    dep = np.full(Y.size, np.nan); dep[ri] = abs(loc[:, 0]); out[name] = dep.reshape(Y.shape)
np.savez('split-depth.npz', ys=ys, zs=zs, **out)
for name, d in out.items():
    face = np.nan_to_num(d, nan=99) < 0.3                   # flat split face
    hole = ndimage.binary_closing(face, iterations=4) & ~face # small gaps inside the face
    lab, n = ndimage.label(hole)
    for k in range(1, n + 1):
        m = lab == k; cnt = m.sum()
        if 4 <= cnt <= 60:
            yy, zz = np.where(m); dd = d[m]
            kind = 'through' if np.isnan(dd).mean() > 0.5 else f'socket {np.nanmax(dd):.1f} deep'
            print(f'{name} half: hole at gun z {zs[zz].mean():6.1f} (= {zs[zz].mean()+5:5.1f} behind muzzle), '
                  f'y {ys[yy].mean():6.1f}: ~{2*np.sqrt(cnt*st*st/np.pi):.1f} dia, {kind}')

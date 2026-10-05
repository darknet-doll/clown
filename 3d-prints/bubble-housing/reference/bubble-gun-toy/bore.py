# Inner radius of the blower bore, both halves joined, every 1 mm along z.
# Run from this folder after extract.py: python3 bore.py

import trimesh, numpy as np
a=trimesh.load('stl/01_Body_REV1.stl'); b=trimesh.load('stl/02_Body_REV1.stl')
m=trimesh.util.concatenate([a,b])
angs=np.radians(np.arange(0,360,15))
print('z    | inner radius at 0..345 deg step 15 (0=+x side, 90=+y bottom, 270=-y top)')
for z in np.arange(-5,50,1.0):
    O=np.tile([0,0,z],(len(angs),1)).astype(float); D=np.stack([np.cos(angs),np.sin(angs),0*angs],1)
    loc,ri,_=m.ray.intersects_location(O,D,multiple_hits=False)
    r=np.full(len(angs),np.nan); r[ri]=np.linalg.norm(loc[:,:2],axis=1)
    print(f'{z:5.1f}| '+' '.join('  -- ' if np.isnan(v) else f'{v:5.1f}' for v in r))

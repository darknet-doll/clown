# Cuff ruffle concept r1. Units mm. x = wrist -> fingers, same frame as
# bubble-housing/concepts/model.py, which supplies the hand/housing context.
# STAND-INS: hand ellipse is the housing concept's stand-in; tongue-to-crease
# distance is UNKNOWN, so every hem position here is a placeholder for looks.
import importlib.util, pathlib
import numpy as np, trimesh

_bh = pathlib.Path(__file__).resolve().parents[2] / 'bubble-housing' / 'concepts' / 'model.py'
_spec = importlib.util.spec_from_file_location('bh_model', _bh)
M = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(M)

HA, HB = M.HA, M.HB          # hand stand-in ellipse half-width / half-height
PHI_MAX = np.radians(125)    # wrap: top +/-125 deg; the palm stays clear

def ellipse_pt(phi):
    """point on the hand ellipse (phi from top) and its outward normal in (y,z)"""
    y = HA*np.sin(phi); z = -HB + HB*np.cos(phi)
    ny, nz = y/HA**2, (z+HB)/HB**2
    n = np.hypot(ny, nz)
    return y, z, ny/n, nz/n

def flounce(x0, L, direc, off0, flare, amp, k, phase=0.0, scallop=0.16,
            holes=(), nphi=480, ns=56):
    """One ruffle tier: a sheet rooted on the hand ellipse at x0, flaring
    direc*(+x or -x) with fluting sin(k*phi+phase), scalloped hem, and faces
    dropped inside `holes` [(phi_c, s_c, phi_hw, s_hh), ...] = the openwork."""
    phis = np.linspace(-PHI_MAX, PHI_MAX, nphi)
    svals = np.linspace(0, 1, ns)
    smax = 1 - scallop*(0.5 + 0.5*np.cos(k*phis + phase))   # scallops follow the flutes
    V = np.zeros((ns, nphi, 3))
    for j, phi in enumerate(phis):
        y, z, ny, nz = ellipse_pt(phi)
        for i, s0 in enumerate(svals):
            s = s0*smax[j]
            r = off0 + flare*s**1.4 + amp*(s**1.2)*np.sin(k*phi + phase)
            V[i, j] = [x0 + direc*L*s, y + ny*r, z + nz*r]
    F = []
    for i in range(ns-1):
        for j in range(nphi-1):
            sc = (svals[i]+svals[i+1])/2; pc = (phis[j]+phis[j+1])/2
            if any(((pc-hp)/hw)**2 + ((sc-hs)/hh)**2 < 1 for hp, hs, hw, hh in holes):
                continue
            a = i*nphi+j; b = a+1; c = a+nphi+1; d = a+nphi
            F += [[a, b, c], [a, c, d]]
    return trimesh.Trimesh(V.reshape(-1, 3), np.array(F))

def hole_rows(k, rows):
    """Staggered rows of openwork holes, one hole per flute."""
    out = []
    for s_c, stag in rows:
        for m in range(-k, k+1):
            phi_c = (2*np.pi*m + np.pi/2 + (np.pi if stag else 0))/k
            if abs(phi_c) < PHI_MAX - 0.1:
                out.append((phi_c, s_c, 0.34*np.pi/k, 0.075))
    return out

K = 13
ROOT = -26.0                                  # the tongue's wrist end (concept frame)
tiers = [
    # main skirt toward the knuckles: covers the tongue + its strap,
    # scalloped hem ends ~x +8, well short of the shroud mouth at x 16
    flounce(ROOT, 34, +1, 2.5, 7.0, 3.8, K, 0.0,
            holes=hole_rows(K, [(0.35, 0), (0.55, 1), (0.78, 0)])),
    # over-tier, flutes interleaved, hem ~x -6
    flounce(ROOT, 20, +1, 4.5, 6.0, 3.2, K, np.pi,
            holes=hole_rows(K, [(0.42, 1), (0.68, 0)])),
    # short back flounce toward the wrist. RIGID -> placeholder hem at x -34;
    # the real limit is >=10 clear of the crease at full extension (unmeasured)
    flounce(ROOT, 8, -1, 2.5, 5.0, 2.8, K, 0.0, holes=hole_rows(K, [(0.55, 0)])),
]

# mount tab: same footprint as the tongue, 1.2 thick, sandwiched underneath it
tab = M.curved_plate(-26, 10, 14, 1.2)
tab.apply_translation([0, 0, -1.2])

scene = dict(M.scene)
scene['ruffle'] = trimesh.util.concatenate(tiers)
scene['tab'] = tab

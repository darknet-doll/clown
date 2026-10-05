# Pull every part out of Bubble_Gun_REV1.3mf into stl/, in the designer's
# assembly frame (mesh + Bambu's source_offset), not the plate layout.
# Run from this folder: python3 extract.py
import re, os, zipfile, numpy as np, trimesh, xml.etree.ElementTree as ET

z = zipfile.ZipFile('Bubble_Gun_REV1.3mf')
top = z.read('3D/3dmodel.model').decode()
comp = dict(re.findall(r'<object id="(\d+)"[^>]*>\s*<components>\s*<component p:path="([^"]+)"', top))
cfg = ET.fromstring(z.read('Metadata/model_settings.config'))
os.makedirs('stl', exist_ok=True)
for o in cfg.findall('object'):
    name = o.find("metadata[@key='name']").get('value')
    p = o.find('part')
    off = np.array([float(p.find(f"metadata[@key='source_offset_{a}']").get('value')) for a in 'xyz'])
    src = z.read(comp[o.get('id')].lstrip('/')).decode()
    V = np.array(re.findall(r'<vertex x="([^"]+)" y="([^"]+)" z="([^"]+)"', src), float)
    F = np.array(re.findall(r'<triangle v1="(\d+)" v2="(\d+)" v3="(\d+)"', src), int)
    m = trimesh.Trimesh(V + off, F, process=True)
    m.export(f'stl/{name}')
    b = m.bounds
    print(f'{name:22s} min {np.round(b[0], 1)} max {np.round(b[1], 1)} size {np.round(b[1] - b[0], 1)}')

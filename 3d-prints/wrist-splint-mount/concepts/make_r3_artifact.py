"""Assemble the r3 review artifact (r3-review.html) from trace-bus-r3.json.

The SVG is painter-method: plate path (outer + kept channel slots,
evenodd) in the TPU colour, pattern cutouts drawn over it in the bench
colour so they read as holes. Model frame is mm, y flipped for SVG.
"""

import json

import numpy as np

d = json.load(open("trace-bus-r3.json"))
S = 0.776  # print scale

def path_of(loops, nd=1):
    ds = []
    for p in loops:
        p = np.asarray(p, float)
        pts = np.round(np.c_[p[:, 0], -p[:, 1]], nd)
        ds.append("M" + " ".join(f"{x:g},{y:g}" for x, y in pts) + "Z")
    return "".join(ds)

plate_d = path_of([d["outer"]] + d["kept"])
ghost_d = path_of(d["honeycomb"])

cut = []  # pattern cutouts, bench-coloured
for pts in d["slots"]:
    p = np.asarray(pts, float)
    pl = " ".join(f"{x:g},{-y:g}" for x, y in np.round(p, 1))
    cut.append(f'<polyline points="{pl}"/>')
for x, y in d["pads"]:
    cut.append(f'<circle cx="{x:g}" cy="{-y:g}" r="{d["pad_r"]}"/>')
for x, y, w, h in d["diamonds"]:
    cut.append(f'<path d="M{x:g},{-(y - h / 2):g} {x + w / 2:g},{-y:g} '
               f'{x:g},{-(y + h / 2):g} {x - w / 2:g},{-y:g}Z" class="f"/>')
for x, y, ang in d["resistors"]:
    ca, sa = np.cos(ang), np.sin(ang)
    L = 12.0
    cut.append(f'<line x1="{x - L * ca:g}" y1="{-(y - L * sa):g}" '
               f'x2="{x + L * ca:g}" y2="{-(y + L * sa):g}"/>')
    for s in (-1, 1):
        cut.append(f'<circle cx="{x + s * (L + 1) * ca:g}" '
                   f'cy="{-(y + s * (L + 1) * sa):g}" r="{d["pad_r"]}"/>')
    t = np.linspace(0, 2 * np.pi, 24)
    bx, by = 7 * np.tanh(1.6 * np.cos(t)), 3.1 * np.tanh(1.6 * np.sin(t))
    pl = " ".join(f"{vx:g},{vy:g}" for vx, vy in
                  np.round(np.c_[x + bx * ca - by * sa,
                                 -(y + bx * sa + by * ca)], 1))
    cut.append(f'<polygon points="{pl}" class="f"/>')
cut_svg = "\n".join(cut)

P = d["patch"]
patch_svg = (f'<rect x="{P["x0"]}" y="{-P["y1"]}" width="{P["x1"] - P["x0"]}" '
             f'height="{P["y1"] - P["y0"]}" rx="3"/>')

o = np.asarray(d["outer"], float)
x0, x1 = o[:, 0].min() - 6, o[:, 0].max() + 6
y0, y1 = -o[:, 1].max() - 6, -o[:, 1].min() + 6
viewbox = f"{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}"

def mm(v):
    return f"{v:g} &rarr; {v * S:.1f}"

rows = "\n".join(
    f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in [
        ("splint footprint", f"229.4 &times; 197.8 &rarr; 178.0 &times; 153.5"),
        ("trace slot width", mm(3.0)),
        ("web floor (between cuts)", mm(3.0)),
        ("pad &Oslash;", mm(5.2)),
        ("harlequin diamond", "6 &times; 11 &rarr; 4.7 &times; 8.5"),
        ("velcro patch (solid)", "53 &times; 44 &rarr; 41.1 &times; 34.1"),
        ("velcro channels take strap", "&le; 20 &rarr; &le; 15.5 (ours: 11)"),
    ])

html = """<title>Splint Trace Bus</title>
<style>
/* layout: figure-first review bench; dark-first, both themes */
:root{
  --bg:#141416; --fg:#e8e9ec; --muted:#98a0ab; --accent:#E49CB4;
  --green:#8FBE78; --bench:#1c1d22; --line:#2b2c32; --tpu:#0d0d10;
  color-scheme:dark;
}
@media (prefers-color-scheme: light){ :root:not([data-theme="dark"]){
  --bg:#f2f3f5; --fg:#1d1e24; --muted:#5a6270; --accent:#b4536f;
  --green:#4e7f3a; --bench:#e2e5ea; --line:#c9cdd6; color-scheme:light;
}}
:root[data-theme="light"]{
  --bg:#f2f3f5; --fg:#1d1e24; --muted:#5a6270; --accent:#b4536f;
  --green:#4e7f3a; --bench:#e2e5ea; --line:#c9cdd6; color-scheme:light;
}
body{background:var(--bg);color:var(--fg);
  font:15px/1.55 "IBM Plex Sans",system-ui,sans-serif;
  padding-inline:16px;max-width:1060px;margin-inline:auto}
h1,h2,.lbl,table,button{font-family:"IBM Plex Mono",ui-monospace,monospace}
h1{font-size:1.45rem;margin:1.1rem 0 .2rem;text-wrap:balance}
h1 b{color:var(--accent);font-weight:600}
.sub{color:var(--muted);margin:0 0 1rem}
.controls{display:flex;flex-wrap:wrap;gap:.6rem 1.4rem;align-items:center;
  margin:0 0 .8rem}
.lbl{font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted)}
.seg{display:flex;gap:0;border:1px solid var(--line);border-radius:8px;
  overflow:hidden}
button{background:none;border:0;color:var(--fg);font-size:.8rem;
  padding:.38rem .7rem;cursor:pointer}
.seg button+button{border-left:1px solid var(--line)}
button[aria-pressed="true"]{background:var(--accent);color:var(--bg)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
figure{margin:0;background:var(--bench);border:1px solid var(--line);
  border-radius:12px;padding:10px}
svg{display:block;width:100%;height:auto}
.plate{fill:var(--tpu);fill-rule:evenodd;transition:fill .2s}
.cuts *{fill:none;stroke:var(--bench);stroke-width:3;
  stroke-linecap:round;stroke-linejoin:round}
.cuts circle,.cuts .f{fill:var(--bench);stroke:none}
.ghost{fill:none;stroke:var(--accent);stroke-width:.7;opacity:.55;
  stroke-dasharray:3 2}
.anno rect{fill:none;stroke:var(--accent);stroke-width:1.2;
  stroke-dasharray:5 3}
.anno text{font:6.5px "IBM Plex Mono",monospace;fill:var(--accent)}
.anno .g{fill:var(--green)}
figcaption{color:var(--muted);font-size:.8rem;padding:.5rem .2rem 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));
  gap:1.2rem;margin:1.4rem 0 2rem}
.grid>div{min-width:0}
h2{font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);margin:0 0 .5rem}
table{border-collapse:collapse;width:100%;font-size:.8rem;
  font-variant-numeric:tabular-nums}
td{padding:.3rem .5rem;border-top:1px solid var(--line)}
td:last-child{text-align:right;white-space:nowrap}
ul{margin:.2rem 0;padding-left:1.1rem}
li{margin:.3rem 0}
li::marker{color:var(--accent)}
.note{color:var(--muted);font-size:.85rem}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap">

<h1>splint trace bus <b>r3</b></h1>
<p class="sub">CIRCUIT-mode openwork on the real wrist-splint outline &mdash;
harlequin diamonds in place of the house heart. Dimensions in mm at 100%
model scale &rarr; at the 77.6% print scale.</p>

<div class="controls">
  <span class="lbl">TPU colour</span>
  <span class="seg" id="tpu">
    <button data-c="#0d0d10" aria-pressed="true">black</button>
    <button data-c="#BAD2DE" aria-pressed="false">ice blue</button>
    <button data-c="#e9edef" aria-pressed="false">natural</button>
  </span>
  <span class="seg">
    <button id="bGhost" aria-pressed="false">original honeycomb</button>
    <button id="bAnno" aria-pressed="true">annotations</button>
  </span>
</div>

<figure>
<svg viewBox="__VIEWBOX__" role="img"
     aria-label="Trace-bus cutout design on the wrist splint outline">
  <path class="plate" d="__PLATE__"/>
  <g class="cuts">__CUTS__</g>
  <path class="ghost" id="ghost" d="__GHOST__" hidden/>
  <g class="anno" id="anno">
    __PATCH__
    <text x="__PX__" y="__PY__">housing velcro patch (solid)</text>
    <text class="g" x="-104" y="104">&larr; forearm end, pads</text>
    <text class="g" x="40" y="-6">thumb opening</text>
    <text class="g" x="-30" y="-98">velcro channel ladders top + bottom</text>
  </g>
</svg>
<figcaption>flat as printed, 100% model scale. Bundle A terminates on the
patch like pins; the patch carries the punched diamond (the chip's die
mark). Velcro channels, label window and all solid margins are untouched
from the original splint.</figcaption>
</figure>

<div class="grid">
<div>
  <h2>numbers (100% &rarr; 77.6%)</h2>
  <table>__ROWS__</table>
</div>
<div>
  <h2>design notes</h2>
  <ul>
    <li>Trace bus per the CIRCUIT grammar: bundles, 45&deg; doglegs, every
      free end terminated with a pad; resistors as punctuation (3).</li>
    <li>Harlequin diamonds replace the pixel-heart signature
      (darknetdoll, 2026-10-14).</li>
    <li>All cutouts auto-checked: &ge;7 to the outer edge, &ge;4 to the
      kept channel slots. Zero violations in this rev.</li>
    <li>In black TPU the skin reads as the trace colour through the cuts;
      ice blue matches the FLORAL shell direction.</li>
  </ul>
  <h2 style="margin-top:1rem">open before export</h2>
  <ul class="note">
    <li>Mirror check for the left hand (thumb side) before any export.</li>
    <li>Z scale: uniform 77.6% (wall 2.72) vs Z held at 3.5 &mdash; dorsal
      coupon decides.</li>
    <li>Patch position assumes the dorsal band between thumb opening and
      top channels; confirm on the first wrap fit.</li>
  </ul>
</div>
</div>

<script>
const root=document.documentElement;
document.querySelectorAll('#tpu button').forEach(b=>b.onclick=()=>{
  document.querySelectorAll('#tpu button').forEach(x=>
    x.setAttribute('aria-pressed','false'));
  b.setAttribute('aria-pressed','true');
  root.style.setProperty('--tpu',b.dataset.c);
});
const tgl=(id,el)=>{const b=document.getElementById(id);
  b.onclick=()=>{const on=b.getAttribute('aria-pressed')!=='true';
    b.setAttribute('aria-pressed',String(on));
    document.getElementById(el).hidden=!on;};};
tgl('bGhost','ghost'); tgl('bAnno','anno');
</script>
"""

html = (html.replace("__VIEWBOX__", viewbox)
        .replace("__PLATE__", plate_d)
        .replace("__CUTS__", cut_svg)
        .replace("__GHOST__", ghost_d)
        .replace("__PATCH__", patch_svg)
        .replace("__PX__", str(P["x0"] + 2)).replace("__PY__", str(-P["y1"] - 3))
        .replace("__ROWS__", rows))
open("r3-review.html", "w").write(html)
print(f"wrote r3-review.html ({len(html) / 1024:.0f} KB)")

"""Rebuild the review artifact with the r4 tulle-sandwich reveal.

Clone of make_r3_artifact.py (kept for history). Emits the SAME file,
r3-review.html, so the publish updates the existing artifact URL.
Adds: r4 positive-elements SVG (default view), rev toggle, tulle colour
picker, the pause/magnet workflow, supplies with Amazon search links,
and prior-art references. Patch tile gains the mount features from the
2026-10-15 discussion: two strap slots (13 x 2.5 printed) + 4 eyelets.
"""

import json

import numpy as np

d = json.load(open("trace-bus-r3.json"))
S = 0.776

def path_of(loops, nd=1):
    ds = []
    for p in loops:
        p = np.asarray(p, float)
        pts = np.round(np.c_[p[:, 0], -p[:, 1]], nd)
        ds.append("M" + " ".join(f"{x:g},{y:g}" for x, y in pts) + "Z")
    return "".join(ds)

outer_d = path_of([d["outer"]])
plate_d = path_of([d["outer"]] + d["kept"])

# ---- r3 cutout layer (bench-coloured cuts), as before
def cut_elems(fill_cls="f"):
    out = []
    for pts in d["slots"]:
        p = np.asarray(pts, float)
        pl = " ".join(f"{x:g},{-y:g}" for x, y in np.round(p, 1))
        out.append(f'<polyline points="{pl}"/>')
    for x, y in d["pads"]:
        out.append(f'<circle cx="{x:g}" cy="{-y:g}" r="{d["pad_r"]}"/>')
    for x, y, w, h in d["diamonds"]:
        out.append(f'<path d="M{x:g},{-(y - h / 2):g} {x + w / 2:g},{-y:g} '
                   f'{x:g},{-(y + h / 2):g} {x - w / 2:g},{-y:g}Z" class="{fill_cls}"/>')
    for x, y, ang in d["resistors"]:
        ca, sa = np.cos(ang), np.sin(ang)
        L = 12.0
        out.append(f'<line x1="{x - L * ca:g}" y1="{-(y - L * sa):g}" '
                   f'x2="{x + L * ca:g}" y2="{-(y + L * sa):g}"/>')
        for s in (-1, 1):
            out.append(f'<circle cx="{x + s * (L + 1) * ca:g}" '
                       f'cy="{-(y + s * (L + 1) * sa):g}" r="{d["pad_r"]}"/>')
        t = np.linspace(0, 2 * np.pi, 24)
        bx, by = 7 * np.tanh(1.6 * np.cos(t)), 3.1 * np.tanh(1.6 * np.sin(t))
        pl = " ".join(f"{vx:g},{vy:g}" for vx, vy in
                      np.round(np.c_[x + bx * ca - by * sa,
                                     -(y + bx * sa + by * ca)], 1))
        out.append(f'<polygon points="{pl}" class="{fill_cls}"/>')
    return out

r3_cuts = "\n".join(cut_elems())

# ---- r4 positive layer
P = d["patch"]
r4 = []
# traces (white) — in r4 bundle A lands ON the tile: extend ends to x0+2
for pts in d["slots"]:
    p = np.asarray(pts, float)
    if abs(p[-1][0] - (P["x0"] - 4.5)) < 0.1 and P["y0"] < p[-1][1] < P["y1"]:
        p = np.vstack([p, [P["x0"] + 2, p[-1][1]]])
    pl = " ".join(f"{x:g},{-y:g}" for x, y in np.round(p, 1))
    r4.append(f'<polyline class="tr" points="{pl}"/>')
for x, y in d["pads"]:
    r4.append(f'<circle class="el" cx="{x:g}" cy="{-y:g}" r="{d["pad_r"]}"/>'
              f'<circle class="punch" cx="{x:g}" cy="{-y:g}" '
              f'r="{d["pad_r"] * 0.4:.2f}"/>')
for x, y, w, h in d["diamonds"][:-1]:
    r4.append(f'<path class="pk" d="M{x:g},{-(y - h / 2):g} {x + w / 2:g},{-y:g} '
              f'{x:g},{-(y + h / 2):g} {x - w / 2:g},{-y:g}Z"/>')
for x, y, ang in d["resistors"]:
    ca, sa = np.cos(ang), np.sin(ang)
    L = 12.0
    r4.append(f'<line class="tr" x1="{x - L * ca:g}" y1="{-(y - L * sa):g}" '
              f'x2="{x + L * ca:g}" y2="{-(y + L * sa):g}"/>')
    for s in (-1, 1):
        r4.append(f'<circle class="el" cx="{x + s * (L + 1) * ca:g}" '
                  f'cy="{-(y + s * (L + 1) * sa):g}" r="{d["pad_r"]}"/>')
    t = np.linspace(0, 2 * np.pi, 24)
    bx, by = 7 * np.tanh(1.6 * np.cos(t)), 3.1 * np.tanh(1.6 * np.sin(t))
    pl = " ".join(f"{vx:g},{vy:g}" for vx, vy in
                  np.round(np.c_[x + bx * ca - by * sa,
                                 -(y + bx * sa + by * ca)], 1))
    r4.append(f'<polygon class="pk" points="{pl}"/>')
# strap tabs around kept slots
for k in d["kept"]:
    k = np.asarray(k, float)
    cx, cy = k.mean(axis=0)
    w, h = np.ptp(k[:, 0]) + 5, np.ptp(k[:, 1]) + 5
    r4.append(f'<rect class="el" x="{cx - w / 2:g}" y="{-cy - h / 2:g}" '
              f'width="{w:g}" height="{h:g}" rx="2"/>')
    pl = " ".join(f"{x:g},{-y:g}" for x, y in np.round(k, 1))
    r4.append(f'<polygon class="punch" points="{pl}"/>')
# patch tile: pink, white rim, die diamond + 2 strap slots + 4 eyelets
pw, ph = P["x1"] - P["x0"], P["y1"] - P["y0"]
cxp, cyp = P["x0"] + pw / 2, P["y0"] + ph / 2
r4.append(f'<rect class="pk" x="{P["x0"]}" y="{-P["y1"]}" width="{pw}" '
          f'height="{ph}" rx="3" stroke-width="2.2"/>')
r4.append(f'<path class="punch" d="M{cxp},{-(cyp - 6)} {cxp + 3.5},{-cyp} '
          f'{cxp},{-(cyp + 6)} {cxp - 3.5},{-cyp}Z"/>')
for sy in (P["y0"] + 9, P["y1"] - 9):
    r4.append(f'<rect class="punch" x="{cxp - 8.4:g}" y="{-sy - 1.6:g}" '
              f'width="16.8" height="3.2" rx="1.6"/>')
for ex in (P["x0"] + 6, P["x1"] - 6):
    for ey in (P["y0"] + 6, P["y1"] - 6):
        r4.append(f'<circle class="punch" cx="{ex}" cy="{-ey}" r="2"/>')
for x in np.arange(32, P["x1"] - 3, 7):
    r4.append(f'<line class="tr" x1="{x:g}" y1="{-(P["y0"] - 6.5):g}" '
              f'x2="{x:g}" y2="{-(P["y0"] - 1):g}"/>')
r4_svg = "\n".join(r4)

o = np.asarray(d["outer"], float)
x0, x1 = o[:, 0].min() - 6, o[:, 0].max() + 6
y0, y1 = -o[:, 1].max() - 6, -o[:, 1].min() + 6
viewbox = f"{x0:.0f} {y0:.0f} {x1 - x0:.0f} {y1 - y0:.0f}"

rows = "\n".join(
    f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in [
        ("splint footprint", "229.4 &times; 197.8 &rarr; 178.0 &times; 153.5"),
        ("r4 element height", "0.4 base + tulle + 1.4 top &asymp; 1.8"),
        ("trace width", "3.0 &rarr; 2.3"),
        ("pad &Oslash; / punched centre", "5.2 / 2.1 &rarr; 4.0 / 1.6"),
        ("patch tile", "53 &times; 44 &rarr; 41.1 &times; 34.1"),
        ("patch strap slots (printed size)", "2 &times; (13 &times; 2.5)"),
        ("patch eyelets &Oslash; (printed)", "4 &times; 3.1"),
        ("velcro channels take strap", "&le; 15.5 printed (ours: 11)"),
    ])

html = """<title>Splint Trace Bus</title>
<style>
/* figure-first review bench; dark-first, both themes */
:root{
  --bg:#141416; --fg:#e8e9ec; --muted:#98a0ab; --accent:#E49CB4;
  --bench:#1c1d22; --line:#2b2c32; --tpu:#0d0d10;
  --tulle:#232430; --mesh:#3a3c48; --el:#F2F2F2; --pk:#F2B8CC;
  color-scheme:dark;
}
@media (prefers-color-scheme: light){ :root:not([data-theme="dark"]){
  --bg:#f2f3f5; --fg:#1d1e24; --muted:#5a6270; --accent:#b4536f;
  --bench:#e2e5ea; --line:#c9cdd6; color-scheme:light;
}}
:root[data-theme="light"]{
  --bg:#f2f3f5; --fg:#1d1e24; --muted:#5a6270; --accent:#b4536f;
  --bench:#e2e5ea; --line:#c9cdd6; color-scheme:light;
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
.seg{display:flex;border:1px solid var(--line);border-radius:8px;
  overflow:hidden}
button{background:none;border:0;color:var(--fg);font-size:.8rem;
  padding:.38rem .7rem;cursor:pointer}
.seg button+button{border-left:1px solid var(--line)}
button[aria-pressed="true"]{background:var(--accent);color:var(--bg)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
figure{margin:0;background:var(--bench);border:1px solid var(--line);
  border-radius:12px;padding:10px}
svg{display:block;width:100%;height:auto}
.plate{fill:var(--tpu);fill-rule:evenodd}
.cuts *{fill:none;stroke:var(--bench);stroke-width:3;
  stroke-linecap:round;stroke-linejoin:round}
.cuts circle,.cuts .f{fill:var(--bench);stroke:none}
.tulle{fill:var(--tulle)}
.bind{fill:none;stroke:var(--el);stroke-width:4;stroke-linecap:round;
  stroke-dasharray:11 5}
.tr{fill:none;stroke:var(--el);stroke-width:3;stroke-linecap:round;
  stroke-linejoin:round}
.el{fill:var(--el);stroke:none}
.pk{fill:var(--pk);stroke:var(--el)}
.pk:not(rect){stroke:none}
.punch{fill:var(--tulle);stroke:none}
figcaption{color:var(--muted);font-size:.8rem;padding:.5rem .2rem 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));
  gap:1.2rem;margin:1.4rem 0 2rem}
.grid>div{min-width:0}
h2{font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;
  color:var(--muted);margin:1rem 0 .5rem}
table{border-collapse:collapse;width:100%;font-size:.8rem;
  font-variant-numeric:tabular-nums}
td{padding:.3rem .5rem;border-top:1px solid var(--line)}
td:last-child{text-align:right;white-space:nowrap}
ol,ul{margin:.2rem 0;padding-left:1.2rem}
li{margin:.32rem 0}
li::marker{color:var(--accent)}
a{color:var(--accent)}
.note{color:var(--muted);font-size:.85rem}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap">

<h1>splint trace bus <b>r4: tulle sandwich</b></h1>
<p class="sub">The trace bus printed as rigid elements ON tulle &mdash; fabric
is the flex, so the stiff 68D &ldquo;TPU for AMS&rdquo; (or PLA) is the right
material, and the AMS makes it multicolour. r3 (the all-TPU cutout) kept
below for comparison. mm at 100% &rarr; at the 77.6% print scale.</p>

<div class="controls">
  <span class="lbl">rev</span>
  <span class="seg" id="rev">
    <button data-v="vR4" aria-pressed="true">r4 tulle</button>
    <button data-v="vR3" aria-pressed="false">r3 cutout</button>
  </span>
  <span class="seg" id="tul">
    <span class="lbl" style="padding:.38rem .5rem">tulle</span>
    <button data-t="#232430" data-m="#3a3c48" aria-pressed="true">black</button>
    <button data-t="#cfd3da" data-m="#b7bcc6" aria-pressed="false">white</button>
    <button data-t="#52333f" data-m="#6b4454" aria-pressed="false">pink</button>
  </span>
</div>

<div id="vR4">
<figure>
<svg viewBox="__VIEWBOX__" role="img" aria-label="Trace bus as printed elements on tulle">
  <path class="tulle" d="__OUTER__"/>
  <path fill="url(#mesh)" d="__OUTER__"/>
  <defs><pattern id="mesh" width="2.6" height="2.6" patternUnits="userSpaceOnUse">
    <path d="M0,0H2.6M0,0V2.6" stroke="var(--mesh)" stroke-width=".3" fill="none"/>
  </pattern></defs>
  <path class="bind" d="__OUTER__"/>
  __R4__
</svg>
<figcaption>dark field = bare tulle = all the flex. Bundle A now lands ON the
patch tile (structure, not just looks). Patch tile: strap slots &times;2,
eyelets &times;4 for a ribbon bow, die-mark diamond; housing straps down
through the slots onto its belt loops. Tulle is trimmed at the outline and
thumb opening after printing; the dashed edge binding is the printed
trim guide.</figcaption>
</figure>
</div>

<div id="vR3" hidden>
<figure>
<svg viewBox="__VIEWBOX__" role="img" aria-label="r3 cutout design">
  <path class="plate" d="__PLATE__"/>
  <g class="cuts">__CUTS__</g>
</svg>
<figcaption>r3: the same geometry as cutouts in a solid 2.72 plate. Printed
2026-10-15 in 68D &mdash; too stiff; needs true TPU 95A. Kept for comparison.</figcaption>
</figure>
</div>

<div class="grid">
<div>
  <h2>numbers (100% &rarr; 77.6%)</h2>
  <table>__ROWS__</table>

  <h2>print workflow (the reveal)</h2>
  <ol>
    <li>Slice elements only, flat. In Bambu Studio right-click the layer
      slider at <b>layer 2</b> &rarr; <b>Add Pause</b>.</li>
    <li>Print the 2 base layers; the printer parks.</li>
    <li>Lay tulle over the whole plate, pull taut.</li>
    <li>Pin it with small neodymium magnets to the steel plate,
      <b>outside the print area</b>, clear of the nozzle path.</li>
    <li>Resume. The next layer welds through the mesh; remaining layers
      sandwich the fabric.</li>
    <li>Cool, peel, trim tulle at the edge binding and inside the thumb
      opening and strap slots (sharp scissors or a hot knife seals
      polyester edges).</li>
  </ol>
</div>
<div>
  <h2>supplies</h2>
  <ul>
    <li><b>Tulle:</b> plain <b>polyester</b> tulle, fine mesh, no glitter
      (glitter blocks the weld; too-fine organza doesn't bond). One bolt is
      a lifetime supply for this part (~200 &times; 180 mm per attempt).
      <a href="https://www.amazon.com/s?k=polyester+tulle+fabric+bolt+54+inch">
      Amazon search: polyester tulle bolt 54&quot;</a></li>
    <li><b>Magnets:</b> neodymium discs, N35 or stronger, ~6&times;3 mm
      (the size the prior-art model below calls for), 10&ndash;14 pcs.
      <a href="https://www.amazon.com/s?k=neodymium+disc+magnets+6mm+x+3mm">
      Amazon search: neodymium disc magnets 6&times;3 mm</a></li>
    <li class="note">Already on hand: 68D TPU-for-AMS spool, 11 mm velcro
      strap, the X1C's magnetic steel plate.</li>
  </ul>

  <h2>prior art (verified technique)</h2>
  <ul>
    <li><a href="https://www.printables.com/model/357819-hex-pattern-for-tulle">
      Printables: &ldquo;Hex pattern for tulle&rdquo;</a> &mdash; same recipe:
      pause at height, tulle pinned with 6&times;3 N35 magnets to a magnetic
      PEI plate, keep the fabric dead flat.</li>
    <li><a href="https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-how-do-i-print-this-printing-help/printing-over-tulle-fabric">
      Prusa forum: printing over tulle</a> &mdash; magnets outside the build
      area; mesh lets melt flow through and bond mechanically.</li>
    <li><a href="https://3dprinterly.com/how-to-3d-print-on-fabric-8-steps/">
      3DPrinterly: How to 3D print on fabric (8 steps)</a> &mdash; the
      general pause-and-lay workflow, taut fabric, few base layers.</li>
  </ul>

  <h2>open before export</h2>
  <ul class="note">
    <li>20-min test square first: traces + one loaded strap tab + a diamond
      on scrap tulle; yank the tab before trusting a spinning motor to it.</li>
    <li>Tulle bond with 68D TPU at its nozzle temp &mdash; prior art is
      mostly PLA; verify on the test square.</li>
    <li>Flip-for-left-hand check still applies (fabric side vs element side
      now differ &mdash; elements face OUT, tulle sits on skin).</li>
  </ul>
</div>
</div>

<script>
const root=document.documentElement;
const seg=(id,fn)=>document.querySelectorAll('#'+id+' button').forEach(b=>
  b.onclick=()=>{document.querySelectorAll('#'+id+' button').forEach(x=>
    x.setAttribute('aria-pressed','false'));
    b.setAttribute('aria-pressed','true');fn(b);});
seg('rev',b=>{document.getElementById('vR4').hidden=b.dataset.v!=='vR4';
  document.getElementById('vR3').hidden=b.dataset.v!=='vR3';});
seg('tul',b=>{root.style.setProperty('--tulle',b.dataset.t);
  root.style.setProperty('--mesh',b.dataset.m);});
</script>
"""

html = (html.replace("__VIEWBOX__", viewbox)
        .replace("__OUTER__", outer_d)
        .replace("__PLATE__", plate_d)
        .replace("__CUTS__", r3_cuts)
        .replace("__R4__", r4_svg)
        .replace("__ROWS__", rows))
open("r3-review.html", "w").write(html)
print(f"wrote r3-review.html ({len(html) / 1024:.0f} KB)")

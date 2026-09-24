import os, json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck import DECK

HERE = os.path.dirname(os.path.abspath(__file__))
SL, AU = os.path.join(HERE,"slides"), os.path.join(HERE,"audio")
os.makedirs(SL, exist_ok=True); os.makedirs(AU, exist_ok=True)

W, H = 1920, 1080
BG      = (13, 10, 18)
PANEL   = (23, 18, 31)
INK     = (246, 242, 250)
MUTED   = (158, 147, 174)
DIM     = (104, 95, 120)
PINK    = (255, 95, 162)
LAV     = (185, 140, 255)
CYAN    = (88, 224, 255)
RED     = (255, 77, 94)
GREEN   = (74, 227, 155)
GOLD    = (255, 198, 88)

AV = "/System/Library/Fonts/Avenir Next.ttc"
IDX = dict(heavy=8, demi=2, medium=5, regular=7, light=10)
_fc = {}
def F(size, w="medium"):
    k = (size, w)
    if k not in _fc: _fc[k] = ImageFont.truetype(AV, size, index=IDX[w])
    return _fc[k]

def tw(d, s, f): return d.textlength(s, font=f)

def wrap(d, text, f, maxw):
    out, line = [], ""
    for word in text.split():
        t = (line + " " + word).strip()
        if tw(d, t, f) <= maxw or not line: line = t
        else: out.append(line); line = word
    if line: out.append(line)
    return out

def bubbles(d, seed=7):
    """faint decorative bubbles"""
    import random
    r = random.Random(seed)
    for _ in range(26):
        x, y = r.randint(-40, W), r.randint(-40, H)
        rad = r.randint(18, 130)
        c = (LAV if r.random() < .5 else PINK)
        a = r.randint(6, 16)
        d.ellipse([x-rad, y-rad, x+rad, y+rad], outline=(c[0], c[1], c[2], a), width=2)

def chrome(img, d, i, n, kicker=None):
    f = F(20, "demi")
    if kicker:
        d.text((96, 74), kicker.upper(), font=f, fill=PINK)
    lab = "BUBBLE CLOWN  ·  BUILD TUTORIAL"
    d.text((W-96, 74), lab, font=F(20, "medium"), fill=DIM, anchor="ra")
    # progress
    y = H-54
    d.rounded_rectangle([96, y, W-96, y+5], 3, fill=(38, 31, 50))
    frac = (i+1)/n
    d.rounded_rectangle([96, y, 96 + int((W-192)*frac), y+5], 3, fill=PINK)
    d.text((96, y-34), f"{i+1} / {n}", font=F(19, "medium"), fill=DIM)

def rich(d, x, y, lead, rest, maxw, fs=38, dry=False):
    """lead in accent demibold, rest in regular, wrapped together"""
    fl, fr = F(fs, "demi"), F(fs, "regular")
    toks = [(w, fl, LAV) for w in lead.split()] if lead else []
    if lead and rest: toks.append((" ", fr, INK))
    toks += [(w, fr, (214, 206, 226)) for w in rest.split()]
    cx, cy = x, y
    space_l, space_r = tw(d, " ", fl), tw(d, " ", fr)
    for t, f, c in toks:
        if t == " ": continue
        wpx = tw(d, t, f)
        if cx > x and cx + wpx > x + maxw:
            cx = x; cy += int(fs*1.42)
        if not dry: d.text((cx, cy), t, font=f, fill=c)
        cx += wpx + (space_l if f is fl else space_r)
    return cy + int(fs*1.42)

# ------------------------------------------------------------------ layouts
def lay_title(img, d, s, i, n):
    bubbles(d)
    t = s["title"]
    f = F(126, "heavy")
    d.text((W//2, 400), t, font=f, fill=INK, anchor="mm")
    d.rounded_rectangle([W//2-70, 480, W//2+70, 486], 3, fill=PINK)
    d.text((W//2, 560), s["sub"], font=F(52, "light"), fill=LAV, anchor="mm")
    if s.get("foot"):
        d.text((W//2, 680), s["foot"], font=F(30, "medium"), fill=MUTED, anchor="mm")

def lay_section(img, d, s, i, n):
    bubbles(d, seed=s["step"]*3)
    d.text((150, H//2-40), f"{s['step']:02d}", font=F(300, "heavy"), fill=(40, 30, 56), anchor="lm")
    x = 560
    d.text((x, H//2-96), f"STEP {s['step']} OF 12", font=F(30, "demi"), fill=PINK)
    for j, ln in enumerate(wrap(d, s["title"], F(84, "heavy"), W-x-140)):
        d.text((x, H//2-40+j*96), ln, font=F(84, "heavy"), fill=INK)
    if s.get("sub"):
        d.text((x, H//2+110), s["sub"], font=F(34, "light"), fill=MUTED)

def _heading(d, s, y=170):
    for j, ln in enumerate(wrap(d, s["title"], F(64, "heavy"), W-192)):
        d.text((96, y+j*76), ln, font=F(64, "heavy"), fill=INK)
        y2 = y+j*76
    return y2 + 120

def lay_bullets(img, d, s, i, n):
    ytop = _heading(d, s)
    items = s["items"]
    fs = 38 if len(items) <= 5 else 34
    blk = 0
    for it in items:
        lead, rest = (it.split("|", 1) + [""])[:2] if "|" in it else ("", it)
        blk += rich(d, 140, 0, lead.strip(), rest.strip(), W-140-110, fs, dry=True) + 26
    y = ytop + max(0, (H - 150 - ytop - blk)//2)
    for it in items:
        lead, rest = (it.split("|", 1) + [""])[:2] if "|" in it else ("", it)
        c = GREEN if s.get("ok") else PINK
        d.ellipse([96, y+14, 96+13, y+27], fill=c)
        ny = rich(d, 140, y, lead.strip(), rest.strip(), W-140-110, fs)
        y = ny + 26

def lay_numbered(img, d, s, i, n):
    ytop = _heading(d, s)
    items = s["items"]
    fs = 38 if len(items) <= 5 else 33
    blk = sum(len(wrap(d, it, F(fs, "regular"), W-160-110))*int(fs*1.4) + 28 for it in items)
    y = ytop + max(0, (H - 150 - ytop - blk)//2)
    for k, it in enumerate(items, 1):
        r = 21
        d.ellipse([96, y-2, 96+r*2, y-2+r*2], outline=LAV, width=3)
        d.text((96+r, y-2+r), str(k), font=F(22, "demi"), fill=LAV, anchor="mm")
        lines = wrap(d, it, F(fs, "regular"), W-160-110)
        for j, ln in enumerate(lines):
            d.text((160, y+j*int(fs*1.4)), ln, font=F(fs, "regular"), fill=(224, 216, 236))
        y += len(lines)*int(fs*1.4) + 28

def lay_table(img, d, s, i, n):
    y = _heading(d, s)
    cols, rows = s["cols"], s["rows"]
    nc = len(cols)
    widths = [0.30, 0.70] if nc == 2 else ([0.34, 0.30, 0.36] if nc == 3 else [1/nc]*nc)
    if nc == 2 and len(cols) == 2 and cols[0] == "Pin": widths = [0.14, 0.86]
    avail = W-192
    xs, acc = [], 96
    for wf in widths: xs.append(acc); acc += int(avail*wf)
    fs = 30 if len(rows) > 6 else 34
    d.text((xs[0], y), cols[0].upper(), font=F(21, "demi"), fill=PINK)
    for c, x in zip(cols[1:], xs[1:]):
        d.text((x, y), c.upper(), font=F(21, "demi"), fill=PINK)
    y += 44
    d.line([96, y, W-96, y], fill=(52, 42, 68), width=2); y += 20
    lh = int(fs*1.34)
    for k, r in enumerate(rows):
        cells = []
        for ci, (cell, x) in enumerate(zip(r, xs)):
            wgt = "demi" if ci == 0 else "regular"
            cells.append(wrap(d, cell, F(fs, wgt), int(avail*widths[ci])-34) if cell.strip() else [])
        nl = max(1, max((len(c) for c in cells), default=1))
        rh = nl*lh + 22
        if k % 2 == 0:
            d.rounded_rectangle([88, y-9, W-88, y+rh-13], 8, fill=(20, 16, 28))
        for ci, (lines, x) in enumerate(zip(cells, xs)):
            col = INK if ci == 0 else (206, 198, 220)
            wgt = "demi" if ci == 0 else "regular"
            for j, ln in enumerate(lines):
                d.text((x, y+j*lh), ln, font=F(fs, wgt), fill=col)
        y += rh
    if s.get("note"):
        d.text((96, min(y+34, H-190)), s["note"], font=F(27, "demi"), fill=GOLD)

def lay_warn(img, d, s, i, n):
    c = GREEN if s.get("ok") else RED
    d.rectangle([0, 0, W, H], fill=(16, 8, 12) if not s.get("ok") else (8, 18, 14))
    d.rectangle([0, 0, 18, H], fill=c)
    lines = s["title"].split("\n")
    fs = 78 if max(len(l) for l in lines) < 34 else 62
    total = len(lines)*int(fs*1.24)
    y = H//2 - total//2 - 60
    for ln in lines:
        d.text((130, y), ln, font=F(fs, "heavy"), fill=INK); y += int(fs*1.24)
    y += 30
    d.text((130, y), s["sub"], font=F(38, "light"), fill=c); y += 90
    if s.get("foot"):
        for ln in wrap(d, s["foot"], F(28, "regular"), W-300):
            d.text((130, y), ln, font=F(28, "regular"), fill=MUTED); y += 40

# ------------------------------------------------------------------ diagrams
def lay_timing(img, d, s, i, n):
    y0 = _heading(d, s)
    steps = [("SQUEEZE", "microswitch closes", PINK, 0),
             ("KICK", "blower over-drive pulse", GOLD, 1),
             ("COMET", "launches from the elbow", LAV, 1),
             ("BUBBLES", "comet lands, blower at speed", CYAN, 2),
             ("HOLD", "comets keep launching", LAV, 3),
             ("RELEASE", "motor cuts, fingertips flare", MUTED, 4)]
    x0, x1 = 230, W-230
    ty = y0 + 210
    d.line([x0, ty, x1, ty], fill=(52, 42, 68), width=4)
    gap = (x1-x0)/(len(steps)-1)
    for k, (nm, sub, c, _) in enumerate(steps):
        x = x0 + gap*k
        d.ellipse([x-16, ty-16, x+16, ty+16], fill=BG, outline=c, width=5)
        d.text((x, ty-70), nm, font=F(30, "heavy"), fill=c, anchor="mm")
        for j, ln in enumerate(wrap(d, sub, F(23, "regular"), int(gap)-40)):
            d.text((x, ty+52+j*32), ln, font=F(23, "regular"), fill=MUTED, anchor="ma")
    d.text((x0 + gap*3, ty+200), "~250 ms after the squeeze", font=F(27, "demi"), fill=CYAN, anchor="ma")
    d.text((W//2, H-190), "The light travel IS the spin-up delay - so it reads as causal, not as lag.",
           font=F(32, "demi"), fill=INK, anchor="mm")

def lay_modules(img, d, s, i, n):
    y0 = _heading(d, s)
    mods = [("POD", "upper arm", "brain · boost · shifter\nMOSFET · fuse · cell", LAV),
            ("SLEEVE", "forearm", "forearm strip\n15 px", CYAN),
            ("GLOVE", "hand", "hand strip 6 px\nthis hand's trigger", PINK),
            ("BUBBLER", "wrist", "bottle · cap · hose\nblower head", GOLD)]
    bw, bh, gap = 380, 250, 46
    x = (W - (bw*4 + gap*3))//2
    y = y0 + 90
    joints = ["elbow\nSM-6 + SM-2", "wrist\nSM-5", "wrist\nSM-2"]
    for k, (nm, where, body, c) in enumerate(mods):
        bx = x + k*(bw+gap)
        d.rounded_rectangle([bx, y, bx+bw, y+bh], 18, fill=PANEL, outline=c, width=3)
        d.text((bx+28, y+26), nm, font=F(38, "heavy"), fill=c)
        d.text((bx+28, y+76), where, font=F(24, "regular"), fill=MUTED)
        for j, ln in enumerate(body.split("\n")):
            d.text((bx+28, y+130+j*36), ln, font=F(26, "regular"), fill=(214, 206, 226))
        if k < 3:
            cx = bx+bw+gap//2
            d.line([bx+bw+8, y+bh//2, bx+bw+gap-8, y+bh//2], fill=(90, 78, 110), width=3)
            for j, ln in enumerate(joints[k].split("\n")):
                d.text((cx, y+bh+34+j*30), ln, font=F(21, "demi" if j else "regular"),
                       fill=GOLD if j else MUTED, anchor="ma")
    d.text((W//2, H-190), "Nothing is soldered end to end across a joint.",
           font=F(34, "demi"), fill=INK, anchor="mm")

def lay_strip(img, d, s, i, n):
    y0 = _heading(d, s)
    y = y0 + 170
    ax, bx = 190, W-190
    # forearm run
    fx0, fx1 = ax, ax + 700
    gx0, gx1 = fx1, fx1 + 300
    hx0, hx1 = gx1, gx1 + 380
    d.rounded_rectangle([fx0, y, fx1, y+56], 10, fill=(30, 24, 42), outline=CYAN, width=3)
    for k in range(15):
        px = fx0 + 26 + k*((fx1-fx0-52)/14)
        d.ellipse([px-9, y+19, px+9, y+37], fill=CYAN if k == 0 else (60, 130, 150))
    d.text((fx0, y-52), "FOREARM  ·  15 px  ·  ~21 cm", font=F(26, "demi"), fill=CYAN)
    d.text((fx0, y+80), "px 0 at the ELBOW", font=F(24, "demi"), fill=PINK)
    # gap
    for k in range(9):
        sx = gx0 + 14 + k*32
        d.line([sx, y+28, sx+16, y+28], fill=(110, 96, 132), width=4)
    d.text(((gx0+gx1)//2, y-52), "UMBILICAL  ·  ~8 cm", font=F(26, "demi"), fill=GOLD, anchor="ma")
    d.text(((gx0+gx1)//2, y+80), "JST-SM 5-pin\n3-4 cm above the crease", font=F(23, "regular"),
           fill=MUTED, anchor="ma", align="center")
    # hand
    d.rounded_rectangle([hx0, y, hx1, y+56], 10, fill=(30, 24, 42), outline=PINK, width=3)
    for k in range(6):
        px = hx0 + 30 + k*((hx1-hx0-60)/5)
        d.ellipse([px-9, y+19, px+9, y+37], fill=(190, 80, 130))
    d.text((hx0, y-52), "HAND  ·  6 px  ·  ~10 cm", font=F(26, "demi"), fill=PINK)
    d.text((hx1, y+80), "stop short of the fingertips", font=F(24, "regular"), fill=MUTED, anchor="ra")
    # arrow
    d.line([ax, y+180, bx-40, y+180], fill=(90, 78, 110), width=3)
    d.polygon([(bx-40, y+170), (bx-10, y+180), (bx-40, y+190)], fill=(90, 78, 110))
    d.text((ax, y+200), "data flows this way - arrows on BOTH pieces point at your fingers",
           font=F(26, "demi"), fill=INK)
    d.text((96, H-190), "One continuous strip across a flexing wrist cracks its traces within hours.",
           font=F(30, "demi"), fill=GOLD)

def lay_rail(img, d, s, i, n):
    y0 = _heading(d, s)
    y = y0 + 100
    # cell
    d.rounded_rectangle([140, y+90, 470, y+230], 16, fill=PANEL, outline=GREEN, width=3)
    d.text((305, y+128), "18650 CELL", font=F(34, "heavy"), fill=GREEN, anchor="ma")
    d.text((305, y+172), "protected · 3.7 V · swappable", font=F(23, "regular"), fill=MUTED, anchor="ma")
    # fuse
    d.rounded_rectangle([520, y+130, 700, y+190], 12, fill=(36, 29, 48), outline=GOLD, width=3)
    d.text((610, y+147), "2 A FUSE", font=F(26, "demi"), fill=GOLD, anchor="ma")
    d.line([470, y+160, 520, y+160], fill=(90, 78, 110), width=4)
    # split
    d.line([700, y+160, 800, y+160], fill=(90, 78, 110), width=4)
    d.line([800, y+40, 800, y+300], fill=(90, 78, 110), width=4)
    # top branch - motor
    d.line([800, y+40, 900, y+40], fill=(90, 78, 110), width=4)
    d.rounded_rectangle([900, y, 1180, y+80], 12, fill=(36, 29, 48), outline=LAV, width=3)
    d.text((1040, y+22), "MOSFET", font=F(30, "demi"), fill=LAV, anchor="ma")
    d.line([1180, y+40, 1280, y+40], fill=(90, 78, 110), width=4)
    d.rounded_rectangle([1280, y-10, 1700, y+90], 14, fill=PANEL, outline=CYAN, width=3)
    d.text((1490, y+14), "BLOWER MOTOR", font=F(32, "heavy"), fill=CYAN, anchor="ma")
    d.text((1490, y+54), "3.7 V native · 0.5-1.0 A", font=F(23, "regular"), fill=MUTED, anchor="ma")
    # bottom branch - 5V
    d.line([800, y+300, 900, y+300], fill=(90, 78, 110), width=4)
    d.rounded_rectangle([900, y+260, 1180, y+340], 12, fill=(36, 29, 48), outline=LAV, width=3)
    d.text((1040, y+282), "5 V BOOST", font=F(30, "demi"), fill=LAV, anchor="ma")
    d.line([1180, y+300, 1280, y+300], fill=(90, 78, 110), width=4)
    d.rounded_rectangle([1280, y+250, 1700, y+350], 14, fill=PANEL, outline=PINK, width=3)
    d.text((1490, y+274), "LED STRIP + XIAO", font=F(32, "heavy"), fill=PINK, anchor="ma")
    d.text((1490, y+314), "5 V · about 0.3 A", font=F(23, "regular"), fill=MUTED, anchor="ma")
    d.text((96, H-190), "Realistic peak from the cell: about 1.3 A.  A 2600 mAh cell outlasts a bottle of solution.",
           font=F(30, "demi"), fill=INK)

def lay_divider(img, d, s, i, n):
    y0 = _heading(d, s)
    y = y0 + 160
    x = 300
    d.text((x, y-70), "Battery + (after fuse)", font=F(28, "demi"), fill=GREEN)
    d.line([x, y, x+300, y], fill=(90, 78, 110), width=4)
    d.rounded_rectangle([x+300, y-26, x+480, y+26], 8, fill=(36, 29, 48), outline=LAV, width=3)
    d.text((x+390, y), "100 k", font=F(28, "demi"), fill=LAV, anchor="mm")
    d.line([x+480, y, x+660, y], fill=(90, 78, 110), width=4)
    # midpoint
    d.ellipse([x+650, y-11, x+672, y+11], fill=CYAN)
    d.line([x+661, y, x+661, y+150], fill=CYAN, width=4)
    d.text((x+686, y+120), "XIAO D0  (GPIO2)", font=F(30, "heavy"), fill=CYAN)
    d.text((x+686, y+164), "sits at exactly half the cell voltage", font=F(24, "regular"), fill=MUTED)
    d.line([x+660, y, x+840, y], fill=(90, 78, 110), width=4)
    d.rounded_rectangle([x+840, y-26, x+1020, y+26], 8, fill=(36, 29, 48), outline=LAV, width=3)
    d.text((x+930, y), "100 k", font=F(28, "demi"), fill=LAV, anchor="mm")
    d.line([x+1020, y, x+1180, y], fill=(90, 78, 110), width=4)
    d.line([x+1180, y-30, x+1180, y+30], fill=MUTED, width=4)
    d.text((x+1200, y-16), "GND", font=F(28, "demi"), fill=MUTED)
    d.text((96, H-190), "Below 3.4 V the firmware pulses the elbow pixel red - warning, not sudden death.",
           font=F(30, "demi"), fill=GOLD)

LAYOUTS = dict(title=lay_title, section=lay_section, bullets=lay_bullets, numbered=lay_numbered,
               table=lay_table, warn=lay_warn, timing=lay_timing, modules=lay_modules,
               strip=lay_strip, rail=lay_rail, divider=lay_divider)

# ------------------------------------------------------------------ build
def render():
    n = len(DECK)
    for i, s in enumerate(DECK):
        img = Image.new("RGB", (W, H), BG)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        LAYOUTS[s["kind"]](img, d, s, i, n)
        if s["kind"] not in ("title",):
            chrome(img, d, i, n, s.get("kicker"))
        img = Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB")
        img.save(os.path.join(SL, f"{i:03d}.png"))
    print(f"rendered {n} slides")

def narrate():
    man = []
    t = 0.0
    for i, s in enumerate(DECK):
        aif = os.path.join(AU, f"{i:03d}.aiff")
        txt = os.path.join(AU, f"{i:03d}.txt")
        open(txt, "w").write(s["say"])
        m4a = os.path.join(AU, f"{i:03d}.m4a")
        if not os.path.exists(aif):
            subprocess.run(["say", "-v", "Samantha", "-r", "174", "-f", txt, "-o", aif], check=True)
        if not os.path.exists(m4a):
            subprocess.run(["afconvert", "-f", "m4af", "-d", "aac@44100", "-b", "96000", aif, m4a], check=True)
        out = subprocess.run(["afinfo", m4a], capture_output=True, text=True).stdout
        dur = next(float(l.split(":")[1].split()[0]) for l in out.splitlines() if "estimated duration" in l)
        lead, tail = 0.35, (1.4 if s["kind"] in ("section", "warn", "title") else 0.9)
        total = lead + dur + tail
        man.append(dict(image=os.path.join(SL, f"{i:03d}.png"), audio=m4a,
                        start=round(t, 3), audioStart=round(t+lead, 3), dur=round(total, 3),
                        say=s["say"], title=s.get("title", "")))
        t += total
    json.dump(dict(width=W, height=H, fps=8, total=round(t, 3), slides=man),
              open(os.path.join(HERE, "manifest.json"), "w"), indent=1)

    def ts(x, comma=True):
        h, r = divmod(x, 3600); m, sec = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{sec:06.3f}".replace(".", "," if comma else ".")
    srt = []
    for k, (m, sl) in enumerate(zip(man, DECK), 1):
        words = m["say"].split()
        chunks, cur = [], []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 74 and w[-1] in ".,;:":
                chunks.append(" ".join(cur)); cur = []
            elif len(" ".join(cur)) > 96:
                chunks.append(" ".join(cur)); cur = []
        if cur: chunks.append(" ".join(cur))
        span = (m["dur"] - 1.25) / max(1, len(chunks))
        for j, c in enumerate(chunks):
            a = m["audioStart"] + j*span
            srt.append(f"{len(srt)+1}\n{ts(a)} --> {ts(a+span-0.06)}\n{c}\n")
    open(os.path.join(HERE, "tutorial.srt"), "w").write("\n".join(srt))

    chaps = []
    for m, sl in zip(man, DECK):
        if sl["kind"] == "section":
            chaps.append(f"{ts(m['start'], False)[:8]}  Step {sl['step']} - {sl['title']}")
        elif sl["kind"] == "title" and m["start"] == 0:
            chaps.append("00:00:00  Intro")
        elif sl.get("kicker") == "REFERENCE" and "wrong" in sl.get("title", ""):
            chaps.append(f"{ts(m['start'], False)[:8]}  Troubleshooting")
    open(os.path.join(HERE, "chapters.txt"), "w").write("\n".join(chaps) + "\n")
    print("wrote tutorial.srt and chapters.txt")
    print(f"narrated {len(man)} slides, total {t/60:.1f} min")

if __name__ == "__main__":
    render(); narrate()

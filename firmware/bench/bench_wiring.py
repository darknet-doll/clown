#!/usr/bin/env python3
"""Draw the full bench rig - trigger, strip and motor - as a breadboard layout.

One drawing, hole by hole, for a standard breadboard (rows 1-30, columns a-j,
a power-rail pair down each side). Every connection is numbered, and the
numbers match the checklist in README.md.

Grounding is the point of this layout:
  - motor current never touches a rail: cell -, Q1 S and R5 all meet in row 22,
    and one jumper (#25) is the only path from that row to the ground rail
  - each ground rail goes straight to the XIAO's own GND pin (#2, #3), no
    rail-to-rail bridge
  - the left red rail is not used at all

Usage:  python3 firmware/bench/bench_wiring.py
Writes bench-wiring.svg; render to PNG with
        sips -s format png bench-wiring.svg --out bench-wiring.png
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "bench-wiring.svg")

W, H = 1720, 1150
P = 30                       # hole pitch
X0, Y0 = 330, 190            # hole a1

COLX = {c: X0 + k * P for k, c in enumerate("abcde")}
GAP = 2.4 * P
COLX.update({c: X0 + 4 * P + GAP + k * P for k, c in enumerate("fghij")})
COLX["L+"] = COLX["a"] - 1.7 * P
COLX["L-"] = COLX["a"] - 2.7 * P
COLX["R+"] = COLX["j"] + 1.7 * P
COLX["R-"] = COLX["j"] + 2.7 * P
GAPX = (COLX["e"] + COLX["f"]) / 2

RED, BLACK, BLUE = "#d93025", "#202124", "#1a73e8"
ORANGE, GREEN, PURPLE = "#e8710a", "#188038", "#9334e6"
TAN, GREY, MUTED = "#c8a97e", "#9aa0a6", "#5f6368"

out = []


def add(s):
    out.append(s)


def X(col):
    return COLX[col]


def Y(row):
    return Y0 + (row - 1) * P


def H_(spec):
    """'c22' -> (x, y); 'L-:5' -> rail hole at row 5."""
    if ":" in spec:
        col, row = spec.split(":")
        return X(col), Y(float(row))
    return X(spec[0]), Y(int(spec[1:]))


def text(x, y, s, size=13, color=BLACK, anchor="start", weight="normal"):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{color}" '
        f'text-anchor="{anchor}" font-weight="{weight}">{s}</text>')


def tag(x, y, n, color):
    add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{color}" stroke="#fff" stroke-width="2"/>')
    text(x, y + 4.5, str(n), 12, "#fff", "middle", "bold")


def wire(points, color, n, tag_at, width=4.5):
    pts = [H_(p) if isinstance(p, str) else p for p in points]
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>')
    for x, y in (pts[0], pts[-1]):
        add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="#fff" stroke-width="1.5"/>')
    tag(*tag_at, n, color)


def part(a, b, body, n, tag_at, label=None, label_at=None, band=False):
    (x1, y1), (x2, y2) = H_(a) if isinstance(a, str) else a, H_(b) if isinstance(b, str) else b
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GREY}" stroke-width="3"/>')
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    vertical = abs(y2 - y1) >= abs(x2 - x1)
    w, h = (16, 38) if vertical else (38, 16)
    add(f'<rect x="{mx - w / 2:.1f}" y="{my - h / 2:.1f}" width="{w}" height="{h}" rx="5" '
        f'fill="{body}" stroke="{BLACK}" stroke-width="1.5"/>')
    if band:  # cathode band on the b end
        if vertical:
            by = my + h / 2 - 8 if y2 > y1 else my - h / 2 + 2
            add(f'<rect x="{mx - w / 2:.1f}" y="{by:.1f}" width="{w}" height="6" fill="#e8eaed"/>')
        else:
            bx = mx + w / 2 - 8 if x2 > x1 else mx - w / 2 + 2
            add(f'<rect x="{bx:.1f}" y="{my - h / 2:.1f}" width="6" height="{h}" fill="#e8eaed"/>')
    for x, y in ((x1, y1), (x2, y2)):
        add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{GREY}" stroke="#fff" stroke-width="1.5"/>')
    tag(*tag_at, n, "#795548")
    if label:
        lx, ly, anchor = label_at
        for k, line in enumerate(label.split("\n")):
            text(lx, ly + k * 15, line, 12.5 if k == 0 else 11.5, BLACK if k == 0 else MUTED,
                 anchor, "bold" if k == 0 else "normal")


def block(x, y, w, h, title, sub=None, fill="#fff"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{BLACK}" stroke-width="1.5"/>')
    text(x + w / 2, y + 22, title, 14, BLACK, "middle", "bold")
    if sub:
        text(x + w / 2, y + 39, sub, 11.5, RED if "LAST" in sub else MUTED, "middle", "bold" if "LAST" in sub else "normal")


# ================================================================= header
add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
text(40, 46, "Bench rig — trigger + LED strip + motor", 26, BLACK, "start", "bold")
text(40, 72, "Breadboard upright, row 1 at the top. Each numbered wire or part is one step in README.md — "
     "do them in number order.", 15, MUTED)
text(40, 94, "Match the rails by COLOUR on your own board, not by position. Use rows 1–30 only "
     "(long boards often split their rails further down).", 15, MUTED)

# ================================================================= breadboard
bx1, bx2 = X("L-") - 26, X("R-") + 26
add(f'<rect x="{bx1:.1f}" y="{Y0 - 52}" width="{bx2 - bx1:.1f}" height="{29 * P + 84}" rx="12" '
    f'fill="#f8f5ec" stroke="#d6d0bf" stroke-width="2"/>')
add(f'<rect x="{GAPX - 16:.1f}" y="{Y0 - 30}" width="32" height="{29 * P + 44}" fill="#ece6d4"/>')

for col, color, sym in (("L-", BLUE, "−"), ("L+", RED, "+"), ("R+", RED, "+"), ("R-", BLUE, "−")):
    x = X(col)
    add(f'<line x1="{x:.1f}" y1="{Y0 - 26}" x2="{x:.1f}" y2="{Y(30) + 14}" stroke="{color}" stroke-width="2.5" opacity="0.55"/>')
    text(x, Y0 - 32, sym, 20, color, "middle", "bold")
    for r in range(1, 31):
        add(f'<circle cx="{x:.1f}" cy="{Y(r)}" r="3" fill="#bdb6a4"/>')
for col in "abcdefghij":
    text(X(col), Y0 - 24, col, 13, "#80868b", "middle", "bold")
    for r in range(1, 31):
        add(f'<circle cx="{X(col):.1f}" cy="{Y(r)}" r="3" fill="#bdb6a4"/>')
for r in range(1, 31):
    text(X("L-") - 34, Y(r) + 4, str(r), 11, "#80868b", "end")
    text(X("R-") + 34, Y(r) + 4, str(r), 11, "#80868b", "start")

# Left red rail: unused.
lx = X("L+")
add(f'<rect x="{lx - 11:.1f}" y="{Y(6) - 10}" width="22" height="{4 * P + 20}" rx="5" fill="#fff" stroke="{RED}" stroke-width="1.5"/>')
for k, ch in enumerate("NONE"):
    text(lx, Y(6) + 10 + k * 28, ch, 13, RED, "middle", "bold")
text(lx, Y0 - 56, "unused", 11, RED, "middle", "bold")

# ================================================================= XIAO (U3), rows 1-7, pins in c and h
xa, xb = X("c") - 20, X("h") + 20
add(f'<rect x="{xa:.1f}" y="{Y0 - 26}" width="{xb - xa:.1f}" height="{6 * P + 52}" rx="12" fill="#1f6f43" stroke="#0f3d24" stroke-width="2"/>')
ux = (xa + xb) / 2
add(f'<rect x="{ux - 34:.1f}" y="{Y0 - 54}" width="68" height="34" rx="8" fill="#9aa0a6" stroke="#555"/>')
text(ux, Y0 - 32, "USB-C", 12, BLACK, "middle", "bold")
text(ux, Y(3) + 2, "XIAO", 17, "#fff", "middle", "bold")
text(ux, Y(4) + 0, "ESP32-C3", 14, "#fff", "middle")
text(ux, Y(5) - 2, "U3", 12, "#cfe8d6", "middle")
for k, (ln, rn) in enumerate(zip(["D0", "D1", "D2", "D3", "D4", "D5", "D6"],
                                 ["5V", "GND", "3V3", "D10", "D9", "D8", "D7"])):
    for col, nm, dx, anchor in (("c", ln, 13, "start"), ("h", rn, -13, "end")):
        x, y = X(col), Y(k + 1)
        hot = nm in ("D1", "D2", "5V", "GND", "D10")
        add(f'<circle cx="{x:.1f}" cy="{y}" r="7" fill="#e8c34a" stroke="#7a5d00" stroke-width="1.5"/>')
        text(x + dx, y + 4.5, nm, 13, "#fff" if hot else "#8fc2a2", anchor, "bold" if hot else "normal")

# ================================================================= 74AHCT125 (U2), rows 10-16, legs in e and f
ca, cb = X("e") - 12, X("f") + 12
add(f'<rect x="{ca:.1f}" y="{Y(10) - 18}" width="{cb - ca:.1f}" height="{6 * P + 36}" rx="5" fill="#2b2b2b"/>')
add(f'<path d="M {GAPX - 10:.1f} {Y(10) - 18} a 10 10 0 0 0 20 0" fill="#f8f5ec"/>')
text(GAPX, Y(10) - 24, "notch", 11, BLACK, "middle", "bold")
text(GAPX, Y(13) - 2, "U2", 14, "#fff", "middle", "bold")
text(GAPX, Y(13) + 14, "AHCT", 9.5, "#ccc", "middle")
text(GAPX, Y(13) + 25, "125", 9.5, "#ccc", "middle")
for k in range(7):
    for col, num in (("e", k + 1), ("f", 14 - k)):
        x, y = X(col), Y(10 + k)
        add(f'<rect x="{x - 5:.1f}" y="{y - 5}" width="10" height="10" fill="#d0d0d0"/>')
        text(x + (11 if col == "e" else -11), y + 4.5, str(num), 11, "#fff", "start" if col == "e" else "end", "bold")
# What each chip pin is, in the gutters beside the rails.
lnames = ["1OE", "1A ← D10", "1Y → strip", "2OE", "2A ← D2", "2Y → gate", "GND"]
rnames = ["Vcc", "4OE", "4A", "4Y — empty", "3OE", "3A", "3Y — empty"]

# ================================================================= Q1, rows 20-22, legs in d
# Seen from above a TO-220 standing upright is a thin bar. Printed face toward
# the LEFT edge puts G nearest row 1.
qx = X("d")
add(f'<rect x="{qx + 6:.1f}" y="{Y(20) - 18}" width="12" height="{2 * P + 36}" rx="2" fill="#2b2b2b"/>')
add(f'<rect x="{qx + 18:.1f}" y="{Y(20) - 18}" width="5" height="{2 * P + 36}" fill="#b0b0b0"/>')
for k, nm in enumerate(("G", "D", "S")):
    y = Y(20 + k)
    add(f'<line x1="{qx:.1f}" y1="{y}" x2="{qx + 6:.1f}" y2="{y}" stroke="#b0b0b0" stroke-width="3.5"/>')
    add(f'<circle cx="{qx:.1f}" cy="{y}" r="5" fill="#b0b0b0" stroke="#555"/>')
    text(qx + 36, y + 4.5, nm, 13, BLACK, "middle", "bold")

# ================================================================= connections, in build order
# --- power and ground, straight from the XIAO's own pins
wire(["i1", "R+:1"], RED, 1, (X("j") + 0.85 * P, Y(1) - 16))
wire(["i2", "R-:2"], BLACK, 2, (X("j") + 0.85 * P, Y(2) + 16))
wire(["j2", (X("j"), Y0 - 72), (X("L-"), Y0 - 72), "L-:1"], BLACK, 3, (X("a") + 0.5 * P, Y0 - 72))

# --- chip tie-offs
wire(["a10", "L-:10"], BLACK, 4, (X("a") - 0.45 * P, Y(10) - 15))
wire(["a13", "L-:13"], BLACK, 5, (X("a") - 0.45 * P, Y(13) - 15))
wire(["a16", "L-:16"], BLACK, 6, (X("a") - 0.45 * P, Y(16) - 15))
wire(["i10", "R+:9"], RED, 7, ((X("i") + X("R+")) / 2 + 6, Y(9.5) - 14))
part("j10", "R-:10", "#fdd663", 8, (X("R-") + 62, Y(10)))
wire(["j11", "R+:11"], RED, 9, (X("R+") + 0.5 * P, Y(11) + 4))
wire(["j12", "R-:12"], BLACK, 10, (X("j") + 0.85 * P, Y(12) + 15))
wire(["j14", "R+:14"], RED, 11, (X("j") + 0.85 * P, Y(14) - 15))
wire(["j15", "R-:15"], BLACK, 12, (X("j") + 0.85 * P, Y(15) + 15))

# --- signals from the XIAO
wire(["j4", (X("j"), Y(8.5)), (X("d"), Y(8.5)), "d11"], ORANGE, 13, (X("g"), Y(8.5)))
lane = X("a") - 0.85 * P
wire(["a3", (lane, Y(3)), (lane, Y(14)), "a14"], GREEN, 14, (lane, Y(6)))
part("d14", "d16", TAN, 15, (X("d"), Y(12.6)))

# --- trigger, off-board left
tx = X("L-") - 34
block(30, Y(1) - 22, 150, 4 * P + 10, "TRIGGER", "kit microswitch")
text(172, Y(2) + 4.5, "NO", 12, BLACK, "end", "bold")
text(172, Y(4) + 4.5, "COM", 12, BLACK, "end", "bold")
wire([(180, Y(2)), "a2"], PURPLE, 16, (tx, Y(2)), 3.5)
wire([(180, Y(4)), "L-:4"], BLACK, 17, (tx, Y(4)), 3.5)

# --- strip path
part("b12", "b18", TAN, 18, (X("a") + 8, Y(15)))
wire(["d18", "g18"], ORANGE, 19, (GAPX, Y(18) + 17))
stx, sty = X("R-") + 110, Y(16) - 14
block(stx, sty, 210, 5 * P + 40, "LED STRIP — 10 px", "input end (arrows point away)")
for k, (nm, c, row) in enumerate((("DIN", ORANGE, 18), ("5V", RED, 19.5), ("GND", BLACK, 21))):
    text(stx + 22, Y(row) + 4.5, nm, 13, c, "start", "bold")
wire([(stx, Y(18)), "j18"], ORANGE, 20, (X("R-") + 72, Y(18)), 3.5)
wire([(stx, Y(19.5)), "R+:19.5"], RED, 21, (X("R-") + 72, Y(19.5)), 3.5)
wire([(stx, Y(21)), "R-:21"], BLACK, 22, (X("R-") + 72, Y(21)), 3.5)

# --- motor side (no cell yet)
part("c15", "c20", TAN, 23, (X("c") + 0.5 * P, Y(19) - 2))
part("b20", "b22", TAN, 24, (X("b"), Y(19)))
wire(["a22", "L-:22"], BLACK, 25, (X("a") - 0.45 * P, Y(22) + 15))
part("c21", "c25", "#3c4043", 26, (X("d") + 2, Y(24) - 2), band=True)
part("b25", "b27", "#f6c26b", 27, (X("c") + 2, Y(26)))

block(30, Y(20) - 22, 150, 6 * P + 10, "MOTOR", "M1 — kit blower")
text(172, Y(21) + 4.5, "−", 15, BLACK, "end", "bold")
text(172, Y(25) + 4.5, "+", 15, RED, "end", "bold")
wire([(180, Y(21)), "a21"], BLACK, 28, (tx, Y(21)), 3.5)
wire([(180, Y(25)), "a25"], RED, 29, (tx, Y(25)), 3.5)

block(30, Y(26.6), 150, 3.4 * P + 20, "18650 CELL", "connect LAST", "#fff8e1")
text(172, Y(28) + 4.5, "+", 15, RED, "end", "bold")
text(172, Y(29.6) + 4.5, "−", 15, BLACK, "end", "bold")
wire([(180, Y(28)), (X("a") - 0.4 * P, Y(28)), (X("a") - 0.4 * P, Y(27)), "a27"], RED, 30, (tx, Y(28)), 3.5)
wire([(180, Y(29.6)), (X("e"), Y(29.6)), "e22"], BLACK, 31, (tx, Y(29.6)), 3.5)

# --- part labels, in the empty right half of the board and beside it
def note(row, title, sub=None, x=None):
    x = X("f") - 6 if x is None else x
    text(x, Y(row) + 4, title, 12.5, BLACK, "start", "bold")
    if sub:
        text(x, Y(row) + 19, sub, 11.5, MUTED)

text(X("R-") + 80, Y(10) - 2, "C2  0.1 µF ceramic (104)", 12.5, BLACK, "start", "bold")
text(X("R-") + 80, Y(10) + 13, "pin-14 row → − rail, legs short", 11.5, MUTED)
note(19.6, "18 = R3 330 Ω  b12 → b18")
note(20.6, "23 = R4 100 Ω  c15 → c20")
note(21.6, "24 = R5 10 kΩ  b20 → b22")
note(22.6, "Q1 RFP30N06LE in d20 / d21 / d22", "printed face → LEFT edge, tab → gap")
note(24.6, "26 = CR1 1N5819  c21 → c25", "band (stripe) in row 25")
note(26.6, "27 = F1 GBX-185  b25 → b27")
note(28.0, "15 = 10 kΩ  d14 → d16", "pin-5 pulldown into the pin-7 (GND) row")


# ================================================================= legend (right)
lx0 = X("R-") + 340
ly = 150
text(lx0, ly, "ROWS", 16, BLACK, "start", "bold")
rows = [
    ("1–7", "XIAO (U3). USB-C off the top. Use free holes outside it."),
    ("10–16", "74AHCT125 (U2) in e / f. Notch toward row 10."),
    ("18", "Strip data: R3 end + jumper 19 (left) → strip DIN (right)."),
    ("20 / 21 / 22", "Q1 gate / drain / source, all in column d."),
    ("22 left", "MOTOR GROUND — Q1 S, R5, cell −, jumper 25. Nothing else."),
    ("25 left", "BATTERY + after fuse — F1, CR1 band, motor +."),
    ("27 left", "CELL + — F1 and cell + only."),
]
for k, (r, d) in enumerate(rows):
    text(lx0, ly + 28 + k * 22, r, 13, BLACK, "start", "bold")
    text(lx0 + 98, ly + 28 + k * 22, d, 13, BLACK)

ly2 = ly + 28 + len(rows) * 22 + 24
text(lx0, ly2, "CHIP PINS", 16, BLACK, "start", "bold")
for k in range(7):
    y = ly2 + 26 + k * 21
    text(lx0, y, f"{k + 1:>2}  {lnames[k]}", 13, BLACK, "start", "bold" if k in (1, 2, 4, 5) else "normal")
    text(lx0 + 200, y, f"{14 - k:>2}  {rnames[k]}", 13, BLACK)

ly3 = ly2 + 26 + 7 * 21 + 24
text(lx0, ly3, "RULES", 16, BLACK, "start", "bold")
rules = [
    "Everything unplugged while you wire.",
    "Left red rail: nothing at all.",
    "Cell + never touches a rail — rows 27 and 25 only.",
    "Chip pins 8 and 11 stay empty. Pin 6 → R4 only.",
    "On: USB first, cell last.  Off: cell first, then USB.",
]
for k, s in enumerate(rules):
    text(lx0, ly3 + 26 + k * 21, "•  " + s, 13, BLACK)

ly4 = ly3 + 26 + len(rules) * 21 + 24
text(lx0, ly4, "KEY", 16, BLACK, "start", "bold")
for k, (c, s) in enumerate(((RED, "5 V or battery +"), (BLACK, "ground"), (ORANGE, "LED data (D10)"),
                             (GREEN, "motor signal (D2)"), (PURPLE, "trigger (D1)"), ("#795548", "numbered part"))):
    add(f'<rect x="{lx0}" y="{ly4 + 16 + k * 21}" width="26" height="9" rx="2" fill="{c}"/>')
    text(lx0 + 36, ly4 + 25 + k * 21, s, 13, BLACK)

with open(OUT, "w") as f:
    f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">\n')
    f.write("\n".join(out))
    f.write("\n</svg>\n")
print("wrote", os.path.relpath(OUT))

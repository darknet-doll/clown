#!/usr/bin/env python3
"""Generate the clown arm schematic and harness diagram as SVG.

Two sheets, both for ONE arm. The other arm is identical.

  sheet 1  clown-arm-schematic.svg  the electrical schematic
  sheet 2  clown-arm-harness.svg    which net rides which pin, module by module

Also rewrites the generated net table inside SCHEMATIC.md, between the
<!-- generated:nets --> markers, so the drawing and the table cannot drift.

NAMING RULES - these are requirements, not style preferences. Anything added to
this drawing has to keep them true:

  1. One name, one thing. No designator, pin name or net name may refer to two
     different things anywhere in the design.
  2. Diodes are CR1, CR2 - never D1, D2. The XIAO's silkscreen already owns the
     names D0 through D10, so a "D" designator would collide with a pin. CR is
     the other standard diode prefix (IEEE 315 / ASME Y14.44); Q1's drain is
     then the only "D" on the sheet.
  3. A pin is never named on its own. Write the owner first: U3 GPIO4, U2 2A,
     J2-3, Q1 G. Bare "GPIO4" or "pin 3" is not a name.
  4. XIAO pins are named by GPIO number. The silkscreen D-number appears in one
     place only - the silk map printed under U3 on sheet 1, and the pin map in
     SCHEMATIC.md - and always with the word "silk" next to it.
  5. Net names are UPPER_SNAKE, and no net shares a name with a designator or a
     pin. A flag carries the net name and nothing else; where the net goes is a
     separate note beside it.

Usage:  python3 docs/schematic/schematic.py
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

INK = "#1A1A1A"
WIRE = "#1A1A1A"
ACCENT = "#C2185B"
MUTED = "#5A5A5A"
PANEL = "#F5F0F2"
PAPER = "#FFFFFF"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------

class Sheet:
    def __init__(self, w, h, title, subtitle):
        self.w, self.h = w, h
        self.o = []
        self.o.append(
            '<rect x="0" y="0" width="%d" height="%d" fill="%s"/>' % (w, h, PAPER))
        self.text(40, 52, title, size=21, weight="bold")
        self.text(40, 76, subtitle, size=11, fill=MUTED)
        self.line(40, 92, w - 40, 92, width=1.6)

    # -- raw ---------------------------------------------------------------
    def add(self, s):
        self.o.append(s)

    def text(self, x, y, s, size=11, fill=INK, anchor="start", weight="normal"):
        self.o.append(
            '<text x="%g" y="%g" font-family="%s" font-size="%g" fill="%s" '
            'text-anchor="%s" font-weight="%s">%s</text>'
            % (x, y, MONO, size, fill, anchor, weight, esc(s)))

    def line(self, x1, y1, x2, y2, width=2.0, color=WIRE, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.o.append(
            '<line x1="%g" y1="%g" x2="%g" y2="%g" stroke="%s" stroke-width="%g" '
            'stroke-linecap="round"%s/>' % (x1, y1, x2, y2, color, width, d))

    def wire(self, pts, width=2.0, color=WIRE):
        d = " ".join("%g,%g" % p for p in pts)
        self.o.append(
            '<polyline points="%s" fill="none" stroke="%s" stroke-width="%g" '
            'stroke-linecap="round" stroke-linejoin="round"/>' % (d, color, width))

    def dot(self, x, y, r=4.5):
        self.o.append('<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (x, y, r, WIRE))

    def rect(self, x, y, w, h, fill="none", stroke=INK, width=2.0, rx=4, dash=None):
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        self.o.append(
            '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" '
            'stroke="%s" stroke-width="%g"%s/>' % (x, y, w, h, rx, fill, stroke, width, d))

    def save(self, name):
        path = os.path.join(HERE, name)
        with open(path, "w") as f:
            f.write(
                '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                'viewBox="0 0 %d %d" role="img">\n' % (self.w, self.h, self.w, self.h)
                + "\n".join(self.o) + "\n</svg>\n")
        return os.path.relpath(path, ROOT)

    # -- symbols -----------------------------------------------------------
    def block(self, x, y, w, h, ref, name, note=None, pad=PANEL, hdr=0):
        """A boxed component: IC, module, sub-assembly.

        hdr pushes the caption down, to clear pins entering the top edge.
        """
        self.rect(x, y, w, h, fill=pad)
        self.text(x + w / 2, y + 26 + hdr, ref, size=13, anchor="middle",
                  weight="bold")
        self.text(x + w / 2, y + 44 + hdr, name, size=10.5, anchor="middle")
        if note:
            self.text(x + w / 2, y + 62 + hdr, note, size=9.5, anchor="middle",
                      fill=MUTED)

    def pin(self, x, y, side, label, size=9.5):
        """A pin stub on a block edge, with its label inside the block."""
        dx = {"l": -18, "r": 18, "t": 0, "b": 0}[side]
        dy = {"l": 0, "r": 0, "t": -18, "b": 18}[side]
        self.line(x, y, x + dx, y + dy)
        if side == "l":
            self.text(x + 8, y + 3.5, label, size=size, fill=MUTED)
        elif side == "r":
            self.text(x - 8, y + 3.5, label, size=size, fill=MUTED, anchor="end")
        elif side == "t":
            self.text(x, y + 16, label, size=size, fill=MUTED, anchor="middle")
        else:
            self.text(x, y - 8, label, size=size, fill=MUTED, anchor="middle")
        return (x + dx, y + dy)

    def resistor(self, x, y, orient, ref, value):
        """IEC rectangle. (x, y) is the centre. Returns both terminals."""
        if orient == "h":
            self.rect(x - 34, y - 13, 68, 26, fill=PAPER, width=2.0, rx=2)
            self.text(x, y - 22, ref, size=10, anchor="middle", weight="bold")
            self.text(x, y + 34, value, size=10, anchor="middle")
            return (x - 34, y), (x + 34, y)
        self.rect(x - 13, y - 34, 26, 68, fill=PAPER, width=2.0, rx=2)
        self.text(x + 22, y - 6, ref, size=10, weight="bold")
        self.text(x + 22, y + 10, value, size=10)
        return (x, y - 34), (x, y + 34)

    def cap_polar(self, x, y, ref, value):
        """Polarised cap, vertical, + terminal on top."""
        self.line(x - 26, y - 9, x + 26, y - 9, width=3.0)
        self.add('<path d="M %g %g A 30 16 0 0 0 %g %g" fill="none" stroke="%s" '
                 'stroke-width="3"/>' % (x - 26, y + 11, x + 26, y + 11, WIRE))
        self.text(x - 34, y - 16, "+", size=13, anchor="end", weight="bold")
        self.text(x + 34, y - 6, ref, size=10, weight="bold")
        self.text(x + 34, y + 10, value, size=10)
        return (x, y - 9), (x, y + 13)

    def cap(self, x, y, ref, value):
        """Non-polarised cap, vertical. Returns both terminals."""
        self.line(x - 26, y - 9, x + 26, y - 9, width=3.0)
        self.line(x - 26, y + 9, x + 26, y + 9, width=3.0)
        self.text(x + 34, y - 6, ref, size=10, weight="bold")
        self.text(x + 34, y + 10, value, size=10)
        return (x, y - 9), (x, y + 9)

    def diode(self, x, y, orient, ref, value, flip=False):
        """Schottky. orient 'v': current flows down unless flip. Returns (a, k)."""
        if orient == "v":
            s = -1 if flip else 1
            tri = "M %g %g L %g %g L %g %g Z" % (
                x - 20, y - 16 * s, x + 20, y - 16 * s, x, y + 14 * s)
            self.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2" '
                     'stroke-linejoin="round"/>' % (tri, INK, WIRE))
            self.line(x - 22, y + 14 * s, x + 22, y + 14 * s, width=3.0)
            self.add('<path d="M %g %g l 8 %g M %g %g l -8 %g" fill="none" '
                     'stroke="%s" stroke-width="2.4"/>'
                     % (x - 22, y + 14 * s, 9 * s, x + 22, y + 14 * s, 9 * s, WIRE))
            self.text(x + 32, y - 6, ref, size=10, weight="bold")
            self.text(x + 32, y + 10, value, size=10)
            return (x, y - 20 * s), (x, y + 20 * s)
        tri = "M %g %g L %g %g L %g %g Z" % (x - 16, y - 20, x - 16, y + 20, x + 14, y)
        self.add('<path d="%s" fill="%s" stroke="%s" stroke-width="2" '
                 'stroke-linejoin="round"/>' % (tri, INK, WIRE))
        self.line(x + 14, y - 22, x + 14, y + 22, width=3.0)
        self.text(x, y - 32, ref, size=10, anchor="middle", weight="bold")
        self.text(x, y + 42, value, size=10, anchor="middle")
        return (x - 16, y), (x + 20, y)

    def fuse(self, x, y, ref, value):
        self.rect(x - 42, y - 15, 84, 30, fill=PAPER, rx=2)
        self.line(x - 42, y, x + 42, y, width=2.0)
        self.text(x, y - 24, ref, size=10, anchor="middle", weight="bold")
        self.text(x, y + 36, value, size=10, anchor="middle")
        return (x - 42, y), (x + 42, y)

    def spst(self, x, y, ref, value):
        """Open switch, horizontal."""
        self.line(x - 40, y, x - 22, y)
        self.line(x + 22, y, x + 40, y)
        self.line(x - 22, y, x + 18, y - 26)
        self.dot(x - 22, y, 4)
        self.dot(x + 22, y, 4)
        self.text(x, y - 40, ref, size=10, anchor="middle", weight="bold")
        self.text(x, y + 26, value, size=10, anchor="middle")
        return (x - 40, y), (x + 40, y)

    def mosfet(self, x, y, ref, value):
        """N-channel enhancement MOSFET. (x, y) is the gate terminal."""
        gx = x + 46           # gate bar
        cx = gx + 14          # channel
        self.line(x, y, gx, y)                       # gate lead
        self.line(gx, y - 34, gx, y + 34, width=3.0)  # gate bar
        for oy in (-28, 0, 28):                      # channel segments
            self.line(cx, y + oy - 9, cx, y + oy + 9, width=3.0)
        self.line(cx, y - 28, cx + 40, y - 28)       # drain
        self.line(cx + 40, y - 28, cx + 40, y - 70)
        self.line(cx, y + 28, cx + 40, y + 28)       # source
        self.line(cx + 40, y + 28, cx + 40, y + 70)
        self.line(cx, y, cx + 40, y)                 # body tie
        self.line(cx + 40, y, cx + 40, y + 28)
        self.text(cx + 58, y - 46, ref, size=11, weight="bold")
        self.text(cx + 58, y - 30, value, size=10)
        self.text(cx + 52, y - 66, "D", size=9.5, fill=MUTED)
        self.text(cx + 52, y + 70, "S", size=9.5, fill=MUTED)
        self.text(x + 18, y - 10, "G", size=9.5, fill=MUTED)
        return (cx + 40, y - 70), (cx + 40, y + 70)   # drain, source

    def motor(self, x, y, ref, value):
        self.add('<circle cx="%g" cy="%g" r="34" fill="%s" stroke="%s" '
                 'stroke-width="2"/>' % (x, y, PAPER, INK))
        self.text(x, y + 7, "M", size=19, anchor="middle", weight="bold")
        self.text(x + 44, y - 6, ref, size=10.5, weight="bold")
        self.text(x + 44, y + 10, value, size=10)
        return (x, y - 34), (x, y + 34)

    def gnd(self, x, y, label="GND"):
        """Ground symbol, stem entering from above at (x, y)."""
        self.line(x, y, x, y + 16)
        for i, w in enumerate((22, 14, 7)):
            self.line(x - w, y + 16 + i * 7, x + w, y + 16 + i * 7, width=2.6)
        if label:
            self.text(x, y + 56, label, size=9, anchor="middle", fill=MUTED)

    def flag(self, x, y, text, direction="r"):
        """A net-label flag: this wire continues at the matching flag."""
        w = 11 * len(text) + 30
        if direction == "r":
            pts = [(x, y - 15), (x + w - 16, y - 15), (x + w, y),
                   (x + w - 16, y + 15), (x, y + 15)]
            tx, anchor = x + 12, "start"
        else:
            pts = [(x, y - 15), (x - w + 16, y - 15), (x - w, y),
                   (x - w + 16, y + 15), (x, y + 15)]
            tx, anchor = x - 12, "end"
        d = " ".join("%g,%g" % p for p in pts)
        self.add('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.6"/>'
                 % (d, PANEL, ACCENT))
        self.text(tx, y + 4, text, size=10.5, anchor=anchor, weight="bold")

    def conn(self, x, y, pins, ref, name, pitch=44):
        """Vertical connector body. Returns [(left, right)] terminals per pin."""
        h = pitch * len(pins) + 26
        self.rect(x, y, 56, h, fill=PANEL, rx=6)
        self.text(x + 28, y - 26, ref, size=11, anchor="middle", weight="bold")
        self.text(x + 28, y - 10, name, size=9.5, anchor="middle", fill=MUTED)
        out = []
        for i, label in enumerate(pins):
            py = y + 26 + i * pitch
            self.line(x - 16, py, x, py)
            self.line(x + 56, py, x + 72, py)
            self.text(x + 28, py + 4, str(i + 1), size=10.5, anchor="middle")
            out.append(((x - 16, py), (x + 72, py)))
        return out

    def note(self, x, y, w, lines, title=None):
        h = 22 * len(lines) + (30 if title else 12) + 14
        self.rect(x, y, w, h, fill=PANEL, stroke=ACCENT, width=1.6, rx=6)
        cy = y + 26
        if title:
            self.text(x + 16, cy, title, size=11, weight="bold")
            cy += 26
        for ln in lines:
            self.text(x + 16, cy, ln, size=10)
            cy += 22


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --------------------------------------------------------------------------
# The nets. Single source of truth for the table in SCHEMATIC.md.
# --------------------------------------------------------------------------

NETS = [
    ("VBATT", "Cell positive, after SW1 and F1",
     "BT1 + · J1-1 · SW1 · F1 · U1 IN+ · R1 · J3-1"),
    ("GND", "The one common ground. Everything returns here",
     "BT1 − · J1-2 · U1 IN− · U1 OUT− · U3 GND · U2 GND · U2 1OE · U2 2OE · "
     "U2 3A · U2 4A · Q1 S · C1 − · C2 · R2 · J2-2 · J2-5 · J2-6 · LD1 GND · "
     "J4-2 · J4-5 · LD2 GND · J6-2 · SW2 COM"),
    ("+5V", "Boost output. Strip, level shifter, and CR2's anode",
     "U1 OUT+ · U2 Vcc · U2 3OE · U2 4OE · C1 + · C2 · CR2 anode · J2-1 · "
     "LD1 5V · J4-1 · LD2 5V"),
    ("+5V_MCU", "Same 5 V, one Schottky drop down, MCU only",
     "CR2 cathode · U3 5V"),
    ("VSENSE", "Half of VBATT, for the ADC",
     "R1 · R2 · U3 GPIO2"),
    ("LED_DATA_3V3", "MCU-level data, level shifter input",
     "U3 GPIO10 · U2 1A"),
    ("LED_DATA", "5 V data, through the series resistor, to the forearm strip",
     "U2 1Y · R3 · J2-3 · LD1 DIN"),
    ("LED_DATA_HAND", "The same chain continued past the wrist",
     "LD1 DOUT · J4-3 · LD2 DIN"),
    ("GATE_3V3", "MCU-level motor PWM, level shifter input",
     "U3 GPIO4 · U2 2A"),
    ("GATE", "5 V gate drive. R5 holds it down while the MCU boots",
     "U2 2Y · R4 · R5 · Q1 G"),
    ("TRIG", "Trigger, idle high on the MCU's internal pull-up",
     "U3 GPIO3 · J2-4 · J4-4 · J6-1 · SW2 NO"),
    ("MOTOR+", "Blower positive, straight off the cell",
     "VBATT · J3-1 · J5-1 · CR1 cathode · M1 +"),
    ("MOTOR-", "Blower negative, switched by the MOSFET",
     "Q1 D · J3-2 · J5-2 · CR1 anode · M1 −"),
]

# Every designator on both sheets. Nothing here may repeat a pin name printed
# on any module we use - see rule 2 in the module docstring.
DESIGNATORS = [
    ("BT1", "Protected 18650, on its factory PH2.0 lead"),
    ("J1", "JST-PH 2.0 2-pin — cell to pod, and cell to charger"),
    ("SW1", "Master disconnect, in the cell positive"),
    ("F1", "2 A PPTC resettable fuse"),
    ("U1", "MT3608 boost module, trimmed to 5.00 V"),
    ("CR2", "1N5819 — USB isolation, cathode to the XIAO 5V pad"),
    ("C1", "1000 uF electrolytic, at the elbow connector"),
    ("C2", "0.1 uF ceramic, across U2 pin 14 and pin 7, at the chip"),
    ("R1, R2", "100 k / 100 k battery-sense divider"),
    ("U3", "Seeed XIAO ESP32-C3"),
    ("U2", "74AHCT125 — gate 1 for LED data, gate 2 for the MOSFET gate, "
           "gates 3 and 4 tied off"),
    ("R3", "330-470 R series resistor on the LED data line"),
    ("R4", "100 R gate series resistor"),
    ("R5", "10 k gate-to-source pulldown"),
    ("Q1", "N-channel logic-level MOSFET (AO3400 / IRLZ44N / RFP30N06LE)"),
    ("CR1", "1N5819 flyback, across the motor, at the blower end"),
    ("M1", "Bubble kit blower motor"),
    ("SW2", "Lever microswitch, in the palm"),
    ("J2", "JST-SM 6-pin — elbow"),
    ("J3", "JST-SM 2-pin — elbow, motor"),
    ("J4", "JST-SM 5-pin — wrist"),
    ("J5", "JST-SM 2-pin — wrist, motor"),
    ("J6", "JST-ZH 1.5 mm 2-pin — at the microswitch"),
    ("LD1", "WS2812B forearm strip, 15 px, pixel 0 at the elbow"),
    ("LD2", "WS2812B hand strip, 6 px, to the knuckles"),
]

# The only place the XIAO's silkscreen D-numbers are allowed to appear, besides
# the silk map printed under U3 on sheet 1. Everything else says GPIOn.
PINMAP = [
    ("U3 GPIO2", "D0", "VSENSE", "ADC, battery divider midpoint"),
    ("U3 GPIO3", "D1", "TRIG", "Input, internal pull-up, switch pulls it low"),
    ("U3 GPIO4", "D2", "GATE_3V3", "Output, motor PWM into U2 2A"),
    ("U3 GPIO10", "D10", "LED_DATA_3V3", "Output, pixel data into U2 1A"),
    ("U3 5V", "5V", "+5V_MCU", "Power in, behind CR2"),
    ("U3 GND", "GND", "GND", "The one ground"),
]


# --------------------------------------------------------------------------
# Sheet 1 — the schematic
# --------------------------------------------------------------------------

def sheet_one():
    s = Sheet(1560, 1660, "clown — one arm — schematic",
              "Sheet 1 of 2 · pod electronics, motor drive, trigger · "
              "both arms are identical")

    # --- cell, disconnect, fuse -------------------------------------------
    s.block(60, 150, 190, 110, "BT1", "18650, protected", "factory PH2.0 lead")
    bp = s.pin(250, 185, "r", "+")
    bn = s.pin(250, 235, "r", "-")
    j1 = s.conn(330, 159, ["+", "-"], "J1", "JST-PH 2.0", pitch=50)
    s.wire([bp, j1[0][0]])
    s.wire([bn, j1[1][0]])

    sw_a, sw_b = s.spst(490, 185, "SW1", "master disconnect")
    s.wire([j1[0][1], sw_a])
    f_a, f_b = s.fuse(640, 185, "F1", "2 A PPTC")
    s.wire([sw_b, f_a])

    # VBATT rail
    s.wire([f_b, (1330, 185)])
    s.text(700, 170, "VBATT  3.0 - 4.2 V", size=11, weight="bold")

    # cell negative to ground
    s.wire([j1[1][1], (430, 235)])
    s.gnd(430, 235)

    # --- boost --------------------------------------------------------------
    s.block(760, 330, 220, 120, "U1", "MT3608 boost", "trim to 5.00 V first")
    in_p = s.pin(760, 370, "l", "IN+")
    in_n = s.pin(760, 420, "l", "IN-")
    out_p = s.pin(980, 370, "r", "OUT+")
    out_n = s.pin(980, 420, "r", "OUT-")
    s.wire([(800, 185), (800, 250), (700, 250), (700, 370), in_p])
    s.dot(800, 185)
    s.wire([in_n, (716, 420), (716, 470)])
    s.gnd(716, 470)
    s.wire([out_n, (1016, 420), (1016, 470)])
    s.gnd(1016, 470)

    # +5V rail
    s.wire([out_p, (1060, 370), (1060, 560)])
    s.wire([(340, 560), (1290, 560), (1290, 620)])
    s.dot(1060, 560)
    s.text(350, 545, "+5 V  strip, shifter, and CR2", size=11, weight="bold")
    s.flag(1295, 620, "+5V", "r")
    s.text(1295, 650, "to J2-1, the strip feed", size=9.5, fill=MUTED)

    # --- motor + tap --------------------------------------------------------
    s.wire([(1100, 185), (1100, 245)])
    s.dot(1100, 185)
    s.flag(1100, 245, "MOTOR+", "r")
    s.text(1100, 275, "to J3-1", size=9.5, fill=MUTED)

    # --- sense divider ------------------------------------------------------
    s.wire([(1330, 185), (1330, 231)])
    s.resistor(1330, 265, "v", "R1", "100 k")
    s.wire([(1330, 299), (1330, 396)])
    s.dot(1330, 360)
    s.flag(1345, 360, "VSENSE", "r")
    s.resistor(1330, 430, "v", "R2", "100 k")
    s.wire([(1330, 464), (1330, 500)])
    s.gnd(1330, 500)

    # --- isolation diode ----------------------------------------------------
    s.wire([(420, 560), (420, 590)])
    s.dot(420, 560)
    d2a, d2k = s.diode(420, 610, "v", "CR2", "1N5819")
    s.wire([d2k, (420, 750), (542, 750)])
    s.text(300, 700, "isolation:", size=10, weight="bold", fill=ACCENT)
    s.text(300, 716, "pack cannot", size=10, fill=ACCENT)
    s.text(300, 732, "backfeed USB", size=10, fill=ACCENT)

    # --- decoupling ---------------------------------------------------------
    s.wire([(1180, 560), (1180, 611)])
    s.dot(1180, 560)
    c_p, c_n = s.cap_polar(1180, 620, "C1", "1000 uF")
    s.wire([c_n, (1180, 690)])
    s.dot(1180, 660)
    s.text(1220, 742, "J2-2  strip ground", size=9.5, fill=MUTED)
    s.text(1220, 758, "J2-6  second ground", size=9.5, fill=MUTED)
    s.gnd(1180, 690)

    # --- MCU ----------------------------------------------------------------
    s.block(560, 700, 220, 260, "U3", "XIAO ESP32-C3", "keep USB-C reachable")
    s.pin(560, 750, "l", "5V")
    g3 = s.pin(560, 800, "l", "GND")
    vsense_pin = s.pin(560, 850, "l", "GPIO2")
    trig_pin = s.pin(560, 900, "l", "GPIO3")
    gate_pin = s.pin(780, 790, "r", "GPIO4")
    data_pin = s.pin(780, 840, "r", "GPIO10")
    s.wire([g3, (500, 800)])
    s.gnd(500, 800)
    s.flag(vsense_pin[0] - 18, 850, "VSENSE", "l")
    s.wire([(vsense_pin[0] - 18, 850), vsense_pin])
    s.flag(trig_pin[0] - 18, 900, "TRIG", "l")
    s.wire([(trig_pin[0] - 18, 900), trig_pin])
    s.text(670, 926, "silk map: GPIO2 = D0 · GPIO3 = D1", size=9,
           anchor="middle", fill=MUTED)
    s.text(670, 942, "GPIO4 = D2 · GPIO10 = D10", size=9,
           anchor="middle", fill=MUTED)

    # --- level shifter ------------------------------------------------------
    # Every pin of U2 is drawn. Pins that tie to Vcc leave the top, pins that
    # tie to ground leave the bottom, and the two unused outputs end in air.
    s.block(900, 700, 220, 290, "U2", "74AHCT125", "2 of 4 gates used", hdr=22)
    a2 = s.pin(900, 790, "l", "2A")
    a1 = s.pin(900, 840, "l", "1A")
    a3 = s.pin(900, 900, "l", "3A")
    a4 = s.pin(900, 950, "l", "4A")
    y2 = s.pin(1120, 790, "r", "2Y")
    y1 = s.pin(1120, 840, "r", "1Y")
    y3 = s.pin(1120, 900, "r", "3Y")
    y4 = s.pin(1120, 950, "r", "4Y")
    vcc = s.pin(950, 700, "t", "Vcc")
    oe3 = s.pin(1020, 700, "t", "3OE")
    oe4 = s.pin(1085, 700, "t", "4OE")
    ug = s.pin(940, 990, "b", "GND")
    oe1 = s.pin(1010, 990, "b", "1OE")
    oe2 = s.pin(1080, 990, "b", "2OE")
    s.wire([gate_pin, a2])
    s.wire([data_pin, a1])

    # to Vcc: the rail, and the two disabled output-enables
    for px in (vcc, oe3, oe4):
        s.wire([px, (px[0], 560)])
        s.dot(px[0], 560)

    c2_p, c2_n = s.cap(860, 620, "C2", "0.1 uF")
    s.wire([(860, 560), c2_p])
    s.dot(860, 560)
    s.wire([c2_n, (860, 690)])
    s.gnd(860, 690, label="")
    s.text(820, 612, "decoupling:", size=10, anchor="end",
           weight="bold", fill=ACCENT)
    s.text(820, 628, "at U2 pin 14 / pin 7", size=10, anchor="end", fill=ACCENT)

    # to ground: U2's own GND, the two enabled gates, the two unused inputs
    s.wire([a3, (860, 900), (860, 1008)])
    s.wire([a4, (860, 950)])
    s.dot(860, 950)
    s.wire([(820, 1008), (1080, 1008)])
    for px in (ug, oe1, oe2):
        s.wire([px, (px[0], 1008)])
        s.dot(px[0], 1008)
    s.dot(860, 1008)
    s.gnd(820, 1008, label="")

    # the two unused outputs: stub, and nothing else
    s.text(y3[0] + 8, y3[1] + 3.5, "open", size=9, fill=MUTED)
    s.text(y4[0] + 8, y4[1] + 3.5, "open", size=9, fill=MUTED)

    s.text(1200, 890, "the unused half of U2:", size=10, weight="bold",
           fill=ACCENT)
    s.text(1200, 906, "3A, 4A to GND - inputs, never floating", size=10,
           fill=ACCENT)
    s.text(1200, 922, "3OE, 4OE to Vcc - outputs off", size=10, fill=ACCENT)
    s.text(1200, 938, "3Y, 4Y open - never tie an output to a rail", size=10,
           fill=ACCENT)
    s.text(1200, 954, "1OE, 2OE to GND - this is what enables gates 1 and 2",
           size=10, fill=ACCENT)

    s.wire([y2, (1180, 790)])
    s.flag(1180, 790, "GATE", "r")
    s.wire([y1, (1186, 840)])
    s.resistor(1220, 840, "h", "R3", "330 - 470 R")
    s.wire([(1254, 840), (1290, 840)])
    s.flag(1290, 840, "LED_DATA", "r")
    s.text(1290, 870, "to J2-3", size=9.5, fill=MUTED)

    # --- motor drive --------------------------------------------------------
    s.text(60, 1040, "MOTOR DRIVE", size=12, weight="bold", fill=ACCENT)
    s.flag(60, 1120, "GATE", "r")
    s.wire([(156, 1120), (236, 1120)])
    s.resistor(270, 1120, "h", "R4", "100 R")
    s.wire([(304, 1120), (400, 1120)])
    s.dot(360, 1120)
    s.wire([(360, 1120), (360, 1186)])
    s.resistor(360, 1220, "v", "R5", "10 k")
    s.wire([(360, 1254), (360, 1300)])
    s.gnd(360, 1300)
    s.text(232, 1300, "holds the blower off", size=10, anchor="end")
    s.text(232, 1316, "while the MCU boots", size=10, anchor="end")

    drain, source = s.mosfet(400, 1120, "Q1", "logic-level N-ch")
    s.wire([drain, (500, 1010)])
    s.flag(510, 1010, "MOTOR-", "r")
    s.text(620, 1014, "to J3-2", size=9.5, fill=MUTED)
    s.wire([(500, 1010), (510, 1010)])
    s.wire([source, (500, 1190)])
    s.gnd(500, 1190)

    # blower end
    s.flag(760, 1100, "MOTOR+", "r")
    s.flag(760, 1260, "MOTOR-", "r")
    s.wire([(856, 1100), (1240, 1100), (1240, 1146)])
    s.wire([(856, 1260), (1240, 1260), (1240, 1214)])
    d1a, d1k = s.diode(1060, 1180, "v", "CR1", "1N5819", flip=True)
    s.wire([d1k, (1060, 1100)])
    s.wire([d1a, (1060, 1260)])
    s.dot(1060, 1100)
    s.dot(1060, 1260)
    s.motor(1240, 1180, "M1", "bubble kit blower")
    s.line(940, 1060, 940, 1310, width=1.4, color=MUTED, dash="6 7")
    s.text(940, 1046, "J3 + J5 (SM-2)", size=9.5, anchor="middle", fill=MUTED)
    s.text(1180, 1318, "CR1 and M1 both live at the blower end", size=9.5,
           anchor="middle", fill=MUTED)

    # --- trigger ------------------------------------------------------------
    s.text(60, 1380, "TRIGGER  (this hand only)", size=12, weight="bold", fill=ACCENT)
    a, b = s.spst(200, 1430, "SW2", "lever microswitch")
    s.wire([a, (120, 1430)])
    s.gnd(120, 1430)
    s.wire([b, (300, 1430)])
    s.flag(300, 1430, "TRIG", "r")
    s.text(430, 1416, "idle high on the XIAO's pull-up; the", size=10, fill=MUTED)
    s.text(430, 1434, "squeeze pulls it down to ground", size=10, fill=MUTED)
    s.text(430, 1452, "J6 (ZH-2) sits at the switch itself", size=10, fill=MUTED)

    # --- notes --------------------------------------------------------------
    s.note(760, 1330, 760, [
        "One name, one thing: no designator, pin or net on these two sheets",
        "names anything else. The diodes are CR1 and CR2, because the XIAO's",
        "silkscreen already owns D0 to D10. XIAO pins are named by GPIO number.",
        "One common ground: U1 IN-/OUT-, U3 GND, U2 GND, Q1 S, C1-, C2, R2,",
        "and both elbow ground pins (J2-2 and J2-6) all land on the same net.",
        "Set U1 to 5.00 V on the meter before the XIAO is ever connected.",
        "CR2 costs ~0.3 V: the XIAO sees ~4.7 V, well inside its regulator.",
        "SW1 kills the pack without unplugging anything. J1 still comes out.",
        "No CMOS input floats: U2's unused 3A/4A go to GND and 3OE/4OE to Vcc.",
        "C2 decouples U2 at the chip. C1 is bulk at the strip - not the same job.",
    ], title="RULES THIS SHEET ENFORCES")

    s.text(40, 1632, "generated by docs/schematic/schematic.py - do not hand-edit",
           size=9.5, fill=MUTED)
    return s.save("clown-arm-schematic.svg")


# --------------------------------------------------------------------------
# Sheet 2 — the harness
# --------------------------------------------------------------------------

def sheet_two():
    s = Sheet(1560, 1000, "clown — one arm — harness",
              "Sheet 2 of 2 · which net rides which pin, and where each module "
              "unplugs")

    L5V, LGND, LDATA, LTRIG, LRTN, LGND2 = 220, 270, 320, 370, 420, 470
    MP, MN = 640, 700

    def module(x, y, w, h, label):
        s.rect(x, y, w, h, fill="none", stroke=MUTED, width=1.6, rx=10, dash="8 8")
        s.text(x + 14, y - 10, label, size=12, weight="bold", fill=ACCENT)

    module(60, 170, 340, 620, "POD - upper arm")
    module(560, 170, 340, 620, "SLEEVE - forearm")
    module(1020, 170, 420, 380, "GLOVE - hand")
    module(1020, 590, 420, 200, "BUBBLER")

    j2 = s.conn(430, 194, [""] * 6, "J2", "SM-6 elbow", pitch=50)
    j3 = s.conn(430, 614, [""] * 2, "J3", "SM-2 elbow", pitch=60)
    j4 = s.conn(930, 194, [""] * 5, "J4", "SM-5 wrist", pitch=50)
    j5 = s.conn(930, 614, [""] * 2, "J5", "SM-2 wrist", pitch=60)

    # --- pod side -----------------------------------------------------------
    pod = [
        (L5V, "+5 V  from U1"),
        (LGND, "GND  common"),
        (LDATA, "LED_DATA  from R3"),
        (LTRIG, "TRIG  to U3 GPIO3"),
        (LRTN, "trigger return  GND"),
        (LGND2, "second ground  GND"),
        (MP, "MOTOR+  VBATT after F1"),
        (MN, "MOTOR-  Q1 D"),
    ]
    for y, label in pod:
        s.text(80, y - 10, label, size=10)
        s.wire([(100, y), (414, y)])

    # --- sleeve -------------------------------------------------------------
    s.block(620, 196, 240, 150, "LD1", "forearm strip", "15 px, px 0 at elbow")
    a5, ag, ad = (s.pin(620, L5V, "l", "5V"), s.pin(620, LGND, "l", "GND"),
                  s.pin(620, LDATA, "l", "DIN"))
    b5, bg, bd = (s.pin(860, L5V, "r", "5V"), s.pin(860, LGND, "r", "GND"),
                  s.pin(860, LDATA, "r", "DOUT"))
    for left, right, y in ((a5, b5, L5V), (ag, bg, LGND), (ad, bd, LDATA)):
        s.wire([j2[{L5V: 0, LGND: 1, LDATA: 2}[y]][1], left])
        s.wire([right, j4[{L5V: 0, LGND: 1, LDATA: 2}[y]][0]])

    s.text(620, 386, "LD1 DOUT crosses the wrist to LD2 DIN as LED_DATA_HAND",
           size=9.5, fill=MUTED)
    s.wire([j2[3][1], j4[3][0]])     # trigger, straight through
    s.wire([j2[4][1], j4[4][0]])     # trigger return, straight through
    s.wire([j2[5][1], (590, LGND2), (590, LGND)])   # second ground joins GND
    s.dot(590, LGND)
    s.text(600, LGND2 + 26, "J2-6 lands on the strip ground here:", size=9.5,
           fill=MUTED)
    s.text(600, LGND2 + 42, "the second conductor serves the elbow run only",
           size=9.5, fill=MUTED)

    s.wire([j3[0][1], (914, MP)])
    s.wire([j3[1][1], (914, MN)])
    s.text(700, MP - 14, "the motor pair crosses the sleeve untouched",
           size=9.5, fill=MUTED, anchor="middle")

    # --- glove --------------------------------------------------------------
    s.block(1060, 196, 240, 150, "LD2", "hand strip", "6 px to the knuckles")
    c5, cg, cd = (s.pin(1060, L5V, "l", "5V"), s.pin(1060, LGND, "l", "GND"),
                  s.pin(1060, LDATA, "l", "DIN"))
    for i, term in ((0, c5), (1, cg), (2, cd)):
        s.wire([j4[i][1], term])

    j6 = s.conn(1060, 394, [""] * 2, "J6", "ZH-2", pitch=50)
    s.wire([j4[3][1], (1030, LTRIG), (1030, LRTN), j6[0][0]])
    s.wire([j4[4][1], (1010, LRTN), (1010, LGND2), j6[1][0]])
    sa, sb = s.spst(1240, LRTN, "SW2", "microswitch")
    s.text(1140, 406, "TRIG", size=9.5, fill=MUTED)
    s.text(1140, 492, "GND", size=9.5, fill=MUTED)
    s.wire([j6[0][1], sa])
    s.wire([sb, (1330, LRTN), (1330, LGND2), j6[1][1]])
    s.text(1040, 530, "the whole glove comes off on one plug", size=9.5,
           fill=MUTED)

    # --- bubbler ------------------------------------------------------------
    s.block(1080, 610, 240, 150, "M1", "blower + CR1", "flyback across the motor")
    m_p = s.pin(1080, MP, "l", "+")
    m_n = s.pin(1080, MN, "l", "-")
    s.wire([j5[0][1], m_p])
    s.wire([j5[1][1], m_n])
    s.text(1040, 780, "its own strap, so it never bridges the wrist", size=9.5,
           fill=MUTED)

    # --- notes --------------------------------------------------------------
    s.note(60, 830, 1440, [
        "Four plugs per arm plus the one at the switch: J2 and J3 at the elbow, "
        "J4 and J5 at the wrist, J6 in the palm.",
        "No two connectors on one arm share both family and pin count: "
        "PH-2 (2.0 mm), ZH-2 (1.5 mm), SM-2 (2.5 mm), SM-5, SM-6.",
        "The two SM-2 plugs are identical on purpose - same net, so cross-mating "
        "them only shortens the motor run.",
        "SW1 off, or the cell out, before you mate or unmate anything. Feeding "
        "data into an unpowered strip is what kills pixel 0.",
    ], title="THE RULES THAT MAKE THIS SAFE TO PULL APART IN A DARK ROOM")

    s.text(40, 972, "generated by docs/schematic/schematic.py - do not hand-edit",
           size=9.5, fill=MUTED)
    return s.save("clown-arm-harness.svg")


# --------------------------------------------------------------------------
# The net table, written back into SCHEMATIC.md
# --------------------------------------------------------------------------

def check_names():
    """Enforce the naming rules at the top of this file.

    Cheap to run, and it is the only thing standing between a future edit and
    another D2-the-pin / D2-the-diode collision, so it runs on every generate.
    """
    refs = []
    for ref, _ in DESIGNATORS:
        refs += [r.strip() for r in ref.split(",")]
    nets = [n for n, _, _ in NETS]

    # Names the XIAO's silkscreen already owns. Nothing of ours may take one.
    silk = set("D%d" % i for i in range(11)) | set("A%d" % i for i in range(4))

    bad = []
    for kind, names in (("designator", refs), ("net", nets)):
        for n in sorted(set(names)):
            if names.count(n) > 1:
                bad.append("%s %s is listed twice" % (kind, n))
    for n in sorted(set(refs) & set(nets)):
        bad.append("%s is both a designator and a net name" % n)
    for n in sorted(set(refs) & silk):
        bad.append("designator %s collides with a XIAO silkscreen pin name; "
                   "diodes use the CR prefix for exactly this reason" % n)
    for n in sorted(set(nets) & silk):
        bad.append("net %s collides with a XIAO silkscreen pin name" % n)

    # Every net member has to name an owner we know about.
    known = set(refs) | set(nets)
    for name, _, members in NETS:
        for member in members.split("·"):
            owner = member.strip().split(" ")[0].split("-")[0]
            if owner and owner not in known:
                bad.append("net %s refers to %s, which is not a designator "
                           "or a net" % (name, owner))
    # And the pin map may only name pins of U3.
    for pin, _, net, _ in PINMAP:
        if not pin.startswith("U3 "):
            bad.append("pin map entry %r does not name its owner" % pin)
        if net not in nets:
            bad.append("pin map entry %r lands on unknown net %s" % (pin, net))

    if bad:
        raise SystemExit("naming rules violated:\n  " + "\n  ".join(bad))


BEGIN = "<!-- generated:nets -->"
END = "<!-- /generated:nets -->"


def net_tables():
    out = ["", "### Nets", "",
           "| Net | What it is | Everything on it |", "|---|---|---|"]
    for name, what, members in NETS:
        out.append("| `%s` | %s | %s |" % (name, what, members))
    out += ["", "### Designators", "", "| Ref | Part |", "|---|---|"]
    for ref, part in DESIGNATORS:
        out.append("| `%s` | %s |" % (ref, part))
    out += ["", "### U3 pin map", "",
            "The only place the XIAO's silkscreen numbers are written down. "
            "Everywhere else, a XIAO pin is named by its GPIO number, so that "
            "`CR1` and `CR2` are the only `D`-ish names left and they are the "
            "two diodes.", "",
            "| Pin | Silkscreen | Net | What it does |", "|---|---|---|---|"]
    for pin, silk, net, what in PINMAP:
        out.append("| `%s` | `%s` | `%s` | %s |" % (pin, silk, net, what))
    out.append("")
    return "\n".join(out)


def write_nets():
    path = os.path.join(ROOT, "SCHEMATIC.md")
    with open(path) as f:
        doc = f.read()
    block = BEGIN + "\n" + net_tables() + "\n" + END
    new = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), lambda _: block,
                 doc, flags=re.S)
    if new == doc and BEGIN not in doc:
        raise SystemExit("SCHEMATIC.md is missing the %s markers" % BEGIN)
    with open(path, "w") as f:
        f.write(new)
    return os.path.relpath(path, ROOT)


if __name__ == "__main__":
    check_names()
    for p in (sheet_one(), sheet_two(), write_nets()):
        print("wrote", p)

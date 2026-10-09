#!/usr/bin/env python3
"""Generate the pod PCB: the circuit the perfboard layout builds, as a real board.

Runs inside the KiCad 9 Docker image (it needs the pcbnew module). Call it
through build.sh, which also runs the autorouter and the exports:

    docs/pcb/build.sh

Two stages, because the autorouter (Freerouting) runs on the host in between:

    pod_pcb.py place   board outline, footprints, nets, silkscreen -> clown-pod.kicad_pcb
                       and build/clown-pod.dsn for the autorouter
    pod_pcb.py finish  import the routed .ses, stitch and pour ground, save

Same parts, same nets, same names as SCHEMATIC.md. Off-board parts (U1 the
MT3608 module, SW1, J1 the cell lead, J2 and J3 the arm leads) land on wire pads,
exactly as they do on the perfboard. The board is 70 x 30 mm, the size of the
3 x 7 cm perfboard it replaces, with an M2 hole in each corner.

Layout, left to right: the XIAO with its USB-C off the left edge; the level
shifter and its tie-offs; the power stage (cell, switch, fuse, MOSFET) at the
right-hand end beside the elbow lead J3, so the motor current loop stays short
and never crosses the logic. GND is not routed: both layers are poured and
stitched, and the router only sees the other nets.
"""

import json
import math
import os
import sys

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = "clown-pod"
PCB = os.path.join(HERE, NAME + ".kicad_pcb")
PRO = os.path.join(HERE, NAME + ".kicad_pro")
DSN = os.path.join(HERE, "build", NAME + ".dsn")
SES = os.path.join(HERE, "build", NAME + ".ses")
LIB = "/usr/share/kicad/footprints"

W, H = 70.0, 30.0
REV = "rev A"
HOLES = ((2.5, 2.5), (W - 2.5, 2.5), (2.5, H - 2.5), (W - 2.5, H - 2.5))

# Router classes: name -> (nets, track width, via diameter, via drill), mm.
# The cell and motor path sees ~2 A firing and ~3 A in the 80 ms kick:
# 1.5 mm of 1 oz copper carries 3.2 A at a 10 C rise. GND is poured, not routed.
CLASSES = {
    "batt": (["VBATT_RAW", "VBATT_SW", "VBATT", "MOTOR-"], 1.5, 1.2, 0.6),
    "rail": (["+5V"], 0.6, 0.8, 0.4),  # branches; the trunk is drawn below
    "mcu": (["+5V_MCU"], 0.6, 0.8, 0.4),
}
SIGNAL_W = 0.3
CLEARANCE = 0.4      # also keeps tracks well off hand-soldered pads
ZONE_CLEARANCE = 0.5
EDGE_KEEPOUT = 1.0   # no tracks within 1 mm of the board edge
HOLE_KEEPOUT = 2.4   # no tracks within 2.4 mm of a hole centre: M2 heads and nuts
                     # reach 1.9-2.3 mm

TEXT = 0.8           # PCBWay's minimum legible silkscreen: 0.8 mm tall,
TEXT_LINE = 0.15     # 0.15 mm line


def mm(v):
    return pcbnew.FromMM(v)


def pt(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


# --------------------------------------------------------------------------
# Netlist. Pad -> net for every part on the board. Net names are the
# schematic's. Four short stretches the schematic draws but does not name get
# names here: VBATT_RAW (J1-1 to SW1) and VBATT_SW (SW1 to F1) ahead of the
# fuse, GATE_Q (R4 to Q1 G and R5) and LED_DATA_STRIP (R3 to J2-3).
# --------------------------------------------------------------------------

NETS = {
    # U3 XIAO ESP32-C3. Pads 1-14 in the module's own order; unused pins open.
    ("U3", "1"): "VSENSE",        # GPIO2
    ("U3", "2"): "TRIG",          # GPIO3
    ("U3", "3"): "GATE_3V3",      # GPIO4
    ("U3", "11"): "LED_DATA_3V3",  # GPIO10
    ("U3", "13"): "GND",
    ("U3", "14"): "+5V_MCU",
    # U2 74AHCT125, DIP-14
    ("U2", "1"): "GND",           # 1OE
    ("U2", "2"): "LED_DATA_3V3",  # 1A
    ("U2", "3"): "LED_DATA",      # 1Y
    ("U2", "4"): "GND",           # 2OE
    ("U2", "5"): "GATE_3V3",      # 2A
    ("U2", "6"): "GATE",          # 2Y
    ("U2", "7"): "GND",
    ("U2", "9"): "GND",           # 3A, tied off
    ("U2", "10"): "+5V",          # 3OE, disabled
    ("U2", "12"): "GND",          # 4A, tied off
    ("U2", "13"): "+5V",          # 4OE, disabled
    ("U2", "14"): "+5V",          # Vcc
    # 3Y (8) and 4Y (11) are outputs and stay open
    ("C1", "1"): "+5V", ("C1", "2"): "GND",
    ("C2", "1"): "+5V", ("C2", "2"): "GND",
    ("C3", "1"): "VSENSE", ("C3", "2"): "GND",
    ("CR2", "1"): "+5V_MCU",      # cathode, to the XIAO
    ("CR2", "2"): "+5V",          # anode
    ("R1", "1"): "VBATT", ("R1", "2"): "VSENSE",
    ("R2", "1"): "VSENSE", ("R2", "2"): "GND",
    ("R3", "1"): "LED_DATA", ("R3", "2"): "LED_DATA_STRIP",
    ("R4", "1"): "GATE", ("R4", "2"): "GATE_Q",
    ("R5", "1"): "GATE_Q", ("R5", "2"): "GND",
    ("R6", "1"): "GATE_3V3", ("R6", "2"): "GND",
    ("Q1", "1"): "GATE_Q",        # G
    ("Q1", "2"): "MOTOR-",        # D
    ("Q1", "3"): "GND",           # S
    ("F1", "1"): "VBATT_SW", ("F1", "2"): "VBATT",
    # Wire pads
    ("J1", "1"): "VBATT_RAW", ("J1", "2"): "GND",
    ("SW1", "1"): "VBATT_RAW", ("SW1", "2"): "VBATT_SW",
    ("U1", "1"): "VBATT",         # IN+
    ("U1", "2"): "GND",           # IN-
    ("U1", "3"): "+5V",           # OUT+
    ("U1", "4"): "GND",           # OUT-
    ("J2", "1"): "+5V", ("J2", "2"): "GND", ("J2", "3"): "LED_DATA_STRIP",
    ("J3", "1"): "VBATT", ("J3", "2"): "MOTOR-", ("J3", "3"): "TRIG", ("J3", "4"): "GND",
}


# --------------------------------------------------------------------------
# Power, routed by hand and locked; the router does the rest. Each entry is
# (net, layer, width, points). Corridors are worked out against the placement
# below: every track clears other nets' pads by at least the 0.4 mm rule.
# --------------------------------------------------------------------------

F, B = pcbnew.F_Cu, pcbnew.B_Cu
POWER_ROUTES = [
    # Cell -> SW1 -> F1 -> U1 IN+, all along the bottom row on the back
    ("VBATT_RAW", B, 1.5, [(58.5, 26.8), (49.5, 26.8)]),          # J1+ to SW1 A
    ("VBATT_SW", B, 1.5, [(46.0, 26.8), (40.0, 26.8)]),           # SW1 B to F1
    ("VBATT", B, 1.5, [(34.92, 26.8), (17.0, 26.8)]),             # F1 to U1 IN+
    # F1 to the motor feed J3-1, on the front above the bottom row
    # (1.2 mm where it squeezes between the resistor row and the bottom pads)
    ("VBATT", F, 1.2, [(34.92, 26.8), (37.02, 24.7), (56.8, 24.7), (58.0, 23.5)]),
    ("VBATT", F, 1.5, [(58.0, 23.5), (58.0, 16.5), (59.5, 15.0), (66.5, 15.0)]),
    # J3-1 up the right side and along the top edge to the divider top R1
    # (signal current only)
    ("VBATT", F, 0.5, [(59.5, 15.0), (59.5, 2.2), (59.0, 1.7), (43.06, 1.7),
                       (42.16, 2.6)]),
    # Motor return: Q1 drain to J3-2, over Q1's source pad
    # (0.9 mm clear of Q1's source pad, which takes a big fillet)
    ("MOTOR-", B, 1.5, [(50.74, 18.6), (50.74, 16.0), (62.5, 16.0), (64.3, 17.8),
                        (66.5, 17.8)]),
    # +5V trunk: U1 OUT+ -> C1 -> J2-1, so strip current never crosses U2.
    # Up the gap between U3 and U2, over U2's top row, into C1, on to J2.
    ("+5V", B, 1.0, [(10.0, 26.8), (10.0, 25.4), (11.4, 24.0), (20.6, 24.0),
                     (20.6, 10.3), (43.0, 10.3), (44.3, 9.0), (46.5, 9.0)]),
    ("+5V", B, 1.0, [(46.5, 9.0), (46.5, 5.4), (64.5, 5.4), (66.5, 6.4)]),
    # CR2's cathode to the XIAO 5V pin, which sits right under hole H1
    ("+5V_MCU", F, 0.5, [(6.5, 2.6), (4.3, 4.8), (2.5, 6.38)]),
    # CR2's anode down past the XIAO's corner pin to the trunk
    ("+5V", B, 0.6, [(16.66, 2.6), (16.66, 4.5), (19.6, 4.5), (20.6, 5.5),
                     (20.6, 10.3)]),
]


# --------------------------------------------------------------------------
# Footprint helpers
# --------------------------------------------------------------------------

def load(lib, name):
    fp = pcbnew.FootprintLoad(os.path.join(LIB, lib + ".pretty"), name)
    if fp is None:
        sys.exit("footprint not found: %s:%s" % (lib, name))
    return fp


def place(board, fp, ref, value, pad1, rot=0, ref_at=None, ref_rot=None):
    """Put fp on the board with pad 1 at pad1 (mm), rotated rot degrees.
    ref_at moves the reference designator; "body" centres it on the part."""
    fp.SetReference(ref)
    fp.SetValue(value)
    board.Add(fp)
    fp.SetOrientationDegrees(rot)
    p1 = [p for p in fp.Pads() if p.GetNumber() == "1"][0].GetPosition()
    fp.Move(pt(*pad1) - p1)
    fp.Value().SetVisible(False)
    r = fp.Reference()
    r.SetTextSize(pcbnew.VECTOR2I(mm(1.0), mm(1.0)))
    r.SetTextThickness(mm(TEXT_LINE))
    if ref_at == "body":
        pads = [p.GetPosition() for p in fp.Pads()]
        r.SetPosition(pcbnew.VECTOR2I(sum(p.x for p in pads) // len(pads),
                                      sum(p.y for p in pads) // len(pads)))
    elif ref_at:
        r.SetPosition(pt(*ref_at))
    if ref_rot is not None:
        r.SetTextAngleDegrees(ref_rot)
    return fp


def segment(parent, x1, y1, x2, y2, width=TEXT_LINE, layer=pcbnew.F_SilkS):
    s = pcbnew.PCB_SHAPE(parent)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pt(x1, y1))
    s.SetEnd(pt(x2, y2))
    s.SetLayer(layer)
    s.SetWidth(mm(width))
    parent.Add(s)


def rect(parent, x1, y1, x2, y2, width=TEXT_LINE, layer=pcbnew.F_SilkS):
    for a, b in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)),
                 ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        segment(parent, a[0], a[1], b[0], b[1], width, layer)


def text(board, s, x, y, size=TEXT, layer=pcbnew.F_SilkS, rot=0, bold=False,
         justify=None):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(s)
    t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    t.SetTextThickness(mm(max(TEXT_LINE, size * (0.2 if bold else 0.15))))
    t.SetPosition(pt(x, y))
    t.SetTextAngleDegrees(rot)
    if justify == "left":
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
    elif justify == "right":
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_RIGHT)
    if layer == pcbnew.B_SilkS:
        t.SetMirrored(True)
    board.Add(t)
    return t


def pth(fp, num, x, y, drill, size, shape=pcbnew.PAD_SHAPE_CIRCLE):
    p = pcbnew.PAD(fp)
    p.SetNumber(num)
    p.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
    p.SetLayerSet(pcbnew.PAD.PTHMask())
    p.SetShape(shape)
    p.SetDrillSize(pcbnew.VECTOR2I(mm(drill), mm(drill)))
    p.SetSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    p.SetPosition(pt(x, y))
    fp.Add(p)
    return p


def custom(board, ref, value, fpid, x, y):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(pt(x, y))
    fp.SetFPID(pcbnew.LIB_ID("clown", fpid))
    fp.Value().SetVisible(False)
    board.Add(fp)
    return fp


def courtyard(fp, x1, y1, x2, y2):
    rect(fp, x1, y1, x2, y2, 0.05, pcbnew.F_CrtYd)


def wire_pads(board, ref, value, labels, xs, ys, label_at):
    """Plain plated holes for wires, one per (x, y). Pad 1 is square.
    label_at(x, y) -> (x, y, justify) places each pad's label."""
    fp = custom(board, ref, value, "WirePads_%d" % len(labels), xs[0], ys[0])
    for i, (lab, px, py) in enumerate(zip(labels, xs, ys)):
        pth(fp, str(i + 1), px, py, 1.1, 2.2,
            pcbnew.PAD_SHAPE_RECT if i == 0 else pcbnew.PAD_SHAPE_CIRCLE)
        lx, ly, just = label_at(px, py)
        text(board, lab, lx, ly, justify=just)
    courtyard(fp, min(xs) - 1.35, min(ys) - 1.35, max(xs) + 1.35, max(ys) + 1.35)
    fp.Reference().SetVisible(False)
    return fp


def rule_area(board, poly, layers=None, pour=True):
    """Keep-out for tracks and vias. Pads are allowed, and so is the ground
    pour unless pour=False."""
    z = pcbnew.ZONE(board)
    z.SetIsRuleArea(True)
    z.SetDoNotAllowTracks(True)
    z.SetDoNotAllowVias(True)
    z.SetDoNotAllowPads(False)
    z.SetDoNotAllowFootprints(False)
    z.SetDoNotAllowCopperPour(not pour)
    z.SetLayerSet(layers or pcbnew.LSET.AllCuMask())
    o = z.Outline()
    o.NewOutline()
    for x, y in poly:
        o.Append(mm(x), mm(y))
    board.Add(z)


# --------------------------------------------------------------------------
# Stage 1 - place
# --------------------------------------------------------------------------

def write_project():
    classes = [{"name": "Default", "clearance": CLEARANCE, "track_width": SIGNAL_W,
                "via_diameter": 0.8, "via_drill": 0.4, "priority": 2147483647}]
    patterns = []
    for i, (name, (nets, width, via_d, via_h)) in enumerate(CLASSES.items()):
        classes.append({"name": name, "clearance": CLEARANCE, "track_width": width,
                        "via_diameter": via_d, "via_drill": via_h, "priority": i})
        patterns += [{"netclass": name, "pattern": n} for n in nets]
    pro = {
        "board": {"design_settings": {
            # PCBWay's standard process, with margin
            "rules": {
                "min_clearance": CLEARANCE, "min_track_width": SIGNAL_W,
                "min_via_diameter": 0.8, "min_via_annular_width": 0.2,
                "min_through_hole_diameter": 0.4, "min_hole_to_hole": 0.5,
                "min_copper_edge_clearance": ZONE_CLEARANCE,
                "min_hole_clearance": 0.3, "min_silk_clearance": 0.0,
                "min_text_height": TEXT, "min_text_thickness": TEXT_LINE},
            "rule_severities": {
                # A thermal whose spokes reach only a pour island is still
                # connected; the unconnected-items check covers it
                "starved_thermal": "warning",
                # Fab-relevant silkscreen problems are errors, so build.sh stops
                "silk_edge_clearance": "error",
                "silk_over_copper": "error",
                "text_height": "error",
                "text_thickness": "error",
                "hole_to_hole": "error",
                # The custom footprints live in this script, not a library
                "lib_footprint_issues": "ignore",
                "lib_footprint_mismatch": "ignore"}}},
        "net_settings": {"classes": classes, "meta": {"version": 4},
                         "netclass_patterns": patterns},
        "meta": {"filename": NAME + ".kicad_pro", "version": 3},
    }
    with open(PRO, "w") as f:
        json.dump(pro, f, indent=2)


def outline(board):
    r = 1.0
    edge = pcbnew.Edge_Cuts
    for (x1, y1, x2, y2) in ((r, 0, W - r, 0), (W, r, W, H - r),
                             (W - r, H, r, H), (0, H - r, 0, r)):
        segment(board, x1, y1, x2, y2, 0.1, edge)
    for cx, cy, sx, sy in ((r, r, 0, r), (W - r, r, W - r, 0),
                           (W - r, H - r, W, H - r), (r, H - r, r, H)):
        a = pcbnew.PCB_SHAPE(board)
        a.SetShape(pcbnew.SHAPE_T_ARC)
        a.SetCenter(pt(cx, cy))
        a.SetStart(pt(sx, sy))
        a.SetArcAngleAndEnd(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T), True)
        a.SetLayer(edge)
        a.SetWidth(mm(0.1))
        board.Add(a)
    for i, (x, y) in enumerate(HOLES):
        fp = load("MountingHole", "MountingHole_2.2mm_M2")
        fp.SetReference("H%d" % (i + 1))
        board.Add(fp)
        fp.SetPosition(pt(x, y))
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)


def stage_place():
    board = pcbnew.BOARD()
    outline(board)
    rfp10 = ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
    rfp7 = ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal")
    disc = ("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm")

    # --- U3 XIAO ESP32-C3, on two 7-pin headers ------------------------------
    # Module pin order, top view: pins 1-7 down one side from the USB end,
    # 8-14 back up the other, so pin 14 (5V) sits across from pin 1 (GPIO2).
    # USB to the left puts pins 1-7 on the bottom row. The module's own board
    # starts 0.4 mm past our left edge, so its USB-C socket stands ~1.5 mm proud.
    x0, ytop, ybot = 2.5, 6.38, 21.62
    u3 = custom(board, "U3", "XIAO ESP32-C3", "XIAO_ESP32C3_Headers", x0, ybot)
    gpio_bot = ["GPIO2", "GPIO3", "GPIO4", "GPIO5", "GPIO6", "GPIO7", "GPIO21"]
    gpio_top = ["5V", "GND", "3V3", "GPIO10", "GPIO9", "GPIO8", "GPIO20"]
    for i in range(7):
        x = x0 + i * 2.54
        pth(u3, str(i + 1), x, ybot, 1.0, 1.7,
            pcbnew.PAD_SHAPE_RECT if i == 0 else pcbnew.PAD_SHAPE_CIRCLE)
        pth(u3, str(14 - i), x, ytop, 1.0, 1.7)
        text(board, gpio_bot[i], x, ybot - 1.5, rot=90, justify="left")
        text(board, gpio_top[i], x, ytop + 1.5, rot=90, justify="right")
    # Module body, 21 x 17.8 mm; the outline stops at our edge
    for seg in ((0.3, 5.1, 20.6, 5.1), (20.6, 5.1, 20.6, 22.9), (20.6, 22.9, 0.3, 22.9)):
        segment(u3, *seg)
    courtyard(u3, -0.4, 5.0, 20.85, 23.15)
    u3.Reference().SetTextSize(pcbnew.VECTOR2I(mm(1.0), mm(1.0)))
    u3.Reference().SetTextThickness(mm(TEXT_LINE))
    u3.Reference().SetPosition(pt(19.4, 14.0))
    u3.Reference().SetTextAngleDegrees(90)

    # --- top strip: CR2, then the battery divider ----------------------------
    cr2 = place(board, load("Diode_THT", "D_DO-41_SOD81_P10.16mm_Horizontal"),
                "CR2", "1N5819", (6.5, 2.6), 0, ref_at=(11.58, 2.6))
    for g in cr2.GraphicalItems():  # the cathode "K"
        if g.GetClass() == "PCB_TEXT" and g.GetText() == "K":
            g.SetPosition(pt(6.5, 4.45))  # below the pad, clear of H1's screw head
            g.SetTextSize(pcbnew.VECTOR2I(mm(TEXT), mm(TEXT)))
            g.SetTextThickness(mm(TEXT_LINE))
    # R2 (GND end left) then R1 (VBATT end right, fed along the top edge)
    place(board, load(*rfp10), "R2", "100k", (29.66, 2.6), 180, ref_at="body")
    place(board, load(*rfp10), "R1", "100k", (42.16, 2.6), 180, ref_at="body")

    # --- U2 74AHCT125, DIP-14, notch to the left, pin 1 bottom-left ---------
    place(board, load("Package_DIP", "DIP-14_W7.62mm"),
          "U2", "74AHCT125", (27.0, 19.81), 90, ref_at=(34.62, 16.0), ref_rot=0)
    # C2 right over U2 pin 14
    place(board, load(*disc), "C2", "0.1uF", (27.0, 8.4), 0, ref_at=(29.5, 6.1))
    # C3 filters the divider. It can sit anywhere on VSENSE for a slow ADC
    # read, so it takes the gap between U3 and U2
    place(board, load(*disc), "C3", "0.1uF", (23.4, 18.6), 90, ref_at=(23.4, 11.4))

    # --- under U2: R6 (U2 2A pulldown), R4 (gate series), R5 (gate pulldown)
    place(board, load(*rfp7), "R6", "100k", (24.2, 22.8), 0, ref_at="body")
    place(board, load(*rfp7), "R4", "100R", (34.6, 22.8), 0, ref_at="body")
    place(board, load(*rfp7), "R5", "10k", (48.2, 22.8), 0, ref_at="body")

    # --- C1 1000 uF and R3, by the strip plug J2 ----------------------------
    place(board, load("Capacitor_THT", "CP_Radial_D10.0mm_P5.00mm"),
          "C1", "1000uF 16V", (46.5, 9.0), 0, ref_at=(49.0, 2.6))
    place(board, load(*rfp10), "R3", "470R", (56.1, 3.6), -90, ref_at="body",
          ref_rot=90)

    # --- Q1 RFP30N06LE, TO-220 standing up, tab toward C1 --------------------
    q1 = place(board, load("Package_TO_SOT_THT", "TO-220-3_Vertical"),
               "Q1", "RFP30N06LE", (48.2, 18.6), 0, ref_at=(50.74, 16.03))
    q1.Reference().SetTextSize(pcbnew.VECTOR2I(mm(TEXT), mm(TEXT)))  # fits the tab band
    for i, s in enumerate("GDS"):
        text(board, s, 48.2 + i * 2.54, 20.75)
    # Source carries the motor current: solid to the pour, no spokes
    for p in q1.Pads():
        if p.GetNumber() == "3":
            p.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)

    # --- bottom row: wire pads and F1 ----------------------------------------
    # Pad names under the pads, group names over them
    below = lambda x, y: (x, y + 2.05, None)
    # U1's IN+ is the right-hand pad so VBATT reaches it in a straight run
    wire_pads(board, "U1", "MT3608 module", ["IN+", "IN-", "OUT+", "OUT-"],
              [17.0, 13.5, 10.0, 6.5], [26.8] * 4, below)
    text(board, "U1 MT3608", 11.75, 24.95)
    f1 = custom(board, "F1", "PPTC 1.85-2.5A", "PPTC_Radial_P5.08mm", 40.0, 26.8)
    pth(f1, "1", 40.0, 26.8, 1.0, 2.0, pcbnew.PAD_SHAPE_RECT)
    pth(f1, "2", 34.92, 26.8, 1.0, 2.0)
    rect(f1, 32.9, 25.0, 42.0, 28.6)
    courtyard(f1, 32.65, 24.75, 42.25, 28.85)
    f1.Reference().SetTextThickness(mm(TEXT_LINE))
    f1.Reference().SetPosition(pt(37.46, 26.8))
    wire_pads(board, "SW1", "KCD1 rocker", ["A", "B"], [49.5, 46.0], [26.8] * 2, below)
    text(board, "SW1", 47.75, 24.95)
    wire_pads(board, "J1", "Cell, PH2.0", ["+", "-"], [58.5, 62.0], [26.8] * 2, below)
    text(board, "J1 CELL", 60.25, 24.95)

    # --- right edge: the two arm leads ----------------------------------------
    left = lambda x, y: (x - 1.8, y, "right")
    wire_pads(board, "J2", "Strip SM-3", ["J2-1 +5V", "J2-2 GND", "J2-3 DATA"],
              [66.5] * 3, [6.4, 9.2, 12.0], left)
    wire_pads(board, "J3", "Elbow SM-4",
              ["J3-1 M+", "J3-2 M-", "J3-3 TRIG", "J3-4 GND"],
              [66.5] * 4, [15.0, 17.8, 20.6, 23.4], left)

    # --- the back --------------------------------------------------------------
    text(board, "CLOWN POD " + REV, 34.62, 13.9, 1.2, layer=pcbnew.B_SilkS, bold=True)
    text(board, "Trim U1 to 5.00 V", 34.62, 15.7, 1.0, layer=pcbnew.B_SilkS)
    text(board, "before fitting U3", 34.62, 17.4, 1.0, layer=pcbnew.B_SilkS)

    # --- nets ------------------------------------------------------------------
    for name in sorted(set(NETS.values())):
        board.Add(pcbnew.NETINFO_ITEM(board, name))
    for (ref, num), name in NETS.items():
        pads = [p for p in board.FindFootprintByReference(ref).Pads()
                if p.GetNumber() == num]
        if len(pads) != 1:
            sys.exit("no pad %s %s" % (ref, num))
        pads[0].SetNet(board.FindNet(name))

    # --- keep-outs for the router ----------------------------------------------
    # One strip per edge (the router can't read a keep-out with a hole in it)
    e = EDGE_KEEPOUT
    for x1, y1, x2, y2 in ((0, 0, W, e), (0, H - e, W, H), (0, 0, e, H), (W - e, 0, W, H)):
        rule_area(board, ((x1, y1), (x2, y1), (x2, y2), (x1, y2)))
    # An octagon round each mounting hole, clear of screw heads and standoffs
    for hx, hy in HOLES:
        rr = HOLE_KEEPOUT / math.cos(math.pi / 8)
        rule_area(board, [(hx + rr * math.cos(math.pi / 8 + k * math.pi / 4),
                           hy + rr * math.sin(math.pi / 8 + k * math.pi / 4))
                          for k in range(8)], pour=False)

    for net, layer, width, pts in POWER_ROUTES:
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            t = pcbnew.PCB_TRACK(board)
            t.SetStart(pt(x1, y1))
            t.SetEnd(pt(x2, y2))
            t.SetWidth(mm(width))
            t.SetLayer(layer)
            t.SetNet(board.FindNet(net))
            t.SetLocked(True)
            board.Add(t)

    # Library outlines draw silk at 0.12 mm; PCBWay wants 0.15
    for fp in board.GetFootprints():
        for g in fp.GraphicalItems():
            if g.GetClass() == "PCB_SHAPE" and g.GetLayer() in (pcbnew.F_SilkS, pcbnew.B_SilkS) \
                    and g.GetWidth() < mm(TEXT_LINE):
                g.SetWidth(mm(TEXT_LINE))

    board.SetCopperLayerCount(2)
    pcbnew.SaveBoard(PCB, board)
    write_project()  # SaveBoard wrote a default project over ours

    # Reload so the project's net classes apply, then export for the router
    board = pcbnew.LoadBoard(PCB)
    os.makedirs(os.path.dirname(DSN), exist_ok=True)
    if not pcbnew.ExportSpecctraDSN(board, DSN):
        sys.exit("DSN export failed")
    patch_dsn()
    print("placed; wrote", DSN)


def patch_dsn():
    """Give the router our net classes.

    KiCad 9's DSN export puts every net in one class at the board minimums,
    whatever the project says. Rewrite the class block from CLASSES, and put
    GND in a class of its own that build.sh tells the router to ignore.
    """
    with open(DSN) as f:
        dsn = f.read()
    start = dsn.index("    (class kicad_default")
    end = dsn.index("  (wiring")
    nets = [l.strip()[len("(net "):].strip('"') for l in dsn.splitlines()
            if l.strip().startswith("(net ")]

    def quote(n):
        return '"%s"' % n if "-" in n or "+" in n else n

    def via(d, h):
        return "Via[0-1]_%d:%d_um" % (d * 1000, h * 1000)

    def cls(name, members, width, via_name):
        return ('    (class %s %s\n      (circuit (use_via "%s"))\n'
                "      (rule (width %d) (clearance %d))\n    )\n"
                % (name, " ".join(quote(n) for n in members), via_name,
                   width * 1000, CLEARANCE * 1000))

    classed = {n for nets_, *_ in CLASSES.values() for n in nets_} | {"GND"}
    blocks = cls("signal", [n for n in nets if n not in classed], SIGNAL_W,
                 via(0.8, 0.4))
    blocks += cls("gnd", ["GND"], SIGNAL_W, via(0.8, 0.4))
    vias = {(0.8, 0.4)}
    for name, (members, width, d, h) in CLASSES.items():
        blocks += cls(name, members, width, via(d, h))
        vias.add((d, h))
    dsn = dsn[:start] + blocks + "  )\n" + dsn[end:]

    padstacks = "".join(
        '    (padstack "%s"\n      (shape (circle F.Cu %d))\n'
        "      (shape (circle B.Cu %d))\n      (attach off)\n    )\n"
        % (via(d, h), d * 1000, d * 1000) for d, h in sorted(vias))
    vstart = dsn.index('    (padstack "Via[0-1]_')
    vend = dsn.index("    )\n", vstart) + len("    )\n")
    old = dsn[vstart:vend].split('"')[1]
    dsn = dsn[:vstart] + padstacks + dsn[vend:]
    dsn = dsn.replace('(via "%s")' % old,
                      "(via %s)" % " ".join('"%s"' % via(d, h) for d, h in sorted(vias)))
    dsn = dsn.replace("(width 200)\n      (clearance 200)",
                      "(width %d)\n      (clearance %d)"
                      % (SIGNAL_W * 1000, CLEARANCE * 1000))
    with open(DSN, "w") as f:
        f.write(dsn)


# --------------------------------------------------------------------------
# Stage 2 - finish
# --------------------------------------------------------------------------

def zone(board, layer):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(board.FindNet("GND"))
    z.SetLocalClearance(mm(ZONE_CLEARANCE))
    z.SetMinThickness(mm(0.3))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(mm(0.5))
    z.SetThermalReliefSpokeWidth(mm(0.6))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    o = z.Outline()
    o.NewOutline()
    c = ZONE_CLEARANCE
    for x, y in ((c, c), (W - c, c), (W - c, H - c), (c, H - c)):
        o.Append(mm(x), mm(y))
    board.Add(z)


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def stitch(board):
    """Ground vias tying the two pours together.

    Candidates on a 1 mm grid that clear every other net's copper by the
    clearance rule, every pad, the edge and the mounting holes. Placed first
    next to the ground pads that carry current, then across the rest of the
    board at least 5 mm apart.
    """
    VIA_D, VIA_H = 0.8, 0.4
    gnd = board.FindNet("GND")
    tracks = []
    for t in board.GetTracks():
        a, b = t.GetStart(), t.GetEnd()
        tracks.append((pcbnew.ToMM(a.x), pcbnew.ToMM(a.y), pcbnew.ToMM(b.x),
                       pcbnew.ToMM(b.y),
                       pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu) if t.GetClass() == "PCB_VIA"
                                   else t.GetWidth()) / 2,
                       t.GetNetCode() == gnd.GetNetCode()))
    pads = []
    for p in board.GetPads():
        s = p.GetSize(pcbnew.F_Cu)
        pads.append((pcbnew.ToMM(p.GetX()), pcbnew.ToMM(p.GetY()),
                     pcbnew.ToMM(max(s.x, s.y)) / 2 * math.sqrt(2) if
                     p.GetShape(pcbnew.F_Cu) == pcbnew.PAD_SHAPE_RECT
                     else pcbnew.ToMM(max(s.x, s.y)) / 2))

    def ok(x, y):
        r = VIA_D / 2
        if x < 1.5 or y < 1.5 or x > W - 1.5 or y > H - 1.5:
            return False
        # the keep-out octagons reach HOLE_KEEPOUT / cos(22.5 deg) at the corners
        if any(math.hypot(x - hx, y - hy) < HOLE_KEEPOUT * 1.09 + VIA_D / 2
               for hx, hy in HOLES):
            return False
        for px, py, pr in pads:  # every pad here is hand-soldered: 0.8 mm
            if math.hypot(x - px, y - py) < pr + r + 0.8:
                return False
        for ax, ay, bx, by, hw, is_gnd in tracks:
            if seg_dist(x, y, ax, ay, bx, by) < hw + r + CLEARANCE:
                return False
        return True

    grid = [(x / 2, y / 2) for x in range(2, int(W * 2) - 1)
            for y in range(2, int(H * 2) - 1)]
    free = [p for p in grid if ok(*p)]
    placed = []

    def add(x, y):
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pt(x, y))
        v.SetWidth(mm(VIA_D))
        v.SetDrill(mm(VIA_H))
        v.SetNet(gnd)
        board.Add(v)
        placed.append((x, y))

    # Two beside each ground pad that carries current, then a 5 mm lattice
    hot = [("Q1", "3"), ("J1", "2"), ("U1", "2"), ("U1", "4"), ("C1", "2"),
           ("J2", "2"), ("U2", "7"), ("U2", "4"), ("C2", "2"), ("U3", "13")]
    for ref, num in hot:
        p = [q for q in board.FindFootprintByReference(ref).Pads() if q.GetNumber() == num][0]
        cx, cy = pcbnew.ToMM(p.GetX()), pcbnew.ToMM(p.GetY())
        for _ in range(2):
            near = sorted((math.hypot(x - cx, y - cy), x, y) for x, y in free
                          if all(math.hypot(x - a, y - b) >= 2.0 for a, b in placed))
            if near and near[0][0] < 5.0:
                add(near[0][1], near[0][2])
    for x, y in free:
        if all(math.hypot(x - a, y - b) >= 5.0 for a, b in placed):
            add(x, y)
    return len(placed)


def prune_stubs(board):
    """Delete the stubs the router leaves: track ends and vias that touch
    nothing, by KiCad's own connectivity. Repeats until none are left."""
    while True:
        board.BuildConnectivity()
        conn = board.GetConnectivity()
        dead = [t for t in board.GetTracks() if not t.IsLocked()
                and conn.TestTrackEndpointDangling(t, False)]
        if not dead:
            return
        for t in dead:
            board.Delete(t)


def stage_finish():
    board = pcbnew.LoadBoard(PCB)
    if not pcbnew.ImportSpecctraSES(board, SES):
        sys.exit("SES import failed")
    # GND is poured. The router draws it anyway; drop its GND copper
    for t in list(board.GetTracks()):
        if t.GetNetname() == "GND" and not t.IsLocked():
            board.Delete(t)
    prune_stubs(board)
    n = stitch(board)
    zone(board, pcbnew.F_Cu)
    zone(board, pcbnew.B_Cu)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(PCB, board)
    print("routed, %d stitching vias, poured; %d track segments"
          % (n, len([t for t in board.GetTracks() if t.GetClass() == "PCB_TRACK"])))


if __name__ == "__main__":
    {"place": stage_place, "finish": stage_finish}[sys.argv[1]]()

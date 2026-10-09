#!/usr/bin/env python3
"""Generate the pod PCB: the circuit the perfboard layout builds, as a real board.

Runs inside the KiCad 9 Docker image (it needs the pcbnew module). Call it
through build.sh, which also runs the autorouter and the exports:

    docs/pcb/build.sh

Two stages, because the autorouter (Freerouting) runs on the host in between:

    pod_pcb.py place   board outline, footprints, nets, silkscreen -> clown-pod.kicad_pcb
                       and clown-pod.dsn for the autorouter
    pod_pcb.py finish  import the routed .ses, pour ground on both layers, save

Same parts, same nets, same names as SCHEMATIC.md. Off-board parts (U1 the
MT3608 module, SW1, J1 the cell lead, J2 and J3 the arm leads) land on wire pads,
exactly as they do on the perfboard. The board is 70 x 30 mm, the size of the
3 x 7 cm perfboard it replaces, with an M2 hole in each corner.
"""

import json
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

# Nets that carry real current: the cell, the motor, the boost output, ground.
POWER = ["GND", "VBATT", "VBATT_RAW", "VBATT_SW", "MOTOR-", "+5V", "+5V_MCU"]
POWER_W = 0.8
SIGNAL_W = 0.3
CLEARANCE = 0.25


def mm(v):
    return pcbnew.FromMM(v)


def pt(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))


# --------------------------------------------------------------------------
# Netlist. Pad -> net for every part on the board. Net names are the
# schematic's. VBATT_RAW and VBATT_SW are the two short stretches of cell
# positive ahead of the fuse, which the schematic draws but does not name:
# J1-1 -> SW1 -> F1 -> VBATT.
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
    ("C2", "1"): "+5V", ("C2", "2"): "GND",
    ("C1", "1"): "+5V", ("C1", "2"): "GND",
    ("CR2", "1"): "+5V_MCU",      # cathode, to the XIAO
    ("CR2", "2"): "+5V",          # anode
    ("R1", "1"): "VBATT", ("R1", "2"): "VSENSE",
    ("R2", "1"): "VSENSE", ("R2", "2"): "GND",
    ("R3", "1"): "LED_DATA", ("R3", "2"): "LED_DATA_STRIP",
    ("R4", "1"): "GATE", ("R4", "2"): "GATE_Q",
    ("R5", "1"): "GATE_Q", ("R5", "2"): "GND",
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
# Footprint helpers
# --------------------------------------------------------------------------

def load(lib, name):
    fp = pcbnew.FootprintLoad(os.path.join(LIB, lib + ".pretty"), name)
    if fp is None:
        sys.exit("footprint not found: %s:%s" % (lib, name))
    return fp


def place(board, fp, ref, value, pad1, rot=0):
    """Put fp on the board with pad 1 at pad1 (mm), rotated rot degrees."""
    fp.SetReference(ref)
    fp.SetValue(value)
    board.Add(fp)
    fp.SetOrientationDegrees(rot)
    p1 = [p for p in fp.Pads() if p.GetNumber() == "1"][0].GetPosition()
    fp.Move(pt(*pad1) - p1)
    fp.Value().SetVisible(False)
    return fp


def silk_line(fp_or_board, x1, y1, x2, y2, width=0.15, layer=pcbnew.F_SilkS):
    s = pcbnew.PCB_SHAPE(fp_or_board)
    s.SetShape(pcbnew.SHAPE_T_SEGMENT)
    s.SetStart(pt(x1, y1))
    s.SetEnd(pt(x2, y2))
    s.SetLayer(layer)
    s.SetWidth(mm(width))
    fp_or_board.Add(s)


def silk_rect(fp_or_board, x1, y1, x2, y2, width=0.15, layer=pcbnew.F_SilkS):
    for a, b in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)),
                 ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        silk_line(fp_or_board, a[0], a[1], b[0], b[1], width, layer)


def text(board, s, x, y, size=1.0, layer=pcbnew.F_SilkS, rot=0, bold=False,
         justify=None):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(s)
    t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(mm(size), mm(size)))
    t.SetTextThickness(mm(size * (0.2 if bold else 0.15)))
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


def custom(board, ref, value, x, y):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(pt(x, y))
    fp.SetFPID(pcbnew.LIB_ID("clown", ref))
    fp.Value().SetVisible(False)
    board.Add(fp)
    return fp


def courtyard(fp, x1, y1, x2, y2):
    silk_rect(fp, x1, y1, x2, y2, 0.05, pcbnew.F_CrtYd)


def wire_pads(board, ref, value, labels, x, y, pitch, axis, label_side):
    """A row of plain plated holes for wires. Pad 1 is square."""
    fp = custom(board, ref, value, x, y)
    for i, lab in enumerate(labels):
        px, py = (x + i * pitch, y) if axis == "x" else (x, y + i * pitch)
        pth(fp, str(i + 1), px, py, 1.1, 2.2,
            pcbnew.PAD_SHAPE_RECT if i == 0 else pcbnew.PAD_SHAPE_CIRCLE)
        if label_side == "left":
            text(board, lab, px - 1.8, py, 0.8, justify="right")
        elif label_side == "above":
            text(board, lab, px, py - 2.3, 0.6)
    n = len(labels) - 1
    if axis == "x":
        courtyard(fp, x - 1.35, y - 1.35, x + n * pitch + 1.35, y + 1.35)
    else:
        courtyard(fp, x - 1.35, y - 1.35, x + 1.35, y + n * pitch + 1.35)
    fp.Reference().SetVisible(False)
    return fp


# --------------------------------------------------------------------------
# Stage 1 - place
# --------------------------------------------------------------------------

def write_project():
    pro = {
        "board": {"design_settings": {"rules": {
            "min_clearance": 0.2, "min_track_width": 0.2,
            "min_via_diameter": 0.6, "min_through_hole_diameter": 0.3,
            "min_copper_edge_clearance": 0.3, "min_hole_clearance": 0.25,
            "min_silk_clearance": 0.0},
            # A thermal whose spokes reach only a pour island is still
            # connected by its track; the unconnected-items check covers it
            "rule_severities": {"starved_thermal": "warning"}}},
        "net_settings": {
            "classes": [
                {"name": "Default", "clearance": CLEARANCE, "track_width": SIGNAL_W,
                 "via_diameter": 0.8, "via_drill": 0.4, "priority": 2147483647},
                {"name": "Power", "clearance": CLEARANCE, "track_width": POWER_W,
                 "via_diameter": 1.2, "via_drill": 0.6, "priority": 0},
            ],
            "meta": {"version": 4},
            "netclass_patterns": [{"netclass": "Power", "pattern": n} for n in POWER],
        },
        "meta": {"filename": NAME + ".kicad_pro", "version": 3},
    }
    with open(PRO, "w") as f:
        json.dump(pro, f, indent=2)


def stage_place():
    board = pcbnew.BOARD()

    # Outline, with 1 mm corner radius
    r = 1.0
    edge = pcbnew.Edge_Cuts
    for (x1, y1, x2, y2) in ((r, 0, W - r, 0), (W, r, W, H - r),
                             (W - r, H, r, H), (0, H - r, 0, r)):
        silk_line(board, x1, y1, x2, y2, 0.1, edge)
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

    # Mounting holes, M2, one per corner
    for i, (x, y) in enumerate(((2.5, 2.5), (W - 2.5, 2.5), (2.5, H - 2.5), (W - 2.5, H - 2.5))):
        fp = load("MountingHole", "MountingHole_2.2mm_M2")
        fp.SetReference("H%d" % (i + 1))
        board.Add(fp)
        fp.SetPosition(pt(x, y))
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

    # --- U3 XIAO ESP32-C3, on two 7-pin headers, USB-C off the left edge ----
    # Module pin order, top view: pins 1-7 down one side from the USB end,
    # 8-14 back up the other, so pin 14 (5V) sits across from pin 1 (GPIO2).
    # USB to the left puts pins 1-7 on the bottom row.
    x0, ytop, ybot = 4.0, 6.38, 21.62
    u3 = custom(board, "U3", "XIAO ESP32-C3", x0, ybot)
    u3.SetFPID(pcbnew.LIB_ID("clown", "XIAO_ESP32C3_Headers"))
    gpio_bot = ["GPIO2", "GPIO3", "GPIO4", "GPIO5", "GPIO6", "GPIO7", "GPIO21"]
    gpio_top = ["5V", "GND", "3V3", "GPIO10", "GPIO9", "GPIO8", "GPIO20"]
    for i in range(7):
        x = x0 + i * 2.54
        pth(u3, str(i + 1), x, ybot, 1.0, 1.7,
            pcbnew.PAD_SHAPE_RECT if i == 0 else pcbnew.PAD_SHAPE_CIRCLE)
        pth(u3, str(14 - i), x, ytop, 1.0, 1.7)
        text(board, gpio_bot[i], x, ybot - 2.0, 0.6, rot=90, justify="left")
        text(board, gpio_top[i], x, ytop + 2.0, 0.6, rot=90, justify="right")
    bx1, bx2 = 1.1, 22.1  # 21 mm module body
    silk_rect(u3, bx1, 5.1, bx2, 22.9)
    courtyard(u3, bx1 - 1.5, 5.0, bx2 + 0.25, 23.15)
    text(board, "USB-C", 2.0, 14.0, 0.8, rot=90)
    u3.Reference().SetPosition(pt(16.5, 14.0))
    u3.Reference().SetTextAngleDegrees(90)

    # --- U2 74AHCT125, DIP-14, notch to the left, pin 1 bottom-left ---------
    u2 = place(board, load("Package_DIP", "DIP-14_W7.62mm_Socket"),
               "U2", "74AHCT125", (27.0, 19.81), 90)

    # --- C2 0.1 uF right over U2 pin 14 -------------------------------------
    place(board, load("Capacitor_THT", "C_Disc_D5.0mm_W2.5mm_P5.00mm"),
          "C2", "0.1uF", (27.0, 8.4), 0)

    # --- CR2 1N5819, USB isolation, banded end toward the XIAO 5V pin --------
    place(board, load("Diode_THT", "D_DO-41_SOD81_P10.16mm_Horizontal"),
          "CR2", "1N5819", (6.5, 2.6), 0)

    # --- R1/R2 battery divider, top edge ------------------------------------
    rfp = ("Resistor_THT", "R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
    place(board, load(*rfp), "R1", "100k", (20.0, 2.6), 0)
    place(board, load(*rfp), "R2", "100k", (33.0, 2.6), 0)

    # --- C1 1000 uF, by the strip plug J2 -----------------------------------
    place(board, load("Capacitor_THT", "CP_Radial_D10.0mm_P5.00mm"),
          "C1", "1000uF 16V", (46.5, 9.0), 0)

    # --- Q1 RFP30N06LE, TO-220 standing up, G D S left to right -------------
    place(board, load("Package_TO_SOT_THT", "TO-220-3_Vertical"),
          "Q1", "RFP30N06LE", (47.0, 19.2), 0)

    # --- R3 data series, R4 gate series, R5 gate pulldown --------------------
    place(board, load(*rfp), "R3", "470R", (56.5, 3.6), -90)
    r3 = board.FindFootprintByReference("R3").Reference()
    r3.SetPosition(pt(56.5, 15.6))
    place(board, load(*rfp), "R4", "100R", (44.0, 23.2), 0)
    place(board, load(*rfp), "R5", "10k", (44.0, 26.8), 0)
    for ref, y in (("R4", 23.2), ("R5", 26.8)):  # inside the body, no room above
        board.FindFootprintByReference(ref).Reference().SetPosition(pt(49.08, y))

    # --- F1 PPTC, radial, 5.08 mm pitch -------------------------------------
    f1 = custom(board, "F1", "PPTC 1.85-2.5A", 33.5, 26.8)
    f1.SetFPID(pcbnew.LIB_ID("clown", "PPTC_Radial_P5.08mm"))
    pth(f1, "1", 33.5, 26.8, 1.0, 2.0, pcbnew.PAD_SHAPE_RECT)
    pth(f1, "2", 38.58, 26.8, 1.0, 2.0)
    silk_rect(f1, 31.5, 25.0, 40.6, 28.6)
    courtyard(f1, 31.25, 24.75, 40.85, 28.85)
    f1.Reference().SetPosition(pt(36.04, 23.6))

    # --- Wire pads ----------------------------------------------------------
    wire_pads(board, "U1", "MT3608 module", ["IN+", "IN-", "OUT+", "OUT-"],
              6.5, 27.2, 3.0, "x", "above")
    wire_pads(board, "SW1", "KCD1 rocker", ["A", "B"], 20.0, 27.2, 3.0, "x", "above")
    wire_pads(board, "J1", "Cell, PH2.0", ["+", "-"], 26.5, 27.2, 3.0, "x", "above")
    wire_pads(board, "J2", "Strip SM-3", ["J2-1 +5V", "J2-2 GND", "J2-3 DATA"],
              66.5, 6.4, 2.8, "y", "left")
    wire_pads(board, "J3", "Elbow SM-4", ["J3-1 M+", "J3-2 M-", "J3-3 TRIG", "J3-4 GND"],
              66.5, 15.0, 2.8, "y", "left")
    text(board, "U1 MT3608", 11.0, 23.75, 0.65)
    text(board, "SW1", 21.5, 23.75, 0.65)
    text(board, "J1 CELL", 28.0, 23.75, 0.65)

    # Board name, and back-side notes
    text(board, "CLOWN POD " + REV, 60.3, 28.5, 0.65, bold=True)
    text(board, "CLOWN POD " + REV, 35.0, 15.0, 1.5, layer=pcbnew.B_SilkS, bold=True)
    text(board, "Trim U1 to 5.00 V before fitting U3", 35.0, 18.0, 0.9,
         layer=pcbnew.B_SilkS)

    # Nets
    for (ref, num), name in NETS.items():
        net = board.FindNet(name)
        if net is None:
            net = pcbnew.NETINFO_ITEM(board, name)
            board.Add(net)
    for (ref, num), name in NETS.items():
        fp = board.FindFootprintByReference(ref)
        pads = [p for p in fp.Pads() if p.GetNumber() == num]
        if len(pads) != 1:
            sys.exit("no pad %s %s" % (ref, num))
        pads[0].SetNet(board.FindNet(name))

    # Keep the router 1 mm off the board edge: one keep-out strip per side
    # (the router can't read a keep-out with a hole in it)
    for x1, y1, x2, y2 in ((0, 0, W, 1), (0, H - 1, W, H), (0, 0, 1, H), (W - 1, 0, W, H)):
        keep = pcbnew.ZONE(board)
        keep.SetIsRuleArea(True)
        keep.SetDoNotAllowTracks(True)
        keep.SetDoNotAllowVias(True)
        keep.SetDoNotAllowPads(False)
        keep.SetDoNotAllowFootprints(False)
        keep.SetLayerSet(pcbnew.LSET.AllCuMask())
        o = keep.Outline()
        o.NewOutline()
        for x, y in ((x1, y1), (x2, y1), (x2, y2), (x1, y2)):
            o.Append(mm(x), mm(y))
        board.Add(keep)

    # Q1 source carries the motor current: solid to the ground pour, no spokes
    for p in board.FindFootprintByReference("Q1").Pads():
        if p.GetNumber() == "3":
            p.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)

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
    whatever the project says. Rewrite the class block: power nets 0.8 mm on
    1.0 mm vias, everything else 0.3 mm on 0.8 mm vias, 0.25 mm clearance.
    """
    with open(DSN) as f:
        dsn = f.read()
    start = dsn.index("    (class kicad_default")
    end = dsn.index("  (wiring")
    nets = [l.strip()[len("(net "):] for l in dsn.splitlines()
            if l.strip().startswith("(net ")]
    quote = lambda n: '"%s"' % n if "-" in n or "+" in n else n
    power = [n.strip('"') for n in nets if n.strip('"') in POWER]
    signal = [n.strip('"') for n in nets if n.strip('"') not in POWER]

    def cls(name, members, width, via):
        return ("    (class %s %s\n      (circuit (use_via \"%s\"))\n"
                "      (rule (width %d) (clearance %d))\n    )\n"
                % (name, " ".join(quote(n) for n in members), via,
                   width * 1000, CLEARANCE * 1000))

    vias = ""
    for d, h in ((800, 400), (1200, 600)):
        vias += ('    (padstack "Via[0-1]_%d:%d_um"\n'
                 "      (shape (circle F.Cu %d))\n      (shape (circle B.Cu %d))\n"
                 "      (attach off)\n    )\n" % (d, h, d, d))
    dsn = dsn[:start] + cls("signal", signal, SIGNAL_W, "Via[0-1]_800:400_um") \
        + cls("power", power, POWER_W, "Via[0-1]_1200:600_um") + "  )\n" + dsn[end:]
    vstart = dsn.index('    (padstack "Via[0-1]_600:300_um"')
    vend = dsn.index("    )\n", vstart) + len("    )\n")
    dsn = dsn[:vstart] + vias + dsn[vend:]
    dsn = dsn.replace('(via "Via[0-1]_600:300_um")',
                      '(via "Via[0-1]_800:400_um" "Via[0-1]_1200:600_um")')
    dsn = dsn.replace("(width 200)\n      (clearance 200)",
                      "(width %d)\n      (clearance %d)" % (SIGNAL_W * 1000, CLEARANCE * 1000))
    with open(DSN, "w") as f:
        f.write(dsn)


# --------------------------------------------------------------------------
# Stage 2 - finish
# --------------------------------------------------------------------------

def zone(board, layer):
    z = pcbnew.ZONE(board)
    z.SetLayer(layer)
    z.SetNet(board.FindNet("GND"))
    z.SetLocalClearance(mm(0.4))
    z.SetMinThickness(mm(0.25))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    z.SetThermalReliefGap(mm(0.4))
    z.SetThermalReliefSpokeWidth(mm(0.5))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    o = z.Outline()
    o.NewOutline()
    for x, y in ((0.3, 0.3), (W - 0.3, 0.3), (W - 0.3, H - 0.3), (0.3, H - 0.3)):
        o.Append(mm(x), mm(y))
    board.Add(z)


def stage_finish():
    board = pcbnew.LoadBoard(PCB)
    if not pcbnew.ImportSpecctraSES(board, SES):
        sys.exit("SES import failed")
    zone(board, pcbnew.F_Cu)
    zone(board, pcbnew.B_Cu)
    pcbnew.ZONE_FILLER(board).Fill(board.Zones())
    pcbnew.SaveBoard(PCB, board)
    print("routed and poured;", len(board.GetTracks()), "track segments")


if __name__ == "__main__":
    {"place": stage_place, "finish": stage_finish}[sys.argv[1]]()

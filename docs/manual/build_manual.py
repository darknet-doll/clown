#!/usr/bin/env python3
"""Generate the clown bubble-sleeve build manual as a PDF.

Page 1 is the numbered parts list with a plain-English note under each part.
Every following page is build steps that reference those numbers in [brackets].

Usage:  python3 docs/manual/build_manual.py
Output: Clown-Build-Manual.pdf in the repo root.
"""

import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ACCENT = colors.HexColor("#C2185B")
INK = colors.HexColor("#1A1A1A")
MUTED = colors.HexColor("#5A5A5A")
RULE = colors.HexColor("#D8D8D8")
PANEL = colors.HexColor("#F5F0F2")

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "Clown-Build-Manual.pdf")

MARGIN = 0.55 * inch
PAGE_W, PAGE_H = LETTER


# --------------------------------------------------------------------------
# Parts — page 1. (number, name, qty, plain-English note)
# --------------------------------------------------------------------------

PARTS = [
    ("THE BUBBLES", [
        (1, "Bambu Lab Electric Bubble Maker Kit 01 (P6M)", "x1",
         "A tiny fan that blows air across a film of soap. You are not modifying it "
         "&mdash; you are just taking over the decision of <i>when</i> it switches on. "
         "Each kit also includes a battery [8] and a charger."),
    ]),
    ("THE LIGHT", [
        (2, "WS2812B LED strip, 60 LED/m, 5V, black PCB, IP65", "0.4 m",
         "A ribbon where every single light has its own chip inside, so each one takes "
         "orders individually down one data wire. That is the only reason a travelling "
         "comet is possible &mdash; an ordinary strip can only be one colour at a time. "
         "IP65 is the clear silicone sleeve that keeps the soap out."),
        (3, "Thin, pale, stretchy glove", "x1",
         "The strip hides under this. Fabric spreads the light into a smooth glow "
         "instead of visible dots &mdash; but only if it is thin and pale. Thick or dark "
         "fabric, especially leather, swallows almost all of it."),
    ]),
    ("THE BRAIN", [
        (4, "Seeed XIAO ESP32-C3", "x1",
         "A complete computer the size of a postage stamp. It watches the trigger and "
         "decides what all 21 lights do, about 60 times a second. You reprogram it with "
         "a USB-C cable."),
        (5, "74AHCT125 level shifter", "x1",
         "A translator that also shouts. The brain speaks at 3.3V; the strip is listening "
         "for 5V. Usually the strip <i>sort of</i> hears it anyway &mdash; which is exactly "
         "the problem. Leave this out and your lights flicker randomly, normally for the "
         "first time once you are in costume."),
    ]),
    ("MOTOR CONTROL", [
        (6, "N-channel logic-level MOSFET module", "x1",
         "An electric switch with no moving parts. The brain can think, but it cannot "
         "push enough power to spin a motor, so it flicks this instead and this lets the "
         "big current through."),
        (7, "1N5819 flyback diode", "x1",
         "A motor is really just a coil of wire, and cutting power to a coil makes it kick "
         "a nasty voltage spike backwards. This is a one-way valve that gives the spike a "
         "safe loop to burn itself out in. It costs 20 cents; skip it and the MOSFET [6] "
         "eventually dies."),
    ]),
    ("POWER", [
        (8, "Protected 18650 cell", "x1 + spares",
         "A rechargeable battery &mdash; one comes free with each bubble kit [1]. "
         "<i>Protected</i> means a guardian circuit inside cuts it off before you "
         "over-drain or over-charge it. Do not substitute cheaper unprotected cells. "
         "This is strapped to your arm."),
        (9, "18650 sled with wire leads", "x1",
         "The slot the battery sits in, so you can swap a flat cell for a fresh one "
         "without a soldering iron. Print one with a lid that clicks shut."),
        (10, "5V boost converter module", "x1",
         "A pump, but for voltage. The battery only makes about 3.7V and the lights and "
         "brain need 5V. Here it only has to carry the lights (~0.3A) because the motor "
         "runs straight off the battery, so a small cheap one is genuinely fine."),
        (11, "2A resettable polyfuse (PPTC)", "x1",
         "A safety valve that resets itself. If something shorts out, it suddenly becomes "
         "very resistant and chokes the current off before anything gets hot. Let it cool "
         "and it goes back to normal by itself."),
        (12, "100 kilo-ohm resistors", "x2",
         "Two resistors that shrink the battery voltage neatly in half, so the brain [4] "
         "can measure it without being damaged. This is what lets the costume warn you "
         "that the cell is nearly flat instead of just dying."),
    ]),
    ("SIGNAL CONDITIONING", [
        (13, "1000 uF electrolytic capacitor", "x1",
         "A tiny water tank for electricity. When a lot of LEDs switch on in the same "
         "instant they all gulp power at once; the tank smooths out the gulp so the "
         "voltage does not dip. Polarised &mdash; the leg with the stripe is negative, and "
         "backwards it pops."),
        (14, "330-470 ohm resistor", "x1",
         "A speed bump on the data wire. It softens the sharp edge of the signal so it "
         "does not bounce back down the wire and garble the message to the first pixel. "
         "Skip it and pixel 1 misbehaves while all the others are fine."),
    ]),
    ("THE TRIGGER", [
        (15, "Snap-action lever microswitch", "x1",
         "A clicky button with a little metal arm sticking off it. The arm is the whole "
         "point: it gives you a wide target, so you can fire mid-performance without "
         "looking or aiming. It also clicks, so you feel it go."),
    ]),
    ("WIRE AND MATERIALS", [
        (16, "Silicone hookup wire, 22-26 AWG", "as needed",
         "Wire with soft rubbery insulation instead of stiff plastic. It survives "
         "thousands of bends. Ordinary wire &mdash; especially solid-core &mdash; snaps at "
         "the elbow and wrist within a few hours of wearing it. Thicker for power, "
         "thinner for signals."),
        (17, "Heat-shrink tubing, assorted", "as needed",
         "Plastic sleeve that shrinks tight when heated, sealing and insulating each "
         "solder joint. Slide it onto the wire BEFORE you solder. Everyone forgets once."),
    ]),
    ("TOOLS", [
        (18, "Multimeter", "x1",
         "For checking polarity before you connect the battery the first time. Two minutes "
         "here saves re-ordering a fried brain [4] and strip [2]."),
        (19, "Soldering iron, solder, flux", "as needed",
         "For all of the above. Work somewhere ventilated; flux fumes are unpleasant."),
        (20, "3D printer", "x1",
         "For the trigger plate, the battery sled [9] and the controller pod. You already "
         "have one."),
    ]),
]


# --------------------------------------------------------------------------
# Parts — page 1-2. (number, name, per-arm, buy-for-two, plain-English note)
#
# "Per arm" and "buy" are deliberately separate columns. Conflating them is the
# single easiest way to end up halfway through a build with one glove.
# --------------------------------------------------------------------------

PARTS = [
    ("THE BUBBLES", [
        (1, "Bambu Lab Electric Bubble Maker Kit 01 (P6M)", "1", "2",
         "A blower head, a one-way-valve bottle cap, silicone hose and a gravity ball. "
         "You are not modifying how it makes bubbles &mdash; only taking over the decision "
         "of <i>when</i>. Each kit also includes a protected cell [12] on a PH2.0 pigtail "
         "and a matching USB charger. <b>The bottle is not included.</b>"),
        (2, "Bottle, 24T or 30T neck", "1", "2 + a spare",
         "The reservoir the kit's cap screws onto. Bambu says explicitly: not a drinking "
         "bottle. Choose the size deliberately &mdash; a full bottle is the heaviest single "
         "item on your arm, so this is your main lever on how tiring the costume is."),
        (3, "Silicone tube, 3 x 5 mm", "&mdash;", "1 m",
         "Same size as the hose in the kit. You need it for the mount test in Step 7, which "
         "decides where the bottle lives. Stock aquarium tubing; costs almost nothing. Keep "
         "the offcut as a field spare."),
        (4, "Bubble solution", "&mdash;", "all you can carry",
         "This runs out long before the battery does. It is the actual limit on your night."),
    ]),
    ("THE LIGHT", [
        (5, "WS2812B LED strip, 60 LED/m, 5V, black PCB, IP65", "0.4 m", "1 m roll",
         "A ribbon where every single light has its own chip inside, so each one takes "
         "orders individually down one data wire. That is the only reason a travelling "
         "comet is possible &mdash; an ordinary strip can only be one colour at a time. "
         "IP65 is the clear silicone sleeve that keeps the soap out."),
        (6, "Thin, pale, stretchy glove", "1", "a pair",
         "The hand strip hides under this. Fabric spreads the light into a smooth glow "
         "instead of visible dots &mdash; but only if it is thin and pale. Thick or dark "
         "fabric, especially leather, swallows almost all of it."),
        (7, "Sleeve or arm warmer", "1", "a pair",
         "Same job as the glove [6], for the forearm segment. Same fabric rules. Buy both "
         "at once and test them together &mdash; a glove that glows over a sleeve that does "
         "not is a half-lit arm."),
    ]),
    ("THE BRAIN", [
        (8, "Seeed XIAO ESP32-C3", "1", "2",
         "A complete computer the size of a postage stamp. It watches its own arm's trigger "
         "and decides what all 21 lights do, about 60 times a second. You reprogram it over "
         "USB-C &mdash; with a data cable [34], not a charge-only one."),
        (9, "74AHCT125 level shifter", "1", "2 (get 5)",
         "A translator that also shouts. The brain speaks at 3.3V; the strip is listening "
         "for 5V. Usually the strip <i>sort of</i> hears it anyway &mdash; which is exactly "
         "the problem. Leave this out and your lights flicker randomly, normally for the "
         "first time once you are in costume."),
    ]),
    ("MOTOR CONTROL", [
        (10, "N-channel logic-level MOSFET", "1", "2",
         "An electric switch with no moving parts. The brain can think, but it cannot "
         "push enough power to spin a motor, so it flicks this instead and this lets the "
         "big current through. <b>Do not buy an IRF520 module</b> &mdash; it is the top "
         "search result and it is not logic-level, so at 3.3V it only half-opens and gets "
         "hot. Prefer AO3400, or drive the gate at 5V through a spare gate on the "
         "74AHCT125 [9], which is what Step 4 does."),
        (11, "1N5819 flyback diode", "1", "2 (get 10)",
         "A motor is really just a coil of wire, and cutting power to a coil makes it kick "
         "a nasty voltage spike backwards. This is a one-way valve that gives the spike a "
         "safe loop to burn itself out in. It costs 20 cents; skip it and the MOSFET [10] "
         "eventually dies."),
    ]),
    ("POWER", [
        (12, "Protected 18650 cell", "1", "2 + 2 spares",
         "A rechargeable battery &mdash; one comes free with each bubble kit [1], already on "
         "a <b>PH2.0 pigtail</b>. Keep that pigtail: it is what the kit's charger mates to, "
         "so a flat cell swaps pod to charger with no adapter. <i>Protected</i> means a "
         "guardian circuit cuts it off before you over-drain it. Never substitute unprotected "
         "cells. This is strapped to your arm."),
        (13, "18650 sled with wire leads", "1", "2",
         "The slot the battery sits in, so you can swap a flat cell for a fresh one "
         "without a soldering iron. Print one with a lid that clicks shut."),
        (14, "5V boost converter module", "1", "2",
         "A pump, but for voltage. The battery only makes about 3.7V and the lights and "
         "brain need 5V. Here it only has to carry the lights (~0.3A) because the motor "
         "runs straight off the battery, so a small cheap one is genuinely fine."),
        (15, "2A resettable polyfuse (PPTC)", "1", "2 (get 5)",
         "A safety valve that resets itself. If something shorts out, it suddenly becomes "
         "very resistant and chokes the current off before anything gets hot. Let it cool "
         "and it goes back to normal by itself."),
        (16, "100 kilo-ohm resistors", "2", "4",
         "Two resistors that shrink the battery voltage neatly in half, so the brain [8] "
         "can measure it without being damaged. This is what lets the costume warn you "
         "that the cell is nearly flat instead of just dying."),
    ]),
    ("SIGNAL CONDITIONING", [
        (17, "1000 uF electrolytic capacitor", "1", "2",
         "A tiny water tank for electricity. When a lot of LEDs switch on in the same "
         "instant they all gulp power at once; the tank smooths out the gulp so the "
         "voltage does not dip. Polarised &mdash; the leg with the stripe is negative, and "
         "backwards it pops."),
        (18, "330-470 ohm resistor", "1", "2",
         "A speed bump on the data wire. It softens the sharp edge of the signal so it "
         "does not bounce back down the wire and garble the message to the first pixel. "
         "Skip it and pixel 1 misbehaves while all the others are fine."),
    ]),
    ("THE TRIGGER", [
        (19, "Snap-action lever microswitch", "1", "2 + 2 spares",
         "A clicky button with a little metal arm sticking off it. <b>One per hand</b> "
         "&mdash; each hand fires its own arm, and nothing crosses the torso. The arm is "
         "the whole point: a wide target you can hit mid-performance without looking. It "
         "also clicks, so you feel it go."),
    ]),
    ("CONNECTORS &mdash; SO IT COMES APART", [
        (20, "JST-SM pigtail pair, 6-pin", "1", "2 + 1 spare",
         "The <b>elbow</b> plug: strip 5V, ground and data, plus the trigger's two wires, "
         "plus a second ground. Both the trigger and the motor have to reach the pod from "
         "your hand, so both cross <i>both</i> joints &mdash; which is why this is 6-pin and "
         "not 3. Pin 6 is not spare: the elbow run is the longest in the costume, and a "
         "second ground cuts the voltage drop."),
        (21, "JST-SM pigtail pair, 5-pin", "1", "2 + 1 spare",
         "The <b>wrist</b> plug: the strip's three conductors plus this hand's trigger. One "
         "pull and the whole glove [6] comes off. Mate it 3-4 cm above the wrist crease, "
         "where the skin barely moves &mdash; never on the crease itself."),
        (22, "JST-SM pigtail pair, 2-pin", "2", "4 + 2 spares",
         "The motor run, one at each joint. Kept off the data line on purpose: an amp of "
         "switched PWM bundled against a WS2812 wire is asking for flicker. These two are "
         "the only identical pair in the build, and that is safe &mdash; they sit on the same "
         "net, so cross-mating them just shortens the run."),
        (23, "JST-ZH pigtail pair, 2-pin, 1.5 mm", "1", "2 + 2 spares",
         "Goes at the microswitch [19] itself, so a dead trigger is a ten-second swap "
         "rather than a soldering job. <b>It must not be PH2.0.</b> Every cell [12] ships on "
         "a PH2.0 lead, and one wrong plug in a dark room would put 3.7V straight onto "
         "GPIO3. ZH is 1.5 mm pitch, PH is 2.0 &mdash; they physically will not mate."),
        (24, "Dielectric grease", "&mdash;", "1 small tube",
         "Non-conductive waterproof goo. A smear in each connector shell stops soap residue "
         "corroding the contacts over a season. The alternative is intermittent faults you "
         "will chase for hours."),
    ]),
    ("WIRE AND MATERIALS", [
        (25, "Silicone hookup wire, 22-26 AWG", "&mdash;", "one assortment",
         "Wire with soft rubbery insulation instead of stiff plastic. It survives "
         "thousands of bends. Ordinary wire &mdash; especially solid-core &mdash; snaps at "
         "the elbow and wrist within a few hours of wearing it. Thicker for power, "
         "thinner for signals."),
        (26, "Heat-shrink tubing, assorted", "&mdash;", "one assortment",
         "Plastic sleeve that shrinks tight when heated, sealing and insulating each "
         "solder joint. Slide it onto the wire BEFORE you solder. Everyone forgets once."),
        (27, "Protoboard, small", "1", "2",
         "The perforated board the pod's components sit on. Nothing exotic &mdash; a 4 x 6 cm "
         "piece per arm is plenty."),
        (28, "Hot glue, or clear RTV silicone", "&mdash;", "1",
         "Seals the cut ends of the strip [5] against soap. Easy to forget when ordering "
         "and annoying to be without at Step 3."),
        (29, "Needle and thread, or fabric glue", "&mdash;", "1",
         "For sewing the strip channels into the glove [6] and sleeve [7]. A channel the "
         "strip can slide inside &mdash; not glued down flat."),
        (30, "Fabric marker pen", "&mdash;", "1",
         "For marking where your finger pads land on your palm in Step 1. That mark is "
         "where the trigger [19] goes."),
    ]),
    ("TOOLS &mdash; ONE EACH, NOT ONE PER ARM", [
        (31, "Multimeter", "&mdash;", "1",
         "Not optional. Polarity before every first power-up, continuity for tracing a dead "
         "segment, and actual current draw. Minimum spec: DC volts, AC volts, DC current to "
         "2A on a <b>fused</b> input, resistance, and <b>continuity with a fast audible "
         "beeper</b> &mdash; that beeper is what you will live in. Capacitance is worth "
         "having. Auto-ranging, backlight and hold, because you will be under a table."),
        (32, "Soldering iron, flux-core solder, flux pen", "&mdash;", "1",
         "Buy <b>flux-core</b> solder, 0.8 mm; solid wire with no flux is miserable. The "
         "flux pen is separate &mdash; the IP65 strip pads are the grubbiest joints here and "
         "want extra. On leaded vs lead-free: <b>the fumes that make you feel ill are the "
         "flux, not the lead</b>, so ventilate either way. The real lead risk is ingestion, "
         "closed by washing your hands. Lead-free needs a hotter iron and wets worse, which "
         "bites on strip pads; 63/37 is more forgiving. Either is defensible."),
        (33, "Thermal camera", "&mdash;", "1 (borrow it)",
         "Optional, genuinely useful. Turns Step 6's \"touch it and see if it is warm\" into "
         "a measurement, and catches what a fingertip misses: a boost [14] running hot from "
         "a short downstream, a MOSFET [10] that turned out not to be logic-level, a strip "
         "section drawing more than its neighbours. One borrowed session is plenty."),
        (34, "USB-C cable, data capable", "&mdash;", "1",
         "A charge-only cable looks identical and will cost you half an hour of confusion "
         "before you think to suspect it."),
        (35, "3D printer", "&mdash;", "1",
         "For the trigger plate, the battery sled [13], the controller pod and the bubbler "
         "mount. You already have one."),
    ]),
]
# --------------------------------------------------------------------------
# Styles
# --------------------------------------------------------------------------

ss = getSampleStyleSheet()


def style(name, **kw):
    base = dict(name=name, fontName="Helvetica", fontSize=9, leading=12,
                textColor=INK, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(**base)


S = {
    "title": style("title", fontName="Helvetica-Bold", fontSize=22, leading=24,
                   textColor=INK, spaceAfter=2),
    "subtitle": style("subtitle", fontSize=10.5, leading=13, textColor=ACCENT,
                      spaceAfter=8),
    "lede": style("lede", fontSize=8, leading=10.2, textColor=MUTED, spaceAfter=4),
    "cat": style("cat", fontName="Helvetica-Bold", fontSize=7.2, leading=8.5,
                 textColor=ACCENT, spaceBefore=6, spaceAfter=2),
    "part": style("part", fontName="Helvetica-Bold", fontSize=8.2, leading=9.8,
                  spaceAfter=1),
    "eli5": style("eli5", fontSize=6.9, leading=8.5, textColor=MUTED,
                  leftIndent=10, spaceAfter=4),
    "h1": style("h1", fontName="Helvetica-Bold", fontSize=15, leading=18,
                spaceBefore=4, spaceAfter=7),
    "h2": style("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                spaceBefore=11, spaceAfter=4),
    "body": style("body", fontSize=9, leading=12.4, spaceAfter=6),
    "bullet": style("bullet", fontSize=9, leading=12.4, leftIndent=13,
                    bulletIndent=3, spaceAfter=3),
    "note": style("note", fontSize=8.5, leading=11.5, textColor=INK,
                  leftIndent=8, rightIndent=8, spaceBefore=3, spaceAfter=3),
    "cell": style("cell", fontSize=7.8, leading=9.6),
    "cellb": style("cellb", fontName="Helvetica-Bold", fontSize=7.8, leading=9.6),
    "code": style("code", fontName="Courier", fontSize=8, leading=10.5,
                  leftIndent=10, textColor=INK, spaceAfter=6),
}


def P(txt, s="body"):
    return Paragraph(txt, S[s])


def bullets(items, s="bullet"):
    return [Paragraph(t, S[s], bulletText="•") for t in items]


def ref(n):
    """Render a part reference like [4] in accent colour."""
    return '<b><font color="#C2185B">[%d]</font></b>' % n


def callout(title, body):
    """A tinted warning/note panel."""
    inner = [P("<b>%s</b>" % title, "note"), P(body, "note")]
    t = Table([[inner]], colWidths=[None])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PANEL),
        ("LINEBEFORE", (0, 0), (0, -1), 2.2, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def grid(rows, widths, header=True):
    data = []
    for i, r in enumerate(rows):
        st = "cellb" if (header and i == 0) else "cell"
        data.append([Paragraph(c, S[st]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    st = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE),
    ]
    if header:
        st += [("BACKGROUND", (0, 0), (-1, 0), PANEL),
               ("LINEBELOW", (0, 0), (-1, 0), 0.9, ACCENT)]
    t.setStyle(TableStyle(st))
    return t


# --------------------------------------------------------------------------
# Page furniture
# --------------------------------------------------------------------------

def chrome(canvas, doc, label):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, MARGIN - 6, PAGE_W - MARGIN, MARGIN - 6)
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(MARGIN, MARGIN - 17, label)
    canvas.drawRightString(PAGE_W - MARGIN, MARGIN - 17, "Page %d" % doc.page)
    canvas.restoreState()


def on_parts(canvas, doc):
    chrome(canvas, doc, "clown — bubble sleeve — parts")


def on_steps(canvas, doc):
    chrome(canvas, doc, "clown — bubble sleeve — assembly")


def build():
    doc = BaseDocTemplate(
        os.path.abspath(OUT), pagesize=LETTER,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=MARGIN,
        title="Clown Bubble Sleeve — Build Manual",
        author="darknetdoll",
    )

    usable_w = PAGE_W - 2 * MARGIN
    usable_h = PAGE_H - 2 * MARGIN

    # Page 1: header band across the full width, then two columns beneath it.
    # Page 2 (parts continued): the same two columns, no header band.
    head_h = 1.12 * inch
    gutter = 0.28 * inch
    col_w = (usable_w - gutter) / 2.0
    col_h = usable_h - head_h

    f_head = Frame(MARGIN, MARGIN + col_h, usable_w, head_h, id="head",
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f_l = Frame(MARGIN, MARGIN, col_w, col_h, id="l",
                leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    f_r = Frame(MARGIN + col_w + gutter, MARGIN, col_w, col_h, id="r",
                leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)
    f_l2 = Frame(MARGIN, MARGIN, col_w, usable_h, id="l2",
                 leftPadding=0, rightPadding=6, topPadding=0, bottomPadding=0)
    f_r2 = Frame(MARGIN + col_w + gutter, MARGIN, col_w, usable_h, id="r2",
                 leftPadding=6, rightPadding=0, topPadding=0, bottomPadding=0)
    f_full = Frame(MARGIN, MARGIN, usable_w, usable_h, id="full",
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id="Parts", frames=[f_head, f_l, f_r], onPage=on_parts),
        PageTemplate(id="PartsCont", frames=[f_l2, f_r2], onPage=on_parts),
        PageTemplate(id="Steps", frames=[f_full], onPage=on_steps),
    ])

    doc.build(story())
    print("wrote", os.path.relpath(os.path.abspath(OUT), os.getcwd()))


# --------------------------------------------------------------------------
# Content
# --------------------------------------------------------------------------

def story():
    s = []

    # ---- Page 1 header band ------------------------------------------------
    s.append(P("CLOWN", "title"))
    s.append(P("Bubble-shooting sleeve &mdash; build manual", "subtitle"))
    s.append(P(
        "Squeeze your fingers into your palm and a comet of light runs from your elbow "
        "to your fingertips, arriving exactly as bubbles start firing out of your hand. "
        "<b>Two arms, two identical rigs, one trigger per hand.</b><br/><br/>"
        "Every part is numbered; the assembly steps refer back to those numbers in "
        "<b><font color=\"#C2185B\">[brackets]</font></b>. Each part carries "
        "<b>two</b> quantities &mdash; <b>per arm</b>, and what to actually "
        "<b>buy</b> for the whole costume. They are different numbers. Confusing them is "
        "how people end up halfway through a build with one glove.",
        "lede"))

    s.append(NextPageTemplate("PartsCont"))

    # ---- Order-first callout, top of the left column -----------------------
    s.append(callout(
        "Order this first",
        "<b>Two bubble kits %s</b> &mdash; one blower per hand, and each kit brings a "
        "protected cell %s and a charger.<br/>"
        "<b>Two bottles %s</b> &mdash; 24T/30T neck. <i>Not included in the kit.</i><br/>"
        "<b>A pair of gloves %s and a pair of sleeves %s</b> &mdash; test the fabric in a "
        "dark room before you commit to either.<br/>"
        "<b>Two of every electronic part.</b> The arms are independent; nothing is shared."
        % (ref(1), ref(12), ref(2), ref(6), ref(7))))
    s.append(Spacer(1, 4))

    # ---- Page 1-2 columns --------------------------------------------------
    for cat, items in PARTS:
        block = [P(cat, "cat")]
        for num, name, per, buy, note in items:
            if per == "&mdash;":
                qty = "buy %s" % buy
            else:
                qty = "%s per arm &middot; buy %s" % (per, buy)
            block.append(P("%s. %s <font color=\"#5A5A5A\">&mdash; %s</font>"
                           % (num, name, qty), "part"))
            block.append(P(note, "eli5"))
        s.append(KeepTogether(block))

    s.append(Spacer(1, 6))
    s.append(callout(
        "The one mistake that costs a board",
        "<b>The trigger pigtail %s must not be PH2.0.</b> Every cell %s ships on a PH2.0 "
        "lead, so an identical trigger plug is one wrong connection away from putting 3.7V "
        "onto GPIO3.<br/><br/>"
        "<b>And rework the kit's motor lead %s off PH2.0 to SM 2-pin %s.</b> As shipped, the "
        "cell mates straight to the motor &mdash; bypassing the MOSFET %s, so the trigger "
        "does nothing and the blower simply runs."
        % (ref(23), ref(12), ref(1), ref(22), ref(10))))

    s.append(NextPageTemplate("Steps"))
    s.append(PageBreak())

    # ---- Assembly ----------------------------------------------------------
    s.append(P("Assembly", "h1"))
    s.append(P(
        "Read this whole manual once before picking up the soldering iron %s. Several "
        "steps are much easier if you know what is coming &mdash; notably that heat-shrink "
        "%s goes on <i>before</i> you solder, and that you bench-test everything "
        "<i>before</i> anything goes inside a glove %s."
        % (ref(32), ref(26), ref(6)), "body"))
    s.append(P("Budget a full afternoon for the first arm. The second takes about half "
               "as long, because by then you know what you are doing.", "body"))

    s.append(P("What you are building", "h2"))
    s.append(P("<b>Two arms.</b> Each arm is four modules that unplug from each other. "
               "Nothing is soldered end to end across a joint &mdash; that is what lets you "
               "get out of the costume alone, with soapy hands.", "body"))
    s.append(grid([
        ["Module", "Holds", "Unplugs at"],
        ["<b>Pod</b> &mdash; upper arm",
         "brain %s, boost %s, level shifter %s, MOSFET %s, fuse %s, sled %s"
         % (ref(8), ref(14), ref(9), ref(10), ref(15), ref(13)),
         "battery plug + straps"],
        ["<b>Sleeve</b> &mdash; forearm", "forearm strip %s, 15 px" % ref(5),
         "elbow: SM 6-pin %s + SM 2-pin %s" % (ref(20), ref(22))],
        ["<b>Glove</b> &mdash; hand",
         "hand strip 6 px, this hand's trigger %s" % ref(19),
         "wrist: SM 5-pin %s" % ref(21)],
        ["<b>Bubbler</b>", "bottle %s, cap, hose, blower head" % ref(2),
         "wrist: SM 2-pin %s + its strap" % ref(22)],
    ], [1.30 * inch, 3.55 * inch, 1.55 * inch]))
    s.append(P("<b>Steps 1&ndash;10 build one arm. Step 11 is the second arm. Step 12 is the "
               "costume</b> &mdash; the two arms together, and how you get in and out of it.",
               "body"))

    s.append(callout(
        "Safety, briefly but seriously",
        "The cell %s is lithium. Never short its terminals, never charge a puffy or "
        "damaged cell, and do not leave it charging unattended. "
        "<b>Check polarity with the multimeter %s before you connect the battery the "
        "first time</b> &mdash; reversed power destroys the brain %s and the strip %s "
        "instantly and permanently.<br/><br/>"
        "Solder somewhere ventilated. The fumes are flux, not lead &mdash; unpleasant "
        "whichever solder %s you bought."
        % (ref(12), ref(31), ref(8), ref(5), ref(32))))

    s.append(callout(
        "The connector rule you will use constantly",
        "<b>Battery out before you mate or unmate anything.</b> Feeding data into an "
        "unpowered WS2812 strip %s pushes current through its input protection diodes, "
        "which is the classic way to kill pixel 0 &mdash; and that is exactly what happens "
        "if you plug the glove in while the pod is live. Unplug the cell %s first, every "
        "time. It takes one second and becomes automatic quickly." % (ref(5), ref(12))))

    # Step 1
    s.append(P("Step 1 &mdash; Measure your arm", "h2"))
    s.append(P("Put on the glove %s and sleeve %s and hold your arm out in the finger-gun "
               "pose. Measure and write down:" % (ref(6), ref(7)), "body"))
    s += bullets([
        "<b>Elbow to wrist crease</b> &mdash; typically about 25 cm.",
        "<b>Wrist crease to knuckles</b>, across the back of the hand &mdash; about 10 cm.",
        "<b>Where your middle and ring finger pads land</b> on your palm when you squeeze. "
        "That is where the trigger %s goes. Mark it with a fabric pen %s." % (ref(19), ref(30)),
    ])
    s.append(P("Convert the first two into pixel counts. At 60 LED/m each pixel on the "
               "strip %s is <b>1.67 cm</b>:" % ref(5), "body"))
    s.append(P("forearm pixels = forearm cm / 1.67<br/>"
               "hand pixels&nbsp;&nbsp;&nbsp; = hand cm / 1.67", "code"))
    s.append(P("That is usually about <b>15</b> forearm pixels and <b>6</b> hand pixels. "
               "Round down. <b>Then subtract about 4 cm from the forearm figure</b> &mdash; "
               "the wrist umbilical and its connector %s need to live in the last few "
               "centimetres of forearm, just above the crease where the skin barely flexes."
               % ref(21), "body"))

    # Step 2
    s.append(P("Step 2 &mdash; Cut the strip", "h2"))
    s.append(P("The strip %s has marked cut lines between every pixel, with copper pads "
               "either side. <b>Cut through the middle of the pads</b>, not beside them "
               "&mdash; you need pad left on both pieces to solder to. Cut two pieces to "
               "the pixel counts from Step 1." % ref(5), "body"))
    s.append(callout(
        "Check the arrows before you cut",
        "The strip has small printed arrows showing which way data flows. Data must run "
        "<b>elbow to fingertips</b>, so both pieces need their arrows pointing the same "
        "way, toward your fingers. Getting this backwards is the most common build "
        "mistake and the fix is unsoldering everything. Mark the elbow end with tape "
        "&mdash; that end is pixel 0."))
    s.append(P("<b>Why two pieces?</b> Your wrist bends constantly, and a single "
               "continuous strip across that joint cracks its internal copper traces "
               "within hours of wear. Everything past the crack then goes dark. The "
               "flexible umbilical in Step 3 absorbs that movement instead.", "body"))

    # Step 3
    s.append(P("Step 3 &mdash; Build the wrist umbilical", "h2"))
    s.append(P("This is the plug that lets the glove %s come off on its own. It carries "
               "<b>five conductors</b>: the strip's 5V, ground and data, plus this hand's "
               "two trigger wires. Use a <b>JST-SM 5-pin pigtail pair</b> %s. Decide the "
               "pin convention now and keep it identical on both arms."
               % (ref(6), ref(21)), "body"))
    s.append(grid([
        ["SM-5 pin", "Carries"],
        ["1", "Strip 5V"],
        ["2", "Strip GND"],
        ["3", "Strip data"],
        ["4", "Trigger"],
        ["5", "Trigger return (to ground at the pod)"],
    ], [0.85 * inch, 6.35 * inch]))
    s.append(P("<b>Sleeve side</b>", "body"))
    s += bullets([
        "Slide heat-shrink %s onto every wire <b>now</b>, before soldering." % ref(26),
        "Solder short silicone leads %s to the forearm piece's <b>output</b> end &mdash; "
        "5V, GND and <b>DO</b> &mdash; then on to pins 1-3 of one pigtail half." % ref(25),
        "Pins 4-5 get two thin wires long enough to run all the way <b>up the forearm to "
        "the elbow</b>. They are the trigger's path to the pod.",
        "Shrink everything down, then seal the exposed strip end with hot glue %s or clear "
        "silicone. That is the soap-proofing." % ref(28),
    ])
    s.append(P("<b>Glove side</b>", "body"))
    s += bullets([
        "Solder pins 1-3 of the other half to the hand piece's <b>input</b> end: 5V to 5V, "
        "GND to GND, pin 3 to <b>DI</b>.",
        "Pins 4-5 get two wires long enough to reach the palm, ending in the <b>female half "
        "of a JST-ZH 2-pin</b> %s. That is where the microswitch plugs in at Step 5." % ref(23),
        "Shrink, and seal the strip end the same way.",
    ])
    s.append(callout(
        "Where the connector sits, and why",
        "<b>Mate the pair 3-4 cm above the wrist crease</b>, on the forearm. That skin barely "
        "moves; the crease itself is the worst possible place for a rigid 20 mm plastic body. "
        "The glove-side wire is the flex element &mdash; leave a <b>service loop</b> so it is "
        "never under tension at full extension.<br/><br/>"
        "<b>Keep the whole umbilical short.</b> Every centimetre between the last forearm "
        "pixel and the first hand pixel is dark arm the comet has to cross. Around 8 cm is "
        "fine; 15 cm reads as a gap. <b>Measure the finished pixel-to-pixel distance and "
        "write it down</b> &mdash; it becomes GAP_PX in Step 8."))

    # Step 4
    s.append(P("Step 4 &mdash; Build the controller pod", "h2"))
    s.append(P("This all lives on a small piece of protoboard %s that sits on your "
               "<b>upper arm</b>, above the soap spray." % ref(27), "body"))
    s.append(grid([
        ["From", "To", "Notes"],
        ["Battery %s + (PH2.0)" % ref(12), "Polyfuse %s, then everything else" % ref(15),
         "Fuse goes first, right at the cell"],
        ["Battery %s &minus; (PH2.0)" % ref(12), "Common ground", "Everything shares this"],
        ["Battery + (after fuse)", "Boost %s IN+" % ref(14), ""],
        ["Boost %s OUT+ (5V)" % ref(14),
         "XIAO %s 5V pad, 74AHCT125 %s Vcc, elbow SM-6 %s pin 1"
         % (ref(8), ref(9), ref(20)), ""],
        ["Battery + (after fuse)", "Motor +, via elbow SM-2 %s" % ref(22),
         "Motor runs <b>direct from the cell</b>, not from 5V"],
        ["Motor &minus; (via elbow SM-2)", "MOSFET %s output" % ref(10), ""],
        ["XIAO D2 (GPIO4)", "74AHCT125 %s <b>second</b> gate input" % ref(9),
         "Gate drive &mdash; see below"],
        ["74AHCT125 %s second gate out" % ref(9),
         "100 ohm, then MOSFET %s gate" % ref(10),
         "Plus a 10k gate-to-source pulldown"],
        ["XIAO D10 (GPIO10)", "74AHCT125 %s input" % ref(9), ""],
        ["74AHCT125 %s output" % ref(9),
         "Resistor %s, then elbow SM-6 pin 3" % ref(18),
         "Resistor at the connector end"],
        ["XIAO D1 (GPIO3)", "Elbow SM-6 pin 4", "Trigger, arriving from the hand"],
        ["Elbow SM-6 pin 5", "Common ground", "Trigger return"],
        ["XIAO D0 (GPIO2)", "Midpoint of the two 100k resistors %s" % ref(16),
         "Battery monitor"],
    ], [1.55 * inch, 3.05 * inch, 1.80 * inch]))

    s.append(callout(
        "Drive the MOSFET gate at 5V, not 3.3V",
        "The XIAO %s swings its outputs to <b>3.3V</b>. Most \"logic-level\" MOSFETs are "
        "specified fully on at <b>Vgs = 5V</b> &mdash; at 3.3V they only partly open, "
        "dissipate the difference as heat, and the blower runs slow and inconsistent."
        "<br/><br/>"
        "<b>The 74AHCT125 %s has four gates and the strip only uses one.</b> Route D2 "
        "through a second gate, exactly as you route the LED data through the first. Add a "
        "<b>100 ohm</b> resistor in series with the gate and a <b>10k</b> pulldown from gate "
        "to source, so the FET is held off while the board boots. It costs nothing &mdash; "
        "the chip is already in the pod.<br/><br/>"
        "<b>Do not use an IRF520 module.</b> It is the top search result for \"Arduino "
        "MOSFET module\" and it is not logic-level: its gate threshold runs to 4V and it "
        "wants ~10V to open properly. It half-works, which is harder to diagnose than not "
        "working at all." % (ref(8), ref(9))))

    s.append(P("The pod's two outward plugs", "h2"))
    s.append(P("Everything the pod sends down the arm leaves through exactly two "
               "connectors:", "body"))
    s.append(grid([
        ["Plug", "Pins"],
        ["<b>SM 6-pin</b> %s" % ref(20),
         "1 strip 5V &middot; 2 strip GND &middot; 3 strip data &middot; 4 trigger "
         "&middot; 5 trigger return &middot; <b>6 second ground</b>"],
        ["<b>SM 2-pin</b> %s" % ref(22),
         "1 motor + (battery, after fuse) &middot; 2 motor &minus; (MOSFET output)"],
    ], [1.35 * inch, 5.85 * inch]))
    s += bullets([
        "<b>Pin 6 is not spare, it is a job.</b> The elbow run is the longest in the "
        "costume and carries the whole strip's current. A second ground conductor cuts the "
        "voltage drop and gives the data line a better return path. Tie it to common ground "
        "at both ends.",
        "<b>The motor gets its own plug on purpose.</b> Roughly an amp of switched PWM "
        "bundled against a WS2812 data line is asking for flicker. Twist the motor pair.",
    ])

    s.append(P("The battery monitor divider", "h2"))
    sp = "&nbsp;"
    s.append(P("Battery + (after fuse) &mdash;[100k]&mdash;+&mdash;[100k]&mdash; Ground<br/>"
               + sp * 31 + "|<br/>"
               + sp * 28 + "XIAO D0", "code"))
    s.append(P("The midpoint sits at exactly half the cell voltage, which is safely "
               "inside what the brain %s can measure." % ref(8), "body"))

    s.append(P("Also fit", "h2"))
    s += bullets([
        "The <b>1000 uF capacitor</b> %s across the strip's 5V and ground, physically "
        "close to the elbow connector. Watch polarity &mdash; the striped leg is negative."
        % ref(17),
        "The <b>1N5819 diode</b> %s directly across the motor's two terminals at the blower "
        "end, banded end to <b>positive</b>. Backwards it is a dead short, so check this one "
        "twice." % ref(11),
    ])

    s.append(callout(
        "Keep the cell on its factory plug",
        "The 18650 %s arrives on a <b>PH2.0 pigtail</b>, and the kit's USB charger mates to "
        "the same connector. Fit the matching half at the pod and you get a clean swap: pull "
        "the flat cell, plug it straight into the charger, plug a fresh one in. No adapters, "
        "no rework.<br/><br/>"
        "<b>PH2.0 must be the only PH connector in the whole build.</b> See Step 5."
        % ref(12)))

    s.append(callout(
        "Three rules that matter",
        "<b>1.</b> Everything shares <b>one common ground</b> &mdash; brain %s, strip %s, "
        "level shifter %s, MOSFET %s, boost %s and cell %s. Skipping this causes bizarre, "
        "hard-to-diagnose behaviour.<br/>"
        "<b>2.</b> <b>Do not use D8 or D9</b> (GPIO8/GPIO9) for anything. They are boot "
        "pins and the board will not start reliably.<br/>"
        "<b>3.</b> <b>Leave the USB-C port reachable</b> when you design the printed pod, "
        "and use a <b>data-capable</b> cable %s. You will reflash this far more often than "
        "you expect."
        % (ref(8), ref(5), ref(9), ref(10), ref(14), ref(12), ref(34))))

    # Step 5
    s.append(P("Step 5 &mdash; Wire this hand's trigger", "h2"))
    s.append(P("<b>Each hand has its own trigger, firing its own arm.</b> Nothing crosses "
               "the torso. You are wiring one of two identical, independent triggers.", "body"))
    s += bullets([
        "Solder two lengths of thin silicone wire %s to the microswitch's <b>COM</b> and "
        "<b>NO</b> (normally open) terminals." % ref(25),
        "Terminate them in the <b>male half of a JST-ZH 2-pin</b> %s &mdash; the mate to the "
        "one you left on the glove side of the umbilical in Step 3." % ref(23),
        "Mount the switch %s on a small printed plate %s, positioned so the <b>lever</b> "
        "sits under your middle and ring finger pads at the spot you marked in Step 1."
        % (ref(19), ref(35)),
    ])
    s.append(P("Orient the lever so a natural squeeze presses across its length. You "
               "should be able to fire it with your eyes closed, in one motion, every "
               "time. If you catch yourself aiming, reposition the plate until you "
               "do not.", "body"))
    s.append(P("<b>Why the switch gets its own tiny plug:</b> the field kit carries a spare "
               "microswitch. Without this pigtail, \"spare\" means \"spare, if you also "
               "brought a soldering iron.\" With it, swapping a dead trigger mid-event is a "
               "ten-second job.", "body"))
    s.append(callout(
        "Why ZH and not PH",
        "<b>The trigger pigtail must not be PH2.0.</b> Every cell %s in this build ships on "
        "a PH2.0 lead. If the trigger used the same connector, one wrong plug in a dark room "
        "puts <b>3.7V directly onto GPIO3</b> &mdash; a dead pin, quite possibly a dead "
        "XIAO %s.<br/><br/>"
        "JST-ZH %s is 1.5 mm pitch; PH is 2.0 mm. They physically will not mate. That "
        "incompatibility is the entire reason for the choice &mdash; do not \"simplify\" it "
        "later by standardising on one connector." % (ref(12), ref(8), ref(23))))

    # Step 6
    s.append(P("Step 6 &mdash; Bench test, before anything goes in the glove", "h2"))
    s.append(callout(
        "Do not skip this step",
        "Sewing everything into a glove %s and <i>then</i> discovering a reversed data "
        "arrow is genuinely miserable. Test it flat on the table first, with every "
        "connector mated." % ref(6)))
    s += bullets([
        "<b>Check polarity with the multimeter</b> %s. Battery + and &minus; where you "
        "expect; boost %s output close to 5.0V. Only then connect the brain %s."
        % (ref(31), ref(14), ref(8)),
        "<b>Beep through every connector, pin by pin.</b> A pigtail with a crimp that did "
        "not seat looks perfect and works intermittently. Find it now, not at the venue.",
        "Power up. You should get the dim breathing idle glow.",
        "Press the microswitch %s by hand. The comet should launch from the <b>elbow</b> "
        "end and travel to the <b>fingertip</b> end, and the motor should spin." % ref(19),
        "If the comet runs backwards, the strip pieces are reversed. <b>Fix it in the "
        "wiring, not in the code</b> &mdash; both arms run identical firmware and that "
        "is worth a resolder.",
        "Let it run five minutes, then check for heat.",
    ])
    s.append(callout(
        "Checking for heat",
        "Touch the boost %s and MOSFET %s. Warm is fine; too hot to touch means power down "
        "and look for a short.<br/><br/>"
        "<b>If you can borrow a thermal camera %s, use it here instead.</b> It turns this "
        "from a fingertip guess into a measurement, and shows you what a fingertip misses: a "
        "boost running hot because something downstream is shorted, a MOSFET that turned out "
        "not to be logic-level and is dissipating the difference, or a strip section drawing "
        "more than its neighbours. One borrowed session is plenty."
        % (ref(14), ref(10), ref(33))))

    # Step 7
    s.append(P("Step 7 &mdash; Fit the bubbler", "h2"))
    s.append(P("<b>First, understand what you actually have.</b> The kit %s is not one "
               "object &mdash; it is a bottle %s, a cap with a one-way valve, and a blower "
               "head, joined by silicone hose:" % (ref(1), ref(2)), "body"))
    s += bullets([
        "<b>~50 mm of hose inside the bottle</b>, ending in the blue <b>gravity ball</b>. "
        "The ball sinks, so the pickup stays in solution at any arm angle &mdash; even "
        "inverted.",
        "<b>~50-70 mm of hose outside the cap</b>, feeding the blower head.",
    ])
    s.append(P("So the heavy thing (the bottle) and the thing that must point past your "
               "fingertips (the blower head) <b>do not have to be in the same place.</b> "
               "That opens up a much better mount &mdash; if the blower can pull solution "
               "far enough.", "body"))
    s.append(callout(
        "The hose test &mdash; do this before you commit to a mount",
        "Twenty minutes, one length of 3 x 5 mm silicone tube %s, and it decides the whole "
        "mount design. Do it the day the kit arrives, before any of the soldering above."
        "<br/><br/>"
        "<b>1.</b> Assemble the kit as supplied and confirm it makes bubbles.<br/>"
        "<b>2.</b> Replace the <i>outside</i> hose with about <b>150 mm</b> of 3 x 5 tube."
        "<br/>"
        "<b>3.</b> Run it again, held roughly the way your arm will hold it.<br/><br/>"
        "<b>Does it still make bubbles at the same rate?</b>" % ref(3)))
    s.append(grid([
        ["If it PASSES &mdash; Mount C", "If it FAILS &mdash; Mount A"],
        ["<b>Bottle on the forearm</b>, blower head at the knuckles pointing past your "
         "fingertips.<br/><br/>Bubbles still appear to come from your fingers, so the comet "
         "illusion is intact &mdash; and the heaviest item on the arm moves off the end of "
         "the lever, where it was costing you most.<br/><br/><b>This is the better build if "
         "you can get it.</b>",
         "<b>Bottle and blower head both on the back of the hand</b>, exactly as the kit "
         "intends, nozzle past the fingertips. Works as shipped, no modification, no "
         "risk.<br/><br/>Manage the weight instead: <b>run the bottle half-full</b> (you "
         "carry refills anyway); mount the bottle body back toward the wrist with the cap "
         "forward, to shorten the lever arm; and anchor to a <b>wrist strap</b>, not glove "
         "fabric &mdash; a glove will not hold 200 g swinging for an evening."],
    ], [3.60 * inch, 3.60 * inch]))
    s.append(P("<b>Either way</b>", "body"))
    s += bullets([
        "Check MakerWorld for existing mounts from the kit's collection as a starting point. "
        "Community CAD for the cap thread and the blower sleeve already exists.",
        "<b>The bubbler is its own module.</b> Give it a quick-release strap, and make sure "
        "nothing about its mount bridges the wrist &mdash; a rigid bottle spanning that joint "
        "means the glove %s cannot come off without removing the bottle first." % ref(6),
        "<b>Rework the motor lead.</b> The kit ships the motor on a <b>PH2.0 female</b> plug "
        "that mates straight to the cell %s. Cut it off and fit a <b>JST-SM 2-pin</b> %s. "
        "This is not cosmetic: leave it and the cell can power the motor directly, bypassing "
        "the MOSFET %s, and the trigger does nothing." % (ref(12), ref(22), ref(10)),
        "Use silicone wire %s for the motor run; it flexes constantly." % ref(25),
        "A longer hose holds more solution, so dribble on shutdown gets slightly worse. The "
        "silicone sleeve over the cap's protrusion &mdash; the one-way valve &mdash; is what "
        "stops it emptying into your bag.",
    ])

    # Step 8
    s.append(P("Step 8 &mdash; Flash the firmware", "h2"))
    s += bullets([
        "Install the Arduino IDE, then add ESP32 board support (Boards Manager, search "
        "<font face=\"Courier\">esp32</font>, install the Espressif package).",
        "Install the <b>FastLED</b> library from the Library Manager.",
        "Select board <font face=\"Courier\">XIAO_ESP32C3</font>.",
        "Open <font face=\"Courier\">firmware/clown_arm/clown_arm.ino</font>.",
        "<b>Edit the layout constants</b> at the top to match your measurements.",
        "Plug in USB-C %s and upload. If it fails, hold BOOT while plugging the cable in."
        % ref(34),
    ])
    s.append(P("constexpr int FOREARM_PX = 15;&nbsp;&nbsp; // your forearm pixel count<br/>"
               "constexpr int HAND_PX&nbsp;&nbsp;&nbsp; = 6;&nbsp;&nbsp;&nbsp; // your hand pixel count<br/>"
               "constexpr int GAP_PX&nbsp;&nbsp;&nbsp;&nbsp; = 5;&nbsp;&nbsp;&nbsp; // umbilical length / 1.67 cm", "code"))
    s.append(P("<b>GAP_PX is the measured pixel-to-pixel distance across the umbilical</b>, "
               "from the last forearm pixel to the first hand pixel, divided by 1.67 cm. "
               "Measure the finished assembly from Step 3 &mdash; <i>including the connector "
               "body</i> %s, which is most of it. About 8 cm gives GAP_PX = 5. Guessing here "
               "is what makes the comet look like it stumbles at the wrist." % ref(21),
               "body"))
    s.append(P("<b>Flash the identical sketch to both arms.</b> There is deliberately no "
               "left/right setting &mdash; as long as pixel 0 is at the elbow on each "
               "arm, the mirroring is physical only.", "body"))

    # Step 9
    s.append(P("Step 9 &mdash; Tune the timing", "h2"))
    s.append(P("This is the step that makes the whole effect work, and it can only be "
               "done on the finished arm. The goal: <b>the comet reaches your fingertips "
               "at the exact moment the first bubble appears.</b> When it is right, the "
               "light looks like it is <i>causing</i> the bubbles. Wrong by even 100 ms "
               "and it just looks like lag.", "body"))
    s += bullets([
        "Film yourself firing it in slow motion &mdash; any modern phone does 120 or 240 fps.",
        "Watch it back frame by frame. Does the comet arrive early or late?",
        "Adjust <font face=\"Courier\">COMET_TRAVEL_MS</font>: comet arrives <b>before</b> "
        "the bubbles, increase it; <b>after</b> the bubbles, decrease it.",
        "Reflash and film again. Expect three or four rounds.",
    ])
    s.append(P("The default is 250 ms. Your real number depends on how fast your "
               "particular blower %s spins up, which is why it is guesswork until you "
               "measure it. <b>If you built Mount C, expect a slightly longer number</b> "
               "&mdash; a 150 mm feed hose takes marginally longer to prime than a 60 mm "
               "one, and that delay lands between the trigger and the first bubble."
               % ref(1), "body"))

    # Step 10
    s.append(P("Step 10 &mdash; Mount into the glove and sleeve", "h2"))
    s.append(P("Hiding the strip %s under fabric is an upgrade, not a compromise &mdash; "
               "the fabric diffuses the pixels into one smooth continuous streak instead "
               "of visible dots. But it only works if the fabric cooperates." % ref(5),
               "body"))
    s.append(callout(
        "Test the fabric before you commit",
        "Hold a powered section of strip %s under the glove %s in a dark room. Thin, pale, "
        "stretchy fabric glows beautifully; thick or dark fabric, especially leather, "
        "swallows almost all of it. If you cannot see it clearly, no firmware setting "
        "will rescue it &mdash; get a different glove. <b>Test the sleeve %s at the same "
        "time</b>; there is no point in a glove that glows over a sleeve that does not."
        % (ref(5), ref(6), ref(7))))
    s += bullets([
        "Run the strip across the <b>back of the hand</b>, over the knuckles. Never the "
        "palm &mdash; that is where the trigger %s is and where you grip things." % ref(19),
        "Stop short of the fingertips. The blower head needs that space, and finger "
        "joints flex too much for strip to survive.",
        "Sew a <b>fabric channel</b> %s for the strip to sit in rather than gluing it down "
        "flat. The channel lets it slide as your hand flexes; glued-taut strip tears "
        "itself off, or tears the glove." % ref(29),
        "<font face=\"Courier\">MAX_BRIGHTNESS</font> is preset high to punch through "
        "fabric. You can raise it further for thicker gloves, but current draw climbs "
        "with it and battery life drops.",
    ])
    s.append(callout(
        "Connectors and strain relief",
        "<b>The connector is never the anchor.</b> Tack the cable to the garment on "
        "<i>both</i> sides of every plug, so a snag pulls the tack rather than the latch. "
        "Leave a <b>service loop</b> either side.<br/><br/>"
        "A smear of <b>dielectric grease</b> %s in each shell keeps soap residue from "
        "corroding the contacts over a season. And position the mated plugs where a tight "
        "sleeve will not press them into your skin &mdash; a 20 mm plastic body under a cuff "
        "for six hours is uncomfortable." % ref(24)))

    # Step 11
    s.append(P("Step 11 &mdash; Build the second arm", "h2"))
    s.append(P("Repeat Steps 1 to 10. Two things to be careful about:", "body"))
    s += bullets([
        "<b>Pixel 0 goes at the elbow on this arm too.</b> It is tempting to mirror the "
        "wiring along with the physical build. Do not. Identical wiring means identical "
        "firmware means one thing to maintain.",
        "<b>Keep the same SM-5 %s and SM-6 %s pin conventions.</b> If arm A puts the trigger "
        "on pins 4-5 and arm B puts it on pins 1-2, then spares are not spares, and one "
        "wrong plug at an event costs you a board. Write the pinout on a bit of tape inside "
        "each pod." % (ref(21), ref(20)),
    ])

    # Step 12
    s.append(PageBreak())
    s.append(P("Step 12 &mdash; Assemble the costume", "h1"))
    s.append(P("Both arms exist. This step is about the thing you actually wear.", "body"))

    s.append(P("Both-arms checkout", "h2"))
    s += bullets([
        "<b>Cells %s out of both pods.</b>" % ref(12),
        "Mate every connector on both arms. Count them: <b>four per arm</b> &mdash; elbow "
        "SM-6 %s, elbow SM-2 %s, wrist SM-5 %s, wrist SM-2 %s &mdash; plus the ZH-2 %s at "
        "each microswitch." % (ref(20), ref(22), ref(21), ref(22), ref(23)),
        "Cells in. Both arms should show the idle glow.",
        "<b>Fire each hand separately.</b> Left trigger drives the left arm only; right "
        "drives right only. If one trigger fires the other arm, you have crossed something "
        "&mdash; there is no cross-arm wiring in this design.",
        "Fire both at once. Watch for either arm dimming or glitching. They are electrically "
        "independent and should not interact at all; if they do, suspect a shared ground you "
        "did not intend.",
        "Run both for the length of a bottle of solution %s. That is your real duty cycle."
        % ref(4),
    ])

    s.append(grid([
        ["Getting into it &mdash; cells go in LAST", "Getting out of it &mdash; cells come out FIRST"],
        ["<b>1.</b> Pods on the upper arms, strapped, cells <b>out</b>.<br/>"
         "<b>2.</b> Sleeves on. Mate elbow SM-6 and SM-2 each side.<br/>"
         "<b>3.</b> Gloves on. Mate wrist SM-5 each side.<br/>"
         "<b>4.</b> Bubblers strapped on, mate wrist SM-2, bottles filled.<br/>"
         "<b>5. Cells in.</b> Check both idle glows before you walk out.",
         "<b>1. Cells out.</b> Both arms are now dead and safe to unplug.<br/>"
         "<b>2.</b> Wrist SM-2 + bubbler strap &rarr; bubblers off, bottles upright.<br/>"
         "<b>3.</b> Wrist SM-5 &rarr; gloves peel off.<br/>"
         "<b>4.</b> Elbow SM-6 + SM-2 &rarr; sleeves come off.<br/>"
         "<b>5.</b> Pod straps.<br/><br/>"
         "Four releases per arm, none needing a second person or a flat surface."],
    ], [3.60 * inch, 3.60 * inch]))

    s.append(callout(
        "The test that matters",
        "<b>Can you get out of it alone, in a bathroom, with soapy hands, in under a "
        "minute?</b><br/><br/>"
        "If not, something is still soldered that should not be, or a strap is fighting a "
        "connector. Fix it before the event, not at it."))

    s.append(P("Care afterwards", "h2"))
    s += bullets([
        "<b>Cells out for storage.</b> Never store the costume with cells connected.",
        "Rinse the blower head and cap in warm water &mdash; dried bubble solution glues the "
        "one-way valve shut.",
        "Leave the silicone sleeve on the cap protrusion so the bottle does not empty into "
        "your bag.",
        "Wipe soap residue off any connector that got sprayed, and re-grease it %s." % ref(24),
    ])

    # Troubleshooting
    s.append(PageBreak())
    s.append(P("Troubleshooting", "h1"))
    s.append(grid([
        ["Symptom", "Likely cause"],
        ["Nothing lights at all",
         "Check common ground. Check boost %s output is about 5V. Check strip DIN is on "
         "the <i>input</i> end &mdash; follow the arrows." % ref(14)],
        ["Nothing lights, and it worked yesterday",
         "Check every connector is fully latched. A half-seated SM plug looks mated."],
        ["Works until you move your arm",
         "Unseated connector, or a crimp that did not take. Beep through each pin while "
         "wiggling the cable."],
        ["First pixel wrong colour, rest fine",
         "Missing or wrong-value data resistor %s." % ref(18)],
        ["Pixel 0 died after a reconnect",
         "Strip was plugged in live. <b>Cell %s out before mating</b>, every time." % ref(12)],
        ["Random flickering, especially when moving",
         "Missing level shifter %s, or a loose ground. Check SM-6 %s pin 6 is actually tied "
         "to ground at both ends." % (ref(9), ref(20))],
        ["Comet runs fingertips to elbow",
         "Strip %s is reversed. Fix the wiring, not the code." % ref(5)],
        ["Comet jumps or stalls at the wrist",
         "<font face=\"Courier\">GAP_PX</font> does not match your measured umbilical length."],
        ["Colours wrong, red and green swapped",
         "Change <font face=\"Courier\">GRB</font> to <font face=\"Courier\">RGB</font> in "
         "the <font face=\"Courier\">addLeds</font> line."],
        ["Motor whines audibly",
         "PWM frequency dropped below 20 kHz &mdash; check "
         "<font face=\"Courier\">MOTOR_PWM_HZ</font>."],
        ["Motor does not spin",
         "MOSFET %s gate not driven, or it is not a logic-level part." % ref(10)],
        ["Motor spins weakly, MOSFET gets hot",
         "Gate driven at 3.3V instead of through the 74AHCT125 %s &mdash; or it is an "
         "IRF520, which is not logic-level." % ref(9)],
        ["Motor runs constantly, trigger does nothing",
         "Motor still on its factory PH2.0 lead, plugged straight to the cell. Rework it to "
         "SM-2 %s &mdash; Step 7." % ref(22)],
        ["Everything dies when the motor starts",
         "Cell %s sagging, or the polyfuse %s tripping. Check the charge."
         % (ref(12), ref(15))],
        ["Works, then dies after a few minutes",
         "Cell %s protection circuit cutting out. Recharge or swap." % ref(12)],
        ["Elbow pixel pulsing red",
         "Low-battery warning. Swap the cell %s." % ref(12)],
        ["One trigger fires the other arm",
         "Not possible by design &mdash; you have cross-plugged two arms. Check each arm is "
         "self-contained."],
        ["Board will not accept uploads",
         "Hold BOOT while plugging in USB. If the port is not recognised at all, suspect a "
         "charge-only cable %s." % ref(34)],
        ["Strip goes dark past the wrist",
         "Cracked trace or failed umbilical joint &mdash; the failure the umbilical exists "
         "to prevent. Swap in your spare."],
        ["Bubbles weak or intermittent",
         "Gravity ball not sitting in solution, or the feed hose %s is too long. See the "
         "Step 7 hose test." % ref(3)],
        ["Bubbles stop but the motor runs",
         "Bottle %s empty, or dried solution in the one-way valve. Rinse the cap." % ref(2)],
    ], [2.35 * inch, 4.85 * inch]))

    # Customising
    s.append(P("Changing how it behaves", "h2"))
    s.append(P("The whole point of the strip %s is that every pixel takes orders "
               "individually. Everything you would normally want to change lives in one "
               "marked block at the top of the sketch &mdash; edit, reflash over USB-C, "
               "done." % ref(5), "body"))
    s.append(grid([
        ["Constant", "Changes"],
        ["THEME_HUE", "The comet's colour, 0-255 around the colour wheel"],
        ["COMET_TRAVEL_MS", "Comet speed, and its sync with the bubbles"],
        ["COMET_REPEAT_MS", "How rapid-fire the stream is while held"],
        ["COMET_FADE", "Tail length &mdash; higher is shorter"],
        ["MAX_BRIGHTNESS", "Overall brightness, for your glove's fabric"],
        ["IDLE_BRIGHTNESS", "Resting glow. Set to 0 for fully dark when idle"],
        ["MOTOR_RUN_DUTY", "Bubble rate"],
        ["VBAT_WARN_MV", "When the low-cell warning starts"],
    ], [1.75 * inch, 5.45 * inch]))
    s.append(P("The XIAO %s has Wi-Fi and Bluetooth sitting unused, already paid for. "
               "Natural next steps, in rough order of effort: more patterns with a "
               "long-press to cycle them; <b>ESP-NOW</b> so either arm's trigger can "
               "<i>also</i> fire the other for a two-handed blast &mdash; note that is "
               "<b>additive</b>, each hand keeps its own trigger and its own arm; and a "
               "small web page served by the board so you can change colour and speed from "
               "your phone without a laptop." % ref(8), "body"))

    # Field kit
    s.append(P("Field kit", "h2"))
    s.append(P("What to carry when you actually wear this. Everything here now swaps "
               "<b>without a soldering iron</b> &mdash; that is what the connectors bought "
               "you:", "body"))
    s += bullets([
        "A spare charged cell %s per arm, on its PH2.0 pigtail." % ref(12),
        "<b>A pre-made spare wrist umbilical</b> %s &mdash; genuinely swappable now that "
        "both ends are connectors." % ref(21),
        "A spare microswitch %s, already on its ZH-2 pigtail %s." % (ref(19), ref(23)),
        "One spare SM pigtail pair of each size %s %s %s."
        % (ref(20), ref(21), ref(22)),
        "<b>Extra bubble solution</b> %s. This runs out long before the battery does." % ref(4),
        "Spare 3 x 5 silicone tube %s, in case a feed hose splits." % ref(3),
        "A solder pen %s, for repairs you cannot connector your way out of." % ref(32),
        "A small screwdriver and some electrical tape.",
    ])

    return s


if __name__ == "__main__":
    build()

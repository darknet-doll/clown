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
    f_full = Frame(MARGIN, MARGIN, usable_w, usable_h, id="full",
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)

    doc.addPageTemplates([
        PageTemplate(id="Parts", frames=[f_head, f_l, f_r], onPage=on_parts),
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
        "Two arms, two identical rigs.<br/><br/>"
        "<b>This page is every part and what it actually does.</b> Each one is numbered. "
        "The assembly steps from page 2 onwards refer back to those numbers in "
        "<b><font color=\"#C2185B\">[brackets]</font></b>. "
        "<b>All quantities are PER ARM &mdash; you are building two of everything.</b>",
        "lede"))

    # ---- Page 1 columns ----------------------------------------------------
    for cat, items in PARTS:
        block = [P(cat, "cat")]
        for num, name, qty, note in items:
            block.append(P("%s. %s <font color=\"#5A5A5A\">&mdash; %s</font>"
                           % (num, name, qty), "part"))
            block.append(P(note, "eli5"))
        s.append(KeepTogether(block))

    s.append(Spacer(1, 8))
    s.append(callout(
        "Before you order",
        "<b>Buy two bubble kits %s.</b> You need one blower per hand, and each kit "
        "also brings a protected cell %s and a charger &mdash; that covers both arms "
        "without buying batteries separately.<br/><br/><b>Test your glove fabric %s first.</b> Hold a lit strip %s under it in a dark room. "
        "If the glow is weak, change gloves &mdash; no setting in the firmware "
        "rescues fabric that eats the light." % (ref(1), ref(8), ref(3), ref(2))))

    s.append(NextPageTemplate("Steps"))
    s.append(PageBreak())

    # ---- Assembly ----------------------------------------------------------
    s.append(P("Assembly", "h1"))
    s.append(P(
        "Read this whole manual once before picking up the soldering iron [19]. Several "
        "steps are much easier if you know what is coming &mdash; notably that heat-shrink "
        "[17] goes on <i>before</i> you solder, and that you bench-test everything "
        "<i>before</i> anything goes inside a glove [3]."
        .replace("[19]", ref(19)).replace("[17]", ref(17)).replace("[3]", ref(3)),
        "body"))
    s.append(P("Budget a full afternoon for the first arm. The second takes about half "
               "as long, because by then you know what you are doing.", "body"))

    s.append(callout(
        "Safety, briefly but seriously",
        "The cell %s is lithium. Never short its terminals, never charge a puffy or "
        "damaged cell, and do not leave it charging unattended. "
        "<b>Check polarity with the multimeter %s before you connect the battery the "
        "first time</b> &mdash; reversed power destroys the brain %s and the strip %s "
        "instantly and permanently."
        % (ref(8), ref(18), ref(4), ref(2))))

    # Step 1
    s.append(P("Step 1 &mdash; Measure your arm", "h2"))
    s.append(P("Put on the glove %s and hold your arm out in the finger-gun pose. "
               "Measure and write down:" % ref(3), "body"))
    s += bullets([
        "<b>Elbow to wrist crease</b> &mdash; typically about 25 cm.",
        "<b>Wrist crease to knuckles</b>, across the back of the hand &mdash; about 10 cm.",
        "<b>Where your middle and ring finger pads land</b> on your palm when you squeeze. "
        "That is where the trigger %s goes. Mark it with a fabric pen." % ref(15),
    ])
    s.append(P("Convert the first two into pixel counts. At 60 LED/m each pixel on the "
               "strip %s is <b>1.67 cm</b>:" % ref(2), "body"))
    s.append(P("forearm pixels = forearm cm / 1.67<br/>"
               "hand pixels&nbsp;&nbsp;&nbsp; = hand cm / 1.67", "code"))
    s.append(P("That is usually about <b>15</b> forearm pixels and <b>6</b> hand pixels. "
               "Round down &mdash; slightly short is fine, too long does not fit. Keep "
               "these numbers; you type them into the firmware in Step 8.", "body"))

    # Step 2
    s.append(P("Step 2 &mdash; Cut the strip", "h2"))
    s.append(P("The strip %s has marked cut lines between every pixel, with copper pads "
               "either side. <b>Cut through the middle of the pads</b>, not beside them "
               "&mdash; you need pad left on both pieces to solder to. Cut two pieces to "
               "the pixel counts from Step 1." % ref(2), "body"))
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
               "flexible jumper in Step 3 absorbs that movement instead.", "body"))

    # Step 3
    s.append(P("Step 3 &mdash; Solder the wrist jumper", "h2"))
    s.append(P("Join the two strip pieces with about 4 cm of silicone wire %s, three "
               "conductors: 5V, GND and data." % ref(16), "body"))
    s += bullets([
        "Slide heat-shrink %s onto each wire <b>now</b>, before soldering." % ref(17),
        "Peel back a little silicone sleeve at each strip end to expose the pads.",
        "Tin the pads and the wire ends separately, then join them.",
        "Forearm piece <b>output</b> end to hand piece <b>input</b> end: 5V to 5V, "
        "GND to GND, <b>DO to DI</b>.",
        "Shrink the tubing over each joint, then seal the exposed strip ends with hot "
        "glue or clear silicone. That is the soap-proofing.",
    ])
    s.append(P("Make the jumper slightly longer than the gap needs, so there is a small "
               "service loop &mdash; it must never be pulled tight when you fully extend "
               "your wrist. Tug each wire gently to test the joints now, while they are "
               "still reachable.", "body"))

    # Step 4
    s.append(P("Step 4 &mdash; Build the controller pod", "h2"))
    s.append(P("This all lives on a small piece of protoboard that sits on your "
               "<b>upper arm</b>, above the soap spray.", "body"))
    s.append(grid([
        ["From", "To", "Notes"],
        ["Battery %s +" % ref(8), "Polyfuse %s, then everything else" % ref(11),
         "Fuse goes first, right at the cell"],
        ["Battery %s &minus;" % ref(8), "Common ground", "Everything shares this"],
        ["Battery + (after fuse)", "Boost %s IN+" % ref(10), ""],
        ["Boost %s OUT+ (5V)" % ref(10),
         "XIAO %s 5V pad, 74AHCT125 %s Vcc, strip %s 5V" % (ref(4), ref(5), ref(2)), ""],
        ["Battery + (after fuse)", "Motor +",
         "Motor runs <b>direct from the cell</b>, not from 5V"],
        ["Motor &minus;", "MOSFET %s output" % ref(6), ""],
        ["XIAO D2 (GPIO4)", "MOSFET %s gate input" % ref(6), ""],
        ["XIAO D10 (GPIO10)", "74AHCT125 %s input" % ref(5), ""],
        ["74AHCT125 %s output" % ref(5),
         "Resistor %s, then strip DIN" % ref(14), "Resistor close to the strip"],
        ["XIAO D1 (GPIO3)", "Microswitch %s, other side to ground" % ref(15), ""],
        ["XIAO D0 (GPIO2)", "Midpoint of the two 100k resistors %s" % ref(12),
         "Battery monitor"],
    ], [1.45 * inch, 2.75 * inch, 2.20 * inch]))

    s.append(P("The battery monitor divider", "h2"))
    sp = "&nbsp;"
    s.append(P("Battery + (after fuse) &mdash;[100k]&mdash;+&mdash;[100k]&mdash; Ground<br/>"
               + sp * 31 + "|<br/>"
               + sp * 28 + "XIAO D0", "code"))
    s.append(P("The midpoint sits at exactly half the cell voltage, which is safely "
               "inside what the brain %s can measure." % ref(4), "body"))

    s.append(P("Also fit", "h2"))
    s += bullets([
        "The <b>1000 uF capacitor</b> %s across the strip's 5V and ground, physically "
        "close to the strip. Watch polarity &mdash; the striped leg is negative." % ref(13),
        "The <b>1N5819 diode</b> %s directly across the motor's two terminals, banded "
        "end to <b>positive</b>. Backwards it is a dead short, so check this one twice."
        % ref(7),
    ])

    s.append(callout(
        "Three rules that matter",
        "<b>1.</b> Everything shares <b>one common ground</b> &mdash; brain %s, strip %s, "
        "level shifter %s, MOSFET %s, boost %s and cell %s. Skipping this causes bizarre, "
        "hard-to-diagnose behaviour.<br/>"
        "<b>2.</b> <b>Do not use D8 or D9</b> (GPIO8/GPIO9) for anything. They are boot "
        "pins and the board will not start reliably.<br/>"
        "<b>3.</b> <b>Leave the USB-C port reachable</b> when you design the printed pod. "
        "You will reflash this far more often than you expect &mdash; every timing tweak, "
        "every colour change. A cutout in the pod wall is enough."
        % (ref(4), ref(2), ref(5), ref(6), ref(10), ref(8))))

    # Step 5
    s.append(P("Step 5 &mdash; Wire the trigger", "h2"))
    s += bullets([
        "Solder thin silicone wire %s to the microswitch's <b>COM</b> and <b>NO</b> "
        "(normally open) terminals." % ref(16),
        "Run them up the forearm to the pod: one to D1, one to ground.",
        "Mount the switch %s on a small printed plate %s, positioned so the <b>lever</b> "
        "sits under your middle and ring finger pads at the spot you marked in Step 1."
        % (ref(15), ref(20)),
    ])
    s.append(P("Orient the lever so a natural squeeze presses across its length. You "
               "should be able to fire it with your eyes closed, in one motion, every "
               "time. If you catch yourself aiming, reposition the plate until you "
               "do not.", "body"))

    # Step 6
    s.append(P("Step 6 &mdash; Bench test, before anything goes in the glove", "h2"))
    s.append(callout(
        "Do not skip this step",
        "Sewing everything into a glove %s and <i>then</i> discovering a reversed data "
        "arrow is genuinely miserable. Test it flat on the table first." % ref(3)))
    s += bullets([
        "<b>Check polarity with the multimeter</b> %s. Battery + and &minus; where you "
        "expect; boost %s output close to 5.0V. Only then connect the brain %s."
        % (ref(18), ref(10), ref(4)),
        "Power up. You should get the dim breathing idle glow.",
        "Press the microswitch %s by hand. The comet should launch from the <b>elbow</b> "
        "end and travel to the <b>fingertip</b> end, and the motor should spin." % ref(15),
        "If the comet runs backwards, the strip pieces are reversed. <b>Fix it in the "
        "wiring, not in the code</b> &mdash; both arms run identical firmware and that "
        "is worth a resolder.",
        "Let it run five minutes, then touch the boost %s and MOSFET %s. Warm is fine; "
        "too hot to touch means power down and look for a short." % (ref(10), ref(6)),
    ])

    # Step 7
    s.append(P("Step 7 &mdash; Fit the bubble maker", "h2"))
    s.append(P("Mount the blower %s so its nozzle points <b>past your fingertips</b>, in "
               "the direction the comet travels. The bottle of solution sits on the back "
               "of the hand or forearm &mdash; the kit's MakerWorld collection has mounts "
               "to start from. Wire the motor back to the MOSFET %s using silicone wire "
               "%s, because this run flexes." % (ref(1), ref(6), ref(16)), "body"))
    s.append(P("Use the one-way valve cap that came with the kit. It is why the bottle "
               "does not dump solution when you swing your arm around.", "body"))

    # Step 8
    s.append(P("Step 8 &mdash; Flash the firmware", "h2"))
    s += bullets([
        "Install the Arduino IDE, then add ESP32 board support (Boards Manager, search "
        "<font face=\"Courier\">esp32</font>, install the Espressif package).",
        "Install the <b>FastLED</b> library from the Library Manager.",
        "Select board <font face=\"Courier\">XIAO_ESP32C3</font>.",
        "Open <font face=\"Courier\">firmware/clown_arm/clown_arm.ino</font>.",
        "<b>Edit the layout constants</b> at the top to match your Step 1 measurements.",
        "Plug in USB-C and upload. If it fails, hold BOOT while plugging the cable in.",
    ])
    s.append(P("constexpr int FOREARM_PX = 15;&nbsp;&nbsp; // your forearm pixel count<br/>"
               "constexpr int HAND_PX&nbsp;&nbsp;&nbsp; = 6;&nbsp;&nbsp;&nbsp; // your hand pixel count<br/>"
               "constexpr int GAP_PX&nbsp;&nbsp;&nbsp;&nbsp; = 2;&nbsp;&nbsp;&nbsp; // jumper length / 1.67 cm", "code"))
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
               "measure it." % ref(1), "body"))

    # Step 10
    s.append(P("Step 10 &mdash; Mount into the glove", "h2"))
    s.append(P("Hiding the strip %s under fabric is an upgrade, not a compromise &mdash; "
               "the fabric diffuses the pixels into one smooth continuous streak instead "
               "of visible dots. But it only works if the fabric cooperates." % ref(2),
               "body"))
    s.append(callout(
        "Test the fabric before you commit",
        "Hold a powered section of strip %s under the glove %s in a dark room. Thin, pale, "
        "stretchy fabric glows beautifully; thick or dark fabric, especially leather, "
        "swallows almost all of it. If you cannot see it clearly, no firmware setting "
        "will rescue it &mdash; get a different glove." % (ref(2), ref(3))))
    s += bullets([
        "Run the strip across the <b>back of the hand</b>, over the knuckles. Never the "
        "palm &mdash; that is where the trigger %s is and where you grip things." % ref(15),
        "Stop short of the fingertips. The bubble nozzle %s needs that space, and finger "
        "joints flex too much for strip to survive." % ref(1),
        "Sew a <b>fabric channel</b> for the strip to sit in rather than gluing it down "
        "flat. The channel lets it slide as your hand flexes; glued-taut strip tears "
        "itself off, or tears the glove.",
        "Add <b>strain relief</b> where wires cross the elbow and wrist &mdash; a small "
        "loop of wire tacked down each side of the joint, so movement pulls on the tack "
        "rather than on a solder joint.",
        "<font face=\"Courier\">MAX_BRIGHTNESS</font> is preset high to punch through "
        "fabric. You can raise it further for thicker gloves, but current draw climbs "
        "with it and battery life drops.",
    ])

    # Step 11
    s.append(P("Step 11 &mdash; Build the second arm", "h2"))
    s.append(P("Repeat Steps 1 to 10. The only thing to watch: <b>pixel 0 goes at the "
               "elbow on this arm too.</b> It is tempting to mirror the wiring along with "
               "the physical build. Do not. Identical wiring means identical firmware "
               "means one thing to maintain.", "body"))

    # Troubleshooting
    s.append(PageBreak())
    s.append(P("Troubleshooting", "h1"))
    s.append(grid([
        ["Symptom", "Likely cause"],
        ["Nothing lights at all",
         "Check common ground. Check boost %s output is about 5V. Check strip DIN is on "
         "the <i>input</i> end &mdash; follow the arrows." % ref(10)],
        ["First pixel wrong colour, rest fine",
         "Missing or wrong-value data resistor %s." % ref(14)],
        ["Random flickering, especially when moving",
         "Missing level shifter %s, or a loose ground." % ref(5)],
        ["Comet runs fingertips to elbow",
         "Strip %s is reversed. Fix the wiring, not the code." % ref(2)],
        ["Comet appears to jump at the wrist",
         "<font face=\"Courier\">GAP_PX</font> does not match your actual jumper length."],
        ["Colours wrong, red and green swapped",
         "Change <font face=\"Courier\">GRB</font> to <font face=\"Courier\">RGB</font> in "
         "the <font face=\"Courier\">addLeds</font> line."],
        ["Motor whines audibly",
         "PWM frequency dropped below 20 kHz &mdash; check "
         "<font face=\"Courier\">MOTOR_PWM_HZ</font>."],
        ["Motor does not spin",
         "MOSFET %s gate not on D2, or it is not a logic-level part." % ref(6)],
        ["Everything dies when the motor starts",
         "Cell %s sagging, or the polyfuse %s tripping. Check the charge."
         % (ref(8), ref(11))],
        ["Works, then dies after a few minutes",
         "Cell %s protection circuit cutting out. Recharge or swap." % ref(8)],
        ["Elbow pixel pulsing red",
         "Low-battery warning. Swap the cell %s." % ref(8)],
        ["Board will not accept uploads",
         "Hold BOOT while plugging in USB."],
        ["Strip goes dark past the wrist",
         "Cracked trace or failed jumper joint &mdash; the failure the jumper exists to "
         "prevent. Replace it."],
    ], [2.35 * inch, 4.85 * inch]))

    # Customising
    s.append(P("Changing how it behaves", "h2"))
    s.append(P("The whole point of the strip %s is that every pixel takes orders "
               "individually. Everything you would normally want to change lives in one "
               "marked block at the top of the sketch &mdash; edit, reflash over USB-C, "
               "done." % ref(2), "body"))
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
               "long-press to cycle them; ESP-NOW so one arm's trigger fires both arms "
               "at once; a small web page served by the board so you can change colour "
               "and speed from your phone without a laptop." % ref(4), "body"))

    # Field kit
    s.append(P("Field kit", "h2"))
    s.append(P("What to carry when you actually wear this:", "body"))
    s += bullets([
        "A spare charged cell %s per arm." % ref(8),
        "A pre-soldered spare wrist jumper.",
        "A spare microswitch %s." % ref(15),
        "<b>Extra bubble solution.</b> This runs out long before the battery does.",
        "A small screwdriver and some electrical tape.",
    ])

    return s


if __name__ == "__main__":
    build()

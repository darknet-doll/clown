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
         "first time once you are in costume. It has <b>four</b> gates: one drives the "
         "strip [5], one drives the MOSFET gate [10], and the other two still have to be "
         "wired to a defined level &mdash; see Step 4."),
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
        (8, "Protected 18650 cell", "x1, from the kit",
         "A rechargeable battery &mdash; one comes free with each bubble kit [1]. "
         "<i>Protected</i> means a guardian circuit inside cuts it off before you "
         "over-drain or over-charge it. Do not substitute cheaper unprotected cells. "
         "This is strapped to your arm."),
        (9, "Printed cell cradle", "x1, printed",
         "A pocket that holds the cell still, with a lid that clicks shut and opens "
         "without a tool. It has no electrical job: the cell arrives on its own PH2.0 "
         "pigtail, so there is no sled and nothing in here is soldered."),
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
         "For the trigger plate, the cell cradle [9] and the controller pod. You already "
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
        (1, "Bambu Lab Electric Bubble Maker Kit 01 (P6M)", "1", "0 &mdash; 2 on hand",
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
        (6, "Thin, pale, stretchy glove", "1", "a pair &mdash; deciding later",
         "The hand strip hides under this. Fabric spreads the light into a smooth glow "
         "instead of visible dots &mdash; but only if it is thin and pale. Thick or dark "
         "fabric, especially leather, swallows almost all of it."),
        (7, "Sleeve or arm warmer", "1", "a pair &mdash; deciding later",
         "Same job as the glove [6], for the forearm segment. Same fabric rules. Buy both "
         "at once and test them together &mdash; a glove that glows over a sleeve that does "
         "not is a half-lit arm."),
    ]),
    ("THE BRAIN", [
        (8, "Seeed XIAO ESP32-C3", "1", "2",
         "A complete computer the size of a postage stamp. It watches its own arm's trigger "
         "and decides what all 21 lights do, about 60 times a second. You reprogram it over "
         "USB-C &mdash; with a data cable [35], not a charge-only one."),
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
         "74AHCT125 [9], which is what Step 4 does. <b>Whatever you buy, it needs a 10k "
         "gate-to-source pulldown</b> &mdash; without one the gate floats while the board "
         "boots and the blower twitches at every power-up. Bare transistors do not have "
         "one; most modules do not either. Meter it and fit one if it reads open."),
        (11, "1N5819 diode", "2", "4 (get 10)",
         "A one-way valve for electricity, and you need <b>two per arm</b> doing two "
         "different jobs. <b>CR1:</b> a motor is really just a coil of wire, and cutting "
         "power to a coil makes it kick a nasty voltage spike backwards &mdash; CR1 gives "
         "that spike a safe loop to burn itself out in, at the blower end, banded leg to "
         "positive. Skip it and the MOSFET [10] eventually dies. <b>CR2:</b> the XIAO's [8] "
         "5V pad is wired straight to its USB-C port, so with the cell [12] connected the "
         "boost [14] would feed whatever you plug in to reflash from &mdash; CR2 sits "
         "between boost and XIAO, banded leg to the XIAO, and stops that. They are called "
         "CR and not D because the XIAO already has pins named D1 and D2, and one of those "
         "pins is what drives the MOSFET CR1 protects."),
    ]),
    ("POWER", [
        (12, "Protected 18650 cell", "1", "0 &mdash; 2 in the kits",
         "A rechargeable battery &mdash; one comes free with each bubble kit [1], already on "
         "a <b>PH2.0 pigtail</b>. Keep that pigtail: it is what the kit's charger mates to, "
         "so a flat cell swaps pod to charger with no adapter. <i>Protected</i> means a "
         "guardian circuit cuts it off before you over-drain it, and the firmware shuts the "
         "arm down at 3.0V so that circuit never has to act. Never substitute unprotected "
         "cells. This is strapped to your arm. <b>There are no spares:</b> two cells came "
         "with the two kits and none were bought, so a flat cell ends that arm for the "
         "night. Charge both full that morning and kill the disconnect [37] between sets. "
         "Any cell that ever travels loose goes in a case [38] &mdash; the whole can of an "
         "18650 is its negative terminal and the thin wrap is all that covers it."),
        (13, "Printed cell cradle", "1", "0 &mdash; you print it",
         "<b>Not a sled.</b> The cell [12] already leaves the factory on a PH2.0 pigtail, "
         "so it needs no spring contacts and no solder tabs &mdash; only a printed pocket "
         "that holds it still, with a lid that clicks shut and <b>opens without a tool</b>. "
         "Getting the cell out fast is a safety feature, not a convenience. The cradle "
         "grips the cell, never the pigtail: if the cell can shift, the crimp is what "
         "eventually fails. A bought sled stays the fallback if a pigtail is ever torn."),
        (14, "5V boost converter module", "1", "2",
         "A pump, but for voltage. The battery only makes about 3.7V and the lights and "
         "brain need 5V. Here it only has to carry the lights (~0.3A) because the motor "
         "runs straight off the battery, so a small cheap one is genuinely fine."),
        (15, "2A resettable polyfuse (PPTC)", "1", "2 (get 5)",
         "A safety valve that resets itself. If something shorts out, it suddenly becomes "
         "very resistant and chokes the current off before anything gets hot. Let it cool "
         "and it goes back to normal by itself."),
        (16, "100 kilo-ohm resistors", "2", "0 &mdash; 4 on hand",
         "Two resistors that shrink the battery voltage neatly in half, so the brain [8] "
         "can measure it without being damaged. This is what lets the costume warn you "
         "that the cell is nearly flat instead of just dying."),
    ]),
    ("SIGNAL CONDITIONING", [
        (17, "1000 uF electrolytic capacitor", "1", "0 &mdash; 2 on hand",
         "A tiny water tank for electricity. When a lot of LEDs switch on in the same "
         "instant they all gulp power at once; the tank smooths out the gulp so the "
         "voltage does not dip. Polarised &mdash; the leg with the stripe is negative, and "
         "backwards it pops."),
        (18, "0.1 uF ceramic capacitor", "1", "2 &mdash; get an assortment",
         "A second, much smaller capacitor that sits <b>on</b> the level shifter [9] "
         "itself, bridging its two power pins. The big one [17] is a water tank by the "
         "elbow; this one is a cup of water held against the thirsty part. Every time the "
         "chip switches it gulps current in billionths of a second, and the tank is too far "
         "away to answer that fast. Not polarised &mdash; it goes in either way round. "
         "Marked <b>104</b> on the body. Costs about three cents; skipping it buys you "
         "flicker that only happens on the arm."),
        (19, "330-470 ohm resistor", "1", "0 &mdash; 2 on hand",
         "A speed bump on the data wire. It softens the sharp edge of the signal so it "
         "does not bounce back down the wire and garble the message to the first pixel. "
         "Skip it and pixel 1 misbehaves while all the others are fine."),
    ]),
    ("THE TRIGGER", [
        (20, "Snap-action lever microswitch", "1", "0 &mdash; 2 in the kits",
         "A clicky button with a little metal arm sticking off it. <b>One per hand</b> "
         "&mdash; each hand fires its own arm, and nothing crosses the torso. The arm is "
         "the whole point: a wide target you can hit mid-performance without looking. It "
         "also clicks, so you feel it go. One came in each bubble kit [1], so both arms are "
         "covered and there is no spare &mdash; a dead trigger ends that arm."),
    ]),
    ("CONNECTORS &mdash; SO IT COMES APART", [
        (21, "JST-SM pigtail pair, 6-pin", "1", "2 + 1 spare",
         "The <b>elbow</b> plug: strip 5V, ground and data, plus the trigger's two wires, "
         "plus a second ground. Both the trigger and the motor have to reach the pod from "
         "your hand, so both cross <i>both</i> joints &mdash; which is why this is 6-pin and "
         "not 3. Pin 6 is not spare: the elbow run is the longest in the costume, and a "
         "second ground cuts the voltage drop."),
        (22, "JST-SM pigtail pair, 5-pin", "1", "2 + 1 spare",
         "The <b>wrist</b> plug: the strip's three conductors plus this hand's trigger. One "
         "pull and the whole glove [6] comes off. Mate it 3-4 cm above the wrist crease, "
         "where the skin barely moves &mdash; never on the crease itself."),
        (23, "JST-SM pigtail pair, 2-pin", "2", "4 + 2 spares",
         "The motor run, one at each joint. Kept off the data line on purpose: an amp of "
         "switched PWM bundled against a WS2812 wire is asking for flicker. These two are "
         "the only identical pair in the build, and that is safe &mdash; they sit on the same "
         "net, so cross-mating them just shortens the run."),
        (24, "JST-ZH pigtail pair, 2-pin, 1.5 mm", "1", "2 + 2 spares",
         "Goes at the microswitch [20] itself, so a dead trigger is a ten-second swap "
         "rather than a soldering job. <b>It must not be PH2.0.</b> Every cell [12] ships on "
         "a PH2.0 lead, and one wrong plug in a dark room would put 3.7V straight onto "
         "GPIO3. ZH is 1.5 mm pitch, PH is 2.0 &mdash; they physically will not mate."),
        (25, "Dielectric grease", "&mdash;", "1 small tube",
         "Non-conductive waterproof goo. A smear in each connector shell stops soap residue "
         "corroding the contacts over a season. The alternative is intermittent faults you "
         "will chase for hours."),
    ]),
    ("WIRE AND MATERIALS", [
        (26, "Silicone hookup wire, 22-26 AWG", "&mdash;", "one assortment",
         "Wire with soft rubbery insulation instead of stiff plastic. It survives "
         "thousands of bends. Ordinary wire &mdash; especially solid-core &mdash; snaps at "
         "the elbow and wrist within a few hours of wearing it. Thicker for power, "
         "thinner for signals."),
        (27, "Heat-shrink tubing, assorted", "&mdash;", "one assortment",
         "Plastic sleeve that shrinks tight when heated, sealing and insulating each "
         "solder joint. Slide it onto the wire BEFORE you solder. Everyone forgets once."),
        (28, "Protoboard, small", "1", "0 &mdash; 2 on hand",
         "The perforated board the pod's components sit on. Nothing exotic &mdash; a 4 x 6 cm "
         "piece per arm is plenty."),
        (29, "Hot glue, or clear RTV silicone", "&mdash;", "1",
         "Seals the cut ends of the strip [5] against soap. Easy to forget when ordering "
         "and annoying to be without at Step 3."),
        (30, "Needle and thread, or fabric glue", "&mdash;", "1",
         "For sewing the strip channels into the glove [6] and sleeve [7]. A channel the "
         "strip can slide inside &mdash; not glued down flat."),
        (31, "Fabric marker pen", "&mdash;", "1",
         "For marking where your finger pads land on your palm in Step 1. That mark is "
         "where the trigger [20] goes."),
    ]),
    ("TOOLS &mdash; ONE EACH, NOT ONE PER ARM", [
        (32, "Multimeter", "&mdash;", "1",
         "Not optional. Polarity before every first power-up, continuity for tracing a dead "
         "segment, and actual current draw. Minimum spec: DC volts, AC volts, DC current to "
         "2A on a <b>fused</b> input, resistance, and <b>continuity with a fast audible "
         "beeper</b> &mdash; that beeper is what you will live in. Capacitance is worth "
         "having. Auto-ranging, backlight and hold, because you will be under a table."),
        (33, "Soldering iron, flux-core solder, flux pen", "&mdash;", "1",
         "Buy <b>flux-core</b> solder, 0.8 mm; solid wire with no flux is miserable. The "
         "flux pen is separate &mdash; the IP65 strip pads are the grubbiest joints here and "
         "want extra. On leaded vs lead-free: <b>the fumes that make you feel ill are the "
         "flux, not the lead</b>, so ventilate either way. The real lead risk is ingestion, "
         "closed by washing your hands. Lead-free needs a hotter iron and wets worse, which "
         "bites on strip pads; 63/37 is more forgiving. Either is defensible."),
        (34, "Thermal camera", "&mdash;", "1 (borrow it)",
         "Optional, genuinely useful. Turns Step 6's \"touch it and see if it is warm\" into "
         "a measurement, and catches what a fingertip misses: a boost [14] running hot from "
         "a short downstream, a MOSFET [10] that turned out not to be logic-level, a strip "
         "section drawing more than its neighbours. One borrowed session is plenty."),
        (35, "USB-C cable, data capable", "&mdash;", "1",
         "A charge-only cable looks identical and will cost you half an hour of confusion "
         "before you think to suspect it."),
        (36, "3D printer", "&mdash;", "1",
         "For the trigger plate, the cell cradle [13], the controller pod and the bubbler "
         "mount. You already have one."),
    ]),
    ("SEALING, AND GETTING THE CELL OUT FAST", [
        (37, "Battery disconnect switch, SPST", "1", "2",
         "An ordinary switch in the cell's positive lead, ahead of the fuse [15], so one "
         "motion through the costume kills the arm without opening the pod. <b>Rated 3A or "
         "more at DC</b> &mdash; small switches are usually specced for mains AC and far "
         "less for DC, so read the DC line. Get one with a rubber boot: it keeps its own "
         "seal and you can find it by feel in the dark. It does not replace pulling the "
         "cell [12]; it makes the pod safe to open and the arm safe to unplug."),
        (38, "18650 storage case", "&mdash;", "0 &mdash; no spare cells to carry",
         "A hard box with a slot per cell, so a cell cannot short against keys, coins or "
         "another cell. Skipped only because no spares were bought; buy one the day that "
         "changes. Check every cell's wrap before every event and re-wrap any that are "
         "nicked."),
        (39, "Conformal coating, clear acrylic spray", "&mdash;", "1 can",
         "A thin lacquer over the finished board that turns a soaked pod into one you "
         "rinse, dry and keep using. Mask the USB-C port, the boost trimpot [14], the "
         "MOSFET tab [10] and every connector first. Two thin coats. Do it after the bench "
         "test passes, not before &mdash; reworking a coated board is miserable."),
        (40, "Self-amalgamating silicone tape", "&mdash;", "1 roll",
         "Tape with no adhesive: it fuses to itself. One wrap over each mated connector "
         "keeps soap out of the shell, and it comes off in one piece leaving no residue, "
         "which matters on something you unplug every night."),
        (41, "Silicone O-ring cord 2 mm, or foam tape", "&mdash;", "1",
         "The actual seal between the pod and its lid, sitting in a printed groove. Foam "
         "weatherstrip tape works too and needs no groove modelled; it just survives fewer "
         "open-and-close cycles. Nothing sticky and permanent &mdash; you will be opening "
         "this."),
        (42, "M3 heat-set inserts 4.6 &times; 5.0 mm, and M3 &times; 8 mm screws", "4 + 4",
         "1 kit",
         "Inserts are M3 &times; 0.5 brass, <b>4.6 mm OD &times; 5.0 mm long</b>; screws are "
         "<b>M3 &times; 8 mm button head, A2 stainless</b> &mdash; not the carbon-steel ones "
         "in the kit, which rust. Four of each per pod, so the lid screws shut and reopens "
         "without stripping the plastic. A gasket [41] only seals if something squeezes it "
         "evenly."),
        (43, "Rubber grommet or small cable gland", "1", "2 + spares",
         "Wires leave the pod through this, on the underside, not through a bare printed "
         "hole. A printed edge saws through silicone insulation [26] over a season, and the "
         "gap around it is the main way water gets in."),
        (44, "PETG filament", "&mdash;", "1 spool",
         "For the pod, lid, cradle [13], trigger plate and bubbler mount. <b>Not PLA:</b> PLA "
         "softens in a hot car and is brittle exactly where a strapped-on part flexes. Four "
         "perimeters and 1.6 mm walls minimum &mdash; thin FDM walls leak through the layer "
         "lines themselves, gasket or no gasket."),
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


def steps(items, s="bullet"):
    """A numbered list, indented like bullets()."""
    return [Paragraph(t, S[s], bulletText="%d." % (i + 1))
            for i, t in enumerate(items)]


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
        "Already on hand &mdash; and what is left",
        "<b>Two bubble kits %s are here</b>, so the two protected cells %s, the two "
        "chargers and the two lever microswitches %s that ship inside them are covered "
        "too. So are the passives &mdash; 100k %s, 1000 uF %s, 330-470 ohm %s &mdash; and "
        "both protoboards %s.<br/>"
        "<b>Still to buy:</b> two bottles %s (24T/30T neck, <i>not</i> in the kit) and "
        "<b>two of every remaining electronic part</b>. The arms are independent; nothing "
        "is shared.<br/>"
        "<b>Deciding later:</b> the glove %s and sleeve %s. Buy one, test the fabric lit "
        "in a dark room, then buy the rest.<br/>"
        "<b>Deliberately skipped:</b> spare cells, a bought battery sled %s and the cell "
        "storage case %s. See those entries for what that costs."
        % (ref(1), ref(12), ref(20), ref(16), ref(17), ref(19), ref(28),
           ref(2), ref(6), ref(7), ref(13), ref(38))))
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
        % (ref(24), ref(12), ref(1), ref(23), ref(10))))

    s.append(NextPageTemplate("Steps"))
    s.append(PageBreak())

    # ---- Assembly ----------------------------------------------------------
    s.append(P("Assembly", "h1"))
    s.append(P(
        "Read this whole manual once before picking up the soldering iron %s. Several "
        "steps are much easier if you know what is coming &mdash; notably that heat-shrink "
        "%s goes on <i>before</i> you solder, and that you bench-test everything "
        "<i>before</i> anything goes inside a glove %s."
        % (ref(33), ref(27), ref(6)), "body"))
    s.append(P("Budget a full afternoon for the first arm. The second takes about half "
               "as long, because by then you know what you are doing.", "body"))

    s.append(P("What you are building", "h2"))
    s.append(P("<b>Two arms.</b> Each arm is four modules that unplug from each other. "
               "Nothing is soldered end to end across a joint &mdash; that is what lets you "
               "get out of the costume alone, with soapy hands.", "body"))
    s.append(grid([
        ["Module", "Holds", "Unplugs at"],
        ["<b>Pod</b> &mdash; upper arm",
         "brain %s, boost %s, level shifter %s, MOSFET %s, fuse %s, disconnect %s, "
         "cradle %s" % (ref(8), ref(14), ref(9), ref(10), ref(15), ref(37), ref(13)),
         "switch %s + battery plug + straps" % ref(37)],
        ["<b>Sleeve</b> &mdash; forearm", "forearm strip %s, 15 px" % ref(5),
         "elbow: SM 6-pin %s + SM 2-pin %s" % (ref(21), ref(23))],
        ["<b>Glove</b> &mdash; hand",
         "hand strip 6 px, this hand's trigger %s" % ref(20),
         "wrist: SM 5-pin %s" % ref(22)],
        ["<b>Bubbler</b>", "bottle %s, cap, hose, blower head" % ref(2),
         "wrist: SM 2-pin %s + its strap" % ref(23)],
    ], [1.30 * inch, 3.55 * inch, 1.55 * inch]))
    s.append(P("<b>Steps 1&ndash;11 build one arm. Step 12 is the second arm. Step 13 is the "
               "costume</b> &mdash; the two arms together, and how you get in and out of it.",
               "body"))

    s.append(callout(
        "Safety, briefly but seriously",
        "The cell %s is lithium. Never short its terminals, never charge a puffy or "
        "damaged cell, and do not leave it charging unattended. "
        "<b>Check polarity with the multimeter %s before you connect the battery the "
        "first time</b> &mdash; reversed power destroys the brain %s and the strip %s "
        "instantly and permanently.<br/><br/>"
        "<b>You must be able to kill and remove the cell in seconds, one-handed.</b> That "
        "is what the disconnect switch %s and a tool-free cradle lid %s are for. If getting "
        "the battery out needs two hands, a screwdriver, or taking a sleeve off first, the "
        "pod is not finished. <b>There are no spare cells</b> &mdash; two came with the "
        "kits and none were bought, so charge both full and kill the switch between sets. "
        "Any cell that does travel loose goes in a case %s, never a bag with keys.<br/><br/>"
        "Solder somewhere ventilated. The fumes are flux, not lead &mdash; unpleasant "
        "whichever solder %s you bought."
        % (ref(12), ref(32), ref(8), ref(5), ref(37), ref(13), ref(38), ref(33))))

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
        "That is where the trigger %s goes. Mark it with a fabric pen %s." % (ref(20), ref(31)),
    ])
    s.append(P("Convert the first two into pixel counts. At 60 LED/m each pixel on the "
               "strip %s is <b>1.67 cm</b>:" % ref(5), "body"))
    s.append(P("forearm pixels = forearm cm / 1.67<br/>"
               "hand pixels&nbsp;&nbsp;&nbsp; = hand cm / 1.67", "code"))
    s.append(P("That is usually about <b>15</b> forearm pixels and <b>6</b> hand pixels. "
               "Round down. <b>Then subtract about 4 cm from the forearm figure</b> &mdash; "
               "the wrist umbilical and its connector %s need to live in the last few "
               "centimetres of forearm, just above the crease where the skin barely flexes."
               % ref(22), "body"))

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
               % (ref(6), ref(22)), "body"))
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
        "Slide heat-shrink %s onto every wire <b>now</b>, before soldering." % ref(27),
        "Solder short silicone leads %s to the forearm piece's <b>output</b> end &mdash; "
        "5V, GND and <b>DO</b> &mdash; then on to pins 1-3 of one pigtail half." % ref(26),
        "Pins 4-5 get two thin wires long enough to run all the way <b>up the forearm to "
        "the elbow</b>. They are the trigger's path to the pod.",
        "Shrink everything down, then seal the exposed strip end with hot glue %s or clear "
        "silicone. That is the soap-proofing." % ref(29),
    ])
    s.append(P("<b>Glove side</b>", "body"))
    s += bullets([
        "Solder pins 1-3 of the other half to the hand piece's <b>input</b> end: 5V to 5V, "
        "GND to GND, pin 3 to <b>DI</b>.",
        "Pins 4-5 get two wires long enough to reach the palm, ending in the <b>female half "
        "of a JST-ZH 2-pin</b> %s. That is where the microswitch plugs in at Step 5." % ref(24),
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
               "<b>upper arm</b>. It used to say \"above the soap spray\" &mdash; Step 11 "
               "explains why that stopped being true and what the enclosure has to do "
               "instead." % ref(28), "body"))
    s.append(grid([
        ["From", "To", "Notes"],
        ["Battery %s + (PH2.0)" % ref(12), "Disconnect switch %s" % ref(37),
         "Kills the arm without opening the pod"],
        ["Disconnect %s out" % ref(37), "Polyfuse %s, then everything else" % ref(15),
         "Fuse next, before anything else"],
        ["Battery %s &minus; (PH2.0)" % ref(12), "Common ground", "Everything shares this"],
        ["Battery + (after fuse)", "Boost %s IN+" % ref(14), ""],
        ["Boost %s OUT+ (5V)" % ref(14),
         "74AHCT125 %s Vcc, elbow SM-6 %s pin 1" % (ref(9), ref(21)),
         "Strip and shifter, straight off the boost"],
        ["74AHCT125 %s Vcc (pin 14)" % ref(9),
         "0.1 uF ceramic %s, then 74AHCT125 GND (pin 7)" % ref(18),
         "<b>Decoupling &mdash; on the chip, see below</b>"],
        ["Boost %s OUT+ (5V)" % ref(14),
         "CR2 %s anode; its banded leg to the XIAO %s 5V pad" % (ref(11), ref(8)),
         "<b>Isolation diode &mdash; see below</b>"],
        ["Battery + (after fuse)", "Motor +, via elbow SM-2 %s" % ref(23),
         "Motor runs <b>direct from the cell</b>, not from 5V"],
        ["Motor &minus; (via elbow SM-2)", "MOSFET %s output" % ref(10), ""],
        ["XIAO GPIO4 (silk D2)", "74AHCT125 %s <b>second</b> gate input" % ref(9),
         "Gate drive &mdash; see below"],
        ["74AHCT125 %s second gate out" % ref(9),
         "100 ohm, then MOSFET %s gate" % ref(10),
         "Plus a 10k gate-to-source pulldown"],
        ["XIAO GPIO10 (silk D10)", "74AHCT125 %s input" % ref(9), ""],
        ["74AHCT125 %s output" % ref(9),
         "Resistor %s, then elbow SM-6 pin 3" % ref(19),
         "Resistor at the connector end"],
        ["XIAO GPIO3 (silk D1)", "Elbow SM-6 pin 4",
         "Trigger, arriving from the hand"],
        ["Elbow SM-6 pin 5", "Common ground", "Trigger return"],
        ["XIAO GPIO2 (silk D0)", "Midpoint of the two 100k resistors %s" % ref(16),
         "Battery monitor"],
        ["74AHCT125 %s 1OE, 2OE" % ref(9), "Common ground",
         "Enables the two gates you use"],
        ["74AHCT125 %s 3A, 4A" % ref(9), "Common ground",
         "Unused inputs &mdash; must not float"],
        ["74AHCT125 %s 3OE, 4OE" % ref(9), "5V",
         "Unused outputs off. 3Y, 4Y stay open"],
    ], [1.55 * inch, 3.05 * inch, 1.80 * inch]))

    s.append(P("Calibrate the boost module &mdash; do this first", "h2"))
    s.append(callout(
        "It does not arrive at 5V",
        "MT3608-style modules %s ship set wherever the factory's screwdriver left them, "
        "often <b>15&ndash;20V</b>. Wire one straight to the strip %s and the brain %s and "
        "you destroy both in the first second of power. <b>Trim it on its own, with the "
        "output connected to nothing.</b>" % (ref(14), ref(5), ref(8))))
    s += steps([
        "<b>Leave the output open.</b> OUT+ and OUT&minus; go nowhere yet &mdash; not the "
        "level shifter %s, not CR2 %s, not the elbow SM-6 %s. Fit the wires if you like, but "
        "leave their far ends loose." % (ref(9), ref(11), ref(21)),
        "<b>Power the input only.</b> Cell %s + through the disconnect %s and fuse %s to "
        "IN+, cell &minus; to IN&minus;. A bench supply at 3.7V with its current limit at "
        "200 mA is better still &mdash; then a wiring mistake cannot become a fire."
        % (ref(12), ref(37), ref(15)),
        "<b>Meter %s across OUT+ and OUT&minus;</b>, and read it <i>before</i> you turn "
        "anything." % ref(32),
        "<b>Wind the trimpot counter-clockwise until the reading drops below 5V</b>, then "
        "bring it up to 5.00V from underneath. Approach from above and every slip "
        "overshoots high, which is the direction that breaks things.",
        "<b>Expect a multi-turn trimpot</b> &mdash; 20-odd turns end to end, and the first "
        "several may appear to do nothing. Keep going and watch the meter; do not force it "
        "past its stop. Some boards use a single-turn pot instead, where a few degrees is "
        "several volts. Clockwise raises the output on the usual boards, but <b>trust the "
        "meter, not the silkscreen</b>.",
        "<b>Anywhere in 4.95&ndash;5.05V is fine.</b> Do not aim high for margin &mdash; "
        "above about 5.25V you are spending the strip's %s headroom for nothing." % ref(5),
        "<b>Check it still holds with a flat cell.</b> Feed the input 3.0V and read the "
        "output again: it should still be ~5V. That is the condition you are in at the end "
        "of the night, and it is where a weak module gives up. One that sags to 4.5V here "
        "has a bad inductor or a cold joint &mdash; bin it, you bought ten.",
        "<b>Re-trim under load.</b> Connect the strip %s and shifter %s, light the strip at "
        "working brightness, and set it back to 5.00V <b>with that load on</b>. That is the "
        "number that matters. The brain %s and CR2 %s stay off until it reads right."
        % (ref(5), ref(9), ref(8), ref(11)),
        "<b>Lock the screw</b> with nail polish or a dab of hot glue. It is a tiny trimmer "
        "on an arm that gets knocked all night, and it drifts.",
    ])
    s.append(P("<b>Each arm has its own module and its own trimpot, so trim both</b> "
               "&mdash; they will not land on the same screw position. And mask the "
               "trimpot before conformal coat in Step 11: coating over it locks the setting "
               "and turns any future retrim into a scraping job.", "body"))

    s.append(callout(
        "Drive the MOSFET gate at 5V, not 3.3V",
        "The XIAO %s swings its outputs to <b>3.3V</b>. Most \"logic-level\" MOSFETs are "
        "specified fully on at <b>Vgs = 5V</b> &mdash; at 3.3V they only partly open, "
        "dissipate the difference as heat, and the blower runs slow and inconsistent."
        "<br/><br/>"
        "<b>The 74AHCT125 %s has four gates and the strip only uses one.</b> Route GPIO4 "
        "through a second gate, exactly as you route the LED data through the first. Add a "
        "<b>100 ohm</b> resistor in series with the gate and a <b>10k</b> pulldown from gate "
        "to source, so the FET is held off while the board boots. It costs nothing &mdash; "
        "the chip is already in the pod.<br/><br/>"
        "<b>Do not use an IRF520 module.</b> It is the top search result for \"Arduino "
        "MOSFET module\" and it is not logic-level: its gate threshold runs to 4V and it "
        "wants ~10V to open properly. It half-works, which is harder to diagnose than not "
        "working at all." % (ref(8), ref(9))))

    s.append(callout(
        "Tie off the two gates you are not using",
        "The 74AHCT125 %s has four gates and you use two. <b>The other two are not spare "
        "parts. They are inputs, and a CMOS input must never be left floating.</b><br/><br/>"
        "A floating input sits wherever stray charge leaves it, usually near the switching "
        "threshold. The gate then oscillates, and the chip dissipates real power doing it "
        "&mdash; tens of milliamps instead of microamps, as heat, continuously, out of a "
        "battery strapped to your arm. It also couples noise into the two gates you do care "
        "about.<br/><br/>"
        "<b>3A and 4A go to ground. 3OE and 4OE go to Vcc</b>, which disables those outputs "
        "&mdash; OE is active low. <b>3Y and 4Y go nowhere at all:</b> they are outputs, so "
        "leave them open and never tie an output to a rail.<br/><br/>"
        "On the DIP-14 part the pins run 1OE, 1A, 1Y, 2OE, 2A, 2Y, GND up one side and 3Y, "
        "3A, 3OE, 4Y, 4A, 4OE, Vcc back down the other. <b>Check the datasheet for the "
        "package you actually bought</b> &mdash; a breakout board renumbers everything. "
        "Four short wires, while the chip is going in." % ref(9)))

    s.append(callout(
        "Decouple the 74AHCT125 at its own pins &mdash; fit C2",
        "<b>A 0.1 uF ceramic %s across pin 14 (Vcc) and pin 7 (GND), legs cut short, "
        "sitting on the chip %s.</b> Not near it &mdash; on it.<br/><br/>"
        "Every time a gate switches, the chip pulls a burst of current out of its supply "
        "pin in a few billionths of a second, and that charge has to come from somewhere "
        "close. The ceramic is a small store right at the pins, so the chip\'s own 5V does "
        "not dip each time it drives an edge.<br/><br/>"
        "<b>The 1000 uF %s does not cover this.</b> That one is bulk storage for the strip, "
        "sitting by the elbow connector, and between it and the chip is a run of protoboard "
        "wire. Different job, different capacitor &mdash; fit both. The ceramic is <b>not "
        "polarised</b>, so it goes in either way round.<br/><br/>"
        "<b>Short legs is the whole point:</b> on 30 mm of leg it is mostly wire. Solder it "
        "straddling the two pins. The XIAO %s and the boost module %s came decoupled "
        "already &mdash; the bare chip is the one part in the pod that did not."
        % (ref(18), ref(9), ref(17), ref(8), ref(14))))

    s.append(callout(
        "Two things that hold the blower off when nothing is telling it to run",
        "<b>The 10k gate-to-source pulldown is not optional.</b> Between the moment the "
        "board resets and the first line of firmware, the gate pin is an input and floats, "
        "and a floating gate holds its last charge. The failure looks like the blower "
        "twitching, or briefly running, every time you power up or reflash &mdash; with the "
        "code doing nothing at all. Bare transistors do not include one. <b>Modules mostly "
        "do not either: meter gate to source with the board unpowered.</b> A few k is fine; "
        "open means fit your own.<br/><br/>"
        "The firmware also drives the pin low as the very first thing it does, but that is "
        "belt to the resistor's braces &mdash; it cannot act before it runs."))

    s.append(callout(
        "Isolate the XIAO's 5V pad &mdash; fit CR2",
        "<b>The XIAO's %s 5V pad is wired straight to its USB-C VBUS.</b> There is no diode "
        "on the board. So with the cell %s connected and a USB cable plugged in, your boost "
        "%s output is sitting on the host port &mdash; a laptop, a phone charger, whatever "
        "you reflash from.<br/><br/>"
        "Fit a <b>1N5819</b> %s between the boost output and the XIAO's 5V pad, <b>banded "
        "leg (cathode) to the XIAO</b>. Current flows boost &rarr; XIAO and nothing flows "
        "back. It costs about 0.3V, so the XIAO sees ~4.7V, comfortably inside its "
        "regulator.<br/><br/>"
        "<b>Only the XIAO goes behind the diode.</b> The strip %s and the level shifter %s "
        "stay on the boost output directly, at a full 5V &mdash; they are the load that "
        "cares." % (ref(8), ref(12), ref(14), ref(11), ref(5), ref(9))))

    s.append(callout(
        "Fit the master disconnect &mdash; SW1",
        "The switch %s goes in the <b>cell positive</b>, between the battery plug and the "
        "fuse %s, so it kills everything downstream including the motor tap and the boost "
        "%s.<br/><br/>"
        "Mount it so you can reach it <b>through the costume, one-handed</b>, without "
        "opening the pod, and <b>label which way is off</b>. Standing in the dark unsure "
        "whether you just switched it off is the failure this part exists to prevent."
        "<br/><br/>"
        "It does not replace pulling the cell %s. It makes the pod safe to open and the arm "
        "safe to unplug in one motion; the cell still comes out for storage, for charging, "
        "and any time something is actually wrong."
        % (ref(37), ref(15), ref(14), ref(12))))

    s.append(P("The pod's two outward plugs", "h2"))
    s.append(P("Everything the pod sends down the arm leaves through exactly two "
               "connectors:", "body"))
    s.append(grid([
        ["Plug", "Pins"],
        ["<b>SM 6-pin</b> %s" % ref(21),
         "1 strip 5V &middot; 2 strip GND &middot; 3 strip data &middot; 4 trigger "
         "&middot; 5 trigger return &middot; <b>6 second ground</b>"],
        ["<b>SM 2-pin</b> %s" % ref(23),
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
               + sp * 26 + "XIAO GPIO2", "code"))
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
        "<b>2.</b> <b>Do not use GPIO8 or GPIO9</b> (silk D8/D9) for anything. They are boot "
        "pins and the board will not start reliably.<br/>"
        "<b>3.</b> <b>Leave the USB-C port reachable</b> when you design the printed pod, "
        "and use a <b>data-capable</b> cable %s. You will reflash this far more often than "
        "you expect."
        % (ref(8), ref(5), ref(9), ref(10), ref(14), ref(12), ref(35))))

    # Step 5
    s.append(P("Step 5 &mdash; Wire this hand's trigger", "h2"))
    s.append(P("<b>Each hand has its own trigger, firing its own arm.</b> Nothing crosses "
               "the torso. You are wiring one of two identical, independent triggers.", "body"))
    s += bullets([
        "Solder two lengths of thin silicone wire %s to the microswitch's <b>COM</b> and "
        "<b>NO</b> (normally open) terminals." % ref(26),
        "Terminate them in the <b>male half of a JST-ZH 2-pin</b> %s &mdash; the mate to the "
        "one you left on the glove side of the umbilical in Step 3." % ref(24),
        "Mount the switch %s on a small printed plate %s, positioned so the <b>lever</b> "
        "sits under your middle and ring finger pads at the spot you marked in Step 1."
        % (ref(20), ref(36)),
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
        "later by standardising on one connector." % (ref(12), ref(8), ref(24))))

    # Step 6
    s.append(P("Step 6 &mdash; Bench test, before anything goes in the glove", "h2"))
    s.append(callout(
        "Do not skip this step",
        "Sewing everything into a glove %s and <i>then</i> discovering a reversed data "
        "arrow is genuinely miserable. Test it flat on the table first, with every "
        "connector mated." % ref(6)))
    s += bullets([
        "<b>Before any power: meter gate to source on the MOSFET</b> %s. A few k, not open. "
        "Open means the pulldown is missing and the blower will twitch at every boot."
        % ref(10),
        "<b>Before any power: check both diodes</b> %s. CR1 banded leg to motor +, at the "
        "blower end. CR2 banded leg to the XIAO %s. CR1 backwards is a dead short across the "
        "cell through the MOSFET, so check that one twice." % (ref(11), ref(8)),
        "<b>Beep through every connector, pin by pin.</b> A pigtail with a crimp that did "
        "not seat looks perfect and works intermittently. Find it now, not at the venue.",
        "<b>Check polarity with the multimeter</b> %s. Battery + and &minus; where you "
        "expect, and the boost %s output at <b>5.00V</b> &mdash; it was trimmed back in "
        "Step 4, before the brain %s was ever connected. If it is not ~5V, unplug the "
        "brain and go retrim it." % (ref(32), ref(14), ref(8)),
        "<b>Confirm CR2 is doing its job:</b> boost output ~5.0V, XIAO 5V pad ~4.7V. That "
        "0.3V step is the diode. The same reading on both sides means you shorted past it.",
        "Power up. You should get the dim breathing idle glow.",
        "<b>Watch the blower as it powers up. It must not twitch.</b> If it kicks, stop: "
        "floating gate.",
        "Press the microswitch %s by hand. The comet should launch from the <b>elbow</b> "
        "end and travel to the <b>fingertip</b> end, and the motor should spin." % ref(20),
        "If the comet runs backwards, the strip pieces are reversed. <b>Fix it in the "
        "wiring, not in the code</b> &mdash; both arms run identical firmware and that "
        "is worth a resolder.",
        "Let it run five minutes, then check for heat.",
    ])
    s.append(callout(
        "Test the low-voltage shutoff, once per arm",
        "Do it on the bench once, so you recognise it in the field and know it works. Feed "
        "the pod <b>2.95V</b> from a bench supply in place of the cell %s: within about six "
        "seconds the elbow pixel starts a slow <b>double</b> blink, the motor stops, and the "
        "trigger does nothing. Wind up to 3.7V and it comes back. No bench supply? Run an "
        "arm flat &mdash; tedious, but it also measures your real runtime.<br/><br/>"
        "<b>Single slow pulse = warning</b> (swap soon). <b>Double blink = shut down</b> "
        "(swap now). They are deliberately different at a glance. Do not lower the cutoff to "
        "squeeze out more runtime: under 3.0V you are trading cell life for a couple of "
        "minutes of bubbles." % ref(12)))
    s.append(callout(
        "Checking for heat",
        "Touch the boost %s and MOSFET %s. Warm is fine; too hot to touch means power down "
        "and look for a short.<br/><br/>"
        "<b>If you can borrow a thermal camera %s, use it here instead.</b> It turns this "
        "from a fingertip guess into a measurement, and shows you what a fingertip misses: a "
        "boost running hot because something downstream is shorted, a MOSFET that turned out "
        "not to be logic-level and is dissipating the difference, or a strip section drawing "
        "more than its neighbours. One borrowed session is plenty."
        % (ref(14), ref(10), ref(34))))

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
        "the MOSFET %s, and the trigger does nothing." % (ref(12), ref(23), ref(10)),
        "Use silicone wire %s for the motor run; it flexes constantly." % ref(26),
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
        % ref(35),
    ])
    s.append(P("constexpr int FOREARM_PX = 15;&nbsp;&nbsp; // your forearm pixel count<br/>"
               "constexpr int HAND_PX&nbsp;&nbsp;&nbsp; = 6;&nbsp;&nbsp;&nbsp; // your hand pixel count<br/>"
               "constexpr int GAP_PX&nbsp;&nbsp;&nbsp;&nbsp; = 5;&nbsp;&nbsp;&nbsp; // umbilical length / 1.67 cm", "code"))
    s.append(P("<b>GAP_PX is the measured pixel-to-pixel distance across the umbilical</b>, "
               "from the last forearm pixel to the first hand pixel, divided by 1.67 cm. "
               "Measure the finished assembly from Step 3 &mdash; <i>including the connector "
               "body</i> %s, which is most of it. About 8 cm gives GAP_PX = 5. Guessing here "
               "is what makes the comet look like it stumbles at the wrist." % ref(22),
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
        "palm &mdash; that is where the trigger %s is and where you grip things." % ref(20),
        "Stop short of the fingertips. The blower head needs that space, and finger "
        "joints flex too much for strip to survive.",
        "Sew a <b>fabric channel</b> %s for the strip to sit in rather than gluing it down "
        "flat. The channel lets it slide as your hand flexes; glued-taut strip tears "
        "itself off, or tears the glove." % ref(30),
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
        "for six hours is uncomfortable." % ref(25)))

    # Step 11
    s.append(PageBreak())
    s.append(P("Step 11 &mdash; Seal it against the soap", "h1"))
    s.append(P("The build used to assume the pod sits on your upper arm, <b>above</b> the "
               "spray. That holds on a bench and fails at a rave, where your arms go up. "
               "Point a bubble gun at the ceiling for four hours and the pod is no longer "
               "above anything. <b>Assume every surface gets wet, from every angle, all "
               "night.</b>", "body"))

    s.append(P("What actually gets in", "h2"))
    s += bullets([
        "<b>Arms overhead.</b> Solution runs <i>down</i> the arm, straight at the pod and "
        "into anything that faces up.",
        "<b>Blowback.</b> The blower %s atomises solution. A fine soapy mist settles on "
        "everything within a metre, including the inside of any vent you left open." % ref(1),
        "<b>Wicking &mdash; the one people miss.</b> Soap film creeps <i>along wire "
        "insulation</i> %s, into a connector shell and out the other end, hours after the "
        "splash that started it. Sealing the box is not enough if the wires are a wick." % ref(26),
        "<b>Other people.</b> Hands go up, drinks get waved, and someone will absolutely "
        "grab your forearm.",
        "<b>Condensation.</b> Warm arm, cold night, sealed box. Water forms <i>inside</i> a "
        "perfectly sealed enclosure with no help from outside.",
    ])
    s.append(P("Dried bubble solution is also mildly conductive and hygroscopic &mdash; it "
               "pulls moisture back out of the air, so a \"dry\" residue across two pins is "
               "a leakage path that comes back every humid night until you clean it off.",
               "body"))

    s.append(callout(
        "The rule: drain it, do not hermetically seal it",
        "Chasing a watertight box is the wrong target. You cannot get there with an FDM "
        "print, a USB port and six wires leaving the case &mdash; and if you did, "
        "condensation would defeat you from the inside.<br/><br/>"
        "Aim for this instead: <b>nothing that gets in can pool on a board; everything that "
        "gets in has a way out at the bottom; everything that gets in dries between "
        "events.</b>"))

    s.append(P("The pod enclosure", "h2"))
    s += bullets([
        "<b>PETG %s, not PLA.</b> PLA goes soft in a hot car and is brittle where this part "
        "flexes under a strap. <b>Four perimeters, 1.6 mm walls minimum</b> &mdash; thin FDM "
        "walls leak through the layer lines themselves." % ref(44),
        "<b>A lid with a gasket groove</b>, closed with four <b>M3 &times; 8 mm button-head "
        "stainless screws</b> into <b>4.6 &times; 5.0 mm brass heat-set inserts</b> %s, with "
        "2 mm silicone cord %s in the groove. Nothing sticky &mdash; you will be opening "
        "this." % (ref(42), ref(41)),
        "<b>Model the insert bosses at 4.0 mm diameter, 6.0 mm deep</b>, with at least 2 mm "
        "of plastic all round &mdash; a boss 8.5 mm across or more. The 0.6 mm the hole is "
        "undersize is the plastic the brass melts into; the extra 1 mm of depth is somewhere "
        "for displaced plastic and the screw tip to go. Clearance in the lid is 3.4 mm. Set "
        "the inserts with a soldering iron at 240 &deg;C, square, until the top is flush to "
        "0.2 mm below the surface. If your lid is not 3 mm thick, screw length is lid "
        "thickness plus 5 mm.",
        "<b>Every opening faces down or aft.</b> Nothing on the top surface, nothing on the "
        "fingertip-facing end.",
        "<b>A 2 mm drain hole at the lowest corner</b>, plus a small vent at the opposite "
        "high corner so it can breathe. Yes, this is a hole in your waterproof box. It is "
        "the difference between a box that drains and a box that holds a puddle against your "
        "protoboard %s." % ref(28),
        "<b>Cable entry through a grommet</b> %s on the underside, and <b>a drip loop on "
        "every wire leaving the pod</b> &mdash; a downward loop below the entry, so water "
        "running along the insulation drips off instead of tracking in." % ref(43),
        "<b>A silicone plug or hinged flap over the USB-C port.</b> It has to stay reachable "
        "and it has to be shut by default.",
    ])

    s.append(callout(
        "Conformal coat the board",
        "The enclosure is the first line, not the only one. A thin coat of clear acrylic "
        "spray %s over the assembled protoboard %s turns a soaked board into one you rinse, "
        "dry and keep using.<br/><br/>"
        "<b>Mask first:</b> the USB-C connector, the boost trimpot %s, the MOSFET tab %s, "
        "every connector housing, and the microswitch %s. Two thin coats beat one thick one. "
        "<b>Do it after the bench test passes</b> &mdash; coating a board you then have to "
        "rework is miserable. Clear RTV %s dabbed over the strip's cut ends does the same "
        "job at the wet end of the arm."
        % (ref(39), ref(28), ref(14), ref(10), ref(20), ref(29))))

    s.append(P("The battery gets its own sealed compartment", "h2"))
    s += bullets([
        "<b>A wall between the cell %s and the electronics</b>, so a leaking or vented cell "
        "does not take the board with it, and so soap that gets in during a swap does not "
        "reach the brain %s." % (ref(12), ref(8)),
        "<b>Nothing in this compartment is soldered</b> %s. With the cell on its factory "
        "pigtail there are no tabs and no joints in here to work loose &mdash; most of why "
        "the cradle beat a sled. Heat-shrink %s and a strain-relief anchor go on the J1 "
        "wires, outside the wall."
        % (ref(13), ref(27)),
        "<b>Nothing metal loose in the compartment.</b> No stray screws, no washers, no "
        "snipped lead ends. Check every time you close it.",
        "<b>Check the cell's own wrap before every event.</b> A nicked 18650 sleeve exposes "
        "the can, which is the negative terminal over the whole body of the cell &mdash; "
        "that is how a cell shorts against something it is only resting on. Re-wrap or bin "
        "any that are torn; they cost almost nothing.",
        "<b>The cradle lid closes positively and opens without a tool.</b> A click, a screw "
        "or a strap.",
        "<b>The cradle grips the cell, not the pigtail.</b> If the cell can shift, the "
        "pigtail takes the load and the crimp is what eventually fails. A foam pad or a "
        "printed rib pinching the wrap is enough.",
    ])

    s.append(callout(
        "The trigger is the leakiest part of the build",
        "A bare lever microswitch %s in your palm, under a glove %s, in soapy water, is not "
        "a sealed part. Cheapest fix first: <b>a printed pocket with a nitrile or silicone "
        "membrane</b> over the lever &mdash; a scrap of a nitrile glove, stretched and glued "
        "around the rim, passes the press through and keeps the liquid out. Otherwise buy a "
        "sealed IP67 microswitch with the same lever, which is harder to source than it "
        "sounds.<br/><br/>"
        "Either way, seal the ZH-2 %s joint: heat-shrink %s over the solder, and dielectric "
        "grease %s in the shell." % (ref(20), ref(6), ref(24), ref(27), ref(25))))

    s.append(P("The connectors", "h2"))
    s += bullets([
        "<b>Grease every shell</b> %s &mdash; you were doing this for corrosion anyway; it "
        "also keeps water out of the contacts." % ref(25),
        "<b>Wrap each mated plug</b> in a turn of self-amalgamating silicone tape %s. It "
        "fuses to itself, takes no adhesive with it, and comes off in one piece when you "
        "need to unplug." % ref(40),
        "<b>Point the plug down</b>, or at worst sideways. A shell facing up is a cup.",
        "The wrist SM-5 %s sits <b>above</b> the cuff, not under it &mdash; a cuff channels "
        "solution straight into the plug." % ref(22),
    ])

    s.append(callout(
        "Test it before you trust it",
        "With the arm assembled, sealed and <b>powered</b> (an unpowered box tells you "
        "nothing about tracking or shorts):<br/><br/>"
        "<b>1.</b> Hold it overhead, the way you would actually fire it. "
        "<b>2.</b> Spray it all over with real bubble solution %s for a full minute &mdash; "
        "from above, from the sides, at the connectors. "
        "<b>3.</b> Fire the trigger a dozen times through the wetting. "
        "<b>4.</b> Leave it ten minutes, still powered, still wet. "
        "<b>5.</b> Open it.<br/><br/>"
        "<b>Look for water inside, and for water tracking along the inside of the wire "
        "entry.</b> Both mean you move the entry point or add a drip loop." % ref(4)))

    # Step 12
    s.append(P("Step 12 &mdash; Build the second arm", "h2"))
    s.append(P("Repeat Steps 1 to 11. Two things to be careful about:", "body"))
    s += bullets([
        "<b>Pixel 0 goes at the elbow on this arm too.</b> It is tempting to mirror the "
        "wiring along with the physical build. Do not. Identical wiring means identical "
        "firmware means one thing to maintain.",
        "<b>Keep the same SM-5 %s and SM-6 %s pin conventions.</b> If arm A puts the trigger "
        "on pins 4-5 and arm B puts it on pins 1-2, then spares are not spares, and one "
        "wrong plug at an event costs you a board. Write the pinout on a bit of tape inside "
        "each pod." % (ref(22), ref(21)),
    ])

    # Step 13
    s.append(PageBreak())
    s.append(P("Step 13 &mdash; Assemble the costume", "h1"))
    s.append(P("Both arms exist. This step is about the thing you actually wear.", "body"))

    s.append(P("Both-arms checkout", "h2"))
    s += bullets([
        "<b>Cells %s out of both pods.</b>" % ref(12),
        "Mate every connector on both arms. Count them: <b>four per arm</b> &mdash; elbow "
        "SM-6 %s, elbow SM-2 %s, wrist SM-5 %s, wrist SM-2 %s &mdash; plus the ZH-2 %s at "
        "each microswitch." % (ref(21), ref(23), ref(22), ref(23), ref(24)),
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
        ["<b>1.</b> Pods on, strapped, cells <b>out</b>, switches %s <b>off</b>.<br/>"
         "<b>2.</b> Sleeves on. Mate elbow SM-6 and SM-2 each side.<br/>"
         "<b>3.</b> Gloves on. Mate wrist SM-5 each side.<br/>"
         "<b>4.</b> Bubblers strapped on, mate wrist SM-2, bottles filled.<br/>"
         "<b>5. Cells in, then switches on.</b> Check both idle glows." % ref(37),
         ("<b>1. Switches %s off, then cells out.</b> Both arms are now dead.<br/>"
          "<b>2.</b> Wrist SM-2 + bubbler strap &rarr; bubblers off, bottles upright.<br/>"
          "<b>3.</b> Wrist SM-5 &rarr; gloves peel off.<br/>"
          "<b>4.</b> Elbow SM-6 + SM-2 &rarr; sleeves come off.<br/>"
          "<b>5.</b> Pod straps.<br/><br/>"
          "Four releases per arm, none needing a second person or a flat surface."
          % ref(37))],
    ], [3.60 * inch, 3.60 * inch]))

    s.append(callout(
        "The two tests that matter",
        "<b>Can you get out of it alone, in a bathroom, with soapy hands, in under a "
        "minute?</b> If not, something is still soldered that should not be, or a strap is "
        "fighting a connector.<br/><br/>"
        "<b>Can you kill and remove either battery %s, one-handed, in under ten seconds?</b> "
        "Switch %s off, cradle lid, plug. If either takes longer, fix the pod before the "
        "event. When something goes wrong mid-event the order is: switch off, cell out, "
        "<i>then</i> work out what happened." % (ref(12), ref(37))))

    s.append(P("Care afterwards", "h2"))
    s += bullets([
        "<b>Cells out for storage.</b> Never store the costume with cells connected. The "
        "switch %s being off is not storage &mdash; a switch can be knocked on in a bag." % ref(37),
        "<b>Open the pods and let them dry</b> before they go away. A sealed damp box is "
        "worse than an open damp box. See Step 11.",
        "Rinse the blower head and cap in warm water &mdash; dried bubble solution glues the "
        "one-way valve shut.",
        "Leave the silicone sleeve on the cap protrusion so the bottle does not empty into "
        "your bag.",
        "Wipe soap residue off any connector that got sprayed, and re-grease it %s." % ref(25),
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
         "Missing or wrong-value data resistor %s." % ref(19)],
        ["Pixel 0 died after a reconnect",
         "Strip was plugged in live. <b>Cell %s out before mating</b>, every time." % ref(12)],
        ["Random flickering, especially when moving",
         "Missing level shifter %s, or a loose ground. Check SM-6 %s pin 6 is actually tied "
         "to ground at both ends." % (ref(9), ref(21))],
        ["Odd pixel glitches or a stuttering blower, only with it all running",
         "Missing 0.1 uF %s at the level shifter %s supply pins, or fitted on long legs. "
         "Step 4." % (ref(18), ref(9))],
        ["Level shifter %s runs warm with nothing obviously wrong" % ref(9),
         "Unused inputs floating. 3A and 4A to ground, 3OE and 4OE to Vcc. Step 4."],
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
         "SM-2 %s &mdash; Step 7." % ref(23)],
        ["Everything dies when the motor starts",
         "Cell %s sagging, or the polyfuse %s tripping. Check the charge."
         % (ref(12), ref(15))],
        ["Works, then dies after a few minutes",
         "Cell %s protection circuit cutting out. Recharge or swap." % ref(12)],
        ["Elbow pixel pulsing red, slow single pulse",
         "Low-battery warning. Swap the cell %s soon." % ref(12)],
        ["Elbow pixel double-blinking red, motor dead, trigger does nothing",
         "Low-voltage shutoff, latched at 3.0V. Swap the cell %s; it clears itself."
         % ref(12)],
        ["Blower twitches every time you power up or reflash",
         "Missing 10k gate pulldown on the MOSFET %s. Meter gate to source &mdash; it "
         "should not read open. Step 4." % ref(10)],
        ["Laptop complains about USB power, or the pod stays alive with the cell out and "
         "USB in",
         "Missing or reversed CR2 %s. The pack is backfeeding the host port. Step 4."
         % ref(11)],
        ["Arm completely dead, cell freshly charged",
         "Disconnect switch %s off, or its DC rating gave out. Check the switch before you "
         "suspect the board." % ref(37)],
        ["It worked, got sprayed, now behaves oddly",
         "Soap tracking across pins. Switch %s off, open it, rinse with isopropyl, dry "
         "fully. Then Step 11." % ref(37)],
        ["One trigger fires the other arm",
         "Not possible by design &mdash; you have cross-plugged two arms. Check each arm is "
         "self-contained."],
        ["Board will not accept uploads",
         "Hold BOOT while plugging in USB. If the port is not recognised at all, suspect a "
         "charge-only cable %s." % ref(35)],
        ["Strip goes dark past the wrist",
         "Cracked trace or failed umbilical joint &mdash; the failure the umbilical exists "
         "to prevent. Swap in your spare."],
        ["Trigger does nothing, one arm",
         "Check the ZH-2 plug %s first, then the switch itself. <b>No spare switch is "
         "carried</b>, so if the switch is dead that arm is done for the night." % ref(24)],
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
        ["VBAT_WARN_MV / VBAT_WARN_CLEAR_MV",
         "When the low-cell warning starts and stops. Keep them apart &mdash; that gap is "
         "the hysteresis that stops it strobing as the motor loads the cell"],
        ["VBAT_CUTOFF_MV",
         "Where the arm shuts itself down. Raising it is fine; lowering it costs cell life"],
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
        "<b>A pre-made spare wrist umbilical</b> %s &mdash; genuinely swappable now that "
        "both ends are connectors." % ref(22),
        "One spare SM pigtail pair of each size %s %s %s."
        % (ref(21), ref(22), ref(23)),
        "<b>The kit's USB charger and a power bank.</b> With no spare cells %s, recharging "
        "between sets is the only way to extend the night." % ref(12),
        "<b>Extra bubble solution</b> %s. This runs out long before the battery does." % ref(4),
        "Spare 3 x 5 silicone tube %s, in case a feed hose splits." % ref(3),
        "A solder pen %s, for repairs you cannot connector your way out of." % ref(33),
        "A small screwdriver and some electrical tape.",
        "<b>Self-amalgamating tape</b> %s, for re-wrapping a plug you had to open." % ref(40),
        "<b>Isopropyl and a cloth.</b> Wiping dried solution off a connector at the venue is "
        "the difference between one dead arm and two.",
    ])
    s.append(P("What this kit cannot fix", "h2"))
    s.append(P(
        "Two failures end an arm for the night, because no spare was bought. "
        "<b>A flat cell</b> %s &mdash; two cells, one per arm, both in use; mitigate by "
        "charging full that morning, knowing the runtime from the Step 6 bench test, and "
        "killing the disconnect %s between sets. <b>A dead trigger</b> %s &mdash; two "
        "switches, one per arm, both in use; the ZH-2 pigtail %s means a spare would swap "
        "in ten seconds, there just is not one yet. Both are cheap to close later: "
        "protected 18650s and lever microswitches sell in multipacks."
        % (ref(12), ref(37), ref(20), ref(24)), "body"))

    return s


if __name__ == "__main__":
    build()

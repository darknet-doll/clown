# Content for the Bubble Clown build tutorial video.
# Each slide: kind, plus fields per kind, plus `say` (narration).

DECK = [

# ---------------------------------------------------------------- opening
dict(kind="title", title="BUBBLE CLOWN", sub="Build tutorial",
     foot="Two arms - thirteen steps - one afternoon each",
     say="This is the build tutorial for the bubble clown costume. "
         "Make a gun shape with either hand, squeeze, and a comet of light runs from your elbow "
         "down to your fingertips, arriving exactly as bubbles start firing out of your fingers. "
         "We will build it in thirteen steps. Follow them in order and you will not have to guess at anything."),

dict(kind="bullets", kicker="OVERVIEW", title="What you are building", items=[
        "Two arms|two identical rigs, one trigger per hand",
        "LED strips|hidden under gloves and sleeves, so it glows from inside",
        "A bubble blower|per hand, firing past your fingertips",
        "Four modules|per arm, that unplug from each other",
     ],
     say="Two arms, two identical rigs. Each hand has its own trigger and fires its own arm. "
         "The light strips hide under the glove and the sleeve, so the glow reads as coming from inside the costume. "
         "And each arm comes apart into four modules that unplug from each other."),

dict(kind="timing", kicker="OVERVIEW", title="The effect, in order",
     say="Here is the sequence you are building. You squeeze. The blower gets a brief over drive pulse to break "
         "static friction, then settles to its run speed. A comet of light launches from the elbow. "
         "About two hundred and fifty milliseconds later the comet lands at your fingertips just as the blower reaches "
         "full speed, and bubbles start. "
         "The light travel is the spin up delay. That is the whole trick. It reads as the light causing the bubbles, "
         "instead of reading as lag."),

dict(kind="modules", kicker="OVERVIEW", title="Four modules per arm",
     say="Nothing is soldered end to end across a joint. The pod sits on your upper arm and holds the brain and the battery. "
         "The sleeve holds the forearm strip. The glove holds the hand strip and that hand's trigger. "
         "And the bubbler is its own module. Each one unplugs, which is what lets you get out of the costume alone, "
         "with soapy hands, without dislocating a shoulder."),

dict(kind="table", kicker="OVERVIEW", title="Five connectors, none interchangeable",
     cols=["Where", "Carries", "Connector"],
     rows=[["Cell to pod", "power", "JST-PH 2.0, 2-pin"],
           ["Elbow", "strip + trigger + ground", "JST-SM 6-pin"],
           ["Elbow", "motor", "JST-SM 2-pin"],
           ["Wrist", "strip + trigger", "JST-SM 5-pin"],
           ["Wrist", "motor", "JST-SM 2-pin"],
           ["Microswitch", "trigger", "JST-ZH 1.5, 2-pin"]],
     note="No two plugs on one arm share both family and pin count",
     say="There are five kinds of connector, and this is deliberate. No two plugs on one arm share both family and pin count. "
         "The three two pin plugs are three different pitches, so none of them will mate with the others. "
         "That is what stops you putting three point seven volts onto a logic pin in a dark room."),

dict(kind="warn", title="Battery out before you mate\nor unmate anything.",
     sub="Every time. It becomes automatic in a day.",
     foot="Feeding data into an unpowered strip is the classic way to kill pixel zero",
     say="This is the one rule you will use constantly. Battery out before you mate or unmate anything. "
         "Feeding data into an unpowered strip pushes current through its input protection diodes, and that is the classic "
         "way to kill pixel zero. Unplug the cell first. Every single time."),

dict(kind="bullets", kicker="BEFORE YOU START", title="Safety, briefly but seriously", items=[
        "Lithium cells|use the protected ones from the kit, never charge a puffy cell",
        "Check polarity|with a multimeter before the first connection, reversed power kills instantly",
        "Soap and electronics|assume every surface gets wet, from every angle, all night",
        "Kill and remove the cell|one-handed, in seconds - that is a safety feature",
        "There are no spare cells|two came with the kits, so a flat cell ends that arm",
        "Ventilate|a cheap fan pulling air away from your face is enough",
     ],
     say="Before you pick up the iron. Use the protected cells that came with the kits, and never charge a damaged or puffy one. "
         "It is strapped to your arm. "
         "Check polarity with a multimeter before you connect the battery the first time, because reversed power destroys the brain "
         "and the strip instantly and permanently. "
         "You must also be able to kill the arm and get the cell out one handed, in seconds. That is what the disconnect switch "
         "and a tool free cradle lid are for. If getting the battery out needs two hands or a screwdriver, the pod is not finished. "
         "Know this before the night starts. There are no spare cells. Two came with the two kits and none were bought, "
         "so a flat cell ends that arm. Charge both full that morning and kill the disconnect between sets. "
         "If you ever do carry a loose cell, it goes in a plastic case, never a bag with keys. The whole can of an "
         "eighteen six fifty is its negative terminal, and the thin wrap is all that covers it. "
         "And solder somewhere ventilated."),

dict(kind="bullets", kicker="BEFORE YOU START", title="How this tutorial runs", items=[
        "Steps one to eleven|build one complete arm, sealed and ready",
        "Step twelve|is the second arm, and takes about half as long",
        "Step thirteen|is the costume, and getting in and out of it",
        "Heat-shrink first|it goes on before you solder, not after",
     ],
     say="Steps one through eleven build one complete arm, sealed and ready to wear. Step twelve is the second arm, "
         "which takes about half as long because you will already know what you are doing. Step thirteen is the costume itself. "
         "One thing worth hearing now, before you start. Heat shrink goes onto the wire before you solder the joint, never after. "
         "Everybody learns this the hard way once."),

# ---------------------------------------------------------------- step 1
dict(kind="section", step=1, title="Measure your arm", sub="Ten minutes. Everything downstream depends on it.",
     say="Step one. Measure your arm."),

dict(kind="numbered", kicker="STEP 1", title="Wear the glove. Strike the pose.", items=[
        "Put on the actual glove and sleeve you will use",
        "Hold your arm out in the finger gun pose",
        "Measure elbow to wrist crease, usually about twenty five centimetres",
        "Measure wrist crease to knuckles, usually about ten",
        "Mark where your middle and ring finger pads land on your palm",
     ],
     say="Put on the glove and the sleeve you are actually going to use, and hold your arm out in the finger gun pose. "
         "Measure elbow to wrist crease, which is usually around twenty five centimetres. "
         "Then measure wrist crease to knuckles across the back of your hand, usually around ten. "
         "And mark the spot on your palm where your middle and ring finger pads land when you squeeze. "
         "That is where the trigger goes. Use a fabric pen."),

dict(kind="bullets", kicker="STEP 1", title="Turn centimetres into pixels", items=[
        "At 60 LED/m|each pixel is 1.67 cm",
        "Forearm pixels|= forearm cm divided by 1.67, about 15",
        "Hand pixels|= hand cm divided by 1.67, about 6",
        "Round down|a slightly short strip is fine, one that does not fit is not",
        "Then subtract 4 cm|from the forearm figure, the umbilical has to live there",
     ],
     say="Now turn those into pixel counts. At sixty LEDs per metre each pixel is one point six seven centimetres. "
         "Divide each measurement by that. For typical arms you get about fifteen pixels on the forearm and six on the hand. "
         "Round down. A slightly short strip is fine. One that does not fit is not. "
         "Then subtract about four centimetres from the forearm figure, because the wrist umbilical and its connector "
         "need to live in the last few centimetres of forearm. "
         "Write these numbers down. You will type them into the firmware in step eight."),

# ---------------------------------------------------------------- step 2
dict(kind="section", step=2, title="Cut the strip", sub="Two pieces. Watch the arrows.",
     say="Step two. Cut the strip."),

dict(kind="numbered", kicker="STEP 2", title="Two pieces, both pointing the same way", items=[
        "Cut in the middle of the copper pads, not beside them",
        "Forearm piece: your forearm pixel count, about 15",
        "Hand piece: your hand pixel count, about 6",
        "Check the printed arrows, data flows elbow to fingertips",
        "Tape the elbow end of the forearm piece, that end is pixel 0",
     ],
     say="The strip has marked cut lines between every pixel, with copper pads either side. "
         "Cut through the middle of the pads, not next to them, so you have pad left on both pieces to solder to. "
         "Cut two pieces, one for the forearm and one for the hand. "
         "Then check the little printed arrows. Data flows elbow to fingertips, so both pieces must have their arrows "
         "pointing the same way, toward your fingers. "
         "Tape the elbow end of the forearm piece. That end is pixel zero."),

dict(kind="warn", title="Getting the arrows backwards\nis the most common build mistake.",
     sub="And the fix is unsoldering everything.",
     foot="Both pieces, arrows toward the fingertips. Check twice.",
     say="It is worth saying plainly. Getting the arrows backwards is the single most common mistake in this build, "
         "and the fix is unsoldering everything. Check both pieces twice before the iron goes anywhere near them."),

dict(kind="strip", kicker="STEP 2", title="Why two pieces, not one",
     say="Here is the layout you are aiming for. Fifteen pixels on the forearm, a gap of about eight centimetres at the wrist, "
         "then six pixels across the back of the hand. "
         "The reason it is split is that your wrist bends constantly. A single continuous strip across that joint will crack "
         "its internal copper traces within a few hours of wear, and everything past the crack goes dark. "
         "The flexible umbilical you build next absorbs that movement instead."),

# ---------------------------------------------------------------- step 3
dict(kind="section", step=3, title="Build the wrist umbilical", sub="The plug that lets the glove come off on its own.",
     say="Step three. Build the wrist umbilical."),

dict(kind="table", kicker="STEP 3", title="Five conductors, one JST-SM 5-pin",
     cols=["Pin", "Carries"],
     rows=[["1", "Strip 5V"], ["2", "Strip GND"], ["3", "Strip data"],
           ["4", "Trigger"], ["5", "Trigger return"]],
     note="Decide this convention now and keep it identical on both arms",
     say="The umbilical carries five conductors. The strip's five volts, ground and data, plus this hand's two trigger wires. "
         "Use a J S T S M five pin pigtail pair, and fix this pin convention now. "
         "Pin one five volts, pin two ground, pin three data, pins four and five the trigger. "
         "Keep it identical on both arms, or your spares are not spares."),

dict(kind="numbered", kicker="STEP 3", title="Sleeve side", items=[
        "Slide heat-shrink onto every wire NOW, before soldering",
        "Solder short silicone leads to the forearm piece's OUTPUT end",
        "Those three go to pins 1, 2 and 3 of one pigtail half",
        "Pins 4 and 5 get thin wire long enough to reach the elbow",
        "Shrink down, then seal the strip end with hot glue or silicone",
     ],
     say="Sleeve side first. Slide the heat shrink onto every wire now. "
         "Solder short silicone leads to the output end of the forearm piece, five volts, ground and data out, "
         "and take those three to pins one, two and three of one half of the pigtail. "
         "Pins four and five get two lengths of thin silicone wire, long enough to run all the way up the forearm to the elbow. "
         "That is the trigger's path to the pod. "
         "Shrink everything down, and seal the exposed strip end with a blob of hot glue or clear silicone. That is your soap proofing."),

dict(kind="numbered", kicker="STEP 3", title="Glove side", items=[
        "Solder pins 1 to 3 of the other half to the hand piece's INPUT end",
        "Pin 3 goes to DI, data in, not data out",
        "Pins 4 and 5 get wire long enough to reach the palm",
        "End those two in the female half of a JST-ZH 2-pin pigtail",
        "Shrink, and seal this strip end the same way",
     ],
     say="Glove side. Solder pins one, two and three of the other pigtail half to the input end of the hand piece. "
         "Five volts to five volts, ground to ground, and pin three to data in. Data in, not data out. "
         "Pins four and five get wire long enough to reach your palm, ending in the female half of a J S T Z H two pin pigtail. "
         "That is where the microswitch will plug in at step five. "
         "Shrink and seal, same as before."),

dict(kind="bullets", kicker="STEP 3", title="Where the connector sits, and why", items=[
        "3 to 4 cm above the wrist crease|that skin barely moves",
        "The glove-side wire is the flex element|leave a service loop, never under tension",
        "Keep it short|about 8 cm total is fine, 15 cm reads as a gap",
        "Measure the finished length|it becomes GAP_PX in step eight",
        "Tug every joint now|better found on the bench than inside a glove",
     ],
     say="Mate the pair about three to four centimetres above the wrist crease, on the forearm, where the skin barely moves. "
         "The crease itself is the worst possible place for a rigid twenty millimetre plastic body. "
         "The glove side wire is the flex element, so leave it long enough to cross the wrist with a service loop. "
         "Keep the whole thing short. Every centimetre between the last forearm pixel and the first hand pixel is dark arm "
         "that the comet has to cross. Eight centimetres is fine. Fifteen will look like a gap. "
         "Measure the finished pixel to pixel distance and write it down. "
         "Then gently tug every joint. Find a weak one now, not inside a sewn glove."),

# ---------------------------------------------------------------- step 4
dict(kind="section", step=4, title="Build the controller pod", sub="The longest step. It all lives on your upper arm.",
     say="Step four. Build the controller pod. This is the longest step, so take it in pieces."),

dict(kind="rail", kicker="STEP 4", title="One cell, two rails",
     say="Start with the shape of the power. One protected eighteen six fifty cell feeds two rails. "
         "The blower motor runs straight off the cell at its native three point seven volts, which is exactly how the kit was designed. "
         "Only the strip and the brain get boosted to five volts, and that is a light load, about zero point three amps, "
         "so a small inexpensive boost module is genuinely adequate. "
         "A master disconnect switch goes first, right at the cell, then a two amp polyfuse, then everything else. "
         "One more part you cannot see on this diagram: a schottky diode between the boost output and the X I A O's five volt pad. "
         "We will come back to why."),

dict(kind="table", kicker="STEP 4", title="The core connections",
     cols=["From", "To"],
     rows=[["Battery + (PH2.0)", "SW1 disconnect, then the polyfuse"],
           ["Battery + after fuse", "Boost IN+ , and motor + via elbow SM-2"],
           ["Boost OUT+ (5V)", "74AHCT125 Vcc and SM-6 pin 1, direct"],
           ["74AHCT125 Vcc (pin 14)", "0.1 uF ceramic, then pin 7 (GND)"],
           ["Boost OUT+ via CR2", "XIAO 5V pad - banded end to the XIAO"],
           ["Motor - via SM-2", "MOSFET module output"],
           ["XIAO GPIO10 (silk D10)", "74AHCT125 in, then 330-470 ohm, SM-6 pin 3"],
           ["XIAO GPIO3 (silk D1)", "SM-6 pin 4, the trigger"],
           ["XIAO GPIO4 (silk D2)", "74AHCT125 second gate, then the MOSFET"],
           ["XIAO GPIO2 (silk D0)", "Battery divider midpoint"]],
     say="These are the core connections. The disconnect switch goes first, then the fuse, right at the battery. "
         "Everything downstream of it shares one common ground. "
         "Data leaves G P I O ten, through the level shifter, through a three hundred and thirty to four hundred and seventy ohm "
         "resistor, and out of the elbow connector. "
         "The trigger arrives on G P I O three. Motor P W M leaves on G P I O four. And G P I O two reads the battery. "
         "A note on names, because it will save you a mistake. We always call a X I A O pin by its G P I O number, and the board's "
         "own printed labels, D ten, D one, D two, D zero, appear only in that silkscreen column. "
         "And the two diodes are called C R one and C R two, never D one and D two, because those are pin names already. "
         "And one small capacitor sits directly across the level shifter's own two power pins. More on that shortly."),

dict(kind="bullets", kicker="STEP 4", title="Drive the MOSFET gate at 5 volts, not 3.3", items=[
        "The XIAO's pins swing to 3.3 V|most logic-level MOSFETs want 5 V to open fully",
        "At 3.3 V|the FET half-opens, gets hot, and the blower runs slow and inconsistent",
        "The 74AHCT125 has four gates|and the strip only uses one, so route GPIO4 through a second",
        "Costs nothing|the chip is already in the pod",
        "Add 100 ohm|in series with the gate, and 10k from gate to source",
     ],
     say="One detail that is easy to get wrong. The X I A O's pins only swing to three point three volts, but most so called "
         "logic level MOSFETs are specified fully on at five. At three point three they only partly open, they dissipate the "
         "difference as heat, and the blower runs slow and inconsistent. "
         "The level shifter in your pod has four gates and the strip only uses one. So route G P I O four through a second gate, "
         "exactly the way you route the LED data through the first. The MOSFET then sees a clean five volt signal, and it costs you nothing. "
         "Add a hundred ohm resistor in series with the gate, and a ten k pulldown from gate to source, so the FET is held off while the board boots."),

dict(kind="warn", title="Do not use an IRF520 module.",
     sub="It is the top search result, and it is not logic-level.",
     foot="Gate threshold up to 4 V, wants ~10 V to open. It half-works, which is harder to diagnose than not working.",
     say="And a warning that will save you an evening. Do not use an I R F five twenty module. "
         "It is the top search result for arduino mosfet module and it is not a logic level part. "
         "Its gate threshold runs up to four volts and it wants about ten to open properly. "
         "It half works, which is much harder to diagnose than not working at all."),

dict(kind="bullets", kicker="STEP 4", title="Fit the master disconnect", items=[
        "SW1 goes in the cell positive|between the battery plug and the fuse",
        "Rated 3 A or more at DC|most small switches are specced for mains AC, read the DC line",
        "Reachable through the costume|one-handed, without opening the pod",
        "Get one with a rubber boot|it keeps its own seal and you can find it by feel",
        "It does not replace pulling the cell|it makes the pod safe to open in one motion",
     ],
     say="First new part. A master disconnect switch, in the cell positive, between the battery plug and the fuse, "
         "so it kills everything downstream including the motor and the boost. "
         "Buy one rated at three amps or more at D C. Most small rockers and toggles are specified for mains A C and far less "
         "for D C, so read the D C line, not the picture. Get one with a rubber boot: it keeps its own seal, and you can find "
         "it by feel in the dark. Mount it so you can reach it through the costume, one handed, without opening the pod, and "
         "label which way is off. "
         "It does not replace pulling the cell. It makes the pod safe to open and the arm safe to unplug in one motion."),

dict(kind="bullets", kicker="STEP 4", title="Isolate the XIAO's 5 V pad - fit CR2", items=[
        "The XIAO's 5V pad|is wired straight to its USB-C VBUS, with no diode on the board",
        "So with the cell in|and a USB cable plugged in, your boost feeds the laptop",
        "Fit a 1N5819|between boost output and the 5V pad, banded end to the XIAO",
        "Costs about 0.3 V|the XIAO sees 4.7 V, well inside its regulator",
        "Only the XIAO goes behind it|the strip and the shifter stay at a full 5 V",
     ],
     say="Second new part, and this one is easy to miss. The X I A O's five volt pad is wired straight to its U S B C power pin. "
         "There is no diode on the board. So with the cell connected and a U S B cable plugged in, your boost converter is sitting "
         "on the host port, feeding a laptop or a phone charger. "
         "Fit a one N five eight one nine schottky between the boost output and the five volt pad, banded end toward the X I A O. "
         "Current flows boost to X I A O, and nothing flows back. It costs about three tenths of a volt, so the board sees about "
         "four point seven, comfortably inside its regulator. "
         "Only the X I A O goes behind the diode. The strip and the level shifter stay on the boost directly, at a full five volts."),

dict(kind="warn", title="The 10k gate pulldown\nis not optional.",
     sub="Without it, the blower twitches every time you power up.",
     foot="Between reset and the first line of firmware the gate pin floats - and a floating gate holds its last charge",
     say="And a warning about the part everyone leaves out. The ten k pulldown from gate to source is not optional. "
         "Between the moment the board resets and the moment the firmware runs, that gate pin is an input, and it floats. "
         "A floating gate holds whatever charge it last had, so the blower twitches, or briefly runs, every time you power up "
         "or reflash, with the code doing nothing at all. "
         "Bare transistors do not include one. Most modules do not either. Meter gate to source with the board unpowered: "
         "a few k is fine, open means fit your own."),

dict(kind="bullets", kicker="STEP 4", title="Tie off the two gates you are not using", items=[
        "The 74AHCT125 has four gates|you use two, and the other two are inputs",
        "A floating CMOS input|drifts to its threshold and oscillates, burning real power",
        "3A and 4A|go to ground - any defined level, ground is the convention",
        "3OE and 4OE|go to Vcc - OE is active low, so that disables those outputs",
        "3Y and 4Y|go nowhere at all - they are outputs, never tie one to a rail",
     ],
     say="One more thing about that level shifter, and it is the kind of detail that bites you months later. "
         "The chip has four gates. You are using two. The other two are not spare parts. They are inputs, and a "
         "C MOS input must never be left floating. "
         "A floating input sits wherever stray charge leaves it, usually somewhere near the switching threshold. "
         "The gate then oscillates, and the chip dissipates real power doing it. Tens of milliamps instead of "
         "microamps, as heat, continuously, out of a battery strapped to your arm. It also couples noise into the "
         "two gates you actually care about, which is the last thing you want on an LED data line. "
         "So: three A and four A go to ground. Three O E and four O E go to V C C, which disables those outputs, "
         "because O E is active low. And three Y and four Y go nowhere at all. Those are outputs. Leave them open, "
         "and never tie an output to a rail. "
         "Four short wires, while the chip is going in."),

dict(kind="bullets", kicker="STEP 4", title="Decouple the level shifter at its own pins", items=[
        "0.1 uF ceramic|across pin 14 and pin 7 - Vcc and ground, on the chip itself",
        "Every switching edge|pulls a burst of current in billionths of a second",
        "The 1000 uF is too far away|that one is bulk storage for the strip, by the elbow",
        "Not polarised|it goes in either way round, unlike the big one",
        "Cut the legs short|on 30 mm of leg it is mostly wire, and does much less",
     ],
     say="And one more part, the cheapest in the build, that people leave out because it looks redundant. "
         "A nought point one microfarad ceramic capacitor goes across the level shifter's power pins. "
         "Pin fourteen and pin seven on the D I P package. V C C and ground, on the chip itself, not near it. "
         "Here is why it is not the same as the big capacitor you already have. "
         "Every time a gate switches, the chip pulls a burst of current out of its supply pin in a few billionths of a second. "
         "The one thousand microfarad sits by the elbow connector, and between it and the chip is a run of protoboard wire. "
         "Electrically that is a long way. It cannot deliver charge that fast. "
         "So the little ceramic sits right at the pins and holds just enough charge for one edge. "
         "Bulk storage at the strip, decoupling at the chip. Different jobs. Fit both. "
         "It is not polarised, so it goes in either way round. And cut the legs short before you solder it, "
         "because on thirty millimetres of leg it is mostly wire, and it does much less than you think. "
         "Skip it and you get a build that works on your bench and misbehaves on your arm."),

dict(kind="table", kicker="STEP 4", title="The pod's two outward plugs",
     cols=["Plug", "Pin", "Carries"],
     rows=[["SM 6-pin", "1", "Strip 5V"], ["", "2", "Strip GND"], ["", "3", "Strip data, after the resistor"],
           ["", "4", "Trigger"], ["", "5", "Trigger return"], ["", "6", "Second ground - not spare"],
           ["SM 2-pin", "1", "Motor +, battery after fuse"], ["", "2", "Motor -, MOSFET output"]],
     say="Everything the pod sends down the arm leaves through exactly two plugs. "
         "A six pin at the elbow for the strip and the trigger, and a two pin for the motor. "
         "Pin six is not a spare, it is a job. The elbow run is the longest in the costume and carries the whole strip's current. "
         "A second ground conductor cuts the voltage drop and gives the data line a better return path. Tie it to common ground at both ends. "
         "And the motor gets its own plug on purpose. Roughly an amp of switched P W M bundled against a data line is asking for flicker. "
         "Twist the motor pair."),

dict(kind="divider", kicker="STEP 4", title="The battery monitor",
     say="The battery monitor is three connections. Two one hundred k resistors in series across the cell, and the midpoint goes to D zero. "
         "That midpoint sits at exactly half the battery voltage, which is safely inside what the brain can measure. "
         "The firmware does two things with that reading. Below three point four volts the elbow pixel pulses red, slowly, as a warning "
         "to swap soon. There is a hundred and fifty millivolt band before that clears again, so it does not strobe on and off "
         "every time the motor loads the cell. "
         "And below three volts, held for several seconds, the arm shuts itself down: the motor cuts, the trigger stops working, "
         "and the elbow pixel double blinks. The cell's own protection board is the backstop, not the plan. "
         "Repeatedly hauling a lithium cell down to its protection cutoff is what kills it."),

dict(kind="bullets", kicker="STEP 4", title="Two parts that are easy to fit backwards", items=[
        "1000 uF capacitor|across the strip's 5V and ground, close to the elbow connector",
        "Its marked stripe|is the NEGATIVE leg",
        "CR1, a 1N5819|straight across the motor terminals, at the blower end",
        "Its banded end|goes to the POSITIVE side - backwards it is a dead short",
        "CR2, the other 1N5819|banded end toward the XIAO - backwards, the board never powers",
        "Check this one twice|it is the cheapest mistake to avoid and the most annoying to find",
     ],
     say="Two parts here are easy to fit backwards. "
         "The one thousand microfarad capacitor goes across the strip's five volts and ground, physically close to the elbow connector. "
         "Watch its polarity. The marked stripe is the negative leg. "
         "The one N five eight one nine diode goes directly across the motor's two terminals at the blower end, "
         "and its banded end goes to the positive side. Backwards, it is a dead short. Check that one twice."),

dict(kind="bullets", kicker="STEP 4", title="Rules that matter", items=[
        "One common ground|brain, strip, shifter, MOSFET, boost and battery all share it",
        "Keep the cell on its factory PH2.0 plug|so it goes pod to charger with no adapter",
        "PH2.0 is the only PH in the build|that is what makes it safe",
        "Never use D8 or D9|they are boot pins, the board will not start reliably",
        "Leave the USB-C port accessible|you will reflash this more often than you expect",
     ],
     say="Four rules worth taping inside the pod. "
         "Everything shares one common ground. Skipping this causes bizarre, hard to diagnose behaviour. "
         "Keep the cell on its factory P H two plug, because the kit's charger mates to the same connector, so a flat cell goes "
         "pod to charger with no adapter. "
         "Never put anything on D eight or D nine, they are boot strapping pins. "
         "And design the printed pod so you can reach the U S B C port without taking anything apart. "
         "Use a data capable cable. A charge only cable looks identical and will cost you half an hour."),

# ---------------------------------------------------------------- step 5
dict(kind="section", step=5, title="Wire this hand's trigger", sub="One of two identical, independent triggers.",
     say="Step five. Wire this hand's trigger."),

dict(kind="numbered", kicker="STEP 5", title="Microswitch to palm plate", items=[
        "Solder thin silicone wire to the switch's COM and NO terminals",
        "Terminate in the MALE half of a JST-ZH 2-pin pigtail",
        "Mount the switch on a small printed plate",
        "Position the lever under your middle and ring finger pads",
        "Orient it so a natural squeeze presses across the lever's length",
     ],
     say="Solder two lengths of thin silicone wire to the microswitch's common and normally open terminals, "
         "and terminate them in the male half of a Z H two pin pigtail. That is the mate to the one you left on the glove side in step three. "
         "Mount the switch on a small printed plate, positioned so the lever sits under your middle and ring finger pads, "
         "at the spot you marked in step one. "
         "Orient the lever so a natural squeeze presses across its length. You should be able to fire it with your eyes closed, "
         "in one motion, every time. If you find yourself aiming, move the plate."),

dict(kind="bullets", kicker="STEP 5", title="Why the switch gets its own tiny plug", items=[
        "A soldered switch|can only be replaced with a soldering iron",
        "On a pigtail|swapping a dead trigger mid-event is a ten second job",
        "You own two switches|one per arm, both in use - the spare is the day you buy one",
        "It must not be PH2.0|every cell in this build ships on a PH2.0 lead",
        "ZH is 1.5 mm, PH is 2.0|they physically will not mate, and that is the entire point",
     ],
     say="Two reasons this tiny plug exists. "
         "First, a soldered in switch can only be replaced with a soldering iron, but one on a pigtail is a ten second swap. "
         "Worth knowing: you own exactly two switches, one per arm, both in use. They came in the bubble kits and no spares "
         "were bought, so right now a dead trigger ends that arm even with the pigtail fitted. The pigtail is what makes a "
         "spare worth carrying the day you buy one. They come in cheap ten packs. "
         "Second, and more important, it must not be P H two point zero. Every cell in this build ships on a P H two lead. "
         "If the trigger used the same connector, one wrong plug in a dark room puts three point seven volts directly onto a logic pin. "
         "Z H is one point five millimetre pitch, P H is two. They will not mate. "
         "That incompatibility is the entire reason for the choice, so do not simplify it away later."),

# ---------------------------------------------------------------- step 6
dict(kind="section", step=6, title="Bench test", sub="Before anything goes into a glove. Do not skip this.",
     say="Step six. Bench test, before anything goes into a glove."),

dict(kind="numbered", kicker="STEP 6", title="Flat on the table, fully wired, nothing mounted", items=[
        "Before any power: meter gate to source, a few k and NOT open",
        "Before any power: check CR1 to motor +, CR2 banded end to the XIAO",
        "Beep through every connector pin by pin, both ends",
        "Meter battery polarity, then set the boost to 5.00 V",
        "Boost 5.0 V but XIAO pad 4.7 V - that 0.3 V step is CR2 doing its job",
        "Power up, dim breathing idle glow, and the blower must NOT twitch",
        "Press the switch: comet from the ELBOW end, motor spins",
        "Run it five minutes, then check for heat",
     ],
     say="Lay the whole thing out flat on the table, fully wired, every connector mated, nothing mounted yet. "
         "Before any power at all, do two checks. Meter gate to source on the MOSFET: you want a few k, not open. Open means the "
         "pulldown is missing. And check both diodes. D one's banded leg to motor positive, at the blower end. D two's banded leg "
         "to the X I A O. D one backwards is a dead short across the cell through the MOSFET, so check that one twice. "
         "Then beep through every connector, pin by pin. A crimp that did not seat looks perfect and works intermittently. Find that now, not at the venue. "
         "Now power. Battery plus and minus where you expect them, and set the boost to five point zero zero volts on its trimpot "
         "before the brain is ever connected. Then confirm the isolation diode: boost output about five volts, X I A O pad about "
         "four point seven. That three tenths of a volt step is the diode. The same reading on both sides means you shorted past it. "
         "Power it up. You should see the dim breathing idle glow, and the blower must not twitch. If it kicks, stop: floating gate. "
         "Press the microswitch by hand. The comet should launch from the elbow end and travel toward the fingertips, and the motor should spin. "
         "Let it run five minutes and check for heat."),

dict(kind="bullets", kicker="STEP 6", title="If the comet runs backwards", items=[
        "Your strip pieces are reversed|the arrows did not match",
        "Fix it in the wiring|not in the code",
        "Both arms run identical firmware|keeping that true is worth the resolder",
        "Warm is fine|too hot to touch is not, power down and look for a short",
        "A borrowed thermal camera|turns the heat check from a guess into a measurement",
     ],
     say="If the comet runs backwards, from the fingertips to the elbow, your strip pieces are reversed. "
         "Fix that in the wiring, not in the code. Both arms run byte identical firmware and keeping that true is worth the resolder. "
         "On heat, warm is fine, too hot to touch is not. Power down and look for a short. "
         "If you can borrow a thermal camera, use it here instead of your fingertip. It shows you a boost module running hot because "
         "something downstream is shorted, or a MOSFET that turned out not to be logic level. One borrowed session is plenty."),

dict(kind="bullets", kicker="STEP 6", title="Test the low-voltage shutoff, once per arm", items=[
        "Feed the pod 2.95 V|from a bench supply, in place of the cell",
        "Within about six seconds|the elbow pixel double-blinks and the motor stops",
        "Wind up to 3.7 V|and it comes back",
        "Single slow pulse = warning|swap soon",
        "Double blink = shut down|swap now",
     ],
     say="One more bench test, worth doing exactly once per arm so you recognise it in the field and know it works. "
         "Feed the pod two point nine five volts from a bench supply in place of the cell. Within about six seconds the elbow "
         "pixel starts a slow double blink, the motor stops, and the trigger does nothing. Wind it up to three point seven and it "
         "comes back. "
         "A single slow pulse is the warning: swap soon. A double blink is the shutoff: swap now. They are deliberately different "
         "at a glance. Do not lower that cutoff to squeeze out more runtime. Below three volts you are trading cell life for a "
         "couple of minutes of bubbles."),

# ---------------------------------------------------------------- step 7
dict(kind="section", step=7, title="Fit the bubbler", sub="Do the hose test before you commit to a mount.",
     say="Step seven. Fit the bubbler."),

dict(kind="bullets", kicker="STEP 7", title="The kit is not one object", items=[
        "A bottle|which you supply, 24T or 30T neck, not in the kit",
        "A cap|with a one-way valve and a silicone sleeve",
        "A blower head|joined to the cap by silicone hose",
        "50 mm of hose inside|ending in the blue gravity ball, so pickup stays in solution at any angle",
        "So the heavy thing and the nozzle|do not have to be in the same place",
     ],
     say="First, understand what you actually have. The kit is not one object. It is a bottle, a cap with a one way valve, "
         "and a blower head, joined by silicone hose. "
         "There is about fifty millimetres of hose inside the bottle ending in a blue gravity ball, which sinks, so the pickup stays "
         "in solution at any arm angle, even inverted. "
         "Which means the heavy thing, the bottle, and the thing that must point past your fingertips, the blower head, "
         "do not have to be in the same place. That opens up a much better mount, if the blower can pull solution far enough."),

dict(kind="numbered", kicker="STEP 7", title="The hose test - twenty minutes, decides the whole mount", items=[
        "Assemble the kit as supplied, confirm it makes bubbles",
        "Replace the OUTSIDE hose with about 150 mm of 3x5 silicone tube",
        "Run it again, held roughly the way your arm will hold it",
        "Does it still make bubbles at the same rate?",
     ],
     say="Now the hose test. Twenty minutes, one length of three by five silicone tube, and it decides your whole mount design. "
         "Do it the day the kit arrives, before any of the soldering. "
         "Assemble the kit as supplied and confirm it makes bubbles. Then replace the outside hose with about a hundred and fifty "
         "millimetres of tube, and run it again, held roughly the way your arm will hold it. "
         "The question is simply, does it still make bubbles at the same rate."),

dict(kind="bullets", kicker="STEP 7", title="If it passes: bottle on the forearm", ok=True, items=[
        "Bottle strapped to the forearm|blower head at the knuckles",
        "Nozzle still points past your fingertips|so the comet illusion is intact",
        "The heaviest item|moves off the end of the lever, where it cost you most",
        "This is the better build|take it if you can get it",
     ],
     say="If it passes, put the bottle on the forearm and the blower head at the knuckles, pointing past your fingertips. "
         "The bubbles still appear to come from your fingers, so the illusion is intact, and the heaviest item on the arm "
         "moves off the end of the lever where it was costing you the most. This is the better build if you can get it."),

dict(kind="bullets", kicker="STEP 7", title="If it fails: both on the back of the hand", items=[
        "Exactly as the kit intends|no modification, no risk",
        "Run the bottle half full|the field kit carries refills anyway",
        "Mount the body back toward the wrist|cap forward, to shorten the lever",
        "Anchor to a wrist strap|a glove will not hold 200 grams swinging all evening",
     ],
     say="If it fails, put both on the back of the hand, exactly as the kit intends, nozzle past the fingertips. "
         "It works as shipped with no modification and no risk. You just manage the weight instead. "
         "Run the bottle half full, mount the body back toward the wrist with the cap forward to shorten the lever arm, "
         "and anchor it to a wrist strap. A glove will not hold two hundred grams swinging for an evening."),

dict(kind="warn", title="Rework the motor lead to JST-SM 2-pin.",
     sub="The kit ships it on PH2.0, which mates straight to the cell.",
     foot="Leave it and the motor can be plugged directly to the battery, bypassing the MOSFET - the trigger does nothing.",
     say="One job on the bubbler that is not cosmetic. The kit ships the motor on a P H two point zero female plug "
         "that mates straight to the cell. Cut it off and fit an S M two pin instead. "
         "If you leave it, the cell can be plugged directly into the motor, bypassing the MOSFET entirely, and then the trigger does nothing. "
         "While you are there, use silicone wire for the motor run, because it flexes constantly, and give the bubbler a quick release strap. "
         "Nothing about its mount should bridge the wrist, or the glove cannot come off without removing the bottle first."),

# ---------------------------------------------------------------- step 8
dict(kind="section", step=8, title="Flash the firmware", sub="Same sketch on both arms, unchanged.",
     say="Step eight. Flash the firmware."),

dict(kind="numbered", kicker="STEP 8", title="Arduino IDE, once", items=[
        "Install the Arduino IDE, then add ESP32 board support",
        "Boards Manager, search esp32, install the Espressif package",
        "Library Manager, search FastLED, install it",
        "Select board: XIAO_ESP32C3",
        "Open firmware/clown_arm/clown_arm.ino",
        "Plug in USB-C and upload",
     ],
     say="Install the Arduino I D E, then add E S P thirty two board support through Boards Manager, searching for esp thirty two "
         "and installing the Espressif package. Then install the Fast L E D library from Library Manager. "
         "Select the X I A O E S P thirty two C three as your board, open the sketch, plug in U S B C and upload. "
         "If the upload fails, hold the boot button while plugging the cable in, to force bootloader mode."),

dict(kind="bullets", kicker="STEP 8", title="Edit three constants at the top", items=[
        "FOREARM_PX|your forearm pixel count, default 15",
        "HAND_PX|your hand pixel count, default 6",
        "GAP_PX|measured umbilical length divided by 1.67 cm, default 5",
        "Measure the finished assembly|connector body included, it is most of the length",
        "Guessing GAP_PX|is what makes the comet stumble at the wrist",
     ],
     say="Before you upload, edit the three layout constants at the top of the sketch to match your own measurements. "
         "Forearm pixels, hand pixels, and gap pixels. "
         "Gap pixels is the measured pixel to pixel distance across the finished umbilical, connector body included, "
         "which is most of it, divided by one point six seven centimetres. About eight centimetres of umbilical gives you five. "
         "Guessing at this number is exactly what makes the comet look like it stumbles at the wrist. "
         "And flash the identical sketch to both arms. There is deliberately no left or right setting. "
         "As long as pixel zero is at the elbow on each arm, the mirroring is physical only."),

# ---------------------------------------------------------------- step 9
dict(kind="section", step=9, title="Tune the timing", sub="The step that makes the whole effect work.",
     say="Step nine. Tune the timing. This is the step that makes the whole effect work, and it can only be done on the finished arm."),

dict(kind="numbered", kicker="STEP 9", title="Film it, watch it, adjust, repeat", items=[
        "Film yourself firing it in slow motion, any phone does 120 or 240 fps",
        "Watch back frame by frame: does the comet arrive early or late?",
        "Comet arrives BEFORE the bubbles: increase COMET_TRAVEL_MS",
        "Comet arrives AFTER the bubbles: decrease it",
        "Reflash and film again, expect three or four rounds",
     ],
     say="The goal is that the comet reaches your fingertips at the exact moment the first bubble appears. "
         "When it is right, the light looks like it is causing the bubbles. When it is wrong by even a tenth of a second, it looks like lag. "
         "So film yourself firing it in slow motion. Any modern phone does a hundred and twenty or two hundred and forty frames a second. "
         "Watch it back frame by frame. If the comet arrives before the bubbles, increase comet travel milliseconds to slow it down. "
         "If it arrives after, decrease it. Reflash, film again. Expect three or four rounds. "
         "The default is two hundred and fifty milliseconds, and if you built the forearm bottle mount, expect a slightly longer number, "
         "because a longer feed hose takes marginally longer to prime."),

# ---------------------------------------------------------------- step 10
dict(kind="section", step=10, title="Mount into the glove and sleeve", sub="Test the fabric before you cut anything.",
     say="Step ten. Mount it into the glove and the sleeve."),

dict(kind="bullets", kicker="STEP 10", title="Test the fabric in a dark room first", items=[
        "Fabric diffuses the pixels|into one smooth streak, which beats an exposed strip",
        "Thin, pale, stretchy|glows beautifully",
        "Thick or dark, especially leather|swallows almost all of it",
        "Hold a powered strip under the actual glove|in a dark room, before committing",
        "Test the sleeve at the same time|no point in a glove that glows and a sleeve that does not",
     ],
     say="Hiding the strip under fabric is a genuine upgrade, not a compromise, because the fabric diffuses the pixels into one smooth "
         "continuous streak instead of visible dots. But it only works if the fabric cooperates. "
         "Thin, pale and stretchy glows beautifully. Thick or dark, especially leather, swallows almost all of it. "
         "So before you commit, hold a powered section of strip under the actual glove, in a dark room. "
         "If you cannot see it clearly, no firmware setting will rescue it. Get a different glove. "
         "And test the sleeve at the same time."),

dict(kind="bullets", kicker="STEP 10", title="Building the lace concept? Read this first", items=[
        "Lace is open mesh|light goes straight through the holes",
        "So the strip stays visibly a strip|a hard bright line with dots, not a glow",
        "Option one: lean in|a crisp glowing line under lace reads as deliberate",
        "Option two: add a diffuser|thin white organza, tulle, or a frosted silicone channel",
        "Test on a scrap|before the gloves are cut into",
     ],
     say="If you are building the lace version from the design board, this section is overridden. "
         "Lace is open mesh. Light passes straight through the holes, so the strip stays visibly a strip, a hard bright line with dots, "
         "rather than a glow. "
         "You can lean into that, because circuitry under something delicate is on theme. Or you can add a diffuser layer underneath, "
         "thin white organza, tulle, or a frosted silicone channel, which gives you the soft glow with the lace pattern silhouetted on top. "
         "It is a taste call and it is cheap to test both. Do it with a scrap, before the gloves are cut into."),

dict(kind="bullets", kicker="STEP 10", title="Routing and strain relief", items=[
        "Back of the hand, over the knuckles|never the palm, that is where the trigger is",
        "Stop short of the fingertips|the nozzle needs that space, and joints flex too much",
        "Sew a fabric channel|rather than gluing the strip taut, so it can slide as you flex",
        "The connector is never the anchor|tack the cable on both sides of every plug",
        "Dielectric grease in each shell|soap residue corrodes contacts over a season",
     ],
     say="Route the strip across the back of the hand, over the knuckles. Never the palm. That is where the trigger is and where you grip things. "
         "Stop short of the fingertips, because the nozzle needs that space and finger joints flex too much for strip to survive. "
         "Sew a fabric channel for the strip to sit in rather than gluing it down flat, so it can slide a little as your hand flexes. "
         "Glued taut strip tears itself off, or tears the glove. "
         "And the connector is never the anchor. Tack the cable to the garment on both sides of every plug, so a snag pulls the tack "
         "rather than the latch. Leave a service loop either side. "
         "Finally, a smear of dielectric grease in each connector shell keeps soap residue from corroding the contacts."),

# ---------------------------------------------------------------- step 11
dict(kind="section", step=11, title="Seal it against the soap",
     sub="Arms go up at a rave. Nothing is above the spray.",
     say="Step eleven. Seal it against the soap."),

dict(kind="bullets", kicker="STEP 11", title="What actually gets in", items=[
        "Arms overhead|solution runs DOWN the arm, straight at the pod",
        "Blowback|the blower atomises solution, a fine mist settles on everything",
        "Wicking|soap film creeps along wire insulation, into a shell, out the other end",
        "Other people|hands go up, drinks get waved, someone grabs your forearm",
        "Condensation|warm arm, cold night, sealed box - water forms INSIDE",
     ],
     say="The build used to assume the pod sits on your upper arm, above the spray. That holds on a bench and fails at a rave, "
         "where your arms go up. Point a bubble gun at the ceiling for four hours and the pod is no longer above anything. "
         "Assume every surface gets wet, from every angle, all night. "
         "Arms overhead means solution runs down the arm, straight at the pod, into anything that faces up. The blower atomises "
         "solution, so a fine soapy mist settles on everything within a metre. "
         "And here is the one people miss: wicking. Soap film creeps along the wire insulation, into a connector shell and out the "
         "other end, hours after the splash that started it. Sealing the box is not enough if the wires are a wick. "
         "Dried bubble solution is also mildly conductive and it pulls moisture back out of the air, so a dry looking residue "
         "across two pins is a leakage path that comes back every humid night until you clean it off."),

dict(kind="warn", title="Drain it.\nDo not hermetically seal it.",
     sub="Nothing pools on a board. Everything has a way out at the bottom.",
     foot="You cannot get watertight with an FDM print, a USB port and six wires leaving the case - and condensation would beat you anyway",
     say="Chasing a watertight box is the wrong target. You cannot get there with an F D M print, a U S B port and six wires "
         "leaving the case, and if you did, condensation would defeat you from the inside. "
         "Aim for this instead. Nothing that gets in can pool on a board. Everything that gets in has a way out at the bottom. "
         "And everything that gets in dries between events."),

dict(kind="bullets", kicker="STEP 11", title="The pod enclosure", items=[
        "PETG, not PLA|PLA goes soft in a hot car and is brittle where a strap flexes it",
        "Four perimeters, 1.6 mm walls|thin FDM walls leak through the layer lines themselves",
        "Gasketed lid|silicone cord in a groove, four M3 x 8 mm screws",
        "Heat-set inserts 4.6 x 5.0 mm|into a 4.0 mm hole, 6.0 mm deep, set at 240 degrees",
        "Every opening faces down or aft|nothing on the top surface",
        "A 2 mm drain hole|at the lowest corner, plus a vent at the high corner",
        "Grommet and a drip loop|on every wire leaving the pod",
     ],
     say="Print the pod in P E T G, not P L A. P L A goes soft in a hot car and it is brittle exactly where a strapped on part "
         "flexes. Four perimeters, one point six millimetre walls minimum, because thin F D M walls leak through the layer lines themselves. "
         "Give it a lid with a gasket groove, two millimetre silicone cord in the groove, and four screws into heat set inserts. "
         "Exact sizes, because they matter here: the inserts are brass, four point six millimetre outside diameter by five millimetre long. "
         "The screws are M three by eight millimetre button heads, in stainless, not the black carbon steel ones the kit comes with. "
         "Model the bosses at four millimetres across and six deep, with at least two millimetres of plastic all round them, "
         "and drill the lid three point four for clearance. "
         "Set the inserts with a soldering iron at two hundred and forty degrees, going in square, until the top sits flush. "
         "Nothing sticky, because you will be opening this. "
         "Every opening faces down or aft. Nothing on the top surface. "
         "Then put a two millimetre drain hole at the lowest corner, and a small vent at the opposite high corner so it can breathe. "
         "Yes, that is a hole in your waterproof box. It is the difference between a box that drains and a box that holds a puddle "
         "against your protoboard. "
         "Wires leave through a grommet on the underside, and every one of them gets a drip loop: a downward loop below the entry, "
         "so water running along the insulation drips off instead of tracking in."),

dict(kind="bullets", kicker="STEP 11", title="Conformal coat the board", items=[
        "Clear acrylic spray|over the assembled protoboard, two thin coats",
        "Mask first|USB-C port, boost trimpot, MOSFET tab, connectors, microswitch",
        "Do it after the bench test passes|reworking a coated board is miserable",
        "Clear RTV on the strip's cut ends|same job, wet end of the arm",
     ],
     say="The enclosure is the first line, not the only one. A thin coat of clear acrylic conformal spray over the assembled "
         "protoboard turns a soaked board into one you rinse, dry and keep using. "
         "Mask before you spray: the U S B C connector, the boost module's trimpot, the MOSFET tab, every connector housing, and "
         "the microswitch. Two thin coats beat one thick one. And do it after the bench test passes, not before, because reworking "
         "a coated board is miserable."),

dict(kind="bullets", kicker="STEP 11", title="The battery gets its own compartment", items=[
        "A wall between cell and electronics|a leaking cell must not take the board with it",
        "Nothing in here is soldered|the cell arrives on its own pigtail, so there are no tabs",
        "Nothing metal loose in there|no screws, no washers, no snipped lead ends",
        "Check the cell's wrap every event|a nick exposes the can, which is the negative terminal",
        "The cradle grips the cell|not the pigtail, or the crimp is what eventually fails",
        "The lid closes positively|and opens without a tool",
     ],
     say="The cell is the part that hurts you if this goes wrong, so it gets its own compartment, with a wall between it and the "
         "electronics. A leaking or vented cell must not take the board with it, and soap that gets in during a swap must not "
         "reach the brain. "
         "Nothing in this compartment is soldered. The cell arrives on its own factory pigtail, so there are no tabs and no "
         "joints in here to work loose. That is most of the reason this build uses a printed cradle instead of a bought sled. "
         "Nothing metal loose in that compartment either, ever. "
         "And check the cell's own wrap before every event. A nicked eighteen six fifty sleeve exposes the can, and the can is the "
         "negative terminal over the whole body of the cell. That is how a cell shorts against something it is only resting on. "
         "Re wrap or bin any that are torn. They cost almost nothing. "
         "The cradle grips the cell itself, never the pigtail. If the cell can shift, the pigtail takes the load and the crimp "
         "is what eventually fails. A foam pad or a printed rib that pinches the wrap is enough. "
         "And the lid closes positively, and opens without a tool."),

dict(kind="bullets", kicker="STEP 11", title="The trigger and the connectors", items=[
        "The microswitch is not sealed|a printed pocket with a nitrile membrane over the lever",
        "Grease every connector shell|it keeps water out as well as corrosion",
        "Wrap each mated plug|in self-amalgamating silicone tape, no adhesive, comes off clean",
        "Point plugs down|a shell facing up is a cup",
        "The wrist SM-5 sits ABOVE the cuff|a cuff funnels solution into the plug",
     ],
     say="A bare lever microswitch in your soapy palm, under a glove, is not a sealed part. The cheapest fix is a printed pocket "
         "with a nitrile or silicone membrane over the lever. A scrap of a nitrile glove, stretched and glued around the rim, "
         "passes the press through and keeps the liquid out. "
         "On the connectors: grease every shell, wrap each mated plug in a turn of self amalgamating silicone tape, and point the "
         "plugs down. A shell facing up is a cup. And the wrist five pin sits above the cuff, not under it, because a cuff funnels "
         "solution straight into the plug."),

dict(kind="numbered", kicker="STEP 11", title="Test it before you trust it", items=[
        "Assemble it, seal it, and POWER it - an unpowered box tells you nothing",
        "Hold it overhead, the way you would actually fire it",
        "Spray it all over with real solution for a full minute, from every angle",
        "Fire the trigger a dozen times through the wetting",
        "Leave it ten minutes, still powered, still wet",
        "Open it: look for water inside, and for water tracking along the wire entry",
     ],
     say="Then test it, before you trust it. Assemble the arm, seal it, and power it, because an unpowered box tells you nothing "
         "about tracking or shorts. "
         "Hold it overhead, the way you would actually fire it. Spray it all over with the real bubble solution for a full minute, "
         "from above, from the sides, and at the connectors. Fire the trigger a dozen times through the wetting. Leave it ten "
         "minutes, still powered, still wet. "
         "Then open it. Look for water inside, and look for water tracking along the inside of the wire entry. Either one means you "
         "move the entry point or add a drip loop."),

# ---------------------------------------------------------------- step 12
dict(kind="section", step=12, title="Build the second arm", sub="Repeat steps one to eleven. Two things to be careful about.",
     say="Step twelve. Build the second arm. It is a repeat of steps one to eleven, with two things to be careful about."),

dict(kind="bullets", kicker="STEP 12", title="Do not mirror the wiring", items=[
        "Pixel 0 goes at the elbow|on this arm too",
        "It is tempting to mirror|along with the physical build, do not",
        "Identical wiring|means identical firmware means one thing to maintain",
        "Keep the same SM-5 and SM-6 pinouts|or your spares are not spares",
        "Write the pinout on tape|inside each pod",
     ],
     say="Pixel zero goes at the elbow on this arm too. It is tempting to mirror the wiring along with the physical build. Do not. "
         "Identical wiring means identical firmware, which means one thing to maintain instead of two. "
         "And keep the same five pin and six pin conventions. If one arm puts the trigger on pins four and five and the other puts it "
         "on one and two, then your spares are not spares, and one wrong plug at an event costs you a board. "
         "Write the pinout on a bit of tape inside each pod."),

# ---------------------------------------------------------------- step 13
dict(kind="section", step=13, title="Assemble the costume", sub="Both arms exist. This is the thing you actually wear.",
     say="Step thirteen. Assemble the costume."),

dict(kind="numbered", kicker="STEP 13", title="Both-arms checkout, before any event", items=[
        "Cells out of both pods, switches off",
        "Mate every connector: four per arm, plus a ZH-2 at each microswitch",
        "Cells in, both arms should show the idle glow",
        "Fire each hand separately, left drives left only, right drives right only",
        "Fire both at once, watch for either arm dimming or glitching",
        "Run both for the length of a bottle of solution",
     ],
     say="With both arms built, run a checkout before any event. "
         "Cells out of both pods. Mate every connector and count them, four per arm, plus the Z H two at each microswitch. "
         "Cells in, and both arms should show the idle glow. "
         "Fire each hand separately. The left trigger drives the left arm only, the right drives the right only. "
         "If one trigger fires the other arm, you have crossed something, because there is no cross arm wiring in this design at all. "
         "Then fire both at once and watch for either arm dimming or glitching. They are electrically independent, so they should not interact. "
         "Then run both for the length of a bottle of solution. That is your real duty cycle."),

dict(kind="numbered", kicker="STEP 13", title="Getting in - cells go in LAST", items=[
        "Pods on the upper arms, strapped, cells OUT",
        "Sleeves on, mate the elbow SM-6 and SM-2 on each side",
        "Gloves on, mate the wrist SM-5 on each side",
        "Bubblers strapped on, mate the wrist SM-2, bottles filled",
        "Cells in - check both idle glows before you walk out",
     ],
     say="Getting into it. Order matters, and cells go in last, always. "
         "Pods onto the upper arms and strapped, with the cells out. Sleeves on, and mate the elbow six pin and two pin on each side. "
         "Gloves on, and mate the wrist five pin. Bubblers strapped on, mate the wrist two pin, bottles filled. "
         "Then cells in, and check both idle glows before you walk out the door."),

dict(kind="numbered", kicker="STEP 13", title="Getting out - four releases per arm", items=[
        "Cells out - both arms are now dead and safe to unplug",
        "Wrist SM-2 and bubbler strap, bottles go somewhere upright",
        "Wrist SM-5, gloves peel off",
        "Elbow SM-6 and SM-2, sleeves come off",
        "Pod straps",
     ],
     say="Getting out is the reverse, and it is the whole point of the build. "
         "Cells out first. Both arms are now dead and safe to unplug. "
         "Wrist two pin and the bubbler strap, and the bottles go somewhere upright. Wrist five pin, and the gloves peel off. "
         "Elbow six pin and two pin, and the sleeves come off. Then the pod straps. "
         "Four releases per arm, and none of them need a second person or a flat surface."),

dict(kind="warn", ok=True, title="Can you get out of it alone,\nin a bathroom, with soapy hands,\nin under a minute?",
     sub="That is the test that matters.",
     foot="If not, something is still soldered that should not be, or a strap is fighting a connector.",
     say="Here is the test that matters. Can you get out of it alone, in a bathroom, with soapy hands, in under a minute? "
         "If you cannot, then something is still soldered that should not be, or a strap is fighting a connector. "
         "Fix that before the event, not at it."),

dict(kind="bullets", kicker="STEP 13", title="Afterwards", items=[
        "Cells out for storage|never store the costume with cells connected",
        "Rinse the blower head and cap|dried solution glues the one-way valve shut",
        "Leave the silicone sleeve on|so the bottle does not empty into your bag",
        "Wipe and re-grease|any connector that got sprayed",
     ],
     say="Afterwards. Cells out for storage, always. Never store the costume with cells connected. "
         "Rinse the blower head and the cap in warm water, because dried bubble solution glues the one way valve shut. "
         "Leave the silicone sleeve on the cap protrusion so the bottle does not empty into your bag. "
         "And wipe soap residue off any connector that got sprayed, then re grease it."),

# ---------------------------------------------------------------- closing
dict(kind="table", kicker="REFERENCE", title="If something is wrong, start here",
     cols=["Symptom", "Likely cause"],
     rows=[["Nothing lights at all", "Common ground, boost output, or data on the wrong end"],
           ["Worked yesterday, dead today", "A half-seated SM plug looks mated"],
           ["Dies when you move your arm", "Unseated connector or a crimp that did not take"],
           ["Pixel 0 died after a reconnect", "Strip was plugged in live. Cell out first, every time"],
           ["Comet runs fingertips to elbow", "Strip reversed. Fix the wiring, not the code"],
           ["Comet jumps at the wrist", "GAP_PX does not match your measured umbilical"],
           ["Motor weak, MOSFET hot", "Gate driven at 3.3 V, or it is not a logic-level part"],
           ["Motor runs constantly", "Motor still on its factory PH2.0 lead, straight to the cell"],
           ["Blower twitches at power-up", "Missing 10k gate pulldown - the gate floats while the board boots"],
           ["Elbow pixel double-blinking", "Low-voltage shutoff at 3.0 V. Swap the cell, it clears itself"],
           ["Laptop complains about USB power", "Missing or reversed CR2 - the pack is backfeeding the host port"],
           ["Dead arm, freshly charged cell", "SW1 off, or its DC rating gave out. Check the switch first"]],
     say="Most faults in this build come from a short list. If nothing lights at all, check your common ground, your boost output, "
         "and that data is going into the input end of the strip. "
         "If it worked yesterday and not today, check every latch, because a half seated plug looks mated. "
         "If pixel zero died after a reconnect, the strip was plugged in live. "
         "If the comet jumps at the wrist, your gap pixels number does not match reality. "
         "And if the motor is weak and the MOSFET is hot, your gate is being driven at three point three volts, "
         "or the part is not logic level. "
         "Four newer ones worth knowing. If the blower twitches every time you power up, your gate pulldown is missing. "
         "If the elbow pixel is double blinking and the trigger does nothing, that is the low voltage shutoff: swap the cell. "
         "If your laptop complains about U S B power, D two is missing or backwards. And if an arm is completely dead with a "
         "freshly charged cell, check the disconnect switch before you suspect the board. The full table is in the build manual."),

dict(kind="bullets", kicker="REFERENCE", title="Field kit - what actually fails at an event", items=[
        "A pre-made spare wrist umbilical|both ends are connectors now, so it swaps in seconds",
        "One spare SM pigtail pair|of each size",
        "The kit charger and a power bank|no spare cells, so recharging is the only extension",
        "Extra solution|this runs out long before the battery does",
        "Self-amalgamating tape|for re-wrapping a plug you had to open",
        "Isopropyl and a cloth|dried solution on a connector is how one dead arm becomes two",
        "Cannot be fixed in the field|a flat cell, or a dead trigger - one of each per arm",
     ],
     say="Last thing. Your field kit. Carry a pre made spare wrist umbilical and one spare S M pigtail pair of each size. "
         "Because of the connector design, both swap without a soldering iron. Carry the kit charger and a power bank too. "
         "Also carry extra bubble solution. It runs out long before the battery does. "
         "And know the two failures you cannot fix. A flat cell, and a dead trigger. There is one of each per arm and both "
         "are in use, because no spares were bought. Protected cells and lever microswitches both sell in multi packs, "
         "so that is a cheap gap to close before the next event."),

dict(kind="title", title="THAT'S THE BUILD", sub="One arm at a time. Bench test before you sew.",
     foot="Full detail: BUILD.md - the circuit: SCHEMATIC.md - parts and why: PARTS.md - the look: DESIGN.md",
     say="And that is the build. Work one arm at a time, bench test before you sew anything into a glove, "
         "and keep the cell out of the pod whenever you are plugging things together. "
         "Full detail is in the build manual, the circuit itself is drawn in the schematic, the reasoning behind every part is in "
         "the parts list, and the costume direction is in the design document. Go make some bubbles."),
]

// clown_arm — bubble-shooting clown sleeve, one arm.
//
// Squeeze the palm trigger: the blower spins up while a comet of light runs
// from the elbow to the fingertips, landing as the first bubbles fire.
//
// Flash this unchanged to BOTH arms. There is no handedness here — as long as
// pixel 0 sits at the elbow on each arm, the mirroring is physical only.
//
// Board:  Seeed XIAO ESP32-C3
// Core:   ESP32 Arduino core 3.x  (see ledcAttach note below for 2.x)
// Lib:    FastLED
//
// Power:  split rail off one 18650. The cell feeds the blower directly at its
//         native ~3.7V, and a small boost converter feeds the strip and this
//         board at 5V, through a Schottky so the pack can't backfeed USB.
//         See SCHEMATIC.md, PARTS.md and BUILD.md.
//
// Battery: warning at 3.40V with hysteresis, hard shutoff at 3.00V sustained.
//         The cell's own protection board is the backstop, not the plan.

#include <FastLED.h>

// ---------------------------------------------------------------------------
// Tunables — everything you'd want to change lives in this block.
// ---------------------------------------------------------------------------

// Physical layout. The strip is split at the wrist; GAP_PX is how many pixels
// of *virtual* distance the umbilical spans, so the comet doesn't appear to
// jump across the wrist. Measure your own arm (BUILD.md step 1) and adjust.
//
// GAP_PX is the measured distance from the last forearm pixel to the first hand
// pixel, divided by 1.67 cm. That run now includes the SM 5-pin connector body,
// which is most of it — so measure the finished umbilical (BUILD.md step 3)
// rather than guessing from the wire length.
constexpr int FOREARM_PX = 15;   // elbow -> wrist
constexpr int HAND_PX    = 6;    // wrist -> knuckles
constexpr int GAP_PX     = 5;    // umbilical + connector, ~8 cm at 60 LED/m

// Timing. COMET_TRAVEL_MS must match how long the blower takes to reach speed —
// tune it last, on the assembled arm, with slow-motion video (BUILD.md step 9).
constexpr uint16_t COMET_TRAVEL_MS = 250;
constexpr uint16_t COMET_REPEAT_MS = 320;   // gap between comets while held
constexpr uint16_t RELEASE_FADE_MS = 400;   // fingertip flare after release

// Brightness. The strip lives under a glove, and fabric eats a lot of light —
// hence the high cap. Raise it for thicker fabric, but current draw scales with
// it. Only a handful of pixels are lit at once, so heat under the glove is a
// non-issue at these levels.
constexpr uint8_t MAX_BRIGHTNESS  = 180;
// Resting glow. Purely aesthetic now that we're on a battery rather than a
// power bank (no auto-shutoff to defeat) — set to 0 for fully dark when idle.
constexpr uint8_t IDLE_BRIGHTNESS = 20;

// Motor. The blower is wired straight to the cell, so it already sees its native
// voltage — no duty cap needed to fake 3.7V out of a 5V bus. Running just under
// full gives headroom for the kickstart pulse and takes the edge off a
// freshly-charged 4.2V cell. Drop it to slow the bubble rate.
constexpr uint8_t  MOTOR_RUN_DUTY  = 230;
constexpr uint8_t  MOTOR_KICK_DUTY = 255;   // breaks static friction
constexpr uint16_t MOTOR_KICK_MS   = 80;
constexpr uint32_t MOTOR_PWM_HZ    = 20000; // above audible, no whine
constexpr uint8_t  MOTOR_PWM_BITS  = 8;

// Look.
constexpr uint8_t THEME_HUE   = 192;  // comet body
constexpr uint8_t COMET_FADE  = 64;   // higher = shorter tail
constexpr uint8_t FRAME_MS    = 16;   // ~60 fps

// Battery monitor. Read through a 100k/100k divider, so the pin sees half the
// cell voltage. Protected cells cut themselves off around 2.8-3.0V; warn well
// before that so you can swap rather than die mid-performance.
//
// Two thresholds, not one, and they are deliberately apart. A cell sitting right
// on a single threshold drifts either side of it every time the motor starts, so
// the warning strobes on and off and stops meaning anything. WARN asserts at
// VBAT_WARN_MV and only clears again above VBAT_WARN_CLEAR_MV.
constexpr uint16_t VBAT_WARN_MV       = 3400;
constexpr uint16_t VBAT_WARN_CLEAR_MV = 3550;   // hysteresis band, ~150 mV
constexpr uint16_t VBAT_SAMPLE_MS     = 2000;

// Low-voltage shutoff. The cell's own protection board is the last line of
// defence, not the plan -- it opens somewhere around 2.5-3.0V, and getting there
// repeatedly is what kills 18650s. Shut the arm down first, on our terms.
//
// Latched on purpose: once we cut, we stay cut until the cell is swapped. Motor
// off -> cell recovers a little -> threshold crosses back -> motor on -> sag.
// That cycle is exactly what deep-discharge damage looks like.
constexpr uint16_t VBAT_CUTOFF_MV      = 3000;  // sustained = swap the cell
constexpr uint16_t VBAT_RECOVER_MV     = 3600;  // clears the latch: a fresh cell
constexpr uint8_t  VBAT_CUTOFF_CONFIRM = 3;     // consecutive samples, 3 x 2s

// Below this there is no cell on the divider at all -- we are running on USB
// with the battery unplugged, which is the normal bench case. A protected cell
// never reads this low while it is still connected: its protection board opens
// first. Without this, bench-flashing over USB would latch straight into
// shutdown before you could test anything.
constexpr uint16_t VBAT_ABSENT_MV = 2500;

// Pins, by GPIO number, with the XIAO's silkscreen label beside each one - see
// the naming rules in SCHEMATIC.md. Avoid GPIO8/GPIO9, they're boot straps.
constexpr uint8_t PIN_LED   = 10;  // silk D10, via 74AHCT125 then 330-470R
constexpr uint8_t PIN_TRIG  = 3;   // silk D1,  microswitch to GND
constexpr uint8_t PIN_MOTOR = 4;   // silk D2,  MOSFET gate
constexpr uint8_t PIN_VBAT  = 2;   // silk D0,  divider midpoint (ADC capable)

constexpr uint16_t DEBOUNCE_MS = 25;

// ---------------------------------------------------------------------------

constexpr int NUM_LEDS    = FOREARM_PX + HAND_PX;
constexpr int VIRTUAL_LEN = FOREARM_PX + GAP_PX + HAND_PX;

CRGB leds[NUM_LEDS];

enum State : uint8_t { IDLE, FIRING, RELEASING, LOCKOUT };
State state = IDLE;

uint32_t cometStart   = 0;   // when the current comet launched
uint32_t fireStart    = 0;   // when the trigger went down
uint32_t releaseStart = 0;

bool     trigStable   = false;  // debounced trigger, true = squeezed
bool     trigLastRaw  = false;
uint32_t trigChangeAt = 0;

uint32_t vbatLastRead = 0;
uint16_t vbatMv       = 4200;   // primed from a real reading in setup()
bool     vbatLow      = false;  // warning latch, with hysteresis
bool     vbatDead     = false;  // shutoff latch, cleared only by a fresh cell
uint8_t  vbatLowCount = 0;      // consecutive samples under the cutoff

// Map a virtual pixel index onto the physical strip, skipping the wrist gap.
// Returns -1 for positions that fall inside the gap (nothing to light there).
static int virtualToPhysical(int v) {
  if (v < 0 || v >= VIRTUAL_LEN) return -1;
  if (v < FOREARM_PX) return v;
  if (v < FOREARM_PX + GAP_PX) return -1;   // in the umbilical
  return v - GAP_PX;
}

// Add color to one virtual pixel, scaled. No-op if it lands in the gap.
static void addVirtual(int v, const CRGB &color, uint8_t scale) {
  int p = virtualToPhysical(v);
  if (p < 0) return;
  CRGB c = color;
  c.nscale8_video(scale);
  leds[p] += c;
}

// Draw the comet head at a fractional virtual position, split across the two
// neighbouring pixels so movement is smooth rather than steppy.
static void drawComet(float pos, const CRGB &color) {
  int   lo   = (int)pos;
  float frac = pos - lo;
  addVirtual(lo,     color, (uint8_t)(255 * (1.0f - frac)));
  addVirtual(lo + 1, color, (uint8_t)(255 * frac));
}

static void readTrigger() {
  bool raw = (digitalRead(PIN_TRIG) == LOW);   // active low
  uint32_t now = millis();
  if (raw != trigLastRaw) {
    trigLastRaw  = raw;
    trigChangeAt = now;
  } else if (raw != trigStable && (now - trigChangeAt) >= DEBOUNCE_MS) {
    trigStable = raw;
  }
}

// One reading of the cell, in millivolts at the cell, divider undone.
static uint16_t sampleBatteryMv() {
  return (uint16_t)(analogReadMilliVolts(PIN_VBAT) * 2);
}

// Sample the cell occasionally and smooth it, so a motor-start sag doesn't
// flash a false warning, then run both latches off the smoothed value.
static void readBattery() {
  uint32_t now = millis();
  if (now - vbatLastRead < VBAT_SAMPLE_MS) return;
  vbatLastRead = now;

  vbatMv = (uint16_t)((vbatMv * 3 + sampleBatteryMv()) / 4);

  // No cell on the divider: bench power over USB. Don't warn, don't cut, and
  // release a latch we may have set on the way down as the cell was unplugged.
  if (vbatMv < VBAT_ABSENT_MV) {
    vbatLowCount = 0;
    vbatLow      = false;
    vbatDead     = false;
    return;
  }

  // Warning, with hysteresis. Asserts low, clears high, so a cell hovering at
  // the threshold stays warned instead of flickering.
  if (!vbatLow && vbatMv < VBAT_WARN_MV)             vbatLow = true;
  else if (vbatLow && vbatMv > VBAT_WARN_CLEAR_MV)   vbatLow = false;

  // Shutoff. Require several consecutive samples so a motor kick, a cold cell
  // or one bad ADC read can't take the arm down mid-performance. Three samples
  // at VBAT_SAMPLE_MS is about six seconds under the line -- no transient.
  if (vbatMv < VBAT_CUTOFF_MV) {
    if (vbatLowCount < VBAT_CUTOFF_CONFIRM) vbatLowCount++;
    if (vbatLowCount >= VBAT_CUTOFF_CONFIRM) vbatDead = true;
  } else {
    vbatLowCount = 0;
  }

  // A fresh cell clears the latch. Swapping the cell normally power-cycles the
  // board anyway; this covers the case where USB is also plugged in, so the
  // board stays alive across the swap.
  if (vbatDead && vbatMv > VBAT_RECOVER_MV) {
    vbatDead = false;
    vbatLow  = false;
  }
}

static void setMotor(uint8_t duty) {
  // ESP32 Arduino core 3.x. On core 2.x use:
  //   ledcWrite(CHANNEL, duty);
  ledcWrite(PIN_MOTOR, duty);
}

static void renderIdle() {
  uint8_t breath = scale8(cubicwave8((millis() / 12) & 0xFF), IDLE_BRIGHTNESS);
  fill_solid(leds, NUM_LEDS, CHSV(THEME_HUE, 200, breath));
}

static void renderFiring() {
  uint32_t now = millis();
  fadeToBlackBy(leds, NUM_LEDS, COMET_FADE);

  // Relaunch on a loop for as long as the trigger is held.
  if (now - cometStart >= COMET_REPEAT_MS) cometStart = now;

  uint32_t age = now - cometStart;
  if (age <= COMET_TRAVEL_MS) {
    float t   = (float)age / COMET_TRAVEL_MS;
    float pos = t * (VIRTUAL_LEN - 1);
    // White-hot at launch, settling into the theme color as it travels.
    CRGB head = CHSV(THEME_HUE, (uint8_t)(120 + 135 * t), 255);
    drawComet(pos, head);
  }

  // Fingertips stay lit once the first comet has landed and bubbles are flowing.
  if (now - fireStart >= COMET_TRAVEL_MS) {
    leds[NUM_LEDS - 1] |= CHSV(THEME_HUE, 160, 200);
  }
}

static void renderReleasing() {
  uint32_t age = millis() - releaseStart;
  if (age >= RELEASE_FADE_MS) { state = IDLE; return; }

  fadeToBlackBy(leds, NUM_LEDS, 40);
  // Parting flare at the fingertips.
  uint8_t v = 255 - (uint8_t)(255UL * age / RELEASE_FADE_MS);
  leds[NUM_LEDS - 1] |= CHSV(THEME_HUE, 60, v);
}

// Slow red pulse on the elbow pixel when the cell is nearly flat. Deliberately
// at the elbow: it's the end you can see without breaking character.
static void overlayLowBattery() {
  if (vbatDead || !vbatLow) return;   // dead has its own, louder, render
  uint8_t pulse = cubicwave8((millis() / 8) & 0xFF);
  leds[0] = CRGB(scale8(pulse, 180), 0, 0);
}

// Cell is flat and we have cut the motor. Everything dark except a slow red
// double-blink at the elbow, which is unmistakably different from the low
// warning's single pulse and draws almost nothing. Swap the cell to clear it.
static void renderLockout() {
  fill_solid(leds, NUM_LEDS, CRGB::Black);
  uint16_t phase = millis() % 2000;
  bool on = (phase < 120) || (phase >= 260 && phase < 380);
  if (on) leds[0] = CRGB(120, 0, 0);
}

void setup() {
  // Gate low first, before anything slow runs. Between reset and this line the
  // pin floats, and the only thing holding the blower off is the 10k pulldown
  // at the MOSFET gate -- which is why that resistor is not optional. See
  // BUILD.md step 4.
  pinMode(PIN_MOTOR, OUTPUT);
  digitalWrite(PIN_MOTOR, LOW);

  pinMode(PIN_TRIG, INPUT_PULLUP);

  // ESP32 Arduino core 3.x. On core 2.x replace with:
  //   ledcSetup(CHANNEL, MOTOR_PWM_HZ, MOTOR_PWM_BITS);
  //   ledcAttachPin(PIN_MOTOR, CHANNEL);
  ledcAttach(PIN_MOTOR, MOTOR_PWM_HZ, MOTOR_PWM_BITS);
  setMotor(0);

  // Prime the smoothed reading from the real cell, so a flat one is caught in
  // the first couple of seconds rather than after the filter has crawled down
  // from an assumed 4.2V.
  vbatMv = sampleBatteryMv();
  if (vbatMv >= VBAT_ABSENT_MV && vbatMv < VBAT_CUTOFF_MV) vbatDead = true;
  if (vbatMv >= VBAT_ABSENT_MV && vbatMv < VBAT_WARN_MV)   vbatLow  = true;
  state = vbatDead ? LOCKOUT : IDLE;

  FastLED.addLeds<WS2812B, PIN_LED, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(MAX_BRIGHTNESS);
  FastLED.clear(true);
}

void loop() {
  readTrigger();
  readBattery();
  uint32_t now = millis();

  // Low-voltage shutoff overrides every other state. Cut the motor on the way
  // in -- the blower is most of the load, and it is the part that drags a tired
  // cell down into damage.
  if (vbatDead && state != LOCKOUT) {
    setMotor(0);
    state = LOCKOUT;
  }

  switch (state) {
    case IDLE:
      if (trigStable) {
        state      = FIRING;
        fireStart  = now;
        cometStart = now;
        setMotor(MOTOR_KICK_DUTY);
      }
      break;

    case FIRING:
      // Drop out of the kickstart pulse once the motor is turning.
      if (now - fireStart >= MOTOR_KICK_MS) setMotor(MOTOR_RUN_DUTY);
      if (!trigStable) {
        state        = RELEASING;
        releaseStart = now;
        setMotor(0);
      }
      break;

    case RELEASING:
      // Let them re-trigger mid-fade without waiting it out.
      if (trigStable) {
        state      = FIRING;
        fireStart  = now;
        cometStart = now;
        setMotor(MOTOR_KICK_DUTY);
      }
      break;

    case LOCKOUT:
      // Squeezing does nothing now, deliberately. readBattery() releases us if
      // a charged cell turns up.
      setMotor(0);
      if (!vbatDead) state = IDLE;
      break;
  }

  switch (state) {
    case IDLE:      renderIdle();      break;
    case FIRING:    renderFiring();    break;
    case RELEASING: renderReleasing(); break;
    case LOCKOUT:   renderLockout();   break;
  }

  overlayLowBattery();

  FastLED.show();
  FastLED.delay(FRAME_MS);
}

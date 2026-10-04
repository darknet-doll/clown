// strip_test — bench test: squeeze the trigger, a comet runs down the strip.
//
// The XIAO on USB, the kit's microswitch, the 74AHCT125, and a short offcut of
// the WS2812B strip. No motor, no battery, no boost. Proves the level-shifted
// data path before it goes into the pod.
//
// Same pins and the same 74AHCT125 gate as clown_arm.ino, so the wiring
// carries straight over.
//
// Board:  Seeed XIAO ESP32-C3
// Core:   ESP32 Arduino core (Espressif)
// Lib:    FastLED
//
// Tools -> USB CDC On Boot: Enabled, or the Serial Monitor stays blank.

#include <FastLED.h>

constexpr uint8_t PIN_LED  = 10;  // silk D10, -> 74AHCT125 1A; 1Y -> 330-470R -> strip DIN
constexpr uint8_t PIN_TRIG = 3;   // silk D1,  microswitch NO; COM to GND

// The strip and the 74AHCT125 run off the XIAO's 5V pin, i.e. USB. Keep the
// offcut short; the power cap below is the backstop if you lengthen it.
constexpr int      NUM_LEDS     = 10;
constexpr uint8_t  BRIGHTNESS   = 80;
constexpr uint16_t USB_LIMIT_MA = 300;

constexpr uint16_t COMET_TRAVEL_MS = 250;   // same as clown_arm.ino
constexpr uint16_t COMET_REPEAT_MS = 320;
constexpr uint8_t  THEME_HUE       = 192;

constexpr uint16_t DEBOUNCE_MS = 25;

CRGB leds[NUM_LEDS];

bool     trigStable   = false;
bool     trigLastRaw  = false;
uint32_t trigChangeAt = 0;
uint32_t cometStart   = 0;

static void readTrigger() {
  bool raw = (digitalRead(PIN_TRIG) == LOW);   // active low
  uint32_t now = millis();
  if (raw != trigLastRaw) {
    trigLastRaw  = raw;
    trigChangeAt = now;
  } else if (raw != trigStable && (now - trigChangeAt) >= DEBOUNCE_MS) {
    trigStable = raw;
    if (trigStable) cometStart = now;
    Serial.println(trigStable ? "trigger: PRESSED" : "trigger: released");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_TRIG, INPUT_PULLUP);

  FastLED.addLeds<WS2812B, PIN_LED, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, USB_LIMIT_MA);

  // Boot check: red, green, blue, half a second each. All three, in that order,
  // means the data path and the colour order are both right.
  const CRGB boot[] = { CRGB::Red, CRGB::Green, CRGB::Blue };
  for (const CRGB& c : boot) {
    fill_solid(leds, NUM_LEDS, c);
    FastLED.show();
    delay(500);
  }
  FastLED.clear(true);

  Serial.println("strip_test ready — squeeze the trigger");
}

void loop() {
  readTrigger();
  uint32_t now = millis();

  if (trigStable) {
    fadeToBlackBy(leds, NUM_LEDS, 64);
    if (now - cometStart >= COMET_REPEAT_MS) cometStart = now;
    uint32_t age = now - cometStart;
    if (age <= COMET_TRAVEL_MS) {
      int pos = (int)(age * (NUM_LEDS - 1) / COMET_TRAVEL_MS);
      leds[pos] = CHSV(THEME_HUE, 160, 255);
    }
  } else {
    // Dim glow so you can tell "idle" from "data path dead".
    fill_solid(leds, NUM_LEDS, CHSV(THEME_HUE, 200, 20));
  }

  FastLED.show();
  delay(16);
}

// motor_test — bench test: squeeze the trigger, the blower runs and a comet
// runs down the strip.
//
// Adds the motor path to strip_test: D2 -> 74AHCT125 gate 2 -> 100R -> MOSFET
// gate, motor powered from the kit's 18650. XIAO and strip still on USB; no
// boost yet. Same pins, gate and motor timing as clown_arm.ino.
//
// Board:  Seeed XIAO ESP32-C3
// Core:   ESP32 Arduino core 3.x  (ledcAttach; see clown_arm.ino for 2.x)
// Lib:    FastLED
//
// Tools -> USB CDC On Boot: Enabled, or the Serial Monitor stays blank.

#include <FastLED.h>

constexpr uint8_t PIN_LED   = 10;  // silk D10, -> 74AHCT125 1A
constexpr uint8_t PIN_TRIG  = 3;   // silk D1,  microswitch NO; COM to GND
constexpr uint8_t PIN_MOTOR = 4;   // silk D2,  -> 74AHCT125 2A; 2Y -> 100R -> gate

// The strip still runs off the XIAO's 5V pin, i.e. USB. 60 pixels at full
// white would be over 3 A; the power cap scales brightness down to stay under
// USB_LIMIT_MA, so the boot flash will look dimmer than the comet.
constexpr int      NUM_LEDS     = 60;
constexpr uint8_t  BRIGHTNESS   = 80;
constexpr uint16_t USB_LIMIT_MA = 300;

constexpr uint16_t COMET_TRAVEL_MS = 250;   // same as clown_arm.ino
constexpr uint16_t COMET_REPEAT_MS = 320;
constexpr uint8_t  THEME_HUE       = 192;

constexpr uint8_t  MOTOR_RUN_DUTY  = 230;   // same as clown_arm.ino
constexpr uint8_t  MOTOR_KICK_DUTY = 255;
constexpr uint16_t MOTOR_KICK_MS   = 80;
constexpr uint32_t MOTOR_PWM_HZ    = 20000;
constexpr uint8_t  MOTOR_PWM_BITS  = 8;

constexpr uint16_t DEBOUNCE_MS = 25;

CRGB leds[NUM_LEDS];

bool     trigStable   = false;
bool     trigLastRaw  = false;
uint32_t trigChangeAt = 0;
uint32_t fireStart    = 0;
uint32_t cometStart   = 0;

static void setMotor(uint8_t duty) {
  ledcWrite(PIN_MOTOR, duty);
}

static void readTrigger() {
  bool raw = (digitalRead(PIN_TRIG) == LOW);   // active low
  uint32_t now = millis();
  if (raw != trigLastRaw) {
    trigLastRaw  = raw;
    trigChangeAt = now;
  } else if (raw != trigStable && (now - trigChangeAt) >= DEBOUNCE_MS) {
    trigStable = raw;
    if (trigStable) {
      fireStart  = now;
      cometStart = now;
      setMotor(MOTOR_KICK_DUTY);
    } else {
      setMotor(0);
    }
    Serial.printf("[%lu ms] %s\n", (unsigned long)now,
                  trigStable ? "trigger: PRESSED, motor on" : "trigger: released, motor off");
  }
}

void setup() {
  // Motor pin low before anything slow runs, same as clown_arm.ino.
  pinMode(PIN_MOTOR, OUTPUT);
  digitalWrite(PIN_MOTOR, LOW);

  Serial.begin(115200);
  // Never let logging stall the loop. With no Serial Monitor reading, a
  // blocking print freezes everything -- including the motor-off on release.
  Serial.setTxTimeoutMs(0);
  pinMode(PIN_TRIG, INPUT_PULLUP);

  ledcAttach(PIN_MOTOR, MOTOR_PWM_HZ, MOTOR_PWM_BITS);
  setMotor(0);

  FastLED.addLeds<WS2812B, PIN_LED, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.setMaxPowerInVoltsAndMilliamps(5, USB_LIMIT_MA);

  const CRGB boot[] = { CRGB::Red, CRGB::Green, CRGB::Blue };
  for (const CRGB& c : boot) {
    fill_solid(leds, NUM_LEDS, c);
    FastLED.show();
    delay(500);
  }
  FastLED.clear(true);

  Serial.println("motor_test ready — squeeze the trigger");
}

void loop() {
  readTrigger();
  uint32_t now = millis();

  if (trigStable) {
    // Drop out of the kickstart pulse once the motor is turning.
    if (now - fireStart >= MOTOR_KICK_MS) setMotor(MOTOR_RUN_DUTY);

    fadeToBlackBy(leds, NUM_LEDS, 64);
    if (now - cometStart >= COMET_REPEAT_MS) cometStart = now;
    uint32_t age = now - cometStart;
    if (age <= COMET_TRAVEL_MS) {
      // On a long strip the head moves several pixels per frame. Light every
      // pixel it passed since the last frame, or most of them never show.
      static int lastPos = 0;
      int pos = (int)(age * (NUM_LEDS - 1) / COMET_TRAVEL_MS);
      if (pos < lastPos) lastPos = 0;   // a new comet just launched
      for (int i = lastPos; i <= pos; i++) leds[i] = CHSV(THEME_HUE, 160, 255);
      lastPos = pos;
    }
  } else {
    fill_solid(leds, NUM_LEDS, CHSV(THEME_HUE, 200, 20));
  }

  uint32_t t0 = micros();
  FastLED.show();
  uint32_t showUs = micros() - t0;

  // Timing report, once a second: slowest show() and slowest whole loop.
  static uint32_t lastLoop = micros(), maxShow = 0, maxLoop = 0, lastReport = 0;
  uint32_t loopUs = t0 - lastLoop;
  lastLoop = t0;
  if (showUs > maxShow) maxShow = showUs;
  if (loopUs > maxLoop) maxLoop = loopUs;
  if (now - lastReport >= 1000) {
    Serial.printf("[%lu ms] show max %lu us, loop max %lu us, trig raw %d stable %d\n",
                  (unsigned long)now, (unsigned long)maxShow, (unsigned long)maxLoop,
                  digitalRead(PIN_TRIG) == LOW, trigStable);
    maxShow = maxLoop = 0;
    lastReport = now;
  }

  delay(16);
}

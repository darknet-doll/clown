// trigger_test — bench test: squeeze the bubble kit's trigger, the LED lights.
//
// No motor, no battery, no strip. Just the XIAO on USB, the kit's microswitch
// and one plain LED. Proves the trigger input before any of it goes into the pod.
//
// Trigger is on the same pin as clown_arm.ino, so that wiring carries over.
//
// Board:  Seeed XIAO ESP32-C3
// Core:   ESP32 Arduino core (Espressif)
//
// Tools -> USB CDC On Boot: Enabled, or the Serial Monitor stays blank.

constexpr uint8_t PIN_LED  = 10;  // silk D10, -> 330-470R -> LED long leg; short leg to GND
constexpr uint8_t PIN_TRIG = 3;   // silk D1,  microswitch NO; COM to GND

constexpr uint16_t DEBOUNCE_MS = 25;

bool     trigStable   = false;
bool     trigLastRaw  = false;
uint32_t trigChangeAt = 0;

static void readTrigger() {
  bool raw = (digitalRead(PIN_TRIG) == LOW);   // active low
  uint32_t now = millis();
  if (raw != trigLastRaw) {
    trigLastRaw  = raw;
    trigChangeAt = now;
  } else if (raw != trigStable && (now - trigChangeAt) >= DEBOUNCE_MS) {
    trigStable = raw;
    Serial.println(trigStable ? "trigger: PRESSED" : "trigger: released");
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_TRIG, INPUT_PULLUP);
  pinMode(PIN_LED, OUTPUT);

  // Boot check: three quick blinks. Proves the LED is wired the right way round
  // before you touch the trigger.
  for (int i = 0; i < 3; i++) {
    digitalWrite(PIN_LED, HIGH);
    delay(150);
    digitalWrite(PIN_LED, LOW);
    delay(150);
  }

  Serial.println("trigger_test ready — squeeze the trigger");
}

void loop() {
  readTrigger();
  digitalWrite(PIN_LED, trigStable ? HIGH : LOW);
  delay(5);
}

// pin_probe — hold D10 at a steady level so the data path can be traced with a
// meter, hop by hop.
//
// Starts HIGH. Type 1 or 0 in the Serial Monitor (then Enter) to set it high or
// low; anything else reprints the current state.
//
// Board:  Seeed XIAO ESP32-C3
//
// Tools -> USB CDC On Boot: Enabled, or the Serial Monitor stays blank.

constexpr uint8_t PIN_PROBE = 10;  // silk D10

bool level = HIGH;

static void apply() {
  digitalWrite(PIN_PROBE, level);
  Serial.println(level ? "D10 = HIGH (3.3 V)" : "D10 = LOW (0 V)");
}

void setup() {
  Serial.begin(115200);
  pinMode(PIN_PROBE, OUTPUT);
  delay(1000);   // give the Serial Monitor a moment to reconnect after reset
  apply();
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '1') { level = HIGH; apply(); }
    else if (c == '0') { level = LOW; apply(); }
    else if (c != '\n' && c != '\r') apply();
  }
}

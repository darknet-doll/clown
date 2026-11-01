// vsense_probe — the XIAO as a voltmeter on the cell, for when there's no meter.
//
// Reads VSENSE (GPIO2, silk D0): half of VBATT through R1/R2, so this is the
// cell voltage after SW1 and F1. Prints it twice a second. Run it on USB.
//
//   ~3.5-4.2 V  cell, J1, SW1, F1 all good -> fault is downstream (U1, CR2)
//   ~0 V        no cell at the board -> cell flat/tripped, J1, SW1 off, or F1
//
// Leaves the motor gate low and the strip alone.
//
// Board:  Seeed XIAO ESP32-C3
//
// Tools -> USB CDC On Boot: Enabled, or the Serial Monitor stays blank.

constexpr uint8_t PIN_VBAT  = 2;   // silk D0, divider midpoint
constexpr uint8_t PIN_MOTOR = 4;   // silk D2, held low

void setup() {
  pinMode(PIN_MOTOR, OUTPUT);
  digitalWrite(PIN_MOTOR, LOW);
  Serial.begin(115200);
  Serial.setTxTimeoutMs(0);
}

void loop() {
  // Average 16 reads; the divider is high impedance and C3 smooths it.
  uint32_t sum = 0;
  for (int i = 0; i < 16; i++) sum += analogReadMilliVolts(PIN_VBAT);
  uint32_t cellMv = sum / 16 * 2;   // undo the 100k/100k divider
  Serial.printf("[%lu ms] VBATT %lu.%02lu V\n", (unsigned long)millis(),
                (unsigned long)(cellMv / 1000), (unsigned long)(cellMv % 1000 / 10));
  delay(500);
}

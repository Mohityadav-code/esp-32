/*
 * ESP32 + MPU-6050 Fall Detector
 *
 * Wiring (matches your board):
 *   MPU-6050 VCC -> 3V3  (RIGHT side pin 1)
 *   MPU-6050 GND -> GND  (RIGHT side pin 2)
 *   MPU-6050 SDA -> GPIO21 (RIGHT side pin 11)
 *   MPU-6050 SCL -> GPIO22 (RIGHT side pin 14)
 *   MPU-6050 ADO -> GND (I2C address 0x68)
 *
 * Behavior:
 *   - Streams accelerometer (g) at 50 Hz
 *   - Detects free-fall (|a| < 0.35 g for >= 60 ms) followed by impact (|a| > 2.2 g) within 1.5 s
 *   - When detected, prints "FALL_DETECTED" and pauses events for 2 s cooldown
 */

#include <Wire.h>

static const uint8_t MPU_ADDR = 0x68; // ADO=GND

// Pins for ESP32 default I2C
static const int I2C_SDA_PIN = 21;
static const int I2C_SCL_PIN = 22;

// Fall detection thresholds
static const float FREE_FALL_G_THRESHOLD = 0.35f;   // g
static const uint32_t FREE_FALL_MIN_MS   = 60;      // min duration to qualify
static const float IMPACT_G_THRESHOLD    = 2.20f;   // g
static const uint32_t IMPACT_WINDOW_MS   = 1500;    // window after free-fall to look for impact
static const uint32_t EVENT_COOLDOWN_MS  = 2000;    // after a detection, ignore new ones for a bit

// Sampling
static const uint32_t SAMPLE_INTERVAL_MS = 20; // 50 Hz

// State
bool inFreeFall = false;
uint32_t freeFallStartMs = 0;
uint32_t lastEventMs = 0;

// Raw readings
int16_t accX = 0, accY = 0, accZ = 0;

bool writeRegister(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(value);
  return Wire.endTransmission() == 0;
}

bool readRegisters(uint8_t startReg, uint8_t count, uint8_t* buffer) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(startReg);
  if (Wire.endTransmission(false) != 0) return false;
  uint8_t received = Wire.requestFrom(MPU_ADDR, count, (uint8_t)true);
  for (uint8_t i = 0; i < received && i < count; i++) {
    buffer[i] = Wire.read();
  }
  return received == count;
}

bool initMPU() {
  // Wake up device
  if (!writeRegister(0x6B, 0x00)) return false; // PWR_MGMT_1: clear sleep
  delay(10);
  // Set accelerometer to +/- 2g (0x00)
  if (!writeRegister(0x1C, 0x00)) return false; // ACCEL_CONFIG
  // Optional: set sample rate / filter if desired
  return true;
}

bool readAccel() {
  uint8_t buf[6];
  if (!readRegisters(0x3B, 6, buf)) return false; // ACCEL_XOUT_H ... ACCEL_ZOUT_L
  accX = ((int16_t)buf[0] << 8) | buf[1];
  accY = ((int16_t)buf[2] << 8) | buf[3];
  accZ = ((int16_t)buf[4] << 8) | buf[5];
  return true;
}

float lsbToG(int16_t v) {
  // For +/- 2g: 16384 LSB per g
  return (float)v / 16384.0f;
}

void setup() {
  Serial.begin(115200);
  while (!Serial) { ; }

  Serial.println();
  Serial.println("====================================");
  Serial.println("ESP32 + MPU-6050 Fall Detector (115200)");
  Serial.println("====================================");

  Wire.begin(I2C_SDA_PIN, I2C_SCL_PIN);
  Serial.print("I2C init: SDA="); Serial.print(I2C_SDA_PIN);
  Serial.print(" SCL="); Serial.println(I2C_SCL_PIN);

  // Check presence
  Wire.beginTransmission(MPU_ADDR);
  int err = Wire.endTransmission();
  if (err == 0) {
    Serial.println("✓ MPU-6050 found at 0x68");
  } else {
    Serial.println("✗ MPU-6050 not responding at 0x68. Check wiring.");
  }

  if (!initMPU()) {
    Serial.println("✗ Failed to initialize MPU-6050 registers");
  } else {
    Serial.println("✓ MPU-6050 initialized");
  }

  Serial.println("Streaming accel at 50 Hz. Move the board to test.\n");
}

void loop() {
  static uint32_t lastSampleMs = 0;
  const uint32_t now = millis();
  if (now - lastSampleMs < SAMPLE_INTERVAL_MS) return;
  lastSampleMs = now;

  if (!readAccel()) {
    Serial.println("E: Failed to read accelerometer");
    return;
  }

  const float ax = lsbToG(accX);
  const float ay = lsbToG(accY);
  const float az = lsbToG(accZ);
  const float amag = sqrtf(ax*ax + ay*ay + az*az);

  // Print telemetry occasionally
  static uint32_t lastPrintMs = 0;
  if (now - lastPrintMs >= 200) {
    lastPrintMs = now;
    Serial.print("ACC g: ");
    Serial.print(ax, 2); Serial.print(", ");
    Serial.print(ay, 2); Serial.print(", ");
    Serial.print(az, 2); Serial.print(" |a|=");
    Serial.println(amag, 2);
  }

  // Cooldown handling
  if (now - lastEventMs < EVENT_COOLDOWN_MS) {
    inFreeFall = false;
    return;
  }

  // Free-fall detection (magnitude significantly below 1 g)
  if (!inFreeFall) {
    if (amag < FREE_FALL_G_THRESHOLD) {
      inFreeFall = true;
      freeFallStartMs = now;
      // Optional debug
      Serial.println("-- free-fall start --");
    }
  } else {
    // If we have been in free-fall long enough, look for impact window
    if (amag > IMPACT_G_THRESHOLD && (now - freeFallStartMs) <= IMPACT_WINDOW_MS && (now - freeFallStartMs) >= FREE_FALL_MIN_MS) {
      Serial.println("FALL_DETECTED");
      lastEventMs = now;
      inFreeFall = false;
    }
    // Cancel free-fall if it lasts too long without impact
    if (now - freeFallStartMs > IMPACT_WINDOW_MS) {
      inFreeFall = false;
      Serial.println("-- free-fall timeout --");
    }
    // Also cancel if magnitude returns close to 1 g quickly
    if (amag > 0.8f && (now - freeFallStartMs) > FREE_FALL_MIN_MS) {
      inFreeFall = false;
    }
  }
} 

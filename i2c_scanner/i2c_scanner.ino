/*
 * I2C Scanner for ESP32
 * This sketch scans for I2C devices and reports their addresses
 * MPU-6050 should appear at address 0x68 if connected properly
 */

#include <Wire.h>

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }
  
  Serial.println("\n\n=================================");
  Serial.println("    ESP32 I2C Scanner");
  Serial.println("=================================");
  Serial.println("Checking MPU-6050 Connection...\n");
  
  // Initialize I2C with SDA=21, SCL=22
  Wire.begin(21, 22);
  Serial.println("I2C initialized on pins:");
  Serial.println("  SDA = GPIO 21");
  Serial.println("  SCL = GPIO 22");
  Serial.println("\nScanning for I2C devices...\n");
  
  delay(1000);
  
  scanI2C();
  
  // Specifically check for MPU-6050
  checkMPU6050();
}

void loop() {
  Serial.println("\n--- Rescanning I2C bus ---");
  scanI2C();
  checkMPU6050();
  delay(5000); // Scan every 5 seconds
}

void scanI2C() {
  byte error, address;
  int deviceCount = 0;
  
  Serial.println("Scanning I2C addresses 0x00 to 0x7F...");
  
  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();
    
    if (error == 0) {
      Serial.print("  ✓ Device found at address 0x");
      if (address < 16) Serial.print("0");
      Serial.print(address, HEX);
      
      // Identify known devices
      if (address == 0x68) {
        Serial.print(" → MPU-6050 (Accelerometer/Gyroscope)");
      } else if (address == 0x69) {
        Serial.print(" → MPU-6050 (Alternative address)");
      } else if (address == 0x76 || address == 0x77) {
        Serial.print(" → Possible BMP280/BME280 sensor");
      }
      
      Serial.println();
      deviceCount++;
    }
    else if (error == 4) {
      Serial.print("  ✗ Unknown error at address 0x");
      if (address < 16) Serial.print("0");
      Serial.println(address, HEX);
    }
  }
  
  if (deviceCount == 0) {
    Serial.println("\n⚠️  No I2C devices found!");
    Serial.println("\nTroubleshooting:");
    Serial.println("1. Check wiring connections:");
    Serial.println("   - VCC to 3.3V");
    Serial.println("   - GND to GND");
    Serial.println("   - SDA to GPIO 21");
    Serial.println("   - SCL to GPIO 22");
    Serial.println("2. Ensure ADO pin is connected to GND");
    Serial.println("3. Check that jumper wires are firmly connected");
  } else {
    Serial.print("\n✓ Total devices found: ");
    Serial.println(deviceCount);
  }
}

void checkMPU6050() {
  Serial.println("\n--- MPU-6050 Status Check ---");
  
  // Check address 0x68 (ADO=LOW)
  Wire.beginTransmission(0x68);
  byte error68 = Wire.endTransmission();
  
  // Check address 0x69 (ADO=HIGH)
  Wire.beginTransmission(0x69);
  byte error69 = Wire.endTransmission();
  
  if (error68 == 0) {
    Serial.println("✅ MPU-6050 DETECTED at address 0x68!");
    Serial.println("   Connection is GOOD!");
    Serial.println("   ADO pin is connected to GND (correct)");
    
    // Try to read WHO_AM_I register
    Wire.beginTransmission(0x68);
    Wire.write(0x75); // WHO_AM_I register
    Wire.endTransmission(false);
    Wire.requestFrom(0x68, 1, true);
    if (Wire.available()) {
      byte whoami = Wire.read();
      Serial.print("   WHO_AM_I register value: 0x");
      Serial.println(whoami, HEX);
      if (whoami == 0x68) {
        Serial.println("   ✓ MPU-6050 identity confirmed!");
      }
    }
  } else if (error69 == 0) {
    Serial.println("⚠️  MPU-6050 found at address 0x69");
    Serial.println("   ADO pin is connected to VCC (not GND)");
    Serial.println("   Recommendation: Connect ADO to GND for address 0x68");
  } else {
    Serial.println("❌ MPU-6050 NOT DETECTED!");
    Serial.println("\nPlease check:");
    Serial.println("□ VCC (MPU) → 3.3V (ESP32 right side, pin 1)");
    Serial.println("□ GND (MPU) → GND (ESP32 right side, pin 2)");
    Serial.println("□ SCL (MPU) → GPIO 22 (ESP32 right side, pin 14)");
    Serial.println("□ SDA (MPU) → GPIO 21 (ESP32 right side, pin 11)");
    Serial.println("□ ADO (MPU) → GND");
    Serial.println("\nCommon issues:");
    Serial.println("• Loose jumper wires");
    Serial.println("• Wires in wrong pins");
    Serial.println("• Bad/broken jumper wires");
    Serial.println("• MPU-6050 not powered (check LED if present)");
  }
} 

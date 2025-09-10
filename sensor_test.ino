/*
 * ESP32 Sensor Test Program
 * Tests MPU-6050 and IR Flame Sensor
 * 
 * Wiring:
 * MPU-6050: SDA->GPIO21, SCL->GPIO22, VCC->3.3V, GND->GND
 * IR Sensor: D0->GPIO34, A0->GPIO35, VCC->3.3V, GND->GND
 */

#include <Wire.h>

// MPU-6050 I2C address
const int MPU_ADDR = 0x68;

// IR Sensor pins
const int IR_DIGITAL_PIN = 34;  // Digital output from IR sensor
const int IR_ANALOG_PIN = 35;   // Analog output from IR sensor

// MPU-6050 variables
int16_t accelerometer_x, accelerometer_y, accelerometer_z;
int16_t gyro_x, gyro_y, gyro_z;
int16_t temperature;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for serial port to connect
  }
  
  Serial.println("\n===================================");
  Serial.println("ESP32 Sensor Test Program Starting");
  Serial.println("===================================\n");
  
  // Initialize I2C for MPU-6050
  Wire.begin(21, 22); // SDA, SCL
  
  // Initialize MPU-6050
  Serial.println("Initializing MPU-6050...");
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B); // PWR_MGMT_1 register
  Wire.write(0);    // Wake up MPU-6050
  Wire.endTransmission(true);
  
  // Check if MPU-6050 is connected
  Wire.beginTransmission(MPU_ADDR);
  int error = Wire.endTransmission();
  
  if (error == 0) {
    Serial.println("✓ MPU-6050 found at address 0x68");
  } else {
    Serial.println("✗ MPU-6050 not found! Check wiring.");
    Serial.print("  I2C Error code: ");
    Serial.println(error);
  }
  
  // Initialize IR sensor pins
  pinMode(IR_DIGITAL_PIN, INPUT);
  pinMode(IR_ANALOG_PIN, INPUT);
  
  Serial.println("✓ IR Flame Sensor pins configured");
  Serial.println("\nStarting sensor readings...\n");
  delay(1000);
}

void loop() {
  Serial.println("----------------------------------------");
  
  // Read MPU-6050 data
  readMPU6050();
  
  // Read IR sensor data
  readIRSensor();
  
  Serial.println("----------------------------------------\n");
  
  delay(1000); // Update every second
}

void readMPU6050() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B); // Starting register for accelerometer readings
  Wire.endTransmission(false);
  
  Wire.requestFrom(MPU_ADDR, 14, true); // Request 14 bytes
  
  if (Wire.available() >= 14) {
    accelerometer_x = Wire.read() << 8 | Wire.read();
    accelerometer_y = Wire.read() << 8 | Wire.read();
    accelerometer_z = Wire.read() << 8 | Wire.read();
    temperature = Wire.read() << 8 | Wire.read();
    gyro_x = Wire.read() << 8 | Wire.read();
    gyro_y = Wire.read() << 8 | Wire.read();
    gyro_z = Wire.read() << 8 | Wire.read();
    
    Serial.println("MPU-6050 Readings:");
    
    // Convert accelerometer values to g (gravity)
    float ax = accelerometer_x / 16384.0;
    float ay = accelerometer_y / 16384.0;
    float az = accelerometer_z / 16384.0;
    
    Serial.print("  Accel (g): X=");
    Serial.print(ax, 2);
    Serial.print(" Y=");
    Serial.print(ay, 2);
    Serial.print(" Z=");
    Serial.println(az, 2);
    
    // Convert gyroscope values to degrees/second
    float gx = gyro_x / 131.0;
    float gy = gyro_y / 131.0;
    float gz = gyro_z / 131.0;
    
    Serial.print("  Gyro (°/s): X=");
    Serial.print(gx, 1);
    Serial.print(" Y=");
    Serial.print(gy, 1);
    Serial.print(" Z=");
    Serial.println(gz, 1);
    
    // Convert temperature to Celsius
    float temp_celsius = (temperature / 340.0) + 36.53;
    Serial.print("  Temperature: ");
    Serial.print(temp_celsius, 1);
    Serial.println(" °C");
    
    // Calculate tilt angles
    float pitch = atan2(ax, sqrt(ay * ay + az * az)) * 180.0 / PI;
    float roll = atan2(ay, sqrt(ax * ax + az * az)) * 180.0 / PI;
    
    Serial.print("  Tilt: Pitch=");
    Serial.print(pitch, 1);
    Serial.print("° Roll=");
    Serial.print(roll, 1);
    Serial.println("°");
    
  } else {
    Serial.println("MPU-6050: No data available");
  }
}

void readIRSensor() {
  // Read digital output (HIGH = no flame, LOW = flame detected)
  int digitalValue = digitalRead(IR_DIGITAL_PIN);
  
  // Read analog output (lower value = stronger flame)
  int analogValue = analogRead(IR_ANALOG_PIN);
  
  Serial.println("\nIR Flame Sensor Readings:");
  
  Serial.print("  Digital: ");
  if (digitalValue == LOW) {
    Serial.println("🔥 FLAME DETECTED!");
  } else {
    Serial.println("No flame");
  }
  
  Serial.print("  Analog: ");
  Serial.print(analogValue);
  Serial.print(" (");
  
  // Convert to percentage (inverse - lower value means stronger flame)
  float intensity = 100.0 - (analogValue / 4095.0 * 100.0);
  Serial.print(intensity, 1);
  Serial.println("% intensity)");
  
  // Flame intensity interpretation
  Serial.print("  Status: ");
  if (analogValue < 500) {
    Serial.println("⚠️  Strong flame/heat source nearby!");
  } else if (analogValue < 1500) {
    Serial.println("Moderate flame/heat detected");
  } else if (analogValue < 3000) {
    Serial.println("Weak flame/heat detected");
  } else {
    Serial.println("No significant heat source");
  }
} 

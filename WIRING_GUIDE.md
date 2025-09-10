# ESP32 Sensor Connections Guide

## Components
- ESP32 DevKit V1 (Type-C)
- MPU-6050 (Accelerometer/Gyroscope)
- IR Flame Sensor Module

## Pin Connections

### MPU-6050 Connections (I2C)
```
MPU-6050    →    ESP32
-----------------------
VCC         →    3.3V
GND         →    GND
SCL         →    GPIO 22 (I2C SCL)
SDA         →    GPIO 21 (I2C SDA)
XCL         →    Not connected
XDA         →    Not connected
ADO         →    GND (sets I2C address to 0x68)
INT         →    Not connected (optional, can connect to any GPIO)
```

### IR Flame Sensor Connections
```
IR Sensor   →    ESP32
-----------------------
VCC         →    3.3V
GND         →    GND
D0          →    GPIO 34 (Digital output)
A0          →    GPIO 35 (Analog output - optional)
```

## Important Notes

1. **Power Supply**: Both sensors can work with 3.3V from ESP32. The MPU-6050 has an onboard voltage regulator, so it can also accept 5V, but 3.3V is recommended for ESP32.

2. **I2C Pull-up Resistors**: The MPU-6050 module usually has built-in pull-up resistors on SDA and SCL lines.

3. **IR Sensor**: 
   - D0 provides digital output (HIGH/LOW based on threshold)
   - A0 provides analog output for precise flame intensity reading
   - The potentiometer on the sensor adjusts the detection threshold

4. **GPIO Selection**:
   - GPIO 34 and 35 are input-only pins (perfect for sensors)
   - GPIO 21 and 22 are the default I2C pins on ESP32

## Pin Layout Reference

### ESP32 DevKit V1 Pinout (30 pins each side):

Left side (top to bottom):
- 3V3, EN, VP(36), VN(39), 34, 35, 32, 33, 25, 26, 27, 14, 12, GND, 13

Right side (top to bottom):  
- VIN, GND, 23, 22, TX0, RX0, 21, GND, 19, 18, 5, 17, 16, 4, 0, 2, 15

## Testing
After wiring, use the provided test code to verify:
1. MPU-6050 I2C communication (address 0x68)
2. IR sensor digital readings
3. IR sensor analog readings (if A0 is connected) 

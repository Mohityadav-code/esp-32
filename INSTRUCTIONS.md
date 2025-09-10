# ESP32 Sensor Project - Setup Instructions

## Hardware Setup

### Required Components
- ESP32 DevKit V1 (Type-C)
- MPU-6050 Accelerometer/Gyroscope Module
- IR Flame Sensor Module
- Jumper wires
- Breadboard (optional but recommended)

### Wiring Instructions

Follow the connections in `WIRING_GUIDE.md`:

1. **MPU-6050 (I2C Connection)**:
   - VCC → 3.3V
   - GND → GND
   - SCL → GPIO 22
   - SDA → GPIO 21
   - ADO → GND (sets address to 0x68)

2. **IR Flame Sensor**:
   - VCC → 3.3V
   - GND → GND
   - D0 → GPIO 34 (digital output)
   - A0 → GPIO 35 (analog output - optional but recommended)

## Software Setup

### Option 1: Using Arduino IDE (Recommended for Beginners)

1. **Install Arduino IDE**:
   - Download from: https://www.arduino.cc/en/software
   - Install for your operating system

2. **Add ESP32 Board Support**:
   - Open Arduino IDE
   - Go to `Arduino IDE → Preferences` (Mac) or `File → Preferences` (Windows/Linux)
   - Add this URL to "Additional Board Manager URLs":
     ```
     https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
     ```
   - Click OK

3. **Install ESP32 Board Package**:
   - Go to `Tools → Board → Board Manager`
   - Search for "esp32"
   - Install "esp32 by Espressif Systems"

4. **Select Your Board**:
   - Go to `Tools → Board → ESP32 Arduino`
   - Select "ESP32 Dev Module"

5. **Configure Settings**:
   - Port: `/dev/cu.usbserial-0001` (Mac) or appropriate COM port
   - Upload Speed: 115200
   - Flash Frequency: 80MHz
   - Flash Mode: QIO
   - Flash Size: 4MB (32Mb)
   - Partition Scheme: Default 4MB with spiffs

6. **Upload the Code**:
   - Open `sensor_test.ino`
   - Click the Upload button (→ arrow)
   - Wait for upload to complete

7. **Monitor Output**:
   - Open Serial Monitor: `Tools → Serial Monitor`
   - Set baud rate to 115200
   - You should see sensor readings

### Option 2: Using Command Line (Advanced)

1. **Install Arduino CLI**:
   ```bash
   brew install arduino-cli
   ```

2. **Configure Arduino CLI**:
   ```bash
   arduino-cli config init
   arduino-cli config add board_manager.additional_urls https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   arduino-cli core update-index
   arduino-cli core install esp32:esp32
   ```

3. **Compile the sketch**:
   ```bash
   arduino-cli compile --fqbn esp32:esp32:esp32 sensor_test.ino
   ```

4. **Upload to ESP32**:
   ```bash
   arduino-cli upload -p /dev/cu.usbserial-0001 --fqbn esp32:esp32:esp32 sensor_test.ino
   ```

5. **Monitor serial output**:
   ```bash
   screen /dev/cu.usbserial-0001 115200
   ```
   (Press `Ctrl+A` then `K` to exit screen)

## Testing the Sensors

Once uploaded, the program will:

1. **Initialize both sensors** and report their status
2. **Display MPU-6050 data** every second:
   - Accelerometer readings (X, Y, Z in g-force)
   - Gyroscope readings (X, Y, Z in degrees/second)
   - Temperature in Celsius
   - Calculated pitch and roll angles

3. **Display IR Sensor data**:
   - Digital output (flame detected or not)
   - Analog value (0-4095)
   - Flame intensity percentage
   - Status interpretation

## Troubleshooting

### Common Issues:

1. **"MPU-6050 not found" error**:
   - Check I2C connections (SDA to GPIO21, SCL to GPIO22)
   - Ensure ADO pin is connected to GND
   - Check power connections (3.3V and GND)

2. **No IR sensor readings**:
   - Verify GPIO 34 and 35 connections
   - Adjust the potentiometer on the IR sensor module
   - Test with a lighter or candle (safely!)

3. **Upload fails**:
   - Hold the BOOT button while uploading starts
   - Check USB cable (must be data cable, not charge-only)
   - Try different upload speed (921600 or 115200)

4. **Serial monitor shows garbage**:
   - Set correct baud rate (115200)
   - Reset ESP32 after opening serial monitor

## Safety Notes

⚠️ **When testing the IR flame sensor**:
- Use caution with open flames
- Keep flammable materials away
- Test in a well-ventilated area
- Have fire safety equipment nearby
- The sensor can also detect other heat sources (soldering iron, hot air, etc.)

## Next Steps

Once both sensors are working:
1. Experiment with sensor fusion (combining MPU-6050 and IR data)
2. Add WiFi connectivity to send data to a server
3. Create a web interface to visualize sensor data
4. Build a fire detection and orientation monitoring system
5. Add SD card logging for data recording

## Useful Resources

- [ESP32 Pinout Reference](https://randomnerdtutorials.com/esp32-pinout-reference-gpios/)
- [MPU-6050 Datasheet](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-6000-Datasheet1.pdf)
- [I2C Scanner Code](https://playground.arduino.cc/Main/I2cScanner/) - To verify I2C devices
- [ESP32 Arduino Core Documentation](https://docs.espressif.com/projects/arduino-esp32/en/latest/) 

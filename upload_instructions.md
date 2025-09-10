# Quick Test Instructions - Check MPU-6050 Connection

## Upload the I2C Scanner

I've created an **I2C Scanner** program (`i2c_scanner.ino`) that will verify if your MPU-6050 is properly connected.

### Using Arduino IDE:

1. **Open Arduino IDE**

2. **Open the I2C Scanner**:
   - File → Open → Navigate to `/Users/mohit/Desktop/esp-32/i2c_scanner.ino`

3. **Select Board and Port**:
   - Tools → Board → ESP32 Arduino → "ESP32 Dev Module"
   - Tools → Port → `/dev/cu.usbserial-0001`

4. **Upload the Code**:
   - Click the Upload button (→ arrow)
   - Wait for "Done uploading"

5. **Open Serial Monitor**:
   - Tools → Serial Monitor
   - Set baud rate to **115200**
   - You should see the scanning results

## What You Should See:

### ✅ If MPU-6050 is Connected Properly:
```
=================================
    ESP32 I2C Scanner
=================================
Checking MPU-6050 Connection...

I2C initialized on pins:
  SDA = GPIO 21
  SCL = GPIO 22

Scanning for I2C devices...

  ✓ Device found at address 0x68 → MPU-6050 (Accelerometer/Gyroscope)

✓ Total devices found: 1

--- MPU-6050 Status Check ---
✅ MPU-6050 DETECTED at address 0x68!
   Connection is GOOD!
   ADO pin is connected to GND (correct)
```

### ❌ If MPU-6050 is NOT Connected Properly:
```
⚠️  No I2C devices found!

Troubleshooting:
1. Check wiring connections...
```

## Quick Alternative Test

If you prefer not to upload new code right now, run this Python script to see if there's any serial output:

```bash
python3 quick_test.py
```

This will show any data the ESP32 is currently sending.

## Troubleshooting Checklist

If the MPU-6050 is not detected:

- [ ] **Power**: Is VCC connected to 3.3V (right side, pin 1)?
- [ ] **Ground**: Is GND connected to GND (right side, pin 2)?
- [ ] **I2C Clock**: Is SCL connected to GPIO 22 (right side, pin 14)?
- [ ] **I2C Data**: Is SDA connected to GPIO 21 (right side, pin 11)?
- [ ] **Address**: Is ADO connected to GND?
- [ ] **Connections**: Are all wires firmly pushed into the breadboard/pins?
- [ ] **Wires**: Try different jumper wires (they can be faulty)

Let me know what the scanner shows! 

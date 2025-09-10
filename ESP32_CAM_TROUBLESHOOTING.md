# ESP32-CAM Troubleshooting Guide

## Error: Camera probe failed with error 0x106 (ESP_ERR_NOT_SUPPORTED)

This error means the ESP32 cannot communicate with the camera sensor. Here's how to fix it:

## Quick Fix Steps (Try These First)

### 1. **Reconnect Camera Ribbon Cable** (Fixes 80% of cases)
**This is the most common cause of the error!**

1. **Power off the ESP32-CAM completely** (unplug USB)
2. Locate the camera connector (black rectangular connector)
3. **Carefully lift the black latch** (it flips up, don't force it)
4. **Remove the ribbon cable completely**
5. **Reinsert the cable ensuring:**
   - Cable is **fully inserted** (golden contacts barely visible)
   - **Blue tape faces AWAY from the board**
   - Cable is **straight, not angled**
   - No dust or debris on contacts
6. **Press the black latch down firmly**
7. Check the camera module isn't loose on the other end

### 2. **Power Supply Issues**
ESP32-CAM needs stable power, especially during camera initialization.

- Use a **quality USB cable** (not a charge-only cable)
- Try a different USB port
- Use a **powered USB hub** if available
- Or connect external 5V power supply (at least 5V/500mA)
- Add a 100-470µF capacitor between 5V and GND if you have one

### 3. **Upload the Diagnostic Sketch**
Upload `camera_diagnostic.ino` to get detailed error information:
```bash
# This sketch will:
# - Test different clock frequencies
# - Disable brownout protection
# - Provide detailed error messages
# - Test the LED flash
```

### 4. **Test Different Camera Models**
Upload `camera_model_tester.ino` to automatically detect your board:
```bash
# This sketch will:
# - Test 6 different camera configurations
# - Automatically identify your board model
# - Provide the correct configuration to use
```

## Detailed Solutions

### Solution A: Manual Pin Configuration Check

Your current configuration (AI_THINKER) uses these pins:
```
PWDN    → GPIO 32
RESET   → Not connected (-1)
XCLK    → GPIO 0
SIOD    → GPIO 26
SIOC    → GPIO 27
Y9-Y2   → GPIO 35,34,39,36,21,19,18,5
VSYNC   → GPIO 25
HREF    → GPIO 23
PCLK    → GPIO 22
LED     → GPIO 4
```

If this doesn't work, you might have a different board model.

### Solution B: Try Lower Clock Frequency

In your `esp32_cam_webserver.ino`, change line 42:
```cpp
// Change from:
config.xclk_freq_hz = 20000000;
// To:
config.xclk_freq_hz = 10000000;  // or even 5000000
```

### Solution C: Disable Brownout Detector

Add this at the beginning of setup():
```cpp
#include "soc/soc.h"
#include "soc/rtc_cntl_reg.h"

void setup() {
  WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // disable brownout
  // rest of your setup code...
}
```

### Solution D: Power Cycle the Camera

Add this before camera initialization:
```cpp
// Power cycle the camera module
pinMode(32, OUTPUT);  // PWDN pin
digitalWrite(32, HIGH);
delay(500);
digitalWrite(32, LOW);
delay(500);
```

## Board Identification

### How to identify your ESP32-CAM board:

1. **Look at the board label:**
   - "AI-Thinker" → Most common ESP32-CAM
   - "M5Stack" → M5Stack camera variants
   - "TTGO" → TTGO T-Journal

2. **Check the antenna:**
   - External antenna connector → Usually AI-Thinker
   - PCB antenna only → Could be various models

3. **Count the pins:**
   - Standard ESP32-CAM has 16 pins on the bottom

## If Nothing Works

### Hardware Issues to Check:

1. **Camera Module:**
   - The camera sensor itself might be faulty
   - Try gently pressing on the camera module while powering on
   - Check for any visible damage on the lens or module

2. **Board Damage:**
   - Check for burnt components
   - Look for broken traces near the camera connector
   - Verify all solder joints look good

3. **Wrong Board Type:**
   - You might have received a different ESP32-CAM variant
   - Some clones use different pin configurations

### Last Resort Options:

1. **Try the Examples in Arduino IDE:**
   - File → Examples → ESP32 → Camera → CameraWebServer
   - Select your board: "AI Thinker ESP32-CAM"
   - This uses the official Espressif configuration

2. **Flash MicroPython:**
   - Sometimes helps identify if it's a hardware vs software issue
   - Use the ESP32_GENERIC firmware you have

3. **External Power:**
   - Connect 5V directly to the 5V pin
   - Connect GND to GND pin
   - This bypasses any USB power issues

## Common Error Codes

- `0x106 (ESP_ERR_NOT_SUPPORTED)` - Camera not detected/wrong model
- `0x103 (ESP_ERR_INVALID_STATE)` - Camera already initialized
- `0x105 (ESP_ERR_NOT_FOUND)` - Camera hardware not found
- `0x101 (ESP_ERR_NO_MEM)` - Out of memory

## Need More Help?

If you're still having issues after trying all these solutions:
1. Note which diagnostic sketch outputs you get
2. Check if the LED flash (GPIO 4) blinks when you upload a simple blink sketch
3. Measure voltage between 5V and GND (should be 4.5-5.5V)
4. Try with a different camera module if available 

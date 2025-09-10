# ESP32-CAM Upload Fix Guide

## Quick Fix (90% Success Rate)

### If Using ESP32-CAM-MB Board:

1. **Check Physical Connection:**
   - ESP32-CAM fully seated on MB board
   - USB cable connected to MB board (not ESP32-CAM directly)
   - Using a data USB cable (not charge-only)

2. **Arduino IDE Settings:**
   ```
   Board: "AI Thinker ESP32-CAM"
   Upload Speed: 115200 (IMPORTANT - change from 921600)
   CPU Frequency: 240MHz (WiFi/BT)
   Flash Frequency: 40MHz
   Flash Mode: DIO
   Partition Scheme: Huge APP (3MB No OTA/1MB SPIFFS)
   Port: /dev/cu.usbserial-230
   ```

3. **Upload Procedure:**
   - Click Upload in Arduino IDE
   - When you see "Connecting.........."
   - Press and release RST button on ESP32-CAM
   - Try different timings if first attempt fails

### If MB Board Isn't Working:

**You need to jumper GPIO 0 to GND for programming:**

1. **Find these pins on ESP32-CAM:**
   - GPIO 0 (labeled IO0)
   - GND (any GND pin)

2. **Use a jumper wire or even a paperclip:**
   - Connect GPIO 0 to GND
   - Keep connected during upload
   - Remove after upload completes

3. **Upload sequence:**
   - Connect GPIO 0 to GND
   - Press RST button
   - Start upload in Arduino IDE
   - After upload succeeds, remove GPIO 0 jumper
   - Press RST to run program

## Alternative Solutions:

### Solution A: Terminal Upload
```bash
# Lower baud rate often works better
esptool.py --chip esp32 --port /dev/cu.usbserial-230 --baud 115200 write_flash 0x10000 your_sketch.bin
```

### Solution B: Check USB Driver
```bash
# Check if port is accessible
ls -la /dev/cu.usbserial-230
# Should show the device

# Check who's using the port
lsof | grep usbserial
# Should be empty or show Arduino IDE
```

### Solution C: Reset USB Serial
1. Unplug ESP32-CAM
2. Close Arduino IDE completely
3. Open Terminal and run:
   ```bash
   sudo killall -9 com.apple.AMPDeviceDiscoveryAgent
   ```
4. Plug ESP32-CAM back in
5. Open Arduino IDE and try again

## Still Not Working?

### Hardware Check:
1. **Voltage:** Measure 5V and 3.3V pins with multimeter
2. **Serial Chip:** The MB board should have a CH340 or CP2102 chip
3. **LED Indicators:** Some MB boards have TX/RX LEDs that should blink during upload

### Last Resort:
1. Try a different USB cable (many are charge-only)
2. Try a different USB port or computer
3. The MB board's serial chip might be faulty

## Success Indicators:
- You'll see: "Writing at 0x00010000... (10%)"
- Progress percentage will increase
- Ends with "Hard resetting via RTS pin..."

## After Successful Upload:
1. Remove any GPIO 0 to GND connection
2. Press RST button
3. Open Serial Monitor (115200 baud)
4. You should see your program output 

# ESP32-CAM Programming Mode Fix

## You're Almost There!
Your ESP32-CAM is working (we can see serial output), but it's not entering programming mode.

## Quick Fix Steps:

### Option A: Use the IO0 Button (If Available)
```
1. Locate the small "IO0" button on ESP32-CAM (near RST button)
2. Hold IO0 button → Press RST → Release RST → Release IO0
3. Upload your sketch immediately
```

### Option B: Jumper Wire Method
```
ESP32-CAM Pin Layout (Bottom of board):
[5V] [GND] [IO12] [IO13] [IO15] [IO14] [IO2] [IO4]
[3V3] [IO16/U2RXD] [IO0] [GND] [VCC] [U0TXD] [U0RXD] [GND]
                     ↑      ↑
                  Connect these two with jumper wire
```

**Steps:**
1. Connect IO0 to GND with a jumper wire (or paperclip)
2. Press and release RST button
3. Start upload in Arduino IDE
4. When upload starts (you'll see percentages), remove jumper
5. After upload completes, press RST to run

### Option C: Timing Method (No Hardware Changes)
1. In Arduino IDE: Set **Upload Speed to 115200**
2. Click Upload
3. Watch for "Connecting........"
4. At the EXACT moment dots appear, press and HOLD RST
5. Hold for 1 second, then release
6. May take a few tries to get timing right

## Arduino IDE Settings (IMPORTANT):
```
Tools Menu:
- Board: "AI Thinker ESP32-CAM"
- Upload Speed: 115200 (NOT 921600!)
- Flash Mode: DIO
- Flash Frequency: 40MHz
- Port: /dev/cu.usbserial-230
```

## Verification:
When it's working, you'll see:
```
Connecting........
Chip is ESP32-D0WD (revision 1)
Writing at 0x00010000... (10%)
Writing at 0x00014000... (20%)
... etc ...
```

## Common Issues:
- **"No serial data received"** = Not in programming mode
- **Dots keep going** = Try the RST button timing again
- **Port busy** = Close Serial Monitor first

## After Successful Upload:
1. Remove any IO0-GND connection
2. Press RST button
3. Open Serial Monitor (115200 baud)
4. You should see your program output 

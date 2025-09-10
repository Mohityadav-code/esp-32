# Arduino IDE Installation Guide for Mac

## 🚀 Quick Install Steps

### Method 1: Download from Website (Easiest)

1. **Go to Arduino website**:
   https://www.arduino.cc/en/software

2. **Download for macOS**:
   - Click "macOS Intel" or "macOS Apple Silicon" (for M1/M2 Macs)
   - Choose "JUST DOWNLOAD" (free option)

3. **Install**:
   - Open the downloaded .dmg file
   - Drag Arduino IDE to Applications folder
   - Open Arduino IDE from Applications

### Method 2: Using Homebrew (If you have it)

```bash
brew install --cask arduino-ide
```

## 📋 After Installation - Setup for ESP32

1. **Open Arduino IDE**

2. **Add ESP32 Support**:
   - Arduino IDE → Settings (or Preferences)
   - Find "Additional Board Manager URLs"
   - Add this URL:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
   - Click OK

3. **Install ESP32 Board**:
   - Tools → Board → Board Manager
   - Search: "esp32"
   - Install: "esp32 by Espressif Systems"
   - Wait for installation (may take 2-3 minutes)

4. **Select ESP32 Board**:
   - Tools → Board → ESP32 Arduino → ESP32 Dev Module

5. **Select Port**:
   - Tools → Port → /dev/cu.usbserial-0001

## ✅ Now You're Ready!

Open any `.ino` file by:
- Double-clicking the file
- Or File → Open in Arduino IDE

## 🌐 Alternative: Arduino Web Editor

If you don't want to install software:

1. Go to: https://create.arduino.cc/editor
2. Create a free account
3. Install browser plugin
4. Upload the .ino code

Note: Web editor requires plugin installation and account creation. 

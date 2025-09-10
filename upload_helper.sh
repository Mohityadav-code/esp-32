#!/bin/bash

echo "ESP32-CAM Upload Helper"
echo "======================="
echo ""
echo "This script will help upload code to your ESP32-CAM"
echo ""
echo "IMPORTANT: When you see 'Connecting....' appear:"
echo "1. Press and HOLD the RST button on the ESP32-CAM"
echo "2. Release it after 1-2 seconds"
echo "3. The upload should start"
echo ""
echo "Press Enter when ready to start upload..."
read

# Try with lower baud rate first
echo "Attempting upload at 115200 baud..."
esptool.py --chip esp32 --port /dev/cu.usbserial-230 --baud 115200 \
  --before default_reset --after hard_reset \
  write_flash -z --flash_mode dio --flash_freq 40m --flash_size detect \
  0x1000 ~/.arduino15/packages/esp32/hardware/esp32/*/tools/sdk/bin/bootloader_dio_40m.bin \
  0x8000 ~/.arduino15/packages/esp32/hardware/esp32/*/tools/partitions/default.bin \
  0x10000 /var/folders/*/T/arduino_build_*/camera_diagnostic.ino.bin

if [ $? -ne 0 ]; then
  echo ""
  echo "Upload failed. Trying alternative method..."
  echo "Please try the following:"
  echo "1. Unplug the USB cable"
  echo "2. Connect GPIO 0 to GND (if not using MB board)"
  echo "3. Plug USB back in"
  echo "4. Try uploading from Arduino IDE"
fi 

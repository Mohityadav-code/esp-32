#!/usr/bin/env python3
"""
ESP32-CAM Upload & Boot Monitor
Specially designed for ESP32-CAM with MB Base Board
"""

import serial
import time
import re

PORT = '/dev/cu.usbserial-230'
BAUD = 115200

def highlight_important(text):
    """Highlight important messages"""
    # WiFi and IP patterns
    if re.search(r'\d+\.\d+\.\d+\.\d+', text):
        return f"🌐 >>> {text} <<<"
    elif "WiFi connected" in text:
        return f"✅ {text}"
    elif "Camera Ready" in text or "Camera init" in text:
        return f"📷 {text}"
    elif "error" in text.lower() or "fail" in text.lower():
        return f"❌ {text}"
    elif "Connecting" in text or "." == text.strip():
        return f"⏳ {text}"
    elif "ESP32-CAM" in text:
        return f"🎯 {text}"
    else:
        return text

print("=" * 60)
print("📷 ESP32-CAM Monitor (with MB Base Board)")
print("=" * 60)
print(f"Port: {PORT}")
print(f"Baud: {BAUD}")
print("-" * 60)

print("\n📝 INSTRUCTIONS:")
print("1. Upload your code from Arduino IDE")
print("2. This monitor will show the boot process")
print("3. Look for the IP address after WiFi connects")
print("4. Press Ctrl+C to exit\n")
print("-" * 60)

try:
    ser = serial.Serial(PORT, BAUD, timeout=0.1)
    print("✅ Connected to ESP32-CAM\n")
    print("Waiting for data... (Press RESET on ESP32-CAM if needed)\n")
    
    ser.reset_input_buffer()
    
    ip_address = None
    wifi_connected = False
    camera_ready = False
    
    while True:
        if ser.in_waiting:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line:
                    # Display with highlighting
                    print(highlight_important(line))
                    
                    # Extract IP address
                    ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if ip_match and "192.168" in ip_match.group(1):
                        ip_address = ip_match.group(1)
                        wifi_connected = True
                    
                    # Check for camera ready
                    if "Camera Ready" in line:
                        camera_ready = True
                    
                    # Show summary when ready
                    if camera_ready and ip_address:
                        print("\n" + "=" * 60)
                        print("🎉 ESP32-CAM READY!")
                        print("=" * 60)
                        print(f"📱 Camera Stream URL: http://{ip_address}")
                        print(f"🎮 Control Panel: http://{ip_address}")
                        print("\nFeatures available at the web interface:")
                        print("  • Live video stream")
                        print("  • Capture photos")
                        print("  • Change resolution")
                        print("  • Adjust camera settings")
                        print("  • Face detection (if enabled)")
                        print("=" * 60)
                        print("\n(Monitor continues... Press Ctrl+C to exit)")
                        camera_ready = False  # Reset to avoid repeating
                        
            except Exception as e:
                if "utf-8" not in str(e).lower():
                    print(f"Error: {e}")
        
        time.sleep(0.01)
        
except serial.SerialException as e:
    print(f"\n❌ Serial Error: {e}")
    if "Resource busy" in str(e):
        print("\n💡 Port is busy. Close Arduino Serial Monitor first!")
        print("   Or run: pkill -f 'serial|screen'")
        
except KeyboardInterrupt:
    print("\n\n✅ Monitor stopped")
    
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Port closed") 

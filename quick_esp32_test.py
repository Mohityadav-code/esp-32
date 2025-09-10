#!/usr/bin/env python3
"""
Quick ESP32-CAM Test - Shows immediate output
"""

import serial
import time

PORT = '/dev/cu.usbserial-230'
BAUD = 115200

print("=" * 50)
print("ESP32-CAM Quick Connection Test")
print("=" * 50)
print(f"Port: {PORT}")
print(f"Baud: {BAUD}")
print("-" * 50)

try:
    # Open serial connection
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print("✅ Connected successfully!")
    
    # Clear buffer
    ser.reset_input_buffer()
    
    print("\n📝 Sending test commands...")
    
    # Send a newline to trigger any response
    ser.write(b'\r\n')
    time.sleep(0.5)
    
    # Try to trigger ESP32 response
    ser.write(b'AT\r\n')  # AT command (if AT firmware)
    time.sleep(0.5)
    
    print("\n📥 Reading output (10 seconds)...")
    print("💡 TIP: Press the RESET button on ESP32-CAM to see boot messages!\n")
    
    start_time = time.time()
    data_received = False
    
    while time.time() - start_time < 10:
        if ser.in_waiting:
            data = ser.readline()
            try:
                text = data.decode('utf-8', errors='ignore').strip()
                if text:
                    print(f">>> {text}")
                    data_received = True
            except:
                print(f"[RAW] {data.hex()}")
                data_received = True
    
    if not data_received:
        print("\n⚠️  No data received in 10 seconds")
        print("\n🔧 Try these steps:")
        print("1. Press the RESET button on your ESP32-CAM")
        print("2. Make sure ESP32-CAM has code uploaded")
        print("3. Check power supply (needs 5V, ~500mA)")
        print("\nTo upload code, use Arduino IDE:")
        print("  - Select board: AI Thinker ESP32-CAM")
        print("  - Select port: /dev/cu.usbserial-230")
        print("  - Upload example: File > Examples > ESP32 > Camera > CameraWebServer")
    else:
        print("\n✅ Communication successful!")
    
    ser.close()
    
except serial.SerialException as e:
    print(f"❌ Error: {e}")
    print("\nIf permission denied, try:")
    print(f"  sudo chmod 666 {PORT}")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    
print("\n" + "=" * 50)
print("Test complete!") 

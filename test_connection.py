#!/usr/bin/env python3
"""
Quick connection test for ESP32 with MPU-6050
"""

import serial
import time
import sys

def test_connection():
    port = '/dev/cu.usbserial-0001'
    baudrate = 115200
    
    print("=" * 50)
    print("ESP32 MPU-6050 Connection Test")
    print("=" * 50)
    print(f"Port: {port}")
    print(f"Baudrate: {baudrate}")
    print("-" * 50)
    
    try:
        # Open serial connection
        print("Connecting to ESP32...")
        ser = serial.Serial(port, baudrate, timeout=2)
        time.sleep(2)  # Wait for connection
        
        # Send a reset command to ESP32 (DTR toggle)
        ser.setDTR(False)
        time.sleep(0.1)
        ser.setDTR(True)
        
        print("Connected! Waiting for data...\n")
        print("If you see sensor readings below, MPU-6050 is working!")
        print("If no data appears, upload the i2c_scanner.ino first.\n")
        print("-" * 50)
        
        # Clear buffer
        ser.reset_input_buffer()
        
        # Read for 10 seconds
        start_time = time.time()
        data_received = False
        
        while time.time() - start_time < 10:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').rstrip()
                    if line:
                        print(line)
                        data_received = True
                        
                        # Check for specific indicators
                        if "MPU-6050" in line or "0x68" in line:
                            print("\n✅ MPU-6050 DETECTED!")
                        elif "not found" in line.lower() or "no i2c" in line.lower():
                            print("\n⚠️ MPU-6050 might not be connected properly")
                            
                except UnicodeDecodeError:
                    pass
        
        if not data_received:
            print("\n⚠️ No data received from ESP32")
            print("\nPossible reasons:")
            print("1. No program is running on ESP32")
            print("2. Program is not sending serial data")
            print("3. Wrong baud rate")
            print("\n📝 Recommendation: Upload i2c_scanner.ino to test")
            
    except serial.SerialException as e:
        print(f"\n❌ Error: Could not open port {port}")
        print(f"Details: {e}")
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("\nConnection closed.")

if __name__ == "__main__":
    test_connection() 

#!/usr/bin/env python3
"""
Quick Serial Monitor for ESP32 Sensors
This script connects to the ESP32 and displays sensor data
"""

import serial
import sys
import time

def main():
    port = '/dev/cu.usbserial-0001'
    baudrate = 115200
    
    print(f"ESP32 Serial Monitor")
    print(f"Port: {port}")
    print(f"Baudrate: {baudrate}")
    print("-" * 50)
    print("Connecting to ESP32...")
    
    try:
        # Open serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for connection to establish
        
        # Clear any existing data
        ser.reset_input_buffer()
        
        print("Connected! Monitoring sensor data...")
        print("Press Ctrl+C to exit\n")
        print("=" * 50)
        
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8').rstrip()
                    print(line)
                except UnicodeDecodeError:
                    # Handle any decoding errors
                    pass
                    
    except serial.SerialException as e:
        print(f"\nError: Could not open port {port}")
        print(f"Details: {e}")
        print("\nMake sure:")
        print("1. ESP32 is connected via USB")
        print("2. The port is correct (check with 'ls /dev/tty.*')")
        print("3. No other program is using the serial port")
        
    except KeyboardInterrupt:
        print("\n\nExiting serial monitor...")
        
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial connection closed.")

if __name__ == "__main__":
    main() 

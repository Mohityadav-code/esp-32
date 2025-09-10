#!/usr/bin/env python3
"""
ESP32-CAM Serial Monitor for Mac
Automatically detects and connects to ESP32-CAM
"""

import serial
import serial.tools.list_ports
import time
import sys

def find_esp32_port():
    """Find ESP32-CAM port automatically"""
    ports = serial.tools.list_ports.comports()
    
    print("Scanning for ESP32-CAM...")
    print("-" * 40)
    
    esp_ports = []
    for port in ports:
        print(f"Found: {port.device} - {port.description}")
        # Common ESP32-CAM USB-to-Serial chips
        if any(x in port.description.lower() for x in ['cp210', 'ch340', 'uart', 'serial', 'usb']):
            esp_ports.append(port.device)
        # Also check device names
        elif 'usbserial' in port.device.lower() or 'slab' in port.device.lower():
            esp_ports.append(port.device)
    
    print("-" * 40)
    
    if not esp_ports:
        print("❌ No ESP32-CAM found. Please check:")
        print("   1. ESP32-CAM is connected via USB")
        print("   2. Using a data cable (not charging-only)")
        print("   3. Drivers are installed (CP2102/CH340)")
        return None
    
    if len(esp_ports) == 1:
        print(f"✅ Found ESP32-CAM on: {esp_ports[0]}")
        return esp_ports[0]
    else:
        print("Multiple serial devices found:")
        for i, port in enumerate(esp_ports, 1):
            print(f"  {i}. {port}")
        
        choice = input("\nSelect port number (or press Enter for first): ").strip()
        if not choice:
            choice = "1"
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(esp_ports):
                return esp_ports[idx]
        except ValueError:
            pass
        
        print("Invalid selection, using first port")
        return esp_ports[0]

def monitor_esp32(port=None, baud_rate=115200):
    """Monitor ESP32-CAM serial output"""
    
    if port is None:
        port = find_esp32_port()
        if port is None:
            return
    
    print(f"\nConnecting to {port} at {baud_rate} baud...")
    print("Press Ctrl+C to exit")
    print("=" * 50 + "\n")
    
    try:
        # Open serial connection
        ser = serial.Serial(
            port=port,
            baudrate=baud_rate,
            timeout=0.1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        
        # Clear any buffered data
        ser.reset_input_buffer()
        
        print("✅ Connected! Waiting for data...\n")
        print("💡 TIP: Press RESET button on ESP32-CAM to see boot messages\n")
        
        empty_reads = 0
        while True:
            if ser.in_waiting:
                empty_reads = 0
                try:
                    # Read and decode line
                    line = ser.readline()
                    
                    # Try different decodings
                    try:
                        text = line.decode('utf-8').rstrip()
                    except UnicodeDecodeError:
                        try:
                            text = line.decode('ascii', errors='ignore').rstrip()
                        except:
                            # Show as hex if can't decode
                            text = f"[HEX] {line.hex()}"
                    
                    if text:
                        # Add timestamp for each line
                        timestamp = time.strftime('%H:%M:%S')
                        print(f"[{timestamp}] {text}")
                        
                        # Check for common ESP32-CAM messages
                        if "Camera" in text or "cam" in text.lower():
                            print("    📷 Camera-related message detected")
                        elif "IP" in text or "192.168" in text or "10.0" in text:
                            print("    🌐 Network information detected")
                        elif "error" in text.lower() or "fail" in text.lower():
                            print("    ⚠️  Error message detected")
                
                except Exception as e:
                    print(f"Error reading line: {e}")
            else:
                empty_reads += 1
                if empty_reads == 50:  # After 5 seconds of no data
                    print("💤 No data received. Try:")
                    print("   - Press RESET button on ESP32-CAM")
                    print("   - Check if ESP32-CAM has code uploaded")
                    print("   - Verify baud rate (typically 115200)")
                    empty_reads = 0
                
                time.sleep(0.1)
    
    except serial.SerialException as e:
        print(f"\n❌ Serial Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check if another program is using the port")
        print("2. Try: sudo chmod 666", port)
        print("3. Disconnect and reconnect ESP32-CAM")
        
    except KeyboardInterrupt:
        print("\n\n✅ Monitor stopped by user")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Serial port closed")

def main():
    """Main function"""
    print("=" * 50)
    print("ESP32-CAM Serial Monitor for Mac")
    print("=" * 50 + "\n")
    
    # Check if pyserial is installed
    try:
        import serial
    except ImportError:
        print("❌ pyserial not installed!")
        print("Install with: pip3 install pyserial")
        sys.exit(1)
    
    # Optional: specify port and baud rate as arguments
    import argparse
    parser = argparse.ArgumentParser(description='Monitor ESP32-CAM serial output')
    parser.add_argument('-p', '--port', help='Serial port (e.g., /dev/cu.usbserial-0001)')
    parser.add_argument('-b', '--baud', type=int, default=115200, help='Baud rate (default: 115200)')
    args = parser.parse_args()
    
    monitor_esp32(args.port, args.baud)

if __name__ == "__main__":
    main() 

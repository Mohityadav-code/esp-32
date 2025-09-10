#!/usr/bin/env python3
"""
Quick ESP32-CAM Connection Checker
Shows all available serial ports and identifies likely ESP32 devices
"""

import subprocess
import sys

def check_with_system_profiler():
    """Check USB devices using macOS system profiler"""
    print("\n📱 USB Devices (from System Profiler):")
    print("-" * 40)
    try:
        result = subprocess.run(
            ["system_profiler", "SPUSBDataType"],
            capture_output=True,
            text=True
        )
        
        lines = result.stdout.split('\n')
        esp_found = False
        
        for i, line in enumerate(lines):
            if any(x in line.lower() for x in ['cp210', 'ch340', 'uart', 'serial', 'esp32', 'silicon labs']):
                # Print context around the match
                start = max(0, i-2)
                end = min(len(lines), i+5)
                for j in range(start, end):
                    print(lines[j])
                esp_found = True
                print()
        
        if not esp_found:
            print("No ESP32-related USB devices found in system profiler")
            
    except Exception as e:
        print(f"Error running system_profiler: {e}")

def check_serial_ports():
    """Check available serial ports"""
    print("\n🔌 Serial Ports Available:")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            ["ls", "-la", "/dev/cu.*"],
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout:
            lines = result.stdout.strip().split('\n')
            esp_ports = []
            
            for line in lines:
                print(line)
                if 'usbserial' in line or 'SLAB' in line or 'wchusbserial' in line:
                    # Extract the device name
                    parts = line.split()
                    if parts:
                        device = parts[-1]
                        esp_ports.append(device)
            
            if esp_ports:
                print("\n✅ Likely ESP32 ports found:")
                for port in esp_ports:
                    print(f"   • {port}")
                return esp_ports
            else:
                print("\n⚠️  No typical ESP32 serial ports found")
        else:
            print("No serial ports found in /dev/cu.*")
            
    except Exception as e:
        print(f"Error checking serial ports: {e}")
    
    return []

def test_port_access(port):
    """Test if we can access a serial port"""
    print(f"\n🧪 Testing port access: {port}")
    print("-" * 40)
    
    try:
        # Check if pyserial is installed
        try:
            import serial
            
            # Try to open the port
            ser = serial.Serial(port, 115200, timeout=0.5)
            print(f"✅ Successfully opened {port}")
            
            # Send a simple command
            ser.write(b'\r\n')
            
            # Try to read something
            data = ser.read(100)
            if data:
                print(f"📥 Received {len(data)} bytes")
                try:
                    text = data.decode('utf-8', errors='ignore')
                    if text.strip():
                        print(f"   Data preview: {text[:50]}...")
                except:
                    print(f"   Raw data: {data[:20].hex()}...")
            else:
                print("📭 No immediate response (device might be idle)")
            
            ser.close()
            return True
            
        except ImportError:
            print("⚠️  pyserial not installed. Install with: pip3 install pyserial")
            print("    Skipping port test...")
            return False
            
    except Exception as e:
        print(f"❌ Could not access port: {e}")
        if "Permission denied" in str(e):
            print(f"\n💡 Try: sudo chmod 666 {port}")
        return False

def main():
    print("=" * 50)
    print("🔍 ESP32-CAM Connection Checker for Mac")
    print("=" * 50)
    
    # Check system profiler
    check_with_system_profiler()
    
    # Check serial ports
    ports = check_serial_ports()
    
    # Test first available port
    if ports:
        print("\n" + "=" * 50)
        print("💡 Quick Start Commands:")
        print("=" * 50)
        
        first_port = ports[0]
        
        print(f"\n1. Monitor with Python script:")
        print(f"   python3 monitor_esp32cam.py")
        
        print(f"\n2. Quick monitor with screen:")
        print(f"   screen {first_port} 115200")
        
        print(f"\n3. Using Arduino IDE:")
        print(f"   - Select port: {first_port}")
        print(f"   - Open Serial Monitor (Cmd+Shift+M)")
        print(f"   - Set baud rate to 115200")
        
        # Test the first port
        test_port_access(first_port)
    else:
        print("\n" + "=" * 50)
        print("❌ No ESP32-CAM detected!")
        print("=" * 50)
        print("\n📋 Troubleshooting Checklist:")
        print("1. ✓ Is ESP32-CAM connected via USB?")
        print("2. ✓ Are you using a DATA cable (not charging-only)?")
        print("3. ✓ Is the USB port working?")
        print("4. ✓ Are drivers installed?")
        print("\n📦 Common ESP32-CAM USB-Serial Drivers:")
        print("   • CP2102: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers")
        print("   • CH340: https://github.com/adrianmihalko/ch340g-ch34g-ch34x-mac-os-x-driver")
        print("\n💡 After installing drivers:")
        print("   1. Disconnect ESP32-CAM")
        print("   2. Restart your Mac")
        print("   3. Reconnect ESP32-CAM")
        print("   4. Run this script again")

if __name__ == "__main__":
    main() 

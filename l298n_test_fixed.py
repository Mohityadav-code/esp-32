"""
L298N Test with Fixed Pin Configuration
Uses D5, D18, D19, D23 (avoiding D21 I2C conflict)
"""

from machine import Pin
import time

print("=" * 50)
print("L298N TEST - FIXED PIN CONFIGURATION")
print("=" * 50)
print("\nIMPORTANT: This uses D23 instead of D21")
print("to avoid conflict with I2C (MPU-6050)\n")

# Fixed pin configuration
IN1 = Pin(5, Pin.OUT)   # D5
IN2 = Pin(18, Pin.OUT)  # D18  
IN3 = Pin(19, Pin.OUT)  # D19
IN4 = Pin(23, Pin.OUT)  # D23 (changed from D21!)

print("Pin Configuration:")
print("  IN1 → GPIO 5 (D5)")
print("  IN2 → GPIO 18 (D18)")
print("  IN3 → GPIO 19 (D19)")
print("  IN4 → GPIO 23 (D23) ← CHANGED FROM D21!")
print("-" * 50)

def all_off():
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()

def power_check():
    """First check if any response from L298N"""
    print("\n### POWER CHECK ###")
    print("All pins HIGH (if L298N has power, LEDs should light)")
    IN1.on()
    IN2.on()
    IN3.on()
    IN4.on()
    time.sleep(2)
    
    print("All pins LOW")
    all_off()
    time.sleep(1)
    print("Power check complete\n")

def motor_test():
    """Test each motor direction"""
    print("### MOTOR TEST ###")
    
    # Motor A Forward
    print("Motor A Forward (IN1=HIGH, IN2=LOW)")
    IN1.on()
    IN2.off()
    time.sleep(2)
    
    # Motor A Backward
    print("Motor A Backward (IN1=LOW, IN2=HIGH)")
    IN1.off()
    IN2.on()
    time.sleep(2)
    
    # Motor A Stop
    print("Motor A Stop")
    IN1.off()
    IN2.off()
    time.sleep(1)
    
    # Motor B Forward
    print("Motor B Forward (IN3=HIGH, IN4=LOW)")
    IN3.on()
    IN4.off()
    time.sleep(2)
    
    # Motor B Backward
    print("Motor B Backward (IN3=LOW, IN4=HIGH)")
    IN3.off()
    IN4.on()
    time.sleep(2)
    
    # Stop all
    print("All Stop")
    all_off()
    print("Motor test complete\n")

# Main test
print("\nStarting tests...")
print("Make sure:")
print("✓ External power (6-12V) connected to L298N")
print("✓ ESP32 GND connected to L298N GND")
print("✓ ENA and ENB jumpers installed")
print("✓ Motors connected to OUT1/OUT2 and OUT3/OUT4")
print("\nPress Enter to start or Ctrl+C to exit")

try:
    input()
    
    # Run tests
    power_check()
    motor_test()
    
    print("\n### CONTINUOUS TEST ###")
    print("Motors will run forward/backward continuously")
    print("Press Ctrl+C to stop\n")
    
    while True:
        print("Both forward")
        IN1.on()
        IN2.off()
        IN3.on()
        IN4.off()
        time.sleep(2)
        
        print("Both backward")
        IN1.off()
        IN2.on()
        IN3.off()
        IN4.on()
        time.sleep(2)
        
except KeyboardInterrupt:
    all_off()
    print("\n\nTest stopped. All motors OFF.")
    print("\nIf motors didn't work, check:")
    print("1. Power supply (MOST IMPORTANT)")
    print("2. Ground connection ESP32→L298N")
    print("3. Rewire IN4 from D21 to D23")
    print("4. Run l298n_diagnostic.py for detailed check") 

"""
Simple L298N Connection Test
Blinks each pin to verify connections
Pins: D5, D18, D19, D21
"""

from machine import Pin
import time

# Setup pins
IN1 = Pin(5, Pin.OUT)   # D5
IN2 = Pin(18, Pin.OUT)  # D18
IN3 = Pin(19, Pin.OUT)  # D19
IN4 = Pin(21, Pin.OUT)  # D21

print("Simple L298N Test - Pins D5, D18, D19, D21")
print("Press Ctrl+C to stop")
print("-" * 40)

# Simple test loop - all pins on/off together
counter = 0
try:
    while True:
        # All on
        IN1.on()
        IN2.on()
        IN3.on()
        IN4.on()
        print(f"Cycle {counter}: All pins ON")
        time.sleep(1)
        
        # All off
        IN1.off()
        IN2.off()
        IN3.off()
        IN4.off()
        print(f"Cycle {counter}: All pins OFF")
        time.sleep(1)
        
        counter += 1
        
except KeyboardInterrupt:
    # Clean stop
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
    print("\nTest stopped. All pins OFF.") 

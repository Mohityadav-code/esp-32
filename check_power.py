"""
Power Supply Diagnostic for L298N
Helps identify if the issue is power-related
"""

from machine import Pin
import time

print("=" * 50)
print("L298N POWER SUPPLY CHECK")
print("=" * 50)

# Use built-in LED if available (GPIO 2 on most ESP32 boards)
try:
    led = Pin(2, Pin.OUT)
    has_led = True
except:
    has_led = False

# Setup motor control pins
pins = {
    'IN1': Pin(5, Pin.OUT),
    'IN2': Pin(18, Pin.OUT),
    'IN3': Pin(19, Pin.OUT),
    'IN4': Pin(23, Pin.OUT)  # or 21 if you haven't changed wiring
}

print("\n### WHAT YOU SHOULD SEE ###\n")
print("WITH PROPER POWER:")
print("✓ L298N Power LED: ON (red)")
print("✓ L298N Motor LEDs: Blink with pins")
print("✓ Motors: Should move/twitch")
print("✓ L298N Heat sink: Gets slightly warm")

print("\nWITHOUT PROPER POWER:")
print("✗ No LEDs on L298N")
print("✗ No motor movement")
print("✗ ESP32 might reset (brownout)")

print("\n" + "=" * 50)
print("QUICK POWER TEST")
print("=" * 50)

def flash_all(count=3):
    """Flash all outputs to check for brownout"""
    for i in range(count):
        # All on
        for pin in pins.values():
            pin.on()
        if has_led:
            led.on()
        print(f"Flash {i+1}: ON")
        time.sleep(0.5)
        
        # All off
        for pin in pins.values():
            pin.off()
        if has_led:
            led.off()
        print(f"Flash {i+1}: OFF")
        time.sleep(0.5)

print("\nTest 1: Flashing all pins...")
print("(If ESP32 resets, you have a power issue!)\n")
flash_all()

print("\nTest 2: Individual pin test...")
for name, pin in pins.items():
    print(f"{name}: HIGH ", end="")
    pin.on()
    time.sleep(0.5)
    print("→ LOW")
    pin.off()
    time.sleep(0.3)

print("\nTest 3: Sustained load test...")
print("All pins HIGH for 3 seconds...")
for pin in pins.values():
    pin.on()
time.sleep(3)

print("All pins LOW")
for pin in pins.values():
    pin.off()

print("\n" + "=" * 50)
print("DIAGNOSIS:")
print("=" * 50)

print("""
If ESP32 reset or motors didn't move:

1. POWER SUPPLY ISSUE (99% likely):
   → Solution: Connect external 6-12V power to L298N
   → USB alone can't power motors!
   
2. Check these connections:
   → Power supply (+) to L298N power input (+)
   → Power supply (-) to L298N power input (-)
   → L298N GND to ESP32 GND (CRITICAL!)
   → 5V jumper installed on L298N
   
3. Minimum power requirements:
   → Voltage: 6-12V DC
   → Current: 2A minimum (more for larger motors)
   → Options: Battery pack (4xAA=6V), 9V adapter, 12V adapter
   
4. Quick test without motors:
   → Remove motors
   → Run this test again
   → L298N LEDs should still light up with proper power
""")

print("Test complete!") 

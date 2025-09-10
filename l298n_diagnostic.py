"""
L298N Diagnostic Tool for ESP32
Helps troubleshoot connection issues
"""

from machine import Pin, ADC
import time

print("=" * 50)
print("L298N DIAGNOSTIC TOOL")
print("=" * 50)

# Setup pins
pins = {
    5: "IN1 (D5)",
    18: "IN2 (D18)", 
    19: "IN3 (D19)",
    21: "IN4 (D21)"
}

print("\n1. TESTING PIN OUTPUTS")
print("-" * 30)

for gpio, name in pins.items():
    pin = Pin(gpio, Pin.OUT)
    print(f"\nTesting {name} - GPIO {gpio}:")
    
    # Test HIGH
    pin.on()
    print(f"  Set HIGH - Pin should output 3.3V")
    time.sleep(0.5)
    
    # Test LOW  
    pin.off()
    print(f"  Set LOW - Pin should output 0V")
    time.sleep(0.5)

print("\n2. CHECKING PIN STATES")
print("-" * 30)

# Set a test pattern
test_pattern = [1, 0, 1, 0]  # IN1=HIGH, IN2=LOW, IN3=HIGH, IN4=LOW
pin_objects = []

for i, (gpio, name) in enumerate(pins.items()):
    pin = Pin(gpio, Pin.OUT)
    pin_objects.append(pin)
    pin.value(test_pattern[i])
    print(f"{name}: {'HIGH' if test_pattern[i] else 'LOW'}")

print("\n3. CONTINUOUS TOGGLE TEST")
print("-" * 30)
print("All pins will toggle every second")
print("Use a multimeter to verify voltage changes")
print("Press Ctrl+C to stop\n")

try:
    state = 0
    while True:
        for pin in pin_objects:
            pin.value(state)
        print(f"All pins: {'HIGH (3.3V)' if state else 'LOW (0V)'}")
        state = 1 - state
        time.sleep(1)
        
except KeyboardInterrupt:
    # Turn all off
    for pin in pin_objects:
        pin.off()
    print("\n\nDiagnostic stopped. All pins set to LOW.")

print("\n" + "=" * 50)
print("TROUBLESHOOTING CHECKLIST:")
print("=" * 50)
print("""
If motors are not working, check:

1. POWER ISSUES (MOST COMMON):
   □ Is 12V/external power connected to L298N power input?
   □ Is L298N ground connected to ESP32 ground? (CRITICAL!)
   □ Is the 5V regulator jumper in place on L298N?
   □ Are motor power terminals properly connected?

2. ENABLE PINS:
   □ Are ENA and ENB jumpers installed on L298N?
   □ OR are ENA/ENB connected to ESP32 PWM pins?

3. WIRING:
   □ D5 (GPIO5) → IN1
   □ D18 (GPIO18) → IN2  
   □ D19 (GPIO19) → IN3
   □ D21 (GPIO21) → IN4
   □ ESP32 GND → L298N GND (MUST HAVE!)

4. MOTORS:
   □ Are motors connected to OUT1/OUT2 and OUT3/OUT4?
   □ Do motors work when directly connected to power?

5. VOLTAGE LEVELS:
   □ Measure voltage at IN1-IN4 (should toggle 0V/3.3V)
   □ Measure motor output voltage when pins are HIGH
   □ Check 5V on L298N board (should be ~5V)

6. L298N MODULE:
   □ Is the L298N getting warm? (normal)
   □ Is the L298N getting HOT? (problem - check shorts)
   □ LED indicators on? (if your module has them)
""") 

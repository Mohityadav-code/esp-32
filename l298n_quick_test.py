"""
Quick L298N Pin Test
Tests each pin individually with your connections:
D5, D18, D19, D21
"""

from machine import Pin
import time

# Your pin configuration
pins = {
    'IN1 (D5)': Pin(5, Pin.OUT),
    'IN2 (D18)': Pin(18, Pin.OUT),
    'IN3 (D19)': Pin(19, Pin.OUT),
    'IN4 (D21)': Pin(21, Pin.OUT)
}

print("L298N Quick Pin Test")
print("=" * 30)
print("Testing each pin individually...")
print("Watch your motors/LEDs to see which pin controls what\n")

# First, turn everything off
for name, pin in pins.items():
    pin.off()

# Test each pin individually
for name, pin in pins.items():
    print(f"Testing {name}: ON")
    pin.on()
    time.sleep(1)
    print(f"Testing {name}: OFF")
    pin.off()
    time.sleep(0.5)
    print()

print("Individual pin test complete!\n")
print("Now testing common motor patterns:")
print("-" * 30)

# Quick motor pattern test
patterns = [
    ("Motor A Forward", [(5, 1), (18, 0), (19, 0), (21, 0)]),
    ("Motor A Backward", [(5, 0), (18, 1), (19, 0), (21, 0)]),
    ("Motor B Forward", [(5, 0), (18, 0), (19, 1), (21, 0)]),
    ("Motor B Backward", [(5, 0), (18, 0), (19, 0), (21, 1)]),
    ("Both Forward", [(5, 1), (18, 0), (19, 1), (21, 0)]),
    ("Both Backward", [(5, 0), (18, 1), (19, 0), (21, 1)]),
    ("Stop All", [(5, 0), (18, 0), (19, 0), (21, 0)])
]

for pattern_name, states in patterns:
    print(f"Pattern: {pattern_name}")
    for pin_num, state in states:
        Pin(pin_num, Pin.OUT).value(state)
    time.sleep(1.5)

# Make sure everything is off at the end
print("\nStopping all motors...")
for pin in pins.values():
    pin.off()

print("Quick test complete!") 

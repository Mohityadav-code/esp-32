"""
ESP32 Pin Test with LED
Test pins D5, D18, D19, D21 with an LED first
This helps verify ESP32 is working before L298N
"""

from machine import Pin
import time

print("ESP32 PIN TEST - Use an LED + resistor")
print("=" * 40)
print("Connect LED + 220-330 ohm resistor between pin and GND")
print("LED should blink when connected to each pin\n")

pins_to_test = [
    (5, "D5"),
    (18, "D18"),
    (19, "D19"),
    (21, "D21")
]

print("Starting pin test...\n")

for gpio, name in pins_to_test:
    print(f"Testing {name} (GPIO{gpio})")
    print(f"Connect LED to {name} now...")
    pin = Pin(gpio, Pin.OUT)
    
    # Blink 5 times
    for i in range(5):
        pin.on()
        print(f"  {name} ON ", end="")
        time.sleep(0.3)
        pin.off()
        print("OFF")
        time.sleep(0.3)
    
    print(f"  {name} test complete\n")
    time.sleep(1)

print("All pins tested!")
print("\nIf LEDs blinked on all pins, ESP32 pins are working.")
print("If not, check:")
print("- ESP32 board for damage")
print("- Correct pin numbers")
print("- LED polarity (long leg to pin, short to GND)")
print("- Resistor value (220-330 ohms)") 

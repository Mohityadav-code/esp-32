# L298N Motor Driver Troubleshooting Guide

## Most Common Issues (90% of problems)

### 1. **POWER SUPPLY ISSUES** ⚡ (Most Common!)
The L298N needs TWO power connections:
- **Logic Power (5V)**: Powers the control circuits
- **Motor Power (6-12V)**: Powers the motors

**Check:**
- [ ] **External power connected?** The L298N needs 6-12V DC power supply connected to the power terminal block
- [ ] **Ground connection?** ESP32 GND MUST connect to L298N GND (shared ground is CRITICAL!)
- [ ] **5V jumper in place?** The jumper near the power terminals enables the onboard 5V regulator
- [ ] **Power supply current?** Motors need significant current (1-2A per motor). USB power alone won't work!

### 2. **ENABLE PINS** 🔌
The L298N has ENA and ENB pins that must be HIGH for motors to run.

**Check:**
- [ ] **Jumpers installed?** Look for small jumpers on ENA and ENB pins (usually blue or black)
- [ ] If no jumpers, connect ENA and ENB to ESP32 3.3V or additional GPIO pins for PWM control

### 3. **PIN CONFLICT** ⚠️
I notice you're using D21, which might conflict with I2C!

From your wiring guide, GPIO 21 is used for:
- MPU-6050 SDA (I2C data)
- Your L298N IN4

**This is a problem!** You can't use the same pin for two different purposes.

**Solution:** Use a different pin for IN4. Try:
- GPIO 23 instead of GPIO 21
- GPIO 22 (if not using I2C)
- GPIO 32, 33, 25, 26, or 27

## Quick Test Sequence

### Step 1: Test ESP32 Pins
Run `pin_led_test.py` with an LED to verify ESP32 outputs work.

### Step 2: Check Voltages
Using a multimeter:
1. Measure L298N power input (should be 6-12V)
2. Measure 5V pin on L298N (should be ~5V)
3. Measure IN1-IN4 when running test (should toggle 0V/3.3V)

### Step 3: Test Without Motors
Remove motors and check if L298N board LEDs light up when running tests.

### Step 4: Test Motors Directly
Connect motors directly to power supply to verify they work.

## Complete Wiring Checklist

### Power Connections:
```
Power Supply (+) → L298N Motor Power (+)
Power Supply (-) → L298N Motor Power (-)
L298N GND → ESP32 GND (CRITICAL!)
```

### Control Connections (Updated to avoid conflicts):
```
ESP32 → L298N
-------------
D5 (GPIO 5)   → IN1
D18 (GPIO 18) → IN2  
D19 (GPIO 19) → IN3
D23 (GPIO 23) → IN4  (Changed from D21 to avoid I2C conflict!)
```

### Motor Connections:
```
Motor A → OUT1 & OUT2
Motor B → OUT3 & OUT4
```

## Visual Check

Look for these on your L298N board:
1. **Power LED** - Should be ON when powered
2. **Motor LEDs** - Should light when pins are HIGH
3. **Heat sink** - Gets warm during operation (normal)
4. **Blue/black jumpers** on ENA and ENB

## Debug Code to Run

1. First run: `l298n_diagnostic.py` - Comprehensive diagnostics
2. If pins work: Check power supply with multimeter
3. If power good: Check for pin conflicts (especially GPIO 21)

## Still Not Working?

If everything above checks out:
1. The L298N module might be damaged (rare but possible)
2. Try different GPIO pins
3. Test with a simple DC motor or even an LED at the motor outputs
4. Check if the L298N is getting hot (indicates short circuit)

## The Fix for Your Setup

Since you're using GPIO 21 for I2C (MPU-6050), change your wiring:

**OLD:**
- D21 → IN4

**NEW:**
- D23 → IN4 (or any other free GPIO)

Then update the code to use GPIO 23 instead of 21! 

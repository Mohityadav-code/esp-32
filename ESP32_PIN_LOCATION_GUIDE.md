# ESP32 DevKit V1 - Pin Location Guide for MPU-6050

## Board Orientation
```
         USB PORT (Type-C)
              ↓
    [====================]
    [                    ]
    [ ESP32 DEVKIT V1    ]
    [ TYPE-C             ]
    [                    ]
    [====================]
         ↑            ↑
      LEFT SIDE    RIGHT SIDE
```

## Pin Layout (Looking at board with USB port at TOP)

### LEFT SIDE (15 pins from top to bottom):
```
Pin #   Label       Use for MPU-6050
-----   -----       ----------------
1       3V3         → Connect to VCC (MPU-6050) ✅
2       EN          
3       VP (36)     
4       VN (39)     
5       34          
6       35          
7       32          
8       33          
9       25          
10      26          
11      27          
12      14          
13      12          
14      GND         → Connect to GND (MPU-6050) ✅
15      13          
```

### RIGHT SIDE (15 pins from top to bottom):
```
Pin #   Label       Use for MPU-6050
-----   -----       ----------------
1       VIN         
2       GND         → Alternative GND (can use this too) ✅
3       23          
4       22          → Connect to SCL (MPU-6050) ✅
5       TX0 (1)     
6       RX0 (3)     
7       21          → Connect to SDA (MPU-6050) ✅
8       GND         → Another GND option ✅
9       19          
10      18          
11      5           
12      17          
13      16          
14      4           
15      0           
16      2           
17      15          
```

## MPU-6050 WIRING SUMMARY

### REQUIRED CONNECTIONS:
```
MPU-6050 Pin    →    ESP32 Location
============         ==============
VCC             →    LEFT SIDE, Pin #1 (3V3)
GND             →    LEFT SIDE, Pin #14 (GND)
                     OR RIGHT SIDE Pin #2 or #8 (GND)
SCL             →    RIGHT SIDE, Pin #4 (GPIO 22)
SDA             →    RIGHT SIDE, Pin #7 (GPIO 21)
ADO             →    Connect to any GND pin
```

## VISUAL WIRING DIAGRAM

```
    ESP32 (USB at top)              MPU-6050
    
    LEFT          RIGHT              
    ====          =====              ========
    3V3  ●--------●----------------● VCC
    EN   ●        ● VIN              
    36   ●        ● GND--●          
    39   ●        ● 23   |          
    34   ●        ● 22---|---------● SCL
    35   ●        ● TX0  |          
    32   ●        ● RX0  |          
    33   ●        ● 21---|---------● SDA
    25   ●        ● GND--●---------● GND
    26   ●        ● 19              
    27   ●        ● 18              ● XCL (leave open)
    14   ●        ● 5               ● XDA (leave open)
    12   ●        ● 17              ● ADO--●
    GND  ●--------●-----------------● GND   |
    13   ●        ● 4                      |
              ● 0                      |
              ● 2                  (connect ADO to GND)
              ● 15              
```

## STEP-BY-STEP WIRING INSTRUCTIONS

1. **Place ESP32 on breadboard** with USB port facing up/away from you

2. **Identify the sides**:
   - LEFT side: Has 3V3 as first pin
   - RIGHT side: Has VIN as first pin

3. **Connect Power (Red wires)**:
   - MPU-6050 VCC → ESP32 LEFT side, 1st pin (3V3)

4. **Connect Ground (Black wires)**:
   - MPU-6050 GND → ESP32 LEFT side, 14th pin (GND)
   - MPU-6050 ADO → Same GND pin (or any other GND)

5. **Connect I2C Clock (Yellow/White wire)**:
   - MPU-6050 SCL → ESP32 RIGHT side, 4th pin (GPIO 22)

6. **Connect I2C Data (Green/Blue wire)**:
   - MPU-6050 SDA → ESP32 RIGHT side, 7th pin (GPIO 21)

## TIPS FOR COUNTING PINS

### Left Side (from USB port down):
- Pin 1: 3V3 (POWER) ← Start here!
- Count down...
- Pin 14: GND (GROUND)

### Right Side (from USB port down):
- Pin 1: VIN ← Start here!
- Pin 2: GND
- Pin 3: 23
- Pin 4: 22 (SCL) ← This one!
- Pin 5: TX0
- Pin 6: RX0
- Pin 7: 21 (SDA) ← This one!
- Pin 8: GND

## DOUBLE-CHECK YOUR CONNECTIONS

✅ **Correct connections**:
- 3.3V power (NOT 5V!)
- SCL on GPIO 22 (right side, 4th pin)
- SDA on GPIO 21 (right side, 7th pin)
- ADO connected to GND (for address 0x68)

❌ **Common mistakes**:
- Don't connect to 5V (VIN)
- Don't mix up GPIO 21 and 22
- Don't forget to connect ADO to GND
- Don't leave GND unconnected

## COLOR CODE SUGGESTION
- Red wire: 3.3V power
- Black wire: GND
- Yellow wire: SCL (clock)
- Green wire: SDA (data)

This makes troubleshooting easier! 

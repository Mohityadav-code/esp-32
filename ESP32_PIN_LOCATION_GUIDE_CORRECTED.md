# ESP32 DevKit - CORRECTED Pin Location Guide for MPU-6050

## Board Orientation (CORRECTED)
```
         USB PORT (Type-C)
              ↓
    [====================]
    [                    ]
    [ ESP32 DEVKIT       ]
    [                    ]
    [====================]
         ↑            ↑
      LEFT SIDE    RIGHT SIDE
```

## CORRECTED Pin Layout (USB port at TOP)

### LEFT SIDE (from top to bottom):
```
Pin #   Label       
-----   -----       
1       EN          
2       VP (36)     
3       VN (39)     
4       34          
5       35          
6       32          
7       33          
8       25          
9       26          
10      27          
11      14          
12      12          
13      13          
14      GND         
15      VIN         
```

### RIGHT SIDE (from top to bottom):
```
Pin #   Label       Use for MPU-6050
-----   -----       ----------------
1       3V3         → Connect to VCC (MPU-6050) ✅
2       GND         → Connect to GND (MPU-6050) ✅
3       15          
4       2           
5       4           
6       16 (RX2)    
7       17 (TX2)    
8       5           
9       18          
10      19          
11      21          → Connect to SDA (MPU-6050) ✅
12      RX0 (3)     
13      TX0 (1)     
14      22          → Connect to SCL (MPU-6050) ✅
15      23          
```

## CORRECTED MPU-6050 WIRING

### ✅ CORRECT CONNECTIONS:
```
MPU-6050 Pin    →    ESP32 Location
============         ==============
VCC             →    RIGHT SIDE, Pin #1 (3V3)
GND             →    RIGHT SIDE, Pin #2 (GND)
                     OR LEFT SIDE Pin #14 (GND)
SDA             →    RIGHT SIDE, Pin #11 (GPIO 21)
SCL             →    RIGHT SIDE, Pin #14 (GPIO 22)
ADO             →    Connect to any GND pin
```

## VISUAL WIRING DIAGRAM (CORRECTED)

```
    ESP32 (USB at top)              MPU-6050
    
    LEFT          RIGHT              
    ====          =====              ========
    EN   ●        ● 3V3--------------● VCC
    VP   ●        ● GND--------------● GND
    VN   ●        ● 15               
    34   ●        ● 2                
    35   ●        ● 4                
    32   ●        ● RX2              
    33   ●        ● TX2              
    25   ●        ● 5                
    26   ●        ● 18               
    27   ●        ● 19               
    14   ●        ● 21---------------● SDA
    12   ●        ● RX0              
    13   ●        ● TX0              
    GND--●        ● 22---------------● SCL
    VIN  ●        ● 23               
         |                           
         └-----------------------● ADO (to set address)
                                 ● XCL (leave open)
                                 ● XDA (leave open)
                                 ● INT (leave open)
```

## STEP-BY-STEP WIRING (CORRECTED)

1. **Orient your ESP32** with USB Type-C port at the TOP

2. **Identify the sides**:
   - LEFT side: First pin is EN (not 3V3)
   - RIGHT side: First pin is 3V3 ✅

3. **Connect Power (Red wire)**:
   - MPU-6050 VCC → ESP32 RIGHT side, Pin #1 (3V3)

4. **Connect Ground (Black wire)**:
   - MPU-6050 GND → ESP32 RIGHT side, Pin #2 (GND)
   - MPU-6050 ADO → Same GND or LEFT side Pin #14 (GND)

5. **Connect I2C Data (Green wire)**:
   - MPU-6050 SDA → ESP32 RIGHT side, Pin #11 (GPIO 21)

6. **Connect I2C Clock (Yellow wire)**:
   - MPU-6050 SCL → ESP32 RIGHT side, Pin #14 (GPIO 22)

## EASY PIN COUNTING METHOD

### RIGHT Side (where all connections go):
Starting from USB port, count DOWN:
1. **3V3** ← Power here! (Red wire)
2. **GND** ← Ground here! (Black wire)
3. 15
4. 2
5. 4
6. RX2
7. TX2
8. 5
9. 18
10. 19
11. **21** ← SDA here! (Green wire)
12. RX0
13. TX0
14. **22** ← SCL here! (Yellow wire)
15. 23

## 🎯 QUICK SUMMARY

**ALL connections are on the RIGHT side!**
- Pin 1: 3V3 (Power)
- Pin 2: GND (Ground)
- Pin 11: GPIO 21 (SDA)
- Pin 14: GPIO 22 (SCL)

## ⚠️ IMPORTANT NOTES

1. **3V3 is on the RIGHT side** (not left as I incorrectly stated before)
2. **All MPU-6050 connections go to the RIGHT side** of the board
3. GPIO 21 comes BEFORE GPIO 22 when counting from top
4. Use 3.3V (first pin on right), NOT VIN (last pin on left)

Thank you for the correction! This layout matches your actual board. 

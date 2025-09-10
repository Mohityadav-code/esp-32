from machine import I2C, Pin
import time, math

# I2C pins for your ESP32
SDA_PIN = 21
SCL_PIN = 22
MPU_ADDR = 0x68

i2c = I2C(0, sda=Pin(SDA_PIN), scl=Pin(SCL_PIN), freq=400000)

# Helpers
w = lambda reg, val: i2c.writeto_mem(MPU_ADDR, reg, bytes([val]))
r = lambda reg, n: i2c.readfrom_mem(MPU_ADDR, reg, n)

# Init MPU-6050
try:
    w(0x6B, 0)    # Wake up
    w(0x1C, 0)    # +/- 2g
except Exception as e:
    print("MPU init error:", e)

FREE = 0.35  # g
IMP  = 2.20  # g
MIN_MS = 60
WIN_MS = 1500
COOLDOWN = 2000

ff = False
ff_t0 = 0
last_event = -COOLDOWN

print("MicroPython Fall Detector running at 50 Hz")
print("I2C: SDA=", SDA_PIN, " SCL=", SCL_PIN)


def lsb2g(v):
    return v / 16384.0

last_print = 0

while True:
    try:
        b = r(0x3B, 6)
    except Exception as e:
        print("I2C read error:", e)
        time.sleep_ms(100)
        continue

    ax = lsb2g(int.from_bytes(b[0:2], 'big', signed=True))
    ay = lsb2g(int.from_bytes(b[2:4], 'big', signed=True))
    az = lsb2g(int.from_bytes(b[4:6], 'big', signed=True))
    amag = math.sqrt(ax*ax + ay*ay + az*az)

    now = time.ticks_ms()

    if time.ticks_diff(now, last_print) >= 200:
        last_print = now
        print("ACC g:", round(ax,2), round(ay,2), round(az,2), "|a|=", round(amag,2))

    if time.ticks_diff(now, last_event) < COOLDOWN:
        time.sleep_ms(20)
        continue

    if not ff:
        if amag < FREE:
            ff = True
            ff_t0 = now
            print("-- free-fall start --")
    else:
        dt = time.ticks_diff(now, ff_t0)
        if IMP <= amag and MIN_MS <= dt <= WIN_MS:
            print("FALL_DETECTED")
            last_event = now
            ff = False
        elif dt > WIN_MS or (amag > 0.8 and dt > MIN_MS):
            ff = False

    time.sleep_ms(20) 

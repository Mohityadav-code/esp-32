from machine import Pin
import sys
import time
import uselect

# Pin mapping for L298N inputs
# Adjust these if your wiring order is different
IN1_PIN = 18  # Motor A input 1
IN2_PIN = 19  # Motor A input 2
IN3_PIN = 22  # Motor B input 1
IN4_PIN = 23  # Motor B input 2

in1 = Pin(IN1_PIN, Pin.OUT)
in2 = Pin(IN2_PIN, Pin.OUT)
in3 = Pin(IN3_PIN, Pin.OUT)
in4 = Pin(IN4_PIN, Pin.OUT)

# Helper functions

def stop():
    in1.off(); in2.off(); in3.off(); in4.off()
    print("STOP")

def forward():
    # Both motors forward
    in1.on();  in2.off()
    in3.on();  in4.off()
    print("FORWARD")

def backward():
    # Both motors backward
    in1.off(); in2.on()
    in3.off(); in4.on()
    print("BACKWARD")

def left():
    # Left motor backward, right motor forward
    in1.off(); in2.on()   # Left
    in3.on();  in4.off()  # Right
    print("LEFT")

def right():
    # Left motor forward, right motor backward
    in1.on();  in2.off()  # Left
    in3.off(); in4.on()   # Right
    print("RIGHT")

# Non-blocking character read from stdin
poll = uselect.poll()
poll.register(sys.stdin, uselect.POLLIN)

def read_char(timeout_ms=0):
    events = poll.poll(timeout_ms)
    if events:
        try:
            return sys.stdin.read(1)
        except Exception:
            return None
    return None

print("ESP32 L298N controller ready.")
print("Controls: Arrow keys or WASD. Space/Enter = STOP, q = quit.")
stop()

while True:
    ch = read_char(100)
    if not ch:
        continue

    # Handle ANSI escape sequences for arrow keys: ESC [ A/B/C/D
    if ch == "\x1b":
        ch1 = read_char(20)
        ch2 = read_char(20)
        if ch1 == "[" and ch2:
            if ch2 == "A":
                forward()
            elif ch2 == "B":
                backward()
            elif ch2 == "C":
                right()
            elif ch2 == "D":
                left()
        continue

    # Simple keys fallback (works in most terminals/Thonny input)
    c = ch.lower()
    if c == 'w':
        forward()
    elif c == 's':
        backward()
    elif c == 'a':
        left()
    elif c == 'd':
        right()
    elif c in (' ', '\r', '\n', 'x'):
        stop()
    elif c == 'q':
        stop()
        print("Exiting control loop. Reboot to run again.")
        break

    # Small debounce
    time.sleep_ms(10) 

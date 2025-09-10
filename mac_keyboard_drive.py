#!/usr/bin/env python3
"""
Mac keyboard controller for ESP32 L298N robot.
- Arrow keys (or WASD) control direction
- Space/Enter stops
- q quits

Requires: pip install pyserial pynput
"""
import sys
import time

# Lazy import so script can suggest installs clearly
try:
    import serial
except Exception:
    print("pyserial not found. Install with: pip3 install pyserial")
    sys.exit(1)

try:
    from pynput import keyboard
except Exception:
    print("pynput not found. Install with: pip3 install pynput")
    sys.exit(1)

PORT = '/dev/cu.usbserial-0001'  # Adjust if needed
BAUD = 115200

KEY_TO_CMD = {
    'up': 'w',
    'down': 's',
    'left': 'a',
    'right': 'd',
}

ALT_KEYS = {
    'w': 'w', 's': 's', 'a': 'a', 'd': 'd',
    'W': 'w', 'S': 's', 'A': 'a', 'D': 'd',
}

class Controller:
    def __init__(self, port: str, baud: int) -> None:
        self.port = port
        self.baud = baud
        self.ser = None

    def open(self) -> None:
        print(f"Connecting to {self.port} @ {self.baud}...")
        self.ser = serial.Serial(self.port, self.baud, timeout=0)
        time.sleep(2)
        print("Connected. Use arrow keys (or WASD). Space=STOP, q=quit.")

    def send(self, s: str) -> None:
        if not self.ser:
            return
        try:
            self.ser.write(s.encode('utf-8'))
        except serial.SerialException as e:
            print(f"Serial error: {e}")

    def stop(self) -> None:
        self.send(' ')

    def close(self) -> None:
        if self.ser and self.ser.is_open:
            self.ser.close()


def main() -> None:
    ctl = Controller(PORT, BAUD)
    try:
        ctl.open()
    except Exception as e:
        print(f"Failed to open port: {e}")
        print("Tip: Check the port with: ls /dev/tty.* /dev/cu.*")
        return

    def on_press(key):
        try:
            if key == keyboard.Key.up:
                ctl.send(KEY_TO_CMD['up'])
            elif key == keyboard.Key.down:
                ctl.send(KEY_TO_CMD['down'])
            elif key == keyboard.Key.left:
                ctl.send(KEY_TO_CMD['left'])
            elif key == keyboard.Key.right:
                ctl.send(KEY_TO_CMD['right'])
            elif key == keyboard.Key.space or key == keyboard.Key.enter:
                ctl.stop()
            elif hasattr(key, 'char') and key.char in ALT_KEYS:
                ctl.send(ALT_KEYS[key.char])
            elif key == keyboard.Key.esc:
                # ESC behaves like stop
                ctl.stop()
        except Exception:
            pass

    def on_release(key):
        # Optional: stop on key release for tap-to-move style
        # Comment this out if you want continuous motion until next command
        if key in (keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right):
            ctl.stop()
        if hasattr(key, 'char') and key.char in ('w','a','s','d','W','A','S','D'):
            ctl.stop()
        if key == keyboard.KeyCode.from_char('q'):
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            listener.join()
        finally:
            ctl.close()

if __name__ == '__main__':
    main() 

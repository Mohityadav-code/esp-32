#!/usr/bin/env python3
"""
Mac Fall Alarm - listens to ESP32 serial and plays a sound on FALL_DETECTED
"""
import subprocess
import time
import serial

PORT = '/dev/cu.usbserial-0001'
BAUD = 115200

SOUND_CMD = [
  'osascript', '-e',
  'beep 3'  # simple system beep; replace with audio file if preferred
]


def play_sound():
    try:
        subprocess.run(SOUND_CMD, check=False)
    except Exception:
        pass


def main():
    print('Listening on', PORT, 'at', BAUD)
    print('Will play a sound when FALL_DETECTED is received')
    try:
        with serial.Serial(PORT, BAUD, timeout=1) as ser:
            time.sleep(2)
            ser.reset_input_buffer()
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                print(line)
                if 'FALL_DETECTED' in line:
                    print('ALERT: FALL DETECTED!')
                    play_sound()
    except serial.SerialException as e:
        print('Serial error:', e)


if __name__ == '__main__':
    main() 

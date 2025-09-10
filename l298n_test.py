"""
L298N Motor Driver Test for ESP32
Pin connections:
- D5 (GPIO 5)   -> IN1
- D18 (GPIO 18) -> IN2  
- D19 (GPIO 19) -> IN3
- D21 (GPIO 21) -> IN4

Run this in Thonny to test your motor connections
"""

from machine import Pin
import time

# Initialize pins for L298N motor driver
# Motor A control pins
IN1 = Pin(5, Pin.OUT)   # D5
IN2 = Pin(18, Pin.OUT)  # D18

# Motor B control pins  
IN3 = Pin(19, Pin.OUT)  # D19
IN4 = Pin(21, Pin.OUT)  # D21

print("L298N Motor Test Starting...")
print("Pin Configuration:")
print("  IN1 -> GPIO 5 (D5)")
print("  IN2 -> GPIO 18 (D18)")
print("  IN3 -> GPIO 19 (D19)")
print("  IN4 -> GPIO 21 (D21)")
print("-" * 40)

def stop_all():
    """Stop all motors"""
    IN1.off()
    IN2.off()
    IN3.off()
    IN4.off()
    print("STOP - All motors off")

def motor_a_forward():
    """Motor A forward"""
    IN1.on()
    IN2.off()
    print("Motor A: Forward")

def motor_a_backward():
    """Motor A backward"""
    IN1.off()
    IN2.on()
    print("Motor A: Backward")

def motor_b_forward():
    """Motor B forward"""
    IN3.on()
    IN4.off()
    print("Motor B: Forward")

def motor_b_backward():
    """Motor B backward"""
    IN3.off()
    IN4.on()
    print("Motor B: Backward")

def both_forward():
    """Both motors forward"""
    IN1.on()
    IN2.off()
    IN3.on()
    IN4.off()
    print("Both Motors: Forward")

def both_backward():
    """Both motors backward"""
    IN1.off()
    IN2.on()
    IN3.off()
    IN4.on()
    print("Both Motors: Backward")

def turn_left():
    """Turn left - Motor A backward, Motor B forward"""
    IN1.off()
    IN2.on()
    IN3.on()
    IN4.off()
    print("Turning Left")

def turn_right():
    """Turn right - Motor A forward, Motor B backward"""
    IN1.on()
    IN2.off()
    IN3.off()
    IN4.on()
    print("Turning Right")

def test_sequence():
    """Run a test sequence"""
    delay = 2  # seconds between tests
    
    print("\n=== Starting Test Sequence ===\n")
    
    # Test Motor A
    print("Test 1: Motor A Forward")
    motor_a_forward()
    time.sleep(delay)
    
    print("Test 2: Motor A Backward")
    motor_a_backward()
    time.sleep(delay)
    
    print("Test 3: Motor A Stop")
    stop_all()
    time.sleep(1)
    
    # Test Motor B
    print("\nTest 4: Motor B Forward")
    motor_b_forward()
    time.sleep(delay)
    
    print("Test 5: Motor B Backward")
    motor_b_backward()
    time.sleep(delay)
    
    print("Test 6: Motor B Stop")
    stop_all()
    time.sleep(1)
    
    # Test both motors together
    print("\nTest 7: Both Motors Forward")
    both_forward()
    time.sleep(delay)
    
    print("Test 8: Both Motors Backward")
    both_backward()
    time.sleep(delay)
    
    # Test turning
    print("\nTest 9: Turn Left")
    turn_left()
    time.sleep(delay)
    
    print("Test 10: Turn Right")
    turn_right()
    time.sleep(delay)
    
    print("\nTest 11: Final Stop")
    stop_all()
    
    print("\n=== Test Sequence Complete ===\n")

def interactive_test():
    """Interactive test mode"""
    print("\n=== Interactive Test Mode ===")
    print("Commands:")
    print("  1 - Motor A Forward")
    print("  2 - Motor A Backward")
    print("  3 - Motor B Forward")
    print("  4 - Motor B Backward")
    print("  5 - Both Forward")
    print("  6 - Both Backward")
    print("  7 - Turn Left")
    print("  8 - Turn Right")
    print("  0 - Stop All")
    print("  t - Run test sequence")
    print("  q - Quit")
    print("-" * 40)
    
    while True:
        cmd = input("Enter command: ").strip().lower()
        
        if cmd == '1':
            motor_a_forward()
        elif cmd == '2':
            motor_a_backward()
        elif cmd == '3':
            motor_b_forward()
        elif cmd == '4':
            motor_b_backward()
        elif cmd == '5':
            both_forward()
        elif cmd == '6':
            both_backward()
        elif cmd == '7':
            turn_left()
        elif cmd == '8':
            turn_right()
        elif cmd == '0':
            stop_all()
        elif cmd == 't':
            test_sequence()
        elif cmd == 'q':
            stop_all()
            print("Exiting...")
            break
        else:
            print("Invalid command. Try again.")

# Main execution
if __name__ == "__main__":
    # Make sure motors are stopped initially
    stop_all()
    time.sleep(1)
    
    # You can choose which mode to run:
    # Option 1: Run automatic test sequence
    print("\nChoose test mode:")
    print("1. Automatic test sequence")
    print("2. Interactive control")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == '1':
        test_sequence()
    elif choice == '2':
        interactive_test()
    else:
        print("Running default test sequence...")
        test_sequence()
    
    # Make sure motors are stopped at the end
    stop_all()
    print("\nTest complete. Motors stopped.") 

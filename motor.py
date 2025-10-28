from machine import Pin, PWM
import time

# Replace with the GPIO pin connected to your motor driver / transistor
motor_pin = 23  

# Set up PWM on the motor pin at 1 kHz
motor = PWM(Pin(motor_pin), freq=1000)

try:
    while True:
        # Ramp motor speed up
        for duty in range(0, 1024, 50):  # 0-1023 for 10-bit PWM
            motor.duty(duty)
            print("Speed:", duty)
            time.sleep(0.1)
        
        # Ramp motor speed down
        for duty in range(1023, -1, -50):
            motor.duty(duty)
            print("Speed:", duty)
            time.sleep(0.1)
        
        # Stop motor for a second
        motor.duty(0)
        print("Motor stopped")
        time.sleep(1)

except KeyboardInterrupt:
    motor.duty(0)
    print("Test stopped")


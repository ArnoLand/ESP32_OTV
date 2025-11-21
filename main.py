from machine import Pin, PWM, time_pulse_us
import time
from enes100 import enes100

enes100.begin("Talhapins", "DATA", 582, 1116)

# ------------ Motor Class ------------
class Motor:
    def __init__(self, IN1_pin, IN2_pin, EN_pin, pwm=1000):
        self.in1 = Pin(IN1_pin, Pin.OUT)
        self.in2 = Pin(IN2_pin, Pin.OUT)
        self.enable = PWM(Pin(EN_pin))
        self.enable.freq(pwm)
        self.stop()

    def forward(self, speed=1.0):
        duty = int(speed * 65535)
        self.in1.value(1)
        self.in2.value(0)
        self.enable.duty_u16(duty)

    def reverse(self, speed=1.0):
        duty = int(speed * 65535)
        self.in1.value(0)
        self.in2.value(1)
        self.enable.duty_u16(duty)

    def stop(self):
        self.in1.value(0)
        self.in2.value(0)
        self.enable.duty_u16(0)

# ------------ Motor Controller ------------
class MotorController:
    def __init__(self):
        self.right = Motor(12, 13, 14)
        self.left  = Motor(25, 26, 27)

    def forward(self, speed=1.0):
        self.right.forward(speed)
        self.left.forward(speed)

    def reverse(self, speed=1.0):
        self.right.reverse(speed)
        self.left.reverse(speed)

    def spin_left(self, speed=0.6):
        self.left.reverse(speed)
        self.right.forward(speed)

    def spin_right(self, speed=0.6):
        self.left.forward(speed)
        self.right.reverse(speed)

    def stop(self):
        self.right.stop()
        self.left.stop()

# ------------ Ultrasonic Sensor ------------
class Ultrasonic:
    def __init__(self, trig_pin, echo_pin):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def get_distance(self):
        self.trig.value(0)
        time.sleep_us(2)
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        duration = time_pulse_us(self.echo, 1, 30000)
        if duration <= 0:
            return None
        distance = (duration / 2) * 0.0343  # cm
        return distance

# ------------ Turn to Target Angle ------------
def turn_to_angle(target_angle, motor, allowance=0.05, speed=0.4):
    """
    Turn robot to target_angle (radians) until within 'allowance'.
    """
    while True:
        error = target_angle - enes100.theta
        if abs(error) < allowance:
            motor.stop()
            return
        if error > 0:
            motor.spin_left(speed)
        else:
            motor.spin_right(speed)
        time.sleep(0.05)
        motor.stop()

# ------------ Move Forward Until Ultrasonic Detection ------------
def move_until_object(sensor, motor, threshold=6.0):
    """
    Move forward until ultrasonic sensor detects an object within threshold cm.
    """
    print("Moving forward until object detected...")
    while True:
        distance = sensor.get_distance()
        if distance is None:
            # nothing detected, keep moving forward
            motor.forward(0.4)
        elif distance <= threshold:
            motor.stop()
            print(f"Object detected at {distance:.2f} cm. Stopping.")
            return
        else:
            motor.forward(0.4)
        time.sleep(0.05)

# ------------ MAIN ------------
def main():
    motor = MotorController()
    sensor = Ultrasonic(23, 36)  # your original ultrasonic pins

    print("Waiting for ENES100 connection...")
    while not enes100.is_connected():
        time.sleep(1)
    print("Connected!")

    # Wait for ArUco detection
    while not enes100.is_visible:
        time.sleep(0.5)

    # ----- Turn to 0 radians -----
    print("Turning to 0 radians...")
    turn_to_angle(0.0, motor)
    print("Aligned to 0 radians.")

    # ----- Move forward until object -----
    move_until_object(sensor, motor, threshold=6.0)

    print("Test complete!")

if __name__ == "__main__":
    main()

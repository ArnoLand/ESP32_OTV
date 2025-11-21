from machine import Pin, PWM
import time

# Motor class
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

# Motor controller
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


# ---------- Test ----------
motor = MotorController()

print("Forward 2 seconds...")
motor.forward(0.5)
time.sleep(2)
motor.stop()
time.sleep(1)

print("Reverse 2 seconds...")
motor.reverse(0.5)
time.sleep(2)
motor.stop()
time.sleep(1)

print("Spin left 2 seconds...")
motor.spin_left(0.5)
time.sleep(2)
motor.stop()
time.sleep(1)

print("Spin right 2 seconds...")
motor.spin_right(0.5)
time.sleep(2)
motor.stop()

print("Motor test complete!")

from machine import Pin, PWM
import time

# ------------------- Motor Class -------------------
class Motor:
    def __init__(self, IN1_pin, IN2_pin, EN_pin, pwm_freq=1000):
        self.in1 = Pin(IN1_pin, Pin.OUT)
        self.in2 = Pin(IN2_pin, Pin.OUT)
        self.enable = PWM(Pin(EN_pin))
        self.enable.freq(pwm_freq)

        # Ensure motor is stopped initially
        self.in1.value(0)
        self.in2.value(0)
        self.enable.duty_u16(0)
        time.sleep(0.05)  # small delay to let PWM initialize

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


# ------------------- Motor Controller -------------------
class MotorController:
    def __init__(self):
        # Initialize left motor first for reliable PWM
        self.left  = Motor(25, 26, 27)
        self.right = Motor(13, 14, 18)

    def forward(self, speed=1.0):
        self.left.forward(speed)
        self.right.forward(speed)

    def reverse(self, speed=1.0):
        self.left.reverse(speed)
        self.right.reverse(speed)

    def spin_left(self, speed=0.5):
        self.left.reverse(speed)
        time.sleep(0.01)  # ensure PWM is set
        self.right.forward(speed)

    def spin_right(self, speed=0.5):
        self.left.forward(speed)
        time.sleep(0.01)
        self.right.reverse(speed)

    def stop(self):
        self.left.stop()
        self.right.stop()


# ------------------- Main Test Sequence -------------------
motor = MotorController()


# 3. Spin left
motor.spin_left(0.5)
time.sleep(3.2)
motor.stop()
time.sleep(1)
motor.spin_left(0.5)
time.sleep(3.2)
motor.stop()
time.sleep(1)
motor.spin_left(0.5)
time.sleep(3.2)
motor.stop()
time.sleep(1)




from machine import Pin, PWM
import time

class Servo:
    def __init__(self, pin_num, min_duty=26, max_duty=123):
        self.servo = PWM(Pin(pin_num), freq=50)
        self.min_duty = min_duty
        self.max_duty = max_duty

         def set_angle(self, angle):
        duty = int((angle / 180) * (self.max_duty - self.min_duty) + self.min_duty)
        self.servo.duty(duty)
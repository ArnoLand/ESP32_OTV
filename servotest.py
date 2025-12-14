from machine import Pin, PWM
import time

# ---------- Servo ----------
class Servo:
    def __init__(self, pin_num, freq=50):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(freq)

    def _write_duty_us(self, us):
        duty = int((us / 20000) * 65535)
        self.pwm.duty_u16(duty)

    def forward(self, speed=1.0):
        speed = max(0.0, min(1.0, speed))
        us = 1500 + 500 * speed
        self._write_duty_us(us)

    def reverse(self, speed=1.0):
        speed = max(0.0, min(1.0, speed))
        us = 1500 - 500 * speed
        self._write_duty_us(us)

    def stop(self):
        self._write_duty_us(1500)

# ---------- Test ----------
servo = Servo(17)  

print("Servo test starting... observe motion!")

servo.reverse(0.5)
time.sleep(1.8)
servo.stop()
time.sleep(1)
servo.forward(0.5)
time.sleep(1.8)
servo.stop()
time.sleep(1)


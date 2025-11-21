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
servo = Servo(2)  

print("Servo test starting... observe motion!")

while True:
    # Forward sweep
    servo.forward(1.0)
    time.sleep(1)

    # Reverse sweep
    servo.reverse(1.0)
    time.sleep(1)

    # Stop
    servo.stop()
    time.sleep(1)

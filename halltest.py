from machine import Pin, ADC, PWM
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


# ---------- DIGITAL HALL SENSOR ----------
class HallSensor:
    def __init__(self, hall_pin):
        self.pin = Pin(hall_pin, Pin.IN)

    def is_magnet_detected(self):
        return self.pin.value() == 0

# ---------- Test Setup ----------
hall1 = HallSensor(32)
hall2 = HallSensor(33)
servo = Servo(17)

#Move servo briefly
servo.reverse(0.5)
time.sleep(1.8)
servo.stop()
time.sleep(1.0)

print("Starting Hall Effect Sensor Test...")
time.sleep(1)

# ---------- Main Loop ----------
servo.forward(0.5)
time.sleep(1.8)
servo.stop()
time.sleep(0.2)

while True:
    detected1 = hall1.is_magnet_detected()
    detected2 = hall2.is_magnet_detected()
    print(detected1)
    print(detected2)
    time.sleep(0.3)
   


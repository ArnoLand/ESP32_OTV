from machine import Pin, PWM, time_pulse_us
import time

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

# ------------ Ultrasonic Reaction Test ------------
sensor = Ultrasonic(23, 36)
THRESHOLD = 10  # cm

print("Ultrasonic motor test starting... observe behavior!")

while True:
    dist = sensor.get_distance()
    print(dist)
    time.sleep(0.1)

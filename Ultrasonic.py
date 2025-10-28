from machine import Pin, time_pulse_us
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
    
        if duration < 0:
            return -1
        
        distance = (duration / 2) * 0.343
        return distance

    def check_distance(self):
        distance = self.get_distance()
        if distance > 0 and distance <= 150:
            return True
        else:
            return False

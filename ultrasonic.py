from machine import Pin, time_pulse_us
import time
#This is the file for the ultrasonic sensor
class Ultrasonic:
    #defining the trig and echo pins of the sensor
    def __init__(self, trig_pin, echo_pin):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
    #get_distance is a helper method that will return the distance
    def get_distance(self):
        self.trig.value(0)
        time.sleep_us(2)
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        duration = time_pulse_us(self.echo, 1, 30000)  # 30 ms timeout
        if duration <= 0:
            return None

        distance = (duration / 2) * 0.0343
        return distance
    #this is the main method of this file, returns true if OTV is within a set threshold value
    def check_distance(self, threshold):
        """Return True if object is within threshold (cm)."""
        distance = self.get_distance()
        return distance is not None and distance <= threshold
    
        


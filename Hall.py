from machine import Pin

class HallSensor:
    def __init__(self, pin_num):
        self.pin = Pin(pin_num, Pin.IN)

    def is_magnet_detected(self):
        return self.pin.value() == 1  

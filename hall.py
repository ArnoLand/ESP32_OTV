from machine import Pin

class HallSensor:
    def __init__(self, hall_pin):
        self.pin = Pin(hall_pin, Pin.IN)

    def is_magnet_detected(self):
        return self.pin.value() == 1

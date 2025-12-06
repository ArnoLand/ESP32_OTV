from machine import Pin, ADC
import time

class HallSensor:
    def __init__(self, hall_pin, threshold=400, neutral=2048):
        self.adc = ADC(Pin(hall_pin))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        self.threshold = threshold
        self.neutral = neutral

    def is_magnet_detected(self):
        detections = 0
        for _ in range(5):
            raw = self.adc.read()
            if abs(raw - self.neutral) > self.threshold:
                detections += 1
            time.sleep_ms(10)
        return detections >= 3



# HALL SENSOR TEST
#change hall_pin to whatever the hall effect is connected to
#if this doesnt work try playing around with the threshold value
hall = HallSensor(hall_pin=34, threshold=400, neutral=2048) 

print("Starting Hall Effect Sensor Test...")
time.sleep(1)

while True:
    raw_value = hall.adc.read()
    detected = hall.is_magnet_detected()

    print("Raw ADC:", raw_value, "| Magnet:", "YES" if detected else "no")

    time.sleep(0.3)
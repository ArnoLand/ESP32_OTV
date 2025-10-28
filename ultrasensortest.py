from machine import Pin, time_pulse_us
import time

trig = Pin(13, Pin.OUT)
echo = Pin(34, Pin.IN)
led = Pin(25, Pin.OUT)

def get_distance():
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    duration = time_pulse_us(echo, 1, 30000)
    
    if duration < 0:
        return -1
    
    distance = (duration / 2) * 0.343
    return distance

def check_distance():
    distance = get_distance()
    if distance > 0 and distance <= 150:
        return True
    else:
        return False

while True:
    close = check_distance()
    
    if close:
        led.value(1)
        print("LED ON: Object detected")
    else:
        led.value(0)
        print("LED OFF: No object")
        
    time.sleep(0.5)

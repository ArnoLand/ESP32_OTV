from machine import Pin, time_pulse_us
import time

trig = Pin(13, Pin.OUT)
echo = Pin(34, Pin.IN)
led = Pin(25, Pin.OUT)

def getDistance():
    trig.value(0)
    trig.sleep_us(2)
    trig.value(1)
    trig.sleep_us(10)
    trig.value(0)
    
    duration = time_pulse_us(echo, 1, 30000)
    
    if duration < 0:
        return -1
    
    distance = (duration/2)*0.343
    return distance_mm

def check_distance():
    distance = getDistance()
    if distance > 0 and distance <= 150:
        return true
    else:
        return false
    
    while True:
        close = check_distance()
        
        if close:
            led.value(1)
            print("ts worked twin")
        else:
            led.value(0)
            print("u cooked vro give up atp")
            
        time.sleep(0.5)


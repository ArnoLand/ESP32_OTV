from machine import Pin
import time

hall = Pin(35, Pin.IN)
led = Pin(25, Pin.OUT)

while True:
    sensor_value = hall.value()  
    
    if sensor_value == 0:  
        led.value(1)        
        print("ts a magnet bro")
    else:
        led.value(0)     
        print("ts not a magnet twin")
    
    time.sleep(0.2)


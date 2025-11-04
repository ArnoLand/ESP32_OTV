from machine import Pin
import time

# Change 4 to your GPIO pin number
hall = Pin(4, Pin.IN)

print("Testing Hall effect sensor...")

while True:
    value = hall.value()
    if value == 1:
        print("Magnet NOT detected")
    else:
        print("Magnet detected!")
    time.sleep(0.5)

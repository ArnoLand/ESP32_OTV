from machine import Pin
import time

# --- Pin Setup ---
HALL_PIN = 27       # Pin connected to OUT of Hall sensor
LED_PIN = 25        # LED indicator pin (optional)

hall = Pin(HALL_PIN, Pin.IN)   # read sensor output
led = Pin(LED_PIN, Pin.OUT)    # LED to show detection

# --- Main Loop ---
while True:
    sensor_value = hall.value()  # read HIGH or LOW (1 or 0)
    
    if sensor_value == 0:  # 0 means magnet detected
        led.value(1)
        print("Magnet detected!")
    else:  # 1 means no magnetic field nearby
        led.value(0)
        print("No magnet.")
    
    time.sleep(0.2)

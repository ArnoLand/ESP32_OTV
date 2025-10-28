from machine import Pin, time_pulse_us
import time

# --- Pin Setup ---
TRIG_PIN = 13
ECHO_PIN = 34
LED_PIN = 25  # choose your LED pin

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
led = Pin(LED_PIN, Pin.OUT)

def get_distance_mm():
    """Measure distance in millimeters."""
    # Send a 10 µs trigger pulse
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    # Measure the echo pulse width
    duration = time_pulse_us(echo, 1, 30000)  # timeout 30 ms
    
    if duration < 0:  # no echo received
        return -1
    
    # Convert time to distance (mm)
    distance_mm = (duration / 2) * 0.343
    return distance_mm

def check_object_close(threshold_mm=150):
    distance = get_distance_mm()
    if distance > 0 and distance <= threshold_mm:
        return True
    return False

# --- Main Loop ---
while True:
    object_close = check_object_close(150)
    
    if object_close:
        led.value(1)  # turn LED ON
        print("🚨 Object detected within 150 mm!")
    else:
        led.value(0)  # turn LED OFF
        print("No object nearby.")
    
    time.sleep(0.5)

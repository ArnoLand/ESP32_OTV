from machine import Pin, Timer
import time

signal_pin = Pin(33, Pin.IN)

last_edge_time = 0
high_time = 0
low_time = 0
last_state = 0

def edge_handler(pin):
    global last_edge_time, high_time, low_time, last_state
    current_time = time.ticks_us()
    state = pin.value()

    if state == 1 and last_state == 0:
        # rising edge: low period ended
        low_time = time.ticks_diff(current_time, last_edge_time)
        last_edge_time = current_time

    elif state == 0 and last_state == 1:
        # falling edge: high period ended
        high_time = time.ticks_diff(current_time, last_edge_time)
        last_edge_time = current_time

    last_state = state

signal_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=edge_handler)

print("Measuring duty cycle...\n")

while True:
    if high_time > 0 and low_time > 0:
        total = high_time + low_time
        duty = high_time / total * 100
        print("Duty Cycle: {:.2f}%   High: {}us   Low: {}us".format(duty, high_time, low_time))
    time.sleep(0.2)

from machine import Pin, PWM, ADC
import time
from enes100 import enes100

class Servo:
    def __init__(self, pin_num, freq=50):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(freq)

    def _write_duty_us(self, us):
        duty = int((us / 20000) * 65535)
        self.pwm.duty_u16(duty)

    def forward(self, speed=1.0):
        speed = max(0.0, min(1.0, speed))
        us = 1500 + 500 * speed
        self._write_duty_us(us)

    def reverse(self, speed=1.0):
        speed = max(0.0, min(1.0, speed))
        us = 1500 - 500 * speed
        self._write_duty_us(us)

    def stop(self):
        self._write_duty_us(1500)
        

# ------------------- Motor Class -------------------
class Motor:
    def __init__(self, IN1_pin, IN2_pin, EN_pin, pwm_freq=1000):
        self.in1 = Pin(IN1_pin, Pin.OUT)
        self.in2 = Pin(IN2_pin, Pin.OUT)
        self.enable = PWM(Pin(EN_pin))
        self.enable.freq(pwm_freq)
        self.stop()
        time.sleep(0.05)

    def forward(self, speed=1.0):
        self.in1.value(1)
        self.in2.value(0)
        self.enable.duty_u16(int(speed * 65535))

    def reverse(self, speed=1.0):
        self.in1.value(0)
        self.in2.value(1)
        self.enable.duty_u16(int(speed * 65535))

    def stop(self):
        self.in1.value(0)
        self.in2.value(0)
        self.enable.duty_u16(0)


# ------------------- Motor Controller -------------------
class MotorController:
    def __init__(self):
        self.left  = Motor(25, 26, 27)
        self.right = Motor(13, 14, 18)

    def forward(self, speed=1.0):
        self.left.forward(speed)
        self.right.forward(speed)

    def reverse(self, speed=1.0):
        self.left.reverse(speed)
        self.right.reverse(speed)

    def spin_left(self, speed=0.5):
        self.left.reverse(speed)
        self.right.forward(speed)

    def spin_right(self, speed=0.5):
        self.left.forward(speed)
        self.right.reverse(speed)

    def stop(self):
        self.left.stop()
        self.right.stop()


# ------------------- Continuous Run Function -------------------
def run_motor(controller, motor_func, speed, duration):
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
        motor_func(speed)
        time.sleep(0.05)
    controller.stop()
    time.sleep(1)


# ------------------- Main Sequence -------------------
#enes100.begin("Talhapins", "DATA", 381, 1116)
motor = MotorController()
servo = Servo(17)

isNorth = enes100.y > 1

time.sleep(1.0)
servo.stop()
time.sleep(0.5)
servo.reverse(0.5)
time.sleep(1.7)
servo.stop()
time.sleep(1.0)

# Magnet detection
detected = False
for i in range(10):
    detected = hall.is_magnet_detected()
    if detected:
        #enes100.mission('MAGNETISM', 'MAGNETIC')
        break
    time.sleep(0.3)

#if not detected:
    #enes100.mission('MAGNETISM', 'NOT_MAGNETIC')

# Servo movements
servo.forward(0.5)
time.sleep(1.7)
servo.stop()
time.sleep(1.0)

# Motor sequence
if isNorth == False:
    run_motor(motor, motor.reverse, 0.5, 2.5)  # backwards only
    run_motor(motor, motor.spin_right, 0.5, 5.9)
    run_motor(motor, motor.forward, 0.5, 5.0)
    run_motor(motor, motor.forward, 0.5, 3.5)
    
run_motor(motor, motor.reverse, 0.5, 2.5) 
run_motor(motor, motor.spin_right, 0.5, 1.2)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 2)
run_motor(motor, motor.spin_right, 0.5, 2.0)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.spin_right, 0.5, 2.8)
run_motor(motor, motor.forward, 0.5, 3)
run_motor(motor, motor.spin_left, 0.5, 1.8)
servo.reverse(0.5)
time.sleep(2.0)
servo.stop()
time.sleep(1.0)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 5)
run_motor(motor, motor.forward, 0.5, 5)

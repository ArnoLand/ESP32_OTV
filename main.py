from machine import Pin, PWM
import time

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
def run_motor(motor_func, speed, duration):
    """
    Continuously refresh the motor PWM while moving for the given duration.
    Avoids long blocking sleep.
    """
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
        motor_func(speed)
        time.sleep(0.05)  # small delay to refresh PWM
    motor.stop()
    time.sleep(1)  # short pause between moves

# ------------------- Main Sequence -------------------
motor = MotorController()

# Example movements: speeds at 0.5
run_motor(motor.reverse, 0.5, 2.6)      # 9 inches
run_motor(motor.spin_left, 0.5, 2.8)    # 11 inches
run_motor(motor.forward, 0.5, 3.2)      # 11 inches
run_motor(motor.spin_right, 0.5, 2.8)   # 11 inches
run_motor(motor.forward, 0.5, 8.2)      # 28 inches
run_motor(motor.spin_right, 0.5, 2.8)   # 11 inches
run_motor(motor.forward, 0.5, 36)       # 123 inches
run_motor(motor.spin_right, 0.5, 2.8)   # 11 inches
run_motor(motor.forward, 0.5, 3)        # 14 inches
run_motor(motor.spin_left, 0.5, 2.8)    # 11 inches
run_motor(motor.forward, 0.5, 10)        # 10 inches


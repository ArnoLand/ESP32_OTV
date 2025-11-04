from machine import Pin, PWM, time_pulse_us
import time

# -----------------------------
# Ultrasonic Sensor Class
# -----------------------------
class Ultrasonic:
    def __init__(self, trig_pin, echo_pin):
        self.trig = Pin(trig_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)

    def get_distance(self):
        self.trig.value(0)
        time.sleep_us(2)
        self.trig.value(1)
        time.sleep_us(10)
        self.trig.value(0)

        duration = time_pulse_us(self.echo, 1, 30000)  # 30 ms timeout
        if duration <= 0:
            return None

        distance = (duration / 2) * 0.0343  # cm
        return distance

    def check_distance(self, threshold):
        """Return True if object is within threshold (cm)."""
        distance = self.get_distance()
        return distance is not None and distance <= threshold


# -----------------------------
# Hall Sensor Class
# -----------------------------
class HallSensor:
    def __init__(self, hall_pin):
        self.pin = Pin(hall_pin, Pin.IN)

    def is_magnet_detected(self):
        return self.pin.value() == 1


# -----------------------------
# Servo Motor Class
# -----------------------------
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


# -----------------------------
# RP Controller Class
# -----------------------------
class RPController:
    def __init__(self, trig_pin, echo_pin, servo_pin, hall_pin, servo_rpm, pinion_teeth, rack_teeth):
        self.sensor = Ultrasonic(trig_pin, echo_pin)
        self.servo = Servo(servo_pin)
        self.hall = HallSensor(hall_pin)
        
        self.spin_time = self._calculate_spin_time(servo_rpm, pinion_teeth, rack_teeth)
        self.speed = 0.8  

    def _calculate_spin_time(self, servo_rpm, pinion_teeth, rack_teeth):
        rotations_per_sec = servo_rpm / 60.0
        travel_ratio = rack_teeth / pinion_teeth
        spin_time = travel_ratio / rotations_per_sec
        return spin_time

    def run(self):
        distance = self.sensor.get_distance()

        if distance is not None:
            print("Distance:", round(distance, 2), "cm")

            if distance <= 6.0:  # 6 cm threshold
                print("We starting twin")
                self.servo.forward(self.speed)
                time.sleep(self.spin_time)
                self.servo.stop()

                # Pause to read the Hall sensor
                print("Pausing to check Hall sensor...")
                time.sleep(2)
                
                if self.hall.is_magnet_detected():
                    print("Magnet detected!")
                else:
                    print("No magnet detected.")
                
                self.servo.reverse(self.speed)
                time.sleep(self.spin_time)
                self.servo.stop()
                print("Complete")
            else:
                print("Object too far — no action")
        else:
            print("No valid reading from ultrasonic sensor")


# -----------------------------
# Main Program
# -----------------------------
def main():
    controller = RPController(
        trig_pin=13,
        echo_pin=34,
        servo_pin=2,
        hall_pin=35,
        servo_rpm=130,
        pinion_teeth=18,
        rack_teeth=25
    )
    
    while True:
        controller.run()
        time.sleep(0.5)  # small delay between loops


if __name__ == "__main__":
    main()

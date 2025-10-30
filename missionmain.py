from ultrasonic import Ultrasonic
from servo import Servo
from hall import HallSensor 
import time

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

            if distance <= 6.0:  # 60 mm
                print("We starting twin")
                self.servo.forward(self.speed)
                time.sleep(self.spin_time)
                self.servo.stop()
                # Pause for a moment to read the Hall sensor
                print("Pausing to check Hall sensor...")
                time.sleep(2)   

                # Read the Hall sensor
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

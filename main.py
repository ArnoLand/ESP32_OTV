from ultrasonic import Ultrasonic
from servo import Servo
from hall import HallSensor
from missionmain import RPController
import time

def main():
    controller = RPController(
        trig_pin=13,
        echo_pin=34,
        servo_pin=2,
        hall_pin=35;
        servo_rpm=130,
        pinion_teeth=18,
        rack_teeth=25
    )
    
    controller.run()


if __name__ == "__main__":
    main()
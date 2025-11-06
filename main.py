from machine import Pin, PWM, time_pulse_us
import time
from enes100 import enes100
enes100.begin("Talhapins", "DATA", 582, 1116)

#Motor Class

class Motor:
    def __init__(self, IN1_pin, IN2_pin, EN_pin, pwm=1000):
        self.in1 = Pin(IN1_pin, Pin.OUT)
        self.in2 = Pin(IN2_pin, Pin.OUT)
        self.enable = PWM(Pin(EN_pin))
        self.enable.freq(pwm)
        self.stop()
    
    def forward(self, speed=1.0):
        duty = int(speed * 65535)
        self.in1.value(1)
        self.in2.value(0)
        self.enable.duty_u16(duty)
    
    def reverse(self, speed=1.0):
        duty = int(speed * 65535)
        self.in1.value(0)
        self.in2.value(1)
        self.enable.duty_u16(duty)
    
    def stop(self):
        self.in1.value(0)
        self.in2.value(0)
        self.enable.duty_u16(0)


# Motor Controller Class

class MotorController:
    def __init__(self):
        self.front_left = Motor(IN1_pin=21, IN2_pin=22, EN_pin=23)
        self.rear_left = Motor(IN1_pin=25, IN2_pin=26, EN_pin=27)
        self.front_right = Motor(IN1_pin=32, IN2_pin=33, EN_pin=19)
        self.rear_right = Motor(IN1_pin=18, IN2_pin=17, EN_pin=16)
    
    def forward(self, speed=1.0):
        self.front_left.forward(speed)
        self.rear_left.forward(speed)
        self.front_right.forward(speed)
        self.rear_right.forward(speed)

    def reverse(self, speed=1.0):
        self.front_left.reverse(speed)
        self.rear_left.reverse(speed)
        self.front_right.reverse(speed)
        self.rear_right.reverse(speed)
    
    def spin_left(self, speed=0.5):  # Added colon
        self.front_left.reverse(speed)
        self.rear_left.reverse(speed)
        self.front_right.forward(speed)
        self.rear_right.forward(speed)
    
    def spin_right(self, speed=0.7):
        self.front_left.forward(speed)
        self.rear_left.forward(speed)
        self.front_right.reverse(speed)
        self.rear_right.reverse(speed)
    
    def stop(self):
        self.front_left.stop()
        self.rear_left.stop()
        self.front_right.stop()
        self.rear_right.stop()

# Ultrasonic Sensor Class

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
        distance = self.get_distance()
        return distance is not None and distance <= threshold

# Hall Sensor Class

class HallSensor:
    def __init__(self, hall_pin):
        self.pin = Pin(hall_pin, Pin.IN)

    def is_magnet_detected(self):
        count = 0
        for i in range(5):
            if self.pin.value() == 1:
                count += 1
            time.sleep_ms(5)  
        return count >= 3
    
#Servo Motor Class

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



# RP Controller Class

class RPController:
    def __init__(self):
        self.sensor = Ultrasonic(trig_pin = 13, echo_pin = 34)
        self.servo = Servo(pin_num = 2)
        self.hall = HallSensor(hall_pin = 35)
        
        self.spin_time = self._calculate_spin_time()
        self.speed = 0.8  

    def _calculate_spin_time(self):
        rotations_per_sec = 130 / 60.0
        travel_ratio = 25 / 18
        spin_time = travel_ratio / rotations_per_sec
        return spin_time

    def run(self):
        distance = self.sensor.get_distance()
        if distance is not None and distance <= 6.0:  
            print("Mission Starting")
            self.servo.forward(self.speed)
            time.sleep(self.spin_time)
            self.servo.stop()

            print("Pausing to check Hall sensor...")
            time.sleep(5)
                
            if self.hall.is_magnet_detected():
                print("Magnet detected!")
                enes100.mission('MAGNETISM', 'MAGNETIC')
            else:
                print("No magnet detected.")
                enes100.mission('MAGNETISM', 'NOT_MAGNETIC') 
                
            self.servo.reverse(self.speed)
            time.sleep(self.spin_time)
            self.servo.stop()
            print("Complete")
            
        else:
            print("mission failed")




# Main Program

def main():
    mission = RPController()
    motor = MotorController()
    
    # Wait for WiFi connection
    print("Waiting for connection...")
    while not enes100.is_connected():
        time.sleep(1)
    print("Connected!")
    
    # Wait for ArUco
    while not enes100.is_visible:
        time.sleep(0.5)
    print(f"Starting at x={enes100.x:.2f}, y={enes100.y:.2f}, theta={enes100.theta:.2f}")
    
    # Step 1: Align to 0 degrees (face the pylon)
    print("Aligning to 0 degrees...")
    angle = enes100.theta
    
    while abs(angle) > 0.05:
        if angle > 0:
            motor.spin_left(0.5)
        else:
            motor.spin_right(0.5)
        time.sleep(0.1)
        angle = enes100.theta
    
    motor.stop()
    print(f"Aligned! Angle: {angle:.3f} rad")
    
    # Step 2: Drive forward until ultrasonic detects pylon
    print("Searching for pylon...")
    distance = mission.sensor.get_distance()
    
    while distance is None:
        motor.forward(0.7)
        time.sleep(0.2)
        distance = mission.sensor.get_distance()
    
    motor.stop()
    print(f"Pylon detected at {distance:.1f}cm!")
    
    # Step 3: Approach to 6cm with angle correction
    print("Approaching pylon...")
    correction_count = 0
    
    while distance is not None and distance > 6.0:
        # Correct angle every 5 iterations
        correction_count += 1
        if correction_count >= 5:
            angle = enes100.theta
            if abs(angle) > 0.15:  
                motor.stop()
                print("Correcting angle...")
                while abs(angle) > 0.05:
                    if angle > 0:
                        motor.spin_left(0.4)
                    else:
                        motor.spin_right(0.4)
                    time.sleep(0.1)
                    angle = enes100.theta
                motor.stop()
            correction_count = 0
        
        # Adjust speed based on distance
        if distance > 20:
            speed = 0.6
        elif distance > 10:
            speed = 0.4
        else:
            speed = 0.25
        
        motor.forward(speed)
        time.sleep(0.2)
        distance = mission.sensor.get_distance()
    
    motor.stop()
    print(f"Reached target! Distance: {distance:.1f}cm")
    
    # Step 4: Run rack and pinion mission
    print("Running mission")
    mission.run()
    
    print("MISSION COMPLETE!")


if __name__ == "__main__":
    main()

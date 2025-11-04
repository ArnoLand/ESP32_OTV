from machine import Pin, PWM
import time


class Motor:    
    def __init__(self, in1_pin, in2_pin, enable_pin, pwm_freq=1000):
       
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.enable = PWM(Pin(enable_pin))
        self.enable.freq(pwm_freq)
        self.stop()
    
    def forward(self, speed=1.0):
    
        speed = max(0.0, min(1.0, speed))  # Clamp between 0 and 1
        duty = int(speed * 65535)  # Convert to 16-bit duty cycle
        
        self.in1.value(1)
        self.in2.value(0)
        self.enable.duty_u16(duty)
    
    def reverse(self, speed=1.0):
        
        speed = max(0.0, min(1.0, speed))
        duty = int(speed * 65535)
        
        self.in1.value(0)
        self.in2.value(1)
        self.enable.duty_u16(duty)
    
    def stop(self):
        
        self.in1.value(0)
        self.in2.value(0)
        self.enable.duty_u16(0)
    
    def coast(self):
        
        self.in1.value(1)
        self.in2.value(1)
        self.enable.duty_u16(0)


class QuadMotorController:
   
    
    def __init__(self):
      
        # Left side motors (H-Bridge 1)
        self.front_left = Motor(in1_pin=21, in2_pin=22, enable_pin=23)
        self.rear_left = Motor(in1_pin=25, in2_pin=26, enable_pin=27)
        
        # Right side motors (H-Bridge 2)
        self.front_right = Motor(in1_pin=32, in2_pin=33, enable_pin=19)
        self.rear_right = Motor(in1_pin=18, in2_pin=17, enable_pin=16)
    
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
    
    def turn_left(self, speed=1.0, turn_ratio=0.5):
       
        turn_ratio = max(0.0, min(1.0, turn_ratio))
        # Left side slowed down
        self.front_left.forward(speed * turn_ratio)
        self.rear_left.forward(speed * turn_ratio)
        # Right side full speed
        self.front_right.forward(speed)
        self.rear_right.forward(speed)
    
    def turn_right(self, speed=1.0, turn_ratio=0.5):
        
        turn_ratio = max(0.0, min(1.0, turn_ratio))
        # Left side full speed
        self.front_left.forward(speed)
        self.rear_left.forward(speed)
        # Right side slowed down
        self.front_right.forward(speed * turn_ratio)
        self.rear_right.forward(speed * turn_ratio)
    
    def spin_left(self, speed=0.7):
        
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

    
# -----------------------------
# Usage Example
# -----------------------------
def main():
    # Create controller with all 4 motors
    motors = QuadMotorController()
    
    try:
        print("Testing 4-motor movements...")
        
        # Drive forward
        print("Forward")
        motors.forward(0.7)
        time.sleep(2)
        motors.stop()
        time.sleep(1)
        
        # Drive backward
        print("Reverse")
        motors.reverse(0.7)
        time.sleep(2)
        motors.stop()
        time.sleep(1)
        
        # Turn left (gentle)
        print("Turn left")
        motors.turn_left(0.7, turn_ratio=0.5)
        time.sleep(2)
        motors.stop()
        time.sleep(1)
        
        # Turn right (gentle)
        print("Turn right")
        motors.turn_right(0.7, turn_ratio=0.5)
        time.sleep(2)
        motors.stop()
        time.sleep(1)
        
        # Spin left in place
        print("Spin left")
        motors.spin_left(0.6)
        time.sleep(2)
        motors.stop()
        time.sleep(1)
        
        # Spin right in place
        print("Spin right")
        motors.spin_right(0.6)
        time.sleep(2)
        motors.stop()
        time.sleep(1)
        

        
        print("Test complete!")
 


if __name__ == "__main__":
    main()
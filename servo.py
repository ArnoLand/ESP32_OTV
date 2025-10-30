from machine import Pin, PWM
#this is the class for the servo motor
class Servo:
    #defining PWM Pin because we need pulse width modulation
    def __init__(self, pin_num, freq=50):
        self.pwm = PWM(Pin(pin_num))
        self.pwm.freq(freq)
    #math for getting the correct duty
    def _write_duty_us(self, us):
        duty = int((us / 20000) * 65535)  
        self.pwm.duty_u16(duty)

    def forward(self, speed=1.0):
        #the speed has a max of 1.0
        speed = max(0.0, min(1.0, speed))
        us = 1500 + 500 * speed
        self._write_duty_us(us)

    def reverse(self, speed=1.0):
        speed = max(0.0, min(1.0, speed))
        us = 1500 - 500 * speed
        self._write_duty_us(us)

    def stop(self):
        self._write_duty_us(1500)


#Program designed to control "Spider-Plotter" a motor driven wall plotting device
#Here GPIO pins are defined to handle Stepper Motors, and stepper motor control is defined
#Dominik Donocik October 2013

"""
Library for motor control
"""

import time

MOTOR_LEFT = 0
MOTOR_RIGHT = 1


class Driver:
    def __init__(self):
        self.motor_resolution = 1
        self.motor_steps = [0, 0]
    
    def step_motor(self, motor, steps):
        pass
    
    def number_steps(self, motor):
        return self.motor_steps[motor]

# Dummy driver class for testing.
class DummyDriver(Driver):
    def step_motor(self, motor, steps):
        print "Stepping motor %i with %f steps" % (motor, steps)


try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None

class PiDriver(Driver):
    def __init__(self):
        if GPIO is None:
            raise Exception('GPIO module not found- probably not a Raspberry Pi')
        
        super().__init__()
        self.direction_pins = [18, 26]
        self.step_pins = [16, 24]
        self.setup_gpio()
    
    def __del__(self):
        GPIO.cleanup()
    
    def setup_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        
        for i in xrange(0, 1):
            GPIO.setup(self.direction_pins[i], GPIO.OUT, initial=GPIO.LOW)
            GPIO.setup(self.step_pins[i], GPIO.OUT, initial=GPIO.LOW)
    
    def write_pin(self, pin_number, level):
        GPIO.output(pin_number, level)
        time.sleep(0.001)
    
    def step_motor(self, motor = 0, steps=1):
        if steps == 0:
            return
        
        # Set Direction
        direction = steps > 0
        self.write_pin(self.direction_pins[motor], direction)
        
        # Pulse the steps
        for i in range(steps * self.motor_resolution):
            self.write_pin(self.step_pins[motor], GPIO.HIGH)
            self.write_pin(self.step_pins[motor], GPIO.LOW)
            self.motor_steps[motor] += 1
            
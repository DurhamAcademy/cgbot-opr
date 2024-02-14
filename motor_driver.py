# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout

left_dir_pin = 17
right_dir_pin = 27
GPIO.setup(left_dir_pin, GPIO.OUT)
GPIO.setup(right_dir_pin, GPIO.OUT)
GPIO.setup(22, GPIO.OUT) # Safety light
GPIO.setup(13, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
right_motor = GPIO.PWM(12, 50)
right_motor.start(0)
left_motor = GPIO.PWM(13, 50)
left_motor.start(0)
# in1: 17
# in2: 27
# an1: 13
# an2: 12
GPIO.output(left_dir_pin, GPIO.HIGH)
GPIO.output(right_dir_pin, GPIO.HIGH)
GPIO.output(22, GPIO.HIGH) # Safety light

def set_right_speed(speed: int):
    """
    :param speed: Speed of right motor, negative for backwards (range unknown) TODO: Find out range
    :return: null
    """
    if speed >= 0:
        GPIO.output(right_dir_pin, GPIO.HIGH)
    else:
        GPIO.output(right_dir_pin, GPIO.LOW)
    right_motor.ChangeDutyCycle(abs(speed))


def set_left_speed(speed: int):
    """
    :param speed: Speed of left motor, negative for backwards (range unknown) TODO: Find out range
    :return: null
    """
    if speed >= 0:
        GPIO.output(left_dir_pin, GPIO.HIGH)
    else:
        GPIO.output(left_dir_pin, GPIO.LOW)
    left_motor.ChangeDutyCycle(abs(speed))


"""# Set up pin 11 for PWM
GPIO.setup(11, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(33, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               # Starts running PWM on the pin and sets it to 0
GPIO.output(11, GPIO.HIGH)
# Move the servo back and forth
p.ChangeDutyCycle(3)     # Changes the pulse width to 3 (so moves the servo)
sleep(2)                 # Wait 1 second
p.ChangeDutyCycle(12)    # Changes the pulse width to 12 (so moves the servo)
sleep(1)
"""

def cleanup():
    # Clean up everything
    right_motor.stop()
    left_motor.stop()
    GPIO.output(22, GPIO.LOW)

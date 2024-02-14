# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program

GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

# IN2 -> Pin 12
# IN1 -> Pin 11
# A1 -> Pin 33
# A2 -> 32

# Set up pin 11 for PWM
GPIO.setup(11, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(33, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               # Starts running PWM on the pin and sets it to 0

while True:
    if keyboard.is_pressed('w'):
        GPIO.output(11, GPIO.HIGH)
        p.ChangeDutyCycle(3) # motors forward
    elif keyboard.is_pressed('s'):
        GPIO.output(11, GPIO.LOW)
        p.ChangeDutyCycle(3)  # motors back
    else:
        p.ChangeDutyCycle(0)  # motors back

# Clean up everything
p.stop()                 # At the end of the program, stop the PWM
GPIO.cleanup()           # Resets the GPIO pins back to defaults

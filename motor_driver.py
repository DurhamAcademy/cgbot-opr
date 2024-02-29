import RPi.GPIO as GPIO
import config

"""
Using a class for motor control
Uses an init method to initialize motors once
"""
class Motor(object):
    def __init__(self):
        # Sets the pin numbering system to use the physical layout
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(config.motor_left_direction_pin, GPIO.OUT)
        GPIO.setup(config.motor_right_direction_pin, GPIO.OUT)
        GPIO.setup(config.safety_light_pin, GPIO.OUT)
        GPIO.setup(config.motor_left_speed_pin, GPIO.OUT)
        GPIO.setup(config.motor_right_speed_pin, GPIO.OUT)

        self.right_motor = GPIO.PWM(config.motor_right_speed_pin, 50)
        self.right_motor.start(0)
        self.left_motor = GPIO.PWM(config.motor_left_speed_pin, 50)
        self.left_motor.start(0)

        GPIO.output(config.motor_left_direction_pin, GPIO.HIGH)
        GPIO.output(config.motor_right_direction_pin, GPIO.HIGH)

        # Turn on Safety light
        GPIO.output(config.safety_light_pin, GPIO.HIGH)

    def set_right_speed(self, speed: int):
        """
        :param speed: Speed of right motor, negative for backwards (range unknown) TODO: Find out range
        :return: null
        """
        if speed >= 0:
            GPIO.output(config.motor_right_direction_pin, GPIO.HIGH)
        else:
            GPIO.output(config.motor_right_direction_pin, GPIO.LOW)
        self.right_motor.ChangeDutyCycle(abs(speed))

    def set_left_speed(self, speed: int):
        """
        :param speed: Speed of left motor, negative for backwards (range unknown) TODO: Find out range
        :return: null
        """
        if speed >= 0:
            GPIO.output(config.motor_left_direction_pin, GPIO.HIGH)
        else:
            GPIO.output(config.motor_left_direction_pin, GPIO.LOW)
        self.left_motor.ChangeDutyCycle(abs(speed))

    def cleanup(self):
        # Clean up everything
        self.right_motor.stop()
        self.left_motor.stop()
        GPIO.output(config.safety_light_pin, GPIO.LOW)

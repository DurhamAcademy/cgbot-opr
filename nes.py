import hid
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library


def snes_input():
    report = nes.read(64)
    if report:
        if report[4] == 0 and report[9] == 255:
            print("up")
            return("up")
        elif report[4] == 255 and report[10] == 255:
            print("down")
            return("down")
        elif report[3] == 0 and report[8] == 255:
            print("left")
            return("left")
        elif report[3] == 255 and report[7] == 255:
            print("right")
            return("right")
        else:
            print("neutral")
            return("neutral")


def wpm_controller(control_input):
    left_speed = 0
    right_speed = 0
    if control_input == "neutral":
        left_speed = 0
        right_speed = 0
    if control_input == "up":
        left_speed = 50
        right_speed = 50
    if control_input =="down":
        left_speed = -50
        right_speed = -50
    if control_input == "left":
        left_speed = -50
        right_speed = 50
    if control_input == "right":
        left_speed = 50
        right_speed = -50
    return left_speed, right_speed


def wpm_set():
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(27, GPIO.OUT)
    global left
    left = GPIO.PWM(13, 1000)
    left.start(0)
    global right
    right = GPIO.PWM(12, 1000)
    right.start(0)
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(27, GPIO.HIGH)
    global setup_yn
    setup_yn = True
    return


GPIO.setmode(GPIO.BCM)
for device in hid.enumerate():
    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
nes = hid.device()
nes.open(0x0079, 0x0126)
# wpm_set()
"""while True:
    wpm_controller(snes_input())"""

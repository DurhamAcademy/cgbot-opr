import hid
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library

def input_move():
    report = nes.read(64)
    if report:
        print(report[4])
        print(report[9])
        print(report)
        if report[4] == 0 and report[9] == 255:
            print("up")


def wpm_controller(control_input):
    if setup_yn:
        if control_input == "neutral":
            left.ChangeDutyCycle(0)
            right.ChangeDutyCycle(0)
        if control_input == "up":
            left.ChangeDutyCycle(50)
            right.ChangeDutyCycle(50)
        if control_input =="down":
            left.ChangeDutyCycle(-50)
            right.ChangeDutyCycle(-50)
        if control_input == "left":
            left.ChangeDutyCycle(-50)
            right.ChangeDutyCycle(50)
        if control_input == "right":
            left.ChangeDutyCycle(50)
            right.ChangeDutyCycle(-50)
    return


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
    GPIO.output(27, GPIO.LOW)
    global setup_yn
    setup_yn = True
    return


GPIO.setmode(GPIO.BCM)
for device in hid.enumerate():
    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
nes = hid.device()
nes.open(0x0079, 0x0126)
wpm_set()
while True:
    wpm_controller(input_move())
import hid
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library



neutral = "[1, 127, 127, 127, 127, 15, 0, 0]"
dPadUp = "[1, 127, 127, 127, 0, 15, 0, 0]"
dPadDown = "[1, 127, 127, 127, 255, 15, 0, 0]"
dPadLeft = "[1, 127, 127, 0, 127, 15, 0, 0]"
dPadRight = "[1, 127, 127, 255, 127, 15, 0, 0]"
dPadA = "[1, 127, 127, 127, 127, 47, 0, 0]"
dPadB = "[1, 127, 127, 127, 127, 79, 0, 0]"
dPadStart = "[1, 127, 127, 127, 127, 15, 32, 0]"
pressed = 0
konamiCount = 0

for device in hid.enumerate():
    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

GPIO.setmode(GPIO.BCM)  # Sets the pin numbering system to use the physical layout
nes = hid.device()
nes.open(0x0079, 0x0011)
# IN1
GPIO.setup(17, GPIO.OUT)
# AN2
GPIO.setup(12, GPIO.OUT)
# AN1
GPIO.setup(13, GPIO.OUT)
# IN2
GPIO.setup(27, GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
left = GPIO.PWM(13, 1000)  # Sets up pin 11 as a PWM pin
left.start(0)  # Starts running PWM on the pin and sets it to 0
right = GPIO.PWM(12, 1000)
right.start(0)

GPIO.output(17, GPIO.HIGH)
GPIO.output(27, GPIO.LOW)

GPIO.setup(22, GPIO.OUT) # Safety light
GPIO.output(22, GPIO.HIGH) # Safety light

for device in hid.enumerate():
    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

while True:
    report = nes.read(64)
    if report:
        if str(report) == dPadUp:
            pressed = "up"
            # forward direction.
            GPIO.output(17, GPIO.HIGH)
            GPIO.output(27, GPIO.HIGH)
            #forward speed.
            left.ChangeDutyCycle(20)  # Changes the pulse width to 3 (so moves the servo)
            right.ChangeDutyCycle(20)
        elif str(report) == dPadDown:
            if pressed == "up":
                konamiCount = 1
            pressed = "down"

            # forward direction.
            GPIO.output(17, GPIO.LOW)
            GPIO.output(27, GPIO.LOW)
            # forward speed.
            left.ChangeDutyCycle(20)  # Changes the pulse width to 3 (so moves the servo)
            right.ChangeDutyCycle(20)

        elif str(report) == dPadLeft:
            if pressed == "down"  and konamiCount == 1:
                konamiCount = 2
            elif pressed == "right" and konamiCount == 3:
                konamiCount = 4
            pressed = "left"
        elif str(report) == dPadRight:
            if pressed == "left" and konamiCount == 2:
                konamiCount = 3
            elif pressed == "left" and konamiCount == 4:
                konamiCount = 5

            pressed = "right"
        elif str(report) == dPadA:
            if pressed == "b" and konamiCount == 6:
                konamiCount = 7

            pressed = "a"
        elif str(report) == dPadB:
            if pressed == "right" and konamiCount == 5:
                konamiCount = 6

            pressed = "b"
        elif str(report) == dPadStart:
            if pressed == "a" and konamiCount == 7:
                print("you did it")

            pressed = "start"

        # Nothing? Stop.
        else:
            left.ChangeDutyCycle(0)
            right.ChangeDutyCycle(0)
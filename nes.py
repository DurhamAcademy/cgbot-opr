import hid
import RPi.GPIO as GPIO


class Nes(object):

    def __init__(self):

        # By default let GPS mode be enabled.
        self.gps_mode = True

        try:
            for device in hid.enumerate():
                print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
            self.nes_device = hid.device()
            self.nes_device.open(0x0079, 0x0126)
        except AttributeError:
            print("Unable to open device")

    def snes_input(self):
        report = self.nes_device.read(64)
        if report:
            #print(report)
            if report[4] == 0 and report[9] == 255:
                self.gps_mode = False
                return("up")
            elif report[4] == 255 and report[10] == 255:
                self.gps_mode = False
                return("down")
            elif report[3] == 0 and report[8] == 255:
                self.gps_mode = False
                return("left")
            elif report[3] == 255 and report[7] == 255:
                self.gps_mode = False
                return("right")
            elif report[1] == 1:
                print("select")
                return("select")
            elif report[1] == 2:
                print("start")
                return("start")
            else:
                return("neutral")

    def wpm_controller(self, control_input):
        left_speed = 0
        right_speed = 0
        if control_input == "neutral":
            left_speed = 0
            right_speed = 0
        if control_input == "up":
            left_speed = 100
            right_speed = 100
        if control_input =="down":
            left_speed = -100
            right_speed = -100
        if control_input == "left":
            left_speed = -50
            right_speed = 50
        if control_input == "right":
            left_speed = 50
            right_speed = -50
        return left_speed, right_speed

import motor_driver
import gps
import time
import nes

controller = nes.Nes()

try:
    while True:

        # If controller is returning anything other than neutral, allow if to move robot.
        if controller.snes_input() != "neutral":
            while controller.snes_input() != "neutral":
                left_speed, right_speed = controller.wpm_controller(controller.snes_input())
                motor_driver.set_left_speed(left_speed)
                motor_driver.set_right_speed(right_speed)
        elif controller.gps_mode:
            # Add another button on SNES controller for "start"  in nes.py to start the GPS program.

            # Do GPS stuff
            """    
            pos = gps.get_gps_coords()
            print("Position", pos)
            pos = gps.get_gps_coords()
            print("Position", pos)
            heading = gps.get_heading()
            print("Heading", heading)
            speed = input()
            motor_driver.set_right_speed(int(speed))
            motor_driver.set_left_speed(int(speed))
            current_heading = gps.get_heading()
            rotate_to_heading(current_heading, (current_heading + -90) % 360)
            print(gps.get_heading())
            """
        elif controller.snes_input() == "neutral":
            motor_driver.set_left_speed(0)
            motor_driver.set_right_speed(0)
finally:
    motor_driver.cleanup()

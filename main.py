import motor_driver
import gps
import time
import nes

controller = nes.Nes()

def rotate_to_heading(current_heading, target_heading):
    # Calculate difference between current and target heading
    # Adjust the following formula based on your specific robot setup
    heading_difference = (target_heading - current_heading + 360) % 360
    # rotate right by default
    rotation_dir = 1
    if heading_difference >= 180:
        # rotate left if that is shorter
        rotation_dir = -1
        print(rotation_dir)

    current_heading = gps.get_heading()
    while abs(target_heading - current_heading) > 5:
        # rotate until real heading is close to target heading
        print((abs(target_heading - current_heading) % 25) + 25)
        motor_driver.set_left_speed(30 * rotation_dir)
        motor_driver.set_right_speed(30 * rotation_dir * -1)
        # update heading and rerun loop
        current_heading = gps.get_heading()
        print("cur", current_heading)
        print("tar", target_heading)
        print("goal", target_heading - current_heading)

    # Set motor speeds using PWM
    motor_driver.set_left_speed(25)
    motor_driver.set_right_speed(25)

    # Move in a straight line for a specified duration
    time.sleep(1)  # Adjust the duration as needed
    print("finished")


def go_to_position(target_pos: tuple):
    current_pos = gps.get_gps_coords()
    current_heading = gps.get_heading()
    while abs(gps.haversine_distance(current_pos, target_pos)) > 0.1:
        current_pos = gps.get_gps_coords()
        current_heading = gps.get_heading()
        target_heading = gps.calculate_heading(current_pos, target_pos)
        rotate_to_heading(current_heading, target_heading)

try:
    # rotate_to_heading(gps.get_heading(), gps.get_heading() + 90)
    go_to_position((-78.9693672, 35.9775664))
    while False:
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

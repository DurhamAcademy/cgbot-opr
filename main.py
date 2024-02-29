import motor_driver
import gps
import time
import nes

controller = nes.Nes()
drive = motor_driver.Motor()


def rotate_to_heading(current_heading, target_heading):
    # Calculate difference between current and target heading
    # Adjust the following formula based on your specific robot setup
    heading_difference = (target_heading - current_heading + 360) % 360
    # rotate right by default
    rotation_dir = 1
    if heading_difference >= 180:
        # rotate left if that is shorter
        rotation_dir = -1

    current_heading = gps.get_heading()
    while abs(target_heading - current_heading) > 5:
        # rotate until real heading is close to target heading
        drive.set_left_speed(30 * rotation_dir)
        drive.set_right_speed(30 * rotation_dir * -1)
        # update heading and rerun loop
        current_heading = gps.get_heading()
        print("turning")
    # Set motor speeds using PWM
    print("forward")
    drive.set_left_speed(28)
    drive.set_right_speed(28)

    # Move in a straight line for a specified duration
    time.sleep(1)  # Adjust the duration as needed
    print("finished")


def go_to_position(target_pos: tuple):
    current_pos = gps.get_gps_coords()
    current_heading = gps.get_heading()
    while abs(gps.haversine_distance(current_pos, target_pos)) > 0.1:
        current_pos = gps.get_gps_coords()
        print(current_pos, target_pos)
        current_heading = gps.get_heading()
        target_heading = gps.calculate_heading(current_pos, target_pos)
        rotate_to_heading(current_heading, target_heading)

try:
    # rotate_to_heading(gps.get_heading(), gps.get_heading() + 90)
    # go_to_position((35.977222, -78.969176))
    while True:
        left_speed, right_speed = controller.wpm_controller(controller.snes_input())
        drive.set_left_speed(left_speed)
        drive.set_right_speed(right_speed)
        """if not controller.gps_mode:
            print("control")
            # If controller.gps_mode is False, then controller is enabled.
            
        elif controller.gps_mode:
            print("gps")"""
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
finally:
    drive.cleanup()

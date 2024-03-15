import motor_driver
import gps
import time
import nes
from dotenv import load_dotenv
import logging
import datetime
import os
import json

# Import env file
load_dotenv()

controller = nes.Nes()
drive = motor_driver.Motor()

"""
Logging
TODO: Setup logrotate on this directory.
"""
if not os.path.isdir("/var/log/cgbot-opr"):
    os.makedirs("/var/log/cgbot")

logfile = "/var/log/cgbot-opr/log_" + str(datetime.date.today()) + ".txt"
logging.basicConfig(filename=logfile)
logging.basicConfig(level=logging.DEBUG)


def get_routes():
    """
    Load routes from json
    :return: routes
    """
    with open("route.json") as route_file:
        route = json.load(route_file)
    return route


def rotate_to_heading(current_heading, target_heading):
    # Calculate difference between current and target heading
    # Adjust the following formula based on your specific robot setup
    heading_difference = (target_heading - current_heading + 360) % 360
    # rotate right by default
    rotation_dir = "left"
    if heading_difference >= 180:
        # rotate left if that is shorter
        rotation_dir = "right"

    current_heading = gps.gps_heading()
    while abs(target_heading - current_heading) > 10:
        # rotate until real heading is close to target heading
        if rotation_dir == "left":
            drive.drive_turn_left()
        else:
            drive.drive_turn_right()

        # update heading and rerun loop
        current_heading = gps.gps_heading()
        print(abs(target_heading - current_heading))
        print("Turning, Current Heading: " + str(current_heading))
    # Set motor speeds using PWM
    print("forward")
    drive.drive_stop()
    drive.drive_forward()

    # Move in a straight line for a specified duration
    time.sleep(2)  # Adjust the duration as needed
    print("finished")


def go_to_position(target_pos: tuple):

    # forward for 1 second.
    drive.drive_forward()
    time.sleep(1)
    drive.drive_stop()
    time.sleep(3)

    current_pos = gps.get_gps_coords()
    logging.debug("go_to_position: current coordinates" + str(current_pos))

    current_heading = gps.gps_heading()
    logging.debug("go_to_position: current heading" + str(current_heading))

    while abs(gps.haversine_distance(current_pos, target_pos)) > 1:
        current_pos = gps.get_gps_coords()
        current_gps_heading = gps.gps_heading()

        print("distance to target in meters:", gps.haversine_distance(current_pos, target_pos))
        print("current position: " + str(current_pos))
        print("target position: " + str(target_pos))
        print("gps heading: " + str(current_gps_heading))

        target_heading = gps.calculate_initial_compass_bearing(current_pos, target_pos)

        print("target heading: ", str(target_heading))
        rotate_to_heading(current_gps_heading, target_heading)


def check_stuck():
    """
    Need a function to check that the robot is not stuck.
    Something like has motors run and GPS coordinates are
    not changing.
    :return: Bool
    """
    return False


def check_perimeter():
    """
    Need a function to check that all ultrasonics are clear
    and nothing is around the robot.
    Return a side that is blocked
    :return: none, left, right, front, back
    """
    return "none"


def main():
    try:
        while True:

            """
            Check safety light timeout
            """
            drive.safety_light_timeout()

            """
            Drive mode
            """

            if controller.get_mode() == "controller":
                """
                Controller Mode
                """
                left_speed, right_speed = controller.wpm_controller(controller.snes_input())
                drive.set_left_speed(left_speed)
                drive.set_right_speed(right_speed)

                """
                If select button is pressed, print coordinates
                """
                if controller.snes_input() == "select":
                    try:
                        print(gps.get_gps_coords())
                        time.sleep(1)
                    except Exception as e:
                        print(e)

            else:
                """
                GPS Mode
                """

                route = get_routes()
                for i in route['coordinates']:
                    # convert to tuple
                    i = eval(i)
                    go_to_position(i)
                    time.sleep(5)


                # rotate_to_heading(gps.get_heading(), gps.get_heading() + 90)
                # go_to_position((36.182629, -78.897478))


                # print(gps.get_gps_coords())

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
        logging.debug("Main loop complete.")
        drive.cleanup()


if __name__ == "__main__":
    logging.debug("Start of program")
    main()

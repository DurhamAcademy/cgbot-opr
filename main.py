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


def num_to_range(num, inMin, inMax, outMin, outMax):
    """
    Map values from one range to the next.
    :param num: value to find 
    :param inMin: input range min
    :param inMax: input range max
    :param outMin: output range min
    :param outMax: output range max
    :return: result
    """""
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax
                  - outMin))


def get_routes():
    """
    Load routes from json
    :return: routes
    """
    with open("route.json") as route_file:
        route = json.load(route_file)
    return route


def fastest_direction(start_degree, end_degree):
    """
    Determines the fastest direction (left or right) from one degree to another
    on a 360-degree circle.

    Args:
        start_degree (float): Starting degree (0 to 359).
        end_degree (float): Ending degree (0 to 359).

    Returns: list
        [0] str: "left" if the fastest direction is to the left, "right" if to the right.
        [1] float: difference in degrees.
    """
    clockwise_distance = (end_degree - start_degree) % 360
    counterclockwise_distance = (start_degree - end_degree) % 360

    if clockwise_distance <= counterclockwise_distance:
        return ["right", clockwise_distance]
    else:
        return ["left", counterclockwise_distance]


def rotate_to_heading(current_heading, target_heading):
    """
    Rotate robot to face the correct heading.
    Appears to work.
    :param current_heading:
    :param target_heading:
    :return:
    """

    rotation_dir = fastest_direction(current_heading, target_heading)
    while rotation_dir[1] > 10:

        # rotate until real heading is close to target heading
        speed = num_to_range(rotation_dir[1], 0, 360, 15, 45)
        if rotation_dir[0] == "left":
            drive.drive_turn_left(speed)
        else:
            drive.drive_turn_right(speed)
        # update heading and rerun loop
        rotation_dir = fastest_direction(gps.gps_heading(), target_heading)

    drive.drive_stop()


def go_to_position(target_pos: tuple):

    current_pos = gps.get_gps_coords()

    while abs(gps.haversine_distance(current_pos, target_pos)) > 1:
        current_pos = gps.get_gps_coords()
        current_heading = gps.gps_heading()

        target_heading = gps.calculate_initial_compass_bearing(current_pos, target_pos)

        rotate_to_heading(current_heading, target_heading)
        drive.drive_forward()
        time.sleep(2)


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

import motor_driver
import gps
import arduino
import time
import nes
from dotenv import load_dotenv
import logging
import datetime
import os
import json
import config
import threading

# Import env file
load_dotenv()

controller = nes.Nes()
drive = motor_driver.Motor()
mc = arduino.Arduino()

"""
Logging
TODO: Setup logrotate on this directory.
"""
if not os.path.isdir("/var/log/cgbot-opr"):
    os.makedirs("/var/log/cgbot")

logfile = "/var/log/cgbot-opr/log_" + str(datetime.date.today()) + ".txt"
logging.basicConfig(filename=logfile)
logging.basicConfig(level=logging.DEBUG)


def log(text):
    """
    Write to logfile and console.
    :param text:
    :return: none
    """
    logging.debug(text)
    print(text)


def check_light_timeout():
    threading.Timer(5.0, check_light_timeout).start()
    drive.safety_light_timeout()


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
    return outMin + (float(num - inMin) / float(inMax - inMin) * (outMax - outMin))


def within_range_degrees(number, target, tolerance=config.turning_degree_accuracy):
    """"
    Check if a degree is withing a certian range
    """
    # Normalize numbers to be within the range of [0, 360)
    number = (number + 360) % 360
    target = (target + 360) % 360
    # Check if the absolute difference is within the tolerance range
    return abs(target - number) <= tolerance or abs(target - number + 360) <= tolerance


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
    # rotation_dir[0] = the direction left/right
    # rotation_dir[1] = the amount of degrees the robot needs to move to get back on track.

    # only turn is more than ## degrees off.
    if rotation_dir[1] > config.turning_degree_accuracy:
        # What is current reading from compass?
        current_compass = (gps.get_heading()) % 360
        print("start", current_compass)

        # Could consolidate with no ifs if you use negatives instead of left or right (-1 for left, 1 for right)
        # Would need to modify turn function to take in -35 to turn left
        if rotation_dir[0] == "left":
            # What is the destination degrees on the compass in relation to target_heading? / subtract for left turn
            dest_compass = ((current_compass - rotation_dir[1])) % 360
            # speed = num_to_range(rotation_dir[1], 0, 360, 30, 50)
            while not within_range_degrees(current_compass, dest_compass):
                drive.drive_turn_left(35)
                current_compass = (gps.get_heading()) % 360
                print("current: ", current_compass)
        else:
            # What is the destination degrees on the compass in relation to target_heading? / add for right turn
            dest_compass = (current_compass + rotation_dir[1]) % 360
            print("dest", dest_compass)
            # speed = num_to_range(rotation_dir[1], 0, 360, 30, 50)
            while not within_range_degrees(current_compass, dest_compass):
                drive.drive_turn_right(35)
                current_compass = (gps.get_heading()) % 360
                print("current: ", current_compass)
        # Stop the rotation and return.
        drive.drive_stop()
    else:
        print("rotation not needed.")


def go_to_position(target_pos: tuple):

    current_pos = gps.get_gps_coords()

    while abs(gps.haversine_distance(current_pos, target_pos)) > 2:
        current_pos = gps.get_gps_coords()
        current_heading = gps.gps_heading()
        # Use heading from GPS to determine a target_heading to destination coordinates
        target_heading = gps.calculate_initial_compass_bearing(current_pos, target_pos)
        print("targetheading: " + str(target_heading))
        rotate_to_heading(current_heading, target_heading)
        drive.drive_forward()
        print("start forward")
        time.sleep(1)
        print("stop forward")
    drive.drive_stop()


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


def check_light_timeout():
    while True:
        drive.safety_light_timeout()
        log("checking light")


def main():
    # Save location to file ever x seconds
    # gps.store_location()
    # Turn light off if not moving after x seconds.
    # check_light_timeout()
    """
    Check Battery Level
    """
    #if mc.get_voltage() <= config.voltage_min_threshold:
    #    log("Battery Level Below Threshold at " + str(config.voltage_min_threshold))

    try:
        # last_print = 0

        while True:
            """
            Check safety light timeout
            TODO: Enable mutilthreading and move this into its own thread.
            """
            #drive.safety_light_timeout()



            """
            Check Humidity Level
            """

            """
            Check Ultrasonic every xx seconds
            """
            if mc.ultrasonic_last_check + config.ultrasonic_check_interval < time.time():
                log("Ultrasonic: " + str(mc.get_ultrasonic()))
                # What to do about Ultrasonic readings?

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
                # print(gps.get_gps_coords())

                """
                print GPS heading every second
                """

                # if last_print < time.time() + 1:
                #     print(str(gps.gps_heading()) + " degrees")
                #     last_print = time.time()

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
                    log("Going to location: {}.".format(i['label']))
                    log("Coordinates: {}.".format(i['coordinates']))

                    # convert to tuple
                    coordinates = eval(i['coordinates'])

                    # go to the spot
                    go_to_position(coordinates)
                    log("Destination reached.!!!")
                    current_heading = gps.gps_heading()
                    log("Rotate to final heading {}.".format(i['final_heading']))
                    rotate_to_heading(current_heading, i['final_heading'])

                    log("Waiting here for {} seconds.".format(str(i['duration'])))
                    time.sleep(i['duration'])


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
        log("Main loop complete.")
        drive.cleanup()


if __name__ == "__main__":
    main()

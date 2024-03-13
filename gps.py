from ublox_gps import UbloxGps
import serial
import math
import adafruit_mlx90393
import board
import time
# from adafruit_bno08x import (
#     BNO_REPORT_ACCELEROMETER,
#     BNO_REPORT_GYROSCOPE,
#     BNO_REPORT_MAGNETOMETER,
#     BNO_REPORT_ROTATION_VECTOR,
# )
from adafruit_bno08x.i2c import BNO08X_I2C

import config

i2c = board.I2C()  # uses board.SCL and board.SDA

# AdaFruit MLX90393
SENSOR = adafruit_mlx90393.MLX90393(i2c, address=0x18, gain=adafruit_mlx90393.GAIN_1X)
# # AdaFruit BNO085
# SENSOR2 = BNO08X_I2C(i2c)
# SENSOR2.enable_feature(BNO_REPORT_ACCELEROMETER)
# SENSOR2.enable_feature(BNO_REPORT_GYROSCOPE)
# SENSOR2.enable_feature(BNO_REPORT_MAGNETOMETER)
# SENSOR2.enable_feature(BNO_REPORT_ROTATION_VECTOR)

port = serial.Serial('/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00', baudrate=38400,
                     timeout=1)
gps = UbloxGps(port)


def run():
    try:
        print("Listenting for UBX Messages.")
        while True:
            try:
                #coords = gps.geo_coords()
                #print("Coords: ", coords.lon, coords.lat)
                #print("Heading: ", coords.headMot)
                print(get_heading())
            except (ValueError, IOError) as err:
                print(err)

    finally:
        print("Closing GPS")


def gps_heading():
    """
    gps heading
    :return: gps heading degrees
    """
    try:
        coords = gps.geo_coords()
        return coords.headMot
    except (ValueError, IOError) as err:
        print(err)


def get_heading_from_magno(x, y):
    """
    convert heading from radians to degrees.
    :param x: magno x
    :param y: magno y
    :return: heading in degrees
    """
    heading_rad = math.atan2(y, x)
    heading_deg = math.degrees(heading_rad)
    heading_true = (heading_deg - 90) % 360
    return heading_true


def get_gps_coords():
    """
    get GPS coordinates from ublox gps interface
    :return: array: [(latitude, longitude )]
    """
    try:
        coords = gps.geo_coords()
        return coords.lat, coords.lon
    except (ValueError, IOError) as err:
        print(err)


def get_heading():
    """
    get heading from mlx90393 sensor
    :return: heading in degrees
    """
    try:
        MX, MY, MZ = SENSOR.magnetic
        return get_heading_from_magno(MX, MY)
    except:
        return "unknown"


def get_heading_sensor2():
    """
    get heading from bmo085
    :return: heading in degrees
    """
    try:
        SEN
        MX, MY, MZ = SENSOR2.magnetic
        return get_heading_from_magno(MX, MY)
    except:
        return "unknown"


def calculate_initial_compass_bearing(point_a, point_b):
    """

    Example:
    A = (38.898556,-77.037852)
    B = (36.1217264,-78.8891156)
    result is 208.44000059760523

    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `point_a: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `point_b: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(point_a) != tuple) or (type(point_b) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(point_a[0])
    lat2 = math.radians(point_b[0])

    difflong = math.radians(point_b[1] - point_a[1])

    x = math.sin(difflong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                                           * math.cos(lat2) * math.cos(difflong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def haversine_distance(coord1, coord2):
    """
    Calculate the Haversine distance between two GPS coordinates.

    Parameters:
    - coord1: Tuple of (latitude, longitude) for the first point.
    - coord2: Tuple of (latitude, longitude) for the second point.

    Returns:
    - distance: Distance in meters.
    """

    # Extract latitude and longitude values
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Earth radius in meters
    earth_radius = 6371000.0

    # Calculate the distance
    distance = earth_radius * c

    return distance

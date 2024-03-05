from ublox_gps import UbloxGps
import serial
import math
import adafruit_mlx90393
import board
import time

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
SENSOR = adafruit_mlx90393.MLX90393(i2c, address=0x18, gain=adafruit_mlx90393.GAIN_1X)

port = serial.Serial('/dev/serial/by-id/usb-u-blox_AG_-_www.u-blox.com_u-blox_GNSS_receiver-if00', baudrate=38400, timeout=1)
gps = UbloxGps(port)


def run():
    try:
        print("Listenting for UBX Messages.")
        while True:
            try:
                coords = gps.geo_coords()
                print("Coords: ", coords.lon, coords.lat)
                print("Heading: ", coords.headMot)
            except (ValueError, IOError) as err:
                print(err)

    finally:
        port.close()

def get_heading_from_magno(x, y):
    heading_rad = math.atan2(y, x)
    heading_deg = math.degrees(heading_rad)
    return (heading_deg - 90) % 360

def get_gps_coords():
    """
    :return: array: [(longitude, latitude), heading]
    """
    try:
        coords = gps.geo_coords()
        return coords.lat, coords.lon, coords.headMot

    except (ValueError, IOError) as err:
        print(err)


def get_heading():
    MX, MY, MZ = SENSOR.magnetic
    # veh = gps.veh_attitude()
    return get_heading_from_magno(MX, MY)

def calculate_heading(current_position, target_coordinates):
    """
    Calculate the heading from the current position to the target coordinates.

    Parameters:
    - current_position: Tuple of (latitude, longitude) representing the current position.
    - target_coordinates: Tuple of (latitude, longitude) representing the target coordinates.

    Returns:
    - heading: Heading in degrees (0 to 360).
    """

    # Extract latitude and longitude values
    lat1, lon1 = current_position
    lat2, lon2 = target_coordinates

    # Calculate the differences in coordinates
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # Calculate the heading using arctan2
    y = math.sin(dlon) * math.cos(math.radians(lat2))
    x = (math.cos(math.radians(lat1)) * math.sin(math.radians(lat2)) -
         math.sin(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.cos(dlon))

    heading = math.degrees(math.atan2(y, x))

    # Ensure the heading is in the range [0, 360)
    heading = ((heading % 360) - 0) % 360

    return heading


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


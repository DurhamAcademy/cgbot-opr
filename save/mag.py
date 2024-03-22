import time
from math import atan2, degrees
import board
import qmc5883l as qmc5883

i2c = board.I2C()
qmc = qmc5883.QMC5883L(i2c)

# https://circuitpython-qmc5883l.readthedocs.io/en/latest/examples.html


def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle = angle + 360
    return angle


def get_heading(sensor):
    mag_x, mag_y, _ = sensor.magnetic
    return vector_2_degrees(mag_x, mag_y)


while True:
    print(f"heading: {get_heading(qmc.magnetic):.2f} degrees")
    print()
    time.sleep(0.2)

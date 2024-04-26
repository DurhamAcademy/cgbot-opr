import serial
import time


class Arduino:

    def __init__(self):
        self.ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0042_851393033313512102C2-if00', 9600, timeout=1)
        self.ultrasonic_last_check = 0.00

    def get_temperature(self):
        """
        Reads the temperature from the Arduino. Returns the temperature in degrees Celsius.
        :return: float degrees
        """
        data = self.ser.readline()
        d = data.decode()
        d.split("|")
        return float(d[4])

    def get_humidity(self):
        """
        Reads the humidity from the Arduino. Returns the humidity as float.
        :return: float humidity
        """
        data = self.ser.readline()
        d = data.decode()
        d.split("|")
        return float(d[5])

    def get_voltage(self):
        """
        Reads the voltage from Battery through the Arduino. Returns the voltage as float.
        :return: float voltage
        """
        data = self.ser.readline()
        d = data.decode()
        d.split("|")
        return float(d[6])

    def get_ultrasonic(self):
        """
        Reads the ultrasonic sensors from the Arduino. Returns the ultrasonic as
        :return: dictionary
        """
        data = self.ser.readline()
        d = data.decode()
        d.split("|")
        self.ultrasonic_last_check = time.time()
        return d[0:3]

import serial
import time


class Arduino:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ultrasonic_last_check = 0.00

    def send_command(self, command):
        if command is "temp":
            self.ser.write("2".encode())
        elif command is "humidity":
            self.ser.write("3".encode())
        elif command is "voltage":
            self.ser.write("4".encode())
        elif command is "ultrasonic":
            self.ser.write("1".encode())

    def get_temperature(self):
        """
        Reads the temperature from the Arduino. Returns the temperature in degrees Celsius.
        :return: float degrees
        """
        self.send_command("temp")
        data = self.ser.readline()
        return float(data.decode())

    def get_humidity(self):
        """
        Reads the humidity from the Arduino. Returns the humidity as float.
        :return: float humidity
        """
        self.send_command("humidity")
        data = self.ser.readline()
        return float(data.decode())

    def get_voltage(self):
        """
        Reads the voltage from Battery through the Arduino. Returns the voltage as float.
        :return: float voltage
        """
        self.send_command("voltage")
        data = self.ser.readline()
        return float(data.decode())

    def get_ultrasonic(self):
        """
        Reads the ultrasonic sensors from the Arduino. Returns the ultrasonic as
        :return: dictionary
        """
        self.send_command("ultrasonic")
        data = self.ser.readline()
        self.ultrasonic_last_check = time.time()
        return data.decode() # is this correct?
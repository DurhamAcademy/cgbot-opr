import serial

ser = serial.Serial('dev/tty/ACM0', 9600, timeout=1)

while True:

    input = ser.read()

    print (input.decode("utf-8"))
    print("check")

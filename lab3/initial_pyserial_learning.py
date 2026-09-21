import serial

print("Learning Pyserial")


ser = serial.Serial("/dev/ttyAMA10",baudrate=19200,timeout=10)

while not ser.is_open:
    print("Opening...")

# TODO: use the ser object


ser.close()

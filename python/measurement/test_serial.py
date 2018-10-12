import serial
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.write(b'10000')
ser.readline()

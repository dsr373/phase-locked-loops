import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
print('opened ' + ser.name)

time.sleep(1)
ser.setDTR(value=0)
time.sleep(1)

def send_command(half_p=125000):
    ser.write(bytes(half_p))    # test??
    time.sleep(1)
    print("ARDUINO: " + ser.readline().strip())
    print("ARDUINO: " + ser.readline().strip())

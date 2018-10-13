import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
print('opened ' + ser.name)

time.sleep(1)
ser.setDTR(value=0)
time.sleep(1)

def send_command(half_p=125000):
    ser.write(str(half_p))
    print(ser.readline().strip())
    print(ser.readline().strip())

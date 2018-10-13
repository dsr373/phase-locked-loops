from serial import Serial
import time

ser = Serial('/dev/ttyACM0', 9600)
print('opened ' + ser.name)

time.sleep(1)
ser.setDTR(value=0)
time.sleep(1)

ser.write('10000')
print(ser.readline().strip())
print(ser.readline().strip())

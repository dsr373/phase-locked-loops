import serial
import time

ser = serial.Serial('/dev/ttyACM0', 9600)
print('opened ' + ser.name)

time.sleep(1)
ser.setDTR(value=0)
time.sleep(1)

def send_command(half_p=None, phase_diff=None, duty_cycle=None):
    if half_p is not None:
        ser.write("f" + bytes(int(half_p)))
        time.sleep(1)
        print("ARDUINO: " + ser.readline().strip())
        print("ARDUINO: " + ser.readline().strip())
    if phase_diff is not None:
        ser.write("p" + bytes(phase_diff))
        time.sleep(1)
        print("ARDUINO: " + ser.readline().strip())
        print("ARDUINO: " + ser.readline().strip())
    if duty_cycle is not None:
        ser.write("v" + bytes(duty_cycle))
        time.sleep(1)
        print("ARDUINO: " + ser.readline().strip())
        print("ARDUINO: " + ser.readline().strip())

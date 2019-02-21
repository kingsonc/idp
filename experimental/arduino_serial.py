import serial
import time

ser = serial.Serial('COM15', 9600)

while True:
    ser.write(b'test2')
    time.sleep(10)

ser.close()

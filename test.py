import serial

ser = serial.Serial('/dev/serial0',9600)
while True:
 read_serial = ser.readline()
 #if (read_serial[2:4] == 'AX'):
 print read_serial

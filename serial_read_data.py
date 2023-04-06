
import sys
import os
import serial
from datetime import datetime
import re
import os
import shutil
import time



#name of the file to which sensor data will be saved
if os.path.exists("myfile.txt"):
  os.remove("myfile.txt") # one file at a time


#to get accel-sensor values from terminal string 
def get_acc(acc_values):
	accel = re.findall(r'-*\d+', acc_values)
	return accel


#returns list of gyroscope values
def get_gyro(gyr_values):
	gyr = re.findall(r'-*\d+', gyr_values)
	return gyr
	
#returns list of magnetometer values
def get_Magn(Magn_values):
	mgn = re.findall(r'-*\d+', Magn_values)
	return mgn

#return values of pressure, Temprature, and Humidity sensor readings
def get_pth(pth_values):
	pth = re.findall(r"[-+]?(?:\d*\.\d+|\d+)", pth_values)
	return pth


col_val = "Timestamp,Acc_x,Acc_Y,Acc_Z,Gyro_X,Gyro_Y,Gyro_Z,Magn_X,Magn_Y,Magn_Z,Pressure,Temprature,Humidity"
figg="myfile"+datetime.now().strftime("%d_%m_%Y_%H%M%S")+".txt"
datafile = open(figg,"a")
datafile.write(col_val)

Tmstmp = time.time()
#ser = serial.Serial('COM5',1152000)
ser = serial.Serial('/dev/ttyACM0',115200) #name of the serial port and buad rate 
while True:
    read_serial = ser.readline().strip()
    #list_items = []
    #print(read_serial.decode("utf-8"))
    print(len(read_serial))


    if (read_serial[0:9] == b'TimeStamp'):
        ts = read_serial[11:22].decode("utf-8")
        datafile = open(figg,"a")
        datafile.write('\n')
        datafile.write(ts+",")
        datafile.close()
        continue
    if(read_serial[0:5] == b'ACC_X'):
        print("aac trigger")
        values = get_acc(read_serial.decode("utf-8"))
        #print(values)
        datafile = open(figg,"a")
        for i in values:
        	datafile.write(i+",")
        datafile.close()
        
    if(read_serial[0:5] == b'GYR_X'):
        print("gyr trigger")
        values = get_gyro(read_serial.decode("utf-8"))
        datafile = open(figg,"a")
        for i in values:
        	datafile.write(i+",")

        datafile.close()
        
    if(read_serial[0:5] == b'MAG_X'):
        print("mag trigger")
        values = get_Magn(read_serial.decode("utf-8"))
        datafile = open(figg,"a")
        for i in values:
        	datafile.write(i+",")
        datafile.close()
    
    if(read_serial[0:5] == b'PRESS'):
        print("press trigger")
        values = get_pth(read_serial.decode("utf-8"))
        datafile = open(figg,"a")
        for i in values:
        	datafile.write(i+",")
        datafile.close()
        
        

   

   



    
   
    




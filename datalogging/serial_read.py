
import sys
import os
import serial
from datetime import datetime
import re
import os
import shutil
import time


address_prefix = '/home/pi/Pollution_Sensing_IOT/sensordata/'
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
figg=address_prefix + "sensortile/"+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"stile"+".csv"
try:
    datafile = open(figg,"a")
except:
    command = "mkdir -p "+address_prefix + "sensortile/"
    print(command)
    os.system(command)
    datafile = open(figg,"a")
datafile.write(col_val)

Tmstmp = time.time()
##this part of code tries to look for a valid serial port,
#if not found it tries 12 times with 5 second intervals and then exits raising system exception

s_try=0
while True:
    s_address='/dev/ttyACM1'
    #s_address='COM5' #for testing directly with computer, see device manager for ur exact port
    try:
        ser = serial.Serial(s_address,115200) #name of the serial port and buadrate
        print("Detected Serial device at "+s_address)
        break
    except:
        print("Not able to detect Serial device at "+s_address)
        s_address='/dev/ttyACM0'
        try:
            ser = serial.Serial(s_address,115200) #name of the serial port and buad rate
            print("Detected Serial device at "+s_address)
            break
        except:
            print("Not able to detect Serial device at "+s_address)
            print("Please check connection to Sensortile")
            print("Retrying in 5 Seconds")
            time.sleep(5) #sleep for 5 seconds
            s_try=s_try+1
            if s_try >12: #number of tries for reconnection(12)
                sys.exit(1)
                break
            continue
##
print("input loop cleared")
while True:
    read_serial = ser.readline().strip()
    #list_items = []
    #print(read_serial.decode("utf-8"))
    print("sensortile")


    if (read_serial[0:9] == b'TimeStamp'):
        ts = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3])
        datafile = open(figg,"a")
        datafile.write('\n')
        datafile.write(ts+",")
        datafile.close()
        continue
    if(read_serial[0:5] == b'ACC_X'):
        #print("aac trigger")u
        values = get_acc(read_serial.decode("utf-8"))
        #print(values)
        datafile = open(figg,"a")
        for i in values:
            datafile.write(i+",")
        datafile.close()
        
    if(read_serial[0:5] == b'GYR_X'):
        #print("gyr trigger")
        values = get_gyro(read_serial.decode("utf-8"))
        datafile = open(figg,"a")
        for i in values:
            datafile.write(i+",")

        datafile.close()
        
    if(read_serial[0:5] == b'MAG_X'):
        #print("mag trigger")
        values = get_Magn(read_serial.decode("utf-8"))
        datafile = open(figg,"a")
        for i in values:
            datafile.write(i+",")
        datafile.close()
    
    if(read_serial[0:5] == b'PRESS'):
        #print("press trigger")
        values = get_pth(read_serial.decode("utf-8"))
        datafile = open(figg,"a")
        for i in values:
            datafile.write(i+",")
        datafile.close()
        
        

   

   



    
   
    




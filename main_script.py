import os
import time
import sys
from datetime import datetime
import multiprocessing as mp
from picamera import PiCamera
import urllib2
import errno
from socket import error as SocketError
import serial
import json
import requests
import uuid
# import schedule
from datetime import timedelta
import numpy as np
# import pymysql

polfile = ''
mpufile = ''
gpsfile = ''
imagefile = ''
bmefile = ''

oldpolfile = ''
oldmpufile = ''
oldgpsfile = ''
oldimagefile = ''
oldbmefile = ''

gpsfile_limit = 30  # every 10 mins, 1 sample per 5 secs
polfile_limit = 30  # every 10 mins, 1 sample per 5 secs
bmefile_limit = 30  # every 10 mins, 1 sample per 5 secs
mpufile_limit = 540  # every 2 mins, 18-19 samples per reading
imagefile_limit = 4  # every 4 mins, 1 sample per 4 minute

gpsfile_lines = gpsfile_limit
polfile_lines = polfile_limit
bmefile_lines = bmefile_limit
mpufile_lines = mpufile_limit
imagefile_count = imagefile_limit


ts = ''
flag_new = -1
flag_old = -1
uid = ''

address_prefix = '/home/pi/Pollution_Sensing_IOT/'
#address_prefix = '/home/anmol/Desktop/'

try:
    import struct
except ImportError:
    import ustruct as struct


def getserial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial


mac = getserial()
# command = "gsutil mv /home/pi/Pollution_Sensing_IOT/upload/" + \
#     str(mac) + " gs://iot_01_test_dataflow/"
command = "gsutil mv /home/pi/Pollution_Sensing_IOT/upload/" + mac + \
    " gs://eziomotiv_files/"
print(command)


def syncdata():
    # if(os.stat("/home/pi/.config/rclone/rclone.conf").st_size == 0):
    #     os.system("cp /home/pi/rclone.conf /home/pi/.config/rclone/rclone.conf")
    #     time.sleep(1)
    os.system(command)
    time.sleep(1)
    # print "Synced"
    # Add excepion handling

# checks if internet connection is available


def get_ts_uid(tsuid_data):
    global flag_new, flag_old, ts, uid
    header = "TS,FLAG"
    c = json.loads(tsuid_data)
    # print(c)
    # ts = c["TS"]
    ts = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S:%f')[:-7])
    flag_new = c["FLAG"]
    # print(flag_old)
    if flag_new == flag_old:
        pass
    else:
        uid = uuid.uuid4()
        # print(uid)
        flag_old = flag_new


def writempu(mpu_data):
    header = "AX, AY, AZ, GX, GY, GZ, deviceId, ts, uid"
    global address_prefix, mpufile, mpufile_lines, mpufile_limit, oldmpufile, uid, ts, mac
    tlast = datetime.now()
    if (mpufile_lines >= mpufile_limit):
        ltime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3])
        mpufile = ltime + 'mpu.csv'
        if(len(oldmpufile) > 1):
            os.rename(address_prefix+'sensordata/mpudata/'+oldmpufile,
                      address_prefix+'upload/' + str(mac) + '/mpudata/'+oldmpufile)
        oldmpufile = mpufile
        mpufile_lines = 0
        file_exists = os.path.isfile(
            address_prefix+'sensordata/mpudata/'+oldmpufile)
        if not file_exists:
            fo = open(address_prefix+'sensordata/mpudata/'+oldmpufile, "a+")
            fo.write(header+"\n")
            fo.close()
    ltime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3])
    data = mpu_data
    c = json.loads(data)
    c['ts'] = ts
    c['uid'] = uid
    c['deviceId'] = mac
    # print(c)
    fa = open(address_prefix+'sensordata/mpudata/'+mpufile, "a+")
    fa.write(str(c["AX"])+","+str(c["AY"])+","+str(c["AZ"]) +
             ","+str(c["GX"])+","+str(c["GY"])+","+str(c["GZ"])+","+str(c['deviceId'])+","+str(c['ts'])+","+str(c['uid'])+'\n')
    fa.close()
    mpufile_lines += 1


def main():
    read_serial = ser.readline().strip()

    while True:
        try:
            null_count = ''
            read_serial = ser.readline().strip()
            if (len(read_serial) < 10):
                continue
            if(read_serial[2:4] == 'TS'):
                get_ts_uid(read_serial)
                continue
            if(read_serial[2:4] == 'PM'):
                writepol(read_serial)
                continue
            if(read_serial[2:5] == 'LAT'):
                writegps(read_serial)
                continue
            if(read_serial[2:4] == 'Pr'):
                writebme(read_serial)
                continue
            if(read_serial[2:4] == 'AX'):
                #print(read_serial)
                writempu(read_serial)
                continue
        except:
            pass


def writegps(gps_data):
    header = "LAT, LONG, deviceId, ts, uid"
    global address_prefix, gpsfile, gpsfile_limit, gpsfile_lines, oldgpsfile, uid, ts, mac
    if (gpsfile_lines >= gpsfile_limit):
        ltime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3])
        gpsfile = ltime + 'gps.csv'
        if(len(oldgpsfile) > 1):
            os.rename(address_prefix+'sensordata/gpsdata/'+oldgpsfile,
                      address_prefix+'upload/' + str(mac) + '/gpsdata/'+oldgpsfile)
        oldgpsfile = gpsfile
        gpsfile_lines = 0
        file_exists = os.path.isfile(
            address_prefix+'sensordata/gpsdata/'+oldgpsfile)
        if not file_exists:
            fo = open(address_prefix+'sensordata/gpsdata/'+oldgpsfile, "a+")
            fo.write(header+"\n")
            fo.close()
    localtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
    data = gps_data
    c = json.loads(data)
    c['ts'] = ts
    c['uid'] = uid
    c['deviceId'] = mac
    # print(c)
    f = open(address_prefix+'sensordata/gpsdata/'+gpsfile, "a+")
    f.write(str(c["LAT"])+","+str(c["LONG"])+"," +
            str(c['deviceId'])+","+str(c['ts'])+","+str(c['uid'])+'\n')
    f.close()
    gpsfile_lines += 1
    #print ("Wrote a gpsdata line!")
    return


def writepol(pol_data):
    header = "PM1, PM2.5, PM10, deviceId, ts, uid"
    global address_prefix, polfile, polfile_limit, polfile_lines, oldpolfile, uid, ts, mac
    if (polfile_lines >= polfile_limit):
        ltime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3])
        polfile = ltime + 'pol.csv'
        if(len(oldpolfile) > 1):
            os.rename(address_prefix+'sensordata/poldata/'+oldpolfile,
                      address_prefix+'upload/' + str(mac) + '/poldata/'+oldpolfile)
        oldpolfile = polfile
        polfile_lines = 0
        file_exists = os.path.isfile(
            address_prefix+'sensordata/poldata/'+oldpolfile)
        if not file_exists:
            fo = open(address_prefix+'sensordata/poldata/'+oldpolfile, "a+")
            fo.write(header+"\n")
            fo.close()
    localtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
    data = pol_data
    c = json.loads(data)
    c['ts'] = ts
    c['uid'] = uid
    c['deviceId'] = mac
    # print(c)
    f = open(address_prefix+'sensordata/poldata/'+oldpolfile, "a+")
    f.write(str(c["PM1"])+","+str(c["PM2.5"])+","+str(c["PM10"]) +
            ","+str(c['deviceId'])+","+str(c['ts'])+","+str(c['uid'])+'\n')
    f.close()
    polfile_lines += 1
    #print ("Wrote a poldata line!")
    return


def writebme(bme_data):
    header = "Pressure, Temperature, Humidity, deviceId, ts, uid"
    global address_prefix, bmefile, bmefile_limit, bmefile_lines, oldbmefile, uid, ts, mac
    if (bmefile_lines >= bmefile_limit):
        ltime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3])
        bmefile = ltime + 'bme.csv'
        if(len(oldbmefile) > 1):
            os.rename(address_prefix+'sensordata/bmedata/'+oldbmefile,
                      address_prefix+'upload/' + str(mac) + '/bmedata/'+oldbmefile)
        oldbmefile = bmefile
        bmefile_lines = 0
        file_exists = os.path.isfile(
            address_prefix+'sensordata/bmedata/'+oldbmefile)
        if not file_exists:
            fo = open(address_prefix+'sensordata/bmedata/'+oldbmefile, "a+")
            fo.write(header+"\n")
            fo.close()
    localtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
    data = bme_data
    c = json.loads(data)
    c['ts'] = ts
    c['uid'] = uid
    c['deviceId'] = mac
    # print(c)
    f = open(address_prefix+'sensordata/bmedata/'+bmefile, "a+")
    f.write(str(c["Pr"])+","+str(c["T"])+","+str(c["H"]) + "," +
            str(c['deviceId'])+","+str(c['ts'])+","+str(c['uid'])+'\n')
    f.close()
    bmefile_lines += 1
    return


# def RTC_on_internet():
#     url = "http://www.google.com"
#     timeout = 5
#     try:
#         request = requests.get(url, timeout=timeout)
#         os.system("sudo hwclock -w -D")
#         time.sleep(30.0)
#     #    print("Time Set")
#     except (requests.ConnectionError, requests.Timeout) as exception:
#         print("No internet connection.")
#         time.sleep(5.0)
#         RTC_on_internet()

# RTC_on_internet()

ser = serial.Serial('/dev/serial0', 9600)
#ser = serial.Serial('/dev/ttyUSB0',9600)

accel_p = mp.Process(target=main)
accel_p.start()

while(1):
    syncdata()

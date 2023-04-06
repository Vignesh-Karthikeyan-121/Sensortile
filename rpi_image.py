import schedule
import os
import time
from datetime import datetime
import zlib
import multiprocessing as mp
from picamera import PiCamera
import urllib2
import errno
from socket import error as SocketError
import serial
import json
import requests
import uuid
from google.cloud import storage
# import schedule
from datetime import timedelta
import numpy as np
# import pymysql


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

address_prefix = '/home/pi/Pollution_Sensing_IOT/'

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


def writeimage():
    global address_prefix, imagefile, imagefile_count, imagefile_limit, oldimagefile
    ltime = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3])
    imagefile = ltime + 'image.jpg'
    if(len(oldimagefile) > 1):
        os.rename(address_prefix+'sensordata/image/'+oldimagefile,
                  address_prefix+'upload/' + mac + '/image/'+oldimagefile)
    oldimagefile = imagefile
    localtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')[:-3]
    string1 = address_prefix+'sensordata/image/img.jpg'
    camera = PiCamera()
    camera.capture(string1)
    camera.close()
    with open(string1, "rb") as imageFile:
        image = imageFile.read()
    f = open(address_prefix+'sensordata/image/'+imagefile, "a+")
    f.write(image)
    f.close()
    print("Wrote file.")
    os.unlink(string1)


# def job():
#     print("I'm working...")


schedule.every(1).minutes.do(writeimage)

while True:
    schedule.run_pending()
    time.sleep(1)

#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import sys
import time
import sqlite3
import os
from datetime import datetime, date

## Constants
PORT_NAME = "ttyACM0"
BAUD_RATE = "115200"
ENCODER = 'latin1'
QUALITY_CODE = str(4)
CODE_PATH = os.path.dirname(__file__)
GIT_PATH = os.path.join(CODE_PATH, '../../../')
DB_PATH = os.path.join(GIT_PATH,'Measurements/database/')
DB_NAME = 'EF_DB.db'
CREATE_TABLE = 'create_table.txt'
TABLE_NAME = 'POSITION'

## Globals
Warning_Xbee = False
Warning_Data = False
Stop = False

## Classes
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Timestamp_ms:
    def __init__(self, timestamp, ms):
        self.timestamp = timestamp
        self.ms = ms
    def __str__(self):
        return f"{self.timestamp} , {str(self.ms)}"

class Position:
    def __init__(self, timestamp, ms, pos_x, pos_y, pos_z):
        self.timestamp = timestamp
        self.ms = ms
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
    def __str__(self):
        return f"{self.timestamp} , {str(self.ms)} , {str(self.pos_x)} , {str(self.pos_y)} , {str(self.pos_z)}"


## Functions

# Externally callable function to stop the process
def stop():
    global stop
    stop = True

# Database connection function
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(str(e))
    return conn

def openXbee(port,baudrate):
    try:
        global Warning_Xbee
        global ENCODER
        ser_GPS = serial.Serial(
            port = port,
            baudrate =baudrate,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 0.05
        )
        print(ser_GPS.readline().decode(ENCODER))
        if not ser_GPS.isOpen():
            ser_GPS.open()
        if not '$' in ser_GPS.readline().decode(ENCODER):
            Warning_Xbee = False
            return False
        else:
            print(f'{bcolors.OKGREEN}[INFO] Xbee is open and connected: {bcolors.ENDC}',ser_GPS.isOpen())
        Warning_Xbee = False
        return ser_GPS
    except:
        if not Warning_Xbee : 
            print(f'{bcolors.WARNING}[Warning] Xbee is not connected or wrong port name or activate ttyS0 port on rpi.{bcolors.ENDC}')
            Warning_Xbee = True
        return False

def ask4observationGPS(ser):
    global ENCODER
    
    gnss_bin_data = ser.readline()
    gnss_asc_data = gnss_bin_data.decode(ENCODER)
    print(gnss_asc_data)
    if isGGA(gnss_asc_data):
        print(gnss_asc_data)
        if isRTK(gnss_asc_data):
            position = readPositionFromGGA(gnss_asc_data)
            return position #[readPositionFromGGA(gnss_asc_data),readTimeFromGGA(gnss_asc_data),time.time()]
        else:
            return None
    return None

def isGGA(trame):
    if trame.split(',')[0] == '$GNGGA':
        return True
    return False

def isRTK(trame):
    global QUALITY_CODE
    if trame.split(',')[6] == QUALITY_CODE:
        return True
    return False

def readPositionFromGGA(trame):
    lat = trame.split(',')[2] #str
    lat = float(lat[0:2]) + float(lat[2:])/60 #degres décimal float
    lon = trame.split(',')[4] #str
    lon = float(lon[0:3]) + float(lon[3:])/60 #degres décimal float
    alt = float(trame.split(',')[9])+float(trame.split(',')[11]) #float on ellipsoide wgs84 (correction du faux geoide)
    timestamp_ms = readTimeFromGGA(trame)
    position = Position(timestamp_ms.timestamp, timestamp_ms.ms, lat, lon, alt)
    return position
    #[format(lat,".8f"), format(lon,".8f"), format(alt,".3f")]

def readTimeFromGGA(trame):
    time = trame.split(',')[1] #str
    timestamp_str = str(date.today().year) + "-" + str(date.today().month) + "-" + str(date.today().day) + " " + str(int(time[0:2]) + 2) + ":" + time[2:4] + ":" + time[4:6]
    dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    
    return Timestamp_ms(dt.strftime("%Y-%m-%d %H:%M:%S"), int(time[7:9])/100) #format(float(SecondUTC),".3f")

 
def get_position(id, comment):
    global Warning_Data
    global PORT_NAME
    global BAUD_RATE
    global Stop
    portXbee = '/dev/' + PORT_NAME
    ser_GPS = openXbee(portXbee,BAUD_RATE)
    while not Stop:
        while not ser_GPS:
            ser_GPS = openXbee(portXbee, BAUD_RATE)
        if ser_GPS:
            try: 
                data_GPS = ask4observationGPS(ser_GPS)
                if (data_GPS):
                    Warning_Data = False
                    conn = create_connection(DB_PATH + DB_NAME)
                    cursorObject = conn.cursor()
                    try : 
                        # insert into database
                        cursorObject.execute("INSERT INTO "+ TABLE_NAME + " values(?,?,?,?,?,?,?)", (id, data_GPS.timestamp, int(data_GPS.ms), comment, data_GPS.pos_x, data_GPS.pos_y , data_GPS.pos_z))
                        conn.commit()
                        conn.close()
                    except TypeError as e:
                        print(e)
            except Exception as e:
                if not Warning_Data:
                    print(f'{bcolors.WARNING}[Warning] No data from GPS.{bcolors.ENDC}' + str(e))
                    Warning_Data = True

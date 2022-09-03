#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
from datetime import datetime, timezone
from xml.etree.ElementTree import Comment
import RPi.GPIO as GPIO
import EFM113B.gather as EFM
import ina219.gather as INA
import bme_280.gather as BME
import os
import sqlite3
import threading

## Constants
REF = 5.08                                  # Modify according to actual voltage
                                            # external AVDD and AVSS(Default), or internal 2.5V
RESISTOR = 1                                # RESISTOR in kOhm
RANGE = 5                                   # Range in kV/m
VOLTAGE_BATTERY_THRESHOLD_UP = 9.5          # in Volt 
VOLTAGE_BATTERY_THRESHOLD_DOWN = 9.0        # in Volt
DB_PATH = os.path.expanduser('~/TB_Drone_Electromagnetic/Measurements/database/EF_DB.db')
MS_SLEEP_BME = 2000                         # time between two gathering of BME sensor values
MS_SLEEP_INA = 2000                         # time between two gathering of INA sensor values
MS_SLEEP_EFM = 50                           # time between two gathering of EFM sensor values
MS_SLEEP_INSERT = 50 

## Global variables
range = 0
resistor = 0
voltage_battery = 0
temperature = 0
altitude = 0
pressure = 0
humidity = 0
voltage_AD = 0
dt = 0
stop = 0

def stop():
    global stop
    input("Press Enter to stop...")
    stop = 1
## Sleep function to set in millisecond
def sleepMilliseconds(ms):
  """ Delay milliseconds using time.sleep(). """
  time.sleep(ms * 1e-3)

## database connection function
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn
    
## check bme measurements and stock them in global variables
def read_bme():
    # gather BME measurements
    global temperature
    global pressure
    global humidity

    while not stop:
        try :
            temperature = BME.get_temperature()
            #altitude = BME.get_altitude()
            pressure = BME.get_pressure()
            humidity = BME.get_humidity()
        
        except IOError as e:
            print ("Error BME :")
            print(e)
            return 0
        sleepMilliseconds(MS_SLEEP_BME)

## check ina measurement and stock them in global variable
def read_ina():
    # Check battery state through INA219 sensor
    global voltage_battery

    while not stop:
        try :
            voltage_battery = INA.get_battery_voltage()
        except IOError as e:
            print ("Error INA :")
            print(e)
            return 0
        sleepMilliseconds(MS_SLEEP_INA)

## check efm measurements and stock them in global variable
def read_efm():
    # gather EFM measurement
    global voltage_AD
    
    while not stop:
        try :
            voltage_AD = EFM.AD_gather()

        except IOError as e:
            print ("Error EFM :")
            print(e)
            return 0
        sleepMilliseconds(MS_SLEEP_EFM)

## thread launchers for sensors data gathering
def read_sensors(cursorObject, conn, id, input_resistor, input_range, comment):
    if (input_resistor <= 0) :
        resistor = RESISTOR
    else :
        resistor = input_resistor
    if (input_range <= 0) :
        range = RANGE
    else : 
        range = input_range
    stop = 0
    bme = threading.Thread(target=read_bme, args=())
    efm = threading.Thread(target=read_efm, args=())
    ina = threading.Thread(target=read_ina, args=())
    bme.start()
    efm.start()
    ina.start()
    while not stop:
        # get timestamp
        dt = datetime.now() #(timezone.utc)
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        ms = int(dt.microsecond / 1000)
        try : 
            # insert into database
            cursorObject.execute("INSERT INTO MEASUREMENTS values(?,?,?,?,?,?,?,?,?,?,?,?)", (id, timestamp, ms, comment, range, resistor, temperature, pressure, humidity, altitude, voltage_AD, voltage_battery))
            conn.commit()
        except TypeError as e:
            print(e)
        sleepMilliseconds(MS_SLEEP_INSERT)
    
    bme.join()
    efm.join()
    ina.join()

def gather(comment):
    EFM.AD_init()
    try : 
        conn = create_connection(DB_PATH)
        with open('../database/create_table.txt') as f:
            conn.execute(f.read())
        cursorObject = conn.cursor()
        cursorObject.execute("SELECT MAX(ID_MEASUREMENT_SET) FROM MEASUREMENTS;")
        id = cursorObject.fetchone()[0]
        if (id == None):
            id = 1
        else  :
            id += 1
        goodbye = threading.Thread(target=stop, args=())
        goodbye.start()
        read_sensors(cursorObject, conn, id, RESISTOR, RANGE, comment)
        goodbye.join()
        conn.close()
        
    except TypeError as e:
        print(e)
    EFM.AD_stop()

gather("test2")

    
    


        

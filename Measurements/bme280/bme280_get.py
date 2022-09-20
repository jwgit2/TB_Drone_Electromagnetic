#!/usr/bin/env python
#-----------------------------------------------------------------------------

from __future__ import print_function
import qwiic_bme280
import time
import sys

def get_humidity():

    bme280 = qwiic_bme280.QwiicBme280()

    if bme280.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    bme280.begin()
    print("Humidity:\t%.3f" % bme280.humidity)
    print("Pressure:\t%.3f" % bme280.pressure)    
    print("Altitude:\t%.3f" % bme280.altitude_meters)
    print("Temperature:\t%.2f" % bme280.temperature_celsius)       


def get_pressure():
    return bme280.pressure

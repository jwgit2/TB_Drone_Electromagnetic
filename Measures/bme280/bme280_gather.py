#!/usr/bin/env python
#-----------------------------------------------------------------------------

from __future__ import print_function
import qwiic_bme280
import time
import sys

def runExample():

    print("\nSparkFun BME280 Sensor  Example 1\n")
    mySensor = qwiic_bme280.QwiicBme280()

    if mySensor.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        return

    mySensor.begin()

    while True:
        print("Humidity:\t%.3f" % mySensor.humidity)

        print("Pressure:\t%.3f" % mySensor.pressure)    

        print("Altitude:\t%.3f" % mySensor.altitude_meters)

        print("Temperature:\t%.2f" % mySensor.temperature_celsius)       

        print("")

        time.sleep(0.5)


if __name__ == '__main__':
    try:
        runExample()
    except (KeyboardInterrupt, SystemExit) as exErr:
        print("\nEnding Example 1")
sys.exit(0)
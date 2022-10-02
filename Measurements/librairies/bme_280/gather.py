#!/usr/bin/python
# -*- coding:utf-8 -*-
import board
import time
from adafruit_bme280 import basic as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()   # uses board.SCL and board.SDA
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25


def get_humidity():
    return bme280.relative_humidity

def get_pressure():
    return bme280.pressure

def get_altitude():
    return bme280.altitude

def get_temperature():
    return bme280.temperature

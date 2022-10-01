#!/usr/bin/python
# -*- coding:utf-8 -*-

import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219


def get_battery_voltage():
    i2c_bus = board.I2C()
    ina219 = INA219(i2c_bus)

    # optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
    ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
    # optional : change voltage range to 16V
    ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

    bus_voltage = ina219.bus_voltage  # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage  # voltage between V+ and V- across the shunt
    current = ina219.current  # current in mA

    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    #print("Voltage (VIN+) : {:6.3f}   V".format(bus_voltage + shunt_voltage))
    # Check internal calculations haven't overflowed (doesn't detect ADC overflows)
    if ina219.overflow:
        print("Internal Math Overflow Detected!")
    return (bus_voltage + shunt_voltage)

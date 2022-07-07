#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
from datetime import datetime
import ADS1263
import RPi.GPIO as GPIO

REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
range = 5000        # Range in V/m
resistor = 2000     # Resistor in Ohm

try:
    ADC = ADS1263.ADS1263()
    if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1):
        exit()
    ADC.ADS1263_SetMode(0)
    
    start = datetime.now()
    print(start.strftime("%m/%d/%Y") + ",  Range is " + str(range) + "kV/m, Resistor is " + str(resistor))
    print("Timestamp \t\tvoltage \tcurrent \tvolt/meter")
    while(1):
        ADC_Value = ADC.ADS1263_GetAll()    # get ADC1 value
        ADC_0 = REF*2 - ADC_Value[0] * REF / 0x80000000
        ADC_n0 = (ADC_Value[0] * REF / 0x7fffffff)

        dt = datetime.now()
        #Timestamp,voltage,current,volt/meter
        if(ADC_Value[0]>>31 ==1):
            res =  dt.strftime("%H:%M:%S") + "." + "{0:0=3d}".format(int(dt.microsecond / 1000)) + "\t%lf\t%lf\t%lf" %(-ADC_0, (-ADC_0)/resistor,  range*(-ADC_0)/resistor)
        else:
            res =  dt.strftime("%H:%M:%S") + "." + "{0:0=3d}".format(int(dt.microsecond / 1000))  + "\t%lf\t%lf\t%lf" %(ADC_n0, ADC_n0/resistor,  range*ADC_n0/resistor)   # 32bit
        print (res)

        time.sleep(0.050)
        
    ADC.ADS1263_Exit()

except IOError as e:
    print(e)
   
except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")
    ADC.ADS1263_Exit()
    exit()
   

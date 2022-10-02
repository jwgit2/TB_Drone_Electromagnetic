#!/usr/bin/python
# -*- coding:utf-8 -*-


import time
from datetime import datetime
import librairies.EFM113B.ADS1263 as ADS1263
import RPi.GPIO as GPIO

REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V
ADC = ADS1263.ADS1263()
#range = 5           # Range in kV/m
#resistor = 2.2      # Resistor in kOhm

def AD_init():
    if (ADC.ADS1263_init_ADC1('ADS1263_7200SPS') == -1):
        return 0
    ADC.ADS1263_SetMode(0)
    return 1

def AD_gather ():
    try:
        ADC_Value = ADC.ADS1263_GetChannalValue(0)    # get ADC1 value
        ADC_0 = REF*2 - ADC_Value * REF / 0x80000000
        ADC_n0 = (ADC_Value * REF / 0x7fffffff)
        if(ADC_Value>>31 ==1):
            #print(-ADC_0)
            return -ADC_0
        else:
            #print(ADC_n0)
            return ADC_n0

    except IOError as e:
        print(e)
        return 0

def AD_stop():
    ADC.ADS1263_Exit()
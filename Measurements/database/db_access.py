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
import logging

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
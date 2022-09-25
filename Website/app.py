#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import os
import sqlite3
import csv
#import ../../Measurements/code

# Global variables
WEB_PATH = os.path.dirname(__file__)
GIT_PATH = os.path.join(WEB_PATH, '../')
DB_PATH = os.path.join(GIT_PATH,'Measurements/database/')
CREATE_TABLE = 'create_table.txt'
DB_NAME = 'EF_DB.db'
TABLE_NAME = 'MEASUREMENTS'
FULL_SET_NAME = "full_set.csv"
LAST_SET_NAME = "last_set.csv"
is_running = 0


app = Flask(__name__)
app.debug = True
# Database management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ DB_PATH + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
# Class to retrieve data from database
class Measurements(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    ID_MEASUREMENT_SET = db.Column(db.Integer)
    MEASUREMENT_DATETIME = db.Column(db.String(20), nullable = False)
    MEASUREMENT_MS = db.Column(db.Integer, nullable = False)
    COMMENT = db.Column(db.Text, unique = False)
    RANGE_VM = db.Column(db.Integer)
    RESISTOR = db.Column(db.Float)
    TEMPERATURE = db.Column(db.Float)
    PRESSURE = db.Column(db.Float)
    HUMIDITY = db.Column(db.Float)
    VOLTAGE_EFM = db.Column(db.Float)
    def __repr__(self):
        return f"Timestamp : {self.datetime}, MS : {self.ms}"
## Standard functions
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
        print(str(e))
    return conn

def get_max_id_set():
    conn = create_connection(DB_PATH + DB_NAME)
    with open(DB_PATH + CREATE_TABLE) as f:
        conn.execute(f.read())
    cursorObject = conn.cursor()
    cursorObject.execute("SELECT MAX(ID_MEASUREMENT_SET) FROM " + TABLE_NAME + ";")
    id = cursorObject.fetchone()[0]
    conn.close()
    return id

## Website architecture
# Test database accessibility
@app.route('/testdb/')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/')
def index():
    measurements = db.session\
                    .query(Measurements)\
                    .order_by(Measurements.rowid.desc())\
                    .limit(10)
                        #Measurements.query.all()
    return render_template('index.html', measurements=measurements)

@app.route('/reload/')
def reload():
    index()

@app.route('/fullset',methods=["GET","POST"])
def dlfulltset():
    measurements = Measurements.query.all()
    with open(FULL_SET_NAME, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
    #csvwriter.writerow()
        for m in measurements:
            csvwriter.writerow([m.ID_MEASUREMENT_SET, m.MEASUREMENT_DATETIME, m.MEASUREMENT_MS, m.COMMENT,\
                m.RANGE_VM, m.RESISTOR, m.TEMPERATURE, m.PRESSURE, m.HUMIDITY, m.VOLTAGE_EFM])
    render_template('index.html', measurements=measurements)
    return send_file(
        f'./' + FULL_SET_NAME,\
        mimetype='text/csv',\
        attachment_filename=FULL_SET_NAME,\
        as_attachment=True
    )
## A revoir
@app.route('/lastset',methods=["GET","POST"])
def dllasttset():
    max = get_max_id_set()
    print(max)
    measurements = Measurements.query.filter(Measurements.ID_MEASUREMENT_SET == max).all()
    with open(LAST_SET_NAME, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter = ',')
        for m in measurements:
            csvwriter.writerow([m.ID_MEASUREMENT_SET, m.MEASUREMENT_DATETIME, m.MEASUREMENT_MS, m.COMMENT,\
                m.RANGE_VM, m.RESISTOR, m.TEMPERATURE, m.PRESSURE, m.HUMIDITY, m.VOLTAGE_EFM])
    render_template('index.html', measurements=measurements)
    return send_file(
        f'./' + LAST_SET_NAME,\
        mimetype='text/csv',\
        attachment_filename=LAST_SET_NAME,\
        as_attachment=True
    )

@app.route('/start')
def start_recording():
    
    measurements = Measurements.query.all()
    return render_template('index.html', measurements=measurements)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
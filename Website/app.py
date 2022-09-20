
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
import os

# Global variables
WEB_PATH = os.path.dirname(__file__)
GIT_PATH = os.path.join(WEB_PATH, '../')
DB_PATH = os.path.join(GIT_PATH,'Measurements/database/')
CREATE_TABLE = 'create_table.txt'
DB_NAME = 'EF_DB.db'
TABLE_NAME = 'MEASUREMENTS'
is_running = 0


app = Flask(__name__)
app.debug = True
# Database management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ DB_PATH + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Measurements(db.Model):
    ID_MEASUREMENT_SET = db.Column(db.Integer, primary_key=True)
    MEASUREMENT_DATETIME = db.Column(db.String(20), nullable = False)
    MEASUREMENT_MS = db.Column(db.Integer, nullable = False)
    COMMENT = db.Column(db.Text, unique = False)
    RANGE_VM = db.Column(db.Integer)
    RESISTOR = db.Column(db.Float)
    TEMPERATURE = db.Column(db.Float)
    PRESSURE = db.Column(db.Float)
    HUMIDITY = db.Column(db.Float)
    ALTITUDE = db.Column(db.Float)
    VOLTAGE_EFM = db.Column(db.Float)
    def __repr__(self):
        return f"Timestamp : {self.datetime}, MS : {self.ms}"

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
    measurements = Measurements.query.all()
    return render_template('index.html', measurements=measurements)

@app.route('/reload/')
def reload():
    index()

@app.route('/fullset')
def dlfulltset():
    measurements = Measurements.query.all()
    return render_template('index.html', measurements=measurements)

@app.route('/start')
def start_recording():
    
    measurements = Measurements.query.all()
    return render_template('index.html', measurements=measurements)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
import serial
import sys
import time
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def openXbee(port,baudrate):
    try:
        ser_GPS = serial.Serial(
            port = port,#'/dev/ttyS0'
            baudrate =baudrate,#115200
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout = 0.05
        )
        print(ser_GPS.readline().decode('latin1'))
        if not ser_GPS.isOpen():
            ser_GPS.open()
        if not '$' in ser_GPS.readline().decode('latin1'):
            return False
        else:
            print(f'{bcolors.OKGREEN}[INFO] Xbee is open and connected: {bcolors.ENDC}',ser_GPS.isOpen())
        return ser_GPS
    except:
        
        print(f'{bcolors.WARNING}[Warning] Xbee is not connected or wrong port name or activate ttyS0 port on rpi.{bcolors.ENDC}')
        return False
def ask4observationGPS(ser):
        gnss_bin_data = ser.readline()
        gnss_asc_data = gnss_bin_data.decode('latin1')
        if isGGA(gnss_asc_data):
            if isRTK(gnss_asc_data):
                return [readPositionFromGGA(gnss_asc_data),readTimeFromGGA(gnss_asc_data),time.time()]
            else:
                return 'GGA'
        else:
           return False

def isGGA(trame):
    if trame.split(',')[0] == '$GNGGA':
        return True
    else:
        return False
def isRTK(trame):
    code = trame.split(',')[6]
    if code == '4' :#code positionnement RTK
        return True
    else:
        return False
def readPositionFromGGA(trame):
    lat = trame.split(',')[2] #str
    lat = float(lat[0:2]) + float(lat[2:])/60 #degres décimal float
    lon = trame.split(',')[4] #str
    lon = float(lon[0:3]) + float(lon[3:])/60 #degres décimal float
    alt = float(trame.split(',')[9])+float(trame.split(',')[11]) #float on ellipsoide wgs84 (correction du faux geoide)
    return [format(lat,".8f"), format(lon,".8f"), format(alt,".3f")]
def readTimeFromGGA(trame):
    time = trame.split(',')[1] #str
    SecondUTC = int(time[0:2])*3600 + int(time[2:4])*60 + int(time[4:6]) + int(time[7:9])/100
    return format(float(SecondUTC),".3f")

 
def getposition():
    portXbee = '/dev/ttyACM0'
    ser_GPS = openXbee(portXbee,115200)
    while True:
        while not ser_GPS:
            ser_GPS = openXbee(portXbee, 115200)
        if ser_GPS:
            try: 
                data_GPS = ask4observationGPS(ser_GPS)
                if (data_GPS):
                    print (data_GPS)
            except Exception as e:
                print("Value not decodable : ", str(e))
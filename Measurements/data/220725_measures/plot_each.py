import glob, os
import numpy as np
import matplotlib
import datetime
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.chdir("./")


for file in glob.glob("*.data"):
    with open(file) as inp:
        currentData = list(zip(*(line.split('\t') for line in inp)))
        timestamp = np.array([datetime.datetime.strptime(timestamp_string, '%H:%M:%S.%f') for timestamp_string in currentData[0]])
        #print(timestamp)
        volt = np.array([float(numeric_string) for numeric_string in currentData[1]])
        #print(volt)
        current = np.array([float(numeric_string) for numeric_string in currentData[2]])
        voltmeter = np.array([float(numeric_string) for numeric_string in currentData[3]])
        plt.plot(timestamp,volt, color='b', label='voltage [V]')
        plt.plot( timestamp,current, color='r', label='current [A]')
        plt.plot( timestamp,voltmeter, color='g', label='E field [kV/m]')
        #plt.xscale('log')
        plt.xlabel("Timestamp")
        plt.xticks(rotation=30)
        plt.title(os.path.splitext(file)[0])
        legend = plt.legend(labelcolor='linecolor')
        #plt.show()
        plt.savefig(os.path.splitext(file)[0]+".png", bbox_inches='tight')
        plt.close()




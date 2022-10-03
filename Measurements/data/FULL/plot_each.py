import glob, os
import numpy as np
import matplotlib
import datetime
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.chdir("./")


for file in glob.glob("*.csv"):
    with open(file) as inp:
        currentData = list(zip(*(line.split(',') for line in inp)))
        timestamp = np.array([datetime.datetime.strptime(timestamp_string, '%Y-%m-%d %H:%M:%S') for timestamp_string in currentData[1]])
        #print(timestamp)
        voltmeter = np.array([float(numeric_string) for numeric_string in currentData[13]])
        plt.plot( timestamp,voltmeter, color='g', label='E field [V/m]')
        #plt.xscale('log')
        plt.xlabel("Timestamp")
        plt.xticks(rotation=30)
        plt.title(os.path.splitext(file)[0])
        legend = plt.legend(labelcolor='linecolor')
        #plt.show()
        plt.savefig(os.path.splitext(file)[0]+"_EF.png", bbox_inches='tight')
        plt.close()




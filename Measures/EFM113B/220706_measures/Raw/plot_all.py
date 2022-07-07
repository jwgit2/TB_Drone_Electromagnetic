import glob, os
import numpy as np
import matplotlib
import datetime
#matplotlib.use('Agg')
import matplotlib.pyplot as plt

os.chdir("./")
i = 0
color_plot = ["red", "black", "blue", "green", "orange", "yellow", "grey"]
for file in glob.glob("*.data"):
    with open(file) as inp:
        currentData = list(zip(*(line.split('\t') for line in inp)))
        timestamp = np.array([datetime.datetime.strptime(timestamp_string, '%H:%M:%S.%f') for timestamp_string in currentData[0]])
        voltmeter = np.array([float(numeric_string) for numeric_string in currentData[3]])
        plt.plot( timestamp, voltmeter, color=color_plot[i], label= os.path.splitext(file)[0])
        i = i + 1
        
plt.xlabel("Timestamp")
plt.ylabel("kV/m")
plt.title("kV/m comparison")
plt.legend()
#plt.show()
plt.savefig("voltmeter_comparison.png")
plt.close()

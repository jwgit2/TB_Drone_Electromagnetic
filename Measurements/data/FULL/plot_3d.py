import glob, os
import numpy as np
import matplotlib
import datetime
#matplotlib.use('Agg')


from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

os.chdir("./")


for file in glob.glob("*.csv"):
    with open(file) as inp:
        currentData = list(zip(*(line.split(',') for line in inp)))
        #timestamp = np.array([datetime.datetime.strptime(timestamp_string, '%Y-%m-%d %H:%M:%S') for timestamp_string in currentData[1]])
        #print(timestamp)
        fig = plt.figure(figsize=(10,8))
        ax = plt.axes(projection='3d')

        x_axis = np.array([float(numeric_string) for numeric_string in currentData[9]])
        y_axis = np.array([float(numeric_string) for numeric_string in currentData[10]])
        z_axis = np.array([float(numeric_string) for numeric_string in currentData[11]])
        ax.set_xlabel("North in decimal degrees")
        ax.set_ylabel("East in decimal degrees")
        ax.set_zlabel("Height [m]")
        ax.plot3D( x_axis, y_axis, z_axis, color='r', label='drone')
        #plt.yscale('log')
        legend = plt.legend(labelcolor='linecolor')
        #plt.show()
        plt.savefig(os.path.splitext(file)[0]+"_3d.png", bbox_inches='tight')
        plt.close()




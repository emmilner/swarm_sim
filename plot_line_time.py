import numpy as np
import matplotlib.pylab as plt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
import ast 
from matplotlib.legend import Legend
import sys
import os 

Task = int(sys.argv[1])

def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	sr_dict = file_in.readline()
	sr_dict = ast.literal_eval(sr_dict)
	file_in.close()
	return sr_dict

fig, ax = plt.subplots()
time_dict = file_opener("total_task"+str(Task)+"_time_results")

robots = range(10,51,2)
boxes = range(10,51,2)
time= []
handles_box = []
lines_for_leg = []

for b in boxes:
	time = []
	for r in robots:
		time.append(time_dict[r][b])
	lines_for_leg += ax.plot(robots,time)
	handles_box.append(b)


leg = Legend(ax, lines_for_leg, handles_box, title = "Number of boxes", loc='lower left', ncol = 1, frameon=True)
plt.title("Time to complete task "+str(Task))
plt.xlabel("Number of agents")
plt.ylabel("Time taken (s)")
ax.add_artist(leg)
plt.show()


	

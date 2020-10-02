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
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict

time_dict = file_opener("total_task"+str(Task)+"_sr_results")
max_time = 10001

x = [] #robots
y = [] #boxes

for r in range(10,101,10):
	x.append(r)
for b in range(10,51,10):
	y.append(b)
Z = np.full([len(y),len(x)],0.)

for i_b in range(len(y)):
	for i_n in range(len(x)): #### should this not be just in y?
		b = y[i_b]
		n = x[i_n]
		if time_dict[n][b] == max_time:
			time_dict[n][b] = max_time-1
		Z[i_b,i_n] = time_dict[n][b] 		
			
fig, ax = plt.subplots()
levs = np.arange(0,1.1,0.1)
cs = ax.contourf(x, y, Z, levs, #cmap = "Greys_r"
				 cmap = "rainbow")
cbar = fig.colorbar(cs, ticks = [levs])
plt.title("Success rate for complete task "+str(Task))
plt.xlabel("Number of agents")
plt.ylabel("Number of boxes requested")
plt.show()
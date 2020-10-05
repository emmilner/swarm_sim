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

#############################################
	
def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict

#time_dict = file_opener("new_task"+str(Task)+"_time_results")
time_dict = file_opener("500000_task2_times_results")
max_time = 500000

if Task == 1:
	print("Cannot show task 1 because file name is wrong in code")

x = [] #robots
y = [] #boxes
for r in range(10,51,5):
#for r in range(10,51,2):  ## 10 to 126 (per 5)
	x.append(r)
#for b in range(10,51,2):  ## 10 to 101 (per 10)
for b in range(10,51,5):
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

if norm == True:
	levs = np.arange(0,11,1)
	levs = levs/10
if norm == False:
	max_out = max_time
	levs = np.arange(0,max_out+1,max_out/10)

cs = ax.contourf(x, y, Z, 
				 levs,
				 #cmap = "Greys_r"
				 cmap = "rainbow"
#				 norm=colors.LogNorm()
				)
cbar = fig.colorbar(cs, ticks = [levs])
cbar.ax.set_yticklabels(["{:}".format(i) for i in cbar.get_ticks()]) # set ticks of your format
if norm == True: 
	cbar.set_label("Normalised time taken (s)")
	plt.title("Normalised time taken to complete task "+str(Task))

if norm == False:
	cbar.set_label("Time taken (s)")
	plt.title("Time taken to complete task "+str(Task))

plt.xlabel("Number of agents")
plt.ylabel("Number of boxes requested")
plt.show()

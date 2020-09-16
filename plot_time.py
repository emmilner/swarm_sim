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
norm = int(sys.argv[2])

#############################################

if norm == 0:
	norm = False
	print("Data is NOT normalised because your second input is 0. Put 1 for normalised data.")

if norm == 1:
	norm = True 
	print("Data is normalised because your second input is 1. Put 0 for none normalised data")
def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict
if Task == 1:
	max_time = 25000
	time_dict = file_opener("task_1/results/total_time_w_sr_results")
if Task == 2:
	max_time = 100001
	time_dict = file_opener("task_2/task_2b/results/task2b_results_times_b_50_r_100")

x = [] #robots
y = [] #boxes
for r in range(10,101,2):  ## 10 to 126 (per 5)
	x.append(r)
for b in range(10,51,2):  ## 10 to 101 (per 10)
	y.append(b)
Z = np.full([len(y),len(x)],0.)
# Normalising results
maximum = np.full([len(y),1],0.)
minimum = np.full([len(y),1],0.)
maximum_onenum = 0 
minimum_onenum = 100000 

for b in range(len(y)):
	list_max_min = []
	box = y[b]
	for robot in x:
		list_max_min.append(time_dict[robot][box])
	
		if time_dict[robot][box] >= maximum_onenum:
			maximum_onenum = time_dict[robot][box]
		if time_dict[robot][box] <= minimum_onenum:
			minimum_onenum = time_dict[robot][box]
	maximum[b] = max(list_max_min)
	minimum[b] = min(list_max_min)
	
for i_n in range(len(x)):
	for i_b in range(len(y)): #### should this not be just in y?
		b = y[i_b]
		n = x[i_n]
		if time_dict[n][b] == max_time:
			time_dict[n][b] = max_time-1
		if norm == True:
			Z[i_b,i_n] = (time_dict[n][b] - minimum[i_b])/(maximum[i_b] - minimum[i_b])
#		Z[i_b,i_n] = (time_dict[n][b] - minimum_onenum)/(maximum_onenum - minimum_onenum)

		if norm == False:
			Z[i_b,i_n] = time_dict[n][b] 

fig, ax = plt.subplots()

if norm == True:
	levs = np.arange(0,11,1)
	levs = levs/10
if norm == False:
	max_out = 50000
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

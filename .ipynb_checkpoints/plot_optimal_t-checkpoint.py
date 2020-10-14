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

time_dict = file_opener("new_total_task"+str(Task)+"_time_results")
max_time = 10000
min_time = max_time

x = [] #robots
y = [] #boxes
min_time = []
max_time_p = []
min_time_r = []
max_time_r = []
for r in range(10,51,2):
#for r in range(10,51,2):  ## 10 to 126 (per 5)
	x.append(r)
	min_time_r.append(-1)
	max_time_r.append(-1)
#for b in range(10,51,2):  ## 10 to 101 (per 10)
for b in range(10,51,2):
	y.append(b)
	min_time.append(max_time)
	max_time_p.append(0)

Z = np.full([len(y),len(x)],0.)

for i_b in range(len(y)):
	for i_n in range(len(x)): #### should this not be just in y?
		b = y[i_b]
		n = x[i_n]
		min_time[i_b] = min_time[i_b]/b
		max_time_p[i_b] = max_time_p[i_b]/b
		time_dict[n][b] = time_dict[n][b]/b

		if time_dict[n][b] < min_time[i_b]:
			min_time[i_b] = time_dict[n][b]
			min_time_r[i_b] = n
		if time_dict[n][b] > max_time_p[i_b]:
			max_time_p[i_b] = time_dict[n][b]
			max_time_r[i_b] = n
		
print(max_time_r)
print(max_time_p)
print(min_time)
print(min_time_r)
		
fig, ax = plt.subplots()

plt.xlabel("Number of agents")
plt.ylabel("Number of boxes requested")
plt.show()

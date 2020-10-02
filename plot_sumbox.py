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

def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict
time = []
rob = []
fig, ax = plt.subplots()
time_dict = file_opener("task_1/results/task_1_sr_R50_B50")
#time_dict = file_opener("task_1/results/task_1_times_w_sr_R50_B50")
for r in range(10,52,2):
	sum_r = 0.
	rob.append(r)
	num_b = 1
	for b in range(10,51,2):
		sum_r += time_dict[r][b]
		num_b += 1
	#time.append((sum_r/num_b)/(60*60))
	#time.append(sum_r)
	time.append(sum_r/num_b)
#time_dict = file_opener("task_1/results/task_1_times_w_sr_R100_B50")
time_dict = file_opener("task_1/results/task_1_sr_R100_B50")

for r in range(52,101,2):
	sum_r = 0.
	rob.append(r)
	num_b = 1
	for b in range(10,51,2):
		sum_r += time_dict[r][b]
		num_b += 1
	#time.append((sum_r/num_b)/(60*60))
	#time.append(sum_r)
	time.append(sum_r/num_b)
print(time)
print(rob)
ax.plot(rob,time)
plt.xlabel("Number of agents")
#plt.ylabel("Sum of times for all boxes")
#plt.ylabel("Average time for all boxes (hours)")
plt.ylabel("Average success rate over all boxes")
#plt.ylim(0.5,1.)
plt.show()

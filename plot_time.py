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

#time_dict = file_opener("task_2_total_results_time")
time_dict = file_opener("new_total_task"+str(Task)+"_time_results")
#time_dict = file_opener("task_2_disp_bias_total_results_time")
#time_dict = file_opener("new_total_task2_bias_time_results")
#time_dict = file_opener("total_disp_time")
#max_time = 50000
#max_time = 100001
#max_time = 15001
max_time = 10000
min_time = 10000

sr = file_opener("new_total_task2_disp_bias_sr_results")

x = [] #robots
y = [] #boxes
for r in range(10,51,2):
#for r in range(10,51,2):  ## 10 to 126 (per 5)
	x.append(r)
#for b in range(10,51,2):  ## 10 to 101 (per 10)
for b in range(10,51,2):
	y.append(b)

Z = np.full([len(y),len(x)],0.)

for i_b in range(len(y)):
	for i_n in range(len(x)): #### should this not be just in y?
		b = y[i_b]
		n = x[i_n]
		#print(b)
		#print(n)
		#if sr[n][b] == 1.0:
			#if time_dict[n][b] == max_time:
			#	time_dict[n][b] = max_time-1
		if time_dict[n][b] < min_time:
			min_time = time_dict[n][b]
		if time_dict[n][b] == max_time:
			time_dict[n][b] == max_time+1
		if time_dict[n][b] >= max_time:
			#time_dict[n][b] = max_time+1
			max_time = time_dict[n][b]
			print(max_time)
			#print(time_dict[n][b])
			#time_dict[n][b] = 10001
			#max_time = 10001
		Z[i_b,i_n] = time_dict[n][b] 
		
			
fig, ax = plt.subplots()
max_out = 10000
print(min_time)
print(max_time)
#levs = np.arange(0,10000+1001,1000)
min_time = 3500
levs = np.arange(min_time,max_out+1+max_out/5, max_out/5)
#levs = np.arange(0,max_out+((max_out-1)/10)+1,(max_out-1)/10)
#levs = np.arange(0,187502,1000)
#levs = np.arange(2500,max_out+2000,1500)#max_out/10)

cs = ax.contourf(x, y, Z, 
				 levs,
				 cmap = "Greys",
				# linestyle = 'solid'
				# cmap = "rainbow"
				#cmap = "Purples"
				#norm=colors.LogNorm()
				)
cbar = fig.colorbar(cs, ticks = [levs])
cbar.ax.set_yticklabels(["{:}".format(i) for i in cbar.get_ticks()]) # set ticks of your format

cbar.set_label("Time taken (s)")
plt.title("Time taken to complete task "+str(Task)+"")

plt.xlabel("Number of agents")
plt.ylabel("Number of boxes requested")
plt.show()

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
max_time_c = 0 

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
		if time_dict[n][b]/n < min_time:
			min_time = time_dict[n][b]/n
		if time_dict[n][b]/n > max_time_c:
			max_time_c = time_dict[n][b]/n
		Z[i_b,i_n] = time_dict[n][b]/n
		
print(Z)
fig, ax = plt.subplots()
max_out = max_time_c
print(max_time_c)
print(min_time)
#levs = np.arange(0,max_out+1,max_out/10)
#levs = np.arange(3000,max_out+2000,max_out/5)
levs = np.arange(min_time,max_out+1,100)
cs = ax.contourf(x, y, Z, 
				 levs,
				 cmap = "Greys"
				# cmap = "rainbow"
#				 norm=colors.LogNorm()
				)
cbar = fig.colorbar(cs, ticks = [levs])
cbar.ax.set_yticklabels(["{:}".format(i) for i in cbar.get_ticks()]) # set ticks of your format

cbar.set_label("Time taken (s)")
plt.title("Time taken to complete task "+str(Task))

plt.xlabel("Number of agents")
plt.ylabel("Number of boxes requested")
plt.show()

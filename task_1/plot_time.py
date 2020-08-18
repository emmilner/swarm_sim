import numpy as np
import matplotlib.pylab as plt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as colors
import ast
from matplotlib.legend import Legend

def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict

time_dict = file_opener("total_time_results")

x = [] #robots
y = [] #boxes
for r in range(10,126,5):  ## 10 to 126 (per 5)
	x.append(r)
for b in range(10,101,10):  ## 10 to 101 (per 10)
	y.append(b)
Z = np.full([len(y),len(x)],0.)
# Normalising results
maximum = np.full([len(y),1],0.)
minimum = np.full([len(y),1],0.)

for b in range(len(y)):
	list_max_min = []
	box = y[b]
	for robot in x:
		list_max_min.append(time_dict[robot][box])
	maximum[b] = max(list_max_min)
	minimum[b] = min(list_max_min)
	
for i_n in range(len(x)):
	for i_b in range(len(y)): #### should this not be just in y?
		b = y[i_b]
		n = x[i_n]
		if time_dict[n][b] == 20000:
			time_dict[n][b] = 19999
		Z[i_b,i_n] = (time_dict[n][b] - minimum[i_b])/(maximum[i_b] - minimum[i_b])
 	#	Z[i_b,i_n] = (time_dict[n])[b] / 20000
	#

X, Y = np.meshgrid(x, y)
fig, ax = plt.subplots()
#im = ax.pcolormesh(x, y, Z)
#lev_exp = np.arange(np.floor(np.log10(Z.min())-1),
 #                  np.ceil(np.log10(Z.max())+1))
#levs = np.power(10, lev_exp)
#levs = np.arange(np.floor(0),
#				np.ceil(20000))
cs = ax.contourf(x, y, Z, 
#				 levs,
				 cmap = "Greys_r"
#				 norm=colors.LogNorm()
				)
cbar = fig.colorbar(cs)
plt.xlabel("Number of agents")
plt.ylabel("Number of boxes requested")
plt.title("Time taken to complete task")
#fig.colorbar(im)
plt.show()

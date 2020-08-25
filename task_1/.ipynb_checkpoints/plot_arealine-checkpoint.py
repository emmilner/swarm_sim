import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import ast


def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict

time_dict = file_opener("results/times_R125_B100")

x = [] #robots
y = [] #boxes
for r in range(10,46,5):  ## 10 to 126 (per 5)
	x.append(r)
for b in range(10,101,10):  ## 10 to 101 (per 10)
	y.append(b)

lines_robot_range = []
lines_box_range = []
handles_robot = []
handles_box = []
t = []
lines = []
for R in range(len(x)):
	r = x[R]
	for B in range(len(y)):
		b = y[B]
		t.append(time_dict[r][b])
#	lines_box_range += ax.plot(y,t)
#	handles_box.append("Robot #"+str(r))

box = []
k = []
for i in range(len(x)):
	for j in range(len(y)):
		box.append(y[j])
		k.append(time_dict[x[i]][y[j]])

my_count=x
df = pd.DataFrame({
"robots":np.repeat(x,len(y)), #countries
"boxes":box, # years
"time":k #values
})

# Create a grid : initialize it
g = sns.FacetGrid(df, col='robots', hue='robots', col_wrap=4, )
 
# Add the line over the area with the plot function
g = g.map(plt.plot, 'boxes', 'time')
 
# Fill the area with fill_between
g = g.map(plt.fill_between, 'boxes', 'time', alpha=0.2).set_titles("{col_name} robots")
 
# Control the title of each facet
g = g.set_titles("{col_name}")
 
# Add a title for the whole plo
plt.subplots_adjust(top=0.92)
g = g.fig.suptitle('Time taken to complete task 1')
 
plt.show()

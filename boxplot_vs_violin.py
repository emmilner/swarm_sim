"""
===================================
Box plot vs. violin plot comparison
===================================

Note that although violin plots are closely related to Tukey's (1977)
box plots, they add useful information such as the distribution of the
sample data (density trace).

By default, box plots show data points outside 1.5 * the inter-quartile
range as outliers above or below the whiskers whereas violin plots show
the whole range of the data.

A good general reference on boxplots and their history can be found
here: http://vita.had.co.nz/papers/boxplots.pdf

Violin plots require matplotlib >= 1.4.

For more information on violin plots, the scikit-learn docs have a great
section: http://scikit-learn.org/stable/modules/density.html
"""

import matplotlib.pyplot as plt
import numpy as np
import ast


###############
boxes = []
robots = []
max_time = 17500
min_time = 0#max_time
for i in range(50,9,-1):
	boxes.append(i)

for i in range(10,51):
	robots.append(i)
	
def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict
def get_times(time):
	#mean = 100000
	times = np.empty((len(boxes),len(robots)))
	min_val = 100000
	min_b = -1
	min_r = -1
	min_p_b = 0 
	for r in range(len(robots)):
		#mean_min = 0 
		for b in range(len(boxes)):
			times[b,r] = time[robots[r]][boxes[b]]
			min_p_b = times[b,r]/boxes[b]
			if min_p_b < min_val:
				min_val = min_p_b
				min_b = boxes[b]
				min_r = robots[r]
				total_time = times[b,r]
				
	print(total_time,min_b,min_r,min_p_b)
	return times
time3 = file_opener("task1_nov_results")
all_data = get_times(time3)

################


fig, axes = plt.subplots()


# plot violin plot
axes.violinplot(all_data,
                   showmeans=False,
                   showmedians=True)
axes.set_title('Violin plot')

# add x-tick labels
plt.setp(axes)
plt.show()

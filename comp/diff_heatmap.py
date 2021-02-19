import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import ast 

boxes = []
robots = []

for i in range(49,9,-1):
	boxes.append(i)

for i in range(10,20):
	robots.append(i)
	
def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict
def get_times(time):
	times = np.empty((len(boxes),len(robots)))*np.nan
	for r in range(len(robots)):
		for b in range(len(boxes)):
			times[b,r] = time[robots[r]][boxes[b]]
	return times
fig, ax = plt.subplots(nrows=1,ncols=1,sharex=True,sharey=True)
time_2 = file_opener("task_1_w_bias_new")

time_new = file_opener("mesh/task_1_mesh")

for j in range(0,2):
	if j == 0: 
		times_1 = get_times(time_2)
		title = "Unordered retrieval with bias"
		#i = 0,0
		i = 0 
	if j == 1: 
		times_2 = get_times(time_new)
		title = "Difference new ideas - with BHB only"
		#i = 0,1
		i = 1
	if j == 2: 
		times = get_times(time_3)
		title = "Ordered retrieval"
		#i = 1,0
		i = 0 
	if j == 3: 
		times = get_times(time_4)
		title = "Ordered retrieval with bias"
		#i = 1,1
		i = 1
times = times_2 - times_1
im1 = ax.imshow(times, cmap= "Accent")#, clim=(0,16000))
cbar = ax.figure.colorbar(im1, ax=ax)
ax.set_title(title,fontsize =  15)
cbar.set_label("Time taken (s)",fontsize = 15 )
ax.set_xticks([0,10,20,30,40])
ax.set_yticks([40,30,20,10,0])
ax.set_xticklabels(range(10,51,10),fontsize = 15)
ax.set_yticklabels(range(10,51,10),fontsize = 15)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
        rotation_mode="anchor",fontsize=15)
ax.set_ylabel("Number of boxes",fontsize = 10)
ax.set_xlabel("Number of robots",fontsize = 10 )
plt.show()

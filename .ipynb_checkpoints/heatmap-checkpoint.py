import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import ast 

boxes = []
robots = []
max_time = 10000
for i in range(50,9,-2):
	boxes.append(i)

for i in range(10,51,2):
	robots.append(i)
	
def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict

time = file_opener("new_total_task1_time_results")
#time = file_opener("task_2_total_results_time")
#time = file_opener("task_2_disp_bias_total_results_time")
#time = file_opener("new_total_task2_bias_time_results")
#time = file_opener("total_disp_time")
times = np.empty((len(robots),len(boxes)))
fig, ax = plt.subplots()
for r in range(len(robots)):
	for b in range(len(boxes)):
		times[b,r] = time[robots[r]][boxes[b]]
		#text = ax.text(b, r, times[r, b],
         #              ha="center", va="center", color="w")

im = ax.imshow(times, cmap= "rainbow", clim=(0,max_time))
cbar = ax.figure.colorbar(im, ax=ax)

ax.set_xticks(np.arange(len(robots)))
ax.set_yticks(np.arange(len(boxes)))
ax.set_xticklabels(robots)
ax.set_yticklabels(boxes)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

fig.tight_layout()
plt.show()
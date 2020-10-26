import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import ast 

boxes = []
robots = []
max_time = 100000
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

#time = file_opener("task1_v_time")
#time = file_opener("task2_v_time_wo_reshuffle")
time = file_opener("task2_v_time_w_reshuffle")
#time = file_opener("task_2_w_bias")
#time = file_opener("new_total_task1_time_results")
#time = file_opener("task_2_total_results_time")
#time = file_opener("task_2_disp_bias_total_results_time")
#time = file_opener("new_total_task2_bias_time_results")
#time = file_opener("total_disp_time")
times = np.empty((len(robots),len(boxes)))
fig, ax = plt.subplots()
for r in range(len(robots)):
	for b in range(len(boxes)):
		times[b,r] = time[robots[r]][boxes[b]]
		#if times[b,r] < min_time:
		#	min_time = times[b,r]
		if times[b,r] >= max_time:
			times[b,r] = times[b,r]
		#	max_time = times[b,r]

		#text = ax.text(b, r, times[r, b],
         #              ha="center", va="center", color="w")

im = ax.imshow(times, cmap= "rainbow", clim=(min_time,max_time))
cbar = ax.figure.colorbar(im, ax=ax)

ax.set_xticks(np.arange(len(robots)))
ax.set_yticks(np.arange(len(boxes)))

ax.set_xticklabels(robots)
ax.set_yticklabels(boxes)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
ax.set_ylabel("Number of boxes",fontsize = 20)
ax.set_xlabel("Number of robots",fontsize =20 )
plt.title("Unordered retrieval, time taken",fontsize = 20)
cbar.set_label("Time taken (s)",fontsize = 20 )

fig.tight_layout()
plt.show()
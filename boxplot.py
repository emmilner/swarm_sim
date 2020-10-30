import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import ast 

boxes = []
robots = []
max_time = 10000
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
	mean = 100000
	times = np.empty((len(boxes),len(robots)))
	for r in range(len(robots)):
		mean_min = 0 
		for b in range(len(boxes)):
			times[b,r] = time[robots[r]][boxes[b]]
			mean_min += times[b,r]
			#if times[b,r] < min_time:
			#	min_time = times[b,r]
			#if times[b,r] >= max_time:
			#	times[b,r] = times[b,r]+10
			#	max_time = times[b,r]
		mean_min = mean_min/b
		if mean_min < mean:
			mean = mean_min
			r_mean = r 
			#text = ax.text(r, b, times[b,r],
			 #             ha="center", va="center", color="w")
	return times

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
fig, ax = plt.subplots()
time = file_opener("task_1_100000")
time2 = file_opener("task_1_w_bias")
#time = file_opener("task2_v_time_wo_reshuffle")
time3 = file_opener("task2_v_time_w_reshuffle")
time4 = file_opener("task_2_w_bias")
#time = file_opener("new_total_task1_time_results")
#time = file_opener("task_2_total_results_time")
#time = file_opener("task_2_disp_bias_total_results_time")
#time = file_opener("new_total_task2_bias_time_results")
#time = file_opener("total_disp_time")

times = get_times(time)
c = "red"
bp1 = ax.boxplot(times,patch_artist= True,boxprops=dict(facecolor=c, color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            )

times = get_times(time2)
c = "blue"
bp2 = ax.boxplot(times,patch_artist= True,boxprops=dict(facecolor=c, color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            )
times = get_times(time3)
c = "magenta"
bp3 = ax.boxplot(times,patch_artist= True,boxprops=dict(facecolor=c, color=c),
            capprops=dict(color=c),
            whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            )
times = get_times(time4)
c = "green"
bp4 = ax.boxplot(times,patch_artist= True,boxprops=dict(facecolor=c, color=c),
            capprops=dict(color=c),
           whiskerprops=dict(color=c),
            flierprops=dict(color=c, markeredgecolor=c),
            )
matplotlib.pyplot.boxplot(times)
ax.legend([bp1["boxes"][0], 
		  bp2["boxes"][0], 
		   bp3["boxes"][0],
		   bp4["boxes"][0]
		  ], ['Unordered without bias', 
			  'Unordered without bias',
			  'Ordered without bias',
			  'Ordered with bias',
			 ], loc='upper right',fontsize = 20 )
ax.set_xlabel("Number of robots",fontsize = 20)
ax.set_ylabel("Time taken (s)",fontsize = 20)
pos = []
for r in range(len(robots)+1):
	pos.append(r)
robots = np.insert(robots,0,0)
plt.xticks(pos,robots)
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 15)

plt.title("Time taken to deliver all the boxes",fontsize = 20)
plt.ylim(0,70000)
#times = NormalizeData(times)
#max_time = 1
#min_time = 0 

plt.show()
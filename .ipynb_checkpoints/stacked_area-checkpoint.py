import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import ast 
import pandas as pd

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

fig, ax = plt.subplots(1,2,sharex='col', sharey='row')
time1 = file_opener("task1_nov_results")
time2 = file_opener("task_1_w_bias")
time3 = file_opener("task2_nov_results")
time4 = file_opener("task2bias_nov_results")
#time = file_opener("new_total_task1_time_results")
#time = file_opener("task_2_total_results_time")
#time = file_opener("task_2_disp_bias_total_results_time")
#time = file_opener("new_total_task2_bias_time_results")
#time = file_opener("total_disp_time")
def plot_line(times,colour,m,a):
	min_time = []
	max_time = []
	robots = [i for i in range(10,51)]
	list_b = []
	new_time = []
	for n in range(41):
		min_time.append(100000)
		max_time.append(0)
		for b in range(41):
			time_nb = times[b,n]
			if time_nb < min_time[n]:
				min_time[n] = time_nb

			if time_nb > max_time[n]:
				max_time[n] = time_nb
		#plt.plot([n+m,n+m],[min_time[n],max_time[n]],colour)
		new_time.append([min_time[n],max_time[n]])
	if a == 1:
		ax[0].plot(robots,min_time,color=colour)
		ax[0].plot(robots,max_time,color=colour)
		ax[0].fill_between(robots,max_time,min_time,facecolor=colour,alpha=0.5)
	if a == 2: 
		ax[1].plot(robots,min_time,color=colour)
		ax[1].plot(robots,max_time,color=colour)
		ax[1].fill_between(robots,max_time,min_time,facecolor=colour,alpha=0.5)
	
	return min_time,max_time

time = get_times(time2)
min_time,max_time = plot_line(time,'green',0,1)
time = get_times(time4)
min_time,max_time = plot_line(time,'magenta',0,1)
time = get_times(time3)
min_time,max_time = plot_line(time,'blue',0,2)
time = get_times(time1)
min_time,max_time = plot_line(time,'orange',0,2)
#dataFrame = pd.DataFrame([time1[0],time1[1]],robots)
#dataFrame.plot(kind='area',stacked=False)
#plt.show(block=True)
		

#plt.legend([plot1,plot2,plot3,plot4], ['Unordered without bias',
#									   'Unordered with bias',
#									   'Ordered without bias',
#									   'Ordered with bias']) #loc='upper right',fontsize = 20 )
ax[0].set_xlabel("Number of robots",fontsize = 20)
ax[0].set_ylabel("Time taken (s)",fontsize = 20)
pos = []
#for r in range(len(robots)+1):
#	pos.append(r)
#robots = np.insert(robots,0,0)
#plt.xticks(pos,robots)
plt.xticks(fontsize = 8)
plt.yticks(fontsize = 10)

#plt.title("Time taken to deliver all the boxes, Ordered task",fontsize = 20)
fig.suptitle("Time taken to deliver all the boxes",fontsize = 20 )
#fig.xlim(10,50)
#fig.ylim(0,100000)
for ax in ax.flat:
	ax.set(xlabel="num",ylabel="time")
plt.xlim(10,50)
plt.ylim(0,100000)
#times = NormalizeData(times)
#max_time = 1
#min_time = 0 

plt.show()
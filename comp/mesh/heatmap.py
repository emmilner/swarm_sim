import numpy as np 
import matplotlib
import matplotlib.pyplot as plt
import ast 

boxes = []
robots = []

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
	max_time = 0
	min_time = 100000#max_time
	times = np.empty((len(boxes),len(robots)))*np.nan
	time_m = np.empty((len(boxes),len(robots)))*np.nan
	for r in range(len(robots)):
		for b in range(len(boxes)):
			times[b,r] = time[robots[r]][boxes[b]]#/boxes[b]
			if boxes[b] == 50:
				print(robots[r])
				print(times[b,r])
				
	print("--")
#if time[robots[r]][boxes[b]] < max_time and time[robots[r]][boxes[b]] > min_time:
				#times[b,r] = time[robots[r]][boxes[b]]
			#if times[b,r] < min_time:
			#	min_time = times[b,r]
			#if time[robots[r]][boxes[b]]/boxes[b] > max_time:
		#	if time[robots[r]][boxes[b]] > max_time:
		#		max_time = time[robots[r]][boxes[b]]#/boxes[b]
		#		max_b = boxes[b]
		#		max_r = robots[r]
			#if time[robots[r]][boxes[b]]/boxes[b] < min_time:
		#	if time[robots[r]][boxes[b]] < min_time:
		#		min_time = time[robots[r]][boxes[b]]#/boxes[b]
		#		min_b = boxes[b]
		#		min_r = robots[r]
			#text = ax.text(r, b, times[b,r],
			             # ha="center", va="center", color="w")
	#times = time_m
	#print("time",time[50][50])
	#print(max_time)
	#print("b", max_b, "r", max_r)
	#print(min_time)
	#print("b", min_b, "r", min_r)

	return times

fig, ax = plt.subplots(nrows=1,ncols=2,sharex=True,sharey=True)
time_1 = file_opener("task_1_new")
time_3 = file_opener("task_2_new")
#time_3 = file_opener("task2_nov_results")
time_4 = file_opener("task_2_w_bias_new")
#time_3 = file_opener("task_2_mesh")
#time_new = file_opener("times_newideas") #task 1 only 
time_2 = file_opener("task1_mesh11_new")
#time_2 = file_opener("task_1_w_bias_new")
#time_4 = file_opener("task2_mesh1_new")
#for r in range(10,51,5):
#	time_D = []
#	for b in range(10,51,5):
#		time_D.append(time_1[r][b])
#	print(time_D)

for j in range(0,2):
	if j == 0: 
		times = get_times(time_1)
		title = "Unordered retrieval"
		#i = 0,0
		i = 0 
	if j == 1: 
		times = get_times(time_2)
		title = "Unordered retrieval with bias"
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
	
	#print(i)
	im1 = ax[i].imshow(times, cmap= "rainbow")#,vmin=0,vmax=25000)#"Greys_r")#, clim=(0,16000))
	cbar = ax[i].figure.colorbar(im1, ax=ax[i])
	ax[i].set_title(title,fontsize =  15)
	cbar.set_label("Time taken (s)",fontsize = 15 )
	#ax.set_xticks(np.arange(len(robots),10))
	ax[i].set_xticks([0,10,20,30,40])
	#ax.set_yticks(np.arange(len(boxes)))
	ax[i].set_yticks([40,30,20,10,0])
	#ax.set_xticklabels(robots,fontsize = 10)
	ax[i].set_xticklabels(range(10,51,10),fontsize = 15)
	ax[i].set_yticklabels(range(10,51,10),fontsize = 15)
	#ax.set_yticklabels(boxes,fontsize = 10)
	plt.setp(ax[i].get_xticklabels(), rotation=45, ha="right",
       rotation_mode="anchor",fontsize=15)
	ax[i].set_ylabel("Number of boxes",fontsize = 10)
	ax[i].set_xlabel("Number of robots",fontsize = 10 )
#fig.tight_layout()
plt.show()

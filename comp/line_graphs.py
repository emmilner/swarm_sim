# new ideas line graphs to compare all the times to pick up 10-50 boxes with 50 robots
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
	times = np.empty(len(boxes))*np.nan
	r = len(robots)-20
	for b in range(len(boxes)):
		times[b] = time[robots[r]][boxes[b]]
	return times

#fig, ax = plt.subplots(nrows=1,ncols=2,sharex=True,sharey=True)

time_1 = file_opener("task_1_w_bias_new")
time_new = file_opener("new_ideas/times_newideas")

for j in range(0,2):
	if j == 0: 
		times = get_times(time_1)
		title = "Unordered retrieval with bias"
		#i = 0,0
		i = 0 
	if j == 1: 
		times = get_times(time_new)
		title = "Unordered retrieval with new ideas"
		#i = 0,1
		i = 1
		
	print(times)
	plt.plot(times,boxes)
	plt.legend(["with bias","with new ideas"])
	plt.ylabel("time (s)")
	plt.xlabel("number of boxes")
	plt.title(str(len(robots)-20)+" robots, task 1")
	
plt.show()
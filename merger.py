import numpy as np
import ast

def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict

time = {}
times = {}

for R in range(10,51,5):
	times[R] = {}

name = "task_2/task_2b/results/500000_task_2b_times_w_sr_R25_B25"
time = file_opener(name)
for R in range(10,26,5):
	for B in range(10,26,5):
		times[R][B] = time[R][B]

name = "task_2/task_2b/results/500000_task_2b_times_w_sr_R50_B25"
for R in range(30,51,5):
	for B in range(10,26,5):
		time = file_opener(name)
		times[R][B] = time[R][B]

name = "task_2/task_2b/results/500000_task_2b_times_w_sr_R50_B50"
for R in range(30,51,5):
	for B in range(30,51,5):
		time = file_opener(name)
		times[R][B] = time[R][B]
		
		
name = "task_2/task_2b/results/500000_task_2b_times_w_sr_R25_B50"
for R in range(10,26,5):
	for B in range(30,51,5):
		time = file_opener(name)
		times[R][B] = time[R][B]

print(times)

f = open("500000_task2_times_results.txt","w+")
f.write(str(times))
f.close()

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
for r in range(10,51,2):
	times[r] = {}
	
name = "total_task2_time_results"
times = file_opener(name)

name = "task_2/task_2b/results/task_2b_times_w_sr_R100_B50"
time = file_opener(name)
for r in range(60,101,10):
	times[r] = {}
for r in range(60,101,10):
	for b in range(10,51,10):
		times[r][b] = time[r][b]
				
				
f = open("total_task2_time_results.txt","w+")
f.write(str(times))
f.close()

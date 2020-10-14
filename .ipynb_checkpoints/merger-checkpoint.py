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

for R in range(10,51,2):
	times[R] = {}

name = "task_2/task_2b/task_2_beh_other/results/bias_task_2b_sr_R24_B24"
time = file_opener(name)
for R in range(10,26,2):
	for B in range(10,26,2):
		times[R][B] = time[R][B]

name = "task_2/task_2b/task_2_beh_other/results/bias_task_2b_sr_R50_B24"
for R in range(26,51,2):
	for B in range(10,26,2):
		time = file_opener(name)
		times[R][B] = time[R][B]

name = "task_2/task_2b/task_2_beh_other/results/bias_task_2b_sr_R50_B50"
for R in range(26,51,2):
	for B in range(26,51,2):
		time = file_opener(name)
		times[R][B] = time[R][B]
		
name = "task_2/task_2b/task_2_beh_other/results/bias_task_2b_sr_R24_B50"
for R in range(10,25,2):
	for B in range(26,51,2):
		time = file_opener(name)
		times[R][B] = time[R][B]

print(times)

f = open("new_total_task2_bias_sr_results.txt","w+")
f.write(str(times))
f.close()

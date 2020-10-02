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

for R in range(10,101,10):
	times[R] = {}

name = "new_task2_sr_results"
time = file_opener(name)
for R in range(10,51,10):
	for B in range(10,51,10):
		times[R][B] = time[R][B]

R = 100 
b = 50 
name = "task_2/task_2b/results/task_2b_sr_R"+str(R)+"_B"+str(b)
for R in range(60,101,10):
	for B in range(10,51,10):
		time = file_opener(name)
		times[R][B] = time[R][B]

b = 100 
for R in range(50,101,50):
	name = "task_2/task_2b/results/task_2b_sr_R"+str(R)+"_B"+str(b)
	for B in range(60,101,10):
		if R == 50:
			for r in range(10,51,10):
				time = file_opener(name)
				times[r][B] = time[r][B]
b = 100 
R = 100
name = "task_2/task_2b/results/task_2b_sr_R"+str(R)+"_B"+str(b)
for B in range(60,101,10):
	for r in range(60,101,10):
		time = file_opener(name)
		times[r][B] = time[r][B]


print(times)

f = open("total_task2_sr_results.txt","w+")
f.write(str(times))
f.close()

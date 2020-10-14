import numpy as np
import ast
import sys
import os 

# Tasks: 1, 1shuffle, 2, 2shuffle, 2bias, 2disp
task = str(sys.argv[1])
# results in 10_trial_results
def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict
time_dict = {}
for i in range(10):
	print(i)
for t in range(1,11):
	for r in range(10,30,10):
		for b in range(10,30,10):
			time = file_opener("10_trial_results/task_"+str(task)+"_trial_"+str(t)+"rob_"+str(r)+"_"+str(r+10)+"_box_"+str(b)+"_"+str(b+10))
			for i in range(10):
				time_dict[r+i] = {}
				for j in range(10):
					time_dict[r+i][b+j] = time[r+i][b+j]
					
for t in range(1,11):
	for r in range(30,45,5):
		for b in range(30,45,5):
			time = file_opener("10_trial_results/task_"+str(task)+"_trial_"+str(t)+"rob_"+str(r)+"_"+str(r+5)+"_box_"+str(b)+"_"+str(b+5))
			for i in range(5):
				time_dict[r+i] = {}
				for j in range(5):
					time_dict[r+i][b+j] = time[r+i][b+j]
					
for t in range(1,11):
	for r in range(45,48,2):
		for b in range(45,48,2):
			time = file_opener("10_trial_results/task_"+str(task)+"_trial_"+str(t)+"rob_"+str(r)+"_"+str(r+2)+"_box_"+str(b)+"_"+str(b+2))
			for i in range(2):
				time_dict[r+i] = {}
				for j in range(2):
					time_dict[r+i][b+j] = time[r+i][b+j]
				
h = open("10_trial_results/total_task_"+str(task)".txt", "w+")
h.write(str(time_dict))
h.close()
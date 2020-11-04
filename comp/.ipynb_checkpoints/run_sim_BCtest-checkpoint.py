import sim_task_2
import sys
import pandas as pd

#PBS -t 20,30,35,40,45,50%7
b = int(sys.argv[1])
if b < 35: 
	b_1 = b-10
if b >= 35:
	b_1 = b-5

time_limit = 100000 # how long to give the robots to complete the task
ani = False # Do you want to generate an animation of the behaviour?

dict_time = {}
dict_time["robot"] = {}
dict_time["robot"]["box"] = "time"

for R in range(10,11):
	dict_time[R] = {}
	for B in range(b_1,b):
		data = sim_task_2.data(R,B,ani,time_limit)
		time = int(data.counter)
		dict_time[R][B] = time

print("task 2, redone without error")
print(dict_time)
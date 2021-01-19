import sim_task_2
import sys

#PBS -t 20,30,35,40,45,50%7
r = int(sys.argv[1])
if r < 35: 
	r_1 = r-10
	r_2 = r
if r >= 35:
	r_1 = r-5
	r_2 = r
	if r == 50:
		r_2 = r+1

time_limit = 100 # how long to give the robots to complete the task
ani = False # Do you want to generate an animation of the behaviour?

dict_time = {}
dict_time["robot"] = {}
dict_time["robot"]["box"] = "time"

for R in range(r_1,r_2):
	dict_time[R] = {}
	for B in range(10,51):
		time = 0 
		for trials in range(1,11):
			data = sim_task_2.data(R,B,ani,time_limit)
			time = time + int(data.counter)
		dict_time[R][B] = time/10

print("task 2, redone without error")
print(time_limit)
print(dict_time)
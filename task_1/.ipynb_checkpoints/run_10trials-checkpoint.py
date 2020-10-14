import 
import sys
import os 

limit = 100000
t = int(sys.argv[1])

dictionary_time["robot"] = {}
(dictionary_time["robot"])["box"] = "time taken"
(dictionary_time["trials number out of 10"]) = t
(dictionary_time["time limit"]) = limit
for r in range(10,20):
	dictionary_time[r] = {}
	for b in range(10,20):
		result = task1.set_up(limit,r,b)
		dictionary_time[r][b] = result[1]
print(dictionary_time)

h = open("task_1"+"_trial_"+str(t)+"rob_"+str(r)+"_"+str(r+10)+"_box_"+str(b)+"_"+str(b+10)".txt", "w+")
h.write(str(dictionary_time))
h.close()


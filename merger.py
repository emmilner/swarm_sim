import numpy as np
import ast

def file_opener(name):
	file_in = open("task_2/task_2b/results/%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict

SR = {}
SRs = {}
for r in range(10,51,2):
	SRs[r] = {}
	

for r in range(20,51,10):
	for b in range(20,51,10):
		name = "task_2b_sr_R"+str(r)+"_B"+str(b)
		SR = file_opener(name)
		print(SR)
		i = 8
		j = 8 
		if r == 20:
			i = 10
		if b == 20:
			j = 10 
		for r in range(r-i,r+1,2):
			for b in range(b-j,b+1,2):
				SRs[r][b] = SR[r][b]

f = open("total_task2b_sr_results.txt","w+")
f.write(str(SRs))
f.close()

import numpy as np
import ast

def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict


name1 = "times_R1050_B50100"
name2 = "times_R50100_B1050"
name3 = "times_R100125_B1050"
name4 = "times_R100125_B50100"
name5 = "times_R50100_B50100"
name_first = "times_R1050_B1050"
times = {}
times = file_opener(name_first)

for r in range(10,51,5):
	for b in range(60,101,10): 
		(times[r])[b] = (file_opener(name1)[r])[b]
for r in range(55,101,5):####
	times[r] = {} 
	for b in range(10,51,10):
		times[r][b] = file_opener(name2)[r][b]		
for r in range(100,126,5):
	times[r] = {} 
	for b in range(10,51,10):
		times[r][b] = file_opener(name3)[r][b]		
for r in range(100,126,5):
	for b in range(50,101,10):
		times[r][b] = file_opener(name4)[r][b]
for r in range(50,101,5):
	for b in range(50,101,10):
		times[r][b] = file_opener(name5)[r][b]
print(times[55])
f = open("total_time_results.txt","w+")
f.write(str(times))
f.close()

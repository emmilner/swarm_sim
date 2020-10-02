import numpy as np
import matplotlib.pylab as plt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
import ast 
from matplotlib.legend import Legend
import sys
import os 
import re

def file_opener(name):
	file_in = open("%s" % name, "r")
	string = ""
	f = []
	for line in file_in.readlines():
		string = line 
		string_new = string.replace("[","")
		string_new = string_new.replace("]","")
		string_new = string_new.split()
		string_new = string_new[0].replace(",","")
		string_new = int(string_new)
		f.append(string_new)
	file_in.close()
	return f

boxes = []
for b in range(10,21,2):
	boxes.append(b)
first_num_avg_list = []

for n in range(42,62,1):
	if n != 44 and n != 55 and n != 57 and n != 60 :
		print(n)
		name = "task_2/task_2b/results/BC_task2b.sh.o99709"+str(n)
		first_numbers = file_opener(name)
		for robot in range(10,21,2):
			#b_n = 0 
			for L in range(1,19,3):
				first_num_avg = []
			#	b = boxes[b_n]
			#	print("b",b)
				for trials in range(3):
					first_num_avg.append(first_numbers[L])
					L +=1
				first_num_avg = np.max(first_num_avg)
				first_num_avg_list.append(first_num_avg*50)
			#	b_n +=1
	
print(first_num_avg_list)
max_time = np.max(first_num_avg_list)
print(max_time)
		

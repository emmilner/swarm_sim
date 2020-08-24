import task1
import sys
import os
#r_start = int(sys.argv[1]) # num of robots
#b_start = int(sys.argv[2])
dictionary = {}
dictionary["robot"] = {}
(dictionary["robot"])["box"] = "times"
for r in range(10,12):
	dictionary[r] = {}
	for b in range(10,12):
		time_total = task1.set_up(5000,r,b)
	#	time_total = BC_animate.run_programme(20000,r,b)
		(dictionary[r])[b] = time_total

print(dictionary)
f = open("results_times_b_"+str(b)+"_r_"+".txt", "w+")
f.write(str(dictionary))
f.close()


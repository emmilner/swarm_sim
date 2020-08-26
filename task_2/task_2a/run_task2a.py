import task2a

dictionary = {}
dictionary["robot"] = {}
(dictionary["robot"])["box"] = "times"
for r in range(10,101,10):
	dictionary[r] = {}
	for b in range(10,51,10):
		time_total = task2a.set_up(100000,r,b)
		(dictionary[r])[b] = time_total

print(dictionary)
f = open("task2a_results_times_b_"+str(b)+"_r_"+str(r)+".txt", "w+")
f.write(str(dictionary))
f.close()


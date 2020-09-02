import task2c

trials = 10 
dictionary = {}
dictionary["robot"] = {}
(dictionary["robot"])["box"] = "times"
(dictionary["trials"]) = trials
for r in range(10,101,10):
	dictionary[r] = {}
	for b in range(10,51,10):
		total = 0
		for trial in range(trials):
			total += task2c.set_up(100000,r,b)
		time_avg = total/trials
		(dictionary[r])[b] = time_avg

print(dictionary)
f = open("task2c_results_times_b_"+str(b)+"_r_"+str(r)+".txt", "w+")
f.write(str(dictionary))
f.close()


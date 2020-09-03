import task2a

trials = 5
limit = 10000
dictionary = {}
dictionary["robot"] = {}
(dictionary["robot"])["box"] = "times"
(dictionary["trials no"]) = trials
(dictionary["time limit"]) = limit
for r in range(20,51,10):
	dictionary[r] = {}
	for b in range(20,41,10):
		total = 0 
		print("R = ")
		print(r)
		print("B = ")
		print(b)
		for trial in range(trials):
			total += task2a.set_up(limit,r,b)
		time_avg = total/trials
		(dictionary[r])[b] = time_avg

print(dictionary)
f = open("task2a_results_times_b_"+str(b)+"_r_"+str(r)+".txt", "w+")
f.write(str(dictionary))
f.close()


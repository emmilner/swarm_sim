import task1

trials = 5
dictionary = {}
dictionary["robot"] = {}
(dictionary["robot"])["box"] = "times"
(dictionary["trials no"]) = trials

for r in range(10,101,5):
	dictionary[r] = {}
	for b in range(55,101,5):
		total = 0 
		for trial in range(trials):
			total += task1.set_up(50000,r,b)
			time_avg = total/trials
			(dictionary[r])[b] = time_avg

print(dictionary)
f = open("task_1_times_R"+str(r)+"_B"+str(b)+".txt", "w+")
f.write(str(dictionary))
f.close()


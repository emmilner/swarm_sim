import task1_sr

trials = 10
limit = 25000
dictionary = {}
dictionary["robot"] = {}
(dictionary["robot"])["box"] = "success rate"
(dictionary["trials no"]) = trials
(dictionary["time limit"]) = limit

for r in range(10,51):
	dictionary[r] = {}
	for b in range(10,51):
		total = 0 
		for trial in range(trials):
			total += task1_sr.set_up(limit,r,b)
			sr_avg = 0 
			if total > 0:	
				sr_avg = total/trials
			(dictionary[r])[b] = sr_avg

print(dictionary)
f = open("task_1_sr_R"+str(r)+"_B"+str(b)+".txt", "w+")
f.write(str(dictionary))
f.close()


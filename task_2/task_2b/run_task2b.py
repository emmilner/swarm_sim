import task2b

trials = 2
limit = 50000
dictionary_sr = {}
dictionary_time = {}
dictionary_sr["robot"] = {}
(dictionary_sr["robot"])["box"] = "success rate"
(dictionary_sr["trials no"]) = trials
(dictionary_sr["time limit"]) = limit
dictionary_time["robot"] = {}
(dictionary_time["robot"])["box"] = "time taken"
(dictionary_time["trials no"]) = trials
(dictionary_time["time limit"]) = limit

for r in range(50,51,2):
	dictionary_sr[r] = {}
	dictionary_time[r] = {}
	for b in range(25,26,2):
		time = 0 
		sr = 0.
		for trial in range(trials):
			result = task2b.set_up(limit,r,b)
			sr += result[0]
			time += result[1]
		sr_avg = 0. 
		if sr > 0.:	
			sr_avg = sr/trials
		(dictionary_sr[r])[b] = sr_avg
		(dictionary_time[r])[b] = time/trials

print(dictionary_sr)
print(dictionary_time)
f = open("task_2_sr_R"+str(r)+"_B"+str(b)+".txt", "w+")
f.write(str(dictionary_sr))
f.close()
h = open("task_2_times_w_sr_R"+str(r)+"_B"+str(b)+".txt", "w+")
h.write(str(dictionary_time))
h.close()



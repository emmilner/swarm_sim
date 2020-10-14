import numpy as np 
import task1b

trials = 10 
limit = 10000

r = 15 
b = 50 

dict_prob = {}

for p in np.arange(0,10,0.5):
	sr = 0. 
	print(p)
	for trial in range(trials):
		result = task1b.set_up(limit,r,b,p)
		sr += result[0]
	sr_avg = 0.
	if sr > 0.:
		sr_avg = sr/trials
	dict_prob[p] = sr_avg
print(dict_prob)

h = open("test_prob_task1.txt", "w+")
h.write(str(dict_prob))
h.close()
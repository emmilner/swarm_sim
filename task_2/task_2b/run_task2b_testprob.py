import task2b

trials = 5
limit = 1000
result_p = []
b = 50
r = 15
for p in range(0,10,1):
	result_p.append(-1)
	sr = 0.
	for trial in range(trials):
		result = task2b.set_up(limit,r,b,p)
		sr += result[0]
	sr_avg = 0. 
	if sr > 0.:	
		sr_avg = sr/trials
	result_p[p] = sr_avg
print(result_p)
		


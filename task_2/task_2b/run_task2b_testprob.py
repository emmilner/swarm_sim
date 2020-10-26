import task2_v

trials = 10
limit = 10000
result_p = []
b = 50
r = 15
for p in range(0,50,1):
	result_p.append(-1)
	sr = 0.
	for trial in range(trials):
		result = task2_v.set_up(limit,r,b,p)
		sr += result[0]
	sr_avg = 0. 
	if sr > 0.:	
		sr_avg = sr/trials
	result_p[p] = sr_avg
print(result_p)
		


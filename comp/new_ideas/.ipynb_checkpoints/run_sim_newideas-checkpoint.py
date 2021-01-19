import sim_task_1_newideas
import sim_task_2_newideas
import numpy as np

'Task 1: collect all the items in the time limit'
'Task 2: collect the items in order of their ascending ID number'

'Inputs'
task = 1 # Task 1 or 2?
bias = 1 # Should the behaviour have a heading bias or not?
new_beh = 0 
swarm_size = 25 # number of agents in the swarm 
num_items = 25# number of items to be collected
time_limit = 100000 # how long to give the robots to complete the task
ani = True # Do you want to generate an animation of the behaviour?

##################################################
if new_beh == 0:
	if task == 1:
		if bias == 1:
			data = sim_task_1_newideas.data(swarm_size,num_items,ani,time_limit,1,1,20) #bias L then R
			# bias L, bias R, disp
			#for u in np.arange(5,55,5):
			#	avg = 0 
			#	for i in range(10):
			#		data = sim_task_1_newideas.data(swarm_size,num_items,ani,time_limit,1,1,u)
			#		avg += data.robots.counter
			#	print(avg/10)

	if task == 2:
		if bias == 1:
			trials = 10 
			s = np.zeros(trials)
			for i in range(trials):
				sim = sim_task_2_newideas.data(swarm_size,num_items,ani,time_limit,1)
				s[i] = sim.counter
			print(np.sum(s)/trials)
			print("disp = 20")
			s = np.zeros(trials)
			for i in range(trials):				
				sim = sim_task_2_newideas.data(swarm_size,num_items,ani,time_limit,20)
				s[i] = sim.counter
			print(np.sum(s)/trials)
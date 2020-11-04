import sim_task_1
import sim_task_2
import sim_task_1_bias
import sim_task_2_bias
import sim_task_2_tester

'Task 1: collect all the items in the time limit'
'Task 2: collect the items in order of their ascending ID number'

'Inputs'
task = 2 # Task 1 or 2?
bias = 0 # Should the behaviour have a heading bias or not?
new_beh = 0 
swarm_size = 30 # number of agents in the swarm 
num_items = 50# number of items to be collected
time_limit = 2000 # how long to give the robots to complete the task
ani = True # Do you want to generate an animation of the behaviour?

##################################################
if new_beh == 0:
	if task == 1:
		if bias == 0:
			sim = sim_task_1.data(swarm_size,num_items,ani,time_limit)
		if bias == 1:
			sim = sim_task_1_bias.data(swarm_size,num_items,ani,time_limit)

	if task == 2:
		if bias == 0:
			sim = sim_task_2.data(swarm_size,num_items,ani,time_limit)
			
		if bias == 1:
			sim = sim_task_2_bias.data(swarm_size,num_items,ani,time_limit)
			
if new_beh == 1:
	sim = sim_task_2_tester.data(swarm_size,num_items,ani,time_limit)

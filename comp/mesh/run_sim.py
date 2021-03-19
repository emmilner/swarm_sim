import sim_task_1_mesh
import sim_task_1_mesh_1
import sim_task_1_mesh_2
import sim_task_1_mesh_3
import sim_task_1_mesh_4
import sim_task_1_mesh_5
import sim_task_1_mesh_6
import sim_task_1_mesh_7
import sim_task_1_mesh_8
import sim_task_1_mesh_9
import sim_task_1_mesh_10
import sim_task_1_mesh_11
import sim_task_1_mesh_11circle
import sim_task_1_mesh_12
import sim_task_1_mesh_13
import sim_task_1_mesh_14
import sim_task_2_mesh_1
import sim_task_2_bias
import sim_task_1_bias
import sim_task_2_mesh_2
import sim_task_2_mesh_3
import sim_task_2_mesh_4

print("simulating task 2 with bias")

'Task 1: collect all the items in the time limit'
'Task 2: collect the items in order of their ascending ID number'

'Inputs'
task = 1 # Task 1 or 2?
bias = 1 # Should the behaviour have a heading bias or not?
beh = 0
swarm_size = 10#umber of agents in the swarm 
num_items = 50 #mber of items to be collected
time_limit = 20000 # how long to give the robots to complete the task
ani = True# Do you want to generate an animation of the behaviour?
##################################################
if task == 1:
	if bias == 0:
		sim = sim_task_1.data(swarm_size,num_items,ani,time_limit)
	if bias == 1:
		print("swarm size", swarm_size)
		print(beh)
		trials = 10
		#for swarm_size in range(150,160,10):
		time = 0 

		for i in range(trials):
			if beh == 0:
				sim = sim_task_1_bias.data(swarm_size,num_items,ani,time_limit)
			if beh == 11:
				sim = sim_task_1_mesh_11.data(swarm_size,num_items,ani,time_limit)
		
			time = time + sim.robots.counter
		print(time/trials)
		#print(sim.robots.counter)
		

if task == 2:
	if bias == 0:
		sim = sim_task_2.data(swarm_size,num_items,ani,time_limit)
		
	if bias == 1:
		time = 0 
		trials= 10
		for n in range(trials):
			if beh == 0:
				sim = sim_task_2_bias.data(swarm_size,num_items,ani,time_limit)
			if beh == 1:
				sim = sim_task_2_mesh_1.data(swarm_size,num_items,ani,time_limit)
			if beh == 2:
				sim = sim_task_2_mesh_2.data(swarm_size,num_items,ani,time_limit)
			if beh == 3:
				sim = sim_task_2_mesh_3.data(swarm_size,num_items,ani,time_limit)
			if beh == 4:
				sim = sim_task_2_mesh_4.data(swarm_size,num_items,ani,time_limit)
			time = time+sim.robots.counter
		print(time/trials)
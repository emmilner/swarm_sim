import behtree.treegen as tg
import sys
import random
import simulation.asim as asim
import numpy as np

'''

Set of functions used to evaluate the performance of individuals.

'''
def adveserial(popa, popb, swarma, swarmb, targets, genum, timesteps):


	# Two supervisors competing against each other for coverage
	for z in range(0, len(popa)):
		# Decode genome into executable behaviour tree
		print( 'Evaluating Individual: ', z, ' Gen: ', genum)
		bta = tg.tree().decode(popa[z], swarma, targets)
		tg.tree().ascii_tree(popa[z])

		btb = tg.tree().decode(popb[z], swarmb, targets)
		tg.tree().ascii_tree(popb[z])
		
		# Set the number of trials per individual to determine fitness
		trials = 1; dur = 0
		scorea = 0 ; scoreb = 0; totscore = 0
		for k in range(trials):
			fitness = 0
			t = 0
			found = False
			# IMPORTANT! need to reset behaviours after each run 
			
			bta = tg.tree().decode(popa[z], swarma, targets)
			btb = tg.tree().decode(popb[z], swarmb, targets)
			

			while t <= timesteps and found == False:
				t += 1
				bta.tick()
				btb.tick()
				swarma.iterate()
				swarma.get_state()
				swarmb.iterate()
				swarmb.get_state()
				scorea += targets.ad_state(swarma, t)
				scoreb += targets.ad_state(swarmb, t)
				if targets.found == len(targets.targets):
					found = True
			
			#totscore += score
			targets.reset()
			swarma.reset()
			swarmb.reset()
			
		print ('-------------------------------------------------------------------')
		
		maxsize = 300
		fitness = 0
		fitness = scorea/(trials*len(targets.targets))
		fitness = fitness - (len(popa[z].genome)/1000000)
		if fitness < 0: fitness = 0

		popa[z].fitness = fitness

		print ('Individual fitness A: ', fitness)
		popb[z].fitness = fitness
		print ('=================================================================================')

		fitness = 0
		fitness = scoreb/(trials*len(targets.targets))
		fitness = fitness - (len(popb[z].genome)/1000000)
		if fitness < 0: fitness = 0
		
		print ('Individual fitness B: ', fitness)
		popb[z].fitness = fitness
		print ('=================================================================================')



def serial1(pop, swarm, targets, genum, timesteps, treecost):
	# Evaluate fitness of each individual in population


	for z in range(0, len(pop)):

		swarmsize = 3
		swarm = asim.swarm()
		swarm.size = swarmsize
		swarm.behaviour = 'none'
		swarm.speed = 0.5
		swarm.origin = np.array([0, 0])
		swarm.gen_agents()


		# swarm = swarm.copy()
		# swarm.gen_agents()

		env = asim.map()
		env.exercise1()
		env.gen()
		swarm.map = env

		# Decode genome into executable behaviour tree
		print( 'Evaluating Individual: ', z, ' Gen: ', genum)
		bt = tg.tree().decode(pop[z], swarm, targets)
		tg.tree().ascii_tree(pop[z])
		
		# Set the number of trials per individual to determine fitness
		trials = 1; dur = 0
		score = 0 ; totscore = 0

		for k in range(trials):
			fitness = 0
			t = 0
			found = False
			# IMPORTANT! need to reset behaviours after each run 
			swarm.beacon_set = []
			bt = tg.tree().decode(pop[z], swarm, targets)
			while t <= timesteps and found == False:
				t += 1
				bt.tick()
				swarm.iterate()
				swarm.get_state()
				score = targets.get_state(swarm, t)
				if targets.found == len(targets.targets):
					found = True
			
			totscore += score
			targets.reset()
			swarm.reset()
			
		print ('-------------------------------------------------------------------')
		
		maxsize = 300
		fitness = 0
		fitness = totscore/(trials*len(targets.targets))
		fitness = fitness - (len(pop[z].genome)*treecost)
		if fitness < 0: fitness = 0
		
		print ('Individual fitness: ', fitness)
		pop[z].fitness = fitness
		print ('=================================================================================')

def serial2(pop, swarm, targets, genum, timesteps, treecost):
	# Evaluate fitness of each individual in population


	for z in range(0, len(pop)):

		swarmsize = 10
		swarm = asim.swarm()
		swarm.size = swarmsize
		swarm.behaviour = 'none'
		swarm.speed = 1.0
		swarm.origin = np.array([0, 0])
		swarm.gen_agents()


		# swarm = swarm.copy()
		# swarm.gen_agents()

		env = asim.map()
		env.map1()
		env.gen()
		swarm.map = env

		# Decode genome into executable behaviour tree
		print( 'Evaluating Individual: ', z, ' Gen: ', genum)
		bt = tg.tree().decode(pop[z], swarm, targets)
		tg.tree().ascii_tree(pop[z])
		
		# Set the number of trials per individual to determine fitness
		trials = 1; dur = 0
		score = 0 ; totscore = 0

		for k in range(trials):
			fitness = 0
			t = 0
			found = False
			# IMPORTANT! need to reset behaviours after each run 
			swarm.beacon_set = []
			bt = tg.tree().decode(pop[z], swarm, targets)
			while t <= timesteps and found == False:
				t += 1
				bt.tick()
				swarm.iterate()
				swarm.get_state()
				score = targets.get_state(swarm, t)
				if targets.found == len(targets.targets):
					found = True
			
			totscore += score
			targets.reset()
			swarm.reset()
			
		print ('-------------------------------------------------------------------')
		
		maxsize = 300
		fitness = 0
		fitness = totscore/(trials*len(targets.targets))
		fitness = fitness - (len(pop[z].genome)*treecost)
		if fitness < 0: fitness = 0
		
		print ('Individual fitness: ', fitness)
		pop[z].fitness = fitness
		print ('=================================================================================')



def parallel(ind, swarm, targets, timesteps):
	
	bt = tg.tree().decode(ind, swarm, targets)
	tg.tree().ascii_tree(ind)
		
	# Set the number of trials per individual to determine fitness
	trials = 1
	dur = 0
	score = 0
	for k in range(trials):
		fitness = 0
		t = 0
		# RUN SIMULATION!!! ############################################
		found = False
		# IMPORTANT! need to reset behaviours after each run 
		swarm.beacon_set = []
		bt = tg.tree().decode(ind, swarm, targets)
		while t <= timesteps and found == False:
			t += 1
			bt.tick()
			swarm.iterate()
	
			swarm.get_state()
			score += targets.get_state(swarm, t)
			if targets.found == len(targets.targets):
				found = True
		
		targets.reset()
		swarm.reset()
		
	maxsize = 300
	fitness = 0
	fitness = score/(trials*len(targets.targets))
	fitness = fitness - (len(ind.genome)*0.001)
	if fitness < 0: fitness = 0

	ind.fitness = fitness

	return ind
	# Write process output
	# sys.stdout.flush()
	# print('Process: ', id, ' completed')
	# output.put(ind)
	# print(fitness)


#!/usr/bin/env python


import behtree.treegen as tg
import behtree.tree_nodes as tree_nodes
import evo.evaluate as evaluate
import evo.operators as op
import simulation.asim as asim
import py_trees
import sys
import logging
import numpy as np
from functools import partial
from itertools import repeat
import matplotlib.pyplot as plt
import random


# Top level execution of evolutionary algorithm.

if __name__ == '__main__':

	''' Required inputs to evolutionary algorithm:
		
		1. Create swarm object:
			- Define the swarm size.
			- Initialize with behavior 'none'.
			- Set agent speed.
			- Generate an array of agent positions.

		2. Create environment object:
			- Assign the environment object to the swarm.map attribute.

		3. Create the set of targets to search for:
			- Create a target set object and set it's state to match the environment.
			- Set the detection radius.
	'''
	random.seed(1000)
	# Create swarm object
	
	swarmsize = 3
	swarm = asim.swarm()
	swarm.size = swarmsize
	swarm.behaviour = 'none'
	swarm.speed = 0.5
	swarm.origin = np.array([0,-20])
	swarm.gen_agents()

	# Create environment
	env = asim.map()
	env.exercise1()
	env.gen()
	swarm.map = env

	# Set target positions
	targets = asim.target_set()
	state = 'exercise1'
	targets.set_state(state)
	targets.radius = 5
	targets.reset()
	

	'''
	EVOLUTIONARY PARAMETERS --------------------------------------------------------------------
		Evolutionary algorithm parameters:
		NGEN - Number of evolutionary generations.
		popsize - Number of individuals in each population.
		indsize - The maximum depth of trees that are initially generated.
		
		tournsize - The number of individuals taken in each tournament selection.
		mutrate - Probability of performing a mutation on a node of a tree.
		growrate - Probability of growing a random tree during mutation.
		growdepth - The depth of randomly grown trees.
		
		hallsize - The number of individuals saved in the hall of fame.
		elitesize - The number of the best individuals saved between generations. 
		newind - The number of randomly generated individuals added each generation.
		
		treecost - The fitness cost per node for an evolved tree.
		timesteps - The time duration of the simulation   
	
	CHANGE THE PARAMETERS BELOW ==============================================================
	'''

	NGEN = 20; popsize = 20; indsize = 2
	tournsize = 3; mutrate = 0.15; growrate = 0.5; growdepth = 1
	hall = []; hallsize = 20; newind = 2
	elitesize = 2
	treecost = 0.01
	timesteps = 200

	'''
	DON'T CHANGE ANY CODE BELOW THIS LINE
	==========================================================================================
	'''

	selectionNum = popsize - elitesize
	# The test duration for each search attempt

	#Log simulation settings
	filename = 'exercise1'
	filename = 'results/exercise1'
	hfile = filename + '_' + 'hallfame'
	pop_file = filename + '_' + 'pop'
	
	op.log_settings(swarm,popsize,indsize,tournsize,elitesize,mutrate,NGEN,targets,state,timesteps,filename)

	# Generate starting population
	pop = []
	generations = []*NGEN
	pop = [tg.individual(tg.tree().make_tree(indsize)) for t in range(popsize)]
	generations.append(pop)

	#  Logging variables
	logfit = []; logpop = []; logavg = []; logmax = []	
	
	# Start evolution!
	for i in range(0, NGEN):

		print ('GEN: ', i) 
		newpop = []
		# Serial execution
		evaluate.serial1(pop, swarm, targets, i, timesteps, treecost)
		
		# Record results -------------------------------------------------------------------------------------------------
		pop.sort(key=lambda x: x.fitness, reverse=True)
		currentgen = []
		currentgen = [ind.copy() for ind in pop]
		generations.append(currentgen)

		hall = op.hallfame(pop, hall[:], hallsize, hfile)
		op.log(pop, hall, logpop, logfit, logavg, logmax, i, filename)
		op.save_gen(generations, pop_file)

		# Generate the next population -----------------------------------------------------------------------------------
		
		elite = [ind.copy() for ind in pop[0:elitesize]]

		# Remove worst individuals
		newpop = op.tournament(pop[newind:], tournsize, selectionNum-newind)

		newpop = op.crossover(newpop[:])
		newpop = op.mutate(newpop[:], mutrate, growrate, growdepth)

		new = [tg.individual(tg.tree().make_tree(indsize)) for t in range(newind)]
		# Create new population of individuals
		pop = []
		pop = list(newpop + elite + new)

	
	fig, ax = plt.subplots()	

	ax.plot(logavg, 'r', label="Average Fitness")
	ax.plot(logmax, 'g', label="Maximimum Fitness")
	
	ax.set_xlabel("Generation")
	ax.set_ylabel("Fitness")
	ax.set_ylim([0,1.1])
	
	legend = ax.legend(loc="upper left")
	plt.show()
	



import pickle
import random
from behtree.treegen import individual
from behtree.treegen import Operator
from behtree.treegen import Action
from behtree.treegen import Condition
from behtree.treegen import Param
from behtree.treegen import Env_control

import behtree.treegen as tg
'''
Evolutionary operators for manipulating trees.

'''

def crossover(offspring):


	newpop = []
	choice = list(range(0, len(offspring)))


	while len(choice) != 0:
		# print '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><'
		branch = [];children = [];point = []
		# print '\nchoiceeeee  ', len(choice)
		for b in range(0, 2):
			sel = random.randint(0,len(choice)-1)
			children.append(individual(offspring[choice[sel]].genome))
			# print 'seleeeee ',sel 
			choice.remove(choice[sel])
		
		#global opsum
		#global leafsum

		# Choose crossover points
		for c in range(0, 2):
			hasop = False
			# Check whether tree has operator
			for d in range(1, len(children[c].genome)):
				if type(children[c].genome[d]) is Operator:
					hasop = True

			if random.random() <= 0.9 and hasop == True:
				# Choose operator
				p = random.randint(1,len(children[c].genome)-1)
				while type(children[c].genome[p]) is not Operator:
					 p = random.randint(1,len(children[c].genome)-1)
				#opsum += 1
			else:
				# Choose leaf node
				p = random.randint(1,len(children[c].genome)-1)
				while type(children[c].genome[p]) is Operator:
					 p = random.randint(1,len(children[c].genome)-1)
				#leafsum += 1
			point.append(p)
		
		branch.append(children[0].genome[point[0]])
		branch.append(children[1].genome[point[1]])

		flat = []
		# Flatten genome
		for z in range(0,2):
			for x in range(0,len(children[z].genome)):
				if type(children[z].genome[x]) is list:
					for y in range(0,len(children[z].genome[x])):
						flat.append(children[z].genome[x][y])
				else:
					flat.append(children[z].genome[x])
			children[z].genome = flat
			# print '\nflattended ind, ' ,flat
			flat = []

		subtree = [[],[]]

		for i in range(0,2):
			# Build the subtree for crossover
			if type(branch[i]) is Operator:

				finished = False
				treepos = []

				# Add new counter for children
				treepos.append(children[i].genome[point[i]].size)
				subtree[i].append(children[i].genome[point[i]])
				n = (point[i]-1) + 1 
				while finished != True:
					n += 1
					# End current operator if max children is reached.
					if treepos[len(treepos)-1] == 0:

						# Check if tree is completed and then end generation
						if treepos[0] == 0 and len(treepos) == 1:
							# Tree has been completed
							finished = True
						# Important! Reduce current tree position in order to move back up the tree
						del treepos[-1]
						n -= 1
					else:
						# Account for added child
						treepos[len(treepos)-1] = int(treepos[len(treepos)-1]) - 1
						if type(children[i].genome[n]) is Operator:

							subtree[i].append(children[i].genome[n])
							treepos.append(children[i].genome[n].size)
						else:
							subtree[i].append(children[i].genome[n])

				# Remove subtree from genome before crossover
				for z in range(point[i]+1, n+1):
					del children[i].genome[point[i]+1]
			else:
				subtree[i].append(branch[i])

		children[0].genome[point[0]] = subtree[1]
		children[1].genome[point[1]] = subtree[0]

		flat = []
		# Flatten genome
		for z in range(0,2):
			for x in range(0,len(children[z].genome)):
				if type(children[z].genome[x]) is list:
					for y in range(0,len(children[z].genome[x])):
						flat.append(children[z].genome[x][y])
				else:
					flat.append(children[z].genome[x])
			children[z].genome = flat
			# print '\nflattended ind, ' ,flat
			flat = []
		# print '\n-------------------------------------------------------------------------'
		newpop.append(children[0])
		newpop.append(children[1])

	return newpop


	'''
	Take a group of individuals and perform single point crossover
	over random pairs of trees to generate a set of offspring
	'''
	# newpop = []; branch = [];children = [];point = []
	# choice = list(range(0, len(pop)))

	# # Keep picking from the list of individuals with array choice until empty
	# while len(choice) != 0:

	# 	# Pick two random entries in the list choice
	# 	for b in range(0, 2):
	# 		sel = random.randint(0,len(choice)-1)
	# 		children.append(individual(pop[choice[sel]].genome))
	# 		# Remove choice from list
	# 		choice.remove(choice[sel])
		
	# 	# Choose crossover points
	# 	for c in range(0, 2):
	# 		hasop = False
	# 		# Check whether tree has operator
	# 		for d in range(1, len(children[c].genome)):
	# 			if type(children[c].genome[d]) is Operator:
	# 				hasop = True
	# 		'''
	# 		Bias choice towards selecting subtrees in individuals 
	# 		to generate more crossover of genetic material. 0.9 Based
	# 		on standard practice when operating on trees.
	# 		'''
	# 		if random.random() <= 0.9 and hasop == True:
	# 			# Choose operator
	# 			p = random.randint(1,len(children[c].genome)-1)
	# 			while type(children[c].genome[p]) is not Operator:
	# 				 p = random.randint(1,len(children[c].genome)-1)
	# 		else:
	# 			# Choose leaf node
	# 			p = random.randint(1,len(children[c].genome)-1)
	# 			while type(children[c].genome[p]) is Operator:
	# 				 p = random.randint(1,len(children[c].genome)-1)
	# 		point.append(p)
		
	# 	branch.append(children[0].genome[point[0]])
	# 	branch.append(children[1].genome[point[1]])

	# 	flat = []
	# 	# Flatten genome
	# 	for z in range(0,2):
	# 		for x in range(0,len(children[z].genome)):
	# 			if type(children[z].genome[x]) is list:
	# 				for y in range(0,len(children[z].genome[x])):
	# 					flat.append(children[z].genome[x][y])
	# 			else:
	# 				flat.append(children[z].genome[x])
	# 		children[z].genome = flat
	# 		flat = []

	# 	subtree = [[],[]]

	# 	for i in range(0,2):
	# 		# Build the subtree for crossover
	# 		if type(branch[i]) is Operator:

	# 			finished = False
	# 			treepos = []

	# 			# Add new counter for children
	# 			treepos.append(children[i].genome[point[i]].size)
	# 			subtree[i].append(children[i].genome[point[i]])
	# 			n = (point[i]-1) + 1 
	# 			while finished != True:
	# 				n += 1
	# 				# End current operator if max children is reached.
	# 				if treepos[len(treepos)-1] == 0:
	# 					# Check if tree is completed and then end generation
	# 					if treepos[0] == 0 and len(treepos) == 1:
	# 						# Tree has been completed
	# 						finished = True
	# 					# Important! Reduce current tree position in order to move back up the tree
	# 					del treepos[-1]
	# 					n -= 1
	# 				else:
	# 					# Account for added child
	# 					treepos[len(treepos)-1] = int(treepos[len(treepos)-1]) - 1
	# 					if type(children[i].genome[n]) is Operator:

	# 						subtree[i].append(children[i].genome[n])
	# 						treepos.append(children[i].genome[n].size)
	# 					else:
	# 						subtree[i].append(children[i].genome[n])

	# 			# Remove subtree from genome before crossover
	# 			for z in range(point[i]+1, n+1):
	# 				del children[i].genome[point[i]+1]
	# 		else:
	# 			subtree[i].append(branch[i])

	# 	children[0].genome[point[0]] = subtree[1]
	# 	children[1].genome[point[1]] = subtree[0]

	# 	flat = []
	# 	# Flatten genome
	# 	for z in range(0,2):
	# 		for x in range(0,len(children[z].genome)):
	# 			if type(children[z].genome[x]) is list:
	# 				for y in range(0,len(children[z].genome[x])):
	# 					flat.append(children[z].genome[x][y])
	# 			else:
	# 				flat.append(children[z].genome[x])
	# 		children[z].genome = flat
	# 		flat = []
	# 	newpop.append(children[0])
	# 	newpop.append(children[1])

	# return newpop
	
def mutate(offspring, mutrate, growrate, growdepth):

	for a in range(0, len(offspring)):
		for b in range(0, len(offspring[a].genome)):

			if random.random() <= mutrate:
				if random.random() <= growrate and b != 0 and b < len(offspring[a].genome) and type(offspring[a].genome[b]) is not Operator:
					# Grow a randomly generated tree
					
					subtree = tg.tree().make_tree(growdepth)

					del offspring[a].genome[b]
					offspring[a].genome[b:b] = subtree[:]

				else:
					
				
					if type(offspring[a].genome[b]) is Action:
						offspring[a].genome[b].type = random.choice(['disperse','north','south','west','east','northwest','southwest','northeast','northwest'])

					if type(offspring[a].genome[b]) is Param:
						if offspring[a].genome[b].type == 'aggregate':
							offspring[a].genome[b].param = random.choice([30,35,40,45,50,55,60,65,70,75,80])
						else:
							offspring[a].genome[b].param = random.choice([1,5,10,15,20,25,30,35,40,45,50,55,60])

					if type(offspring[a].genome[b]) is Env_control:

						choice = random.choice(['type','pos'])
						if choice == 'type':
							offspring[a].genome[b].type = random.choice(['attract','repel'])
						if choice == 'pos':
							offspring[a].genome[b].pos[0] = random.choice([-34,-32,-30,-28,-26,-24,-22,-20,-18,-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34])
							offspring[a].genome[b].pos[1] = random.choice([-34,-32,-30,-28,-26,-24,-22,-20,-18,-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34])

					if type(offspring[a].genome[b]) is Condition:
					
						# offspring[a].genome[b].generate()
						choice = random.choice(['var','value','op'])
						if choice == 'var':
							offspring[a].genome[b].var = random.choice(['centerx','centery', 'density'])
						if choice == 'op':
							offspring[a].genome[b].op = random.choice(['<','>'])
						if choice == 'value':
							if offspring[a].genome[b].var == 'density':
								offspring[a].genome[b].value = random.choice([1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35])
							if offspring[a].genome[b].var == 'centery':
								offspring[a].genome[b].value = random.choice([-34,-32,-30,-28,-26,-24,-22,-20,-18,-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34])
							if offspring[a].genome[b].var == 'centerx':
								offspring[a].genome[b].value = random.choice([-34,-32,-30,-28,-26,-24,-22,-20,-18,-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34])
							if offspring[a].genome[b].var == 'coverage':
								offspring[a].genome[b].value = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

	return offspring

def reduce(ind):

	for x in range(1, len(ind.genome)):

		if ind.genome[x].type == 'sel':

			if type(ind.genome[x+1]) is Action:

				# Remove selector subtree whose first child is an action and replace with the same action					
				finished = False
				treepos = []
				subtree = []

				# Add new counter for children
				treepos.append(ind.genome[x].size)
				subtree.append(ind.genome[x])
				n = (x-1) + 1 
				while finished != True:
					n += 1
					# End current operator if max children is reached.
					if treepos[len(treepos)-1] == 0:

						# Check if tree is completed and then end generation
						if treepos[0] == 0 and len(treepos) == 1:
							# Tree has been completed
							finished = True
						# Important! Reduce current tree position in order to move back up the tree
						del treepos[-1]
						n -= 1
					else:
						# Account for added child
						treepos[len(treepos)-1] = int(treepos[len(treepos)-1]) - 1
						if type(ind.genome[n]) is Operator:

							subtree.append(ind.genome[n])
							treepos.append(ind.genome[n].size)
						else:
							subtree.append(ind.genome[n])

				# insert replacement node
				ind.genome[x] = ind.genome[x+1]
				# Remove subtree from genome before crossover
				for z in range(x+1, n+1):
					del ind.genome[x+1]


		if ind.genome[x].type == 'seq':

			if type(ind.genome[x+1]) is Action:

				# Remove selector subtree whose first child is an action and replace with the same action					
				finished = False
				treepos = []
				subtree = []

				# Add new counter for children
				treepos.append(ind.genome[x].size)
				subtree.append(ind.genome[x])
				n = (x-1) + 1 
				while finished != True:
					n += 1
					# End current operator if max children is reached.
					if treepos[len(treepos)-1] == 0:

						# Check if tree is completed and then end generation
						if treepos[0] == 0 and len(treepos) == 1:
							# Tree has been completed
							finished = True
						# Important! Reduce current tree position in order to move back up the tree
						del treepos[-1]
						n -= 1
					else:
						# Account for added child
						treepos[len(treepos)-1] = int(treepos[len(treepos)-1]) - 1
						if type(ind.genome[n]) is Operator:

							subtree.append(ind.genome[n])
							treepos.append(ind.genome[n].size)
						else:
							subtree.append(ind.genome[n])

				# insert replacement node
				ind.genome[x] = ind.genome[x+1]
				# Remove subtree from genome before crossover
				for z in range(x+1, n+1):
					del ind.genome[x+1]



	return ind

def hallfame(pop, hall, hallsize, file):

	hall = hall + pop
	hall.sort(key=lambda x: x.fitness, reverse=True)
	hall = [ind.copy() for ind in hall[0:hallsize]]

	# Save hall of fame object
	with open(file, 'wb') as output:
		pickle.dump(hall, output, pickle.HIGHEST_PROTOCOL)

	return hall

def save_gen(gens, file):
	# Save population
	with open(file, 'wb') as output:
		pickle.dump(gens, output, pickle.HIGHEST_PROTOCOL)


def tournament(pop, tournsize, offspring):
	sel = []
	newpop = []
	topfit = -9999; fit = 0; best = 0

	for n in range(0, offspring):
		# Reset best fittness and choice list!!!!
		topfit = -9999
		choice = list(range(0,len(pop)))
		for i in range(0, tournsize):
			# make a selection of the availible individuals in the choice list.
			sel = (random.randint(0,(len(choice)-1)))
			fit = pop[choice[sel]].fitness
			if fit > topfit:
				# Track individual with best fitness
				best = choice[sel]
				topfit = fit
			# remove selected indivudal from list.
			choice.remove(choice[sel])
		newpop.append(pop[best])

	return newpop

def log(pop, hall, logpop, logfit, logavg, logmax, g, filename):

	f = []; tot = 0; maxfit = 0

	file = open(filename, 'a+')
	file.write('\n\n\n GENERATION: %d' %g )
	file.write('\n ID: %s' % id(pop))
	for i in range(0, len(pop)):
		f.append(pop[i].fitness)
		tot += pop[i].fitness
		
		if pop[i].fitness > maxfit:
			maxfit = pop[i].fitness

		file.write('\n\nIndividual Fitness = %f' % pop[i].fitness)
		file.write('\n%s' % pop[i].tree)

	file.write('\n\nHALL OF FAME -----------------------------------------------------')
	for i in range(0, len(hall)):
		file.write('\n\nIndividual Fitness = %f' % hall[i].fitness)
		file.write('\n%s' % hall[i].tree)
	
	avg = tot/len(pop)
	logfit.append(f)
	logmax.append(maxfit)
	logavg.append(avg)
	logpop.append(pop)

	file.write('\n\nAverage Fitness: %s' % logavg)
	print('\n\nAverage Fitness: %s' % logavg)
	file.write('\n\nMaximum Fitness: %s' % logmax)
	print('\nMaximum Fitness: %s' % logmax)
	#file.write('\n\nPop Fitnesses: %s' % f)
	file.write('\n============================================================================================================================================')
	file.close()

def log_settings(swarm, popsize, indsize, tournsize, elitesize, mutrate ,ngen,targets,state, timesteps, filename):


	file = open(filename, 'w+')
	file.write('\nRun settings: --->')
	file.write('\n\nSwarm size: %d' % swarm.size)
	file.write('\n\nSwarm agent speed: %f' % swarm.speed)
	file.write('\n\nSwarm map: %s' % swarm.map)
	file.write('\nTarget setup: %s' % state)
	file.write('\nTarget detection radius: %d' % targets.radius)
	file.write('\n\nNumber of generations: %d' % ngen)
	file.write('\n\nTest length: %d' % timesteps)
	file.write('\nPopulation size: %d' % popsize)
	file.write('\nBehaviour tree initial depth: %d' % indsize)
	file.write('\nTournament size: %d' % tournsize)
	file.write('\nElite size: %d' % elitesize)
	file.write('\nMutation rate: %f' % mutrate)
	file.close()



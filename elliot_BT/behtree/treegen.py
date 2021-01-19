
'''
	Classes which define the types of nodes that are used to build trees.
	Also contains functions to generate and decode trees into executable trees with the py-trees library. 

'''
import random
import py_trees
import behtree.tree_nodes as tree_nodes

class Condition(object):

	def __init__(self):

		self.var = []
		self.value = []
		self.op = []
		self.type = []

	def generate(self):

		self.var = random.choice(['centerx', 'centery', 'density'])
		self.op = random.choice(['<','>'])
		if self.var == 'centerx' or self.var == 'centery':
			self.value = random.choice([-34,-32,-30,-28,-26,-24,-22,-20,-18,-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34])
		if self.var == 'density':
			self.value = random.choice([1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35])
		if self.var == 'coverage':
			self.value = random.choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
		return 'cond', self.var, self.op, self.value

	def copy(self):
		newcond = Condition()
		newcond.var = self.var[:]
		newcond.op = self.op[:]
		newcond.value = self.value
		return newcond

class Action(object):
	def __init__(self):
		self.type = []

	def generate(self):

		self.type = random.choice(['disperse','north','south','west','east','northwest','southwest','northeast','northwest'])
		return self.type

	def copy(self):
		newac = Action()
		newac.type = self.type[:]
		return newac

class Param(object):
	def __init__(self):
		self.type = []
		self.param = 0

	def generate(self):

		self.type = random.choice(['disperse','north','south','west','east','northwest','southwest','northeast','northwest'])

		if self.type == 'aggregate':
			self.param = random.choice([30,35,40,45,50,55,60,65,70,75,80])
		else:
			self.param = random.choice([1,5,10,15,20,25,30,35,40,45,50,55,60])
		return self.type

	def copy(self):
		newp = Param()
		newp.type = self.type[:]
		newp.param = self.param
		return newp

class Env_control(object):
	def __init__(self):
		self.type = []
		self.pos = [0, 0]

	def generate(self):

		self.type = random.choice(['attract', 'repel'])

		p = [-38,-36,-34,-32,-30,-28,-26,-24,-22,-20,-18,-16,-14,-12,-10,-8,-6,-4,-2,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38]
		self.pos[0] = random.choice(p)
		self.pos[1] = random.choice(p)
		return self.type

	def copy(self):
		newac = Env_control()
		newac.type = self.type[:]
		newac.pos[0] = self.pos[0]
		newac.pos[1] = self.pos[1]
		return newac 

class Operator(object):

	def __init__(self):
		self.type = []
		self.size = []

	def generate(self):
		self.type = 'seq'
		self.size = random.choice(['2','3','4','5','6','7'])

	def copy(self):
		newop = Operator()
		newop.type = self.type[:]
		newop.size = self.size
		return newop

class individual(object):

	def __init__ (self, genome):

		self.genome = genome
		self.tree = []
		self.fitness = []

	def copy(self):
		newind = individual([g.copy() for g in self.genome])
		#newind.genome = self.genome
		newind.tree=self.tree
		newind.fitness = self.fitness
		return newind


class tree(object):


	def ascii_tree(self, ind):

		length = len(ind.genome)
		n = 0
		parents = []
		treepos = []
		asci = ''
		finished = False
	
		while finished != True:
			if n == 0:
				asci += ind.genome[n].type
				asci += '('
				treepos.append(ind.genome[n].size)		
			else:
				# End current operator if max children is reached.
				if treepos[len(treepos)-1] == 0:
					if treepos[0] == 0 and len(treepos) == 1:
						# Tree has been completed
						finished = True
						asci += ')'
					else:
						# Important! Reduce current tree position in order to move back up the tree
						del treepos[-1]
						n -= 1
						asci += ')'
				else:
					treepos[len(treepos)-1] = int(treepos[len(treepos)-1]) - 1

					if type(ind.genome[n]) is Operator:
						asci += ind.genome[n].type
						asci += '('
						# Add new counter for children
						treepos.append(ind.genome[n].size)

					# Action nodes
					if type(ind.genome[n]) is Action:
						# Account for new child added to parent
						asci += ind.genome[n].type
						asci += ', '
					# Param nodes
					if type(ind.genome[n]) is Param:
						# Account for new child added to parent
						asci += ind.genome[n].type
						asci += ': '
						asci += str(ind.genome[n].param)
						asci += ', '

					if type(ind.genome[n]) is Env_control:
						# Account for new child added to parent
						asci += ind.genome[n].type
						asci += ': '
						asci += str(ind.genome[n].pos[0]) + ', ' + str(ind.genome[n].pos[1])
						asci += ', '
					# Condition nodes
					if type(ind.genome[n]) is Condition:
						# Account for new child added to parent
						asci += 'cond['
						asci += str(ind.genome[n].var)
						asci += str(ind.genome[n].op)
						asci += str(ind.genome[n].value)
						asci += ']'
						asci += ', '

			n += 1
		ind.tree = asci

	def make_tree(self, height):

		depth = 0
		tree = []
		treepos = []
		
		while depth <= height:
			# Select tree root
			if depth == 0:
				node = Operator()
				node.generate()
				tree.append(node)
				treepos.append(node.size)
				depth += 1

				# Make first node to execute some form of action. Not a condition!
				choice = random.choice(['act','param'])

				if choice == 'act': node = Action()
				if choice == 'param': node = Param()
				if choice == 'env': node = Env_control()
			
				node.generate()
				# account for added child
				treepos[len(treepos)-1] = int(treepos[len(treepos)-1]) - 1
				tree.append(node)
	
			# Choose next type of node to add to the tree
			if depth != height:
				choice = random.choice(['op', 'cond', 'action'])
			else:
				choice = random.choice(['action', 'cond'])

			# End current operator if max children is reached.
			if treepos[len(treepos)-1] == 0:
				# Check if tree is completed and then end generation
				if treepos[0] == 0 and len(treepos) == 1:
					# Tree has been completed
					depth = 999
				# Important! Reduce current tree position in order to move back up the tree
				del treepos[-1]
			else:
				treepos[len(treepos)-1] = int(treepos[len(treepos)-1]) - 1

				if choice == 'op':
					op = Operator()
					op.generate()
					treepos.append(op.size)
					tree.append(op)
					depth += 1

				if choice == 'cond':
					node = Condition()
					# account for added child
					node.generate()
					tree.append(node)

				if choice == 'action':
					choice = random.choice(['beh', 'param'])

					if choice == 'beh': node = Action()
					if choice == 'param': node = Param()
					if choice == 'env': node = Env_control()
					node.generate()
					tree.append(node)
		
		return tree

	def decode (self, ind, swarm, targets):
		
		length = len(ind.genome)
		tickspeed = 0.05
		n = 0
		parents = []
		treepos = []
		finished = False
		
		while finished != True:
		
			if n == 0:
				if ind.genome[n].type == 'sel':
					root = py_trees.composites.Selector("Selector")
				if ind.genome[n].type == 'seq':
					root = py_trees.composites.Sequence("Sequence")
				parent = root
				parents.append(parent)
				treepos.append(ind.genome[n].size)
			
			else:
				# End current operator if max children is reached.
				if treepos[len(treepos)-1] == 0:
					# print 'ending operatororororo'
					if treepos[0] == 0 and len(treepos) == 1:
						# Tree has been completed
						finished = True
					else:
						# Important! Reduce current tree position in order to move back up the tree
						del treepos[-1]
						del parents[-1]
						parent = parents[len(parents)-1]
						n -= 1
				# Operators
				else:
					treepos[len(treepos)-1] = int(treepos[len(treepos)-1]) - 1
					
					if type(ind.genome[n]) is Operator:

						if ind.genome[n].type == 'sel':
							op = py_trees.composites.Selector("Selector")
						if ind.genome[n].type == 'seq':
							op = py_trees.composites.Sequence("Sequence")
						# Add new counter for children
						parent.add_child(op)
						parent = op
						parents.append(parent)
						treepos.append(ind.genome[n].size)

					# Action nodes
					if type(ind.genome[n]) is Action:

						behaviour_node = tree_nodes.behaviour()
						behaviour_node.swarm = swarm
						behaviour_node.command = ind.genome[n].type
						behaviour_node.name = ind.genome[n].type
						behaviour_node.setup()
						parent.add_child(behaviour_node)
		
					# Param nodes
					if type(ind.genome[n]) is Param:
						
						param_node = tree_nodes.beh_param()
						param_node.swarm = swarm
						param_node.command = ind.genome[n].type
						param_node.param = ind.genome[n].param
						param_node.name = ind.genome[n].type + ': ' + str(ind.genome[n].param)
						param_node.setup()
						parent.add_child(param_node)

					if type(ind.genome[n]) is Env_control:
						
						env_node = tree_nodes.env_control()
						env_node.swarm = swarm
						env_node.beacon = ind.genome[n]
						env_node.name = ind.genome[n].type + ': ' + str(ind.genome[n].pos[0]) + ', ' + str(ind.genome[n].pos[1])
						env_node.setup()
						parent.add_child(env_node)

					# Condition nodes
					if type(ind.genome[n]) is Condition:
						# Account for new child added to parent
						if ind.genome[n].var == 'density':
							name = 'Dense'
							if ind.genome[n].op == '<':
								node = tree_nodes.LessDense()
							if ind.genome[n].op == '>':
								node = tree_nodes.GreaterDense()

						if ind.genome[n].var == 'centery':
							name = 'CenterY'
							if ind.genome[n].op == '<':
								node = tree_nodes.LessY()
							if ind.genome[n].op == '>':
								node = tree_nodes.GreaterY()
			
						if ind.genome[n].var == 'centerx':
							name = 'CenterX'
							if ind.genome[n].op == '<':
								node = tree_nodes.LessX()
							if ind.genome[n].op == '>':
								node = tree_nodes.GreaterX()

						if ind.genome[n].var == 'coverage':
							name = 'Coverage'
							if ind.genome[n].op == '>':
								node = tree_nodes.GreaterCov()
							if ind.genome[n].op == '<':
								node = tree_nodes.LessCov()
							node.targets = targets
						node.swarm = swarm
						node.const = ind.genome[n].value
						node.name = name +' '+ ind.genome[n].op + ' '+ str(node.const)
						node.setup()
						parent.add_child(node)

			n += 1

		# Instantiate Tree
		bt = py_trees.trees.BehaviourTree(root)
		bt.setup(15)
	
		return bt
#!/usr/bin/env python

import string
import numpy as np
import logging
import time
import random
import math

import simulation.environment as environment
import scipy
from numpy.linalg import norm
from scipy.spatial.distance import cdist, pdist, euclidean


###########################################################################################


class swarm(object):

	def __init__(self):

		self.agents = []
		self.speed = 0.5
		self.size = 0
		self.behaviour = 'none'
		self.centermass = [0,0]
		self.spread = 0
		self.velocity = 0
		self.param = 3
		self.map = 'none'
		self.beacon_att = np.array([[]])
		self.beacon_rep = np.array([[]])
		self.origin = np.array([0,0])
		self.noise = []

	def gen_agents(self):

		#self.agents = 0.0001*np.random.randint(-1., 1., (self.size,2)) + self.origin
		#self.agents = [np.array([[0,0]]) for x in range(self.size)]
		#self.agents = np.zeros((self.size, 2))
		if self.size == 10:
			self.agents = np.array([[0.0,0.0],[-0.11,0.0],[0.12,0.0],[0.13,0.11],[-0.12,0.15],[0.11,-0.15],[-0.11,-0.11],[0.12,0.24],[0.0,0.21],[-0.12,0.23]])
			self.noise = 0.00001*np.random.randint(-1., 1., (self.size,2))
		if self.size == 3:
			self.agents = np.array([[0,-20],[0.1,-20.2],[-0.1,-19.8]])
			self.noise = 0.0*np.random.randint(-1., 1., (self.size,2))

	def reset(self):

		self.behaviour = 'none'
		#self.agents = 0.0001*np.random.randint(-1., 1., (self.size,2)) + self.origin
		#self.agents = [np.array([[0, 0]]) for x in range(self.size)]
		if self.size == 10:
			self.agents = np.array([[0.0,0.0],[-0.11,0.0],[0.12,0.0],[0.13,0.11],[-0.12,0.15],[0.11,-0.15],[-0.11,-0.11],[0.12,0.24],[0.0,0.21],[-0.12,0.23]])
		if self.size == 3:
			self.agents = np.array([[0,-20],[0.1,-20.2],[-0.1,-19.8]])
		#self.agents = np.array([[0.0,0.0],[-0.1,0.0],[0.1,0.0],[0.1,0.1],[-0.1,0.1],[0.1,-0.1],[-0.1,-0.1],[0.1,0.2],[0.0,0.2],[-0.1,0.2]])
		#self.agents = np.zeros((self.size, 2))

	def iterate(self):
		global env
		if self.behaviour == 'aggregate':
			aggregate(self, self.param)
		if self.behaviour == 'disperse':
			dispersion(self, np.array([0,0]), self.param)
		if self.behaviour == 'north':
			dispersion(self, np.array([0,1]), self.param)
		if self.behaviour == 'south':
			dispersion(self, np.array([0,-1]), self.param)
		if self.behaviour == 'west':
			dispersion(self, np.array([-1,0]), self.param)
		if self.behaviour == 'east':
			dispersion(self, np.array([1,0]), self.param)
		if self.behaviour == 'northwest':
			dispersion(self, np.array([-1,1]), self.param)
		if self.behaviour == 'northeast':
			dispersion(self, np.array([1,1]), self.param)
		if self.behaviour == 'southwest':
			dispersion(self, np.array([-1,-1]), self.param)
		if self.behaviour == 'southeast':
			dispersion(self, np.array([1,-1]), self.param)


	def get_state(self):

		totx = 0; toty = 0; totmag = 0

		# Calculate connectivity matrix between agents
		mag = cdist(self.agents, self.agents)
		totmag = np.sum(mag)
		totpos = np.sum(self.agents, axis=0)

		# calculate density and center of mass of the swarm
		self.spread = totmag/((self.size -1)*self.size)
		self.centermass[0] = (totpos[0])/(self.size)
		self.centermass[1] = (totpos[1])/(self.size)

	def copy(self):
		newswarm = swarm()
		newswarm.agents = self.agents[:]
		newswarm.speed = self.speed
		newswarm.size = self.size
		newswarm.behaviour = self.behaviour = 'none'
		newswarm.map = self.map
		#newswarm.beacon_set = self.beacon_set
		return newswarm



class target_set(object):

	def __init__(self):
		self.targets = []
		self.radius = 0
		self.found = 0
		self.coverage = 0
		self.old_state = np.zeros(len(self.targets))

	def set_state(self, state):


		if state == 'set1':
			self.targets = np.array([[-35,35],[-25,35],[-15,35],[-5,35],[5,35],[15,35],[25,35],[35,35],
							[-35,25],[-15,25],[-5,25],[5,25],[15,25],[25,25],[35,25],
							[-35,15],[-15,15],[-5,15],[5,15],[15,15],[25,15],[35,15],
							[-35,5],[-15,5],[15,5],[25,5],[35,5],
							[-35,-5],[-25,-5],[-15,-5],[15,-5],[25,-5],[35,-5],
							[-35,-15],[-25,-15],[-15,-15],[-5,-15],[5,-15],[15,-15],[25,-15],[35,-15],
							[-35,-25],[-25,-25],[-15,-25],[-5,-25],[5,-25],[15,-25],[25,-25],[35,-25],
							[-35,-35],[-25,-35],[-15,-35],[-5,-35],[5,-35],[15,-35],[25,-35],[35,-35]])


		# if state == 'exercise1a':
		# 	self.targets = np.array([[0,-15],[0,-10],[0,-5],[0,0],[0,5],[5,5],[10,5],[15,5],[20,5],[20,10],[20,15],[20,20],[20,25]])

		if state == 'exercise1':
			self.targets = np.array([[0,-15],[0,-10],[0,-5],[0,0],[0,5],[5,5],[10,5],[15,5],[20,5],[20,10],[20,15],[20,20],[20,25],
										[-5,5],[-10,5],[-15,5],[-20,5],[-20,10],[-20,15],[-20,20],[-20,25]])

		if state == 'exercise2':
			self.targets = np.array([[0,-20],[0,-25],[0,-15],[0,-10],[0,-5],[0,0],[0,5],[0,10],[0,15],[0,20],[0,25],[-5,25],[-5,30],[-5,35],
									  [5,25],[5,30],[5,35],[0,30],[0,35]])

		if state == 'exercise3':
			self.targets = np.array([[-15,-15],[-10,-15],[-5,-15],[0,-15],[5,-15],[10,-15],[15,-15],
										[-15,-10],[0,-10],[15,-10],
										[-15,-5],[0,-5],[15,-5],
										[-15,0],[-10,0],[-5,0],[0,0],[5,0],[10,0],[15,0],
										[-15,5],[0,5],[15,5],
										[-15,10],[0,10],[15,10],
										[-15,15],[-10,15],[-5,15],[0,15],[5,15],[10,15],[15,15]])

	def get_state(self, swarm, t):

		score = 0
		# adjacency matrix of agents and targets
		mag = cdist(swarm.agents, self.targets)

		# Check which distances are less than detection range
		a = mag < self.radius
		# Sum over agent axis 
		detected = np.sum(a, axis = 0)
		# convert to boolean, targets with 0 detections set to false.
		detected = detected > 0
		# Check detection against previous state
		updated = np.logical_or(detected, self.old_state) 
		self.old_state = updated
		score = np.sum(updated)
		self.coverage = score/len(self.targets)	

		return score

	def ad_state(self, swarm, t):

		score = 0
		# adjacency matrix of agents and targets
		mag = cdist(swarm.agents, self.targets)

		# Check which distances are less than detection range
		a = mag < self.radius
		# Sum over agent axis 
		detected = np.sum(a, axis = 0)
		# convert to boolean, targets with 0 detections set to false.
		detected = detected > 0
		# Check detection against previous state
		# check which new targets were found
		new =  np.logical_and(np.logical_xor(detected, self.old_state), detected) 

		updated = np.logical_or(detected, self.old_state) 
		self.old_state = updated
		score = np.sum(new)
		self.coverage = np.sum(updated)/len(self.targets)	

		return score

	def reset(self):
		self.old_state = np.zeros(len(self.targets))

class map(object):

	def __init__(self):

		self.obsticles = []
		self.force = 0
		self.walls = np.array([])
		self.wallh = np.array([])
		self.wallv = np.array([])
		self.planeh = np.array([])
		self.planev = np.array([])

	def gen(self):

		# Perform pre-processing on map object for efficency
		self.walls = np.zeros((2*len(self.obsticles), 2))
		self.wallh = np.zeros((2*len(self.obsticles), 2))
		self.wallv = np.zeros((2*len(self.obsticles), 2))
		self.planeh = np.zeros(len(self.obsticles))
		self.planev = np.zeros(len(self.obsticles))
		self.limh = np.zeros((len(self.obsticles), 2))
		self.limv = np.zeros((len(self.obsticles), 2))

		for n in range(0, len(self.obsticles)):
			# if wall is vertical
			if self.obsticles[n].start[0] == self.obsticles[n].end[0]:
				self.wallv[2*n] = np.array([self.obsticles[n].start[0], self.obsticles[n].start[1]])
				self.wallv[2*n+1] = np.array([self.obsticles[n].end[0], self.obsticles[n].end[1]])

				self.planev[n] = self.wallv[2*n][0]
				self.limv[n] = np.array([np.min([self.obsticles[n].start[1], self.obsticles[n].end[1]])-0.5, np.max([self.obsticles[n].start[1], self.obsticles[n].end[1]])+0.5])

			# if wall is horizontal
			if self.obsticles[n].start[1] == self.obsticles[n].end[1]:
				self.wallh[2*n] = np.array([self.obsticles[n].start[0], self.obsticles[n].start[1]])
				self.wallh[2*n+1] = np.array([self.obsticles[n].end[0], self.obsticles[n].end[1]])

				self.planeh[n] = self.wallh[2*n][1]
				self.limh[n] = np.array([np.min([self.obsticles[n].start[0], self.obsticles[n].end[0]])-0.5, np.max([self.obsticles[n].start[0], self.obsticles[n].end[0]])+0.5])

			self.walls[2*n] = np.array([self.obsticles[n].start[0], self.obsticles[n].start[1]])
			self.walls[2*n+1] = np.array([self.obsticles[n].end[0], self.obsticles[n].end[1]])


	def exercise1(self):

		box = environment.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		# Bottom corridor
		wall = environment.wall(); wall.start = [-5,-25]; wall.end = [5,-25];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [-5,0]; wall.end = [-5,-25];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [5,0]; wall.end = [5,-25];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [-25,0]; wall.end = [-5,0];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [5,0]; wall.end = [25,0];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [-25,0]; wall.end = [-25,30];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [25,0]; wall.end = [25,30];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [-25,30]; wall.end = [-15,30];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [25,30]; wall.end = [15,30];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [15,30]; wall.end = [15,10];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [-15,30]; wall.end = [-15,10];
		self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [-15,10]; wall.end = [15,10];
		self.obsticles.append(wall)

	def exercise3(self):
		box = environment.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		box = environment.box(40, 40, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		box = environment.box(7, 7, [7, 7]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		
		box = environment.box(7, 7, [-7,7]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		box = environment.box(7, 7, [7,-7]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		box = environment.box(7, 7, [-7,-7]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		




	def map1(self):

		# Bounding Walls ---------------------------------
		box = environment.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		room = environment.room(20, 20, 10, 'top', [0, 0]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		room = environment.room(20, 20, 7, 'bottom', [0, 30]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		room = environment.room(20, 30, 10, 'bottom', [25, 30]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		#doorway = environment.doorway(30, 7, 'horizontal', [25, 10]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = environment.wall(); wall.start = [10,10]; wall.end = [40,10];
		self.obsticles.append(wall)

		box = environment.box(3, 3, [20, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		box = environment.box(3, 3, [30, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		box = environment.box(3, 3, [20, -10]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		box = environment.box(3, 3, [30, -10]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		doorway = environment.doorway(30, 7, 'horizontal', [25, -20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = environment.doorway(30, 7, 'vertical', [10, -25]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		doorway = environment.doorway(30, 7, 'horizontal', [-25, -10]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		room = environment.room(30, 10, 7, 'right', [-35, -25]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		box = environment.box(15, 3, [-2, -25]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		box = environment.box(15, 3, [-18, -25]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		box = environment.box(30, 5, [-25, 15]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		#corridor = environment.corridor(30, 5, 'horizontal', [30,-10]); [self.obsticles.append(corridor.walls[x]) for x in range(0, len(corridor.walls))]

	def map2(self):


		# Bounding Walls ---------------------------------
		box = environment.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		room = environment.room(20, 20, 10, 'top', [0, 0]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		doorway = environment.doorway(20, 7, 'vertical', [20, 30]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = environment.doorway(20, 7, 'horizontal', [30, 20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		doorway = environment.doorway(30, 10, 'vertical', [10, 25]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = environment.doorway(30, 10, 'horizontal', [25, 10]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = environment.wall(); wall.start = [-10,40]; wall.end = [-10,10]; self.obsticles.append(wall)

		doorway = environment.doorway(30, 7, 'horizontal', [25, -20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = environment.wall(); wall.start = [-10,-20]; wall.end = [10,-20]; self.obsticles.append(wall)
		wall = environment.wall(); wall.start = [-10,-20]; wall.end = [-10,-40]; self.obsticles.append(wall)

		room = environment.room(20, 20, 7, 'top', [-30, -30]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]
		room = environment.room(20, 20, 7, 'bottom', [-30, 0]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		doorway = environment.doorway(30, 7, 'vertical', [-20, 25]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		box = environment.box(7, 15, [25, -5]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		#box = environment.box(15, 7, [30, 30]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

	def map3(self):
		
		# Bounding Walls ---------------------------------
		box = environment.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		wall = environment.wall(); wall.start = [-10,-10]; wall.end = [10,-10]; self.obsticles.append(wall)

		doorway = environment.doorway(20, 7, 'horizontal', [0, 10]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = environment.doorway(20, 7, 'vertical', [10, 0]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = environment.doorway(20, 7, 'vertical', [-10, 0]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		doorway = environment.doorway(40, 10, 'horizontal', [0, 20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		#doorway = environment.doorway(40, 10, 'horizontal', [0, -20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = environment.wall(); wall.start = [-20, -20]; wall.end = [20,-20]; self.obsticles.append(wall)

		doorway = environment.doorway(30, 10, 'vertical', [-20, -5]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = environment.wall(); wall.start = [-40, 10]; wall.end = [-20,10]; self.obsticles.append(wall)

		wall = environment.wall(); wall.start = [20, 30]; wall.end = [20,-20]; self.obsticles.append(wall)

		wall = environment.wall(); wall.start = [20, -20]; wall.end = [40,-20]; self.obsticles.append(wall)

		wall = environment.wall(); wall.start = [-20, 40]; wall.end = [-20,20]; self.obsticles.append(wall)

		doorway = environment.doorway(10, 7, 'vertical', [-20, 15]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		room = environment.room(10, 30, 7, 'top', [-25, -35]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		room = environment.room(10, 30, 7, 'top', [25, -35]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]


	def ex1(self):
		
		# Bounding Walls ---------------------------------
		box = environment.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		wall = environment.wall(); wall.start = [-20, -20]; wall.end = [30,-20]; self.obsticles.append(wall)

		wall = environment.wall(); wall.start = [-20, -20]; wall.end = [-20,20]; self.obsticles.append(wall)



	def empty(self):
		
		# Bounding Walls ---------------------------------
		box = environment.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]






def avoidance(agents, map):

	size = len(agents)
	# Compute vectors between agents and wall planes
	diffh = np.array([map.planeh-agents[n][1] for n in range(size)])
	diffv = np.array([map.planev-agents[n][0] for n in range(size)])
		
	# Check intersection of agents with walls
	# split agent positions into x and y arrays
	agentsx = agents.T[0]
	agentsy = agents.T[1]

	low = agentsx[:, np.newaxis] >= map.limh.T[0]
	up = agentsx[:, np.newaxis] <= map.limh.T[1]
	intmat = up*low

	# Compute force based vector and multiply by intersection matrix
	Fy = np.exp(-2*abs(diffh) + 5)
	Fy = Fy*diffh*intmat

	low = agentsy[:, np.newaxis] >= map.limv.T[0]
	up = agentsy[:, np.newaxis] <= map.limv.T[1]
	intmat = up*low

	Fx = np.exp(-2*abs(diffv) + 5)
	Fx = Fx*diffv*intmat

	# Sum the forces between every wall into one force.
	Fx = np.sum(Fx, axis=1)
	Fy = np.sum(Fy, axis=1)
	# Combine x and y force vectors
	F = np.array([[Fx[n], Fy[n]] for n in range(size)])
	return F

	

def dispersion(swarm, vector, param):

	R = param; r = 2; A = 1; a = 20
	W = np.zeros((swarm.size, 2))
	B = np.zeros((swarm.size, 2))

	#noise = [[np.random.uniform(-0.5,0.5), np.random.uniform(-0.5,0.5)] for x in range(swarm.size)]
	# noise = 0.1*np.random.randint(-1., 1., (swarm.size,2))

	# Compute euclidean distance between agents
	mag = cdist(swarm.agents, swarm.agents)

	# Compute vectors between agents
	diff = swarm.agents[:,:,np.newaxis]-swarm.agents.T[np.newaxis,:,:] 

	A = avoidance(swarm.agents, swarm.map)
	a = R*r*np.exp(-mag/r)[:,np.newaxis,:]*diff/(swarm.size-1)	
	a = np.sum(a, axis =0).T
	a += A + B +swarm.noise - vector

	vecx = a.T[0]
	vecy = a.T[1]

	angles = np.arctan2(vecy, vecx)
	Wx = swarm.speed*np.cos(angles)
	Wy = swarm.speed*np.sin(angles)

	W = -np.array([[Wx[n], Wy[n]] for n in range(0, swarm.size)])
	swarm.agents += W 

	
def aggregate(swarm, param):
	pass















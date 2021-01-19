#!/usr/bin/env python


# This is a multi-agent simulator

from matplotlib import pyplot as plt
from matplotlib import gridspec
from matplotlib import colors as cls
from matplotlib import cm
from matplotlib import animation
import matplotlib.image as mpimg
import string
import numpy as np
import logging
import subprocess
import time
import random
import math

import map_gen
import scipy

import time

###########################################################################################


class agent(object):

	def __init__(self):
		lim = 3
		self.location = [random.randint(-lim,lim),random.randint(-lim,lim)]
		self.detect_range = 5

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
		self.beacon_set = []

	def reset(self):

		lim = 3
		self.behaviour = 'none'
		for n in range(self.size):
			self.agents[n].location = [random.randint(-lim,lim),random.randint(-lim,lim)]

	def iterate(self):
		global env
		if self.behaviour == 'waypoint':
			[waypoint(self.agents[n], swarm) for n in range(swarm.size)]
		if self.behaviour == 'aggregate':
			aggregate(self, self.param)
		if self.behaviour == 'disperse':
			dispersion(self, [0,0], self.param)
		if self.behaviour == 'north':
			dispersion(self, [0,1], self.param)
		if self.behaviour == 'south':
			dispersion(self, [0,-1], self.param)
		if self.behaviour == 'west':
			dispersion(self, [-1,0], self.param)
		if self.behaviour == 'east':
			dispersion(self, [1,0], self.param)
		if self.behaviour == 'northwest':
			dispersion(self, [-1,1], self.param)
		if self.behaviour == 'northeast':
			dispersion(self, [1,1], self.param)
		if self.behaviour == 'southwest':
			dispersion(self, [-1,-1], self.param)
		if self.behaviour == 'southeast':
			dispersion(self, [1,-1], self.param)
		if self.behaviour == 'avoidance':
			avoidance(self, env)

	def get_state(self):

		totx = 0; toty = 0
		totmag = 0

		now = time.time()
		
		for n in range (0,self.size):

			totx += self.agents[n].location[0]
			toty += self.agents[n].location[1]

			for i in range (0,self.size):
				
				if n != i:
					# calculate distance between agents
					distx = (self.agents[n].location[0] - self.agents[i].location[0])
					disty = (self.agents[n].location[1] - self.agents[i].location[1])

					mag = pow(pow(distx,2) + pow(disty,2),0.5)
					totmag += mag

		# calculate density and center of mass of the swarm
		self.spread = totmag/((self.size -1)*self.size)
		
		self.centermass[0] = (totx)/(self.size)
		self.centermass[1] = (toty)/(self.size)

		addnoise = False
		if addnoise == True:
			self.spread += random.uniform(-1,1)
			self.centermass[0] += random.uniform(-1,1)
			self.centermass[1] += random.uniform(-1,1)

		print("get state: "+str(1000*(time.time()-now))+"ms")



class environment(object):


	def __init__(self):

		self.obsticles = []
		self.force = 0

	def map1(self):

		# Bounding Walls ---------------------------------
		box = map_gen.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		room = map_gen.room(20, 20, 10, 'top', [0, 0]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		room = map_gen.room(20, 20, 7, 'bottom', [0, 30]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		room = map_gen.room(20, 30, 10, 'bottom', [25, 30]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		#doorway = map_gen.doorway(30, 7, 'horizontal', [25, 10]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = map_gen.wall(); wall.start = [10,10]; wall.end = [40,10];
		self.obsticles.append(wall)

		box = map_gen.box(3, 3, [20, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		box = map_gen.box(3, 3, [30, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		box = map_gen.box(3, 3, [20, -10]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		box = map_gen.box(3, 3, [30, -10]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		doorway = map_gen.doorway(30, 7, 'horizontal', [25, -20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = map_gen.doorway(30, 7, 'vertical', [10, -25]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		doorway = map_gen.doorway(30, 7, 'horizontal', [-25, -10]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		room = map_gen.room(30, 10, 7, 'right', [-35, -25]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		box = map_gen.box(15, 3, [-2, -25]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		box = map_gen.box(15, 3, [-18, -25]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		box = map_gen.box(30, 5, [-25, 15]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		#corridor = map_gen.corridor(30, 5, 'horizontal', [30,-10]); [self.obsticles.append(corridor.walls[x]) for x in range(0, len(corridor.walls))]

	def map2(self):


		# Bounding Walls ---------------------------------
		box = map_gen.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		room = map_gen.room(20, 20, 10, 'top', [0, 0]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		doorway = map_gen.doorway(20, 7, 'vertical', [20, 30]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = map_gen.doorway(20, 7, 'horizontal', [30, 20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		doorway = map_gen.doorway(30, 10, 'vertical', [10, 25]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = map_gen.doorway(30, 10, 'horizontal', [25, 10]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = map_gen.wall(); wall.start = [-10,40]; wall.end = [-10,10]; self.obsticles.append(wall)

		doorway = map_gen.doorway(30, 7, 'horizontal', [25, -20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = map_gen.wall(); wall.start = [-10,-20]; wall.end = [10,-20]; self.obsticles.append(wall)
		wall = map_gen.wall(); wall.start = [-10,-20]; wall.end = [-10,-40]; self.obsticles.append(wall)

		room = map_gen.room(20, 20, 7, 'top', [-30, -30]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]
		room = map_gen.room(20, 20, 7, 'bottom', [-30, 0]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		doorway = map_gen.doorway(30, 7, 'vertical', [-20, 25]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		box = map_gen.box(7, 15, [25, -5]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]
		#box = map_gen.box(15, 7, [30, 30]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

	

	def map3(self):
		
		# Bounding Walls ---------------------------------
		box = map_gen.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]

		wall = map_gen.wall(); wall.start = [-10,-10]; wall.end = [10,-10]; self.obsticles.append(wall)

		doorway = map_gen.doorway(20, 7, 'horizontal', [0, 10]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = map_gen.doorway(20, 7, 'vertical', [10, 0]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		doorway = map_gen.doorway(20, 7, 'vertical', [-10, 0]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		doorway = map_gen.doorway(40, 10, 'horizontal', [0, 20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]
		#doorway = map_gen.doorway(40, 10, 'horizontal', [0, -20]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = map_gen.wall(); wall.start = [-20, -20]; wall.end = [20,-20]; self.obsticles.append(wall)

		doorway = map_gen.doorway(30, 10, 'vertical', [-20, -5]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		wall = map_gen.wall(); wall.start = [-40, 10]; wall.end = [-20,10]; self.obsticles.append(wall)

		wall = map_gen.wall(); wall.start = [20, 30]; wall.end = [20,-20]; self.obsticles.append(wall)

		wall = map_gen.wall(); wall.start = [20, -20]; wall.end = [40,-20]; self.obsticles.append(wall)

		wall = map_gen.wall(); wall.start = [-20, 40]; wall.end = [-20,20]; self.obsticles.append(wall)

		doorway = map_gen.doorway(10, 7, 'vertical', [-20, 15]); [self.obsticles.append(doorway.walls[x]) for x in range(0, len(doorway.walls))]

		room = map_gen.room(10, 30, 7, 'top', [-25, -35]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

		room = map_gen.room(10, 30, 7, 'top', [25, -35]); [self.obsticles.append(room.walls[x]) for x in range(0, len(room.walls))]

	def empty(self):
		
		# Bounding Walls ---------------------------------
		box = map_gen.box(80, 80, [0, 0]); [self.obsticles.append(box.walls[x]) for x in range(0, len(box.walls))]


		


class beacon(object):

	def __init__(self):
		
		self.type = ''
		self.force = 10
		self.life = 0



def avoidance(agent, map):

	Fx = 0; Fy = 0

	# Loop through all obsitcles in the map
	for a in range(0, len(map.obsticles)):

		# Check if obsticle is within detection range
		if map.obsticles[a].start[0] == map.obsticles[a].end[0]:
			if agent.location[1] <= map.obsticles[a].start[1]+0.5 and agent.location[1] >= map.obsticles[a].end[1]-0.5:

				# calculate distance to wall
				dist = map.obsticles[a].start[0] - agent.location[0]
				#print('dist  ', dist)
				if abs(dist) <= agent.detect_range:

					Fx += -3/dist*math.exp(-abs(dist) + 3)
					#print('force:  ', Fx)

		# Check if obsticle is within detection range
		if map.obsticles[a].start[1] == map.obsticles[a].end[1]:
			if agent.location[0] <= map.obsticles[a].end[0] +0.5 and agent.location[0] >= map.obsticles[a].start[0]-0.5:

				# calculate distance to wall
				dist = map.obsticles[a].start[1] - agent.location[1]
				#print('dist  ', dist)
				if abs(dist) <= agent.detect_range:

					#Fy += -math.exp(-abs(dist) - 3)/dist
					Fy += -3/dist*math.exp(-abs(dist) + 3)
					#print('force:  ', Fx)

	return [Fx,Fy]
	

def dispersion(swarm, vector, param):
        
	R = param
	r = 2
	A = 1
	a = 20
	W = [0]*2
	Threshold = 4
    
	now = time.time()

	for n in range(0, len(swarm.agents)):
		# Add random walk with field vector
		Fx = random.uniform(-1,1) + vector[0]; Fy = random.uniform(-1,1) + vector[1]

		for i in range (0, len(swarm.agents)):
			if i != n:
				# Find distance to other agents
				xc = swarm.agents[i].location[0] - swarm.agents[n].location[0]
				yc = swarm.agents[i].location[1] - swarm.agents[n].location[1]
				mag = pow(pow(xc, 2) + pow(yc, 2), 0.5)

				# Generate repulsion force
				G = R*r*math.exp(-mag/r)
				xc = G*xc
				yc = G*yc
				W[0] += xc
				W[1] += yc

		W[0] = W[0]/(swarm.size-1)
		W[1] = W[1]/(swarm.size-1)

		t = time.time()
		F = avoidance(swarm.agents[n], swarm.map)
		atime = time.time()-t
		
		Fx += F[0]
		Fy += F[1]

		if len(swarm.beacon_set) != 0:
			E = beacon(swarm.beacon_set, swarm.agents[n])
			Fx += E[0]
			Fy += E[1]


		# Calculate resultant vector to follow
		Fx -= W[0]
		Fy -= W[1]
		RF = pow( pow(Fx, 2) + pow(Fy, 2) , 0.5 )
		RFangle = math.degrees(math.atan2(Fy, Fx))

		swarm.agents[n].location[0] += swarm.speed*math.cos(math.radians(RFangle))
		swarm.agents[n].location[1] += swarm.speed*math.sin(math.radians(RFangle))

	print("Loop time dispersion: "+str(1000*(time.time()-now)-1000*atime*swarm.size)+"ms")
	print("Loop time avoidance: "+str(1000*(atime*swarm.size))+"ms")
	#now = time.time()







def aggregate(swarm, param):
	
	R = param
	r = 3.5
	A = 6.5
	a = 7.5
	g = 20
	W = [0]*2
	
	#global env

	for n in range(0, len(swarm.agents)):
		
		Fx = 0; Fy = 0

		for i in range (0, len(swarm.agents)):
			if i != n:

				# Find distance to other agents
				xc = swarm.agents[i].location[0] - swarm.agents[n].location[0]
				yc = swarm.agents[i].location[1] - swarm.agents[n].location[1]

				mag = pow( pow(xc, 2) + pow(yc, 2) , 0.5 )
				G = -R*r*math.exp(-mag/r) + A*a*math.exp(-mag/a)
				#G = a - b*math.exp(-pow(mag, 2)/c)
				xc = G*xc
				yc = G*yc
				W[0] += xc
				W[1] += yc


		W[0] = W[0]/(swarm.size-1)
		W[1] = W[1]/(swarm.size-1)

		# Determine repulsion from obstacle
		F = avoidance(swarm.agents[n], swarm.map)
		Fx += F[0]
		Fy += F[1]

		if len(swarm.beacon_set) != 0:
			E = beacon(swarm.beacon_set, swarm.agents[n])
			Fx += E[0]
			Fy += E[1]

		# Calculate resultant vector to follow
		Fx += W[0]
		Fy += W[1]
		RF = pow( pow(Fx, 2) + pow(Fy, 2) , 0.5 )
		RFangle = math.degrees(math.atan2(Fy, Fx))

		swarm.agents[n].location[0] += swarm.speed*math.cos(math.radians(RFangle))
		swarm.agents[n].location[1] += swarm.speed*math.sin(math.radians(RFangle))

def beacon(beacon_set, agent):

	Fx = 0; Fy = 0
	#print(beacon_set)

	for n in range(0, len(beacon_set)):
	
		xc = agent.location[0] - beacon_set[n].pos[0]
		yc = agent.location[1] - beacon_set[n].pos[1]
		mag = pow(pow(xc, 2) + pow(yc, 2), 0.5)

		# print(beacon_set[n].type)
		# print(n)

		if beacon_set[n].type == 'attract':

			R = 1
			r = 3.5
			A = 1
			a = 2

			G = -A*a*math.exp(-mag/a)
			xc = G*xc
			yc = G*yc
			Fx += xc
			Fy += yc

		if beacon_set[n].type == 'repel':

			R = 5
			r = 2
			A = 1
			a = 20

			G = R*r*math.exp(-mag/r)
			xc = G*xc
			yc = G*yc
			Fx += xc
			Fy += yc

	return [Fx,Fy]








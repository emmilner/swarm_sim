'''
Swarm Warehouse with Boxes Code:
Displays a bird's eye view of a warehouse with robots moving around, avoiding the walls and each other. Boxes are picked up and moved to exit zone by robots. 

** Requires the script warehouse.py to be in the same folder as this script as it is called in the code **

Code authored by Emma Milner and Elliot Hogg

The actual specification for the Toshiba robots is as follows: 
agent speed = 2 m/s
agent acceleration 2 m/s/s
diameter of agent is 250 mm
width of testbed is 5m
height (depth) of warehouse is 5m 
'''

import numpy as np 
import math 
import random 
from matplotlib import pyplot as plt
from matplotlib import animation  
import scipy
from scipy.spatial.distance import cdist, pdist, euclidean
import pickle
import warehouse
import sys
import os

### INPUTS ###
radius = 12.5 # Radius of single agent (half of 25)
width = 500 # Width of warehouse (100)
height = 500 # Height (depth) of warehouse (100)
speed = 2 # Agent speed (0.5)
repulsion_distance = radius/2 # Distance at which repulsion is first felt (3)

box_radius = radius # radius of the box is the same as the robots
box_range = 2*box_radius # range at which a box can be picked up 
exit_width = int(0.2*width) # if it is too small then it will avoid the wall and be less likely to reach the exit zone 
###
R_rob = 15 # repulsion 'forces'/influence factors for robots-robots
R_box = 15 # repulsion 'forces'/influence factors for robots-boxes
R_wall = 25 # repulsion 'forces'/influence factors for robots-walls
stuck_limit = 1 #boxes

pick_up_prob = 100 # 100% likely to pick up a box it comes across if it is free 
marker_size = width*0.5/20 #diameter


class boxes():
	def __init__(self,number_of_boxes,robots):
		self.num_boxes = number_of_boxes 
		self.radius = box_radius # physical radius of the box (approximated to a circle even though square in animation)
		self.check_b = np.ones(self.num_boxes) # Box states set to 1 = Free (not on a robots), if = 0 = Not free (on a robot)
		self.delivered = 0 # Number of boxes that have been delivered 
		self.box_c = np.random.randint(box_radius*2,width-box_radius-exit_width,(self.num_boxes,2)) # box_c is the centre coordinate of the box which starts at a random position within the warehouse
		self.box_d = np.zeros((self.num_boxes,2)) # box centre coordinate deviation (how far the box moves in one time step)
		self.gone = np.ones(self.num_boxes) # set box state 'gone' as 1 meaning NOT DELIVERED ie gone from warehouse (0 is delivered)
		self.robot_carrier = np.full((self.num_boxes),-1) # Value at index = box number is the robot number that is currently moving that box
		self.beyond_b = np.zeros(self.num_boxes) # Boolean list of boxes that are over the delivery boundary (1 is in the delivery area)
		self.ask_mesh = np.zeros(self.num_boxes) # Boolean list of boxes that are over the delivery boundary (1 is in the delivery area)
		self.box_n = -1 

class swarm():
	def __init__(self,num_agents):
		self.speed = speed # Agent speed 
		self.num_agents = num_agents # Swarm size
		self.check_r = np.ones(self.num_agents) # Robot states set to 1 = Free (no box), if = 0 = Not free (has a box)
		self.heading = 0.0314*np.random.randint(-100,100,self.num_agents) # initial heading for all robots is randomly chosen
		self.rob_c = np.random.randint(box_radius*2,width-box_radius-exit_width,(self.num_agents,2)) # rob_c is the centre coordinate of the agent which starts at a random position within the warehouse 
		self.counter = 0 # time starts at 0s or time step = 0 
		self.rob_d = np.zeros((self.num_agents,2)) # robot centre cooridinate deviation (how much the robot moves in one time step)
		self.beyond_r = np.zeros(self.num_agents) # Boolean list of robots that are over the delivery boundary (1 is in the delivery area)
		self.heading_x = 0 
		self.heading_y = 0 
		self.rob_n = np.full(self.num_agents,-1) 
		self.beyond_r = 0 
		self.limit_in_delivery = self.num_agents/4
		
		self.state = np.zeros(self.num_agents)
		self.state_0 = np.zeros((self.num_agents,2))
		self.state_1 = np.zeros((self.num_agents,2))
		self.state_2 = np.zeros((self.num_agents,2))
		self.state_3 = np.zeros((self.num_agents,2))
		self.state_41 = np.zeros((self.num_agents,2))
		self.state_42 = np.zeros((self.num_agents,2))
		self.state_43 = np.zeros((self.num_agents,2))
		self.new_st_12 = False #reset 
		self.new_st_23 = False #reset
		self.new_st_31 = False #reset
		self.num_1 = (self.state==1).sum()
		self.num_2 = (self.state==2).sum()
		self.num_3 = (self.state==3).sum()
		self.count = [self.num_1,self.num_2,self.num_3]
		self.have_a_box = np.argwhere(self.check_r==0) 
		self.st_0 = np.argwhere(self.state==0) 
		self.st_5 = np.argwhere(self.state==5) 
		self.st_50 = np.append(self.st_0,self.st_5) 
		self.box_and_0 = np.intersect1d(self.st_50,self.have_a_box) 
		self.random_states = np.random.randint(1,3,np.size(self.box_and_0)) 
		self.r = np.argwhere(self.random_states==1)
		self.random_states[self.r] = 2
		self.total = (self.rob_c.T[0]>width-exit_width-50).sum() 
		self.dist = cdist(self.rob_c,self.rob_c)
		self.qu_close_box = np.min(self.dist,1) < box_range
		self.mins = np.argmin(self.dist,1)	
		self.checkb = self.check_r*self.qu_close_box
		self.box_b = np.argwhere(self.checkb==1)
		self.st0 = np.argwhere(self.state==0).flatten()
		self.st1 = np.argwhere(self.state==1).flatten()
		self.st2 = np.argwhere(self.state==2).flatten()
		self.st3 = np.argwhere(self.state==3).flatten()
		self.st41 = np.argwhere(self.state==4.1).flatten()
		self.st42 = np.argwhere(self.state==4.2).flatten()
		self.st43 = np.argwhere(self.state==4.3).flatten()
		self.st5 = np.argwhere(self.state==5).flatten()
		self.stuck = np.zeros(self.num_agents)
			
	def iterate(self,boxes): # moves the robot and box positions forward in one time step
		self.dist = cdist(boxes.box_c, self.rob_c) # calculates the euclidean distance from every robot to every box (centres)
		self.stuck_not = np.argwhere(boxes.check_b==0)
		self.dist[self.stuck_not] = 1000
		self.stuck = np.count_nonzero(self.dist<3*box_range,axis=0)		
		self.qu_close_box = np.min(self.dist,1) < box_range # if the minimum distance box-robot is less than the pick up sensory range, then qu_close_box = 1
		#qu_close_rob = np.min(dist,0) < box_range
		self.mins = np.argmin(self.dist,1)	
		self.checkb = boxes.check_b*self.qu_close_box
		self.box_b = np.argwhere(self.checkb==1)
		# needs to be a loop (rather than vectorised) in case two robots are close to the same box
		for b in self.box_b:		
			if self.check_r[self.mins[b]] == 1: # if the box is close to a robot and free AND the robot that is closest to box b is also free:
				self.check_r[self.mins[b]] = 0 # change robot state to 0 (not free, has a box)
				boxes.check_b[b] = 0 # change box state to 0 (not free, on a robot)
				boxes.box_c[b] = self.rob_c[self.mins[b]] # change the box centre so it is aligned with its robot carrier's centre
				boxes.robot_carrier[b] = self.mins[b] # set the robot_carrier for box b to that robot ID

		random_walk(self,boxes) # the robots move using the random walk function which generates a new deviation (rob_d)
		self.rob_c = self.rob_c + self.rob_d # robots centres change as they move
		anti_check_b = boxes.check_b == 0 # if box is not free, anti_check_b = 1 and therefore box_d(below) is not 0 
		boxes.box_d = np.array((anti_check_b,anti_check_b)).T*self.rob_d[boxes.robot_carrier] # move the boxes by the amount equal to the robot carrying them 
		boxes.box_c = boxes.box_c + boxes.box_d
		boxes.beyond_b = boxes.box_c.T[0] > width - exit_width#4*radius # beyond_b = 1 if box centre is in the delivery area (including those already delivered)
		if any(boxes.beyond_b) == 1:
			boxes.delivered = boxes.delivered + np.sum(boxes.beyond_b)
			boxes.box_n = np.argwhere(boxes.beyond_b == 1)
			rob_n = boxes.robot_carrier[boxes.box_n]
			boxes.robot_carrier[boxes.box_n] = -1
			boxes.check_b[boxes.box_n] = 1
			self.check_r[rob_n] = 1
			boxes.box_c.T[0,boxes.box_n] = boxes.box_c.T[0,boxes.box_n] - 600
			# any robots that have just delivered a box go to state 4.2 (move west)
			self.state[rob_n] = 5 
	
		# robots that have a box and are in state 0 or 5 recieve new random states 1,2,3
		self.have_a_box = np.argwhere(self.check_r==0) # have a box (1= free)
		self.st_0 = np.argwhere(self.state==0) # robot numbers with state 0 
		self.st_5 = np.argwhere(self.state==5) # robot numbers with state 5
		self.st_50 = np.append(self.st_0,self.st_5) # robot numbers with state 0 or 5 
		self.box_and_0 = np.intersect1d(self.st_50,self.have_a_box) # robots with state 0 or 5 that are carrying a box
		self.random_states = np.ones(np.size(self.box_and_0))*2 # random states selected between 1 and 3
		self.state[self.box_and_0] = self.random_states # assign the states to the bots with a box and in state 0 or 5 at the moment
		#
		
		# total number of robots in the range of beacons i.e. in the delivery area 
		west = np.argwhere(self.rob_c.T[0]<2*radius)
		west5 = np.intersect1d(self.st5,west)
		self.state[west5] = 0 
	
		self.st0 = np.argwhere(self.state==0).flatten()
		self.st2 = np.argwhere(self.state==2).flatten()	
		self.st5 = np.argwhere(self.state==5).flatten()
	# the following is for plotting purposes only 
		self.state_0 = self.rob_c[self.st0]
		self.state_2 = self.rob_c[self.st2]
		self.state_5 = self.rob_c[self.st5]
	###

## Movement function with agent-agent avoidance behaviours ## 
def random_walk(swarm,boxes):
	swarm.counter += 1 # time step forwards 1s 
	# Add noise to the heading 
	noise = 0.01*np.random.randint(-50,50,(swarm.num_agents))
	swarm.heading += noise
	
	# Force for movement according to new chosen heading 
	swarm.heading_x = 1*np.cos(swarm.heading) # move in x 
	swarm.heading_y = 1*np.sin(swarm.heading) # move in y

	# S2, with box, move to right (E), y zero
	swarm.heading_x[swarm.st2] = swarm.heading_x[swarm.st2] + 1
		#swarm.heading_y[swarm.st2] = 0 
	# S5, too many robots in delivery area, all without box move left (W)
	swarm.heading_x[swarm.st5] = swarm.heading_x[swarm.st5] - 1 

	
	F_heading = -np.array([[swarm.heading_x[n], swarm.heading_y[n]] for n in range(0, swarm.num_agents)]) # influence on the robot's movement based on the noise added to the heading
	
	# Agent-agent avoidance
	r = repulsion_distance # distance at which repulsion is felt (set at start of code)
	
	# Compute (euclidean == cdist) distance between agents
	agent_distance = cdist(swarm.rob_c, swarm.rob_c)	# distance between all the agents to all the agents
	box_dist = cdist(boxes.box_c,swarm.rob_c) # distance between all the boxes and all the agents
	# Compute vectors between agents
	proximity_to_robots = swarm.rob_c[:,:,np.newaxis]-swarm.rob_c.T[np.newaxis,:,:] 
	proximity_to_boxes = boxes.box_c[:,:,np.newaxis] - swarm.rob_c.T[np.newaxis,:,:]
	
	# Calc repulsion vector on agents due to proximity to (none moving) boxes
	# Equation chosen so that the repulsion is proportional to the distance and influence factor (R_box). It is high at close range and low at far
	F_box = R_box*r*np.exp(-box_dist/r)[:,np.newaxis,:]*proximity_to_boxes/(swarm.num_agents-1)	
	F_box = np.sum(F_box,axis=0) # sum the repulsion vectors due to boxes on the agents
	
	not_free = swarm.check_r == 0 # list of boxes that are sitting in the warehouse not picked up 
	F_box[0] = not_free*F_box[0].T # repulsion force on agents goes to 0 for the boxes that are being carried 
	F_box[1] = not_free*F_box[1].T
	
	# Calc repulsion vector on agent due to proximity to other agents
	# Equation chosen so that the repulsion is proportional to the distance and influence factor (R_rob). It is high at close range and low at far
	F_agent = R_rob*r*np.exp(-agent_distance/r)[:,np.newaxis,:]*proximity_to_robots/(swarm.num_agents-1)	
	
	# disperse from agents with boxes
	m = np.argwhere(swarm.check_r==0).flatten() # robot numbers which are holding boxes
	#dispersion below


	for N in range(swarm.num_agents):
		for n in m: 
			if N != n:
				F_agent[n][0][N] = F_agent[n][0][N]*10 # disperse from robots with boxes
				F_agent[n][1][N] = F_agent[n][1][N]*10
			if N == n: 
				F_agent[N][0][n] = 0 # don't disperse from yourself
				F_agent[N][1][n] = 0
		#for n in k:
		#	if N != n:
		#F_agent[k][0][N] = F_agent[k][0][N]*-10
		#F_agent[k][1][N] = F_agent[k][1][N]*-10
		#	if N == n:
		#		F_agent[N][0][n] = 0 # don't disperse from yourself
		#		F_agent[N][1][n] = 0

	F_agent = np.sum(F_agent, axis =0).T # sum the repulsion vectors
#	F_agent = F_agent*(1+(boxes.delivered/4))
	i = np.argwhere(swarm.check_r==1)
	F_box[:,i] = 0
	
	# Force on agent due to proximity to walls
	F_wall_avoidance = avoidance(swarm.rob_c, swarm.map)

	# Repulsion vectors added together
	F_agent += F_wall_avoidance + F_heading + F_box.T
	F_x = F_agent.T[0] # Repulsion vector in x
	F_y = F_agent.T[1] # in y 
	
	# New movement due to repulsion vectors
	new_heading = np.arctan2(F_y, F_x) # new heading due to repulsions
	move_x = swarm.speed*np.cos(new_heading) # Movement in x 
	move_y = swarm.speed*np.sin(new_heading) # Movement in y 
	
	# Total change in movement of agent (robot deviation)
	swarm.rob_d = -np.array([[move_x[n], move_y[n]] for n in range(0, swarm.num_agents)])
	return swarm.rob_d

## Avoidance behaviour for avoiding the warehouse walls ##		
def avoidance(rob_c,map): # input the agent positions array and the warehouse map 
	num_agents = len(rob_c) # num_agents is number of agents according to position array
## distance from agents to walls ##
	# distance from the vertical walls to your agent (horizontal distance between x coordinates)
	difference_in_x = np.array([map.planeh-rob_c[n][1] for n in range(num_agents)])
	# distance from the horizontal walls to your agent (vertical distance between y coordinates)
	difference_in_y = np.array([map.planev-rob_c[n][0] for n in range(num_agents)])
	
	# x coordinates of the agent's centre coordinate
	agentsx = rob_c.T[0]
	# y coordinates  
	agentsy = rob_c.T[1]

## Are the agents within the limits of the warehouse? 
	x_lower_wall_limit = agentsx[:, np.newaxis] >= map.limh.T[0] # limh is for horizontal walls. x_lower is the bottom of the square
	x_upper_wall_limit = agentsx[:, np.newaxis] <= map.limh.T[1] # x_upper is the top bar of the warehouse square 
	# Interaction combines the lower and upper limit information to give a TRUE or FALSE value to the agents depending on if it is IN/OUT the warehouse boundaries 
	interaction = x_upper_wall_limit*x_lower_wall_limit
		
	# Fy is repulsion vector on the agent in y direction due to proximity to the horziontal walls 
	# This equation was designed to be very high when the agent is close to the wall and close to 0 otherwise
	Fy = np.exp(-2*abs(difference_in_x) + R_wall)
	# The repulsion vector is zero if the interaction is FALSE meaning that the agent is safely within the warehouse boundary
	Fy = Fy*difference_in_x*interaction	

	# Same as x boundaries but now in y
	y_lower_wall_limit = agentsy[:, np.newaxis] >= map.limv.T[0] # limv is vertical walls 
	y_upper_wall_limit = agentsy[:, np.newaxis] <= map.limv.T[1]
	interaction = y_lower_wall_limit*y_upper_wall_limit
	Fx = np.exp(-2*abs(difference_in_y) + R_wall)
	Fx = Fx*difference_in_y*interaction
	
	# For each agent the repulsion in x and y is the sum of the repulsion vectors from each wall
	Fx = np.sum(Fx, axis=1)
	Fy = np.sum(Fy, axis=1)
	# Combine to one vector variable
	F = np.array([[Fx[n], Fy[n]] for n in range(num_agents)])
	return F
####################################################################################
'The following run the simulation in two different ways. They should not be run together. i.e. set_up should only be called if ani = False (set at the start of the code) 1. Set-up is used to collect data about the simulation and run it for a chosen time limit 2. if ani=true then an animation is generated of the warehouse but no data is  collected or kept about that run'
####################################################################################
class data:
	def __init__(self,num_agents,num_boxes,anim,limit):
		self.num_agents = num_agents
		self.num_boxes = num_boxes
		self.robots = swarm(self.num_agents)
		self.items = boxes(self.num_boxes,self.robots)
		self.time = limit
		self.anim = anim
		self.counter = 0 

		warehouse_map = warehouse.map()
		warehouse_map.warehouse_map(width,height)
		warehouse_map.gen()
		self.robots.map = warehouse_map

		self.data_collect()
		
	def data_collect(self):
		self.robots.iterate(self.items)
		if self.anim == False:
			while self.robots.counter <= self.time:
				self.robots.iterate(self.items)
				if self.items.delivered == self.items.num_boxes:
					#print(1,self.robots.counter)
					return self.robots.counter
					break
					self.robots.counter = self.time+1
					#exit()
			sr = self.items.delivered
			if sr > 0:
				sr = float(sr/self.items.num_boxes)
			#print(self.items.delivered,"of",self.items.num_boxes,"collected =",sr*100,"%")
			#print("in",self.robots.counter,"seconds")
		if self.anim == True:
			self.ani()
			
	def ani(self):
		fig = plt.figure()
		ax = plt.axes(xlim=(0, width), ylim=(0, height))
		dot0, = ax.plot(self.robots.state_0[:,0],self.robots.state_0[:,1],
					  'ko',	  markersize = marker_size, fillstyle = 'none')
		dot2, = ax.plot(self.robots.state_2[:,0],self.robots.state_2[:,1],
					  'go',	  markersize = marker_size, fillstyle = 'none')
		dot5, = ax.plot(self.robots.state_5[:,0],self.robots.state_5[:,1],
					  'yo',	  markersize = marker_size, fillstyle = 'none')
		box, = ax.plot(self.items.box_c[:,0],self.items.box_c[:,1], 'rs', markersize = marker_size-5)

		plt.axis('square')
		plt.axis([0,width,0,height])
		def animate(i):
			self.robots.iterate(self.items)

			dot0.set_data(self.robots.state_0[:,0],self.robots.state_0[:,1])
			dot2.set_data(self.robots.state_2[:,0] ,self.robots.state_2[:,1] )
			dot5.set_data(self.robots.state_5[:,0] ,self.robots.state_5[:,1] )

			box.set_data(self.items.box_c[:,0], self.items.box_c[:,1])

			plt.title("Time is "+str(self.robots.counter)+"s")
			if self.items.delivered == self.num_boxes or self.robots.counter > self.time:
				sr = self.items.delivered
				if sr > 0:
					sr = float(sr/self.items.num_boxes)
				print(self.items.delivered,"of",self.items.num_boxes,"collected =",sr*100,"%")
				print("in",self.robots.counter,"seconds")
				exit()
		anim = animation.FuncAnimation(fig, animate, frames=500, interval=0.1)
		
		plt.xlabel("Warehouse width (cm)")
		plt.ylabel("Warehouse height (cm)")
		ex = [width-exit_width, width-exit_width]
		ey = [0, height]
		plt.plot(ex,ey,':')
		plt.show()
		
		


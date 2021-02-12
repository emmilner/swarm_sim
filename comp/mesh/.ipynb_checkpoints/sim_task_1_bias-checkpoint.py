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
		self.state = np.zeros(self.num_agents)
		self.state_0 = np.zeros((self.num_agents,2))
		self.state_1 = np.zeros((self.num_agents,2))
		self.state_2 = np.zeros((self.num_agents,2))
		self.state_3 = np.zeros((self.num_agents,2))
		self.state_41 = np.zeros((self.num_agents,2))
		self.state_42 = np.zeros((self.num_agents,2))
		self.state_43 = np.zeros((self.num_agents,2))

		
	def iterate(self,boxes): # moves the robot and box positions forward in one time step
		dist = cdist(boxes.box_c, self.rob_c) # calculates the euclidean distance from every robot to every box (centres)
		qu_close_box = np.min(dist,1) < box_range # if the minimum distance box-robot is less than the pick up sensory range, then qu_close_box = 1
		#qu_close_rob = np.min(dist,0) < box_range
		mins = np.argmin(dist,1)	
		checkb = boxes.check_b*qu_close_box
		box_b = np.argwhere(checkb==1)
		# needs to be a loop (rather than vectorised) in case two robots are close to the same box
		for b in box_b:		
			if self.check_r[mins[b]] == 1: # if the box is close to a robot and free AND the robot that is closest to box b is also free:
				self.check_r[mins[b]] = 0 # change robot state to 0 (not free, has a box)
				boxes.check_b[b] = 0 # change box state to 0 (not free, on a robot)
				boxes.box_c[b] = self.rob_c[mins[b]] # change the box centre so it is aligned with its robot carrier's centre
				boxes.robot_carrier[b] = mins[b] # set the robot_carrier for box b to that robot ID

		random_walk(self,boxes) # the robots move using the random walk function which generates a new deviation (rob_d)
		self.rob_c = self.rob_c + self.rob_d # robots centres change as they move
		anti_check_b = boxes.check_b == 0 # if box is not free, anti_check_b = 1 and therefore box_d(below) is not 0 
		boxes.box_d = np.array((anti_check_b,anti_check_b)).T*self.rob_d[boxes.robot_carrier] # move the boxes by the amount equal to the robot carrying them 
		boxes.box_c = boxes.box_c + boxes.box_d
		boxes.beyond_b = boxes.box_c.T[0] > width - 4*radius # beyond_b = 1 if box centre is in the delivery area (including those already delivered)
		if any(boxes.beyond_b) == 1:
			boxes.delivered = boxes.delivered + np.sum(boxes.beyond_b)
			boxes.box_n = np.argwhere(boxes.beyond_b == 1)
			rob_n = boxes.robot_carrier[boxes.box_n]
			boxes.robot_carrier[boxes.box_n] = -1
			boxes.check_b[boxes.box_n] = 1
			self.check_r[rob_n] = 1
			boxes.box_c.T[0,boxes.box_n] = boxes.box_c.T[0,boxes.box_n] - 600
			# any robots that have just delivered a box go to state 4.2 (move west)
			self.state[rob_n] = 4.2

			# any robots that have just delivered and are in lower sections, go to state 4.1
			rob_n_lower  = np.argwhere(self.rob_c.T[0]<(height/3))
			intersect_low = np.intersect1d(rob_n_lower,rob_n) # delivered and in lower section
			self.state[intersect_low] = 4.1
			# robots that have just delivered and are in upper section, go to state 4.3
			rob_n_upper = np.argwhere(self.rob_c.T[0]>(height/3))
			intersect_up = np.intersect1d(rob_n_upper,rob_n) # delivered and in upper section 
			self.state[intersect_up] = 4.3
		
		# robots in state 4 (no box, in exit) that are clear of the exit area, go to state 0 
		st_41 = np.argwhere(self.state==4.1)
		st_42 = np.argwhere(self.state==4.2)
		st_43 = np.argwhere(self.state==4.3)
		
		cleared = np.argwhere(self.rob_c.T[0] < width - exit_width) # beyond line without a box 
		inter_clear_41 = np.intersect1d(st_41,cleared)
		self.state[inter_clear_41] = 0 
		inter_clear_42 = np.intersect1d(st_42,cleared)
		self.state[inter_clear_42] = 0 
		inter_clear_43 = np.intersect1d(st_43,cleared)
		self.state[inter_clear_43] = 0 
		
		in_upper = np.argwhere(self.rob_c.T[1]>(2*height/3)) # in upper section
		in_lower = np.argwhere(self.rob_c.T[1]<(height/3)) # in lower sectio
		inter_lower = np.intersect1d(st_41,in_upper) # a lower node in upper section
		self.state[inter_lower] = 4.2 # lower becomes middle
		inter_upper = np.intersect1d(st_43,in_lower) # an upper node in lower section 
		self.state[inter_upper] = 4.2 # upper becomes middle

		#### 
		# robots that are in state 0, have no box and are in exit area, go to state 4.2 
		st_0 = np.argwhere(self.state==0)
		notcleared = np.argwhere(self.rob_c.T[0] > width - exit_width) # beyond line without a box 
		inter_notclear_0 = np.intersect1d(st_0,notcleared)
		self.state[inter_notclear_0] = 4.2 
		
		# reset count of robots near beacons
		new_st_12 = False
		new_st_23 = False
		new_st_31 = False
		# count number of beacons that are in states 1,2,3
		num_1 = (self.state==1).sum()
		num_2 = (self.state==2).sum()
		num_3 = (self.state==3).sum()
			
		# if there are more than 5 already at that beacon then when assigning new states, assign elsewhere
		if num_1 > 5:
			new_st_12 = True
		if num_2 > 5:
			new_st_23 = True
		if num_3 > 5:
			new_st_31 = True		

		# robots that have a box and are in state 0 recieve new random states 1,2,3
		have_a_box = np.argwhere(self.check_r==0) # have a box ( 1= free)
		st_0 = np.argwhere(self.state==0)
		st_5 = np.argwhere(self.state==5)
		st_50 = np.append(st_0,st_5)
		box_and_0 = np.intersect1d(st_50,have_a_box)
		num_new_states = np.size(box_and_0)
	#	if skip == False:
		random_states = np.random.randint(1,3,num_new_states)
		# if one of the beacons is too busy, then change the states set to that beacon to a new one
		if new_st_12 == True:
			r = np.argwhere(random_states==1)
			random_states[r] = 2
		if new_st_23 == True:
			r = np.argwhere(random_states==2)
			random_states[r] = 3
		if new_st_31 == True:
			r = np.argwhere(random_states==3)
			random_states[r] = 1
		self.state[box_and_0] = random_states
		
		total = (self.rob_c.T[0]>width-exit_width-50).sum()
		if total > 15:
			n = np.argwhere(self.state == 0)
			self.state[n] = 5
		if total < 15:
			n = np.argwhere(self.state == 5)
			self.state[n] = 0 
		
		state_0 = np.argwhere(self.state==0).flatten()
		state_1 = np.argwhere(self.state==1).flatten()
		state_2 = np.argwhere(self.state==2).flatten()
		state_3 = np.argwhere(self.state==3).flatten()
		state_41 = np.argwhere(self.state==4.1).flatten()
		state_42 = np.argwhere(self.state==4.2).flatten()
		state_43 = np.argwhere(self.state==4.3).flatten()
		state_5 = np.argwhere(self.state==5).flatten()

		self.state_0 = self.rob_c[state_0]
		self.state_1 = self.rob_c[state_1]
		self.state_2 = self.rob_c[state_2]
		self.state_3 = self.rob_c[state_3]
		self.state_41 = self.rob_c[state_41]
		self.state_42 = self.rob_c[state_42]
		self.state_43 = self.rob_c[state_43]
		self.state_5 = self.rob_c[state_5]

## Movement function with agent-agent avoidance behaviours ## 
def random_walk(swarm,boxes):
	swarm.counter += 1 # time step forwards 1s 
	# Add noise to the heading 
	noise = 0.01*np.random.randint(-50,50,(swarm.num_agents))
	swarm.heading += noise
	
	# Force for movement according to new chosen heading 
	swarm.heading_x = 1*np.cos(swarm.heading) # move in x 
	swarm.heading_y = 1*np.sin(swarm.heading) # move in y
	
	state_1 = np.argwhere(swarm.state ==1)
	state_2 = np.argwhere(swarm.state ==2)
	state_3 = np.argwhere(swarm.state ==3)
	state_42 = np.argwhere(swarm.state ==4.2)	
	state_41 = np.argwhere(swarm.state ==4.1)	
	state_43 = np.argwhere(swarm.state ==4.3)
	state_5 = np.argwhere(swarm.state ==5)
	
	swarm.heading_x[state_1] = swarm.heading_x[state_1] + 1
	swarm.heading_y[state_1] = swarm.heading_y[state_1] + 1
	swarm.heading_x[state_2] = swarm.heading_x[state_2] + 1
	#swarm.heading_y[state_2] = 0#swarm.heading_y[state_2] + 1
	swarm.heading_x[state_3] = swarm.heading_x[state_3] + 1
	swarm.heading_y[state_3] = swarm.heading_y[state_3] - 1
	swarm.heading_x[state_42] = swarm.heading_x[state_42] - 1 # middle
	swarm.heading_y[state_42] = 0#swarm.heading_y[state_4] - 1 # middle
	swarm.heading_x[state_41] = swarm.heading_x[state_41] #- 1 #lower
	swarm.heading_y[state_41] = swarm.heading_y[state_41] + 1 #lower
	swarm.heading_x[state_43] = swarm.heading_x[state_43] #- 1 #upper
	swarm.heading_y[state_43] = swarm.heading_y[state_43] - 1 #upper
	swarm.heading_x[state_5] = swarm.heading_x[state_5] - 1 # too many in delivery
	
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
	m = np.argwhere(swarm.check_r==0).flatten() #dispersion below
	for N in range(swarm.num_agents):
		for n in m:
			#n = m[i]
			if N != n:
				F_agent[n][0][N] = F_agent[n][0][N]*10
				F_agent[n][1][N] = F_agent[n][1][N]*10
			if N == n: 
				F_agent[N][0][n] = 0 
				F_agent[N][1][n] = 0

	F_agent = np.sum(F_agent, axis =0).T # sum the repulsion vectors
	
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
					print(1,self.robots.counter)
					exit()
			sr = self.items.delivered
			if sr > 0:
				sr = float(sr/self.items.num_boxes)
			print(self.items.delivered,"of",self.items.num_boxes,"collected =",sr*100,"%")
			print("in",self.robots.counter,"seconds")
		if self.anim == True:
			self.ani()
			
	def ani(self):
		fig = plt.figure()
		ax = plt.axes(xlim=(0, width), ylim=(0, height))
		dot0, = ax.plot(self.robots.state_0[:,0],self.robots.state_0[:,1],
					  'ko',	  markersize = marker_size, fillstyle = 'none')
		dot1, = ax.plot(self.robots.state_1[:,0],self.robots.state_1[:,1],
					  'bo',	  markersize = marker_size, fillstyle = 'none')
		dot2, = ax.plot(self.robots.state_2[:,0],self.robots.state_2[:,1],
					  'go',	  markersize = marker_size, fillstyle = 'none')
		dot3, = ax.plot(self.robots.state_3[:,0],self.robots.state_3[:,1],
					  'mo',	  markersize = marker_size, fillstyle = 'none')
		dot41, = ax.plot(self.robots.state_41[:,0],self.robots.state_41[:,1],
					  'co',	  markersize = marker_size, fillstyle = 'none')
		dot42, = ax.plot(self.robots.state_42[:,0],self.robots.state_42[:,1],
					  'co',	  markersize = marker_size, fillstyle = 'none')
		dot43, = ax.plot(self.robots.state_43[:,0],self.robots.state_43[:,1],
					  'co',	  markersize = marker_size, fillstyle = 'none')
		dot5, = ax.plot(self.robots.state_5[:,0],self.robots.state_5[:,1],
					  'yo',	  markersize = marker_size, fillstyle = 'none')
		box, = ax.plot(self.items.box_c[:,0],self.items.box_c[:,1], 'rs', markersize = marker_size-5)

		plt.axis('square')
		plt.axis([0,width,0,height])
		def animate(i):
			self.robots.iterate(self.items)

			dot0.set_data(self.robots.state_0[:,0],self.robots.state_0[:,1])
			dot1.set_data(self.robots.state_1[:,0] ,self.robots.state_1[:,1] )
			dot2.set_data(self.robots.state_2[:,0] ,self.robots.state_2[:,1] )
			dot3.set_data(self.robots.state_3[:,0] ,self.robots.state_3[:,1] )
			dot41.set_data(self.robots.state_41[:,0] ,self.robots.state_41[:,1] )
			dot42.set_data(self.robots.state_42[:,0] ,self.robots.state_42[:,1] )
			dot43.set_data(self.robots.state_43[:,0] ,self.robots.state_43[:,1] )
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
		
		


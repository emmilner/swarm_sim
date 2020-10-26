'''
Swarm Warehouse with Boxes Code:
Displays a bird's eye view of a warehouse with robots moving around, avoiding the walls and each other. Boxes are picked up and moved to exit zone by robots. The boxes are requested to be delivered in a given sequence and that sequence is broadcast to the swarm. The robots will only pick up a box if it is the correct on in the sequence. They will then only pick up a new box when the sequence has moved on and the previous box has been delivered to the exit zone.

** Requires the script warehouse.py to be in the same folder as this script as it is called in the code **

Code authored by Emma Milner and Elliot Hogg

The actual specification for the Toshiba robots is as follows: 
agent speed = 2 m/s
agent acceleration 2 m/s/s
diameter of agent is 250 mm
width of warehouse is 5m
height (depth) of warehouse is 5m 
'''
# Still to do
	# Consider other exit zone options e.g. square in the centre (so that wall avoidance doesn't come in)
	# if delivered change the number of boxes.num_boxes so don't have to keep plotting them?
	# avoid boxes if you already have a box 

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
#num_agents = 20 # Number of agents in swarm (default 50)
radius = 12.5 # Radius of single agent (half of 25)
width = 500 # Width of warehouse (100)
height = 500 # Height (depth) of warehouse (100)
speed = 2 # Agent speed (0.5)
repulsion_distance = radius/2# Distance at which repulsion is first felt (3)
#marker_size = 14 # Diameter of circular marker on plot of warehouse (14)

#num_boxes = 3
box_radius = radius
box_range = 2*box_radius # range at which a box can be picked up 
exit_width = int(0.2*width) # if it is too small then it will avoid the wall and be less likely to reach the exit zone 
###
R_rob = 15
R_box = 15
R_wall = 25

pick_up_prob = 100 # prob is <= this 

ani = True
if ani == True:
	num_agents = 10
	num_boxes = 50
	p = 3
	marker_size = width*0.5/20 #diameter
	
	
class swarm():
	def __init__(self,num_agents,p):
		self.speed = speed # Agent speed 
		self.num_agents = num_agents
		self.check_r = np.ones(self.num_agents)
		self.heading = 0.0314*np.random.randint(-100,100,self.num_agents)
		self.rob_c = np.random.randint(box_radius*2,width-box_radius-exit_width,(self.num_agents,2))		
		self.counter = 0 
		self.rob_d = np.zeros((self.num_agents,2))
		self.drop_off_prob = p
		self.beyond_r = np.zeros(self.num_agents)
		self.last_box = np.full((self.num_agents,2),-1)
	
	def iterate(self,boxes): # moves the positions forward in time 
		dist = cdist(boxes.box_c, self.rob_c)
		qu_close_box = np.min(dist,1) < box_range
		qu_close_rob = np.min(dist,0) < box_range
		mins = np.argmin(dist,1)	
		cf_box = qu_close_box*boxes.check_b
		cf_rob = qu_close_rob*self.check_r

		for b in range(boxes.num_boxes):		
			if cf_box[b] == True and cf_rob[mins[b]] == True and self.last_box[mins[b],0] != b and self.last_box[mins[b],1] != b:
				self.check_r[mins[b]] = 0 
				boxes.check_b[b] = 0 
				boxes.box_c[b] = self.rob_c[mins[b]]
				boxes.robot_carrier[b] = mins[b]		

		random_walk(self,boxes) # the robots move using the random walk function 
		self.rob_c = self.rob_c + self.rob_d
		boxes.box_d = np.zeros((boxes.num_boxes,2))
		
		check_b_a = boxes.check_b == 0 
		boxes.box_d = np.array((check_b_a,check_b_a)).T*self.rob_d[boxes.robot_carrier]
		
		boxes.box_d = (boxes.box_d.T*boxes.gone).T
		boxes.box_c = boxes.box_c + boxes.box_d
		boxes.beyond_b = boxes.box_c.T[0] > width - exit_width - radius
		sum_beyond = np.sum(boxes.beyond_b)
		
		self.beyond_r = self.rob_c.T[0] > width - exit_width - radius
		anti_check_b = boxes.check_b == 0 
		boxes.box_c.T[0] = boxes.box_c.T[0] + (boxes.gone*boxes.beyond_b*anti_check_b*200)
		boxes.gone = boxes.beyond_b == 0 
		anti_check_r = self.check_r == 0 
		self.check_r = self.check_r + self.beyond_r*anti_check_r
		boxes.delivered  = sum_beyond
		
		box_drop = np.random.randint(0,100,boxes.num_boxes)
		prob = box_drop < self.drop_off_prob # don't drop if prob below 50 
		prob_check_b = boxes.check_b == 0 
		prob[boxes.seq] = 0 
		for b in range(boxes.num_boxes):
			if prob_check_b[b]*prob[b] == 1 and b!= boxes.seq:
				self.last_box[boxes.robot_carrier[b],1] = self.last_box[boxes.robot_carrier[b],0]
				self.last_box[boxes.robot_carrier[b],0] = b 
				self.check_r[boxes.robot_carrier[b]] = 1
	
		boxes.check_b = boxes.check_b + (prob*prob_check_b)
		
		if boxes.box_c.T[0,boxes.seq] > width:
			boxes.seq += 1
class boxes():
	def __init__(self,number_of_boxes,robots):
		self.num_boxes = number_of_boxes
		self.radius = box_radius
		self.check_b = np.ones(self.num_boxes)
		self.robot_carrier = np.full((self.num_boxes),-1) # Value at index = box number is the robot number that is currently moving that box
		self.delivered = 0
		self.box_c = np.random.randint(box_radius*2,width-box_radius-exit_width,(self.num_boxes,2))
		self.box_d = np.zeros((self.num_boxes,2))
		self.gone = np.ones(self.num_boxes)
		self.beyond_b = np.zeros(self.num_boxes)
		self.seq = 0 
							
## Avoidance behaviour for avoiding the warehouse walls ##		
def avoidance(rob_c,map): # input the agent positions array and the warehouse map 
	num_agents = len(rob_c) # num_agents is number of agents according to position array
## distance from agents to walls ##
	# distance from the vertical walls to your agent (horizontal distance between x coordinates)
	difference_in_x = np.array([map.planeh-rob_c[n][1] for n in range(num_agents)])
	# distance from the horizontal walls to your agent (vertical distance between y coordinates)
	difference_in_y = np.array([map.planev-rob_c[n][0] for n in range(num_agents)])
	
	# x coordinates are the first row (or column) of the agent positions transposed
	agentsx = rob_c.T[0]
	# y coordinates are the second row (or column) of the agent positions transposed 
	agentsy = rob_c.T[1]

## Are the agents within the limits of the warehouse? 
	# Check x coordinates are within the x boundaries
	# x_lower and x_upper give a bool value of:
		# TRUE if within the warehouse limits 
		# FALSE if outside the warehouse limits 
	x_lower_wall_limit = agentsx[:, np.newaxis] >= map.limh.T[0] # limh is for horizontal walls
	x_upper_wall_limit = agentsx[:, np.newaxis] <= map.limh.T[1]
	# Interaction combines the lower and upper limit information to give a TRUE or FALSE value to the agents depending on if it is IN/OUT the warehouse boundaries 
	interaction = x_upper_wall_limit*x_lower_wall_limit
		
	# Fy is Force on the agent in y direction due to proximity to the horziontal walls 
	# This equation was designed to be very high when the agent is close to the wall and close to 0 otherwise
	Fy = np.exp(-2*abs(difference_in_x) + R_wall)
	# The Force is zero if the interaction is FALSE meaning that the agent is safely within the warehouse boundary (so that is does not keep going forever if there is a mistake)
	Fy = Fy*difference_in_x*interaction	

	# Same as x boundaries but now in y
	y_lower_wall_limit = agentsy[:, np.newaxis] >= map.limv.T[0] # limv is vertical walls 
	y_upper_wall_limit = agentsy[:, np.newaxis] <= map.limv.T[1]
	interaction = y_lower_wall_limit*y_upper_wall_limit
	
	Fx = np.exp(-2*abs(difference_in_y) + R_wall)
	Fx = Fx*difference_in_y*interaction
	
	# For each agent the force in x and y is the sum of the forces from each wall
	Fx = np.sum(Fx, axis=1)
	Fy = np.sum(Fy, axis=1)
	# Combine x and y force vectors
	F = np.array([[Fx[n], Fy[n]] for n in range(num_agents)])
	return F
	
## Movement function with agent-agent avoidance behaviours ## 
def random_walk(swarm,boxes):
	swarm.counter += 1
	# Add noise to the heading function
	noise = 0.01*np.random.randint(-50,50,(swarm.num_agents))
	swarm.heading += noise
	
	# Force for movement according to new chosen heading 
	heading_x = 1*np.cos(swarm.heading) # move in x 
	heading_y = 1*np.sin(swarm.heading) # move in y
	F_heading = -np.array([[heading_x[n], heading_y[n]] for n in range(0, swarm.num_agents)])
	
	# Agent-agent avoidance
	r = repulsion_distance # distance at which repulsion is felt (set at start of code)
	
	# Compute (euclidean == cdist) distance between agents
	agent_distance = cdist(swarm.rob_c, swarm.rob_c)	
	box_dist = cdist(boxes.box_c,swarm.rob_c)
	# Compute vectors between agents
	proximity_vectors = swarm.rob_c[:,:,np.newaxis]-swarm.rob_c.T[np.newaxis,:,:] 
	proximity_to_boxes = boxes.box_c[:,:,np.newaxis] - swarm.rob_c.T[np.newaxis,:,:]
	
	F_box = R_box*r*np.exp(-box_dist/r)[:,np.newaxis,:]*proximity_to_boxes/(swarm.num_agents-1)	
	F_box = np.sum(F_box,axis=0)
	
	not_free = swarm.check_r == 0 
	F_box[0] = not_free*F_box[0].T
	F_box[1] = not_free*F_box[1].T
	
	# Force on agent due to proximity to other agents
	F_agent = R_rob*r*np.exp(-agent_distance/r)[:,np.newaxis,:]*proximity_vectors/(swarm.num_agents-1)	
	F_agent = np.sum(F_agent, axis =0).T # Sum of proximity forces
	# Force on agent due to proximity to walls
	F_wall_avoidance = avoidance(swarm.rob_c, swarm.map)

	# Forces added together
	F_agent += F_wall_avoidance + F_heading + F_box.T
	F_x = F_agent.T[0] # Force in x
	F_y = F_agent.T[1] # Force in y 
	
	# New movement due to forces
	new_heading = np.arctan2(F_y, F_x) # new heading due to forces
	move_x = swarm.speed*np.cos(new_heading) # Movement in x due to forces 
	move_y = swarm.speed*np.sin(new_heading) # Movement in y due to forces
	# Total change in movement of agent 
	swarm.rob_d = -np.array([[move_x[n], move_y[n]] for n in range(0, swarm.num_agents)])
	return swarm.rob_d
	# New agent positions 
	#swarm.rob_c += M	
##########################################################

def set_up(time,r,b,p):
	
	swarm_group = swarm(r,p)
	box_group = boxes(b,swarm_group)
	
	warehouse_map = warehouse.map()
	warehouse_map.warehouse_map(width,height)
	warehouse_map.gen()
	swarm_group.map = warehouse_map
	
	swarm_group.iterate(box_group)
	
	while swarm_group.counter <= time:
		swarm_group.iterate(box_group)
		if box_group.delivered == box_group.num_boxes:
			return (1,swarm_group.counter)
			exit()
	sr = box_group.delivered
	#print(box_group.box_times)
	if sr > 0:
		sr = float(sr/box_group.num_boxes)
	return (sr,swarm_group.counter)

if ani == True: 
	swarm = swarm(num_agents,p)
	boxes = boxes(num_boxes,swarm)
	
	warehouse_map = warehouse.map()
	warehouse_map.warehouse_map(width,height)
	warehouse_map.gen()
	swarm.map = warehouse_map
	
	swarm.iterate(boxes)
	
	fig = plt.figure()
	ax = plt.axes(xlim=(0, width), ylim=(0, height))
	dot, = ax.plot([swarm.rob_c[i,0] for i in range(swarm.num_agents)],[swarm.rob_c[i,1] for i in range(num_agents)],
				  'ko',
				  markersize = marker_size, fillstyle = 'none')
	
	box, = ax.plot([boxes.box_c[i,0] for i in range(boxes.num_boxes)],[boxes.box_c[i,1] for i in range(boxes.num_boxes)], 'rs', markersize = marker_size-5)
	seq, = ax.plot([boxes.box_c[0,0]],[boxes.box_c[0,1]],'ks',markersize = marker_size-5)
	plt.axis('square')
	plt.axis([0,width,0,height])
	def animate(i):
		swarm.iterate(boxes)

		dot.set_data([swarm.rob_c[n,0] for n in range(num_agents)],[swarm.rob_c[n,1] for n in range(num_agents)])
	#	for b in range(num_boxes):
	#		plt.annotate(str(b), (boxes.box_c[b,0], boxes.box_c[b,1]))
		box.set_data([boxes.box_c[n,0] for n in range(boxes.num_boxes)],[boxes.box_c[n,1] for n in range(boxes.num_boxes)])
		seq.set_data([boxes.box_c[boxes.seq,0],[boxes.box_c[boxes.seq,1]]])

		plt.title("Time is "+str(swarm.counter)+"s")
		if boxes.delivered == boxes.num_boxes:
			exit()
	anim = animation.FuncAnimation(fig, animate, frames=500, interval=0.1)
	plt.xlabel("Warehouse width (cm)")
	plt.ylabel("Warehouse height (cm)")
	ex = [width-exit_width, width-exit_width]
	ey = [0, height]
	plt.plot(ex,ey,':')
	plt.show()

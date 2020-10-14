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
R_rob = 20
R_box = 20
R_wall = 25

pick_up_prob = 100 # prob is <= this 
drop_off_prob = 4 # prob is <= this

#counter = 1
#finished = False
ani = False
if ani == True:
	num_agents = 50
	num_boxes = 50
	marker_size = width*0.5/20 #diameter
	
def convert_to_list(self):
	listed = []
	for i in range(len(self)):
		listed.append(self[i])
	return listed 
	
class swarm():
	def __init__(self,num_agents):
		self.speed = speed # Agent speed 
		self.heading = []
		self.num_agents = num_agents
		#0.0314*np.random.randint(-100,100,self.num_agents) # create a new heading direction for each agent (this is pi * angle in degrees between -100 and + 100 = angle in radians)
		self.check_r = [False for i in range(self.num_agents)]
		self.holding_box = [] # value is -1 if the robot has no box
		self.last_box = []
		for i in range(self.num_agents):
			self.holding_box.append(-1)
			self.last_box.append([-1,-1])
		self.rob_c = self.gen_agents()
		self.counter = 0

	def gen_agents(self): # generate the agent's positions 
		# rob_c is the centre point coordinate of the robot
		self.heading = 0.0314*np.random.randint(-100,100,self.num_agents) # create a new heading direction for each agent (this is pi * angle in degrees between -100 and + 100 = angle in radians)
		self.rob_c = np.zeros((self.num_agents,2)) # set all to zero initially
		
		for i in range(self.num_agents): # for every agent generate a random staring position
			# coordinates are anywhere within the warehouse but at least a robot radius from the wall so it does not start in the wall
			a = (width-(2*radius))*np.random.random_sample() + radius # x coordinate 
			#a = (width-exit_width+radius) + np.random.random_sample()*exit_width - radius
			b = (height-(2*radius))*np.random.random_sample() + radius # y coordinate 
			#self.rob_c[i] = [np.random.randint(box_radius+(width-exit_width),width-box_radius),np.random.randint(box_radius,height-box_radius)]
			self.rob_c[i] = [a,b]
			#np.array([a,b]) # agent position is (x,y)
		return self.rob_c
	
	def robot_iterate(self,boxes): # moves the positions forward in time 
		global warehouse_map # sets the map everywhere
		random_walk(self,boxes) # the robots move using the random walk function 
		these_boxes = boxes
		#global counter
		#global finished
		#counter = 1 + counter
		#if False not in these_boxes.delivered and finished == False:
		#	finished = True
			
class boxes():
	def __init__(self,number_of_boxes,robots):
		self.num_boxes = number_of_boxes
		self.radius = box_radius
		self.check_b = [False for i in range(self.num_boxes)] # True if box is moving
		self.robot_carrier = [] # Value at index = box number is the robot number that is currently moving that box
		self.seq = 0
		self.box_times = []
		for i in range(self.num_boxes):
			self.robot_carrier.append(-1)
			self.box_times.append(0)
		self.delivered = [False for i in range(self.num_boxes)]# True if box delivered
		self.box_c = self.generate_boxes(robots)

		
	def generate_boxes(self,robots):
		self.box_c = np.zeros((self.num_boxes,2))
		for i in range(self.num_boxes):
			# box_c is the centre point coordinate of the box
			self.box_c[i] = [np.random.randint(box_radius*2,width-box_radius-exit_width),np.random.randint(box_radius*2,height-box_radius)]
		self.check_for_boxes(robots)
		return self.box_c
						
	def pick_up_box(self,robots,rob_num,box_num):
		self.check_b[box_num] = True # the box is now picked up
		robots.check_r[rob_num] = True # the robot now has a box
		self.robot_carrier[box_num] = rob_num # the robot is assigned to that box
		robots.holding_box[rob_num] = box_num # the box is assigned to that robot
		self.box_c[box_num,0] = robots.rob_c[self.robot_carrier[box_num],0]
		self.box_c[box_num,1] = robots.rob_c[self.robot_carrier[box_num],1]
				

	def drop_box(self,robots,rob_num,box_num):
		self.check_b[box_num] = False # the box is now picked up
		robots.check_r[rob_num] = False # the robot now has a box
		self.robot_carrier[box_num] = -1 # the robot is assigned to that box
		robots.holding_box[rob_num] = -1 # the box is assigned to that robot
		robots.last_box[rob_num][1] = robots.last_box[rob_num][0]
		robots.last_box[rob_num][0] = box_num

		if box_num == self.seq:
			self.delivered[box_num] = True
			self.box_times[box_num] = robots.counter
			if self.seq < self.num_boxes:
				self.seq += 1
	
	def calc_dist(self,robots,r,b,qu):
		x_diff = robots.rob_c[r,0] - self.box_c[b,0]
		y_diff = robots.rob_c[r,1] - self.box_c[b,1]
		if qu == 0:
			distance = np.sqrt(np.square(x_diff) + np.square(y_diff))
			return distance
		if qu == 1:
			return [x_diff,y_diff]
	
	def convert_dict_to_list(self,robots,dict_to_convert):
		distance_list = np.zeros(robots.num_agents)
		for r in range(robots.num_agents): 
			distance_list[r] = dict_to_convert[r]
		return distance_list
			
	def check_for_boxes(self,robots):
		if self.check_b[self.seq] == False: # if the seq box hasn't been picked up yet 
			dist_to_seq = cdist([self.box_c[self.seq]],robots.rob_c)				
			mini = dist_to_seq.min() # find the minimum distance per robot
			qu = mini <= box_range # True/False list to question: is this box within range of the robot
			if qu == True: # if at least one box is within range 
				for i in range(robots.num_agents):
					if dist_to_seq[0,i] == mini and robots.check_r[i] == False: # if robot is within range of robot
						self.pick_up_box(robots,i,self.seq)
		
		#dist_to_box = cdist(self.box_c,robots.rob_c)
		dists = {}
		for b in range(self.num_boxes):
			dists[b] = {}
			for r in range(robots.num_agents):
				dists[b][r] = self.calc_dist(robots,r,b,0)
		
		for b in range(self.num_boxes):
			if self.check_b[b] == False and self.delivered[b] == False:
				distances = self.convert_dict_to_list(robots,dists[b])
				qu = distances <= box_range # True/False list to question: is this box within range of the robot
				if any(qu) == True: #if any of the robots are close enough to box b
					#Which robots are close and which is closest?
					qu_ans = qu*distances
					for robot in range(robots.num_agents):
						if qu_ans[robot] != 0 and self.check_b[b] == False:
							prob = np.random.randint(0,100)
							if robots.check_r[robot] == False and prob <= pick_up_prob and b != robots.last_box[robot][0] and b != robots.last_box[robot][1]:
								self.pick_up_box(robots,robot,b)

	def box_iterate(self,robots): 
		self.check_for_boxes(robots)
		for b in range(self.num_boxes):
			prob = np.random.randint(0,100)
			if self.check_b[b] == True and prob <= drop_off_prob and b != self.seq: 
				self.drop_box(robots,self.robot_carrier[b],b)
					
		for b in range(self.num_boxes):
			if self.check_b[b] == True:
				self.box_c[b,0] = robots.rob_c[self.robot_carrier[b],0]
				self.box_c[b,1] = robots.rob_c[self.robot_carrier[b],1]
					
		if self.box_c[self.seq,0] > width-exit_width-radius: # if correct box is in the exit zone 
			self.box_c[self.seq,0] += exit_width+20 
			self.drop_box(robots,self.robot_carrier[self.seq],self.seq)
		return (self.delivered, self.seq)
								
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
	for N in range(swarm.num_agents):
		if N == boxes.robot_carrier[boxes.seq]:
			heading_x[N] += 1	
	
	F_heading = -np.array([[heading_x[n], heading_y[n]] for n in range(0, swarm.num_agents)])
	
	# Agent-agent avoidance
	r = repulsion_distance # distance at which repulsion is felt (set at start of code)
	
	# Compute (euclidean == cdist) distance between agents
	agent_distance = cdist(swarm.rob_c, swarm.rob_c)	
	box_dist = cdist(boxes.box_c,swarm.rob_c)
#	print("agent distance shape", np.shape(agent_distance))
#	print("box distance shape",np.shape(box_dist))
	# Compute vectors between agents
	proximity_vectors = swarm.rob_c[:,:,np.newaxis]-swarm.rob_c.T[np.newaxis,:,:] 
	proximity_to_boxes = boxes.box_c[:,:,np.newaxis] - swarm.rob_c.T[np.newaxis,:,:]
#	print("agent vectors shape",np.shape(proximity_vectors))
#	print("box vectors shape",np.shape(proximity_to_boxes))
	
	F_box = R_box*r*np.exp(-box_dist/r)[:,np.newaxis,:]*proximity_to_boxes/(swarm.num_agents-1)	

	F_box = np.sum(F_box,axis=0)
	F_box[0] = swarm.check_r*F_box[0].T
	F_box[1] = swarm.check_r*F_box[1].T	
	# Force on agent due to proximity to other agents
	F_agent = R_rob*r*np.exp(-agent_distance/r)[:,np.newaxis,:]*proximity_vectors/(swarm.num_agents-1)	
	n = boxes.robot_carrier[boxes.seq]
	if n != -1:
		for N in range(swarm.num_agents):
			if N != n:
				F_agent[n][0][N] = F_agent[n][0][N]*100
				F_agent[n][1][N] = F_agent[n][1][N]*100
			if N == n: 
				F_agent[N][0][n] = 0 
				F_agent[N][1][n] = 0
	
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
	M = -np.array([[move_x[n], move_y[n]] for n in range(0, swarm.num_agents)])
	
	# New agent positions 
	swarm.rob_c += M	
##########################################################

def set_up(time,r,b):
#	global counter
#	counter = 1
#	global finished 
#	finished = False
	swarm_group = swarm(r)
	box_group = boxes(b,swarm_group)
		
	warehouse_map = warehouse.map()
	warehouse_map.warehouse_map(width,height)
	warehouse_map.gen()
	swarm_group.map = warehouse_map
	
	swarm_group.robot_iterate(box_group)
	box_group.box_iterate(swarm_group)
	
	while swarm_group.counter <= time:
		if False in box_group.delivered: 
			swarm_group.robot_iterate(box_group)
		if False in box_group.delivered: 
			box_group.box_iterate(swarm_group)
		if False not in box_group.delivered:
			print(box_group.box_times)
			return (1,swarm_group.counter)
			exit()
	sr = 0 
	print(box_group.box_times)

	for i in range(b):
		if box_group.delivered[i] == True:
			sr += 1
	if sr > 0:
		sr = float(sr/b)
	return (sr,swarm_group.counter)

if ani == True: 
	swarm = swarm(num_agents)
	boxes = boxes(num_boxes,swarm)
	
	warehouse_map = warehouse.map()
	warehouse_map.warehouse_map(width,height)
	warehouse_map.gen()
	swarm.map = warehouse_map
	
	swarm.robot_iterate(boxes)
	boxes.box_iterate(swarm)
	
	fig = plt.figure()
	ax = plt.axes(xlim=(0, width), ylim=(0, height))
	dot, = ax.plot([swarm.rob_c[i,0] for i in range(swarm.num_agents)],[swarm.rob_c[i,1] for i in range(num_agents)],
				  'ko',
				  markersize = marker_size, fillstyle = 'none')
	
	box, = ax.plot([boxes.box_c[i,0] for i in range(boxes.num_boxes)],[boxes.box_c[i,1] for i in range(boxes.num_boxes)], 'rs', markersize = marker_size-5)
	seq, = ax.plot([boxes.box_c[0,0]],[boxes.box_c[0,1]],'ks',markersize = marker_size-5)

	#cir, = ax.plot([radius,radius*3,radius*5,radius*7,10,10,10,10],[10,10,10,10,radius,radius*3,radius*5,radius*7],'ko',markersize = marker_size)
	
	plt.axis('square')
	plt.axis([0,width,0,height])
	def animate(i):
		swarm.robot_iterate(boxes)
		boxes.box_iterate(swarm)
		
		dot.set_data([swarm.rob_c[n,0] for n in range(num_agents)],[swarm.rob_c[n,1] for n in range(num_agents)])
	#	for b in range(num_boxes):
	#		plt.annotate(str(b), (boxes.box_c[b,0], boxes.box_c[b,1]))
		box.set_data([boxes.box_c[n,0] for n in range(boxes.num_boxes)],[boxes.box_c[n,1] for n in range(boxes.num_boxes)])
		seq.set_data([boxes.box_c[boxes.seq,0],[boxes.box_c[boxes.seq,1]]])

		plt.title("Time is "+str(counter)+"s")
		if False not in boxes.delivered:
			exit()
	anim = animation.FuncAnimation(fig, animate, frames=500, interval=0.1)
	plt.xlabel("Warehouse width (cm)")
	plt.ylabel("Warehouse height (cm)")
	ex = [width-exit_width, width-exit_width]
	ey = [0, height]
	plt.plot(ex,ey,':')
	plt.show()

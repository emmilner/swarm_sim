'''
Swarm Warehouse with Boxes Code:
Displays a bird's eye view of a warehouse with robots moving around, avoiding the walls and each other. Boxes are picked up and moved to exit zone by robots. The boxes are requested to be delivered in a given sequence.

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
#import swarm_animation
import sys
import os

### INPUTS ###
#num_agents = 20 # Number of agents in swarm (default 50)
radius = 12.5 # Radius of single agent (5)
width = 500 # Width of warehouse (100)
height = 500 # Height (depth) of warehouse (100)
speed = 2 # Agent speed (0.5)
repulsion_distance = radius/2 # Distance at which repulsion is first felt (3)
#marker_size = 14 # Diameter of circular marker on plot of warehouse (14)

#num_boxes = 3
box_radius = radius
box_range = box_radius # range at which a box can be picked up 
exit_width = int(0.2*width) # if it is too small then it will avoid the wall and be less likely to reach the exit zone 
###
counter = 1
finished = False
ani = True
if ani == True:
	num_agents = 125
	num_boxes = 100
	marker_size = width*0.5/20 #radius #width/(width/radius) # diameter
	
class swarm():
	def __init__(self,num_agents):
		self.rob_c = []
		#self.gen_agents() # coordinate of agent centre point
		self.x = [] 
		#np.zeros(self.num_agents) # Agent x coordinates
		self.y = [] 
		#np.zeros(self.num_agents) # Agent y coordinates
		#self.vel_x = np.zeros(self.num_agents) # Agent x velocity
		#self.vel_y = np.zeros(self.num_agents) # Agent y velocity
		self.speed = speed # Agent speed 
		self.heading = []
		#0.0314*np.random.randint(-100,100,self.num_agents) # create a new heading direction for each agent (this is pi * angle in degrees between -100 and + 100 = angle in radians)
		self.check_r = []
		self.num_agents = num_agents
		#[False for i in range(num_agents)]

	def gen_agents(self): # generate the agent's positions 
		# rob_c is the centre point coordinate of the robot
		self.heading = 0.0314*np.random.randint(-100,100,self.num_agents) # create a new heading direction for each agent (this is pi * angle in degrees between -100 and + 100 = angle in radians)
		self.check_r = [False for i in range(self.num_agents)]
		self.holding_box = [] # value is -1 if the robot has no box
		for i in range(self.num_agents):
			self.holding_box.append(-1)
		self.rob_c = np.zeros((self.num_agents,2)) # set all to zero initially
		
		for i in range(self.num_agents): # for every agent generate a random staring position
			# coordinates are anywhere within the warehouse but at least a robot radius from the wall so it does not start in the wall
			a = (width-(2*radius))*np.random.random_sample() + radius # x coordinate 
			b = (height-(2*radius))*np.random.random_sample() + radius # y coordinate
			self.rob_c[i] = np.array([a,b]) # agent position is (x,y)
		self.x = self.rob_c[0,:] # set to the array of x coordinates
		self.y = self.rob_c[1,:] # set to the array of y coordinates
		
		return self.rob_c
	
	def iterate(self,boxes): # moves the positions forward in time 
		global warehouse_map # sets the map everywhere
		random_walk(self) # the robots move using the random walk function 
		these_boxes = boxes
		these_boxes.check_for_boxes(self)
		global counter
		global finished
		counter = 1 + counter
		if False not in these_boxes.delivered and finished == False:
			print("Finished at: ")
			print(counter)
			finished = True

def convert_to_list(self):
	listed = []
	for i in range(len(self)):
		listed.append(self[i])
	return listed 

class boxes():
	def __init__(self,number_of_boxes):
		self.num_boxes = number_of_boxes
		self.radius = box_radius
		self.box_c = self.generate_boxes()
		self.check_b = [False for i in range(self.num_boxes)] # True if box is moving
		self.robot_carrier = [] # Value at index = box number is the robot number that is currently moving that box
		for i in range(self.num_boxes):
			self.robot_carrier.append(-1)
		self.delivered = [False for i in range(self.num_boxes)]# True if box delivered
		
	def generate_boxes(self):
		self.box_c = np.zeros((self.num_boxes,2))
		for i in range(self.num_boxes):
			# box_c is the centre point coordinate of the box
			self.box_c[i] = [np.random.randint(box_radius,width-box_radius-exit_width),np.random.randint(box_radius,height-box_radius)]
		return self.box_c
		
	def check_for_boxes_set_up(self,robots):
		self.bx = []
		self.by = []
		for i in range(self.num_boxes):
			self.bx.append(self.box_c[i,0])
			self.by.append(self.box_c[i,1])
			
	def check_for_boxes(self,robots):
		box_to_rob = cdist(self.box_c,robots.rob_c) # find the distances from every box to every robot
		btr_list = convert_to_list(box_to_rob) # convert those collection of distances to a list for ease
		mini = box_to_rob.min(1) # find the minimum distance per box
		qu = mini <= box_range # True/False list to question: is this box within range of the robot
		if True in qu: # if at least one box is within range 
			for i in range(self.num_boxes):
				if self.check_b[i] == False and qu[i] == True: # if box is available and within range of robot
					minimum = mini[i] # select the minimum distance to a robot for this box, i 
					btr_list_current = btr_list[i] # select the list of box-robot distances for this box, i
					btr_list_current = convert_to_list(btr_list_current)
					counted = btr_list_current.count(minimum) # count the number of times that minimum distance occurs in the list of box-robot distances
					index = btr_list_current.index(minimum) # find the robot number that is closest
					if robots.check_r[index] == False: # if the robot is available
						self.check_b[i] = True # the box is now picked up
						robots.check_r[index] = True # the robot now has a box
						self.robot_carrier[i] = index # the robot is assigned to that box
						robots.holding_box[index] = i # the box is assigned to that robot
					
					elif robots.check_r[index] == True: # if the robot was carrying a box already 
						for s in range(1,counted): # then go through the other robots which are an equally close distance to the box
							index = btr_list_current.index(minimum,s) 
							if robots.check_r[index] == False: # do the same as above for this robot/box
								self.check_b[i] = True
								robots.check_r[index] = True
								self.robot_carrier[i] = index
								robots.holding_box[index] = i
								break 

	def iterate(self,robots): 
		self.check_for_boxes(robots)
		for i in range(self.num_boxes):
			if self.check_b[i] == True and self.delivered[i] == False: #self.bx[i] <= width-exit_width:
				self.bx[i] = robots.x[self.robot_carrier[i]]
				self.by[i] = robots.y[self.robot_carrier[i]]
				if self.bx[i] > width-exit_width:
					self.delivered[i] = True
					robots.check_r[self.robot_carrier[i]] = False
					robots.holding_box[self.robot_carrier[i]] = -1
		return self.delivered
								
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
	Fy = np.exp(-2*abs(difference_in_x) + 20)
	# The Force is zero if the interaction is FALSE meaning that the agent is safely within the warehouse boundary (so that is does not keep going forever if there is a mistake)
	Fy = Fy*difference_in_x*interaction	
	
	#Fy = 3/difference_in_x
	#Fy = Fy*interaction
	
	# Same as x boundaries but now in y
	y_lower_wall_limit = agentsy[:, np.newaxis] >= map.limv.T[0] # limv is vertical walls 
	y_upper_wall_limit = agentsy[:, np.newaxis] <= map.limv.T[1]
	interaction = y_lower_wall_limit*y_upper_wall_limit
	
	Fx = np.exp(-2*abs(difference_in_y) + 20)
	Fx = Fx*difference_in_y*interaction
	
	#Fx = 3/difference_in_y
	#Fx = Fx*interaction 
	
	# For each agent the force in x and y is the sum of the forces from each wall
	Fx = np.sum(Fx, axis=1)
	Fy = np.sum(Fy, axis=1)
	# Combine x and y force vectors
	F = np.array([[Fx[n], Fy[n]] for n in range(num_agents)])
	return F
	
## Movement function with agent-agent avoidance behaviours ## 
def random_walk(swarm):
	 
	# Add noise to the heading function
	noise = 0.01*np.random.randint(-50,50,(swarm.num_agents))
	swarm.heading += noise
	
	# Force for movement according to new chosen heading 
	heading_x = 1*np.cos(swarm.heading) # move in x 
	heading_y = 1*np.sin(swarm.heading) # move in y
	F_heading = -np.array([[heading_x[n], heading_y[n]] for n in range(0, swarm.num_agents)])
	
	# Agent-agent avoidance
	R = 20 # repulsion strength
	r = repulsion_distance # distance at which repulsion is felt (set at start of code)
	
	# Compute (euclidean == cdist) distance between agents
	agent_distance = cdist(swarm.rob_c, swarm.rob_c)
	
	# Compute vectors between agents
	proximity_vectors = swarm.rob_c[:,:,np.newaxis]-swarm.rob_c.T[np.newaxis,:,:] 
	# Force on agent due to proximity to other agents
	F_agent = R*r*np.exp(-agent_distance/r)[:,np.newaxis,:]*proximity_vectors/(swarm.num_agents-1)	
	F_agent = np.sum(F_agent, axis =0).T # Sum of proximity forces
	
	# Force on agent due to proximity to walls
	F_wall_avoidance = avoidance(swarm.rob_c, swarm.map)
	
	# Forces added together
	F_agent += F_wall_avoidance + F_heading
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
	swarm.x = swarm.rob_c[:,0]
	swarm.y = swarm.rob_c[:,1]
			
##########################################################
def run(num_box):
#n = int(sys.argv[1]) # num of robots
#b = int(sys.argv[2])  # num of boxes
	b = num_box
	num_trials = 5
	time_for_trial = 10000
	time_taken_dict = {}
	
	for n in range(5,150,5):
		time_taken_dict[n] = time_for_trial
		for trial in range(num_trials):
			time_taken = 0.
			boxes_delivered = []
			collecting_robot_numbers = []
			box_to_collect_num = []
			average_time = []
			num_box_del = 0.
			swarm_group = swarm(n)
			box_group = boxes(b)
			this_swarm = swarm_group
			this_swarm.gen_agents()

			warehouse_map = warehouse.map() # call the warehouse script to generate the warehouse walls
			warehouse_map.warehouse_map(width,height) # create a warehouse of size width by height (as seen from bove). Width and height are both declared at the start of the code by the variables 'width' and 'height'
			warehouse_map.gen() # generates the wall obstacles and limits
			this_swarm.map = warehouse_map # declares the warhouse as the map that the swarm is in 
			these_boxes = box_group
			these_boxes.check_for_boxes_set_up(this_swarm)
			these_boxes.check_for_boxes(this_swarm)
			
			for t in range(time_for_trial):
				this_swarm.iterate(these_boxes)
				num_box_delivered = these_boxes.iterate(this_swarm)
				num_box_del = num_box_delivered.count(True)
				if num_box_del == these_boxes.num_boxes: 
					num_box_del = 0 
					average_time.append(t)
					break
				if t == time_for_trial-1 and num_box_del < these_boxes.num_boxes:
					average_time.append(time_for_trial)
					average_time.append(time_for_trial)
		time_a = np.median(average_time)
		time_taken_dict[n] = time_a
		boxes_delivered.append(num_box_del)
		#robot_dict[rob] = num_box_del
	return time_taken_dict


if ani == True: 
	swarm = swarm(num_agents)
	boxes = boxes(num_boxes)
	swarm.gen_agents()
	boxes.check_for_boxes_set_up(swarm)
	
	boxes.check_for_boxes(swarm)
	
	warehouse_map = warehouse.map()
	warehouse_map.warehouse_map(width,height)
	warehouse_map.gen()
	swarm.map = warehouse_map
	swarm.iterate(boxes)
	boxes.iterate(swarm)
	
	fig = plt.figure()
	ax = plt.axes(xlim=(0, width), ylim=(0, height))
	dot, = ax.plot([swarm.x[i] for i in range(swarm.num_agents)],[swarm.y[i] for i in range(num_agents)],
				  'ko',
				  markersize = marker_size, fillstyle = 'none')
	box, = ax.plot([boxes.bx[i] for i in range(boxes.num_boxes)],[boxes.by[i] for i in range(num_boxes)], 'rs', markersize = marker_size)
	#cir, = ax.plot([radius,radius*3,radius*5,radius*7,10,10,10,10],[10,10,10,10,radius,radius*3,radius*5,radius*7],'ko',markersize = marker_size)
	
	plt.axis('square')
	
	def animate(i):
		swarm.iterate(boxes)
		boxes.iterate(swarm)
		
		dot.set_data([swarm.x[n] for n in range(num_agents)],[swarm.y[n] for n in range(num_agents)])
		box.set_data([boxes.bx[n] for n in range(boxes.num_boxes)],[boxes.by[n] for n in range(boxes.num_boxes)])
		plt.title(str(counter))
		if finished == True:
			exit()
	
	anim = animation.FuncAnimation(fig, animate, frames=200, interval=20)
	plt.show()
	

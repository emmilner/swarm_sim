import numpy as np
import scipy.spatial.distance as distance

sensor_range = 10 

# set beacon positions
num_bea = 16 
bea_xy = np.zeros([num_bea,2])
m = 0 
beacon_list = range(10,50,10)
for n in range(4):
	for k in range(4):
		bea_xy[m] = [beacon_list[n],beacon_list[k]]
		m = m + 1 

# set initial box and robot positions
num_r = 5
num_b = 10 
rob_xy = np.zeros([num_r,2])
rob_xy[:,0] = 50 
m = 0 
for n in range(10,50,10):
	rob_xy[m,1] = n
	m = m + 1
box_xy = np.random.randint(0,45,[num_b,2])
rob_xy_dir = np.zeros([num_r,2])
rob_free = np.zeros(num_r)

# Initial conditions
recent_delivery = True

#### START NEW TIME STEP #####

# 'mesh': count nearby boxes and form a prioritised list. 
# At this point the mesh is one entity for simplification.
if recent_delivery == True:
	beacon_box = distance.cdist(box_xy,bea_xy) # re do this once pinged by robot that box has been delivered 
	recent_delivery == False
close_to = beacon_box < sensor_range
sum_truth = sum(close_to)
max_beacon = np.argsort(sum_truth)

# Free robots: ping the mesh for assignment
rob_free_n = np.argwhere(rob_free == 0)
#if np.size(rob_free_n) < num_b:
#	rob_xy_dir[rob_free_n] = bea_xy[max_beacon[0:np.size(rob_free_n)]]
#else:
#	rob_xy_dir[0:num_b] = bea_xy[max_beacon[0:num_b]]

# mesh bots: assign robots to their beacons and update list 

# robots: move to beacons 

# robots: once arrived at beacon, search randomly for box. stay close to beacon

# robots: once find box, return to delivery area 

# robots: once in delivery area, drop box and ping the mesh for new assignment 

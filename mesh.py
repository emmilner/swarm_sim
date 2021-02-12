import numpy as np
import scipy.spatial.distance as distance

sensor_range = 5

num_r = 2
num_r_st = 4 #number of robot states
num_b = 3
num_rb_st = 5

st_rob = np.zeros([num_r,num_r_st])
st_rb = np.zeros([num_r,num_b,num_rb_st])

#starting positons
rob_xy = np.random.randint(0,25,[num_r,2])
box_xy = np.random.randint(0,25,[num_b,2])

# row 0 is distance from robot 0 to boxes 0,1,2
# column 0 is distnace from box 0 to robots 0,1
#cdist is the same size as a slice of robot-box state (st_rb)
box_dist = distance.cdist(rob_xy,box_xy)
rob_dist = distance.cdist(rob_xy,rob_xy)
in_exit = rob_xy[:,0] > 10

# close robots 
close_robots = np.zeros([num_r,num_r])
for r in range(num_r):
	n = np.argwhere(rob_dist[r]<=sensor_range)
	close_robots[r,n] = 1
	close_robots[r,r] = 1 

#exchanging information
loaded = np.zeros([num_r,num_b])



# Share information about which box IDs are now picked up 
for r in range(num_r):
    n = np.argwhere(close_robots[r] == 1)
   # for j in range(sum(close_robots[r])):
    for m in range(np.size(n)):
        if sum(loaded[m]) > sum(loaded[r]):
            loaded[r] = loaded[m]
        else:
            loaded[m] = loaded[r]

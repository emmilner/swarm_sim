import numpy as np

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

loaded = np.zeros(num_r) #Y/N
box_tf = box_dist < sensor_range
rob_tf = rob_dist < sensor_range

box_detected = sum(box_tf.T) #Y/N
rob_detected = sum(rob_tf.T)
in_exit = rob_xy[:,0] > 10

#exchanging information
loaded = np.zeros([num_r,num_r])
loaded[2,2] = 1
times = np.zeros([num_r,num_r])
times[2,2] = 12
for a in range(num_r):
	for b in range(num_r):
		for c in range(num_r):
			if c!=a:
				val_a = loaded[a,c]
				val_b = loaded[b,c]
				if times[a,c] > times[b,c]:
					loaded[b,c] = loaded[a,c]
				if times[b,c] > times[a,c]:
					loaded[a,c] = loaded[b,c]
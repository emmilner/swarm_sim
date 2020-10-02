import ast
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.legend import Legend

def file_opener(name):
	file_in = open("%s.txt" % name, "r")
	time_dict = file_in.readline()
	time_dict = ast.literal_eval(time_dict)
	file_in.close()
	return time_dict

time_dict = file_opener("task_1/results/total_time_results")
fig, ax = plt.subplots()

x = [] #robots
y = [] #boxes
for r in range(10,126,40):  ## 10 to 126 (per 5)
	x.append(r)
for b in range(10,101,40):  ## 10 to 101 (per 10)
	y.append(b)
Z = np.full([len(y),len(x)],0.)
for i_n in range(len(x)):
	for i_b in range(len(y)): #### should this not be just in y?
		b = y[i_b]
		n = x[i_n]
		if time_dict[n][b] == 50000:
			time_dict[n][b] = 49999
		Z[i_b,i_n] = time_dict[n][b]

lines_robot_range = []
lines_box_range = []
handles_robot = []
handles_box = []

for B in range(len(y)):
	t = []
	b = y[B]
	for R in range(len(x)):
		r = x[R]
		t.append(time_dict[r][b])
#	#lines.append(plt.plot(x,y,label='test'))
	lines_robot_range += ax.plot(x,t)
	handles_robot.append("Box #"+str(b))
for R in range(len(x)):
	t = []
	r = x[R]
	for B in range(len(y)):
		b = y[B]
		t.append(time_dict[r][b])
#	#lines.append(plt.plot(x,y,label='test'))
	lines_box_range += ax.plot(y,t)
	handles_box.append("Robot #"+str(r))
	
plt.ylabel("Time taken to collect all boxes")

leg = Legend(ax, lines_robot_range, handles_robot,
            loc='lower center', ncol = 2, frameon=True)
plt.xlabel("Number of robots")

#leg = Legend(ax, lines_box_range, handles_box,
#             loc='lower center', ncol = w, frameon=True)
#plt.xlabel("Number of boxes")

ax.add_artist(leg)
plt.ylim(0, 50000)
plt.show()
	

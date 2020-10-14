import numpy as np
import matplotlib.pylab as plt
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as colors
import matplotlib.colorbar as colorbar
import ast 
from matplotlib.legend import Legend
import sys
import os 
import task1_traj

r = 2 
b = 3
limit = 20
position = task1_traj.set_up(limit,r,b)
rob_x = position[0]
rob_y = position[1]
box_x = position[2]
box_y = position[3]
print(position[3])
print(position[3][7])

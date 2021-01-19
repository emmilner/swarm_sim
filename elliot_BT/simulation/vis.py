#!/usr/bin/env python


import time
import pydot

import py_trees
import argparse
import functools
import sys
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import numpy as np
import random
import behtree.treegen as tg



def justsim(ind, swarm, targets, timesteps, trials = 100):

	# Decode genome into executable behaviour tree
	bt = tg.tree().decode(ind, swarm, targets)
	bt.setup(timeout=15)
	fits = []

	dur = 0
	score = 0
	for k in range(trials):
		fitness = 0; score = 0 ;t = 0
		found = False
		bt = tg.tree().decode(ind, swarm, targets)
		swarm.beacon_set = []
		while t <= timesteps and found == False:
			t += 1
			bt.tick()
			swarm.iterate()
			swarm.get_state()
			score = targets.get_state(swarm, t)
			if targets.found == len(targets.targets):
				found = True

		maxsize = 300
		fitness = 0
		fitness = score/len(targets.targets)
		fitness = fitness - (len(ind.genome)/1000000)
		if fitness < 0: fitness = 0
		print ('fitness: ', fitness)

		targets.reset()
		swarm.reset()

	maxsize = 300
	fitness = 0
	fitness = score/(trials*len(targets.targets))
	fitness = fitness - (len(ind.genome)*0.001)
	if fitness < 0: fitness = 0
	print ('Average fitness: ', fitness)
	print(ind.tree)

	return fits



def post_tick_handler(snapshot_visitor, behaviour_tree):
    print(
        py_trees.display.unicode_tree(
            behaviour_tree.root,
            visited=snapshot_visitor.visited,
            previously_visited=snapshot_visitor.visited
        )
    )

def default(ind, swarm, targets, timesteps):
		
	# Decode genome into executable behaviour tree
	bt = tg.tree().decode(ind, swarm, targets)
	bt.setup(timeout=15)


	# Setup post tick handlers for tree animation
	snapshot_visitor = py_trees.visitors.SnapshotVisitor()
	bt.add_post_tick_handler(functools.partial(post_tick_handler, snapshot_visitor))
	bt.visitors.append(snapshot_visitor)

	# Setup plot
	lim = 40
	xmin = -lim; xmax = lim
	ymin = -lim; ymax = lim
	fig, ax = plt.subplots(facecolor=(.99, .99, .99))	
	ax.set_xlim([xmin,xmax])
	ax.set_ylim([ymin,ymax])
	[ax.plot(swarm.agents[t][0],swarm.agents[t][1], 'bo') for t in range(swarm.size)]
	plt.ion()
	plt.grid()
	fig.canvas.draw()
	plt.show()

	dur = 0; score = 0; fitness = 0; t = 0
	fontsize = 12
	found = False
	swarm.beacon_set = []
	while t <= timesteps and found == False:
		t += 1
		# input()
		bt.tick()
		swarm.iterate()
		swarm.get_state()
		score = targets.get_state(swarm, t)	

		ax.clear()
		ax.set_xlim([xmin,xmax])
		ax.set_ylim([ymin,ymax])
		plt.show()
		plt.grid()
		[ax.plot(swarm.agents[a][0],swarm.agents[a][1], 'bo') for a in range(swarm.size)]
		[ax.plot([swarm.map.obsticles[a].start[0], swarm.map.obsticles[a].end[0]], [swarm.map.obsticles[a].start[1], swarm.map.obsticles[a].end[1]], 'k-', lw=2) for a in range(len(swarm.map.obsticles))]
		
		ax.text(5, 41, 'Swarm behviour: ' + swarm.behaviour + ', ' + str(swarm.param), fontsize=fontsize, color='green')
		ax.text(5, 45, 'Time: %d/%d' %(t, timesteps), fontsize=fontsize, color='purple')
		ax.text(-40, 41, 'Center of Mass: %.2f, %.2f' % (swarm.centermass[0], swarm.centermass[1]), fontsize=fontsize, color='green')
		ax.text(-40, 45, 'Spread: %.2f' % swarm.spread, fontsize=fontsize, color='red')
		ax.text(-20, 45, 'Coverage: %.2f' % targets.coverage, fontsize=fontsize, color='blue')

		#[ax.plot(swarm.beacon_set[a].pos[0],swarm.beacon_set[a].pos[1], 'ro', markersize=70, alpha=0.3) for a in range(len(swarm.beacon_set))]
		if swarm.beacon_att.size != 0:
			for a in range(0, len(swarm.beacon_att)):
				ax.plot(swarm.beacon_att[a][0],swarm.beacon_att[a][1], 'go', markersize=70, alpha=0.3)
		
					#ax.text(swarm.beacon_set[a].pos[0],swarm.beacon_set[a].pos[1], 'A', fontsize=15, color='green')
		if swarm.beacon_rep.size != 0:
			for a in range(0, len(swarm.beacon_rep)):
				ax.plot(swarm.beacon_rep[a][0],swarm.beacon_rep[a][1], 'ro', markersize=70, alpha=0.)
					#ax.text(swarm.beacon_set[a].pos[0],swarm.beacon_set[a].pos[1], 'R', fontsize=15, color='red')

		for n in range(0, len(targets.targets)):
			if targets.old_state[n] == False:
				ax.plot(targets.targets[n][0],targets.targets[n][1], 'ro', markersize=10, alpha=0.5)
			else:
				ax.plot(targets.targets[n][0],targets.targets[n][1], 'go', markersize=10, alpha=0.5)

		fig.canvas.draw()
		print('Time: ', t, '/',timesteps,  end='\r')

	
	print('\n\nScore: ', score)
	print('len targets: ', len(targets.targets))
	maxsize = 300
	fitness = 0
	fitness = score/len(targets.targets)
	print('fitness pre cost: ', fitness)
	#fitness = fitness - (len(ind.genome)*0.001)

	return fitness



def default_ad(inda, indb, swarma, swarmb, targets, timesteps):
		
	# Decode genome into executable behaviour tree
	bta = tg.tree().decode(inda, swarma, targets)
	bta.setup(timeout=15)

	btb = tg.tree().decode(indb, swarmb, targets)
	btb.setup(timeout=15)

	# Setup plot
	lim = 40
	xmin = -lim; xmax = lim
	ymin = -lim; ymax = lim
	fig, ax = plt.subplots(facecolor=(.99, .99, .99))	
	ax.set_xlim([xmin,xmax])
	ax.set_ylim([ymin,ymax])
	plt.ion()
	plt.grid()
	fig.canvas.draw()
	plt.show()

	dur = 0; scorea = 0; scoreb = 0; fitness = 0; t = 0
	fontsize = 12
	found = False
	
	while t <= timesteps and found == False:
		t += 1
		# input()
		bta.tick()
		btb.tick()
		swarma.iterate()
		swarma.get_state()
		swarmb.iterate()
		swarmb.get_state()

		scorea += targets.ad_state(swarma, t)
		scoreb += targets.ad_state(swarmb, t)		

		ax.clear()
		ax.set_xlim([xmin,xmax])
		ax.set_ylim([ymin,ymax])
		plt.show()
		plt.grid()

		[ax.plot(swarma.agents[a][0],swarma.agents[a][1], 'bo') for a in range(swarma.size)]
		[ax.plot(swarmb.agents[a][0],swarmb.agents[a][1], 'ro') for a in range(swarmb.size)]
		[ax.plot([swarma.map.obsticles[a].start[0], swarma.map.obsticles[a].end[0]], [swarma.map.obsticles[a].start[1], swarma.map.obsticles[a].end[1]], 'k-', lw=2) for a in range(len(swarma.map.obsticles))]
		
		ax.text(5, 41, 'Swarm behviour A: ' + swarma.behaviour + ', ' + str(swarma.param), fontsize=fontsize, color='green')
		ax.text(5, 45, 'Swarm behviour B: ' + swarmb.behaviour + ', ' + str(swarmb.param), fontsize=fontsize, color='green')
		#ax.text(-40, 41, 'Center of Mass: %.2f, %.2f' % (swarm.centermass[0], swarm.centermass[1]), fontsize=fontsize, color='green')
		#ax.text(-40, 45, 'Spread: %.2f' % swarm.spread, fontsize=fontsize, color='red')
		ax.text(-20, 45, 'Coverage: %.2f' % targets.coverage, fontsize=fontsize, color='blue')
		
		for n in range(0, len(targets.targets)):
			if targets.old_state[n] == False:
				ax.plot(targets.targets[n][0],targets.targets[n][1], 'ro', markersize=10, alpha=0.5)
			else:
				ax.plot(targets.targets[n][0],targets.targets[n][1], 'go', markersize=10, alpha=0.5)

		fig.canvas.draw()
		print('Time: ', t, '/',timesteps,  end='\r')

	
	print('\n\nScore A: ', scorea)
	print('\nScore B: ', scoreb)
	print('len targets: ', len(targets.targets))
	maxsize = 300
	fitness = 0
	fitness = score/len(targets.targets)
	print('fitness pre cost: ', fitness)
	fitness = fitness - (len(ind.genome)*0.001)
	if fitness < 0: fitness = 0
	print ('Individual fitness: ', fitness)
	input()
	return fitness



# Reworked py-trees code to enable animated dot graphs of solutions

def generate_pydot_graph(root, visibility_level, collapse_decorators=False):

	def get_node_attributes(node, visibility_level):
		blackbox_font_colours = {py_trees.common.BlackBoxLevel.DETAIL: "dodgerblue",
								py_trees.common.BlackBoxLevel.COMPONENT: "lawngreen",
								py_trees.common.BlackBoxLevel.BIG_PICTURE: "white"
								}

		coldict = {py_trees.Status.SUCCESS: 'green', py_trees.Status.FAILURE: 'red', py_trees.Status.INVALID: 'white' , py_trees.Status.RUNNING: 'white' }

		# if isinstance(node, py_trees.composites.Chooser):
		# 	attributes = ('doubleoctagon', col, 'black')  # octagon
		if isinstance(node, py_trees.composites.Selector):
			attributes = ('octagon', coldict[node.status], 'black')  # octagon
		elif isinstance(node, py_trees.composites.Sequence):
			attributes = ('box', coldict[node.status], 'black')
		# elif isinstance(node, py_trees.composites.Parallel):
		# 	attributes = ('parallelogram', col, 'black')
		# elif isinstance(node, py_trees.decorators.Decorator):
		# 	attributes = ('ellipse', 'ghostwhite', 'black')
		else:
			attributes = ('ellipse', coldict[node.status], 'black')
		if node.blackbox_level != py_trees.common.BlackBoxLevel.NOT_A_BLACKBOX:
			attributes = (attributes[0], coldict[node.status], blackbox_font_colours[node.blackbox_level])
		return attributes

	fontsize = 11
	graph = pydot.Dot(graph_type='digraph')
	graph.set_name(root.name.lower().replace(" ", "_"))
	# fonts: helvetica, times-bold, arial (times-roman is the default, but this helps some viewers, like kgraphviewer)
	graph.set_graph_defaults(fontname='times-roman')
	graph.set_node_defaults(fontname='times-roman')
	graph.set_edge_defaults(fontname='times-roman')
	(node_shape, node_colour, node_font_colour) = get_node_attributes(root, visibility_level)
	node_root = pydot.Node(root.name, shape=node_shape, style="filled", fillcolor=node_colour, fontsize=fontsize, fontcolor=node_font_colour)
	graph.add_node(node_root)
	names = [root.name]

	def add_edges(root, root_dot_name, visibility_level, collapse_decorators):
		# if isinstance(root, py_trees.decorators.Decorator) and collapse_decorators:
		# 	return
		if visibility_level < root.blackbox_level:
			for c in root.children:
				(node_shape, node_colour, node_font_colour) = get_node_attributes(c, visibility_level)
				proposed_dot_name = c.name
				while proposed_dot_name in names:
					proposed_dot_name = proposed_dot_name + "*"
				names.append(proposed_dot_name)
				node = pydot.Node(proposed_dot_name, shape=node_shape, style="filled", fillcolor=node_colour, fontsize=fontsize, fontcolor=node_font_colour)
				graph.add_node(node)
				edge = pydot.Edge(root_dot_name, proposed_dot_name)
				graph.add_edge(edge)
				if c.children != []:
					add_edges(c, proposed_dot_name, visibility_level, collapse_decorators)

	add_edges(root, root.name, visibility_level, collapse_decorators)
	return graph

def stringify_dot_tree(root):
	
	graph = generate_pydot_graph(root, visibility_level=common.VisibilityLevel.DETAIL)
	return graph.to_string()

def render_dot_tree(root, visibility_level=py_trees.common.VisibilityLevel.DETAIL, collapse_decorators=False, name=None):

	graph = generate_pydot_graph(root, visibility_level, collapse_decorators)
	filename_wo_extension = root.name.lower().replace(" ", "_") if name is None else name
	#print("Writing %s.dot/svg/png" % filename_wo_extension)
	#graph.write('treeanim' + '.dot')
	# graph.write_png(filename_wo_extension + '.png')
	graph.write_svg(filename_wo_extension + '.svg')
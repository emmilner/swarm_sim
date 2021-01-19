#!/usr/bin/env python

import string
import numpy as np
import logging
import time
import random
import math



class wall(object):

    def __init__(self):

        self.start = np.array([0, 0])
        self.end = np.array([0, 0])
        self.width = 1
        self.hitbox = []


class box(object):

    def __init__(self, h, w, origin):

        self.height = h
        self.width = w
        self.walls = []


        self.walls.append(wall())
        self.walls[0].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[0].end = [origin[0]+(0.5*w), origin[1]+(0.5*h)]

        self.walls.append(wall())
        self.walls[1].start = [origin[0]-(0.5*w), origin[1]-(0.5*h)]; self.walls[1].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

        self.walls.append(wall())
        self.walls[2].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[2].end = [origin[0]-(0.5*w), origin[1]-(0.5*h)]

        self.walls.append(wall())
        self.walls[3].start = [origin[0]+(0.5*w), origin[1]+(0.5*h)]; self.walls[3].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]
        

class corridor(object):

    def __init__(self, h, w, orient, origin):

        self.length = h
        self.width = w
        self.origin = origin
        self.walls = []

        if orient == 'vertical':
        
            self.walls.append(wall())
            self.walls[0].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[0].end = [origin[0]-(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[1].start = [origin[0]+(0.5*w), origin[1]+(0.5*h)]; self.walls[1].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

        if orient == 'horizontal':
        
            self.walls.append(wall())
            self.walls[0].start = [origin[0]-(0.5*h), origin[1]+(0.5*w)]; self.walls[0].end = [origin[0]+(0.5*h), origin[1]+(0.5*w)]

            self.walls.append(wall())
            self.walls[1].start = [origin[0]-(0.5*h), origin[1]-(0.5*w)]; self.walls[1].end = [origin[0]+(0.5*h), origin[1]-(0.5*w)]

class doorway(object):

    def __init__(self, l, doorwidth, orient, origin):

        
        self.walls = []

        if orient == 'vertical':
        
            self.walls.append(wall())
            self.walls[0].start = [origin[0], origin[1]+(0.5*l)]; self.walls[0].end = [origin[0], origin[1]+(0.5*doorwidth)]

            self.walls.append(wall())
            self.walls[1].start = [origin[0], origin[1]-(0.5*doorwidth)]; self.walls[1].end = [origin[0], origin[1]-(0.5*l)]

        if orient == 'horizontal':
        
            self.walls.append(wall())
            self.walls[0].start = [origin[0]-(0.5*l), origin[1]]; self.walls[0].end = [origin[0]-(0.5*doorwidth), origin[1]]

            self.walls.append(wall())
            self.walls[1].start = [origin[0]+(0.5*doorwidth), origin[1]]; self.walls[1].end = [origin[0]+(0.5*l), origin[1]]

class room(object):

    def __init__(self, h, w, doorwidth, orient, origin):

        self.length = h
        self.width = w
        self.origin = origin
        self.walls = []

        if orient == 'top':
        
            self.walls.append(wall())
            self.walls[0].start = [origin[0]-(0.5*w), origin[1]-(0.5*h)]; self.walls[0].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[1].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[1].end = [origin[0]-(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[2].start = [origin[0]+(0.5*w), origin[1]+(0.5*h)]; self.walls[2].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[3].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[3].end = [origin[0]-(0.5*doorwidth), origin[1]+(0.5*h)]

            self.walls.append(wall())
            self.walls[4].start = [origin[0]+(0.5*doorwidth), origin[1]+(0.5*h)]; self.walls[4].end = [origin[0]+(0.5*w), origin[1]+(0.5*h)]

        if orient == 'bottom':
        
            self.walls.append(wall())
            self.walls[0].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[0].end = [origin[0]+(0.5*w), origin[1]+(0.5*h)]

            self.walls.append(wall())
            self.walls[1].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[1].end = [origin[0]-(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[2].start = [origin[0]+(0.5*w), origin[1]+(0.5*h)]; self.walls[2].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[3].start = [origin[0]-(0.5*w), origin[1]-(0.5*h)]; self.walls[3].end = [origin[0]-(0.5*doorwidth), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[4].start = [origin[0]+(0.5*doorwidth), origin[1]-(0.5*h)]; self.walls[4].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

        if orient == 'left':
        
            self.walls.append(wall())
            self.walls[0].start = [origin[0]-(0.5*w), origin[1]-(0.5*h)]; self.walls[0].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[1].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[1].end = [origin[0]+(0.5*w), origin[1]+(0.5*h)]

            self.walls.append(wall())
            self.walls[2].start = [origin[0]+(0.5*w), origin[1]+(0.5*h)]; self.walls[2].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[3].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[3].end = [origin[0]-(0.5*w), origin[1]+(0.5*doorwidth)]

            self.walls.append(wall())
            self.walls[4].start = [origin[0]-(0.5*w), origin[1]-(0.5*doorwidth)]; self.walls[4].end = [origin[0]-(0.5*w), origin[1]-(0.5*h)]

        if orient == 'right':
        
            self.walls.append(wall())
            self.walls[0].start = [origin[0]-(0.5*w), origin[1]-(0.5*h)]; self.walls[0].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[1].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[1].end = [origin[0]+(0.5*w), origin[1]+(0.5*h)]

            self.walls.append(wall())
            self.walls[2].start = [origin[0]-(0.5*w), origin[1]+(0.5*h)]; self.walls[2].end = [origin[0]-(0.5*w), origin[1]-(0.5*h)]

            self.walls.append(wall())
            self.walls[3].start = [origin[0]+(0.5*w), origin[1]+(0.5*h)]; self.walls[3].end = [origin[0]+(0.5*w), origin[1]+(0.5*doorwidth)]

            self.walls.append(wall())
            self.walls[4].start = [origin[0]+(0.5*w), origin[1]-(0.5*doorwidth)]; self.walls[4].end = [origin[0]+(0.5*w), origin[1]-(0.5*h)]



        


        

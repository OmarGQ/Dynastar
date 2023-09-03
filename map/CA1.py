# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 17:14:57 2023

@author: Kiddra
"""
#https://gamedevelopment.tutsplus.com/generate-random-cave-levels-using-cellular-automata--gamedev-9664t
from __future__ import annotations
import numpy as np
import random
import render.tile_types as tile_types
from typing import List, TYPE_CHECKING
from map.game_map import GameMap

if TYPE_CHECKING:
    from engine import Engine

# walls will be 0
# floors will be 1
WALL = 0
FLOOR = 1
fill_prob = 0.4
deadLimit = 4
birthLimit = 5
numberOfSteps = 4

def generate_terrain(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
):
    """Generate a new terrain map."""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    
    shape = (map_width, map_height)
    new_map = np.ones(shape)
    for i in range(shape[0]):
    	for j in range(shape[1]):
    		choice = random.uniform(0, 1)
    		new_map[i][j] = WALL if choice < fill_prob else FLOOR

    # run for 6 generations
    generations = 6
    for generation in range(generations):
    	for i in range(shape[0]):
    		for j in range(shape[1]):
    			# get the number of walls 1 away from each index
    			# get the number of walls 2 away from each index
    			submap = new_map[max(i-1, 0):min(i+2, new_map.shape[0]),max(j-1, 0):min(j+2, new_map.shape[1])]
    			wallcount_1away = len(np.where(submap.flatten() == WALL)[0])
    			submap = new_map[max(i-2, 0):min(i+3, new_map.shape[0]),max(j-2, 0):min(j+3, new_map.shape[1])]
    			wallcount_2away = len(np.where(submap.flatten() == WALL)[0])
    			# this consolidates walls
    			# for first five generations build a scaffolding of walls
    			if generation < 5:
    				# if looking 1 away in all directions you see 5 or more walls
    				# consolidate this point into a wall, if that doesnt happpen
    				# and if looking 2 away in all directions you see less than
    				# 7 walls, add a wall, this consolidates and adds walls
    				if wallcount_1away >= 5 or wallcount_2away <= 7:
    					new_map[i][j] = WALL
    				else:
    					new_map[i][j] = FLOOR
    				if i==0 or j == 0 or i == shape[0]-1 or j == shape[1]-1:
    					new_map[i][j] = WALL 

    			# this consolidates open space, fills in standalone walls,
    			# after generation 5 consolidate walls and increase walking space
    			# if there are more than 5 walls nearby make that point a wall,
    			# otherwise add a floor
    			else:
    				# if looking 1 away in all direction you see 5 walls
    				# consolidate this point into a wall,
    				if wallcount_1away >= 5:
    					new_map[i][j] = WALL
    				else:
    					new_map[i][j] = FLOOR

    return translate(new_map, terrain)

def countAliveNeighbours(map, x, y, shape):
    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            neighbour_x = x+i
            neighbour_y = y+j
            if(i == 0 and j == 0):
                pass
            elif (neighbour_x < 0 or neighbour_y < 0 or neighbour_x >= shape[0] or neighbour_y >= shape[1]):
                count += 1
            elif map[neighbour_x][neighbour_y] == FLOOR:
                count += 1
    return count

def doSimulationStep(oldMap, shape):
    new_map = np.ones(shape)
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            nbs = countAliveNeighbours(oldMap, x, y, shape)
            if oldMap[x][y] == FLOOR:
                if nbs < deadLimit:
                    new_map[x][y] = WALL
                else:
                    new_map[x][y] = FLOOR
            else:
                if nbs > birthLimit:
                    new_map[x][y] = FLOOR
                else:
                    new_map[x][y] = WALL
    return new_map

def generate_terrain_2(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
):
    """Generate a new terrain map."""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    
    shape = (map_width, map_height)
    new_map = np.zeros(shape)
    for i in range(shape[0]):
    	for j in range(shape[1]):
    		choice = random.uniform(0, 1)
    		new_map[i][j] = WALL if choice < fill_prob else FLOOR  
    for i in range(0, numberOfSteps):
        new_map = doSimulationStep(new_map, shape);

    return translate(new_map, terrain)
        
        
def translate(matrix, terrain):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == WALL:
                terrain.tiles[i][j] = tile_types.wall
            else:
                terrain.tiles[i][j] = tile_types.floor
    return terrain
        
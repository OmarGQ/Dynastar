# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 17:17:22 2023

@author: danie
"""
import random
import numpy as np

def display_cave(matrix):
	for i in range(matrix.shape[0]):
		for j in range(matrix.shape[1]):
			char = "#" if matrix[i][j] == WALL else "."
			print(char, end='')
		print()
		
# the cave should be 42x42
shape = (42,42)
l = 42
w =42

# walls will be 0
# floors will be 1
WALL = 0
FLOOR = 1

shape = (42,42)
WALL = 0
FLOOR = 1
fill_prob = 0.4

numberOfSteps = 4
deadLimit = 4
birthLimit = 5

def countAliveNeighbours(map, x, y):
    count = 0
    for i in range(-1,2):
        for j in range(-1,2):
            neighbour_x = x+i
            neighbour_y = y+j
            if(i == 0 and j == 0):
                pass
            elif (neighbour_x < 0 or neighbour_y < 0 or neighbour_x >= l or neighbour_y >= w):
                count += 1
            elif map[neighbour_x][neighbour_y] == FLOOR:
                count += 1
    return count

def doSimulationStep(oldMap):
    new_map = np.ones(shape)
    for x in range(0, l):
        for y in range(0, w):
            nbs = countAliveNeighbours(oldMap, x, y)
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

new_map = np.zeros(shape)
for i in range(shape[0]):
	for j in range(shape[1]):
		choice = random.uniform(0, 1)
		new_map[i][j] = WALL if choice < fill_prob else FLOOR  
for i in range(0, numberOfSteps):
    new_map = doSimulationStep(new_map);

display_cave(new_map)


"""
Place treasure
public void placeTreasure(boolean[][] world){
	//How hidden does a spot need to be for treasure? 
	//I find 5 or 6 is good. 6 for very rare treasure. 
	int treasureHiddenLimit = 5;
	for (int x=0; x < worldWidth; x++){
		for (int y=0; y < worldHeight; y++){
 			if(!world[x][y]){
 				int nbs = countAliveNeighbours(world, x, y);
  				if(nbs >= treasureHiddenLimit){
					placeTreasure(x, y);
				}
			}
		}
	}
}
"""
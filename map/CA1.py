# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 17:14:57 2023

@author: Kiddra
"""

from __future__ import annotations
import numpy as np
import random
import tile_types as tile_types
from typing import TYPE_CHECKING
from map.game_map import GameMap

if TYPE_CHECKING:
    from engine import Engine

fill_prob = 0.4

def CA(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
):
    """Generate a new terrain map."""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    
    """Generate initial random map"""
    shape = (map_width, map_height)
    new_map = np.ones(shape)
    for i in range(shape[0]):
    	for j in range(shape[1]):
    		choice = random.uniform(0, 1)
    		new_map[i][j] = 0 if choice < fill_prob else 1

    """run for 6 generations"""
    generations = 6
    for generation in range(generations):
    	for i in range(shape[0]):
    		for j in range(shape[1]): # Count walls around the cell
    			submap = new_map[max(i-1, 0):min(i+2, new_map.shape[0]),max(j-1, 0):min(j+2, new_map.shape[1])]
    			wallcount_1away = len(np.where(submap.flatten() == 0)[0])
    			submap = new_map[max(i-2, 0):min(i+3, new_map.shape[0]),max(j-2, 0):min(j+3, new_map.shape[1])]
    			wallcount_2away = len(np.where(submap.flatten() == 0)[0])
    			"""for first five generations build a scaffolding of walls"""
    			if generation < 5:
    				if wallcount_1away >= 5 or wallcount_2away <= 7:
    					new_map[i][j] = 0
    				else:
    					new_map[i][j] = 1
    				if i==0 or j == 0 or i == shape[0]-1 or j == shape[1]-1:
    					new_map[i][j] = 0 
    			else:
    				"""For the last generation generate openings"""
    				if wallcount_1away >= 5:
    					new_map[i][j] = 0
    				else:
    					new_map[i][j] = 1

    return translate(new_map, terrain), new_map    
        
def translate(matrix, terrain):
    """Turns the generated terrain into a functional map"""
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 0:
                terrain.tiles[i][j] = tile_types.wall
            else:
                terrain.tiles[i][j] = tile_types.floor
    return terrain
        
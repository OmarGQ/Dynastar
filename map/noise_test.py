# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:41:27 2023

@author: danie
"""
from __future__ import annotations
import numpy as np
import random
from typing import Iterator, Tuple, List, TYPE_CHECKING
import tcod
from game_map import GameMap
import tile_types
from procgen import *

if TYPE_CHECKING:
    from entity import Entity
    
def simplex(
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new terrain map."""
    #"""
    cave = GameMap(map_width, map_height)
    # Set noise
    noise = tcod.noise.Noise(
        dimensions=2,
        algorithm=2,
        implementation=tcod.noise.SIMPLE,
        hurst=0.5,
        lacunarity=3.0,
        octaves=4,
        seed=None,
        )
    ogrid = [np.arange(map_width, dtype=np.float32),
             np.arange(map_height, dtype=np.float32)]

    # Scale the grid.
    ogrid[0] *= 0.20
    ogrid[1] *= 0.20

    # Return the sampled noise from this grid of points.
    samples = noise.sample_ogrid(ogrid)

    cave = GameMap(map_width, map_height)
    for i in range(map_width):
        for j in range(map_height):
            if samples[i][j]<-0.4:
                cave.tiles[i][j] = tile_types.water
            elif samples[i][j]<0.1:
                cave.tiles[i][j] = tile_types.floor
            elif samples[i][j]<.3:
                cave.tiles[i][j] = tile_types.tree
            else:
                 cave.tiles[i][j] = tile_types.wall  
    return cave

def Perlin(
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new terrain map."""
    #"""
    cave = GameMap(map_width, map_height)
    # Set noise
    noise = tcod.noise.Noise(
        dimensions=2,
        algorithm=1,
        implementation=tcod.noise.SIMPLE,
        hurst=0.5,
        lacunarity=3.0,
        octaves=4,
        seed=None,
        )
    ogrid = [np.arange(map_width, dtype=np.float32),
             np.arange(map_height, dtype=np.float32)]

    # Scale the grid.
    ogrid[0] *= 0.20
    ogrid[1] *= 0.20

    # Return the sampled noise from this grid of points.
    samples = noise.sample_ogrid(ogrid)

    cave = GameMap(map_width, map_height)
    for i in range(map_width):
        for j in range(map_height):
            if samples[i][j]<-0.4:
                cave.tiles[i][j] = tile_types.water
            elif samples[i][j]<0.1:
                cave.tiles[i][j] = tile_types.floor
            elif samples[i][j]<.3:
                cave.tiles[i][j] = tile_types.tree
            else:
                 cave.tiles[i][j] = tile_types.wall  
    return cave
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:41:27 2023

@author: Kiddra
"""
from __future__ import annotations
import numpy as np
import tcod
import tile_types
import random
from typing import TYPE_CHECKING
from map.game_map import GameMap

if TYPE_CHECKING:
    from engine import Engine
    
def generate_terrain_old(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
):
    """Generate a new terrain map."""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    # Set noise
    noise = tcod.noise.Noise(
         dimensions=2,
         algorithm=tcod.noise.Algorithm.SIMPLEX)
    # Generate noise grid
    samples = noise[tcod.noise.grid(
        shape=(map_width, map_height), 
        scale = complexity,
        origin=(map_width/2, map_height/2))]
    # Scale grid.
    samples = ((samples + 1.0) * (256 / 2)).astype(np.uint8) 
    # Set tiles
    for i in range(map_width):
        for j in range(map_height):
            if samples[j][i]<40:
                terrain.tiles[i][j] = tile_types.water
            elif samples[j][i]<155:
                terrain.tiles[i][j] = tile_types.floor
            elif samples[j][i]<200:
                terrain.tiles[i][j] = tile_types.tree
    return terrain, samples
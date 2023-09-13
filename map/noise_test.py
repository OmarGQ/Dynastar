# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 11:41:27 2023

@author: danie
"""
from __future__ import annotations
import numpy as np
import tcod
import tile_types
from typing import TYPE_CHECKING
from map.game_map import GameMap

if TYPE_CHECKING:
    from engine import Engine
     
    
    
def Simplex(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
) -> GameMap:
    """Generate a new terrain map."""
    #"""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    # Set noise
    noise = tcod.noise.Noise(
        dimensions=2,
        algorithm=2,
        implementation=tcod.noise.Implementation.SIMPLE,
        hurst=0.5,
        lacunarity=3.0,
        octaves=4,
        seed=None,
        )
    ogrid = [np.arange(map_width, dtype=np.float32),
             np.arange(map_height, dtype=np.float32)]

    # Scale the grid.
    ogrid[0] *= complexity
    ogrid[1] *= complexity

    # Return the sampled noise from this grid of points.
    samples = noise.sample_ogrid(ogrid)

    for i in range(map_width):
        for j in range(map_height):
            if samples[i][j]<-0.7:
                terrain.tiles[i][j] = tile_types.water
            elif samples[i][j]<0.2:
                terrain.tiles[i][j] = tile_types.floor
            elif samples[i][j]<0.5:
                terrain.tiles[i][j] = tile_types.tree
    return terrain, samples

def Perlin(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
) -> GameMap:
    """Generate a new terrain map."""
    #"""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    # Set noise
    noise = tcod.noise.Noise(
        dimensions=2,
        algorithm=1,
        implementation=tcod.noise.Implementation.SIMPLE, #Try TURBULENCE
        hurst=0.5,
        lacunarity=3.0,
        octaves=4,
        seed=None,
        )
    ogrid = [np.arange(map_width, dtype=np.float32),
             np.arange(map_height, dtype=np.float32)]

    # Scale the grid.
    ogrid[0] *= complexity
    ogrid[1] *= complexity

    # Return the sampled noise from this grid of points.
    samples = noise.sample_ogrid(ogrid)

    for i in range(map_width):
        for j in range(map_height):
            if samples[i][j]<-0.3:
                terrain.tiles[i][j] = tile_types.water
            elif samples[i][j]<0.1:
                terrain.tiles[i][j] = tile_types.floor
            elif samples[i][j]<0.3:
                terrain.tiles[i][j] = tile_types.tree
    return terrain , samples

def Wavelet(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
) -> GameMap:
    """Generate a new terrain map."""
    #"""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    # Set noise
    noise = tcod.noise.Noise(
        dimensions=2,
        algorithm=4,
        implementation=tcod.noise.Implementation.SIMPLE,
        hurst=0.5,
        lacunarity=3.0,
        octaves=4,
        seed=None,
        )
    ogrid = [np.arange(map_width, dtype=np.float32),
             np.arange(map_height, dtype=np.float32)]

    # Scale the grid.
    ogrid[0] *= complexity
    ogrid[1] *= complexity

    # Return the sampled noise from this grid of points.
    samples = noise.sample_ogrid(ogrid)

    for i in range(map_width):
        for j in range(map_height):
            if samples[i][j]<-0.7:
                terrain.tiles[i][j] = tile_types.water
            elif samples[i][j]<0.09:
                terrain.tiles[i][j] = tile_types.floor
            elif samples[i][j]<0.2:
                terrain.tiles[i][j] = tile_types.tree
    return terrain , samples
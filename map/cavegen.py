# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 14:31:36 2023

@author: Kiddra
"""

from __future__ import annotations
import numpy as np
import random
import tcod
import tile_types
from perlin_noise import PerlinNoise
from perlin_numpy import generate_perlin_noise_2d, generate_fractal_noise_2d
from typing import List, TYPE_CHECKING
from map.game_map import GameMap
from map.procgen import RectangularRoom, tunnel_between, place_entities

if TYPE_CHECKING:
    from engine import Engine

def generate_terrain(
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
    """
    noise = tcod.noise.Noise(
        dimensions=2,
        algorithm=4,
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

    cave = GameMap(map_width, map_height, entities=[player]))
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
    """
    return terrain, samples

def generate_terrain_2(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
):
    """Generate a new terrain map."""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    # Set noise
    noise1 = PerlinNoise(octaves=3*complexity+3)
    noise2 = PerlinNoise(octaves=6*complexity+6)
    noise3 = PerlinNoise(octaves=12*complexity+12)
    noise4 = PerlinNoise(octaves=24*complexity+24)

    xpix, ypix = map_height, map_width
    noise = []
    for i in range(xpix):
        row = []
        for j in range(ypix):
            noise_val = noise1([i/xpix, j/ypix])
            noise_val += 0.5 * noise2([i/xpix, j/ypix])
            noise_val += 0.25 * noise3([i/xpix, j/ypix])
            noise_val += 0.125 * noise4([i/xpix, j/ypix])

            row.append(noise_val)
        noise.append(row)   
    samples = np.array(noise)
    samples = ((samples + 1.0) * (256 / 2)).astype(np.uint8)
    for i in range(map_width):
        for j in range(map_height):
            if samples[j][i]<90:
                terrain.tiles[i][j] = tile_types.water
            elif samples[j][i]<135:
                terrain.tiles[i][j] = tile_types.floor
            elif samples[j][i]<145:
                terrain.tiles[i][j] = tile_types.tree
    return terrain, samples

def generate_terrain_3(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float
):
    """Generate a new terrain map."""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    # Set noise
    noise = generate_fractal_noise_2d((100, 100), (5, 5), 3)
    # Scale grid.
    samples = ((noise + 1.0) * (256 / 2)).astype(np.uint8) 
    # Set tiles
    for i in range(map_width):
        for j in range(map_height):
            if samples[j][i]<40:
                terrain.tiles[i][j] = tile_types.water
            elif samples[j][i]<145:
                terrain.tiles[i][j] = tile_types.floor
            elif samples[j][i]<170:
                terrain.tiles[i][j] = tile_types.tree
    return terrain, samples

def generate_rooms(
    dungeon: GameMap,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate a new dungeon map."""
    rooms: List[RectangularRoom] = []
    center_of_last_room = (0, 0)
    player = dungeon.engine.player
    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)
        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.

        # Clear out the room's inner area.
        dungeon.tiles[new_room.area] = tile_types.wall
        if len(rooms) == 0: # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  #Place enemies and items
            place_entities(new_room, dungeon, engine.game_world.current_floor) 
        rooms.append(new_room) # Append the new room to the list.
        
    """ Make a tunnel between this rooms"""
    i = 0
    while True:
        if rooms[i] == rooms[-1]:
            break
        for x, y in tunnel_between(rooms[i].center, rooms[i+1].center):
            dungeon.tiles[x, y] = tile_types.floor
        i += 1
    """Replaces the room's floor"""
    for room in rooms:
        dungeon.tiles[room.inner] = tile_types.room_floor
    """Places the exit"""
    center_of_last_room = rooms[-1].center
    dungeon.tiles[center_of_last_room] = tile_types.down_stairs
    dungeon.downstairs_location = center_of_last_room
        
    return dungeon
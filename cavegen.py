# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 14:31:36 2023

@author: Kiddra
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

def generate_terrain(
    map_width: int,
    map_height: int,
    player: Entity
):
    """Generate a new terrain map."""
    #"""
    #terrain = GameMap(map_width, map_height)
    terrain = GameMap(map_width, map_height, entities=[player])
    # Set noise
    noise = tcod.noise.Noise(
         dimensions=2,
         algorithm=tcod.noise.Algorithm.SIMPLEX)
    # Generate noise grid
    samples = noise[tcod.noise.grid(
        shape=(map_width, map_height), 
        scale=0.25, 
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

def generate_rooms(
    dungeon: GameMap,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    max_monsters_per_room: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    """Generate a new dungeon map."""
    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        # "RectangularRoom" class makes rectangles easier to work with
        new_room = RectangularRoom(x, y, room_width, room_height)

        # Run through the other rooms and see if they intersect with this one.
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue  # This room intersects, so go to the next attempt.
        # If there are no intersections then the room is valid.

        # Clear out the room's inner area.
        dungeon.tiles[new_room.area] = tile_types.wall
        #dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0: # The first room, where the player starts.
            player.x, player.y = new_room.center
        else:  # Make a tunnel between this room and the previous one.
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor
        #Place enemies
        place_entities(new_room, dungeon, max_monsters_per_room)
        
        rooms.append(new_room) # Append the new room to the list.
    for room in rooms:
        dungeon.tiles[room.inner] = tile_types.room_floor
    x, y = rooms[-1].center
    dungeon.tiles[x][y] = tile_types.goal
    return dungeon

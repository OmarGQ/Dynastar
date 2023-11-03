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
from typing import List, TYPE_CHECKING
from map.game_map import GameMap
from map.procgen import RectangularRoom, tunnel_between, place_entities_room, place_entities

if TYPE_CHECKING:
    from engine import Engine

#algorithm, implementation, lacunarity, octaves, map values
parameters = {
    "Simplex": [2, tcod.noise.Implementation.SIMPLE, 8, 8, [-0.8, 0.2, 0.5]],
    "Perlin":  [1, tcod.noise.Implementation.FBM, 3, 4, [-0.47, 0.1, 0.3]],
    "Wavelet": [4, tcod.noise.Implementation.TURBULENCE, 3, 2, [-1, 0.4, 0.7]]
    }

def generate_terrain(
    map_width: int,
    map_height: int,
    engine: Engine,
    complexity: float,
    version: str,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
) -> GameMap:
    """Generate a new GameMap."""
    player = engine.player
    terrain = GameMap(engine, map_width, map_height, entities=[player])
    
    if version == "Dungeon":
        return generate_rooms_dungeon(
            dungeon = terrain,
            max_rooms = max_rooms,
            room_min_size = room_min_size,
            room_max_size = room_max_size,
            map_width = map_width,
            map_height = map_height,
            engine = engine
        )
    elif version == "Cave":
        sample = CA(map_width, map_height)
        sample, rooms = locate_rooms(terrain, max_rooms, room_min_size, room_max_size, map_width, map_height, engine, sample)
        lis = rooms.copy()
        sample = path_generation(terrain, lis, sample, [1,-0.5])
        cave = translate_CA(sample, terrain)
        cave = populate_rooms(terrain, rooms)
        place_entities(cave, engine.game_world.current_floor, 5, 2)
        return cave
       
    else:
        values = parameters[version]
        tile_v = values[4]
    """Noise function"""
    noise = tcod.noise.Noise(
        dimensions=2,
        algorithm=values[0],
        implementation=values[1],
        hurst=0.5,
        lacunarity=values[2],
        octaves=values[3],
        seed=None,
        )
    ogrid = [np.arange(map_width, dtype=np.float32),
             np.arange(map_height, dtype=np.float32)]

    """"Scale the grid"""
    ogrid[0] *= complexity
    ogrid[1] *= complexity

    """Sample noise from this grid of points"""
    samples = noise.sample_ogrid(ogrid)
    """Allocate rooms"""
    samples, rooms = locate_rooms(terrain, max_rooms, room_min_size, room_max_size, map_width, map_height, engine, samples)
    """Generate paths"""
    lis = rooms.copy()
    samples = path_generation(terrain, lis, samples, [0, tile_v[1]])
    """Set tiles"""
    terrain = Set_tiles(terrain, map_width, map_height, tile_v, samples)
    """Set and populate rooms"""
    terrain = populate_rooms(terrain, rooms)
    """Populate gamemap"""
    place_entities(terrain, engine.game_world.current_floor, 1, 3)
    return terrain

def locate_rooms(dungeon: GameMap,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
    noise
):
    """Identify plane areas to set rooms"""
    rooms: List[RectangularRoom] = []
    player = dungeon.engine.player
    while(len(rooms) < 3):
        for r in range(max_rooms):
            room_width = random.randint(room_min_size, room_max_size)
            room_height = random.randint(room_min_size, room_max_size)
    
            x = random.randint(2, dungeon.width - room_width - 3)
            y = random.randint(2, dungeon.height - room_height - 3)
    
            new_room = RectangularRoom(x, y, room_width, room_height)
            # Run through the other rooms and see if they intersect with this one.
            if any(new_room.intersects(other_room) for other_room in rooms):
                continue  # This room intersects, so go to the next attempt.

            mean = np.average(noise[new_room.area])
            if mean > 0.1 and mean < 0.6:
                #Reduce the value of adjacent tiles, increasing the posibility of open spaceses
                noise[new_room.sourindingd_area] *= 0.7
                noise[new_room.area] = 3
                noise[new_room.inner] = 2
                if len(rooms) == 0: # The first room, where the player starts.
                    player.place(*new_room.center, dungeon)
                rooms.append(new_room) # Append the new room to the list.
    return noise, rooms

def path_generation(dungeon: GameMap, rooms: np.array, noise, tiles, flag = False, door = None, start = None):
    """Clear the path to get out and into the rooms"""
    midX = int(dungeon.width/2)
    midY = int(dungeon.height/2)
    clear = 0
    distance = 0
    room = rooms.pop(0)
    if door == None and start == None:
        door, start, d2, s2 = Select_direction2(dungeon, room, noise)
    for x, y in tunnel_between(start, [midX, midY]):
        if clear == 7:
            break
        if (noise[x, y] > tiles[1] and noise[x, y] < 1.1):
            noise[x, y] = tiles[0]
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if noise[x+j, y+k] != 3 and noise[x+j, y+k] != 2:
                        if tiles[0] == 1 and random.random() > 0.5:
                            noise[x+j, y+k] = 1
                        else:
                            noise[x+j, y+k] *= 0.7
            clear = 0
        clear += 1
        distance += 1
    noise[door] = tiles[0]
    if (distance < 15 or random.random() < 0.4) and flag ==False:
        noise = path_generation(dungeon, [room], noise, tiles, True, d2, s2)
    if len(rooms) == 0:
        return noise
    else:
        return path_generation(dungeon, rooms, noise, tiles, True)

def Select_direction(dungeon: GameMap, room, noise):
    midX = int(dungeon.width/2)
    midY = int(dungeon.height/2)
    center = room.center
    if center[1] < midY:
        if center[0] < midX : #Top left
            if noise[center[0], room.y2+1] < 0.4:
                door = (center[0], room.y2-1) #bottom
                start = (center[0], room.y2) #bottom
                door2 = (room.x2-1, center[1]) #right
                start2 = (room.x2, center[1]) #right
            else:
                door = (room.x2-1, center[1]) #right
                start = (room.x2, center[1]) #right
                door2 = (center[0], room.y2-1) #bottom
                start2 = (center[0], room.y2) #bottom
        else: #Top right
            if noise[center[0], room.y2+1] < 0.4:
                door = (center[0], room.y2-1) #bottom
                start = (center[0], room.y2)
                door2 = (room.x1, center[1]) #left
                start2 = (room.x1-1, center[1]) #left
            else:
                door = (room.x1, center[1]) #left
                start = (room.x1-1, center[1]) #left
                door2 = (center[0], room.y2-1) #bottom
                start2 = (center[0], room.y2)
    else:
        if center[0] < midX:  #Bottom left
            if noise[center[0], room.y1-1] < 0.4:
                door = (center[0], room.y1) #top
                start = (center[0], room.y1-1) #top
                door2 = (room.x2-1, center[1]) #right
                start2 = (room.x2, center[1]) #right
            else:
                door = (room.x2-1, center[1]) #right
                start = (room.x2, center[1]) #right
                door2 = (center[0], room.y1) #top
                start2 = (center[0], room.y1-1) #top
        else: #Bottom right
            if noise[center[0], room.y1-1] < 0.4:
                door = (center[0], room.y1) #top
                start = (center[0], room.y1-1) #top
                door2 = (room.x1, center[1]) #left
                start2 = (room.x1-1, center[1]) #left
            else:
                door = (room.x1, center[1]) #left
                start = (room.x1-1, center[1]) #left
                door2 = (center[0], room.y1) #top
                start2 = (center[0], room.y1-1) #top
    return door, start, door2, start2

def Select_direction2(dungeon: GameMap, room, noise):
    thirdX = int(dungeon.width/3)
    thirdY = int(dungeon.height/3)
    center = room.center
    if center[1] < thirdY:
        if center[0] < thirdX: #Top left
            if noise[center[0], room.y2+1] < 0.4:
                door = (center[0], room.y2-1) #bottom
                start = (center[0], room.y2) #bottom
                door2 = (room.x2-1, center[1]) #right
                start2 = (room.x2, center[1]) #right
            else:
                door = (room.x2-1, center[1]) #right
                start = (room.x2, center[1]) #right
                door2 = (center[0], room.y2-1) #bottom
                start2 = (center[0], room.y2) #bottom
        elif center[0] > thirdX*2: #Top right
            if noise[center[0], room.y2+1] < 0.4:
                door = (center[0], room.y2-1) #bottom
                start = (center[0], room.y2)
                door2 = (room.x1, center[1]) #left
                start2 = (room.x1-1, center[1]) #left
            else:
                door = (room.x1, center[1]) #left
                start = (room.x1-1, center[1]) #left
                door2 = (center[0], room.y2-1) #bottom
                start2 = (center[0], room.y2)
        else:
            door = (center[0], room.y2-1) #bottom
            start = (center[0], room.y2) #bottom
            door2 = (center[0], room.y2-1) #bottom
            start2 = (center[0], room.y2) #bottom
    elif center[1] > thirdY*2:
        if center[0] < thirdX:  #Bottom left
            if noise[center[0], room.y1-1] < 0.4:
                door = (center[0], room.y1) #top
                start = (center[0], room.y1-1) #top
                door2 = (room.x2-1, center[1]) #right
                start2 = (room.x2, center[1]) #right
            else:
                door = (room.x2-1, center[1]) #right
                start = (room.x2, center[1]) #right
                door2 = (center[0], room.y1) #top
                start2 = (center[0], room.y1-1) #top
        elif center[0] > thirdX*2: #Bottom right
            if noise[center[0], room.y1-1] < 0.4:
                door = (center[0], room.y1) #top
                start = (center[0], room.y1-1) #top
                door2 = (room.x1, center[1]) #left
                start2 = (room.x1-1, center[1]) #left
            else:
                door = (room.x1, center[1]) #left
                start = (room.x1-1, center[1]) #left
                door2 = (center[0], room.y1) #top
                start2 = (center[0], room.y1-1) #top
        else:
            door = (center[0], room.y1) #top
            start = (center[0], room.y1-1) #top
            door2 = (center[0], room.y1) #top
            start2 = (center[0], room.y1-1) #top
    else:
        if center[0] < thirdX:  #Bottom left
            door = (room.x2-1, center[1]) #right
            start = (room.x2, center[1]) #right
            door2 = (room.x2-1, center[1]) #right
            start2 = (room.x2, center[1]) #right

        elif center[0] > thirdX*2: #Bottom right
            door = (room.x1, center[1]) #left
            start = (room.x1-1, center[1]) #left
            door2 = (room.x1, center[1]) #left
            start2 = (room.x1-1, center[1]) #left
        else:
            if noise[center[0], room.y2+1] < 0.4:
                door = (center[0], room.y2-1) #bottom
                start = (center[0], room.y2) #bottom
                door2 = (room.x2-1, center[1]) #right
                start2 = (room.x2, center[1]) #right
            else:
                door = (center[0], room.y1) #top
                start = (center[0], room.y1-1) #top
                door2 = (room.x1, center[1]) #left
                start2 = (room.x1-1, center[1]) #left
    return door, start, door2, start2
                
def Set_tiles(
    dungeon: GameMap,
    map_width: int,
    map_height: int,
    tiles,
    samples) -> GameMap:
    """Set tiles"""
    for i in range(map_width):
        for j in range(map_height):
            if samples[i][j]<tiles[0]:
                dungeon.tiles[i][j] = tile_types.water
            elif samples[i][j]<tiles[1]:
                dungeon.tiles[i][j] = tile_types.floor
            elif samples[i][j]<tiles[2]:
                dungeon.tiles[i][j] = tile_types.tree
            elif samples[i][j]==3:
                dungeon.tiles[i][j] = tile_types.room_wall
            elif samples[i][j]==2:
                dungeon.tiles[i][j] = tile_types.room_floor
    return dungeon
    
def populate_rooms(
    dungeon: GameMap,
    rooms: np.array
) -> GameMap:
    """Set entities"""
    for r in rooms:
        if rooms[0] != r: # The first room, where the player starts.
            place_entities_room(r, dungeon, dungeon.engine.game_world.current_floor)
    """Places the exit"""
    center_of_last_room = rooms[-1].center
    dungeon.tiles[center_of_last_room] = tile_types.down_stairs
    dungeon.downstairs_location = center_of_last_room
        
    return dungeon

def CA(
    map_width: int,
    map_height: int
):
    fill_prob = 0.4  
    """Generate initial random map"""
    shape = (map_width, map_height)
    sample = np.ones(shape)
    for i in range(shape[0]):
    	for j in range(shape[1]):
    		choice = random.uniform(0, 1)
    		sample[i][j] = 0 if choice < fill_prob else 1

    """run for 6 generations"""
    generations = 6
    for generation in range(generations):
    	for i in range(shape[0]):
    		for j in range(shape[1]): # Count walls around the cell
    			submap = sample[max(i-1, 0):min(i+2, sample.shape[0]),max(j-1, 0):min(j+2, sample.shape[1])]
    			wallcount_1away = len(np.where(submap.flatten() == 0)[0])
    			submap = sample[max(i-2, 0):min(i+3, sample.shape[0]),max(j-2, 0):min(j+3, sample.shape[1])]
    			wallcount_2away = len(np.where(submap.flatten() == 0)[0])
    			"""for first five generations build a scaffolding of walls"""
    			if generation < 5:
    				if wallcount_1away >= 5 or wallcount_2away <= 7:
    					sample[i][j] = 0
    				else:
    					sample[i][j] = 1
    				if i==0 or j == 0 or i == shape[0]-1 or j == shape[1]-1:
    					sample[i][j] = 0 
    			else:
    				"""For the last generation generate openings"""
    				if wallcount_1away >= 5:
    					sample[i][j] = 0
    				else:
    					sample[i][j] = 1
    return sample
        
def translate_CA(matrix, terrain):
    """Turns the generated CA terrain into a functional map"""
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == 0 or matrix[i][j] == 1.1:
                terrain.tiles[i][j] = tile_types.wall
            elif matrix[i][j] == 2:
                terrain.tiles[i][j] = tile_types.room_floor
            elif matrix[i][j] == 3:
                terrain.tiles[i][j] = tile_types.room_wall
            else:
                terrain.tiles[i][j] = tile_types.floor
    return terrain

def generate_rooms_dungeon(
    dungeon: GameMap,
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    engine: Engine,
) -> GameMap:
    """Generate rooms for a dungeon"""
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

        dungeon.tiles[new_room.area] = tile_types.wall
        if len(rooms) == 0: # The first room, where the player starts.
            player.place(*new_room.center, dungeon)
        else:  #Place enemies and items
            place_entities_room(new_room, dungeon, engine.game_world.current_floor) 
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
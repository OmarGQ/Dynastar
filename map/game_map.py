# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:17:40 2023

@author: kiddra
"""

from __future__ import annotations
from typing import Iterable, Iterator, Optional, TYPE_CHECKING, List, Tuple
import numpy as np
from tcod.console import Console
from entity import Actor, Item
import tile_types
import random

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

"""(level, Min, Max, Rooms)"""
room_size_by_floor = [
    (1, 9, 13, 7),
    (3, 7, 11, 7),
    (5, 7, 10, 8),
    (7, 7, 9, 10),
    (9, 7, 8, 12)
]

generation = ["Perlin", "Simplex", "Wavelet", "Dungeon", "Cave"] 

class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Iterable[Entity] = ()):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = set(entities)
        self.tiles = np.full((width, height), fill_value=tile_types.wall, order="F")
        self.visible = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player can currently see
        self.explored = np.full(
            (width, height), fill_value=False, order="F"
        )  # Tiles the player has seen before
        self.downstairs_location = (0, 0)
    
    @property
    def gamemap(self) -> GameMap:
        return self

    @property
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (
            entity
            for entity in self.entities
            if isinstance(entity, Actor) and entity.is_alive
        )
    
    @property
    def items(self) -> Iterator[Item]:
        yield from (entity for entity in self.entities if isinstance(entity, Item))

    def get_blocking_entity_at_location(
        self, location_x: int, location_y: int,) -> Optional[Entity]:
        for entity in self.entities:
            if (entity.blocks_movement and entity.x == location_x and entity.y == location_y):
                return entity
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.rgb[0:self.width, 0:self.height] = self.tiles["light"]
        """
        Renders the map.
 
        If a tile is in the "visible" array, then draw it with the "light" colors.
        If it isn't, but it's in the "explored" array, then draw it with the "dark" colors.
        Otherwise, the default is "SHROUD".
        """
        """
        console.tiles_rgb[0 : self.width, 0 : self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD,
        )
        """
        # Set entities
        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda x: x.render_order.value
        )
        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(
                    x=entity.x, y=entity.y, string=entity.char, fg=entity.color
                )
    
    def get_actor_at_location(self, x: int, y: int) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None
    
class GameWorld:
    """
    Holds the settings for the GameMap, and generates new maps when moving down the stairs.
    """
    def __init__(
        self,
        *,
        engine: Engine,
        map_width: int,
        map_height: int,
        current_floor: int = 0,
    ):
        self.engine = engine

        self.map_width = map_width
        self.map_height = map_height

        self.max_rooms = 7

        self.room_min_size = 0
        self.room_max_size = 0

        self.current_floor = current_floor
        self.complexity = 0.10

    def generate_floor(self) -> None:
        from map.levelgen import generate_terrain
        
        self.current_floor += 1
        if self.complexity < 0.25:
            self.complexity += 0.01
        self.room_min_size, self.room_max_size, self.max_rooms = get_size_values(room_size_by_floor, self.current_floor)
        extra = 1
        version = random.choice(generation)
        
        if version == "Dungeon":
            extra = 1.5
        elif version == "Cave":
            self.room_min_size = 9
            self.room_max_size = 13
            self.max_rooms = 3
            
        self.engine.game_map = generate_terrain(
            map_width = self.map_width,
            map_height = self.map_height,
            engine = self.engine,
            complexity = self.complexity,
            version = version,
            max_rooms = int(self.max_rooms * extra),
            room_min_size = int(self.room_min_size * extra),
            room_max_size = int(self.room_max_size * extra),
        )
        
def get_size_values(
    weighted_chances_by_floor: List[Tuple[int, int, int, int]], floor: int
 ) -> int:
    current_min = 0
    current_max = 0
    current_rooms = 7

    for floor_minimum, min_value, max_value, rooms in weighted_chances_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_min = min_value
            current_max = max_value
            current_rooms = rooms
    return current_min, current_max, current_rooms
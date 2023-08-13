# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:41:16 2023

@author: Kiddra
"""

from __future__ import annotations
from typing import Dict, List, Iterator, Tuple, TYPE_CHECKING
from game_map import GameMap
import random
import tcod
import entity_factories

if TYPE_CHECKING:
    from entity import Entity
    
"""(Floor, Quantity)"""
max_items_by_floor = [
    (1, 2),
    (4, 3),
]

"""(Floor, Quantity)"""
max_monsters_by_room = [
    (1, 3),
    (4, 4),
    (6, 5),
]

"""Floor: (Item, Probability)"""
item_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.health_potion, 25), (entity_factories.axe, 5), 
        (entity_factories.mace, 5), (entity_factories.chain_mail, 5)],
    2: [(entity_factories.confusion_scroll, 10)],
    3: [(entity_factories.axe, 0), (entity_factories.breast_plate, 5), 
        (entity_factories.plate_armor, 5)],
    4: [(entity_factories.lightning_scroll, 25), (entity_factories.sword, 5), 
        (entity_factories.health_potion, 25)],
    6: [(entity_factories.fireball_scroll, 25), (entity_factories.chain_mail, 0), 
        (entity_factories.long_sword, 5)],
    8: [(entity_factories.scale_armor, 5), (entity_factories.mace, 0),
        (entity_factories.breast_plate, 0)]
}

"""Floor: (Enemy, Probability)"""
enemy_chances: Dict[int, List[Tuple[Entity, int]]] = {
    0: [(entity_factories.skeleton, 40), (entity_factories.zombie, 40), (entity_factories.orc, 20)],
    1: [(entity_factories.orc, 60), (entity_factories.zombie, 20), (entity_factories.skeleton, 20)],
    3: [(entity_factories.troll, 15)],
    4: [(entity_factories.kobold, 25)],
    5: [(entity_factories.troll, 30)],
    7: [(entity_factories.troll, 60)],
}

def get_max_value_for_floor(
    weighted_chances_by_floor: List[Tuple[int, int]], floor: int
 ) -> int:
    current_value = 0

    for floor_minimum, value in weighted_chances_by_floor:
        if floor_minimum > floor:
            break
        else:
            current_value = value

    return current_value

def get_entities_at_random(
    weighted_chances_by_floor: Dict[int, List[Tuple[Entity, int]]],
    number_of_entities: int,
    floor: int,
 ) -> List[Entity]:
    entity_weighted_chances = {}

    for key, values in weighted_chances_by_floor.items():
        if key > floor:
            break
        else:
            for value in values:
                entity = value[0]
                weighted_chance = value[1]
                entity_weighted_chances[entity] = weighted_chance

    entities = list(entity_weighted_chances.keys())
    entity_weighted_chance_values = list(entity_weighted_chances.values())
    chosen_entities = random.choices(entities, weights=entity_weighted_chance_values, k=number_of_entities)
    return chosen_entities

class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property #Returns center of the room
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property #Returns two “slices”, which represent the inner portion of the room
    def inner(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1 + 1, self.x2-1), slice(self.y1 + 1, self.y2-1)
    
    @property #Returns two “slices”, which represent the inner portion of the room
    def area(self) -> Tuple[slice, slice]:
        """Return the inner area of this room as a 2D array index."""
        return slice(self.x1, self.x2), slice(self.y1, self.y2)
    
    #Detects if two rooms overlap
    def intersects(self, other: RectangularRoom) -> bool:
        """Return True if this room overlaps with another RectangularRoom."""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )
    
def place_entities(room: RectangularRoom, dungeon: GameMap, floor_number: int,) -> None:
    number_of_monsters = random.randint(
        0, get_max_value_for_floor(max_monsters_by_room, floor_number)
    )
    number_of_items = random.randint(
        0, get_max_value_for_floor(max_items_by_floor, floor_number)
    )
    
    monsters: List[Entity] = get_entities_at_random(enemy_chances, number_of_monsters, floor_number)
    items: List[Entity] = get_entities_at_random(item_chances, number_of_items, floor_number)
    
    for entity in monsters + items:
        x = random.randint(room.x1 + 1, room.x2 - 2)
        y = random.randint(room.y1 + 1, room.y2 - 2)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity.spawn(dungeon, x, y)
    
def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    """Return an L-shaped tunnel between these two points."""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance.
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

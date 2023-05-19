# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:15:47 2023

@author: Kiddra
"""
import tcod
from engine import Engine
from input_handlers import EventHandler
from entity import Entity
from procgen import generate_dungeon
from cavegen import generate_terrain, generate_rooms
from noise_test import *


def main() -> None:
    screen_width = 80
    screen_height = 50
    
    map_width = 80
    map_height = 45
    
    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        #"index.png", 6, 8, tcod.tileset.CHARMAP_TCOD
    )

    event_handler = EventHandler()
    
    player = Entity(int(screen_width / 2), int(screen_height / 2), "@", (255, 0, 0))
    #npc = Entity(int(screen_width / 2 - 5), int(screen_height / 2), " ", (255, 255, 0))
    entities = {player}
    """
    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player
    )
    """
    #"""
    game_map, noise = generate_terrain(
        map_width=map_width,
        map_height=map_height
    )
    game_map = generate_rooms(
        dungeon=game_map,
        max_rooms=4,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player)
    """
    game_map = Perlin(
        map_width=map_width,
        map_height=map_height,
        player=player
    )
    """
    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)
    
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Dungeon gen",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            engine.render(console=root_console, context=context)
            events = tcod.event.wait()
            engine.handle_events(events)

if __name__ == "__main__":
    main()
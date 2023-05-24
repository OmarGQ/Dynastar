# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:15:47 2023

@author: Kiddra
"""
import tcod
import copy
import entity_factories
import colors
from engine import Engine
#from procgen import generate_dungeon
from cavegen import generate_terrain, generate_rooms
from noise_test import *


def main() -> None:
    screen_width = 80
    screen_height = 50
    
    map_width = 80
    map_height = 43
    
    room_max_size = 10
    room_min_size = 6
    max_rooms = 5
    
    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        #"index.png", 6, 8, tcod.tileset.CHARMAP_TCOD
    )
    
    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)

    """
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )
    """
    engine.game_map, noise = generate_terrain(
        map_width=map_width,
        map_height=map_height,
        engine=engine
    )
    engine.game_map = generate_rooms(
        dungeon=engine.game_map,
        max_rooms = max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        max_monsters_per_room = max_monsters_per_room,
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
    engine.update_fov()
    
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", colors.welcome_text
    )
    
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Dungeon gen",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)
            engine.event_handler.handle_events(context)

if __name__ == "__main__":
    main()
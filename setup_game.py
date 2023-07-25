# -*- coding: utf-8 -*-
"""
Created on Sun May 28 08:46:37 2023

@author: kiddra
"""

from __future__ import annotations

import copy
from typing import Optional

import tcod
import lzma
import pickle
import traceback
import colors
import entity_factories
import input_handlers
import winsound
from engine import Engine
from game_map import GameWorld
from cavegen import generate_terrain, generate_rooms


# Load the background image and remove the alpha channel.
background_image = tcod.image.load("images/menu_background.png")[:, :, :3]

def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 90
    map_height = 61

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)
    
    engine.game_world = GameWorld(
        engine=engine,
        map_width=map_width,
        map_height=map_height
    )

    engine.game_world.generate_floor()
    engine.update_fov()
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to yet another dungeon!", colors.welcome_text
    )
    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)
    
    winsound.PlaySound("Music/Exploration.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
    
    return engine

def load_game(filename: str) -> Engine:
    """Load an Engine instance from a file."""
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    winsound.PlaySound("Music/Exploration.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
    return engine

class MainMenu(input_handlers.BaseEventHandler):
    """Handle the main menu rendering and input."""
    winsound.PlaySound("Music/Menu.wav", winsound.SND_LOOP + winsound.SND_ASYNC)
    def on_render(self, console: tcod.Console) -> None:
        """Render the main menu on a background image."""
        console.draw_semigraphics(background_image, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "DYNASTAR",
            fg=colors.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Kiddra",
            fg=colors.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        for i, text in enumerate(
            ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        ):
            console.print(
                console.width // 2,
                console.height // 2 - 2 + i,
                text.ljust(menu_width),
                fg=colors.menu_text,
                bg=colors.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[input_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            winsound.PlaySound(None, 0)
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return input_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return input_handlers.PopupMessage(self, "No saved game to load.")
            except Exception as exc:
                traceback.print_exc()  # Print to stderr.
                return input_handlers.PopupMessage(self, f"Failed to load save:\n{exc}")
        elif event.sym == tcod.event.K_n:
            winsound.PlaySound(None, 0)
            return input_handlers.MainGameEventHandler(new_game())

        return None
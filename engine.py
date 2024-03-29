# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:59:20 2023

@author: Kiddra
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from tcod.console import Console
from tcod.map import compute_fov
from message_log import MessageLog
import exceptions
import lzma
import pickle
import render.render_functions as render_functions

if TYPE_CHECKING:
    from entity import Actor
    from map.game_map import GameMap, GameWorld

class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible
            
    def render(self, console: Console) -> None:
        # Render map
        self.game_map.render(console)
        # Render interface
        self.message_log.render(console=console, x=1, y=62, width=70, height=7)
        
        render_functions.render_ui(
            console=console,
            player=self.player,
            world=self.game_world
            )
        
        render_functions.render_names_at_mouse_location(
            console=console, x=92, y=40, engine=self
        )
        
        render_functions.render_names_at_player_location(
            console=console, x=92, y=44, engine=self
        )
        
    def save_as(self, filename: str) -> None:
        """Save this Engine instance as a compressed file."""
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
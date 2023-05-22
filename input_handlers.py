# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:34:05 2023

@author: Kiddra
"""

from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from actions import Action, BumpAction, EscapeAction
import tcod.event

if TYPE_CHECKING:
   from engine import Engine

class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self) -> None:
        for event in tcod.event.wait():
            action = self.dispatch(event)

            if action is None:
                continue

            action.perform()

            self.engine.handle_enemy_turns()
            self.engine.update_fov()  # Update the FOV before the players next action.

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        if key == tcod.event.K_w:
            action = BumpAction(player, dx=0, dy=-1)
        elif key == tcod.event.K_s:
            action = BumpAction(player, dx=0, dy=1)
        elif key == tcod.event.K_a:
            action = BumpAction(player, dx=-1, dy=0)
        elif key == tcod.event.K_d:
            action = BumpAction(player, dx=1, dy=0)
        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction(player)
        # No valid key was pressed
        return action
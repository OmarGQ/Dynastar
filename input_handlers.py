# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:34:05 2023

@author: Kiddra
"""

from typing import Optional
from actions import Action, BumpAction, EscapeAction
import tcod.event



class EventHandler(tcod.event.EventDispatch[Action]):
    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym

        if key == tcod.event.K_w:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.K_s:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.K_a:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.K_d:
            action = BumpAction(dx=1, dy=0)

        elif key == tcod.event.K_ESCAPE:
            action = EscapeAction()

        # No valid key was pressed
        return action
# -*- coding: utf-8 -*-
"""
Created on Sat May 20 19:53:48 2023

@author: Kiddra
"""

from entity import Entity

player = Entity(char="@", color=(255, 0, 0), name="Player", blocks_movement=True)

orc = Entity(char="o", color=(0, 255, 145), name="Orc", blocks_movement=True)
troll = Entity(char="T", color=(0, 102, 58), name="Troll", blocks_movement=True)
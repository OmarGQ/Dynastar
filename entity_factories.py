# -*- coding: utf-8 -*-
"""
Created on Sat May 20 19:53:48 2023

@author: Kiddra
"""

from entity import Entity

player = Entity(char="@", color=(255, 255, 255), name="Player", blocks_movement=True)

orc = Entity(char="o", color=(63, 127, 63), name="Orc", blocks_movement=True)
troll = Entity(char="T", color=(0, 127, 0), name="Troll", blocks_movement=True)
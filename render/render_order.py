# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:23:42 2023

@author: kiddra
"""

from enum import auto, Enum


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 16:10:37 2023

@author: Kiddra
"""

from typing import Tuple

import numpy as np  # type: ignore

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ("ch", np.int32),  #Unicode codepoint.
        ("fg", "3B"),  #3 unsigned bytes, for RGB colors.
        ("bg", "3B"),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ("walkable", np.bool_),  #True if this tile can be walked over.
        ("goal", np.bool_),  #True if this tile is the exit.
        ("transparent", np.bool_),  #True if this tile doesn't block FOV.
        ("dark", graphic_dt),  #Graphics for when this tile is not in FOV.
        ("light", graphic_dt), # Graphics for when the tile is in FOV.
    ]
)


def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    walkable: int,
    goal: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, goal, transparent, dark, light), dtype=tile_dt)


# SHROUD represents unexplored, unseen tiles
SHROUD = np.array((ord(" "), (255, 255, 255), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(
    walkable=True, 
    goal=False,
    transparent=True, 
    dark=(ord(" "), (155, 155, 155), (25, 25, 0)),
    light=(ord(" "), (255, 255, 255), (50, 50, 0)),
)
wall = new_tile(
    walkable=False, 
    goal=False,
    transparent=False, 
    dark=(ord("#"), (155, 155, 155), (65, 55, 25)),
    light=(ord("#"), (255, 255, 255), (50, 50, 0)),
)
tree = new_tile(
    walkable=False, 
    goal=False,
    transparent=False, 
    dark=(ord("↑"), (25, 155, 25), (25, 25, 0)),
    light=(ord("↑"), (55, 255, 55), (50, 50, 0)),
)
water = new_tile(
    walkable=True, 
    goal=False,
    transparent=True, 
    dark=(ord("▓"), (0, 0, 155), (75, 75, 155)),
    light=(ord("▓"), (0, 0, 255), (155, 155, 255)),
)
room_floor = new_tile(
    walkable=True, 
    goal=False,
    transparent=True, 
    dark=(ord("█"), (50, 50, 0), (50, 50, 0)),
    light=(ord("█"), (100, 100, 0), (100, 100, 0)),
)
goal = new_tile(
    walkable=True, 
    goal=True,
    transparent=True, 
    dark=(ord("▲"), (10, 155, 10), (50, 50, 0)),
    light=(ord("▲"), (20, 255, 20), (100, 100, 0)),
)
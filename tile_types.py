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
        ("transparent", np.bool_),  #True if this tile doesn't block FOV.
        ("dark", graphic_dt),  #Graphics for when this tile is not in FOV.
    ]
)


def new_tile(
    *,  
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    """Helper function for defining individual tile types """
    return np.array((walkable, transparent, dark), dtype=tile_dt)


floor = new_tile(
    walkable=True, transparent=True, dark=(ord(" "), (255, 255, 255), (50, 50, 0)),
)
wall = new_tile(
    walkable=False, transparent=False, dark=(ord("#"), (255, 255, 255), (50, 50, 0)),
)
tree = new_tile(
    walkable=False, transparent=False, dark=(ord("↑"), (55, 255, 55), (50, 50, 0)),
)
water = new_tile(
    walkable=True, transparent=False, dark=(ord("▓"), (0, 0, 255), (155, 155, 255)),
)
room_floor = new_tile(
    walkable=True, transparent=False, dark=(ord("█"), (100, 100, 0), (100, 100, 0)),
)
goal = new_tile(
    walkable=True, transparent=True, dark=(ord("▲"), (20, 255, 20), (100, 100, 0)),
)
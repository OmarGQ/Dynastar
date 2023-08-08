# -*- coding: utf-8 -*-
"""
Created on Wed May 24 12:34:06 2023

@author: kiddra
"""

from __future__ import annotations

from typing import Tuple, TYPE_CHECKING
import colors

if TYPE_CHECKING:
    from tcod import Console
    from engine import Engine
    from game_map import GameMap

def get_names_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()

def get_items_at_location(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bounds(x, y) or not game_map.visible[x, y]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y and entity in game_map.items
    )

    return names.capitalize()

def render_bar(
    console: Console, current_value: int, maximum_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / maximum_value * total_width)

    console.draw_rect(x=91, y=3, width=total_width, height=1, ch=1, bg=colors.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=91, y=3, width=bar_width, height=1, ch=1, bg=colors.bar_filled
        )

    console.print(
        x=92, y=3, string=f"HP: {current_value}/{maximum_value}", fg=colors.bar_text
    )

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )

    console.print(x=x, y=y, string=names_at_mouse_location)

def render_names_at_player_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:

    names_at_location = get_items_at_location(
        x=engine.player.x, y=engine.player.y, game_map=engine.game_map
    )
    if names_at_location != "":
        names_at_location = "Press E to interact\n" + names_at_location
    console.print(x=x, y=y, string=names_at_location)
    
def render_ui(console, player, world) -> None:
    "Render player's stats"
    console.print(x=90, y=1, string="o-Player----------------o")
    console.print(x=91, y=2, string=f"Dungeon level: {world.current_floor}")
    render_bar(
        console=console,
        current_value=player.fighter.hp,
        maximum_value=player.fighter.max_hp,
        total_width=20,
    )
    console.print(x=91, y=4, string=f"Power: {player.fighter.defense}")
    console.print(x=91, y=5, string=f"Power: {player.fighter.power}")
    console.print(x=90, y=14, string="o-Inventory-------------o")
    
    number_of_items_in_inventory = len(player.inventory.items)
    y=15
    if number_of_items_in_inventory > 0:
        for i, item in enumerate(player.inventory.items):
            item_key = chr(ord("1") + i)
            is_equipped = player.equipment.item_is_equipped(item)
            item_string = f"({item_key}) {item.name}"

            if is_equipped:
                item_string = f"{item_string} (E)"
            console.print(x=91, y=y + i, string=item_string)
    else:
        console.print(x=91, y=y, string="(Empty)")
    console.print(x=90, y=69, string="o--------------------------o")
    
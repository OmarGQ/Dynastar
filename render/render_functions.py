# -*- coding: utf-8 -*-
"""
Created on Wed May 24 12:34:06 2023

@author: kiddra
"""

from __future__ import annotations

from typing import TYPE_CHECKING
import render.colors as colors

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

    console.draw_rect(x=92, y=5, width=total_width, height=1, ch=1, bg=colors.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=92, y=5, width=bar_width, height=1, ch=1, bg=colors.bar_filled
        )

    console.print(
        x=93, y=5, string=f"HP: {current_value}/{maximum_value}", fg=colors.bar_text
    )

def render_names_at_mouse_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:
    mouse_x, mouse_y = engine.mouse_location

    names_at_mouse_location = get_names_at_location(
        x=mouse_x, y=mouse_y, game_map=engine.game_map
    )
    console.print(x=x, y=y, string="Mouse is selecting:")
    console.print(x=x+2, y=y+1, string=names_at_mouse_location, fg=colors.UI_selection)

def render_names_at_player_location(
    console: Console, x: int, y: int, engine: Engine
) -> None:

    names_at_location = get_items_at_location(
        x=engine.player.x, y=engine.player.y, game_map=engine.game_map
    )
    message = ""
    if names_at_location != "":
        message = "Press E to interact\nwhit: "
    console.print(x=x, y=y, string=message)
    console.print(x=x+6, y=y+1, string=names_at_location, fg=colors.UI_selection)
    
def render_ui(console, player, world) -> None:
    "Render player's stats"
    for i in range(1, 69):
        console.print(x=90, y=i, string="|", fg=colors.UI_border)
        console.print(x=114, y=i, string="|", fg=colors.UI_border)
    
    console.print(x=90, y=1, string="o-Player----------------o", fg=colors.UI_border)
    console.print(x=92, y=3, string=f"Dungeon level: {world.current_floor}", fg=[0, 128, 255])
    render_bar(
        console=console,
        current_value=player.fighter.hp,
        maximum_value=player.fighter.max_hp,
        total_width=20,
    )
    console.print(x=92, y=7, string=f"Level: {player.level.current_level}", fg=colors.UI_xp)
    console.print(x=92, y=8, 
                  string=f"XP: {player.level.current_xp}/{player.level.experience_to_next_level}", fg=colors.UI_xp)
    console.print(x=92, y=10, string=f"Defense: {player.fighter.defense}")
    console.print(x=92, y=11, string=f"Power: {player.fighter.power}")
    console.print(x=90, y=14, string="o-Inventory-------------o", fg=colors.UI_border)
    
    number_of_items_in_inventory = len(player.inventory.items)
    y=16
    if number_of_items_in_inventory > 0:
        for i, item in enumerate(player.inventory.items):
            item_key = chr(ord("1") + i)
            is_equipped = player.equipment.item_is_equipped(item)
            item_string = f"{item_key}) {item.name}"

            if is_equipped:
                item_string = f"{item_string} (E)"
            console.print(x=92, y=y + i, string=item_string)
    else:
        console.print(x=92, y=y, string="(Empty)")
    console.print(x=90, y=26, string="o-Controls--------------o", fg=colors.UI_border)
    console.print(x=92, y=28, string="You can move with:\n ASWD, NumPad,\n or ArrowKeys")
    console.print(x=92, y=32, string="'SPACE' or '5' Wait")
    console.print(x=92, y=33, string="'I' use item")
    console.print(x=92, y=34, string="'O' Drop item'")
    console.print(x=92, y=35, string="'V' See full log")
    console.print(x=92, y=36, string="'esc' Exit the game")
    console.print(x=90, y=38, string="o-Information-----------o", fg=colors.UI_border)
    console.print(x=90, y=69, string="o-----------------------o", fg=colors.UI_border)
    
    
    console.print(x=0, y=61, string="o-GameLog--------------------------------------------------------------------------------o", fg=colors.UI_border)
    for i in range(62, 69):
        console.print(x=0, y=i, string="|", fg=colors.UI_border)
        console.print(x=89, y=i, string="|", fg=colors.UI_border)
    console.print(x=0, y=69, string="o----------------------------------------------------------------------------------------o", fg=colors.UI_border)
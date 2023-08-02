# -*- coding: utf-8 -*-
"""
Created on Sat May 20 19:53:48 2023

@author: kiddra
"""

from components.ai import HostileEnemy, SlowEnemy
from components import consumable, equippable
from components.fighter import Fighter
from entity import Actor, Item
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=9),
    level=Level(level_up_base=200)
)

orc = Actor(
    char="O",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=35)
)
 
skeleton = Actor(
    char="S",
    color=(255, 255, 255),
    name="Skeleton",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=6, base_defense=1, base_power=2),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=25)
)
 
kobold = Actor(
    char="K",
    color=(164, 15, 15),
    name="Kobold",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=10, base_defense=2, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=60)
)
 
zombie = Actor(
    char="Z",
    color=(211, 244, 212),
    name="Zombie",
    ai_cls=SlowEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=5, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15)
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=SlowEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=16, base_defense=1, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100)
)

health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=5),
)

health_potion_Lv2 = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=10),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)

fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)

dagger = Item(    char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger())

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail()
)
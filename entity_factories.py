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
    color=(0, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=30, base_defense=1, base_power=2),
    inventory=Inventory(capacity=9),
    level=Level(level_up_base=120)
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
    fighter=Fighter(hp=8, base_defense=2, base_power=3),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=25)
)
 
zombie = Actor(
    char="Z",
    color=(211, 244, 212),
    name="Zombie",
    ai_cls=SlowEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=6, base_defense=0, base_power=4),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=15)
)
 
kobold = Actor(
    char="K",
    color=(164, 15, 15),
    name="Kobold",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=17, base_defense=3, base_power=5),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=60)
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=SlowEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=20, base_defense=2, base_power=7),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=100)
)

super_orc = Actor(
    char="O",
    color=(174, 8, 196),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=18, base_defense=3, base_power=7),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=85)
)
 
super_skeleton = Actor(
    char="S",
    color=(204, 38, 226),
    name="Skeleton",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=17, base_defense=5, base_power=6),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=75)
)
 
super_zombie = Actor(
    char="Z",
    color=(224, 58, 246),
    name="Zombie",
    ai_cls=SlowEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=12, base_defense=3, base_power=7),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=105)
)
 
super_kobold = Actor(
    char="K",
    color=(255, 0, 43),
    name="Kobold",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=22, base_defense=6, base_power=8),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=110)
)

super_troll = Actor(
    char="T",
    color=(2, 201, 2),
    name="Troll",
    ai_cls=SlowEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=25, base_defense=5, base_power=10),
    inventory=Inventory(capacity=0),
    level=Level(xp_given=150)
)


health_potion = Item(
    char="!",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=6),
)

health_potion_Lv2 = Item(
    char="!",
    color=(147, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=12),
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

dagger = Item(char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger())

sword = Item(char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword())

axe = Item(char="/", color=(0, 191, 255), name="Axe", equippable=equippable.Axe())

mace = Item(char="/", color=(0, 191, 255), name="Mace", equippable=equippable.Mace())

long_sword = Item(char="/", color=(0, 191, 255), name="Long Sword", equippable=equippable.LongSword())

leather_armor = Item(char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="↓", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail()
)

breast_plate = Item(
    char="↓", color=(209, 205, 194), name="Breast Plate", equippable=equippable.BreastPlate()
)

plate_armor = Item(
    char="↓", color=(148, 143, 129), name="Plate Armor", equippable=equippable.PlateArmor()
)

scale_armor = Item(
    char="↓", color=(158, 5, 5), name="Scale Armor", equippable=equippable.ScaleArmor()
)
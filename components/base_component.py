# -*- coding: utf-8 -*-
"""
Created on Tue May 23 12:41:53 2023

@author: kiddra
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class BaseComponent:
    entity: Entity  # Owning entity instance.

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine
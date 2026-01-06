"""
Collection managers for UnitHandle.

These provide list-like access and collective modification methods 
for various unit attribute collections.
"""
from __future__ import annotations

from .tasks import TasksManager
from .attacks import AttacksManager
from .armours import ArmoursManager
from .damage_graphics import DamageGraphicsManager
from .train_locations import TrainLocationsManager
from .drop_sites import DropSitesManager
from .annexes import AnnexesManager
from .costs import CostsManager
from .resources import ResourcesManager

__all__ = [
    "TasksManager",
    "AttacksManager",
    "ArmoursManager",
    "DamageGraphicsManager",
    "TrainLocationsManager",
    "DropSitesManager",
    "AnnexesManager",
    "CostsManager",
    "ResourcesManager",
    # Legacy aliases
    "TasksWrapper",
    "DamageGraphicsWrapper",
    "TrainLocationsWrapper",
    "CostWrapper",
    "ResourceStoragesWrapper",
]

TasksWrapper = TasksManager
DamageGraphicsWrapper = DamageGraphicsManager
TrainLocationsWrapper = TrainLocationsManager
CostWrapper = CostsManager
ResourceStoragesWrapper = ResourcesManager

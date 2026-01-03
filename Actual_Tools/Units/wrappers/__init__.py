"""
Unit property wrappers package.

Each wrapper provides flat property access to nested genieutils classes and collection management.
"""

from Actual_Tools.Units.wrappers.type_50 import Type50Wrapper
from Actual_Tools.Units.wrappers.creatable import CreatableWrapper
from Actual_Tools.Units.wrappers.costs import CostWrapper
from Actual_Tools.Units.wrappers.dead_fish import DeadFishWrapper
from Actual_Tools.Units.wrappers.bird import BirdWrapper
from Actual_Tools.Units.wrappers.projectile import ProjectileWrapper
from Actual_Tools.Units.wrappers.building import BuildingWrapper
from Actual_Tools.Units.wrappers.tasks import TasksWrapper
from Actual_Tools.Units.wrappers.resource_storages import ResourceStoragesWrapper
from Actual_Tools.Units.wrappers.damage_graphics import DamageGraphicsWrapper
from Actual_Tools.Units.wrappers.annex import AnnexHandle, AnnexesWrapper
from Actual_Tools.Units.wrappers.train_location import TrainLocationHandle, TrainLocationsWrapper

__all__ = [
    "Type50Wrapper",
    "CreatableWrapper",
    "CostWrapper",
    "DeadFishWrapper",
    "BirdWrapper",
    "ProjectileWrapper",
    "BuildingWrapper",
    "TasksWrapper",
    "ResourceStoragesWrapper",
    "DamageGraphicsWrapper",
    "AnnexHandle",
    "AnnexesWrapper",
    "TrainLocationHandle",
    "TrainLocationsWrapper",
]



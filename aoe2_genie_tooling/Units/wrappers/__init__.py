"""
Unit property wrappers package.

Each wrapper provides flat property access to nested GenieDatParser classes.

Wrappers are for TYPE-LEVEL attributes (single nested objects):
- CombatWrapper → unit.combat_info
- CreationWrapper → unit.creation_info
- MovementWrapper → unit.movement_info
- BehaviorWrapper → unit.task_info (scalar properties only)
- ProjectileWrapper → unit.projectile_info
- BuildingWrapper → unit.building_info

For LIST management (attacks, armours, tasks, etc.), see collections/ folder.

OLD wrapper files have been moved to wrappers_OLD/ for reference.
"""

from aoe2_genie_tooling.Units.wrappers.combat import CombatWrapper
from aoe2_genie_tooling.Units.wrappers.creation import CreationWrapper
from aoe2_genie_tooling.Units.wrappers.movement import MovementWrapper
from aoe2_genie_tooling.Units.wrappers.behavior import BehaviorWrapper
from aoe2_genie_tooling.Units.wrappers.projectile import ProjectileWrapper
from aoe2_genie_tooling.Units.wrappers.building import BuildingWrapper

# Backward compatibility aliases
Type50Wrapper = CombatWrapper
CreatableWrapper = CreationWrapper
DeadFishWrapper = MovementWrapper
BirdWrapper = BehaviorWrapper

__all__ = [
    # New names (preferred)
    "CombatWrapper",
    "CreationWrapper",
    "MovementWrapper",
    "BehaviorWrapper",
    "ProjectileWrapper",
    "BuildingWrapper",
    # Legacy aliases
    "Type50Wrapper",
    "CreatableWrapper",
    "DeadFishWrapper",
    "BirdWrapper",
]

"""
Units module - Unit editing functionality.

Provides:
- UnitManager: Create, clone, move, and query units
- UnitHandle: High-level wrapper for Genie Unit objects with multi-civ support
- TaskBuilder: Fluent API for adding typed tasks
- Handles: TaskHandle, AttackHandle, ArmourHandle, DamageGraphicHandle, TrainLocationHandle, DropSiteHandle
"""
from .unit_manager import UnitManager
from .unit_handle import UnitHandle
from .task_builder import TaskBuilder
from .handles import (
    TaskHandle,
    AttackHandle,
    ArmourHandle,
    DamageGraphicHandle,
    TrainLocationHandle,
    DropSiteHandle,
)

__all__ = [
    "UnitManager",
    "UnitHandle",
    "TaskBuilder",
    "TaskHandle",
    "AttackHandle",
    "ArmourHandle",
    "DamageGraphicHandle",
    "TrainLocationHandle",
    "DropSiteHandle",
]


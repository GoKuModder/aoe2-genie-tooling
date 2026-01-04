"""Units module with UnitManager, UnitHandle, and collection handles."""

from Actual_Tools_GDP.Units.unit_manager import GenieUnitManager
from Actual_Tools_GDP.Units.unit_handle import UnitHandle
from Actual_Tools_GDP.Units.handles import (
    TaskHandle,
    AttackHandle,
    ArmourHandle,
    DamageGraphicHandle,
    TrainLocationHandle,
    DropSiteHandle,
)

__all__ = [
    "GenieUnitManager",
    "UnitHandle",
    "TaskHandle",
    "AttackHandle",
    "ArmourHandle",
    "DamageGraphicHandle",
    "TrainLocationHandle",
    "DropSiteHandle",
]

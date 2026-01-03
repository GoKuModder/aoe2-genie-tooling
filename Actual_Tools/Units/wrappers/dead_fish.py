"""
DeadFishWrapper - Complete dead fish movement attribute wrapper for UnitHandle.

Provides flat property access to ALL DeadFish attributes:
- Graphics: walking_graphic, running_graphic
- Movement: rotation_speed, turn_radius, turn_radius_speed
- Yaw: max_yaw_per_second_moving, stationary_yaw_revolution_time, max_yaw_per_second_stationary
- Tracking: tracking_unit, tracking_unit_mode, tracking_unit_density
- Misc: old_size_class, old_move_algorithm, min_collision_size_multiplier

Mirrors genieutils.unit.DeadFish structure completely.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from genieutils.unit import Unit

__all__ = ["DeadFishWrapper"]


class DeadFishWrapper:
    """
    Complete wrapper for DeadFish (dead fish movement) attributes.
    
    Provides flat property access to all dead fish-specific stats.
    Changes propagate to all units in the provided list.
    """
    
    __slots__ = ("_units",)
    
    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)
    
    def _get_dead_fish(self) -> Optional[Any]:
        """Get DeadFish from first unit."""
        if self._units and self._units[0].dead_fish:
            return self._units[0].dead_fish
        return None
    
    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' dead_fish."""
        for unit in self._units:
            if unit.dead_fish:
                setattr(unit.dead_fish, attr, value)
    
    # Graphics
    @property
    def walking_graphic(self) -> int:
        """Walking graphic ID."""
        df = self._get_dead_fish()
        return df.walking_graphic if df else -1
    
    @walking_graphic.setter
    def walking_graphic(self, value: int) -> None:
        self._set_all("walking_graphic", value)
    
    @property
    def running_graphic(self) -> int:
        """Running graphic ID."""
        df = self._get_dead_fish()
        return df.running_graphic if df else -1
    
    @running_graphic.setter
    def running_graphic(self, value: int) -> None:
        self._set_all("running_graphic", value)
    
    # Movement & Rotation
    @property
    def rotation_speed(self) -> float:
        """Rotation speed."""
        df = self._get_dead_fish()
        return df.rotation_speed if df else 0.0
    
    @rotation_speed.setter
    def rotation_speed(self, value: float) -> None:
        self._set_all("rotation_speed", value)
    
    @property
    def turn_radius(self) -> float:
        """Turn radius."""
        df = self._get_dead_fish()
        return df.turn_radius if df else 0.0
    
    @turn_radius.setter
    def turn_radius(self, value: float) -> None:
        self._set_all("turn_radius", value)
    
    @property
    def turn_radius_speed(self) -> float:
        """Turn radius speed."""
        df = self._get_dead_fish()
        return df.turn_radius_speed if df else 0.0
    
    @turn_radius_speed.setter
    def turn_radius_speed(self, value: float) -> None:
        self._set_all("turn_radius_speed", value)
    
    # Yaw
    @property
    def max_yaw_per_second_moving(self) -> float:
        """Max yaw per second while moving."""
        df = self._get_dead_fish()
        return df.max_yaw_per_second_moving if df else 0.0
    
    @max_yaw_per_second_moving.setter
    def max_yaw_per_second_moving(self, value: float) -> None:
        self._set_all("max_yaw_per_second_moving", value)
    
    @property
    def stationary_yaw_revolution_time(self) -> float:
        """Stationary yaw revolution time."""
        df = self._get_dead_fish()
        return df.stationary_yaw_revolution_time if df else 0.0
    
    @stationary_yaw_revolution_time.setter
    def stationary_yaw_revolution_time(self, value: float) -> None:
        self._set_all("stationary_yaw_revolution_time", value)
    
    @property
    def max_yaw_per_second_stationary(self) -> float:
        """Max yaw per second while stationary."""
        df = self._get_dead_fish()
        return df.max_yaw_per_second_stationary if df else 0.0
    
    @max_yaw_per_second_stationary.setter
    def max_yaw_per_second_stationary(self, value: float) -> None:
        self._set_all("max_yaw_per_second_stationary", value)
    
    # Tracking
    @property
    def tracking_unit(self) -> int:
        """Tracking unit ID."""
        df = self._get_dead_fish()
        return df.tracking_unit if df else -1
    
    @tracking_unit.setter
    def tracking_unit(self, value: int) -> None:
        self._set_all("tracking_unit", value)
    
    @property
    def tracking_unit_mode(self) -> int:
        """Tracking unit mode."""
        df = self._get_dead_fish()
        return df.tracking_unit_mode if df else 0
    
    @tracking_unit_mode.setter
    def tracking_unit_mode(self, value: int) -> None:
        self._set_all("tracking_unit_mode", value)
    
    @property
    def tracking_unit_density(self) -> float:
        """Tracking unit density."""
        df = self._get_dead_fish()
        return df.tracking_unit_density if df else 0.0
    
    @tracking_unit_density.setter
    def tracking_unit_density(self, value: float) -> None:
        self._set_all("tracking_unit_density", value)
    
    # Misc
    @property
    def old_size_class(self) -> int:
        """Old size class."""
        df = self._get_dead_fish()
        return df.old_size_class if df else 0
    
    @old_size_class.setter
    def old_size_class(self, value: int) -> None:
        self._set_all("old_size_class", value)
    
    @property
    def old_move_algorithm(self) -> int:
        """Old move algorithm."""
        df = self._get_dead_fish()
        return df.old_move_algorithm if df else 0
    
    @old_move_algorithm.setter
    def old_move_algorithm(self, value: int) -> None:
        self._set_all("old_move_algorithm", value)
    
    @property
    def min_collision_size_multiplier(self) -> float:
        """Minimum collision size multiplier."""
        df = self._get_dead_fish()
        return df.min_collision_size_multiplier if df else 0.0
    
    @min_collision_size_multiplier.setter
    def min_collision_size_multiplier(self, value: float) -> None:
        self._set_all("min_collision_size_multiplier", value)

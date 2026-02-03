"""
MovementWrapper - Movement attribute wrapper for UnitHandle.

Ported from dead_fish_OLD.py to work with GenieDatParser.

Provides flat property access to MovementInfo attributes:
- Graphics: walking_graphic_id, running_graphic_id
- Movement: rotation_speed, rotation_radius, rotation_radius_speed
- Yaw: max_yaw_per_sec_walking, standing_yaw_revolution_time, max_yaw_per_sec_standing
- Tracking: trailing_unit_id, trail_mode, trail_spacing
- Misc: old_size_class, old_move_algorithm, min_collision_size_multiplier

Maps to GenieDatParser's MovementInfo structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["MovementWrapper"]


class MovementWrapper:
    """
    Wrapper for MovementInfo (movement) attributes.

    Provides flat property access to all movement stats.
    Changes propagate to all units in the provided list.

    Attributes from GenieDatParser MovementInfo:
        walking_sprite_id, running_sprite_id, rotation_speed,
        old_size_class, trailing_unit_id, trail_mode, trail_spacing,
        old_move_algorithm, rotation_radius, rotation_radius_speed,
        max_yaw_per_sec_walking, standing_yaw_revolution_time,
        max_yaw_per_sec_standing, min_collision_size_multiplier
    """

    __slots__ = ("_units",)

    def __init__(self, units: List["Unit"]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_movement_info(self) -> Optional[Any]:
        """Get MovementInfo from first unit."""
        if self._units and hasattr(self._units[0], "movement_info") and self._units[0].movement_info:
            return self._units[0].movement_info
        return None

    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' movement_info."""
        for unit in self._units:
            if hasattr(unit, "movement_info") and unit.movement_info:
                setattr(unit.movement_info, attr, value)

    # -------------------------
    # Graphics
    # -------------------------

    @property
    def walking_graphic_id(self) -> int:
        """Walking graphic ID."""
        mi = self._get_movement_info()
        return mi.walking_sprite_id if mi else -1

    @walking_graphic_id.setter
    def walking_graphic_id(self, value: int) -> None:
        self._set_all("walking_sprite_id", value)

    @property
    def running_graphic_id(self) -> int:
        """Running graphic ID."""
        mi = self._get_movement_info()
        return mi.running_sprite_id if mi else -1

    @running_graphic_id.setter
    def running_graphic_id(self, value: int) -> None:
        self._set_all("running_sprite_id", value)

    # -------------------------
    # Movement & Rotation
    # -------------------------

    @property
    def rotation_speed(self) -> float:
        """Rotation speed."""
        mi = self._get_movement_info()
        return mi.rotation_speed if mi else 0.0

    @rotation_speed.setter
    def rotation_speed(self, value: float) -> None:
        self._set_all("rotation_speed", value)

    @property
    def turn_radius(self) -> float:
        """Turn radius (rotation_radius)."""
        mi = self._get_movement_info()
        return mi.rotation_radius if mi else 0.0

    @turn_radius.setter
    def turn_radius(self, value: float) -> None:
        self._set_all("rotation_radius", value)

    @property
    def rotation_radius(self) -> float:
        """Rotation radius."""
        mi = self._get_movement_info()
        return mi.rotation_radius if mi else 0.0

    @rotation_radius.setter
    def rotation_radius(self, value: float) -> None:
        self._set_all("rotation_radius", value)

    @property
    def turn_radius_speed(self) -> float:
        """Turn radius speed (rotation_radius_speed)."""
        mi = self._get_movement_info()
        return mi.rotation_radius_speed if mi else 0.0

    @turn_radius_speed.setter
    def turn_radius_speed(self, value: float) -> None:
        self._set_all("rotation_radius_speed", value)

    @property
    def rotation_radius_speed(self) -> float:
        """Rotation radius speed."""
        mi = self._get_movement_info()
        return mi.rotation_radius_speed if mi else 0.0

    @rotation_radius_speed.setter
    def rotation_radius_speed(self, value: float) -> None:
        self._set_all("rotation_radius_speed", value)

    # -------------------------
    # Yaw
    # -------------------------

    @property
    def max_yaw_per_second_moving(self) -> float:
        """Max yaw per second while moving."""
        mi = self._get_movement_info()
        return mi.max_yaw_per_sec_walking if mi else 0.0

    @max_yaw_per_second_moving.setter
    def max_yaw_per_second_moving(self, value: float) -> None:
        self._set_all("max_yaw_per_sec_walking", value)

    @property
    def max_yaw_per_sec_walking(self) -> float:
        """Max yaw per second while walking."""
        mi = self._get_movement_info()
        return mi.max_yaw_per_sec_walking if mi else 0.0

    @max_yaw_per_sec_walking.setter
    def max_yaw_per_sec_walking(self, value: float) -> None:
        self._set_all("max_yaw_per_sec_walking", value)

    @property
    def stationary_yaw_revolution_time(self) -> float:
        """Stationary yaw revolution time."""
        mi = self._get_movement_info()
        return mi.standing_yaw_revolution_time if mi else 0.0

    @stationary_yaw_revolution_time.setter
    def stationary_yaw_revolution_time(self, value: float) -> None:
        self._set_all("standing_yaw_revolution_time", value)

    @property
    def standing_yaw_revolution_time(self) -> float:
        """Standing yaw revolution time."""
        mi = self._get_movement_info()
        return mi.standing_yaw_revolution_time if mi else 0.0

    @standing_yaw_revolution_time.setter
    def standing_yaw_revolution_time(self, value: float) -> None:
        self._set_all("standing_yaw_revolution_time", value)

    @property
    def max_yaw_per_second_stationary(self) -> float:
        """Max yaw per second while stationary."""
        mi = self._get_movement_info()
        return mi.max_yaw_per_sec_standing if mi else 0.0

    @max_yaw_per_second_stationary.setter
    def max_yaw_per_second_stationary(self, value: float) -> None:
        self._set_all("max_yaw_per_sec_standing", value)

    @property
    def max_yaw_per_sec_standing(self) -> float:
        """Max yaw per second while standing."""
        mi = self._get_movement_info()
        return mi.max_yaw_per_sec_standing if mi else 0.0

    @max_yaw_per_sec_standing.setter
    def max_yaw_per_sec_standing(self, value: float) -> None:
        self._set_all("max_yaw_per_sec_standing", value)

    # -------------------------
    # Tracking
    # -------------------------

    @property
    def tracking_unit_id(self) -> int:
        """Tracking unit ID (trailing_unit_id)."""
        mi = self._get_movement_info()
        return mi.trailing_unit_id if mi else -1

    @tracking_unit_id.setter
    def tracking_unit_id(self, value: int) -> None:
        self._set_all("trailing_unit_id", value)

    @property
    def trailing_unit_id(self) -> int:
        """Trailing unit ID."""
        mi = self._get_movement_info()
        return mi.trailing_unit_id if mi else -1

    @trailing_unit_id.setter
    def trailing_unit_id(self, value: int) -> None:
        self._set_all("trailing_unit_id", value)

    @property
    def tracking_unit_mode(self) -> int:
        """Tracking unit mode (trail_mode)."""
        mi = self._get_movement_info()
        return mi.trail_mode if mi else 0

    @tracking_unit_mode.setter
    def tracking_unit_mode(self, value: int) -> None:
        self._set_all("trail_mode", value)

    @property
    def trail_mode(self) -> int:
        """Trail mode."""
        mi = self._get_movement_info()
        return mi.trail_mode if mi else 0

    @trail_mode.setter
    def trail_mode(self, value: int) -> None:
        self._set_all("trail_mode", value)

    @property
    def tracking_unit_density(self) -> float:
        """Tracking unit density (trail_spacing)."""
        mi = self._get_movement_info()
        return mi.trail_spacing if mi else 0.0

    @tracking_unit_density.setter
    def tracking_unit_density(self, value: float) -> None:
        self._set_all("trail_spacing", value)

    @property
    def trail_spacing(self) -> float:
        """Trail spacing."""
        mi = self._get_movement_info()
        return mi.trail_spacing if mi else 0.0

    @trail_spacing.setter
    def trail_spacing(self, value: float) -> None:
        self._set_all("trail_spacing", value)

    # -------------------------
    # Misc
    # -------------------------

    @property
    def old_size_class(self) -> int:
        """Old size class."""
        mi = self._get_movement_info()
        return mi.old_size_class if mi else 0

    @old_size_class.setter
    def old_size_class(self, value: int) -> None:
        self._set_all("old_size_class", value)

    @property
    def old_move_algorithm(self) -> int:
        """Old move algorithm."""
        mi = self._get_movement_info()
        return mi.old_move_algorithm if mi else 0

    @old_move_algorithm.setter
    def old_move_algorithm(self, value: int) -> None:
        self._set_all("old_move_algorithm", value)

    @property
    def min_collision_size_multiplier(self) -> float:
        """Minimum collision size multiplier."""
        mi = self._get_movement_info()
        return mi.min_collision_size_multiplier if mi else 0.0

    @min_collision_size_multiplier.setter
    def min_collision_size_multiplier(self, value: float) -> None:
        self._set_all("min_collision_size_multiplier", value)

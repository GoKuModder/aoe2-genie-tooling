"""
ProjectileWrapper - Projectile attribute wrapper for UnitHandle.

Ported from projectile_OLD.py to work with GenieDatParser.

Provides flat property access to ProjectileInfo attributes:
- projectile_type, smart_mode, hit_mode, vanish_mode, 
  area_effect_specials, projectile_arc

Maps to GenieDatParser's ProjectileInfo structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["ProjectileWrapper"]


class ProjectileWrapper:
    """
    Wrapper for ProjectileInfo attributes.

    Provides flat property access to projectile-specific stats.
    Changes propagate to all units in the provided list.

    Attributes from GenieDatParser ProjectileInfo:
        projectile_type, smart_mode, hit_mode, vanish_mode,
        area_effect_specials, projectile_arc
    """

    __slots__ = ("_units",)

    def __init__(self, units: List["Unit"]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_projectile_info(self) -> Optional[Any]:
        """Get ProjectileInfo from first unit."""
        if self._units and hasattr(self._units[0], "projectile_info") and self._units[0].projectile_info:
            return self._units[0].projectile_info
        return None

    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' projectile_info."""
        for unit in self._units:
            if hasattr(unit, "projectile_info") and unit.projectile_info:
                setattr(unit.projectile_info, attr, value)

    # -------------------------
    # Projectile Properties
    # -------------------------

    @property
    def projectile_type(self) -> int:
        """Projectile type."""
        pi = self._get_projectile_info()
        return pi.projectile_type if pi else 0

    @projectile_type.setter
    def projectile_type(self, value: int) -> None:
        self._set_all("projectile_type", value)

    @property
    def smart_mode(self) -> int:
        """Smart targeting mode."""
        pi = self._get_projectile_info()
        return pi.smart_mode if pi else 0

    @smart_mode.setter
    def smart_mode(self, value: int) -> None:
        self._set_all("smart_mode", value)

    @property
    def hit_mode(self) -> int:
        """Hit detection mode."""
        pi = self._get_projectile_info()
        return pi.hit_mode if pi else 0

    @hit_mode.setter
    def hit_mode(self, value: int) -> None:
        self._set_all("hit_mode", value)

    @property
    def vanish_mode(self) -> int:
        """Vanish mode (what happens on impact)."""
        pi = self._get_projectile_info()
        return pi.vanish_mode if pi else 0

    @vanish_mode.setter
    def vanish_mode(self, value: int) -> None:
        """Set vanish mode with VanishMode enum validation."""
        import traceback

        try:
            from Datasets.attributes import VanishMode

            # Validate against VanishMode enum
            valid_values = {e.value for e in VanishMode}
            if value not in valid_values:
                # Capture source for error
                stack = traceback.extract_stack()
                source_frame = stack[-2] if len(stack) >= 2 else stack[-1]
                source_info = f"{source_frame.filename}:{source_frame.lineno} - {source_frame.line}"

                valid_list = ", ".join(f"{e.name}={e.value}" for e in VanishMode)
                raise ValueError(
                    f"vanish_mode: Invalid value {value} for VanishMode.\n"
                    f"  Valid values: {valid_list}\n"
                    f"  Source: {source_info}"
                )
        except ImportError:
            # If Datasets not available, skip validation
            pass

        self._set_all("vanish_mode", value)

    @property
    def area_effect_specials(self) -> int:
        """Area effect special flags."""
        pi = self._get_projectile_info()
        return pi.area_effect_specials if pi else 0

    @area_effect_specials.setter
    def area_effect_specials(self, value: int) -> None:
        self._set_all("area_effect_specials", value)

    @property
    def projectile_arc(self) -> float:
        """Projectile arc (trajectory)."""
        pi = self._get_projectile_info()
        return pi.projectile_arc if pi else 0.0

    @projectile_arc.setter
    def projectile_arc(self, value: float) -> None:
        self._set_all("projectile_arc", value)

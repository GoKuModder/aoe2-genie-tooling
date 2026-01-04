"""
ProjectileWrapper - Projectile attribute wrapper for UnitHandle.

Provides flat property access to Projectile attributes:
- projectile_type, smart_mode, hit_mode, vanish_mode, area_effect_specials, projectile_arc

Mirrors genieutils.unit.Projectile structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from genie_rust import Unit

__all__ = ["ProjectileWrapper"]


class ProjectileWrapper:
    """
    Wrapper for Projectile attributes.

    Provides flat property access to projectile-specific stats.
    Changes propagate to all units in the provided list.

    Attributes from genieutils.unit.Projectile:
        projectile_type, smart_mode, hit_mode, vanish_mode,
        area_effect_specials, projectile_arc
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_projectile(self) -> Optional[Any]:
        """Get Projectile from first unit."""
        if self._units and self._units[0].projectile:
            return self._units[0].projectile
        return None

    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' projectile."""
        for unit in self._units:
            if unit.projectile:
                setattr(unit.projectile, attr, value)

    @property
    def projectile_type(self) -> int:
        """Projectile type."""
        p = self._get_projectile()
        return p.projectile_type if p else 0

    @projectile_type.setter
    def projectile_type(self, value: int) -> None:
        self._set_all("projectile_type", value)

    @property
    def smart_mode(self) -> int:
        """Smart targeting mode."""
        p = self._get_projectile()
        return p.smart_mode if p else 0

    @smart_mode.setter
    def smart_mode(self, value: int) -> None:
        self._set_all("smart_mode", value)

    @property
    def hit_mode(self) -> int:
        """Hit detection mode."""
        p = self._get_projectile()
        return p.hit_mode if p else 0

    @hit_mode.setter
    def hit_mode(self, value: int) -> None:
        self._set_all("hit_mode", value)

    @property
    def vanish_mode(self) -> int:
        """Vanish mode (what happens on impact)."""
        p = self._get_projectile()
        return p.vanish_mode if p else 0

    @vanish_mode.setter
    def vanish_mode(self, value: int) -> None:
        """Set vanish mode with VanishMode enum validation."""
        import traceback
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

        self._set_all("vanish_mode", value)

    @property
    def area_effect_specials(self) -> int:
        """Area effect special flags."""
        p = self._get_projectile()
        return p.area_effect_specials if p else 0

    @area_effect_specials.setter
    def area_effect_specials(self, value: int) -> None:
        self._set_all("area_effect_specials", value)

    @property
    def projectile_arc(self) -> float:
        """Projectile arc (trajectory)."""
        p = self._get_projectile()
        return p.projectile_arc if p else 0.0

    @projectile_arc.setter
    def projectile_arc(self, value: float) -> None:
        self._set_all("projectile_arc", value)

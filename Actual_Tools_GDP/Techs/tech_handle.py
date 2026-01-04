"""
TechHandle - High-level wrapper for Tech objects.

Provides attribute access and effect linking for Technologies.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Tuple

if TYPE_CHECKING:
    from ..backend import DatFile, Tech, ResourceCost

__all__ = ["TechHandle"]


class TechHandle:
    """
    High-level wrapper for Tech objects.

    Provides attribute access for technologies.

    Example:
        >>> tech = tm.get(100)
        >>> tech.research_time = 30
        >>> tech.effect_id = 50
    """

    __slots__ = ("_tech_id", "_dat_file")

    def __init__(self, tech_id: int, dat_file: DatFile) -> None:
        if tech_id < 0:
            raise ValueError(f"tech_id must be non-negative, got {tech_id}")
        object.__setattr__(self, "_tech_id", tech_id)
        object.__setattr__(self, "_dat_file", dat_file)

    def __repr__(self) -> str:
        t = self._tech
        name = t.name if t else "<not found>"
        return f"TechHandle(id={self._tech_id}, name={name!r})"

    # =========================================================================
    # CORE ACCESS
    # =========================================================================

    @property
    def _tech(self) -> Optional[Tech]:
        """Get the underlying Tech object."""
        if 0 <= self._tech_id < len(self._dat_file.techs):
            return self._dat_file.techs[self._tech_id]
        return None

    def exists(self) -> bool:
        """Check if this tech exists."""
        return self._tech is not None

    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================

    @property
    def id(self) -> int:
        """Tech ID."""
        return self._tech_id

    @property
    def name(self) -> str:
        """Technology name."""
        t = self._tech
        return t.name if t else ""

    @name.setter
    def name(self, value: str) -> None:
        t = self._tech
        if t:
            t.name = value

    @property
    def research_time(self) -> int:
        """Research time in seconds."""
        t = self._tech
        return t.research_time if t else 0

    @research_time.setter
    def research_time(self, value: int) -> None:
        t = self._tech
        if t:
            t.research_time = value

    @property
    def effect_id(self) -> int:
        """Effect ID linked to this tech."""
        t = self._tech
        return t.effect_id if t else -1

    @effect_id.setter
    def effect_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.effect_id = value

    @property
    def tech_type(self) -> int:
        """Technology type."""
        t = self._tech
        return t.tech_type if t else 0

    @tech_type.setter
    def tech_type(self, value: int) -> None:
        t = self._tech
        if t:
            t.tech_type = value

    @property
    def icon_id(self) -> int:
        """Icon ID."""
        t = self._tech
        return t.icon_id if t else -1

    @icon_id.setter
    def icon_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.icon_id = value

    @property
    def button_id(self) -> int:
        """Button ID."""
        t = self._tech
        return t.button_id if t else -1

    @button_id.setter
    def button_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.button_id = value

    @property
    def lang_dll_name(self) -> int:
        """Language DLL name ID."""
        t = self._tech
        return t.lang_dll_name if t else 0

    @lang_dll_name.setter
    def lang_dll_name(self, value: int) -> None:
        t = self._tech
        if t:
            t.lang_dll_name = value

    @property
    def lang_dll_description(self) -> int:
        """Language DLL description ID."""
        t = self._tech
        return t.lang_dll_description if t else 0

    @lang_dll_description.setter
    def lang_dll_description(self, value: int) -> None:
        t = self._tech
        if t:
            t.lang_dll_description = value

    @property
    def research_location_id(self) -> int:
        """Building ID where tech is researched."""
        t = self._tech
        return t.research_location_id if t else -1

    @research_location_id.setter
    def research_location_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.research_location_id = value

    @property
    def required_tech_count(self) -> int:
        """Number of required techs."""
        t = self._tech
        return t.required_tech_count if t else 0

    @required_tech_count.setter
    def required_tech_count(self, value: int) -> None:
        t = self._tech
        if t:
            t.required_tech_count = value

    @property
    def required_techs(self) -> Tuple[int, ...]:
        """Required tech IDs."""
        t = self._tech
        return t.required_techs if t else ()

    @required_techs.setter
    def required_techs(self, value: Tuple[int, ...]) -> None:
        t = self._tech
        if t:
            t.required_techs = value

    @property
    def resource_costs(self) -> Tuple[ResourceCost, ...]:
        """Resource costs."""
        t = self._tech
        return t.resource_costs if t else ()

    @resource_costs.setter
    def resource_costs(self, value: Tuple[ResourceCost, ...]) -> None:
        t = self._tech
        if t:
            t.resource_costs = value

    @property
    def civilization_id(self) -> int:
        """Civ restriction (-1 = all)."""
        t = self._tech
        return t.civilization_id if t else -1

    @civilization_id.setter
    def civilization_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.civilization_id = value

    @property
    def full_tech_mode(self) -> int:
        """Full tech mode flag."""
        t = self._tech
        return t.full_tech_mode if t else 0

    @full_tech_mode.setter
    def full_tech_mode(self, value: int) -> None:
        t = self._tech
        if t:
            t.full_tech_mode = value

    # =========================================================================
    # DYNAMIC ACCESS
    # =========================================================================

    def __getattr__(self, name: str) -> Any:
        t = self._tech
        if t and hasattr(t, name):
            return getattr(t, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__slots__:
            object.__setattr__(self, name, value)
            return
        t = self._tech
        if t and hasattr(t, name):
            setattr(t, name, value)
            return
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

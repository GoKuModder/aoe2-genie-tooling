"""
TechHandle - High-level wrapper for Tech objects.

Provides attribute access and effect linking for Technologies.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Tuple

if TYPE_CHECKING:
<<<<<<< HEAD
    from genieutils.datfile import DatFile
    from genieutils.tech import Tech
=======
    from ..backend import DatFile, Tech, ResourceCost
>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3

__all__ = ["TechHandle"]


class TechHandle:
    """
    High-level wrapper for Tech objects.
<<<<<<< HEAD
    
    Provides attribute access for technologies.
    
=======

    Provides attribute access for technologies.

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    Example:
        >>> tech = tm.get(100)
        >>> tech.research_time = 30
        >>> tech.effect_id = 50
    """
<<<<<<< HEAD
    
    __slots__ = ("_tech_id", "_dat_file")
    
=======

    __slots__ = ("_tech_id", "_dat_file")

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    def __init__(self, tech_id: int, dat_file: DatFile) -> None:
        if tech_id < 0:
            raise ValueError(f"tech_id must be non-negative, got {tech_id}")
        object.__setattr__(self, "_tech_id", tech_id)
        object.__setattr__(self, "_dat_file", dat_file)
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    def __repr__(self) -> str:
        t = self._tech
        name = t.name if t else "<not found>"
        return f"TechHandle(id={self._tech_id}, name={name!r})"
<<<<<<< HEAD
    
    # =========================================================================
    # CORE ACCESS
    # =========================================================================
    
=======

    # =========================================================================
    # CORE ACCESS
    # =========================================================================

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def _tech(self) -> Optional[Tech]:
        """Get the underlying Tech object."""
        if 0 <= self._tech_id < len(self._dat_file.techs):
            return self._dat_file.techs[self._tech_id]
        return None
<<<<<<< HEAD
    
    def exists(self) -> bool:
        """Check if this tech exists."""
        return self._tech is not None
    
    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================
    
=======

    def exists(self) -> bool:
        """Check if this tech exists."""
        return self._tech is not None

    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def id(self) -> int:
        """Tech ID."""
        return self._tech_id
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def name(self) -> str:
        """Technology name."""
        t = self._tech
        return t.name if t else ""
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @name.setter
    def name(self, value: str) -> None:
        t = self._tech
        if t:
            t.name = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def research_time(self) -> int:
        """Research time in seconds."""
        t = self._tech
        return t.research_time if t else 0
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @research_time.setter
    def research_time(self, value: int) -> None:
        t = self._tech
        if t:
            t.research_time = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def effect_id(self) -> int:
        """Effect ID linked to this tech."""
        t = self._tech
        return t.effect_id if t else -1
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @effect_id.setter
    def effect_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.effect_id = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def tech_type(self) -> int:
        """Technology type."""
        t = self._tech
        return t.tech_type if t else 0
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @tech_type.setter
    def tech_type(self, value: int) -> None:
        t = self._tech
        if t:
            t.tech_type = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def icon_id(self) -> int:
        """Icon ID."""
        t = self._tech
        return t.icon_id if t else -1
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @icon_id.setter
    def icon_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.icon_id = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def button_id(self) -> int:
        """Button ID."""
        t = self._tech
        return t.button_id if t else -1
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @button_id.setter
    def button_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.button_id = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def lang_dll_name(self) -> int:
        """Language DLL name ID."""
        t = self._tech
        return t.lang_dll_name if t else 0
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @lang_dll_name.setter
    def lang_dll_name(self, value: int) -> None:
        t = self._tech
        if t:
            t.lang_dll_name = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def lang_dll_description(self) -> int:
        """Language DLL description ID."""
        t = self._tech
        return t.lang_dll_description if t else 0
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @lang_dll_description.setter
    def lang_dll_description(self, value: int) -> None:
        t = self._tech
        if t:
            t.lang_dll_description = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def research_location_id(self) -> int:
        """Building ID where tech is researched."""
        t = self._tech
        return t.research_location_id if t else -1
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @research_location_id.setter
    def research_location_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.research_location_id = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def required_tech_count(self) -> int:
        """Number of required techs."""
        t = self._tech
        return t.required_tech_count if t else 0
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @required_tech_count.setter
    def required_tech_count(self, value: int) -> None:
        t = self._tech
        if t:
            t.required_tech_count = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def required_techs(self) -> Tuple[int, ...]:
        """Required tech IDs."""
        t = self._tech
        return t.required_techs if t else ()
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @required_techs.setter
    def required_techs(self, value: Tuple[int, ...]) -> None:
        t = self._tech
        if t:
            t.required_techs = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def resource_costs(self) -> Tuple[ResourceCost, ...]:
        """Resource costs."""
        t = self._tech
        return t.resource_costs if t else ()
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @resource_costs.setter
    def resource_costs(self, value: Tuple[ResourceCost, ...]) -> None:
        t = self._tech
        if t:
            t.resource_costs = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def civilization_id(self) -> int:
        """Civ restriction (-1 = all)."""
        t = self._tech
        return t.civilization_id if t else -1
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @civilization_id.setter
    def civilization_id(self, value: int) -> None:
        t = self._tech
        if t:
            t.civilization_id = value
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @property
    def full_tech_mode(self) -> int:
        """Full tech mode flag."""
        t = self._tech
        return t.full_tech_mode if t else 0
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    @full_tech_mode.setter
    def full_tech_mode(self, value: int) -> None:
        t = self._tech
        if t:
            t.full_tech_mode = value
<<<<<<< HEAD
    
    # =========================================================================
    # DYNAMIC ACCESS
    # =========================================================================
    
=======

    # =========================================================================
    # DYNAMIC ACCESS
    # =========================================================================

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    def __getattr__(self, name: str) -> Any:
        t = self._tech
        if t and hasattr(t, name):
            return getattr(t, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
<<<<<<< HEAD
    
=======

>>>>>>> ca684f02b9ff97a9baad04f5cc1ec0cd347cc3d3
    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__slots__:
            object.__setattr__(self, name, value)
            return
        t = self._tech
        if t and hasattr(t, name):
            setattr(t, name, value)
            return
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

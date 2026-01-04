"""
BuildingWrapper - Building attribute wrapper for UnitHandle.

Provides flat property access to Building attributes:
- construction_graphic, snow_graphic, adjacent_mode, graphics_angle, disappears_when_built, stack_unit_id, foundation_terrain, old_overlap_id, tech_id, can_burn, building_annex, annexes, head_unit, transform_unit, unknown2, transform_sound, construction_sound, wwise_transform_sound_id, wwise_construction_sound_id, garrison_type, garrison_heal_rate, garrison_repair_rate, pile_unit, looting_table

Mirrors genieutils.unit.Building structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Shared.dat_adapter import Unit
    from Datasets.attributes import GarrisonType

__all__ = ["BuildingWrapper"]


class BuildingWrapper:
    """
    Wrapper for Building attributes.
    
    Provides flat property access to building-specific stats.
    Changes propagate to all units in the provided list.
    
    Attributes from genieutils.unit.Building:
        construction_graphic, snow_graphic, adjacent_mode, graphics_angle,
        disappears_when_built, stack_unit_id, foundation_terrain,
        old_overlap_id, tech_id, can_burn, building_annex, annexes,
        head_unit, transform_unit, unknown2, transform_sound,
        construction_sound, wwise_transform_sound_id, wwise_construction_sound_id,
        garrison_type, garrison_heal_rate, garrison_repair_rate,
        pile_unit, looting_table
    """
    
    __slots__ = ("_units",)
    
    def __init__(self, units: List[Unit]) -> None:
        """
        Initialize with list of units to modify.
        
        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)
    
    def _get_building(self) -> Optional[Any]:
        """Get Building from first unit."""
        if self._units and self._units[0].building:
            return self._units[0].building
        return None
    
    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' building."""
        for unit in self._units:
            if unit.building:
                setattr(unit.building, attr, value)
    
    @property
    def construction_graphic(self) -> int:
        """Construction graphic ID."""
        b = self._get_building()
        return b.construction_graphic if b else -1
    
    @construction_graphic.setter
    def construction_graphic(self, value: int) -> None:
        self._set_all("construction_graphic", value)
    
    @property
    def snow_graphic(self) -> int:
        """Snow variant graphic ID."""
        b = self._get_building()
        return b.snow_graphic if b else -1
    
    @snow_graphic.setter
    def snow_graphic(self, value: int) -> None:
        self._set_all("snow_graphic", value)
    
    @property
    def adjacent_mode(self) -> int:
        """Adjacent building mode."""
        b = self._get_building()
        return b.adjacent_mode if b else 0
    
    @adjacent_mode.setter
    def adjacent_mode(self, value: int) -> None:
        self._set_all("adjacent_mode", value)
    
    @property
    def graphics_angle(self) -> int:
        """Graphics angle."""
        b = self._get_building()
        return b.graphics_angle if b else 0
    
    @graphics_angle.setter
    def graphics_angle(self, value: int) -> None:
        self._set_all("graphics_angle", value)
    
    @property
    def disappears_when_built(self) -> int:
        """Whether building disappears when fully built."""
        b = self._get_building()
        return b.disappears_when_built if b else 0
    
    @disappears_when_built.setter
    def disappears_when_built(self, value: int) -> None:
        self._set_all("disappears_when_built", value)
    
    @property
    def stack_unit_id(self) -> int:
        """Stack unit ID."""
        b = self._get_building()
        return b.stack_unit_id if b else -1
    
    @stack_unit_id.setter
    def stack_unit_id(self, value: int) -> None:
        self._set_all("stack_unit_id", value)
    
    @property
    def foundation_terrain(self) -> int:
        """Foundation terrain ID."""
        b = self._get_building()
        return b.foundation_terrain if b else -1
    
    @foundation_terrain.setter
    def foundation_terrain(self, value: int) -> None:
        self._set_all("foundation_terrain", value)
    
    @property
    def old_overlap_id(self) -> int:
        """Old overlap ID."""
        b = self._get_building()
        return b.old_overlap_id if b else -1
    
    @old_overlap_id.setter
    def old_overlap_id(self, value: int) -> None:
        self._set_all("old_overlap_id", value)
    
    @property
    def tech_id(self) -> int:
        """Associated tech ID."""
        b = self._get_building()
        return b.tech_id if b else -1
    
    @tech_id.setter
    def tech_id(self, value: int) -> None:
        self._set_all("tech_id", value)
    
    @property
    def can_burn(self) -> int:
        """Whether building can burn."""
        b = self._get_building()
        return b.can_burn if b else 0
    
    @can_burn.setter
    def can_burn(self, value: int) -> None:
        self._set_all("can_burn", value)
    
    @property
    def head_unit(self) -> int:
        """Head unit ID for annexes."""
        b = self._get_building()
        return b.head_unit if b else -1
    
    @head_unit.setter
    def head_unit(self, value: int) -> None:
        self._set_all("head_unit", value)
    
    @property
    def transform_unit(self) -> int:
        """Transform into unit ID."""
        b = self._get_building()
        return b.transform_unit if b else -1
    
    @transform_unit.setter
    def transform_unit(self, value: int) -> None:
        self._set_all("transform_unit", value)
    
    @property
    def transform_sound(self) -> int:
        """Transform sound ID."""
        b = self._get_building()
        return b.transform_sound if b else -1
    
    @transform_sound.setter
    def transform_sound(self, value: int) -> None:
        self._set_all("transform_sound", value)
    
    @property
    def construction_sound(self) -> int:
        """Construction sound ID."""
        b = self._get_building()
        return b.construction_sound if b else -1
    
    @construction_sound.setter
    def construction_sound(self, value: int) -> None:
        self._set_all("construction_sound", value)
    
    @property
    def wwise_transform_sound_id(self) -> int:
        """Wwise transform sound ID."""
        b = self._get_building()
        return b.wwise_transform_sound_id if b else 0
    
    @wwise_transform_sound_id.setter
    def wwise_transform_sound_id(self, value: int) -> None:
        self._set_all("wwise_transform_sound_id", value)
    
    @property
    def wwise_construction_sound_id(self) -> int:
        """Wwise construction sound ID."""
        b = self._get_building()
        return b.wwise_construction_sound_id if b else 0
    
    @wwise_construction_sound_id.setter
    def wwise_construction_sound_id(self, value: int) -> None:
        self._set_all("wwise_construction_sound_id", value)
    
    @property
    def garrison_type(self) -> int | GarrisonType:
        """Garrison type."""
        b = self._get_building()
        return b.garrison_type if b else 0
    
    @garrison_type.setter
    def garrison_type(self, value: int | GarrisonType) -> None:
        self._set_all("garrison_type", value)
    
    @property
    def garrison_heal_rate(self) -> float:
        """Garrison heal rate."""
        b = self._get_building()
        return b.garrison_heal_rate if b else 0.0
    
    @garrison_heal_rate.setter
    def garrison_heal_rate(self, value: float) -> None:
        self._set_all("garrison_heal_rate", value)
    
    @property
    def garrison_repair_rate(self) -> float:
        """Garrison repair rate."""
        b = self._get_building()
        return b.garrison_repair_rate if b else 0.0
    
    @garrison_repair_rate.setter
    def garrison_repair_rate(self, value: float) -> None:
        self._set_all("garrison_repair_rate", value)
    
    @property
    def pile_unit(self) -> int:
        """Pile unit ID."""
        b = self._get_building()
        return b.pile_unit if b else -1
    
    @pile_unit.setter
    def pile_unit(self, value: int) -> None:
        self._set_all("pile_unit", value)
    
    @property
    def looting_table(self) -> list:
        """Looting table (read-only for now)."""
        b = self._get_building()
        return list(b.looting_table) if b and b.looting_table else []
    

    
    @property
    def annexes(self) -> list:
        """List of annex units (read-only for now)."""
        b = self._get_building()
        return list(b.annexes) if b and b.annexes else []
    
    @property
    def annexes_wrapper(self) -> "AnnexesWrapper":
        """
        Get AnnexesWrapper for managing building annexes.
        
        Usage:
            building.annexes_wrapper.set(0, unit_id=500, x=1.0, y=1.0)
            building.annexes_wrapper[0].unit_id  # Get first annex unit_id
        """
        from Actual_Tools_GDP.Units.wrappers.annex import AnnexesWrapper
        return AnnexesWrapper(self._units)


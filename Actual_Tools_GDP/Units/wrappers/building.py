"""
BuildingWrapper - Building attribute wrapper for UnitHandle.

Ported from building_OLD.py to work with GenieDatParser.

Provides flat property access to BuildingInfo attributes:
- construction_graphic_id, snow_graphic_id, destruction_graphic_id
- adjacent_mode, graphics_angle, disappears_when_built
- stack_unit_id, foundation_terrain_id, completion_tech_id
- garrison_type, garrison_heal_rate, garrison_repair_rate
- sound IDs, annex management, looting_table

Maps to GenieDatParser's BuildingInfo structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from sections.civilization.unit import Unit
    from Datasets.attributes import GarrisonType

__all__ = ["BuildingWrapper"]


class BuildingWrapper:
    """
    Wrapper for BuildingInfo attributes.

    Provides flat property access to building-specific stats.
    Changes propagate to all units in the provided list.

    Attributes from GenieDatParser BuildingInfo:
        construction_sprite_id, snow_sprite_id, destruction_sprite_id,
        destruction_rubble_sprite_id, research_sprite_id, research_complete_sprite_id,
        adjacent_mode, graphics_angle, disappears_when_built, stack_unit_id,
        foundation_terrain_id, old_overlay_id, completion_tech_id, can_burn,
        building_annex, head_unit_id, transform_unit_id, transform_sound_id,
        construction_sound_id, wwise_construction_sound_id, wwise_transform_sound_id,
        garrison_type, garrison_heal_rate, garrison_repair_rate,
        salvage_unit_id, salvage_attributes
    """

    __slots__ = ("_units",)

    def __init__(self, units: List["Unit"]) -> None:
        """
        Initialize with list of units to modify.

        Args:
            units: List of Unit objects to proxy
        """
        object.__setattr__(self, "_units", units)

    def _get_building_info(self) -> Optional[Any]:
        """Get BuildingInfo from first unit."""
        if self._units and hasattr(self._units[0], "building_info") and self._units[0].building_info:
            return self._units[0].building_info
        return None

    def _set_all(self, attr: str, value: Any) -> None:
        """Set attribute on all units' building_info."""
        for unit in self._units:
            if hasattr(unit, "building_info") and unit.building_info:
                setattr(unit.building_info, attr, value)

    # -------------------------
    # Graphics
    # -------------------------

    @property
    def construction_graphic_id(self) -> int:
        """Construction graphic ID."""
        bi = self._get_building_info()
        return bi.construction_sprite_id if bi else -1

    @construction_graphic_id.setter
    def construction_graphic_id(self, value: int) -> None:
        self._set_all("construction_sprite_id", value)

    @property
    def snow_graphic_id(self) -> int:
        """Snow variant graphic ID."""
        bi = self._get_building_info()
        return bi.snow_sprite_id if bi else -1

    @snow_graphic_id.setter
    def snow_graphic_id(self, value: int) -> None:
        self._set_all("snow_sprite_id", value)

    @property
    def destruction_graphic_id(self) -> int:
        """Destruction graphic ID."""
        bi = self._get_building_info()
        return bi.destruction_sprite_id if bi else -1

    @destruction_graphic_id.setter
    def destruction_graphic_id(self, value: int) -> None:
        self._set_all("destruction_sprite_id", value)

    @property
    def destruction_rubble_graphic_id(self) -> int:
        """Destruction rubble graphic ID."""
        bi = self._get_building_info()
        return bi.destruction_rubble_sprite_id if bi else -1

    @destruction_rubble_graphic_id.setter
    def destruction_rubble_graphic_id(self, value: int) -> None:
        self._set_all("destruction_rubble_sprite_id", value)

    @property
    def research_graphic_id(self) -> int:
        """Research graphic ID."""
        bi = self._get_building_info()
        return bi.research_sprite_id if bi else -1

    @research_graphic_id.setter
    def research_graphic_id(self, value: int) -> None:
        self._set_all("research_sprite_id", value)

    @property
    def research_complete_graphic_id(self) -> int:
        """Research complete graphic ID."""
        bi = self._get_building_info()
        return bi.research_complete_sprite_id if bi else -1

    @research_complete_graphic_id.setter
    def research_complete_graphic_id(self, value: int) -> None:
        self._set_all("research_complete_sprite_id", value)

    # -------------------------
    # Building Properties
    # -------------------------

    @property
    def adjacent_mode(self) -> int:
        """Adjacent building mode."""
        bi = self._get_building_info()
        return bi.adjacent_mode if bi else 0

    @adjacent_mode.setter
    def adjacent_mode(self, value: int) -> None:
        self._set_all("adjacent_mode", value)

    @property
    def graphics_angle(self) -> int:
        """Graphics angle."""
        bi = self._get_building_info()
        return bi.graphics_angle if bi else 0

    @graphics_angle.setter
    def graphics_angle(self, value: int) -> None:
        self._set_all("graphics_angle", value)

    @property
    def disappears_when_built(self) -> int:
        """Whether building disappears when fully built."""
        bi = self._get_building_info()
        return bi.disappears_when_built if bi else 0

    @disappears_when_built.setter
    def disappears_when_built(self, value: int) -> None:
        self._set_all("disappears_when_built", value)

    @property
    def stack_unit_id(self) -> int:
        """Stack unit ID."""
        bi = self._get_building_info()
        return bi.stack_unit_id if bi else -1

    @stack_unit_id.setter
    def stack_unit_id(self, value: int) -> None:
        self._set_all("stack_unit_id", value)

    @property
    def foundation_terrain_id(self) -> int:
        """Foundation terrain ID."""
        bi = self._get_building_info()
        return bi.foundation_terrain_id if bi else -1

    @foundation_terrain_id.setter
    def foundation_terrain_id(self, value: int) -> None:
        self._set_all("foundation_terrain_id", value)

    @property
    def old_overlap_id(self) -> int:
        """Old overlap ID (old_overlay_id)."""
        bi = self._get_building_info()
        return bi.old_overlay_id if bi else -1

    @old_overlap_id.setter
    def old_overlap_id(self, value: int) -> None:
        self._set_all("old_overlay_id", value)

    @property
    def tech_id(self) -> int:
        """Associated tech ID (completion_tech_id)."""
        bi = self._get_building_info()
        return bi.completion_tech_id if bi else -1

    @tech_id.setter
    def tech_id(self, value: int) -> None:
        self._set_all("completion_tech_id", value)

    @property
    def completion_tech_id(self) -> int:
        """Completion tech ID."""
        bi = self._get_building_info()
        return bi.completion_tech_id if bi else -1

    @completion_tech_id.setter
    def completion_tech_id(self, value: int) -> None:
        self._set_all("completion_tech_id", value)

    @property
    def can_burn(self) -> int:
        """Whether building can burn."""
        bi = self._get_building_info()
        return bi.can_burn if bi else 0

    @can_burn.setter
    def can_burn(self, value: int) -> None:
        self._set_all("can_burn", value)

    # -------------------------
    # Unit References
    # -------------------------

    @property
    def head_unit_id(self) -> int:
        """Head unit ID for annexes."""
        bi = self._get_building_info()
        return bi.head_unit_id if bi else -1

    @head_unit_id.setter
    def head_unit_id(self, value: int) -> None:
        self._set_all("head_unit_id", value)

    @property
    def transform_unit_id(self) -> int:
        """Transform into unit ID."""
        bi = self._get_building_info()
        return bi.transform_unit_id if bi else -1

    @transform_unit_id.setter
    def transform_unit_id(self, value: int) -> None:
        self._set_all("transform_unit_id", value)

    @property
    def salvage_unit_id(self) -> int:
        """Salvage/pile unit ID."""
        bi = self._get_building_info()
        return bi.salvage_unit_id if bi else -1

    @salvage_unit_id.setter
    def salvage_unit_id(self, value: int) -> None:
        self._set_all("salvage_unit_id", value)

    # Backward compatibility alias
    @property
    def pile_unit_id(self) -> int:
        """Pile unit ID (alias for salvage_unit_id)."""
        return self.salvage_unit_id

    @pile_unit_id.setter
    def pile_unit_id(self, value: int) -> None:
        self.salvage_unit_id = value

    # -------------------------
    # Sound Properties
    # -------------------------

    @property
    def transform_sound_id(self) -> int:
        """Transform sound ID."""
        bi = self._get_building_info()
        return bi.transform_sound_id if bi else -1

    @transform_sound_id.setter
    def transform_sound_id(self, value: int) -> None:
        self._set_all("transform_sound_id", value)

    @property
    def construction_sound_id(self) -> int:
        """Construction sound ID."""
        bi = self._get_building_info()
        return bi.construction_sound_id if bi else -1

    @construction_sound_id.setter
    def construction_sound_id(self, value: int) -> None:
        self._set_all("construction_sound_id", value)

    @property
    def wwise_transform_sound_id(self) -> int:
        """Wwise transform sound ID."""
        bi = self._get_building_info()
        return bi.wwise_transform_sound_id if bi else 0

    @wwise_transform_sound_id.setter
    def wwise_transform_sound_id(self, value: int) -> None:
        self._set_all("wwise_transform_sound_id", value)

    @property
    def wwise_construction_sound_id(self) -> int:
        """Wwise construction sound ID."""
        bi = self._get_building_info()
        return bi.wwise_construction_sound_id if bi else 0

    @wwise_construction_sound_id.setter
    def wwise_construction_sound_id(self, value: int) -> None:
        self._set_all("wwise_construction_sound_id", value)

    # -------------------------
    # Garrison Properties
    # -------------------------

    @property
    def garrison_type(self) -> int:
        """Garrison type."""
        bi = self._get_building_info()
        return bi.garrison_type if bi else 0

    @garrison_type.setter
    def garrison_type(self, value: int) -> None:
        self._set_all("garrison_type", value)

    @property
    def garrison_heal_rate(self) -> float:
        """Garrison heal rate."""
        bi = self._get_building_info()
        return bi.garrison_heal_rate if bi else 0.0

    @garrison_heal_rate.setter
    def garrison_heal_rate(self, value: float) -> None:
        self._set_all("garrison_heal_rate", value)

    @property
    def garrison_repair_rate(self) -> float:
        """Garrison repair rate."""
        bi = self._get_building_info()
        return bi.garrison_repair_rate if bi else 0.0

    @garrison_repair_rate.setter
    def garrison_repair_rate(self, value: float) -> None:
        self._set_all("garrison_repair_rate", value)

    # -------------------------
    # Lists (Read-Only)
    # -------------------------

    @property
    def looting_table(self) -> Any:
        """Looting table (salvage_attributes)."""
        bi = self._get_building_info()
        return bi.salvage_attributes if bi else None

    @looting_table.setter
    def looting_table(self, value: Any) -> None:
        """Set the looting table for all units."""
        self._set_all("salvage_attributes", value)

    @property
    def annexes(self) -> "AnnexesManager":
        """Annexes collection manager."""
        return self.annexes_manager

    @annexes.setter
    def annexes(self, value: List) -> None:
        """Set the entire annexes list for all units."""
        for u in self._units:
            if u.building_info:
                u.building_info.building_annex = value

    @property
    def annexes_manager(self) -> "AnnexesManager":
        """
        Get AnnexesManager for managing building annexes.

        Usage:
            building.annexes_manager.set(0, unit_id=500, x=1.0, y=1.0)
            building.annexes_manager[0].unit_id  # Get first annex unit_id
        """
        from Actual_Tools_GDP.Units.unit_collections import AnnexesManager
        return AnnexesManager(self._units)

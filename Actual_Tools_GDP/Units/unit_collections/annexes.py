"""
AnnexesManager - Collection manager for building annexes.

Manages the `building_info.building_annex` collection (fixed size of 4).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from Actual_Tools_GDP.Units.handles import BuildingAnnexHandle

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["AnnexesManager"]


class AnnexesManager:
    """
    Manager for the annexes collection (building_info.building_annex) of a unit bundle.
    """

    MAX_ANNEXES = 4
    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)

    def _get_building_info(self) -> Optional[Any]:
        if self._units and hasattr(self._units[0], "building_info"):
            return self._units[0].building_info
        return None

    def __len__(self) -> int:
        """Always returns MAX_ANNEXES as the list is fixed size, but counts active ones."""
        bi = self._get_building_info()
        if not bi or not bi.building_annex:
            return 0
        return sum(1 for a in bi.building_annex if a.unit_id >= 0)

    def __getitem__(self, index: int) -> BuildingAnnexHandle:
        if index < 0 or index >= self.MAX_ANNEXES:
            raise IndexError(f"Annex index must be 0-{self.MAX_ANNEXES-1}")
        
        bi = self._get_building_info()
        if bi and bi.building_annex:
            return BuildingAnnexHandle(bi.building_annex[index], index)
        raise RuntimeError("Unit does not have BuildingInfo")

    def __iter__(self) -> Iterator[BuildingAnnexHandle]:
        for i in range(self.MAX_ANNEXES):
            yield self[i]

    def set(self, index: int, unit_id: int, x: float = 0.0, y: float = 0.0) -> BuildingAnnexHandle:
        """Set an annex at specified index for all units."""
        if index < 0 or index >= self.MAX_ANNEXES:
            raise IndexError(f"Annex index must be 0-{self.MAX_ANNEXES-1}")

        for u in self._units:
            if hasattr(u, "building_info") and u.building_info and u.building_info.building_annex:
                annex = u.building_info.building_annex[index]
                annex.unit_id = unit_id
                annex.displacement_x = x
                annex.displacement_y = y
        
        return self[index]

    def get_annex(self, index: int) -> Optional[BuildingAnnexHandle]:
        """
        Get the annex object at specified index.
        
        Args:
            index: Annex index (0-3).
            
        Returns:
            BuildingAnnexHandle if valid, None otherwise.
        """
        if index < 0 or index >= self.MAX_ANNEXES:
            return None
        
        bi = self._get_building_info()
        if bi and bi.building_annex:
            return BuildingAnnexHandle(bi.building_annex[index], index)
        return None

    def get_unit(self, index: int) -> Optional[Any]:
        """
        Get the UnitHandle for the annex at specified index.
        
        Args:
            index: Annex index (0-3).
            
        Returns:
            UnitHandle for the annex unit, or None if not set.
        """
        from Actual_Tools_GDP.Units.unit_handle import UnitHandle
        
        if index < 0 or index >= self.MAX_ANNEXES:
            return None
        
        bi = self._get_building_info()
        if bi and bi.building_annex:
            unit_id = bi.building_annex[index].unit_id
            if unit_id >= 0:
                # Get workspace from first unit
                if self._units and hasattr(self._units[0], '_workspace'):
                    return UnitHandle(self._units[0]._workspace, unit_id)
        return None

    def get_annex_coordinates(self, index: int) -> Optional[tuple]:
        """
        Get the coordinates (x, y) of the annex at specified index.
        
        Args:
            index: Annex index (0-3).
            
        Returns:
            Tuple (x, y) of displacement coordinates, or None if invalid.
        """
        if index < 0 or index >= self.MAX_ANNEXES:
            return None
        
        bi = self._get_building_info()
        if bi and bi.building_annex:
            annex = bi.building_annex[index]
            return (annex.displacement_x, annex.displacement_y)
        return None

    def clear(self, index: int) -> None:
        """Clear annex at index for all units."""
        self.set(index, -1, 0.0, 0.0)

    def clear_all(self) -> None:
        """Clear all 4 annexes."""
        for i in range(self.MAX_ANNEXES):
            self.clear(i)

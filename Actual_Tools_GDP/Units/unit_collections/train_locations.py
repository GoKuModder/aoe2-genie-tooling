"""
TrainLocationsManager - Collection manager for unit training locations.

Manages the `creation_info.train_locations_new` collection across multiple units.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from Actual_Tools_GDP.Units.handles import TrainLocationHandle
from sections.civilization.type_info.creation_info import TrainLocation

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["TrainLocationsManager"]


class TrainLocationsManager:
    """
    Manager for the training locations collection (creation_info.train_locations_new) 
    of a unit bundle.
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)

    def _get_creation_info(self) -> Optional[Any]:
        if self._units and hasattr(self._units[0], "creation_info"):
            return self._units[0].creation_info
        return None

    def __len__(self) -> int:
        ci = self._get_creation_info()
        return len(ci.train_locations_new) if ci and ci.train_locations_new else 0

    def __getitem__(self, index: int) -> TrainLocationHandle:
        ci = self._get_creation_info()
        if ci and 0 <= index < len(ci.train_locations_new):
            return TrainLocationHandle(ci.train_locations_new[index], index)
        raise IndexError(f"Train location index {index} out of range (0-{len(self)-1})")

    def __iter__(self) -> Iterator[TrainLocationHandle]:
        for i in range(len(self)):
            yield self[i]

    def add(
        self,
        unit_id: int,
        train_time: int = 0,
        button_id: int = 0,
        hot_key_id: int = 0,
        **kwargs
    ) -> TrainLocationHandle:
        """Add a training location to all units."""
        # Backward compatibility
        if 'hotkey_id' in kwargs:
             hot_key_id = kwargs.pop('hotkey_id')

        loc_idx = -1
        for u in self._units:
            if hasattr(u, "creation_info") and u.creation_info:
                new_loc = TrainLocation(ver=u.ver)
                new_loc.location_unit_id = unit_id
                new_loc.train_time = train_time
                new_loc.button_id = button_id
                new_loc.hotkey_id = hot_key_id
                u.creation_info.train_locations_new.append(new_loc)
                if loc_idx == -1:
                    loc_idx = len(u.creation_info.train_locations_new) - 1
        
        return self[loc_idx]

    def remove(self, index: int) -> bool:
        """Remove train location at index from all units."""
        removed = False
        for u in self._units:
            if hasattr(u, "creation_info") and u.creation_info:
                if 0 <= index < len(u.creation_info.train_locations_new):
                    u.creation_info.train_locations_new.pop(index)
                    removed = True
        return removed

    def clear(self) -> None:
        """Clear all train locations from all units."""
        for u in self._units:
            if hasattr(u, "creation_info") and u.creation_info:
                u.creation_info.train_locations_new.clear()

    def get_by_unit_id(self, unit_id: int) -> Optional[TrainLocationHandle]:
        """Find the first train location for a specific building unit ID."""
        for handle in self:
            if handle.unit_id == unit_id:
                return handle
        return None

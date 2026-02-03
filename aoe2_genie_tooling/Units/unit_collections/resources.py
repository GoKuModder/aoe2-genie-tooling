"""
ResourcesManager - Collection manager for unit resource storage/carry.

Manages the `unit.resources` collection (fixed size of 3).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from aoe2_genie_tooling.Units.handles import ResourceHandle

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["ResourcesManager"]


class ResourcesManager:
    """
    Manager for the resource collection (unit.resources) of a unit bundle.
    """

    MAX_RESOURCES = 3
    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)

    def __len__(self) -> int:
        """Counts how many resources have a valid type."""
        u = self._units[0]
        if not u or not u.resources:
            return 0
        return sum(1 for r in u.resources if r.type >= 0)

    def __getitem__(self, index: int) -> ResourceHandle:
        if index < 0 or index >= self.MAX_RESOURCES:
            raise IndexError(f"Resource index must be 0-{self.MAX_RESOURCES-1}")
        
        u = self._units[0]
        if u and u.resources:
            return ResourceHandle(u.resources[index], index)
        raise RuntimeError("No units in bundle")

    def __iter__(self) -> Iterator[ResourceHandle]:
        for i in range(self.MAX_RESOURCES):
            yield self[i]

    def set(self, index: int, type_id: int, quantity: float, store_mode: int = 0) -> ResourceHandle:
        """Set a resource entry at specified index for all units."""
        if index < 0 or index >= self.MAX_RESOURCES:
            raise IndexError(f"Resource index must be 0-{self.MAX_RESOURCES-1}")

        for u in self._units:
            if u.resources:
                res = u.resources[index]
                res.type = type_id
                res.quantity = quantity
                res.store_mode = store_mode
        
        return self[index]

    def clear(self, index: int) -> None:
        """Clear a resource slot (set type to -1)."""
        self.set(index, -1, 0.0, 0)

    def clear_all(self) -> None:
        """Clear all 3 resource slots."""
        for i in range(self.MAX_RESOURCES):
            self.clear(i)

    def resource_1(self, type: int, quantity: float, flag: int = 0) -> ResourceHandle:
        """Convenience method for the first resource slot."""
        return self.set(0, type, quantity, flag)

    def resource_2(self, type: int, quantity: float, flag: int = 0) -> ResourceHandle:
        """Convenience method for the second resource slot."""
        return self.set(1, type, quantity, flag)

    def resource_3(self, type: int, quantity: float, flag: int = 0) -> ResourceHandle:
        """Convenience method for the third resource slot."""
        return self.set(2, type, quantity, flag)

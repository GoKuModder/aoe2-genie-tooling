"""
CostsManager - Collection manager for unit resource costs.

Manages the `creation_info.costs` collection (fixed size of 3).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from aoe2_genie_tooling.Units.handles import CostHandle

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["CostsManager"]


class CostsManager:
    """
    Manager for the resource costs collection (creation_info.costs) of a unit bundle.
    """

    MAX_COSTS = 3
    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)

    def _get_creation_info(self) -> Optional[Any]:
        if self._units and hasattr(self._units[0], "creation_info"):
            return self._units[0].creation_info
        return None

    def __len__(self) -> int:
        """Counts how many costs have a valid resource_id."""
        ci = self._get_creation_info()
        if not ci or not ci.costs:
            return 0
        return sum(1 for c in ci.costs if c.resource_id >= 0)

    def __getitem__(self, index: int) -> CostHandle:
        if index < 0 or index >= self.MAX_COSTS:
            raise IndexError(f"Cost index must be 0-{self.MAX_COSTS-1}")
        
        ci = self._get_creation_info()
        if ci and ci.costs:
            return CostHandle(ci.costs[index], index)
        raise RuntimeError("Unit does not have CreationInfo")

    def __iter__(self) -> Iterator[CostHandle]:
        for i in range(self.MAX_COSTS):
            yield self[i]

    def set(self, index: int, resource_id: int, quantity: int, deduct_flag: int = 1) -> CostHandle:
        """Set a resource cost at specified index for all units."""
        if index < 0 or index >= self.MAX_COSTS:
            raise IndexError(f"Cost index must be 0-{self.MAX_COSTS-1}")

        for u in self._units:
            if hasattr(u, "creation_info") and u.creation_info and u.creation_info.costs:
                cost = u.creation_info.costs[index]
                cost.resource_id = resource_id
                cost.quantity = quantity
                cost.deduct_flag = deduct_flag
        
        return self[index]

    def clear(self, index: int) -> None:
        """Clear a cost slot (set resource_id to -1)."""
        self.set(index, -1, 0, 1)

    def clear_all(self) -> None:
        """Clear all 3 cost slots."""
        for i in range(self.MAX_COSTS):
            self.clear(i)

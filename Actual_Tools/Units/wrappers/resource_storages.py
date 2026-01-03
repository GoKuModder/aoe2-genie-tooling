"""
ResourceStoragesWrapper - Resource storage attribute wrapper for UnitHandle.

Provides access to the 3 fixed Resource Storage slots.
- unit.resource_storages.add(type, amount, flag)
- unit.resource_storages.resource_1(type, amount, flag)
- unit.resource_storages[Resource.FOOD] = 100

Mirrors genieutils.unit.ResourceStorage structure (fixed tuple of 3).
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional
from genieutils.unit import ResourceStorage

if TYPE_CHECKING:
    from genieutils.unit import Unit
    from Datasets.resources import Resource
    from Datasets.store_modes import StoreMode

__all__ = ["ResourceStoragesWrapper"]


class ResourceStoragesWrapper:
    """
    Wrapper for ResourceStorages (inventory/cost/capacity).
    
    Genie Units have exactly 3 resource storage slots.
    
    Usage:
        handle.resource_storages[Resource.FOOD] = 50
        handle.resource_storages.resource_1(type=Resource.GOLD, amount=100, flag=1)
    """
    
    __slots__ = ("_units",)
    
    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)
    
    def __call__(self, resource_type: int | Resource = -1, amount: float = 0.0, flag: int | StoreMode = 0, **kwargs) -> None:
        """Add storage (alias for add)."""
        if "type" in kwargs:
            resource_type = kwargs["type"]
        self.add_storage(resource_type, amount, flag)

    def _set_slot(self, index: int, type_: int, amount: float, flag: int) -> None:
        """Set specific slot (0-2) on all units."""
        for unit in self._units:
            current = list(unit.resource_storages)
            # Ensure enough slots (though it should be 3)
            while len(current) <= index:
                 current.append(ResourceStorage(0, 0.0, 0))
            
            current[index] = ResourceStorage(int(type_), amount, int(flag))
            
            # Ensure max 3? Unit definition expects tuple of 3.
            if len(current) > 3:
                current = current[:3]
                
            unit.resource_storages = tuple(current)

    def resource_1(self, type: int | Resource = 0, amount: float = 0.0, flag: int | StoreMode = 0) -> None:
        """Set 1st resource storage slot."""
        self._set_slot(0, type, amount, flag)

    def resource_2(self, type: int | Resource = 0, amount: float = 0.0, flag: int | StoreMode = 0) -> None:
        """Set 2nd resource storage slot."""
        self._set_slot(1, type, amount, flag)

    def resource_3(self, type: int | Resource = 0, amount: float = 0.0, flag: int | StoreMode = 0) -> None:
        """Set 3rd resource storage slot."""
        self._set_slot(2, type, amount, flag)

    def add_storage(self, resource_type: int | Resource, amount: float, flag: int | StoreMode) -> None:
        """
        Add or update storage.
        Finds first slot with same type, OR first empty slot (type 0), OR overwrites last slot?
        Prefers updating existing type.
        """
        r_type = int(resource_type)
        r_flag = int(flag)
        
        for unit in self._units:
            current = list(unit.resource_storages)
            found_idx = -1
            empty_idx = -1
            
            for i, s in enumerate(current):
                if s.type == r_type:
                    found_idx = i
                    break
                if s.type == 0 and empty_idx == -1:
                    empty_idx = i
            
            target_idx = -1
            if found_idx != -1:
                target_idx = found_idx
            elif empty_idx != -1:
                target_idx = empty_idx
            else:
                # No empty slot, maybe overwrite last? Or do nothing?
                # Better to use slots explicitly if full.
                # We'll overwrite slot 2 (last) if full, or print warning?
                # Silent overwrite of last slot is dangerous.
                # Let's overwrite last slot 2 as fallback.
                target_idx = 2
            
            if 0 <= target_idx < len(current):
                current[target_idx] = ResourceStorage(r_type, amount, r_flag)
                unit.resource_storages = tuple(current)

    def __getitem__(self, resource_type: int) -> float:
        """Get amount of specific resource type (summed across slots? usually unique)."""
        if not self._units: return 0.0
        total = 0.0
        for s in self._units[0].resource_storages:
            if s.type == resource_type:
                total += s.amount
        return total

    def __setitem__(self, resource_type: int, amount: float) -> None:
        """Set amount of resource type (updates existing or adds to new slot). Flag defaults to 0."""
        self.add_storage(resource_type, amount, 0)

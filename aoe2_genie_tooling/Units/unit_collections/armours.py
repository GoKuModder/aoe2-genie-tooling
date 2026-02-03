"""
ArmoursManager - Collection manager for unit armours.

Manages the `combat_info.armors` collection across multiple units.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from aoe2_genie_tooling.Units.handles import ArmourHandle
from sections.civilization.type_info.damage_class import DamageClass

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["ArmoursManager"]


class ArmoursManager:
    """
    Manager for the armour collection (combat_info.armors) of a unit bundle.
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)

    def _get_combat_info(self) -> Optional[Any]:
        if self._units and hasattr(self._units[0], "combat_info"):
            return self._units[0].combat_info
        return None

    def __len__(self) -> int:
        ci = self._get_combat_info()
        return len(ci.armors) if ci and ci.armors else 0

    def __getitem__(self, index: int) -> ArmourHandle:
        ci = self._get_combat_info()
        if ci and 0 <= index < len(ci.armors):
            return ArmourHandle(ci.armors[index], index)
        raise IndexError(f"Armour index {index} out of range (0-{len(self)-1})")

    def __iter__(self) -> Iterator[ArmourHandle]:
        for i in range(len(self)):
            yield self[i]

    def add(self, class_id: int, amount: int) -> ArmourHandle:
        """Add an armour entry to all units.
        
        IMPORTANT: Uses setattr with a new list instead of append() because
        bfp_rs Retriever lists share internal storage across clones.
        """
        armour_idx = -1
        for u in self._units:
            if hasattr(u, "combat_info") and u.combat_info:
                new_armour = DamageClass()
                new_armour.id = class_id
                new_armour.amount = amount
                
                # CRITICAL: Don't use append()! bfp_rs lists share internal storage.
                current_armors = list(u.combat_info.armors)
                current_armors.append(new_armour)
                u.combat_info.armors = current_armors  # setattr triggers bfp_rs copy
                
                if armour_idx == -1:
                    armour_idx = len(u.combat_info.armors) - 1
        
        return self[armour_idx]

    def remove(self, index: int) -> bool:
        """Remove armour at index from all units.
        
        IMPORTANT: Uses setattr with a new list instead of pop() because
        bfp_rs Retriever lists share internal storage across clones.
        """
        removed = False
        for u in self._units:
            if hasattr(u, "combat_info") and u.combat_info:
                current_armors = list(u.combat_info.armors)
                if 0 <= index < len(current_armors):
                    current_armors.pop(index)
                    u.combat_info.armors = current_armors  # setattr triggers bfp_rs copy
                    removed = True
        return removed

    def clear(self) -> None:
        """Clear all armours from all units.
        
        IMPORTANT: Uses setattr with empty list instead of clear() because
        bfp_rs Retriever lists share internal storage across clones.
        """
        for u in self._units:
            if hasattr(u, "combat_info") and u.combat_info:
                u.combat_info.armors = []  # setattr triggers bfp_rs copy

    def get_by_class(self, class_id: int) -> Optional[ArmourHandle]:
        """Get armour handle by damage class ID."""
        for i, handle in enumerate(self):
            if handle.class_ == class_id:
                return handle
        return None

    def set(self, class_id: int, amount: int) -> ArmourHandle:
        """Update existing armour if it exists, otherwise add it."""
        existing = self.get_by_class(class_id)
        if existing:
            for u in self._units:
                if hasattr(u, "combat_info") and u.combat_info:
                    for arm in u.combat_info.armors:
                        if arm.id == class_id:
                            arm.amount = amount
                            break
            return existing
        return self.add(class_id, amount)

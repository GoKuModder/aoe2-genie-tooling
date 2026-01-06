"""
AttacksManager - Collection manager for unit attacks.

Manages the `combat_info.attacks` collection across multiple units.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from Actual_Tools_GDP.Units.handles import AttackHandle
from sections.civilization.type_info.damage_class import DamageClass

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["AttacksManager"]


class AttacksManager:
    """
    Manager for the attack collection (combat_info.attacks) of a unit bundle.
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
        return len(ci.attacks) if ci and ci.attacks else 0

    def __getitem__(self, index: int) -> AttackHandle:
        ci = self._get_combat_info()
        if ci and 0 <= index < len(ci.attacks):
            return AttackHandle(ci.attacks[index], index)
        raise IndexError(f"Attack index {index} out of range (0-{len(self)-1})")

    def __iter__(self) -> Iterator[AttackHandle]:
        for i in range(len(self)):
            yield self[i]

    def add(self, class_id: int, amount: int) -> AttackHandle:
        """Add an attack entry to all units."""
        attack_idx = -1
        for u in self._units:
            if hasattr(u, "combat_info") and u.combat_info:
                new_attack = DamageClass()
                new_attack.id = class_id
                new_attack.amount = amount
                u.combat_info.attacks.append(new_attack)
                if attack_idx == -1:
                    attack_idx = len(u.combat_info.attacks) - 1
        
        return self[attack_idx]

    def remove(self, index: int) -> bool:
        """Remove attack at index from all units."""
        removed = False
        for u in self._units:
            if hasattr(u, "combat_info") and u.combat_info:
                if 0 <= index < len(u.combat_info.attacks):
                    u.combat_info.attacks.pop(index)
                    removed = True
        return removed

    def clear(self) -> None:
        """Clear all attacks from all units."""
        for u in self._units:
            if hasattr(u, "combat_info") and u.combat_info:
                u.combat_info.attacks.clear()

    def get_by_class(self, class_id: int) -> Optional[AttackHandle]:
        """Get attack handle by damage class ID."""
        for i, handle in enumerate(self):
            if handle.class_ == class_id:
                return handle
        return None

    def set(self, class_id: int, amount: int) -> AttackHandle:
        """Update existing attack if it exists, otherwise add it."""
        existing = self.get_by_class(class_id)
        if existing:
            # Updating via handle will update the first unit, 
            # we need to update all units if we want collective 'set' behavior.
            for u in self._units:
                if hasattr(u, "combat_info") and u.combat_info:
                    for atk in u.combat_info.attacks:
                        if atk.id == class_id:
                            atk.amount = amount
                            break
            return existing
        return self.add(class_id, amount)

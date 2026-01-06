"""
DamageGraphicsManager - Collection manager for unit damage graphics.

Manages the `unit.damage_sprites` collection across multiple units.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Iterator

from Actual_Tools_GDP.Units.handles import DamageGraphicHandle
from sections.civilization.unit_damage_sprite import UnitDamageSprite

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

__all__ = ["DamageGraphicsManager"]


class DamageGraphicsManager:
    """
    Manager for the damage graphics collection (unit.damage_sprites) of a unit bundle.
    """

    __slots__ = ("_units",)

    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)

    def __len__(self) -> int:
        return len(self._units[0].damage_sprites) if self._units and self._units[0].damage_sprites else 0

    def __getitem__(self, index: int) -> DamageGraphicHandle:
        u = self._units[0]
        if u and 0 <= index < len(u.damage_sprites):
            return DamageGraphicHandle(u.damage_sprites[index], index)
        raise IndexError(f"Damage graphic index {index} out of range (0-{len(self)-1})")

    def __iter__(self) -> Iterator[DamageGraphicHandle]:
        for i in range(len(self)):
            yield self[i]

    def add(self, graphic_id: int, damage_percent: int, apply_mode: int = 0) -> DamageGraphicHandle:
        """Add a damage graphic to all units."""
        dg_idx = -1
        for u in self._units:
            new_dg = UnitDamageSprite(ver=u.ver)
            new_dg.sprite_id = graphic_id
            new_dg.damage_percent = damage_percent
            new_dg.apply_mode = apply_mode
            u.damage_sprites.append(new_dg)
            if dg_idx == -1:
                dg_idx = len(u.damage_sprites) - 1
        
        return self[dg_idx]

    def remove(self, index: int) -> bool:
        """Remove damage graphic at index from all units."""
        removed = False
        for u in self._units:
            if 0 <= index < len(u.damage_sprites):
                u.damage_sprites.pop(index)
                removed = True
        return removed

    def clear(self) -> None:
        """Clear all damage graphics from all units."""
        for u in self._units:
            u.damage_sprites.clear()

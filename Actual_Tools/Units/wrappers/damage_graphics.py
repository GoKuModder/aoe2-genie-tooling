"""
DamageGraphicsWrapper - Damage graphics collection management for units.

Provides methods to manage damage graphics:
- add_damage_graphic: Add a new damage graphic
- remove_damage_graphic: Remove by graphic ID
- get_damage_graphics: Get all damage graphics
- clear_damage_graphics: Remove all

Mirrors genieutils.unit.DamageGraphic structure.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

if TYPE_CHECKING:
    from genieutils.unit import Unit, DamageGraphic

__all__ = ["DamageGraphicsWrapper"]


class DamageGraphicsWrapper:
    """
    Wrapper for managing Unit.damage_graphics collection.
    
    Provides methods to add and manipulate damage graphics.
    Changes propagate to all units in the provided list.
    """
    
    __slots__ = ("_units",)
    
    def __init__(self, units: List[Unit]) -> None:
        object.__setattr__(self, "_units", units)
    
    def add_damage_graphic(
        self,
        graphic_id: int,
        damage_percent: int,
        apply_mode: int = 0,
    ) -> None:
        """
        Add a new damage graphic to all units.
        
        Args:
            graphic_id: Graphic ID to display
            damage_percent: Damage percentage at which to show (0-100)
            apply_mode: Apply mode
        """
        from genieutils.unit import DamageGraphic
        
        new_damage_graphic = DamageGraphic(
            graphic_id=graphic_id,
            damage_percent=damage_percent,
            apply_mode=apply_mode,
        )
        
        for unit in self._units:
            import copy
            unit.damage_graphics.append(copy.deepcopy(new_damage_graphic))
    
    def remove_damage_graphic(self, graphic_id: int) -> bool:
        """
        Remove damage graphics with specified graphic ID.
        
        Args:
            graphic_id: Graphic ID to remove
        
        Returns:
            True if any were removed, False otherwise
        """
        found = False
        for unit in self._units:
            original_len = len(unit.damage_graphics)
            unit.damage_graphics = [
                dg for dg in unit.damage_graphics if dg.graphic_id != graphic_id
            ]
            if len(unit.damage_graphics) < original_len:
                found = True
        return found
    
    def get_damage_graphics(self) -> List[DamageGraphic]:
        """
        Get all damage graphics from primary unit.
        
        Returns:
            List of DamageGraphic objects
        """
        if self._units and self._units[0]:
            return list(self._units[0].damage_graphics)
        return []
    
    def clear_damage_graphics(self) -> None:
        """Remove all damage graphics from all units."""
        for unit in self._units:
            unit.damage_graphics.clear()
    
    def get_by_damage_percent(self, damage_percent: int) -> Optional[DamageGraphic]:
        """
        Get damage graphic by damage percentage.
        
        Args:
            damage_percent: Damage percentage to search for
        
        Returns:
            DamageGraphic if found, None otherwise
        """
        if self._units and self._units[0]:
            for dg in self._units[0].damage_graphics:
                if dg.damage_percent == damage_percent:
                    return dg
        return None

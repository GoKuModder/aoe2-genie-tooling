"""
TechHandle - Wrapper for individual Tech objects.

Techs are single-tier objects with properties like name, effect_id, costs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

__all__ = ["TechHandle"]


class CostBuilder:
    """Builder for setting tech costs with nice API: tech.set_cost.cost_1(type, amount)"""
    
    def __init__(self, tech_handle: 'TechHandle') -> None:
        self._tech_handle = tech_handle
    
    def cost_1(self, resource_type: int, amount: int, deduct: bool = True) -> None:
        """
        Set cost slot 1.
        
        Args:
            resource_type: 0=Food, 1=Wood, 2=Stone, 3=Gold
            amount: Quantity
            deduct: Whether to deduct (default True)
        """
        self._set(0, resource_type, amount, deduct)
    
    def cost_2(self, resource_type: int, amount: int, deduct: bool = True) -> None:
        """Set cost slot 2."""
        self._set(1, resource_type, amount, deduct)
    
    def cost_3(self, resource_type: int, amount: int, deduct: bool = True) -> None:
        """Set cost slot 3."""
        self._set(2, resource_type, amount, deduct)
    
    def _set(self, slot: int, resource_type: int, amount: int, deduct: bool) -> None:
        costs = self._tech_handle._tech.costs
        costs[slot].resource_id = resource_type
        costs[slot].quantity = amount
        costs[slot].deduct_flag = 1 if deduct else 0


class TechHandle:
    """
    Handle for a single tech.
    
    Provides direct attribute access to the underlying Tech object.
    """
    
    def __init__(self, workspace: GenieWorkspace, tech_id: int) -> None:
        """Initialize TechHandle."""
        object.__setattr__(self, '_workspace', workspace)
        object.__setattr__(self, '_id', tech_id)
        object.__setattr__(self, '_tech', workspace.dat.techs[tech_id])
    
    @property
    def id(self) -> int:
        """Get the tech ID."""
        return self._id
    
    @property
    def workspace(self) -> GenieWorkspace:
        """Get the workspace."""
        return self._workspace

    @property
    def set_cost(self) -> CostBuilder:
        """
        Builder for setting costs.
        
        Example:
            tech.set_cost.cost_1(3, 100)  # 100 Gold
            tech.set_cost.cost_2(0, 50)   # 50 Food
        """
        return CostBuilder(self)

    @property
    def name(self) -> str:
        """Get the tech name."""
        try:
            return self._tech.name
        except Exception:
            return ""

    @name.setter
    def name(self, value: str) -> None:
        """Set the tech name."""
        try:
            self._tech.name = value
        except Exception:
            pass

    @property
    def effect_id(self) -> int:
        """Get the linked effect ID."""
        return self._tech.effect_id

    @effect_id.setter
    def effect_id(self, value: int) -> None:
        """Set the linked effect ID."""
        self._tech.effect_id = value

    @property
    def research_time(self) -> int:
        """Get research time."""
        try:
            return self._tech.research_time
        except Exception:
            return 0

    @research_time.setter
    def research_time(self, value: int) -> None:
        """Set research time."""
        try:
            self._tech.research_time = value
        except Exception:
            pass

    @property
    def cost_1(self) -> Any:
        """Get first cost slot."""
        return self._tech.costs[0]

    @property
    def cost_2(self) -> Any:
        """Get second cost slot."""
        return self._tech.costs[1]

    @property
    def cost_3(self) -> Any:
        """Get third cost slot."""
        return self._tech.costs[2]

    @property
    def costs(self) -> list:
        """Get the cost array (3 TechCost objects). Use set_cost.cost_1() etc for easier modification."""
        return self._tech.costs

    def clear_cost(self, slot: int) -> None:
        """
        Clear a cost slot (set to 0 quantity).
        
        Args:
            slot: Cost slot (0, 1, or 2)
        """
        if not (0 <= slot <= 2):
            raise ValueError(f"slot must be 0-2, got {slot}")
        self._tech.costs[slot].resource_id = 0
        self._tech.costs[slot].quantity = 0
        self._tech.costs[slot].deduct_flag = 0

    def clear_all_costs(self) -> None:
        """Clear all cost slots."""
        for i in range(3):
            self.clear_cost(i)

    def get_cost(self, slot: int) -> tuple:
        """
        Get cost at slot as tuple.
        
        Args:
            slot: Cost slot (0, 1, or 2)
            
        Returns:
            Tuple of (resource_id, quantity, deduct_flag)
        """
        if not (0 <= slot <= 2):
            raise ValueError(f"slot must be 0-2, got {slot}")
        c = self._tech.costs[slot]
        return (c.resource_id, c.quantity, c.deduct_flag)

    @property
    def required_tech_ids(self) -> tuple:
        """Get required tech IDs (6 slots, -1 means empty). Use set_required_tech() to modify."""
        return tuple(self._tech.required_tech_ids)

    def set_required_tech(self, slot: int, tech_id: int) -> None:
        """
        Set a required tech ID at a specific slot.
        
        Args:
            slot: Slot index (0-5)
            tech_id: Tech ID to require (-1 to clear the slot)
            
        Raises:
            ValueError: If slot is not in range 0-5
        """
        max_slot = len(self._tech.required_tech_ids) - 1
        if not (0 <= slot <= max_slot):
            raise ValueError(f"slot must be 0-{max_slot}, got {slot}")
        self._tech.required_tech_ids[slot] = tech_id

    def clear_required_techs(self) -> None:
        """Clear all required tech slots (set to -1)."""
        for i in range(len(self._tech.required_tech_ids)):
            self._tech.required_tech_ids[i] = -1

    @property
    def icon_id(self) -> int:
        """Get icon ID."""
        return self._tech.icon_id

    @icon_id.setter
    def icon_id(self, value: int) -> None:
        self._tech.icon_id = value

    @property
    def type(self) -> int:
        """Get tech type."""
        return self._tech.type

    @type.setter
    def type(self, value: int) -> None:
        self._tech.type = value

    @property
    def min_required_techs(self) -> int:
        """Get minimum required techs count."""
        return self._tech.min_required_techs

    @min_required_techs.setter
    def min_required_techs(self, value: int) -> None:
        self._tech.min_required_techs = value

    @property
    def civilization_id(self) -> int:
        """Get civilization ID (-1 = all civs)."""
        return self._tech.civilization_id

    @civilization_id.setter
    def civilization_id(self, value: int) -> None:
        self._tech.civilization_id = value

    @property
    def full_tech_tree_mode(self) -> int:
        """Get full tech tree mode."""
        return self._tech.full_tech_tree_mode

    @full_tech_tree_mode.setter
    def full_tech_tree_mode(self, value: int) -> None:
        self._tech.full_tech_tree_mode = value

    @property
    def location_unit_id(self) -> int:
        """Get research location unit ID (pre-DE versions only)."""
        try:
            return self._tech.location_unit_id
        except Exception:
            return -1

    @location_unit_id.setter
    def location_unit_id(self, value: int) -> None:
        try:
            self._tech.location_unit_id = value
        except Exception:
            pass

    @property
    def name_str_id(self) -> int:
        """Get language file name string ID."""
        return self._tech.name_str_id

    @name_str_id.setter
    def name_str_id(self, value: int) -> None:
        self._tech.name_str_id = value

    @property
    def description_str_id(self) -> int:
        """Get language file description string ID."""
        return self._tech.description_str_id

    @description_str_id.setter
    def description_str_id(self, value: int) -> None:
        self._tech.description_str_id = value

    @property
    def help_str_id(self) -> int:
        """Get language file help string ID."""
        return self._tech.help_str_id

    @help_str_id.setter
    def help_str_id(self, value: int) -> None:
        self._tech.help_str_id = value

    @property
    def tech_tree_str_id(self) -> int:
        """Get tech tree string ID."""
        return self._tech.tech_tree_str_id

    @tech_tree_str_id.setter
    def tech_tree_str_id(self, value: int) -> None:
        self._tech.tech_tree_str_id = value

    @property
    def hotkey_str_id(self) -> int:
        """Get hotkey string ID (pre-DE versions only)."""
        try:
            return self._tech.hotkey_str_id
        except Exception:
            return -1

    @hotkey_str_id.setter
    def hotkey_str_id(self, value: int) -> None:
        try:
            self._tech.hotkey_str_id = value
        except Exception:
            pass

    @property
    def button_id(self) -> int:
        """Get button ID (pre-DE versions only)."""
        try:
            return self._tech.button_id
        except Exception:
            return 0

    @button_id.setter
    def button_id(self, value: int) -> None:
        try:
            self._tech.button_id = value
        except Exception:
            pass

    @property
    def repeatable(self) -> bool:
        """Get if tech is repeatable (DE only)."""
        try:
            return self._tech.repeatable
        except Exception:
            return False

    @repeatable.setter
    def repeatable(self, value: bool) -> None:
        try:
            self._tech.repeatable = value
        except Exception:
            pass

    @property
    def name2(self) -> str:
        """Get secondary name (SWGB only)."""
        try:
            return self._tech.name2
        except Exception:
            return ""

    @name2.setter
    def name2(self, value: str) -> None:
        try:
            self._tech.name2 = value
        except Exception:
            pass

    @property
    def research_locations(self) -> list:
        """
        Get research locations list (DE v8.8+ only).
        
        For older versions, use location_unit_id and research_time directly.
        """
        try:
            return self._tech.research_locations
        except Exception:
            return []

    def get_research_location(self, location_id: int) -> Optional[Any]:
        """
        Get a specific research location by index.
        
        Args:
            location_id: Index of the research location (0-based)
            
        Returns:
            ResearchLocation object or None if not found
        """
        try:
            if 0 <= location_id < len(self._tech.research_locations):
                return self._tech.research_locations[location_id]
        except Exception:
            pass
        return None

    def add_research_location(
        self,
        location_unit_id: int = -1,
        research_time: int = 0,
        button_id: int = 0,
        hotkey_str_id: int = -1,
    ) -> Optional[Any]:
        """
        Add a new research location.
        
        Args:
            location_unit_id: Building unit ID where this can be researched
            research_time: Time to research at this location
            button_id: UI button position
            hotkey_str_id: Hotkey string ID
            
        Returns:
            The new ResearchLocation object, or None if failed
        """
        try:
            from sections.tech.tech import ResearchLocation
            
            new_loc = ResearchLocation(ver=self._tech.ver)
            new_loc.location_unit_id = location_unit_id
            new_loc.research_time = research_time
            new_loc.button_id = button_id
            new_loc.hotkey_str_id = hotkey_str_id
            
            self._tech.research_locations.append(new_loc)
            return new_loc
        except Exception:
            return None

    def remove_research_location(self, location_id: int) -> bool:
        """
        Remove a research location by index.
        
        Args:
            location_id: Index of the research location to remove
            
        Returns:
            True if removed, False if failed or out of range
        """
        try:
            if 0 <= location_id < len(self._tech.research_locations):
                del self._tech.research_locations[location_id]
                return True
        except Exception:
            pass
        return False

    def copy_research_location(self, location_id: int, target_index: Optional[int] = None) -> Optional[Any]:
        """
        Copy a research location.
        
        Args:
            location_id: Source location index
            target_index: Destination index. If None, appends to end.
            
        Returns:
            The new ResearchLocation object, or None if failed
        """
        try:
            if not (0 <= location_id < len(self._tech.research_locations)):
                return None
                
            source = self._tech.research_locations[location_id]
            
            from sections.tech.tech import ResearchLocation
            new_loc = ResearchLocation(ver=source.ver)
            new_loc.location_unit_id = source.location_unit_id
            new_loc.research_time = source.research_time
            new_loc.button_id = source.button_id
            new_loc.hotkey_str_id = source.hotkey_str_id
            
            if target_index is None:
                self._tech.research_locations.append(new_loc)
            else:
                target_index = max(0, min(target_index, len(self._tech.research_locations)))
                self._tech.research_locations.insert(target_index, new_loc)
                
            return new_loc
        except Exception:
            return None

    def move_research_location(self, source_index: int, target_index: int) -> bool:
        """
        Move a research location to a new position.
        
        Args:
            source_index: Index of location to move
            target_index: New index position
            
        Returns:
            True if moved, False if out of range
        """
        try:
            if not (0 <= source_index < len(self._tech.research_locations)):
                return False
                
            target_index = max(0, min(target_index, len(self._tech.research_locations) - 1))
            
            if source_index == target_index:
                return True
                
            obj = self._tech.research_locations.pop(source_index)
            self._tech.research_locations.insert(target_index, obj)
            return True
        except Exception:
            return False

    def clear_research_locations(self) -> None:
        """Remove all research locations."""
        try:
            self._tech.research_locations = []
        except Exception:
            pass

    def exists(self) -> bool:
        """Check if this tech entry exists."""
        return self._tech is not None

    def __getattr__(self, name: str) -> Any:
        """Get attribute from underlying tech."""
        return getattr(self._tech, name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute on underlying tech."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._tech, name, value)
    
    def __repr__(self) -> str:
        if not self.exists():
            return f"TechHandle(id={self._id}, status=DELETED)"
        return f"TechHandle(id={self._id}, name='{self.name}')"

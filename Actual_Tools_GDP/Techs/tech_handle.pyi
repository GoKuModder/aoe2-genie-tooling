"""Type stubs for TechHandle - enables IDE autocomplete"""
from typing import Any, Optional

class TechHandle:
    """Handle for a single tech."""
    
    @property
    def id(self) -> int:
        """Get the tech ID."""
        ...
    
    @property
    def name(self) -> str:
        """Get the tech name."""
        ...

    @name.setter
    def name(self, value: str) -> None:
        ...

    @property
    def effect_id(self) -> int:
        """Get the linked effect ID."""
        ...

    @effect_id.setter
    def effect_id(self, value: int) -> None:
        ...

    @property
    def research_time(self) -> int:
        """Get research time."""
        ...

    @research_time.setter
    def research_time(self, value: int) -> None:
        ...

    @property
    def cost_1(self) -> Any:
        """Get first cost slot."""
        ...

    @property
    def cost_2(self) -> Any:
        """Get second cost slot."""
        ...

    @property
    def cost_3(self) -> Any:
        """Get third cost slot."""
        ...

    @property
    def costs(self) -> list:
        """Get the cost array (3 TechCost objects). Use cost_1, cost_2, cost_3 for cleaner access."""
        ...

    @property
    def required_tech_ids(self) -> tuple:
        """Get required tech IDs (6 slots, -1 means empty). Use set_required_tech() to modify."""
        ...

    def set_required_tech(self, slot: int, tech_id: int) -> None:
        """
        Set a required tech ID at a specific slot.
        
        Args:
            slot: Slot index (0-5)
            tech_id: Tech ID to require (-1 to clear the slot)
            
        Raises:
            ValueError: If slot is not in range 0-5
        """
        ...

    def clear_required_techs(self) -> None:
        """Clear all required tech slots (set to -1)."""
        ...

    @property
    def icon_id(self) -> int:
        """Get icon ID."""
        ...

    @icon_id.setter
    def icon_id(self, value: int) -> None:
        ...

    @property
    def type(self) -> int:
        """Get tech type."""
        ...

    @type.setter
    def type(self, value: int) -> None:
        ...

    @property
    def min_required_techs(self) -> int:
        """Get minimum required techs count."""
        ...

    @min_required_techs.setter
    def min_required_techs(self, value: int) -> None:
        ...

    @property
    def civilization_id(self) -> int:
        """Get civilization ID (-1 = all civs)."""
        ...

    @civilization_id.setter
    def civilization_id(self, value: int) -> None:
        ...

    @property
    def full_tech_tree_mode(self) -> int:
        """Get full tech tree mode."""
        ...

    @full_tech_tree_mode.setter
    def full_tech_tree_mode(self, value: int) -> None:
        ...

    @property
    def location_unit_id(self) -> int:
        """Get research location unit ID (pre-DE versions only)."""
        ...

    @location_unit_id.setter
    def location_unit_id(self, value: int) -> None:
        ...

    @property
    def name_str_id(self) -> int:
        """Get language file name string ID."""
        ...

    @name_str_id.setter
    def name_str_id(self, value: int) -> None:
        ...

    @property
    def description_str_id(self) -> int:
        """Get language file description string ID."""
        ...

    @description_str_id.setter
    def description_str_id(self, value: int) -> None:
        ...

    @property
    def help_str_id(self) -> int:
        """Get language file help string ID."""
        ...

    @help_str_id.setter
    def help_str_id(self, value: int) -> None:
        ...

    @property
    def tech_tree_str_id(self) -> int:
        """Get tech tree string ID."""
        ...

    @tech_tree_str_id.setter
    def tech_tree_str_id(self, value: int) -> None:
        ...

    @property
    def hotkey_str_id(self) -> int:
        """Get hotkey string ID (pre-DE versions only)."""
        ...

    @hotkey_str_id.setter
    def hotkey_str_id(self, value: int) -> None:
        ...

    @property
    def button_id(self) -> int:
        """Get button ID (pre-DE versions only)."""
        ...

    @button_id.setter
    def button_id(self, value: int) -> None:
        ...

    @property
    def repeatable(self) -> bool:
        """Get if tech is repeatable (DE only)."""
        ...

    @repeatable.setter
    def repeatable(self, value: bool) -> None:
        ...

    @property
    def name2(self) -> str:
        """Get secondary name (SWGB only)."""
        ...

    @name2.setter
    def name2(self, value: str) -> None:
        ...

    @property
    def research_locations(self) -> list:
        """Get research locations list (DE v8.8+ only)."""
        ...

    def get_research_location(self, location_id: int) -> Optional[Any]:
        """
        Get a specific research location by index.
        
        Args:
            location_id: Index of the research location (0-based)
            
        Returns:
            ResearchLocation object or None if not found
        """
        ...

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
        ...

    def remove_research_location(self, location_id: int) -> bool:
        """
        Remove a research location by index.
        
        Args:
            location_id: Index of the research location to remove
            
        Returns:
            True if removed, False if failed or out of range
        """
        ...

    def copy_research_location(self, location_id: int, target_index: Optional[int] = None) -> Optional[Any]:
        """
        Copy a research location.
        
        Args:
            location_id: Source location index
            target_index: Destination index. If None, appends to end.
            
        Returns:
            The new ResearchLocation object, or None if failed
        """
        ...

    def move_research_location(self, source_index: int, target_index: int) -> bool:
        """
        Move a research location to a new position.
        
        Args:
            source_index: Index of location to move
            target_index: New index position
            
        Returns:
            True if moved, False if out of range
        """
        ...

    def clear_research_locations(self) -> None:
        """Remove all research locations."""
        ...

    def exists(self) -> bool:
        """Check if this tech entry exists."""
        ...

"""Type stubs for CivHandle - enables IDE autocomplete"""
from typing import Any, Optional
from Actual_Tools_GDP.Civilizations.resource_accessor import ResourceAccessor

class CivHandle:
    """Handle for a single civilization."""
    
    @property
    def id(self) -> int:
        """Get the civilization ID."""
        ...
    
    @property
    def name(self) -> str:
        """Get the civilization name."""
        ...

    @name.setter
    def name(self, value: str) -> None:
        ...

    @property
    def tech_tree_effect_id(self) -> int:
        """Get the tech tree effect ID."""
        ...

    @tech_tree_effect_id.setter
    def tech_tree_effect_id(self, value: int) -> None:
        ...

    @property
    def team_bonus_effect_id(self) -> int:
        """Get the team bonus effect ID."""
        ...

    @team_bonus_effect_id.setter
    def team_bonus_effect_id(self, value: int) -> None:
        ...

    @property
    def icon_set(self) -> int:
        """Get the icon set."""
        ...

    @icon_set.setter
    def icon_set(self, value: int) -> None:
        ...

    @property
    def player_type(self) -> int:
        """Get the player type."""
        ...

    @player_type.setter
    def player_type(self, value: int) -> None:
        ...

    @property
    def resources(self) -> list:
        """Get the resources list directly."""
        ...

    @property
    def resource(self) -> ResourceAccessor:
        """
        Access per-civ resource values.
        
        Usage:
            civ.resource.get(0)           # Get value at index 0
            civ.resource.set(0, 200.0)    # Set value at index 0
            civ.resource[0]               # Get via indexing
            civ.resource[0] = 200.0       # Set via indexing
            
        Note: To add/remove resources, use CivManager.add_resource() and
              CivManager.remove_resource() - these apply to ALL civilizations.
        """
        ...

    @property
    def units(self) -> list:
        """Get the units list."""
        ...

    def exists(self) -> bool:
        """Check if this civilization entry exists."""
        ...

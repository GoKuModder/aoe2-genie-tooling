"""Type stubs for TechHandle - enables IDE autocomplete"""
from typing import Any, Optional
from Actual_Tools_GDP.Techs.research_location_accessor import ResearchLocationAccessor

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
    def required_tech_ids(self) -> list:
        """Get required tech IDs."""
        ...

    @property
    def icon_id(self) -> int:
        """Get icon ID."""
        ...

    @icon_id.setter
    def icon_id(self, value: int) -> None:
        ...

    @property
    def research_locations(self) -> list:
        """Get research locations list (DE v8.8+ only)."""
        ...

    @property
    def research_location(self) -> ResearchLocationAccessor:
        """
        Access research location operations.
        
        Usage:
            tech.research_location.add(location_unit_id=87, research_time=60)
            tech.research_location.get(0)
            tech.research_location.remove(0)
            tech.research_location.copy(0)
            tech.research_location.move(0, 1)
        """
        ...

    def clear_research_locations(self) -> None:
        """Remove all research locations."""
        ...

    def exists(self) -> bool:
        """Check if this tech entry exists."""
        ...

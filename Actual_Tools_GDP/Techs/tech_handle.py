"""
TechHandle - Wrapper for individual Tech objects.

Techs are single-tier objects with properties like name, effect_id, costs.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

__all__ = ["TechHandle"]


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
        """Get the cost array (3 TechCost objects). Use cost_1, cost_2, cost_3 for cleaner access."""
        return self._tech.costs

    @property
    def required_tech_ids(self) -> list:
        """Get required tech IDs."""
        return self._tech.required_tech_ids

    @property
    def icon_id(self) -> int:
        """Get icon ID."""
        return self._tech.icon_id

    @icon_id.setter
    def icon_id(self, value: int) -> None:
        self._tech.icon_id = value

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

    @property
    def research_location(self) -> Any:
        """
        Access research location operations.
        
        Usage:
            tech.research_location.add(location_unit_id=87, research_time=60)
            tech.research_location.get(0)
            tech.research_location.remove(0)
            tech.research_location.copy(0)
            tech.research_location.move(0, 1)
        """
        from Actual_Tools_GDP.Techs.research_location_accessor import ResearchLocationAccessor
        return ResearchLocationAccessor(self)

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

"""
CivHandle - Wrapper for individual Civilization objects.

Civilizations contain units, resources, and effect links.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace
    from aoe2_genie_tooling.Civilizations.resource_accessor import ResourceAccessor

__all__ = ["CivHandle"]


class CivHandle:
    """
    Handle for a single civilization.
    
    Provides direct attribute access and resource management.
    """
    
    def __init__(self, workspace: GenieWorkspace, civ_id: int) -> None:
        """Initialize CivHandle."""
        object.__setattr__(self, '_workspace', workspace)
        object.__setattr__(self, '_id', civ_id)
        object.__setattr__(self, '_civ', workspace.dat.civilizations[civ_id])
    
    @property
    def id(self) -> int:
        """Get the civilization ID."""
        return self._id
    
    @property
    def workspace(self) -> GenieWorkspace:
        """Get the workspace."""
        return self._workspace

    @property
    def name(self) -> str:
        """Get the civilization name."""
        try:
            return self._civ.name
        except Exception:
            return ""

    @name.setter
    def name(self, value: str) -> None:
        """Set the civilization name."""
        try:
            self._civ.name = value
        except Exception:
            pass

    @property
    def tech_tree_effect_id(self) -> int:
        """Get the tech tree effect ID."""
        return self._civ.tech_tree_effect_id

    @tech_tree_effect_id.setter
    def tech_tree_effect_id(self, value: int) -> None:
        self._civ.tech_tree_effect_id = value

    @property
    def team_bonus_effect_id(self) -> int:
        """Get the team bonus effect ID."""
        try:
            return self._civ.team_bonus_effect_id
        except Exception:
            return -1

    @team_bonus_effect_id.setter
    def team_bonus_effect_id(self, value: int) -> None:
        try:
            self._civ.team_bonus_effect_id = value
        except Exception:
            pass

    @property
    def icon_set(self) -> int:
        """Get the icon set."""
        return self._civ.icon_set

    @icon_set.setter
    def icon_set(self, value: int) -> None:
        self._civ.icon_set = value

    @property
    def player_type(self) -> int:
        """Get the player type."""
        return self._civ.player_type

    @player_type.setter
    def player_type(self, value: int) -> None:
        self._civ.player_type = value

    # Resource Management
    @property
    def resources(self) -> list:
        """Get the resources list directly."""
        return self._civ.resources

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
        from aoe2_genie_tooling.Civilizations.resource_accessor import ResourceAccessor
        return ResourceAccessor(self)

    # Unit Management
    @property
    def units(self) -> list:
        """Get the units list."""
        return self._civ.units

    def exists(self) -> bool:
        """Check if this civilization entry exists."""
        return self._civ is not None

    def __getattr__(self, name: str) -> Any:
        """Get attribute from underlying civilization."""
        return getattr(self._civ, name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute on underlying civilization."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._civ, name, value)
    
    def __repr__(self) -> str:
        if not self.exists():
            return f"CivHandle(id={self._id}, status=DELETED)"
        return f"CivHandle(id={self._id}, name='{self.name}')"

"""
TechHandle - Wrapper for individual Tech objects.

Provides attribute access to tech properties.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

__all__ = ["TechHandle"]


class TechHandle:
    """
    Handle for a single tech.
    
    Provides direct attribute access to the underlying Tech object.
    """
    
    def __init__(self, workspace: GenieWorkspace, tech_id: int) -> None:
        """
        Initialize TechHandle.
        
        Args:
            workspace: The GenieWorkspace instance
            tech_id: ID of the tech
        """
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
        return f"TechHandle(id={self._id})"

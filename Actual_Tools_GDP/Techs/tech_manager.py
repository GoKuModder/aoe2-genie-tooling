"""
TechManager - Manages tech/technology operations.

Responsibilities:
- Get techs by ID
- Create new techs
- Validate tech references
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

from Actual_Tools_GDP.Techs.tech_handle import TechHandle

__all__ = ["TechManager"]


class TechManager:
    """
    Manager for tech operations.
    
    Pattern: Receives workspace, accesses dat through workspace.dat.techs
    """
    
    def __init__(self, workspace: GenieWorkspace) -> None:
        """
        Initialize TechManager with workspace reference.
        
        Args:
            workspace: The GenieWorkspace instance
        """
        self.workspace = workspace
    
    def get(self, tech_id: int) -> TechHandle:
        """
        Get a tech by ID.
        
        Args:
            tech_id: ID of the tech
            
        Returns:
            TechHandle for the tech
            
        Raises:
            InvalidIdError: If tech_id is out of range or None
        """
        from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
        
        if tech_id < 0 or tech_id >= len(self.workspace.dat.techs):
            raise InvalidIdError(
                f"Tech ID {tech_id} out of range (0-{len(self.workspace.dat.techs)-1})"
            )
        
        tech = self.workspace.dat.techs[tech_id]
        if tech is None:
            raise InvalidIdError(f"Tech ID {tech_id} is None (deleted/unused)")
        
        return TechHandle(self.workspace, tech_id)
    
    def count(self) -> int:
        """Get total number of techs."""
        return len(self.workspace.dat.techs)

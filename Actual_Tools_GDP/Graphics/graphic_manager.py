"""
GraphicManager - Manages sprite/graphic operations.

Responsibilities:
- Get graphics by ID
- Create new graphics
- Validate graphic references
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

from Actual_Tools_GDP.Graphics.graphic_handle import GraphicHandle

__all__ = ["GraphicManager"]


class GraphicManager:
    """
    Manager for sprite/graphic operations.
    
    Pattern: Receives workspace, accesses dat through workspace.dat.sprites
    """
    
    def __init__(self, workspace: GenieWorkspace) -> None:
        """
        Initialize GraphicManager with workspace reference.
        
        Args:
            workspace: The GenieWorkspace instance
        """
        self.workspace = workspace
    
    def get(self, graphic_id: int) -> GraphicHandle:
        """
        Get a graphic by ID.
        
        Args:
            graphic_id: ID of the graphic
            
        Returns:
            GraphicHandle for the graphic
            
        Raises:
            InvalidIdError: If graphic_id is out of range or None
        """
        from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
        
        if graphic_id < 0 or graphic_id >= len(self.workspace.dat.sprites):
            raise InvalidIdError(
                f"Graphic ID {graphic_id} out of range (0-{len(self.workspace.dat.sprites)-1})"
            )
        
        sprite = self.workspace.dat.sprites[graphic_id]
        if sprite is None:
            raise InvalidIdError(f"Graphic ID {graphic_id} is None (deleted/unused)")
        
        return GraphicHandle(self.workspace, graphic_id)
    
    def count(self) -> int:
        """Get total number of graphics."""
        return len(self.workspace.dat.sprites)

"""
GraphicHandle - Wrapper for individual Sprite objects.

Provides attribute access to sprite properties.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

__all__ = ["GraphicHandle"]


class GraphicHandle:
    """
    Handle for a single sprite/graphic.
    
    Provides direct attribute access to the underlying Sprite object.
    """
    
    def __init__(self, workspace: GenieWorkspace, graphic_id: int) -> None:
        """
        Initialize GraphicHandle.
        
        Args:
            workspace: The GenieWorkspace instance
            graphic_id: ID of the graphic
        """
        object.__setattr__(self, '_workspace', workspace)
        object.__setattr__(self, '_id', graphic_id)
        object.__setattr__(self, '_sprite', workspace.dat.sprites[graphic_id])
    
    @property
    def id(self) -> int:
        """Get the graphic ID."""
        return self._id
    
    @property
    def workspace(self) -> GenieWorkspace:
        """Get the workspace."""
        return self._workspace
    
    def __getattr__(self, name: str) -> Any:
        """
        Get attribute from underlying sprite.
        
        Args:
            name: Attribute name
            
        Returns:
            Attribute value from sprite
        """
        return getattr(self._sprite, name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        Set attribute on underlying sprite.
        
        Args:
            name: Attribute name
            value: Value to set
        """
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._sprite, name, value)
    
    def __repr__(self) -> str:
        return f"GraphicHandle(id={self._id})"

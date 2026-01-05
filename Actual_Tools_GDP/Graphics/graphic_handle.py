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
    
    # =========================================================================
    # DELTA MANAGEMENT
    # =========================================================================
    
    def add_delta(
        self,
        graphic_id: int,
        offset_x: int = 0,
        offset_y: int = 0,
        display_angle: int = -1,
    ):
        """
        Add a delta (sub-graphic) to this graphic.
        
        Args:
            graphic_id: ID of graphic to attach as delta
            offset_x: X offset from parent (default: 0)
            offset_y: Y offset from parent (default: 0)
            display_angle: Angle filter, -1 = all angles (default: -1)
            
        Returns:
            DeltaHandle for the new delta
            
        Example:
            >>> gfx = gm.get(100)
            >>> shadow = gfx.add_delta(graphic_id=200, offset_y=5)
            >>> shadow.offset_x = 2
        """
        from sections.sprite_data.sprite_delta import SpriteDelta
        from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle
        
        # Create new delta - try direct construction first
        new_delta = SpriteDelta()
        new_delta.sprite_id = graphic_id
        new_delta.offset_x = offset_x
        new_delta.offset_y = offset_y
        new_delta.display_angle = display_angle
        new_delta._padding1 = 0
        new_delta._padding2 = 0
        new_delta._parent_sprite_ptr = b"\x00" * 4
        
        # Append to sprite's delta list
        self._sprite.deltas.append(new_delta)
        
        # Update count
        self._sprite.num_deltas = len(self._sprite.deltas)
        
        # Return handle for new delta
        return DeltaHandle(self, len(self._sprite.deltas) - 1)
    
    def get_delta(self, delta_id: int):
        """
        Get a delta by index.
        
        Args:
            delta_id: Index in deltas list (0-based)
            
        Returns:
            DeltaHandle if exists, None otherwise
        """
        from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle
        
        if 0 <= delta_id < len(self._sprite.deltas):
            return DeltaHandle(self, delta_id)
        return None
    
    def remove_delta(self, delta_id: int) -> bool:
        """
        Remove a delta by index.
        
        Args:
            delta_id: Index in deltas list (0-based)
            
        Returns:
            True if removed, False if index invalid
        """
        if 0 <= delta_id < len(self._sprite.deltas):
            del self._sprite.deltas[delta_id]
            self._sprite.num_deltas = len(self._sprite.deltas)
            return True
        return False
    
    def add_delta_from_graphic(self, graphic_id: int, delta_id: int):
        """
        Copy a delta from another graphic and add it to this graphic.
        
        Args:
            graphic_id: Source graphic ID
            delta_id: Delta index in source graphic
            
        Returns:
            DeltaHandle for the new delta, or None if source not found
            
        Example:
            >>> new_gfx.add_delta_from_graphic(graphic_id=100, delta_id=0)
        """
        from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle
        
        # Get source graphic
        source_gfx = self._workspace.graphic_manager.get(graphic_id)
        if not source_gfx or delta_id >= len(source_gfx.deltas):
            return None
        
        # Get source delta
        source_delta = source_gfx.deltas[delta_id]
        
        # Create new delta with same properties
        return self.add_delta(
            graphic_id=source_delta.sprite_id,
            offset_x=source_delta.offset_x,
            offset_y=source_delta.offset_y,
            display_angle=source_delta.display_angle,
        )
    
    def clear_deltas(self) -> None:
        """Remove all deltas from this graphic."""
        self._sprite.deltas.clear()
        self._sprite.num_deltas = 0

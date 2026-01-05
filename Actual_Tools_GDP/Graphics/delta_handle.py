"""
DeltaHandle - Wrapper for SpriteDelta with clean property access.

Provides access to delta properties:
- delta_id: Index in parent's deltas list
- graphic_id: Referenced graphic ID (sprite_id in SpriteDelta)
- offset_x, offset_y: Position offsets
- display_angle: Angle filter (-1 = all)
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Actual_Tools_GDP.Graphics.graphic_handle import GraphicHandle

__all__ = ["DeltaHandle"]


class DeltaHandle:
    """Handle for a single delta (sub-graphic attachment)."""
    
    def __init__(self, parent: GraphicHandle, delta_index: int) -> None:
        """
        Initialize DeltaHandle.
        
        Args:
            parent: Parent GraphicHandle
            delta_index: Index in parent's deltas list
        """
        self.parent = parent
        self.index = delta_index
    
    def __repr__(self) -> str:
        return f"DeltaHandle(delta_id={self.delta_id}, graphic_id={self.graphic_id})"
    
    @property
    def delta_id(self) -> int:
        """Get the delta index."""
        return self.index
    
    @property
    def graphic_id(self) -> int:
        """Get the referenced graphic ID."""
        return self.parent._sprite.deltas[self.index].sprite_id
    
    @graphic_id.setter
    def graphic_id(self, value: int) -> None:
        """Set the referenced graphic ID."""
        self.parent._sprite.deltas[self.index].sprite_id = value
    
    @property
    def offset_x(self) -> int:
        """Get X offset from parent."""
        return self.parent._sprite.deltas[self.index].offset_x
    
    @offset_x.setter
    def offset_x(self, value: int) -> None:
        """Set X offset from parent."""
        self.parent._sprite.deltas[self.index].offset_x = value
    
    @property
    def offset_y(self) -> int:
        """Get Y offset from parent."""
        return self.parent._sprite.deltas[self.index].offset_y
    
    @offset_y.setter
    def offset_y(self, value: int) -> None:
        """Set Y offset from parent."""
        self.parent._sprite.deltas[self.index].offset_y = value
    
    @property
    def display_angle(self) -> int:
        """Get display angle filter (-1 = all angles)."""
        return self.parent._sprite.deltas[self.index].display_angle
    
    @display_angle.setter
    def display_angle(self, value: int) -> None:
        """Set display angle filter (-1 = all angles)."""
        self.parent._sprite.deltas[self.index].display_angle = value

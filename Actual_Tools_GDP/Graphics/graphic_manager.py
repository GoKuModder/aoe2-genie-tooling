"""
GraphicManager - Manages sprite/graphic operations.

Responsibilities:
- Get graphics by ID
- Create new graphics
- Validate graphic references
"""
from __future__ import annotations

import copy as copy_module
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
        """Get total number of graphics (including None slots)."""
        return len(self.workspace.dat.sprites)
    
    def exists(self, graphic_id: int) -> bool:
        """
        Check if a graphic ID exists and is not None.
        
        Args:
            graphic_id: ID to check
            
        Returns:
            True if graphic exists and is not None
        """
        return (
            0 <= graphic_id < len(self.workspace.dat.sprites)
            and self.workspace.dat.sprites[graphic_id] is not None
        )
    
    def count_active(self) -> int:
        """Return number of non-None graphics."""
        return sum(1 for g in self.workspace.dat.sprites if g is not None)
    
    def add_graphic(
        self,
        file_name: str,
        name: Optional[str] = None,
        graphic_id: Optional[int] = None,
        frame_count: int = 1,
        angle_count: int = 1,
        frame_duration: float = 0.1,
        speed_multiplier: float = 1.0,
    ) -> GraphicHandle:
        """
        Add a new graphic to the DAT file.
        
        Args:
            file_name: The SLP/SMX file name (e.g., "hero_attack.slp")
            name: Internal name. If None, uses file_name
            graphic_id: Target ID. If None, appends to end
            frame_count: Number of animation frames
            angle_count: Number of angles/facings
            frame_duration: Duration per frame in seconds
            speed_multiplier: Animation speed multiplier
            
        Returns:
            GraphicHandle for the new graphic
        """
        from sections.sprite_data.sprite import Sprite
        
        if not file_name:
            raise ValueError("file_name cannot be empty")
        
        if name is None:
            name = file_name
        
        if graphic_id is None:
            graphic_id = len(self.workspace.dat.sprites)
        elif graphic_id < 0:
            raise ValueError(f"graphic_id must be non-negative, got {graphic_id}")
        
        # GenieDatParser doesn't provide a create API - we work around this by
        # reusing an existing sprite object and modifying all its fields
        # This preserves the version context while giving us a "new" sprite
        
        # Find any existing sprite to use as template
        template_sprite = None
        for sprite in self.workspace.dat.sprites:
            if sprite is not None:
                template_sprite = sprite
                break
        
        if template_sprite is None:
            raise RuntimeError("Cannot add graphic: DAT file has no existing sprites")
        
        # Use the existing sprite object (it's mutable) and modify all fields
        # This works because we're changing every relevant field anyway
        new_sprite = template_sprite
        
        # Set ALL fields to create a "new" sprite
        new_sprite._name_de2 = name
        new_sprite._file_name_de2 = file_name
        new_sprite.particle_effect_name = ""
        new_sprite.id = graphic_id
        new_sprite.num_frames = frame_count
        new_sprite.num_facets = angle_count
        new_sprite.frame_rate = frame_duration
        new_sprite.speed_mult = speed_multiplier
        new_sprite.slp_id = -1
        new_sprite.is_loaded = False
        new_sprite.force_player_color = 0
        new_sprite.layer = 0
        new_sprite.color_table = -1
        new_sprite.transparent_selection = 2
        new_sprite.bounding_box = [0, 0, 0, 0]
        new_sprite.sound_id = -1
        new_sprite.wwise_sound_id = 0
        new_sprite.facets_have_attack_sounds = False
        new_sprite.replay_delay = 0.0
        new_sprite.sequence_type = 0
        new_sprite.mirroring_mode = 0
        new_sprite.editor_mode = 0
        new_sprite.num_deltas = 0
        new_sprite.deltas = []
        new_sprite.facet_attack_sounds = []
        
        # Ensure list capacity
        while len(self.workspace.dat.sprites) <= graphic_id:
            self.workspace.dat.sprites.append(None)
        
        # Assign to target slot
        self.workspace.dat.sprites[graphic_id] = new_sprite
        
        return GraphicHandle(self.workspace, graphic_id)
    
    def copy(self, source_id: int, target_id: Optional[int] = None) -> GraphicHandle:
        """
        Copy a graphic to a new ID.
        
        Args:
            source_id: ID of graphic to copy
            target_id: Target ID. If None, appends to end
            
        Returns:
            GraphicHandle for the copied graphic
            
        Raises:
            InvalidIdError: If source doesn't exist
        """
        from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
        
        if not self.exists(source_id):
            raise InvalidIdError(f"Source graphic {source_id} does not exist")
        
        source = self.workspace.dat.sprites[source_id]
        copied = copy_module.deepcopy(source)
        
        if target_id is None:
            target_id = len(self.workspace.dat.sprites)
        elif target_id < 0:
            raise ValueError(f"target_id must be non-negative, got {target_id}")
        
        copied.id = target_id
        
        # Ensure capacity
        while len(self.workspace.dat.sprites) <= target_id:
            self.workspace.dat.sprites.append(None)
        
        self.workspace.dat.sprites[target_id] = copied
        
        return GraphicHandle(self.workspace, target_id)
    
    def remove_delta_by_graphic(self, graphic_id: int) -> int:
        """
        Remove all deltas that reference a specific graphic (from ALL graphics).
        
        Args:
            graphic_id: Graphic ID to search for and remove
            
        Returns:
            Total number of deltas removed across all graphics
            
        Example:
            >>> # Remove all shadows (graphic 200) from all graphics
            >>> gm.remove_delta_by_graphic(graphic_id=200)
        """
        total_removed = 0
        for sprite in self.workspace.dat.sprites:
            if sprite is not None and len(sprite.deltas) > 0:
                initial_count = len(sprite.deltas)
                sprite.deltas = [
                    d for d in sprite.deltas if d.sprite_id != graphic_id
                ]
                removed = initial_count - len(sprite.deltas)
                if removed > 0:
                    sprite.num_deltas = len(sprite.deltas)
                    total_removed += removed
        return total_removed

"""
GraphicManager - Manager for creating and modifying graphics.

Provides methods:
- add_graphic: Create new graphic
- get: Get GraphicHandle by ID
- copy: Copy graphic to new ID
- delete: Delete graphic
- paste: Paste copied graphic data
"""
from __future__ import annotations

import copy as copy_module
from typing import TYPE_CHECKING, Optional

from Actual_Tools.backend import DatFile, Graphic
from Actual_Tools.Graphics.graphic_handle import GraphicHandle
from Actual_Tools.Shared.tool_base import ToolBase, tracks_creation
from Actual_Tools.exceptions import InvalidIdError

if TYPE_CHECKING:
    pass

__all__ = ["GraphicManager"]


class GraphicManager(ToolBase):
    """
    Manager for creating and modifying graphics in a DAT file.
    
    Provides methods to add, copy, delete, and paste graphics.
    
    Examples:
        >>> gfx_mgr = GraphicManager(dat_file)
        >>> handle = gfx_mgr.add_graphic("hero.slp", frame_count=10)
        >>> handle.sound_id = 5
        >>> copied = gfx_mgr.copy(original_id=100, new_id=200)
    """
    
    # Clipboard for copy/paste operations
    _clipboard: Optional[Graphic] = None
    
    def __init__(self, dat_file: DatFile) -> None:
        super().__init__(dat_file)
    
    # =========================================================================
    # RETRIEVAL
    # =========================================================================
    
    def get(self, graphic_id: int) -> GraphicHandle:
        """
        Get a GraphicHandle by ID.
        
        Args:
            graphic_id: The graphic ID to retrieve.
        
        Returns:
            GraphicHandle wrapping the graphic.
        
        Note:
            Returns handle even if graphic doesn't exist. Check .exists()
        """
        return GraphicHandle(graphic_id, self.dat_file)
    
    def exists(self, graphic_id: int) -> bool:
        """Check if a graphic ID exists and is not None."""
        return (
            0 <= graphic_id < len(self.dat_file.graphics)
            and self.dat_file.graphics[graphic_id] is not None
        )
    
    def count(self) -> int:
        """Return total number of graphic slots."""
        return len(self.dat_file.graphics)
    
    def count_active(self) -> int:
        """Return number of non-None graphics."""
        return sum(1 for g in self.dat_file.graphics if g is not None)
    
    # =========================================================================
    # CREATION
    # =========================================================================
    
    @tracks_creation("graphic", name_param="file_name")
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
            name: Internal name. If None, uses file_name.
            graphic_id: Target ID. If None, uses next available.
            frame_count: Number of animation frames.
            angle_count: Number of angles/facings.
            frame_duration: Duration per frame in seconds.
            speed_multiplier: Animation speed multiplier.
        
        Returns:
            GraphicHandle for the new graphic.
        """
        if not file_name:
            raise ValueError("file_name cannot be empty.")
        
        if name is None:
            name = file_name
        
        if graphic_id is None:
            graphic_id = self.allocate_next_graphic_id()
        else:
            self.validate_id_positive(graphic_id, "graphic_id")
        
        new_graphic = Graphic(
            name=name,
            file_name=file_name,
            particle_effect_name="",
            slp=-1,
            is_loaded=0,
            old_color_flag=0,
            layer=0,
            player_color=-1,
            transparent_selection=0,
            coordinates=(0, 0, 0, 0),
            sound_id=-1,
            wwise_sound_id=0,
            angle_sounds_used=0,
            frame_count=frame_count,
            angle_count=angle_count,
            speed_multiplier=speed_multiplier,
            frame_duration=frame_duration,
            replay_delay=0.0,
            sequence_type=0,
            id=graphic_id,
            mirroring_mode=0,
            editor_flag=0,
            deltas=[],
            angle_sounds=[],
        )
        
        self.ensure_capacity(self.dat_file.graphics, graphic_id)
        self.dat_file.graphics[graphic_id] = new_graphic
        
        return GraphicHandle(graphic_id, self.dat_file)
    
    # =========================================================================
    # COPY / DELETE / PASTE
    # =========================================================================
    
    def copy(self, source_id: int, target_id: Optional[int] = None) -> GraphicHandle:
        """
        Copy a graphic to a new ID.
        
        Args:
            source_id: ID of graphic to copy.
            target_id: Target ID. If None, uses next available.
        
        Returns:
            GraphicHandle for the copied graphic.
        
        Raises:
            InvalidIdError: If source doesn't exist.
        """
        if not self.exists(source_id):
            raise InvalidIdError(f"Source graphic {source_id} does not exist.")
        
        source = self.dat_file.graphics[source_id]
        copied = copy_module.deepcopy(source)
        
        if target_id is None:
            target_id = self.allocate_next_graphic_id()
        else:
            self.validate_id_positive(target_id, "target_id")
        
        copied.id = target_id
        
        self.ensure_capacity(self.dat_file.graphics, target_id)
        self.dat_file.graphics[target_id] = copied
        
        return GraphicHandle(target_id, self.dat_file)
    
    def delete(self, graphic_id: int) -> bool:
        """
        Delete a graphic (set slot to None).
        
        Args:
            graphic_id: ID of graphic to delete.
        
        Returns:
            True if deleted, False if didn't exist.
        """
        if not self.exists(graphic_id):
            return False
        
        self.dat_file.graphics[graphic_id] = None
        return True
    
    def copy_to_clipboard(self, graphic_id: int) -> bool:
        """
        Copy a graphic to internal clipboard.
        
        Args:
            graphic_id: ID of graphic to copy.
        
        Returns:
            True if copied, False if doesn't exist.
        """
        if not self.exists(graphic_id):
            return False
        
        GraphicManager._clipboard = copy_module.deepcopy(
            self.dat_file.graphics[graphic_id]
        )
        return True
    
    def paste(self, target_id: Optional[int] = None) -> Optional[GraphicHandle]:
        """
        Paste graphic from clipboard to target ID.
        
        Args:
            target_id: Target ID. If None, uses next available.
        
        Returns:
            GraphicHandle for pasted graphic, or None if clipboard empty.
        """
        if GraphicManager._clipboard is None:
            return None
        
        pasted = copy_module.deepcopy(GraphicManager._clipboard)
        
        if target_id is None:
            target_id = self.allocate_next_graphic_id()
        else:
            self.validate_id_positive(target_id, "target_id")
        
        pasted.id = target_id
        
        self.ensure_capacity(self.dat_file.graphics, target_id)
        self.dat_file.graphics[target_id] = pasted
        
        return GraphicHandle(target_id, self.dat_file)
    
    def clear_clipboard(self) -> None:
        """Clear the internal clipboard."""
        GraphicManager._clipboard = None
    
    # =========================================================================
    # UTILITIES
    # =========================================================================
    
    def find_by_name(self, name: str) -> Optional[GraphicHandle]:
        """
        Find first graphic matching name.
        
        Args:
            name: Name to search for (case-sensitive).
        
        Returns:
            GraphicHandle if found, None otherwise.
        """
        for i, gfx in enumerate(self.dat_file.graphics):
            if gfx is not None and gfx.name == name:
                return GraphicHandle(i, self.dat_file)
        return None
    
    def find_by_file_name(self, file_name: str) -> Optional[GraphicHandle]:
        """
        Find first graphic matching file_name.
        
        Args:
            file_name: File name to search for.
        
        Returns:
            GraphicHandle if found, None otherwise.
        """
        for i, gfx in enumerate(self.dat_file.graphics):
            if gfx is not None and gfx.file_name == file_name:
                return GraphicHandle(i, self.dat_file)
        return None
    
    def remove_graphic_delta(self, graphic_id: int, delta_id: int) -> bool:
        """
        Remove a delta from a graphic by index.
        
        Args:
            graphic_id: ID of the parent graphic.
            delta_id: Index of the delta to remove (0-based).
        
        Returns:
            True if removed, False otherwise.
        """
        handle = self.get(graphic_id)
        if handle.exists():
            return handle.remove_delta(delta_id)
        return False
    
    def add_graphic_delta(
        self,
        graphic_id: int,
        delta_graphic_id: int,
        offset_x: int = 0,
        offset_y: int = 0,
        display_angle: int = -1,
    ) -> bool:
        """
        Add a delta to a graphic.
        
        Args:
            graphic_id: ID of the parent graphic.
            delta_graphic_id: ID of the graphic to add as delta.
            offset_x: X offset from parent.
            offset_y: Y offset from parent.
            display_angle: Display angle (-1 = all angles).
        
        Returns:
            True if added, False if graphic doesn't exist.
        """
        handle = self.get(graphic_id)
        if handle.exists():
            handle.add_delta(delta_graphic_id, offset_x, offset_y, display_angle)
            return True
        return False

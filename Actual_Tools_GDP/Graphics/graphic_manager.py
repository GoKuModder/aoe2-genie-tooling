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
    from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle

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
        self._clipboard: Optional[Any] = None

    def set_valid_attributes(self, obj: Any, attributes: dict[str, Any]) -> None:
        """
        Set attributes on an object only if they are valid for the current target version.
        
        Uses BFP-RS Retriever metadata (min_ver, max_ver) to determine validity.
        
        Args:
            obj: The object to set attributes on
            attributes: Dictionary of {attribute_name: value}
        """
        from bfp_rs import Retriever
        
        target_ver = self.workspace.target_version
        obj_type = type(obj)
        
        for name, value in attributes.items():
            # Check if attribute exists on the class
            if not hasattr(obj_type, name):
                # Standard attribute (not a descriptor) or dynamic? Try set it anyway?
                # For safety in this strict environment, we only skip if version check fails.
                # If it's not a descriptor, we assume it's always valid or handled elsewhere.
                try:
                    setattr(obj, name, value)
                except Exception:
                    pass
                continue
                
            # Inspect the descriptor
            descriptor = getattr(obj_type, name)
            
            # If it's a Retriever, checks version bounds
            if isinstance(descriptor, Retriever):
                min_ver = getattr(descriptor, 'min_ver', None)
                max_ver = getattr(descriptor, 'max_ver', None)
                
                if min_ver and target_ver < min_ver:
                    continue
                if max_ver and target_ver > max_ver:
                    continue
            
            # If we passed check, set the value
            setattr(obj, name, value)

    
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
    
    def delete(self, graphic_id: int) -> bool:
        """
        Delete a graphic (sets slot to None).
        
        Args:
            graphic_id: ID to delete
            
        Returns:
            True if deleted, False if didn't exist
        """
        if self.exists(graphic_id):
            self.workspace.dat.sprites[graphic_id] = None
            return True
        return False
    
    def find_by_name(self, name: str) -> Optional[GraphicHandle]:
        """
        Find first graphic matching name.
        
        Args:
            name: Internal name to search for
            
        Returns:
            GraphicHandle if found, None otherwise
        """
        for i, sprite in enumerate(self.workspace.dat.sprites):
            if sprite is not None and sprite.name == name:
                return GraphicHandle(self.workspace, i)
        return None
    
    def find_by_file_name(self, file_name: str) -> Optional[GraphicHandle]:
        """
        Find first graphic matching file name.
        
        Args:
            file_name: SLP/SMX file name to search for
            
        Returns:
            GraphicHandle if found, None otherwise
        """
        for i, sprite in enumerate(self.workspace.dat.sprites):
            if sprite is not None and sprite.file_name == file_name:
                return GraphicHandle(self.workspace, i)
        return None
    
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
    def add_graphic(
        self,
        file_name: str,
        name: Optional[str] = None,
        graphic_id: Optional[int] = None,
        slp_id: int = -1,
        is_loaded: bool = False,
        old_color_flag: int = 0,
        layer: int = 0,
        force_player_color: int = -1,
        transparent_selection: int = 0,
        coordinates: tuple[int, int, int, int] = (0, 0, 0, 0),
        sound_id: int = -1,
        wwise_sound_id: int = 0,
        frame_count: int = 1,
        angle_count: int = 1,
        speed_multiplier: float = 1.0,
        frame_duration: float = 0.1,
        replay_delay: float = 0.0,
        sequence_type: int = 0,
        mirroring_mode: int = 0,
        editor_flag: int = 0,
        particle_effect_name: str = "",
        first_frame: int = 0,
    ) -> GraphicHandle:
        """
        Add a new graphic to the DAT file.
        
        Args:
            file_name: The SLP/SMX file name
            name: Internal name. If None, uses file_name
            graphic_id: Target ID. If None, appends to end
            slp_id: SLP file ID (default: -1)
            is_loaded: Whether sprite is loaded (default: False)
            old_color_flag: Legacy color flag (was player_color) (default: 0)
            layer: Rendering layer (default: 0)
            force_player_color: Force player color ID (was color_table) (default: -1)
            transparent_selection: Transparent pick mode (default: 0)
            coordinates: Bounding box (X1, Y1, X2, Y2) (default: (0,0,0,0))
            sound_id: Sound ID (default: -1)
            wwise_sound_id: Wwise sound ID (default: 0)
            frame_count: Number of animation frames (default: 1)
            angle_count: Number of angles/facings (default: 1)
            speed_multiplier: Animation speed multiplier (default: 1.0)
            frame_duration: Duration per frame in seconds (default: 0.1)
            replay_delay: Delay before animation replay (default: 0.0)
            sequence_type: Animation sequence type (default: 0)
            mirroring_mode: Mirroring mode (default: 0)
            editor_flag: Editor display flag (default: 0)
            particle_effect_name: Particle effect name (default: "")
            first_frame: First frame index (default: 0)
            
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
        
        # Find any existing sprite to use as version template
        template_sprite = None
        for sprite in self.workspace.dat.sprites:
            if sprite is not None:
                template_sprite = sprite
                break
        
        if template_sprite is None:
            raise RuntimeError("Cannot add graphic: DAT file has no existing sprites")
        
        # Instantiate a NEW sprite with the correct version
        new_sprite = Sprite(ver=template_sprite.ver)
        
        # Set ALL fields to create a "new" sprite
        # Prepare attributes dictionary
        attributes = {
            'name': name,
            'file_name': file_name,
            'particle_effect_name': particle_effect_name,
            'id': graphic_id,
            'num_frames': frame_count,
            'num_facets': angle_count,
            'frame_rate': frame_duration,
            'speed_mult': speed_multiplier,
            'slp_id': slp_id,
            'is_loaded': is_loaded,
            'force_player_color': old_color_flag,
            'layer': layer,
            'color_table': force_player_color,
            'transparent_selection': transparent_selection,
            'bounding_box': list(coordinates),
            'sound_id': sound_id,
            'wwise_sound_id': wwise_sound_id,
            'facets_have_attack_sounds': False,
            'replay_delay': replay_delay,
            'sequence_type': sequence_type,
            'mirroring_mode': mirroring_mode,
            'editor_mode': editor_flag,
            'first_frame': first_frame,
        }
        
        # Apply attributes safely using version filtering
        self.set_valid_attributes(new_sprite, attributes)
            
        new_sprite.num_deltas = 0
        new_sprite.deltas = []
        new_sprite.facet_attack_sounds = []
        
        # Extend the sprites list if needed (append to end only)
        # Direct indexed assignment at existing indices is safe
        sprites = self.workspace.dat.sprites
        while len(sprites) <= graphic_id:
            sprites.append(None)
        
        # Direct assignment at index
        sprites[graphic_id] = new_sprite
        
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
        copied = self._copy_sprite(source)
        
        if target_id is None:
            target_id = len(self.workspace.dat.sprites)
        elif target_id < 0:
            raise ValueError(f"target_id must be non-negative, got {target_id}")
        
        copied.id = target_id
        
        # Extend the sprites list if needed (append to end only)
        # Direct indexed assignment at existing indices is safe
        sprites = self.workspace.dat.sprites
        while len(sprites) <= target_id:
            sprites.append(None)
        
        # Direct assignment at index (this triggers bfp_rs copy for the element)
        sprites[target_id] = copied
        
        return GraphicHandle(self.workspace, target_id)
    
    def _copy_sprite(self, source: Any) -> Any:
        """
        Manual deep copy of a Sprite object (bypass pickle blocker).
        """
        from sections.sprite_data.sprite import Sprite
        
        new_sprite = Sprite(ver=source.ver)
        

        
        # Other attributes to copy
        attrs = [
            'name', 'file_name', 'particle_effect_name', 'id',
            'num_frames', 'frame_rate', 'speed_mult',
            'slp_id', 'is_loaded', 'force_player_color', 'layer',
            'color_table', 'transparent_selection', 'bounding_box',
            'sound_id', 'wwise_sound_id',
            'replay_delay', 'sequence_type', 'mirroring_mode', 'editor_mode',
            'first_frame',  # DE1 version-specific
        ]
        
        for attr in attrs:
            try:
                if hasattr(source, attr):
                    setattr(new_sprite, attr, getattr(source, attr))
            except Exception:
                pass  # Skip version-specific attrs that fail
        
        # Copy deltas
        new_sprite.num_deltas = source.num_deltas
        new_sprite.deltas = [self._copy_delta(d) for d in source.deltas]
        
        # Copy facet attack sounds safely
        # CRITICAL: bfp_rs validation prevents assigning list if size doesn't match num_facets expectation.
        # Strategy: Assign empty (safe), then append individually, then update metadata.
        if source.facets_have_attack_sounds and hasattr(source, 'facet_attack_sounds'):
            new_sprite.facet_attack_sounds = [] # Break store linkage & init to 0
            
            for sound in source.facet_attack_sounds:
                new_sprite.facet_attack_sounds.append(self._copy_facet_sound(sound))
            
            # Sync metadata AFTER populating
            new_sprite.num_facets = len(new_sprite.facet_attack_sounds)
            new_sprite.facets_have_attack_sounds = True
        else:
            new_sprite.facet_attack_sounds = []
            new_sprite.num_facets = source.num_facets
            new_sprite.facets_have_attack_sounds = False
        
        return new_sprite

    def _copy_delta(self, source: Any) -> Any:
        """Manual copy of a SpriteDelta object."""
        from sections.sprite_data.sprite_delta import SpriteDelta
        new_delta = SpriteDelta(ver=source.ver)
        attrs = ['sprite_id', 'offset_x', 'offset_y', 'display_angle']
        for attr in attrs:
            setattr(new_delta, attr, getattr(source, attr))
        return new_delta

    def _copy_facet_sound(self, source: Any) -> Any:
        """Manual copy of a FacetAttackSound object."""
        from sections.sprite_data.facet_attack_sound import FacetAttackSound
        new_sound = FacetAttackSound(ver=source.ver)
        attrs = [
            'sound_delay1', 'sound_id1', 'wwise_sound_id1',
            'sound_delay2', 'sound_id2', 'wwise_sound_id2',
            'sound_delay3', 'sound_id3', 'wwise_sound_id3'
        ]
        for attr in attrs:
            setattr(new_sound, attr, getattr(source, attr))
        return new_sound

    def copy_to_clipboard(self, graphic_id: int) -> bool:
        """
        Copy a graphic to internal clipboard.
        
        Args:
            graphic_id: ID to copy
            
        Returns:
            True if copied, False otherwise
        """
        if self.exists(graphic_id):
            self._clipboard = self._copy_sprite(self.workspace.dat.sprites[graphic_id])
            return True
        return False
    
    def paste(self, target_id: Optional[int] = None) -> Optional[GraphicHandle]:
        """
        Paste from clipboard to new ID.
        
        Args:
            target_id: Target ID. If None, appends to end
            
        Returns:
            GraphicHandle for the pasted graphic, or None if clipboard empty
        """
        if self._clipboard is None:
            return None
        
        pasted = self._copy_sprite(self._clipboard)
        
        if target_id is None:
            target_id = len(self.workspace.dat.sprites)
        
        pasted.id = target_id
        
        # Ensure capacity
        while len(self.workspace.dat.sprites) <= target_id:
            self.workspace.dat.sprites.append(None)
        
        self.workspace.dat.sprites[target_id] = pasted
        
        return GraphicHandle(self.workspace, target_id)
    
    def clear_clipboard(self) -> None:
        """Clear the internal clipboard."""
        self._clipboard = None
    
    def add_graphic_delta(
        self,
        graphic_id: int,
        delta_graphic_id: int,
        offset_x: int = 0,
        offset_y: int = 0,
        display_angle: int = -1,
    ) -> DeltaHandle:
        """
        Add a delta to a specific graphic via manager.
        
        Args:
            graphic_id: Parent graphic ID
            delta_graphic_id: Graphic ID to attach as delta
            offset_x: X offset
            offset_y: Y offset
            display_angle: Angle filter
            
        Returns:
            DeltaHandle for the new delta
        """
        return self.get(graphic_id).add_delta(
            graphic_id=delta_graphic_id,
            offset_x=offset_x,
            offset_y=offset_y,
            display_angle=display_angle,
        )
    
    def remove_graphic_delta(self, graphic_id: int, delta_id: int) -> bool:
        """
        Remove a delta from a specific graphic via manager.
        
        Args:
            graphic_id: Parent graphic ID
            delta_id: Index of delta to remove
            
        Returns:
            True if removed
        """
        return self.get(graphic_id).remove_delta(delta_id)
    
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

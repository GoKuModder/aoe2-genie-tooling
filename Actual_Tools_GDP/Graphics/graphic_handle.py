"""
GraphicHandle - Wrapper for individual Sprite objects.

Provides attribute access to sprite properties.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Union

from Actual_Tools_GDP.Base.core.typed_ids import GraphicId, DeltaIndex

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace
    from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle

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
    def id(self) -> GraphicId:
        """Get the graphic ID (typed for IDE checking)."""
        return GraphicId(self._id)
    
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
        # Check if this class has a property descriptor for the name
        elif hasattr(type(self), name) and isinstance(getattr(type(self), name), property):
            prop = getattr(type(self), name)
            if prop.fset is not None:
                prop.fset(self, value)
            else:
                raise AttributeError(f"property '{name}' has no setter")
        else:
            setattr(self._sprite, name, value)
    
    def __repr__(self) -> str:
        return f"GraphicHandle(id={self._id})"
    
    # =========================================================================
    # PROPERTY ALIASES (Match Documentation)
    # =========================================================================
    
    @property
    def slp(self) -> int:
        """Alias for slp_id."""
        return self._sprite.slp_id
    
    @slp.setter
    def slp(self, value: int) -> None:
        self._sprite.slp_id = value
        
    @property
    def frame_count(self) -> int:
        """Alias for num_frames."""
        return self._sprite.num_frames
    
    @frame_count.setter
    def frame_count(self, value: int) -> None:
        self._sprite.num_frames = value
        
    @property
    def angle_count(self) -> int:
        """Alias for num_facets."""
        return self._sprite.num_facets
    
    @angle_count.setter
    def angle_count(self, value: int) -> None:
        self._sprite.num_facets = value
        
    @property
    def frame_duration(self) -> float:
        """Alias for frame_rate."""
        return self._sprite.frame_rate
    
    @frame_duration.setter
    def frame_duration(self, value: float) -> None:
        self._sprite.frame_rate = value
        
    @property
    def speed_multiplier(self) -> float:
        """Alias for speed_mult."""
        return self._sprite.speed_mult
    
    @speed_multiplier.setter
    def speed_multiplier(self, value: float) -> None:
        self._sprite.speed_mult = value
        
    @property
    def angle_sounds_used(self) -> bool:
        """Alias for facets_have_attack_sounds."""
        return self._sprite.facets_have_attack_sounds
    
    @angle_sounds_used.setter
    def angle_sounds_used(self, value: bool) -> None:
        self._sprite.facets_have_attack_sounds = value
        
    @property
    def player_color(self) -> int:
        """Alias for force_player_color."""
        return self._sprite.force_player_color
    
    @player_color.setter
    def player_color(self, value: int) -> None:
        self._sprite.force_player_color = value
        
    @property
    def coordinates(self) -> tuple[int, int, int, int]:
        """Alias for bounding_box (returning as tuple)."""
        return tuple(self._sprite.bounding_box) # type: ignore
    
    @coordinates.setter
    def coordinates(self, value: list[int] | tuple[int, int, int, int]) -> None:
        self._sprite.bounding_box = list(value)
        
    @property
    def editor_flag(self) -> int:
        """Alias for editor_mode."""
        return self._sprite.editor_mode
    
    @editor_flag.setter
    def editor_flag(self, value: int) -> None:
        self._sprite.editor_mode = value
    
    # =========================================================================
    # DELTA MANAGEMENT
    # =========================================================================
    
    def add_delta(
        self,
        graphic_id: Union[int, str, Any],
        offset_x: int = 0,
        offset_y: int = 0,
        display_angle: int = -1,
    ) -> DeltaHandle:
        """
        Add a delta (sub-graphic) to this graphic.
        
        Args:
            graphic_id: ID of graphic to attach as delta (int, UUID, or Handle)
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
        
        # Resolve graphic_id (accepts int, GraphicHandle, or UUID - NOT DeltaHandle!)
        resolved_id = self._workspace.validator.resolve_id(
            graphic_id,
            "graphics",
            self._workspace,
            expected_handle_type=GraphicHandle,
            param_name="graphic_id",
        )
        
        # Create new delta with same version as parent
        new_delta = SpriteDelta(ver=self._sprite.ver)
        new_delta.sprite_id = resolved_id
        new_delta.offset_x = offset_x
        new_delta.offset_y = offset_y
        new_delta.display_angle = display_angle
        
        # CRITICAL: Don't use append()! bfp_rs lists share internal storage.
        current_deltas = list(self._sprite.deltas)
        current_deltas.append(new_delta)
        self._sprite.deltas = current_deltas  # setattr triggers bfp_rs copy
        
        # Update count
        self._sprite.num_deltas = len(self._sprite.deltas)
        
        # Return handle for new delta
        return DeltaHandle(self, len(self._sprite.deltas) - 1)
    
    def get_delta(self, delta_id: int) -> Optional[DeltaHandle]:
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
    
    def add_delta_from_graphic(
        self,
        graphic_id: Union[int, str, Any],
        delta_id: int,
    ) -> DeltaHandle:
        """
        Copy a delta from another graphic and add it to this graphic.
        
        Args:
            graphic_id: Source graphic ID (int, UUID, or Handle)
            delta_id: Delta index in source graphic
            
        Returns:
            DeltaHandle for the new delta
            
        Raises:
            InvalidIdError: If graphic_id or delta_id is invalid
            
        Example:
            >>> new_gfx.add_delta_from_graphic(graphic_id=100, delta_id=0)
        """
        from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle
        from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
        from Actual_Tools_GDP.Base.core.typed_ids import GraphicId, DeltaIndex
        
        validator = self._workspace.validator
        
        # Validate delta_id type - should be int, DeltaIndex, or DeltaHandle, NOT GraphicHandle/GraphicId
        resolved_delta_id = delta_id
        if hasattr(delta_id, 'delta_id'):
            # It's a DeltaHandle - extract the index
            resolved_delta_id = int(delta_id.delta_id)
        elif hasattr(delta_id, 'id'):
            # It's some other Handle (like GraphicHandle) - ERROR!
            actual_type = type(delta_id).__name__
            raise InvalidIdError(
                f"Expected int or DeltaHandle, got {actual_type}",
                action_description=f"Wrong type passed to 'delta_id'",
                context=f"Parameter: delta_id",
                hints=[
                    f"You passed a {actual_type} where an int or DeltaHandle was expected",
                    f"delta_id should be an index (0, 1, 2...) or a DeltaHandle object",
                    f"If you meant to pass a graphic, use the 'graphic_id' parameter instead",
                ],
            )
        elif isinstance(delta_id, GraphicId):
            # GraphicId passed to delta_id - ERROR!
            raise InvalidIdError(
                f"Expected int or DeltaIndex, got GraphicId",
                action_description=f"Wrong ID type passed to 'delta_id'",
                context=f"Parameter: delta_id",
                hints=[
                    f"You passed a GraphicId where a delta index was expected",
                    f"This usually means you're passing graphic.id to a delta_id parameter",
                    f"delta_id should be an index (0, 1, 2...) not a graphic ID",
                ],
            )
        elif isinstance(delta_id, DeltaIndex):
            resolved_delta_id = int(delta_id)
        elif not isinstance(delta_id, int):
            raise InvalidIdError(
                f"delta_id must be int or DeltaHandle, got {type(delta_id).__name__}",
                action_description=f"Invalid type for 'delta_id'",
            )
        
        # Resolve source graphic ID (must be GraphicHandle, not DeltaHandle!)
        resolved_gfx_id = validator.resolve_id(
            graphic_id,
            "graphics",
            self._workspace,
            expected_handle_type=GraphicHandle,
            param_name="graphic_id",
        )
        
        # Get source graphic
        source_gfx = self._workspace.graphic_manager.get(resolved_gfx_id)
        
        # Build rich context for error message
        gfx_name = source_gfx.name if source_gfx else "Unknown"
        context = f"Graphic '{gfx_name}' (ID: {resolved_gfx_id})"
        
        # Build current items list
        current_items = []
        if source_gfx:
            for i, delta in enumerate(source_gfx.deltas):
                current_items.append(f"Delta {i}: → Graphic {delta.graphic_id}")
        if not current_items:
            current_items = ["(no deltas exist)"]
        
        # Validate delta index with rich context
        validator.validate_index(
            resolved_delta_id,
            source_gfx._sprite.deltas,
            "delta_id",
            context=context,
            current_items=current_items,
            hints=[
                f"This graphic has {len(source_gfx.deltas)} delta(s)",
                "Use source_graphic.deltas to list all deltas",
                "Use source_graphic.add_delta() to add a new delta first",
            ],
            action_description="Attempt to copy a delta that doesn't exist",
        )
        
        # Get source delta
        source_delta = source_gfx.deltas[resolved_delta_id]
        
        # Create new delta with same properties
        return self.add_delta(
            graphic_id=source_delta.graphic_id,
            offset_x=source_delta.offset_x,
            offset_y=source_delta.offset_y,
            display_angle=source_delta.display_angle,
        )
    
    def clear_deltas(self) -> None:
        """Remove all deltas from this graphic."""
        self._sprite.deltas.clear()
        self._sprite.num_deltas = 0

    def exists(self) -> bool:
        """
        Check if this graphic entry exists and is not None.
        
        Returns:
            True if graphic exists
        """
        return self._sprite is not None
    
    def add_angle_sound(
        self,
        frame_num: int = 0,
        sound_id: int = -1,
        wwise_sound_id: int = 0,
        frame_num_2: int = 0,
        sound_id_2: int = -1,
        wwise_sound_id_2: int = 0,
        frame_num_3: int = 0,
        sound_id_3: int = -1,
        wwise_sound_id_3: int = 0,
    ) -> None:
        """
        Add an angle sound entry.
        
        Args:
            frame_num: Trigger frame for sound 1
            sound_id: Sound ID 1
            wwise_sound_id: Wwise sound ID 1 (DE2)
            frame_num_2: Trigger frame for sound 2
            sound_id_2: Sound ID 2
            wwise_sound_id_2: Wwise sound ID 2 (DE2)
            frame_num_3: Trigger frame for sound 3
            sound_id_3: Sound ID 3
            wwise_sound_id_3: Wwise sound ID 3 (DE2)
        """
        from sections.sprite_data.facet_attack_sound import FacetAttackSound
        
        angle_sound = FacetAttackSound(ver=self._sprite.ver)
        angle_sound.sound_delay1 = frame_num
        angle_sound.sound_id1 = sound_id
        angle_sound.wwise_sound_id1 = wwise_sound_id
        angle_sound.sound_delay2 = frame_num_2
        angle_sound.sound_id2 = sound_id_2
        angle_sound.wwise_sound_id2 = wwise_sound_id_2
        angle_sound.sound_delay3 = frame_num_3
        angle_sound.sound_id3 = sound_id_3
        angle_sound.wwise_sound_id3 = wwise_sound_id_3
        
        # CRITICAL: bfp_rs validation is strict on list assignment vs num_facets.
        # Strategy: Use Reset-Append to bypass assignment check and break storage sharing.
        
        # 1. Backup existing sounds (triggers copy)
        current_sounds = list(self._sprite.facet_attack_sounds)
        current_sounds.append(angle_sound)
        
        # 2. Clear to break storage linkage & satisfy "Expected: 0" check if uninitialized
        self._sprite.facet_attack_sounds = []
        
        # 3. Append individually (bypasses strict size check)
        for sound in current_sounds:
            self._sprite.facet_attack_sounds.append(sound)
            
        # 4. Sync metadata
        self._sprite.facets_have_attack_sounds = True
        self._sprite.num_facets = len(self._sprite.facet_attack_sounds)
    
    @property
    def deltas(self) -> list[DeltaHandle]:
        """
        Get all deltas as DeltaHandle objects.
        
        Returns:
            List of DeltaHandle objects for iteration
        """
        from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle
        return [DeltaHandle(self, i) for i in range(len(self._sprite.deltas))]
    
    def remove_delta_by_graphic(self, graphic_id: int) -> int:
        """
        Remove all deltas from THIS graphic that point to a specific graphic ID.
        
        Args:
            graphic_id: Graphic ID to search for
            
        Returns:
            Number of deltas removed
        """
        initial_count = len(self._sprite.deltas)
        self._sprite.deltas = [
            d for d in self._sprite.deltas if d.sprite_id != graphic_id
        ]
        removed = initial_count - len(self._sprite.deltas)
        if removed > 0:
            self._sprite.num_deltas = len(self._sprite.deltas)
        return removed
    
    def clear_angle_sounds(self) -> None:
        """Remove all angle sounds."""
        self._sprite.facet_attack_sounds.clear()
        self._sprite.facets_have_attack_sounds = False

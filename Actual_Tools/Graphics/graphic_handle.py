"""
GraphicHandle - High-level wrapper for Genie Graphic objects.

Provides full attribute flattening: access any attribute directly.
    graphic.frame_count = 10
    graphic.sound_id = 5
    graphic.deltas  # Returns list of GraphicDelta
"""
from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from genieutils.graphic import Graphic, GraphicDelta, GraphicAngleSound

if TYPE_CHECKING:
    from genieutils.datfile import DatFile

__all__ = ["GraphicHandle", "DeltaHandle"]


class DeltaHandle:
    """
    Wrapper for a GraphicDelta with its index.
    
    Attributes:
        delta_id: Index of this delta in the parent's deltas list.
        graphic_id: The referenced graphic ID.
        offset_x: X offset from parent.
        offset_y: Y offset from parent.
        display_angle: Display angle.
    """
    
    __slots__ = ("_delta", "_delta_id")
    
    def __init__(self, delta: GraphicDelta, delta_id: int) -> None:
        object.__setattr__(self, "_delta", delta)
        object.__setattr__(self, "_delta_id", delta_id)
    
    def __repr__(self) -> str:
        return f"DeltaHandle(delta_id={self._delta_id}, graphic_id={self._delta.graphic_id})"
    
    @property
    def delta_id(self) -> int:
        """Index of this delta in the parent's list."""
        return self._delta_id
    
    @property
    def graphic_id(self) -> int:
        """Referenced graphic ID."""
        return self._delta.graphic_id
    
    @graphic_id.setter
    def graphic_id(self, value: int) -> None:
        self._delta.graphic_id = value
    
    @property
    def offset_x(self) -> int:
        """X offset from parent."""
        return self._delta.offset_x
    
    @offset_x.setter
    def offset_x(self, value: int) -> None:
        self._delta.offset_x = value
    
    @property
    def offset_y(self) -> int:
        """Y offset from parent."""
        return self._delta.offset_y
    
    @offset_y.setter
    def offset_y(self, value: int) -> None:
        self._delta.offset_y = value
    
    @property
    def display_angle(self) -> int:
        """Display angle (-1 = all)."""
        return self._delta.display_angle
    
    @display_angle.setter
    def display_angle(self, value: int) -> None:
        self._delta.display_angle = value


class GraphicHandle:
    """
    High-level wrapper for Genie Graphic objects with full attribute access.
    
    Unlike UnitHandle, Graphics don't have civ-specific versions.
    Each graphic exists once in dat_file.graphics.
    
    Args:
        graphic_id: The graphic ID to wrap.
        dat_file: The source DatFile.
    
    Examples:
        >>> gfx = GraphicHandle(100, dat_file)
        >>> gfx.frame_count = 20
        >>> gfx.sound_id = 5
        >>> gfx.add_delta(graphic_id=101, offset_x=10, offset_y=5)
    """
    
    __slots__ = ("_graphic_id", "_dat_file")
    
    def __init__(self, graphic_id: int, dat_file: DatFile) -> None:
        if graphic_id < 0:
            raise ValueError(f"graphic_id must be non-negative, got {graphic_id}")
        
        object.__setattr__(self, "_graphic_id", graphic_id)
        object.__setattr__(self, "_dat_file", dat_file)
    
    def __repr__(self) -> str:
        gfx = self._graphic
        name = gfx.name if gfx else "<not found>"
        return f"GraphicHandle(id={self._graphic_id}, name={name!r})"
    
    # =========================================================================
    # CORE GRAPHIC ACCESS
    # =========================================================================
    
    @property
    def _graphic(self) -> Optional[Graphic]:
        """Get the underlying Graphic object."""
        if 0 <= self._graphic_id < len(self._dat_file.graphics):
            return self._dat_file.graphics[self._graphic_id]
        return None
    
    def exists(self) -> bool:
        """Check if this graphic exists in the DAT file."""
        return self._graphic is not None
    
    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================
    
    @property
    def id(self) -> int:
        """Graphic ID."""
        return self._graphic_id
    
    @property
    def name(self) -> str:
        """Graphic name."""
        gfx = self._graphic
        return gfx.name if gfx else ""
    
    @name.setter
    def name(self, value: str) -> None:
        gfx = self._graphic
        if gfx:
            gfx.name = value
    
    @property
    def file_name(self) -> str:
        """SLP/SMX file name."""
        gfx = self._graphic
        return gfx.file_name if gfx else ""
    
    @file_name.setter
    def file_name(self, value: str) -> None:
        gfx = self._graphic
        if gfx:
            gfx.file_name = value
    
    @property
    def particle_effect_name(self) -> str:
        """Particle effect name."""
        gfx = self._graphic
        return gfx.particle_effect_name if gfx else ""
    
    @particle_effect_name.setter
    def particle_effect_name(self, value: str) -> None:
        gfx = self._graphic
        if gfx:
            gfx.particle_effect_name = value
    
    @property
    def slp(self) -> int:
        """SLP resource ID."""
        gfx = self._graphic
        return gfx.slp if gfx else -1
    
    @slp.setter
    def slp(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.slp = value
    
    @property
    def is_loaded(self) -> int:
        """Is loaded flag."""
        gfx = self._graphic
        return gfx.is_loaded if gfx else 0
    
    @is_loaded.setter
    def is_loaded(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.is_loaded = value
    
    @property
    def old_color_flag(self) -> int:
        """Old color flag."""
        gfx = self._graphic
        return gfx.old_color_flag if gfx else 0
    
    @old_color_flag.setter
    def old_color_flag(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.old_color_flag = value
    
    @property
    def layer(self) -> int:
        """Render layer."""
        gfx = self._graphic
        return gfx.layer if gfx else 0
    
    @layer.setter
    def layer(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.layer = value
    
    @property
    def player_color(self) -> int:
        """Player color index."""
        gfx = self._graphic
        return gfx.player_color if gfx else -1
    
    @player_color.setter
    def player_color(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.player_color = value
    
    @property
    def transparent_selection(self) -> int:
        """Transparent selection flag."""
        gfx = self._graphic
        return gfx.transparent_selection if gfx else 0
    
    @transparent_selection.setter
    def transparent_selection(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.transparent_selection = value
    
    @property
    def coordinates(self) -> Tuple[int, int, int, int]:
        """Bounding box coordinates (x1, y1, x2, y2)."""
        gfx = self._graphic
        return gfx.coordinates if gfx else (0, 0, 0, 0)
    
    @coordinates.setter
    def coordinates(self, value: Tuple[int, int, int, int]) -> None:
        gfx = self._graphic
        if gfx:
            gfx.coordinates = value
    
    @property
    def sound_id(self) -> int:
        """Sound ID."""
        gfx = self._graphic
        return gfx.sound_id if gfx else -1
    
    @sound_id.setter
    def sound_id(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.sound_id = value
    
    @property
    def wwise_sound_id(self) -> int:
        """Wwise sound ID."""
        gfx = self._graphic
        return gfx.wwise_sound_id if gfx else 0
    
    @wwise_sound_id.setter
    def wwise_sound_id(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.wwise_sound_id = value
    
    @property
    def angle_sounds_used(self) -> int:
        """Whether angle sounds are used."""
        gfx = self._graphic
        return gfx.angle_sounds_used if gfx else 0
    
    @angle_sounds_used.setter
    def angle_sounds_used(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.angle_sounds_used = value
    
    @property
    def frame_count(self) -> int:
        """Number of animation frames."""
        gfx = self._graphic
        return gfx.frame_count if gfx else 0
    
    @frame_count.setter
    def frame_count(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.frame_count = value
    
    @property
    def angle_count(self) -> int:
        """Number of angles/facings."""
        gfx = self._graphic
        return gfx.angle_count if gfx else 0
    
    @angle_count.setter
    def angle_count(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.angle_count = value
    
    @property
    def speed_multiplier(self) -> float:
        """Animation speed multiplier."""
        gfx = self._graphic
        return gfx.speed_multiplier if gfx else 1.0
    
    @speed_multiplier.setter
    def speed_multiplier(self, value: float) -> None:
        gfx = self._graphic
        if gfx:
            gfx.speed_multiplier = value
    
    @property
    def frame_duration(self) -> float:
        """Duration per frame in seconds."""
        gfx = self._graphic
        return gfx.frame_duration if gfx else 0.0
    
    @frame_duration.setter
    def frame_duration(self, value: float) -> None:
        gfx = self._graphic
        if gfx:
            gfx.frame_duration = value
    
    @property
    def replay_delay(self) -> float:
        """Delay before animation replays."""
        gfx = self._graphic
        return gfx.replay_delay if gfx else 0.0
    
    @replay_delay.setter
    def replay_delay(self, value: float) -> None:
        gfx = self._graphic
        if gfx:
            gfx.replay_delay = value
    
    @property
    def sequence_type(self) -> int:
        """Sequence type."""
        gfx = self._graphic
        return gfx.sequence_type if gfx else 0
    
    @sequence_type.setter
    def sequence_type(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.sequence_type = value
    
    @property
    def mirroring_mode(self) -> int:
        """Mirroring mode."""
        gfx = self._graphic
        return gfx.mirroring_mode if gfx else 0
    
    @mirroring_mode.setter
    def mirroring_mode(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.mirroring_mode = value
    
    @property
    def editor_flag(self) -> int:
        """Editor display flag."""
        gfx = self._graphic
        return gfx.editor_flag if gfx else 0
    
    @editor_flag.setter
    def editor_flag(self, value: int) -> None:
        gfx = self._graphic
        if gfx:
            gfx.editor_flag = value
    
    # =========================================================================
    # COLLECTION PROPERTIES
    # =========================================================================
    
    @property
    def deltas(self) -> List[GraphicDelta]:
        """List of graphic deltas (sub-graphics)."""
        gfx = self._graphic
        return gfx.deltas if gfx else []
    
    @deltas.setter
    def deltas(self, value: List[GraphicDelta]) -> None:
        gfx = self._graphic
        if gfx:
            gfx.deltas = value
    
    @property
    def angle_sounds(self) -> List[GraphicAngleSound]:
        """List of angle-based sounds."""
        gfx = self._graphic
        return gfx.angle_sounds if gfx else []
    
    @angle_sounds.setter
    def angle_sounds(self, value: List[GraphicAngleSound]) -> None:
        gfx = self._graphic
        if gfx:
            gfx.angle_sounds = value
    
    # =========================================================================
    # CONVENIENCE METHODS (Deltas)
    # =========================================================================
    
    def add_delta(
        self,
        graphic_id: int,
        offset_x: int = 0,
        offset_y: int = 0,
        display_angle: int = -1,
    ) -> Optional[DeltaHandle]:
        """
        Add a delta (sub-graphic) to this graphic.
        
        Args:
            graphic_id: ID of the delta graphic.
            offset_x: X offset from parent.
            offset_y: Y offset from parent.
            display_angle: Display angle (-1 = all angles).
        
        Returns:
            DeltaHandle for the new delta, or None if graphic doesn't exist.
        """
        gfx = self._graphic
        if gfx:
            delta = GraphicDelta(
                graphic_id=graphic_id,
                padding_1=0,
                sprite_ptr=0,
                offset_x=offset_x,
                offset_y=offset_y,
                display_angle=display_angle,
                padding_2=0,
            )
            gfx.deltas.append(delta)
            delta_id = len(gfx.deltas) - 1
            return DeltaHandle(delta, delta_id)
        return None
    
    def remove_delta(self, delta_id: int) -> bool:
        """
        Remove a delta by index (position in list).
        
        Args:
            delta_id: Index of the delta to remove (0-based).
        
        Returns:
            True if removed, False if index out of range.
        """
        gfx = self._graphic
        if gfx and 0 <= delta_id < len(gfx.deltas):
            gfx.deltas.pop(delta_id)
            return True
        return False
    
    def remove_delta_by_graphic(self, graphic_id: int) -> bool:
        """
        Remove all deltas referencing a specific graphic ID.
        
        Args:
            graphic_id: ID of the referenced graphic to remove.
        
        Returns:
            True if any removed, False if none found.
        """
        gfx = self._graphic
        if gfx:
            original_len = len(gfx.deltas)
            gfx.deltas = [d for d in gfx.deltas if d.graphic_id != graphic_id]
            return len(gfx.deltas) < original_len
        return False
    
    def get_delta(self, delta_id: int) -> Optional[DeltaHandle]:
        """
        Get a delta by index.
        
        Args:
            delta_id: Index of the delta (0-based).
        
        Returns:
            DeltaHandle if found, None otherwise.
        """
        gfx = self._graphic
        if gfx and 0 <= delta_id < len(gfx.deltas):
            return DeltaHandle(gfx.deltas[delta_id], delta_id)
        return None
    
    def clear_deltas(self) -> None:
        """Remove all deltas."""
        gfx = self._graphic
        if gfx:
            gfx.deltas.clear()
    
    # =========================================================================
    # CONVENIENCE METHODS (Angle Sounds)
    # =========================================================================
    
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
        """Add an angle sound entry."""
        gfx = self._graphic
        if gfx:
            angle_sound = GraphicAngleSound(
                frame_num=frame_num,
                sound_id=sound_id,
                wwise_sound_id=wwise_sound_id,
                frame_num_2=frame_num_2,
                sound_id_2=sound_id_2,
                wwise_sound_id_2=wwise_sound_id_2,
                frame_num_3=frame_num_3,
                sound_id_3=sound_id_3,
                wwise_sound_id_3=wwise_sound_id_3,
            )
            gfx.angle_sounds.append(angle_sound)
            gfx.angle_sounds_used = 1
    
    def clear_angle_sounds(self) -> None:
        """Remove all angle sounds."""
        gfx = self._graphic
        if gfx:
            gfx.angle_sounds.clear()
            gfx.angle_sounds_used = 0
    
    # =========================================================================
    # DYNAMIC ATTRIBUTE ACCESS (fallback)
    # =========================================================================
    
    def __getattr__(self, name: str) -> Any:
        gfx = self._graphic
        if gfx and hasattr(gfx, name):
            return getattr(gfx, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__slots__:
            object.__setattr__(self, name, value)
            return
        gfx = self._graphic
        if gfx and hasattr(gfx, name):
            setattr(gfx, name, value)
            return
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

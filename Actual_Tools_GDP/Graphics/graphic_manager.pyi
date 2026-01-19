"""Type stubs for GraphicManager - enables IDE autocomplete"""
from typing import Optional, Any
from Actual_Tools_GDP.Graphics.graphic_handle import GraphicHandle
from Actual_Tools_GDP.Graphics.delta_handle import DeltaHandle

class GraphicManager:
    """Manager for sprite/graphic operations."""

    def set_valid_attributes(self, obj: Any, attributes: dict[str, Any]) -> None:
        """Set attributes safely with version filtering."""
        ...
    
    def get(self, graphic_id: int) -> GraphicHandle:
        """Get a graphic by ID."""
        ...
    
    def count(self) -> int:
        """Get total number of graphics (including None)."""
        ...
    
    def exists(self, graphic_id: int) -> bool:
        """Check if graphic exists and is not None."""
        ...
    
    def count_active(self) -> int:
        """Get number of non-None graphics."""
        ...
    
    def delete(self, graphic_id: int) -> bool:
        """Delete a graphic (sets slot to None)."""
        ...
    
    def find_by_name(self, name: str) -> Optional[GraphicHandle]:
        """Find first graphic matching name."""
        ...
    
    def find_by_file_name(self, file_name: str) -> Optional[GraphicHandle]:
        """Find first graphic matching file name."""
        ...
    
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
        speed_multiplier: float = 0.0,
        frame_duration: float = 0.1,
        replay_delay: float = 0.0,
        sequence_type: int = 0,
        mirroring_mode: int = 0,
        editor_flag: int = 0,
        particle_effect_name: str = "",
        first_frame: int = 0,
    ) -> GraphicHandle:
        """Add a new graphic to the DAT file."""
        ...
    
    def copy(self, source_id: int, target_id: Optional[int] = None) -> GraphicHandle:
        """Copy a graphic to a new ID."""
        ...
    
    def copy_to_clipboard(self, graphic_id: int) -> bool:
        """Copy a graphic to internal clipboard."""
        ...
    
    def paste(self, target_id: Optional[int] = None) -> Optional[GraphicHandle]:
        """Paste from clipboard to new ID."""
        ...
    
    def clear_clipboard(self) -> None:
        """Clear the internal clipboard."""
        ...
    
    def add_graphic_delta(
        self,
        graphic_id: int,
        delta_graphic_id: int,
        offset_x: int = 0,
        offset_y: int = 0,
        display_angle: int = -1,
    ) -> DeltaHandle:
        """Add a delta to a specific graphic via manager."""
        ...
    
    def remove_graphic_delta(self, graphic_id: int, delta_id: int) -> bool:
        """Remove a delta from a specific graphic via manager."""
        ...
    
    def remove_delta_by_graphic(self, graphic_id: int) -> int:
        """Remove all deltas that reference a specific graphic (from ALL graphics)."""
        ...

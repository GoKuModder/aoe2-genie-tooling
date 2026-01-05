"""Type stubs for GraphicManager - enables IDE autocomplete"""
from typing import Optional
from Actual_Tools_GDP.Graphics.graphic_handle import GraphicHandle

class GraphicManager:
    """Manager for sprite/graphic operations."""
    
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
    
    def add_graphic(
        self,
        file_name: str,
        name: Optional[str] = None,
        slp_id: Optional[int] = -1,
        frame_count: int = 1,
        angle_count: int = 1,
        frame_duration: float = 0.1,
        speed_multiplier: float = 1.0,
    ) -> GraphicHandle:
        """Add a new graphic to the DAT file."""
        ...
    
    def copy(self, source_id: int, target_id: Optional[int] = None) -> GraphicHandle:
        """Copy a graphic to a new ID."""
        ...
    
    def remove_delta_by_graphic(self, graphic_id: int) -> int:
        """Remove all deltas that reference a specific graphic (from ALL graphics)."""
        ...

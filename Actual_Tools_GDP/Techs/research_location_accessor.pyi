"""Type stubs for ResearchLocationAccessor - enables IDE autocomplete"""
from typing import Any, Optional

class ResearchLocationAccessor:
    """Accessor for research location operations."""
    
    def __iter__(self) -> Any:
        """Iterate over research locations."""
        ...
    
    def __len__(self) -> int:
        """Get number of research locations."""
        ...

    def add(
        self,
        location_unit_id: int = -1,
        research_time: int = 0,
        button_id: int = 0,
        hotkey_str_id: int = -1,
    ) -> Any:
        """
        Add a new research location.
        
        Args:
            location_unit_id: Building unit ID where this can be researched
            research_time: Time to research at this location
            button_id: UI button position
            hotkey_str_id: Hotkey string ID
            
        Returns:
            The new ResearchLocation object
        """
        ...

    def get(self, index: int) -> Any:
        """Get a research location by index."""
        ...

    def remove(self, index: int) -> bool:
        """Remove a research location by index."""
        ...

    def copy(self, index: int, target_index: Optional[int] = None) -> Any:
        """
        Copy a research location.
        
        Args:
            index: Source location index
            target_index: Destination index. If None, appends to end.
            
        Returns:
            The new ResearchLocation object
        """
        ...

    def move(self, source_index: int, target_index: int) -> bool:
        """
        Move a research location to a new position.
        
        Args:
            source_index: Index of location to move
            target_index: New index position
            
        Returns:
            True if moved, False if out of range
        """
        ...

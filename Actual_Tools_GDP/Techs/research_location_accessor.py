"""
ResearchLocationAccessor - Provides clean API for research location management.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Techs.tech_handle import TechHandle

__all__ = ["ResearchLocationAccessor"]


class ResearchLocationAccessor:
    """
    Accessor for research location operations.
    
    Usage:
        tech.research_location.add(location_unit_id=87, research_time=60)
        tech.research_location.get(0)
        tech.research_location.remove(0)
    """
    
    def __init__(self, tech_handle: TechHandle) -> None:
        self._tech_handle = tech_handle
        self._tech = tech_handle._tech
    
    def __iter__(self):
        """Iterate over research locations."""
        try:
            return iter(self._tech.research_locations)
        except Exception:
            return iter([])
    
    def __len__(self) -> int:
        """Get number of research locations."""
        try:
            return len(self._tech.research_locations)
        except Exception:
            return 0

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
        from sections.tech.tech import ResearchLocation
        
        new_loc = ResearchLocation(ver=self._tech.ver)
        new_loc.location_unit_id = location_unit_id
        new_loc.research_time = research_time
        new_loc.button_id = button_id
        new_loc.hotkey_str_id = hotkey_str_id
        
        self._tech.research_locations.append(new_loc)
        return new_loc

    def get(self, index: int) -> Optional[Any]:
        """Get a research location by index."""
        try:
            if 0 <= index < len(self._tech.research_locations):
                return self._tech.research_locations[index]
        except Exception:
            pass
        return None

    def remove(self, index: int) -> bool:
        """Remove a research location by index."""
        try:
            if 0 <= index < len(self._tech.research_locations):
                del self._tech.research_locations[index]
                return True
        except Exception:
            pass
        return False

    def copy(self, index: int, target_index: Optional[int] = None) -> Optional[Any]:
        """
        Copy a research location.
        
        Args:
            index: Source location index
            target_index: Destination index. If None, appends to end.
            
        Returns:
            The new ResearchLocation object
        """
        try:
            if not (0 <= index < len(self._tech.research_locations)):
                return None
                
            source = self._tech.research_locations[index]
            
            from sections.tech.tech import ResearchLocation
            new_loc = ResearchLocation(ver=source.ver)
            new_loc.location_unit_id = source.location_unit_id
            new_loc.research_time = source.research_time
            new_loc.button_id = source.button_id
            new_loc.hotkey_str_id = source.hotkey_str_id
            
            if target_index is None:
                self._tech.research_locations.append(new_loc)
            else:
                target_index = max(0, min(target_index, len(self._tech.research_locations)))
                self._tech.research_locations.insert(target_index, new_loc)
                
            return new_loc
        except Exception:
            return None

    def move(self, source_index: int, target_index: int) -> bool:
        """
        Move a research location to a new position.
        
        Args:
            source_index: Index of location to move
            target_index: New index position
            
        Returns:
            True if moved, False if out of range
        """
        try:
            if not (0 <= source_index < len(self._tech.research_locations)):
                return False
                
            target_index = max(0, min(target_index, len(self._tech.research_locations) - 1))
            
            if source_index == target_index:
                return True
                
            obj = self._tech.research_locations.pop(source_index)
            self._tech.research_locations.insert(target_index, obj)
            return True
        except Exception:
            return False

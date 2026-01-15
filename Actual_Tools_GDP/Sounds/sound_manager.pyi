"""Type stubs for SoundManager - enables IDE autocomplete"""
from typing import Optional, Any, Union
from Actual_Tools_GDP.Sounds.sound_handle import SoundHandle

class SoundManager:
    """Manager for sound operations."""
    
    def get(self, sound_id: int) -> SoundHandle:
        """Get a sound by ID."""
        ...
    
    def count(self) -> int:
        """Get total number of sounds (including None)."""
        ...
    
    def exists(self, sound_id: int) -> bool:
        """Check if sound exists and is not None."""
        ...
        
    def count_active(self) -> int:
        """Get number of non-None sounds."""
        ...

    def delete(self, sound_id: int) -> bool:
        """Delete a sound (sets slot to None)."""
        ...

    def find_by_name(self, name: Union[str, int]) -> Optional[SoundHandle]:
        """Find a sound by its internal ID property."""
        ...

    def find_by_file_name(self, file_name: str) -> Optional[SoundHandle]:
        """Find first sound that contains a sound file with matching filename."""
        ...

    def add_new(
        self,
        sound_id: Optional[int] = None,
        play_delay: int = 0,
        cache_time: int = 300000,
        total_probability: int = 100,
    ) -> SoundHandle:
        """Add a new sound holder (container)."""
        ...

    def add_sound(
        self,
        sound_id: Optional[int] = None,
        play_delay: int = 0,
        cache_time: int = 300000,
        total_probability: int = 100,
    ) -> SoundHandle:
        """Alias for add_new."""
        ...

    def copy(self, source_id: int, target_id: Optional[int] = None) -> SoundHandle:
        """Copy a sound to a new ID."""
        ...

    def copy_to_clipboard(self, sound_id: int) -> bool:
        """Copy sound to internal clipboard."""
        ...

    def paste(self, target_id: Optional[int] = None) -> Optional[SoundHandle]:
        """Paste sound from clipboard."""
        ...

    def clear_clipboard(self) -> None:
        """Clear clipboard."""
        ...

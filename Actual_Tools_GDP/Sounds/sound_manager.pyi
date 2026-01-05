"""Type stubs for SoundManager - enables IDE autocomplete"""
from Actual_Tools_GDP.Sounds.sound_handle import SoundHandle

class SoundManager:
    """Manager for sound operations."""
    
    def get(self, sound_id: int) -> SoundHandle:
        """
        Get a sound by ID.
        
        Args:
            sound_id: ID of the sound
            
        Returns:
            SoundHandle for the sound
        """
        ...
    
    def count(self) -> int:
        """Get total number of sounds."""
        ...

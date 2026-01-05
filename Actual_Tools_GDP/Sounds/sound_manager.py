"""
SoundManager - Manages sound operations.

Responsibilities:
- Get sounds by ID
- Create new sounds
- Validate sound references
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

from Actual_Tools_GDP.Sounds.sound_handle import SoundHandle

__all__ = ["SoundManager"]


class SoundManager:
    """
    Manager for sound operations.
    
    Pattern: Receives workspace, accesses dat through workspace.dat.sounds
    """
    
    def __init__(self, workspace: GenieWorkspace) -> None:
        """
        Initialize SoundManager with workspace reference.
        
        Args:
            workspace: The GenieWorkspace instance
        """
        self.workspace = workspace
    
    def get(self, sound_id: int) -> SoundHandle:
        """
        Get a sound by ID.
        
        Args:
            sound_id: ID of the sound
            
        Returns:
            SoundHandle for the sound
            
        Raises:
            InvalidIdError: If sound_id is out of range
        """
        from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
        
        if sound_id < 0 or sound_id >= len(self.workspace.dat.sounds):
            raise InvalidIdError(
                f"Sound ID {sound_id} out of range (0-{len(self.workspace.dat.sounds)-1})"
            )
        
        return SoundHandle(self.workspace, sound_id)
    
    def count(self) -> int:
        """Get total number of sounds."""
        return len(self.workspace.dat.sounds)

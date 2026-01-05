"""
SoundHandle - Wrapper for individual Sound objects.

Provides attribute access to sound properties.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace

__all__ = ["SoundHandle"]


class SoundHandle:
    """
    Handle for a single sound.
    
    Provides direct attribute access to the underlying Sound object.
    """
    
    def __init__(self, workspace: GenieWorkspace, sound_id: int) -> None:
        """
        Initialize SoundHandle.
        
        Args:
            workspace: The GenieWorkspace instance
            sound_id: ID of the sound
        """
        object.__setattr__(self, '_workspace', workspace)
        object.__setattr__(self, '_id', sound_id)
        object.__setattr__(self, '_sound', workspace.dat.sounds[sound_id])
    
    @property
    def id(self) -> int:
        """Get the sound ID."""
        return self._id
    
    @property
    def workspace(self) -> GenieWorkspace:
        """Get the workspace."""
        return self._workspace
    
    def __getattr__(self, name: str) -> Any:
        """
        Get attribute from underlying sound.
        
        Args:
            name: Attribute name
            
        Returns:
            Attribute value from sound
        """
        return getattr(self._sound, name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        Set attribute on underlying sound.
        
        Args:
            name: Attribute name
            value: Value to set
        """
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._sound, name, value)
    
    def __repr__(self) -> str:
        return f"SoundHandle(id={self._id})"

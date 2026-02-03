"""
SoundHandle - Wrapper for individual Sound objects.

Provides attribute access to sound properties.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from aoe2_genie_tooling.Base.workspace import GenieWorkspace
    from aoe2_genie_tooling.Sounds.sound_file_handle import SoundFileHandle

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
    
    @property
    def sounds(self) -> list[SoundFileHandle]:
        """Get all actual sound entries inside this holder."""
        from aoe2_genie_tooling.Sounds.sound_file_handle import SoundFileHandle
        return [SoundFileHandle(self, i) for i in range(len(self._sound.sound_files))]

    # Alias for sounds
    files = sounds

    def new_sound(
        self,
        filename: str = "",
        sound_name: str = "",
        resource_id: int = -1,
        probability: int = 100,
        civilization_id: int = -1,
        icon_set: int = -1,
        **kwargs: Any
    ) -> SoundFileHandle:
        """
        Add a new actual sound file entry to this holder.
        
        Args:
            filename: Physical filename (e.g. "attack.wav")
            sound_name: Internal name (DE only)
            resource_id: Resource ID (optional)
            probability: Chance to play (0-100)
            civilization_id: Civilization filter (optional)
            icon_set: Icon set filter (optional)
            **kwargs: Supports 'file_name' as an alias for 'filename'
            
        Returns:
            SoundFileHandle for the new sound entry
        """
        from sections.sounds.sound_file import SoundFile
        from aoe2_genie_tooling.Sounds.sound_file_handle import SoundFileHandle
        
        # Support file_name alias
        final_filename = filename or kwargs.get("file_name", "")
        
        new_file = SoundFile(ver=self._sound.ver)
        
        # Safely set name/filename based on version support
        try:
            new_file.filename = final_filename
        except Exception:
            pass # Not supported in this version
            
        try:
            new_file.sound_name = sound_name or final_filename
        except Exception:
            pass # Not supported in this version

        new_file.resource_id = resource_id
        new_file.probability = probability
        new_file.civilization_id = civilization_id
        new_file.icon_set = icon_set
        
        self._sound.sound_files.append(new_file)
        self._sound.num_sound_files = len(self._sound.sound_files)
        
        return SoundFileHandle(self, len(self._sound.sound_files) - 1)

    def get_file(self, index: int) -> Optional[SoundFileHandle]:
        """Get a sound file by index."""
        from aoe2_genie_tooling.Sounds.sound_file_handle import SoundFileHandle
        if 0 <= index < len(self._sound.sound_files):
            return SoundFileHandle(self, index)
        return None

    def copy_sound(self, index: int, target_index: Optional[int] = None) -> Optional[SoundFileHandle]:
        """
        Copy a sound entry within this holder.
        
        Args:
            index: Source sound index
            target_index: Destination index. If None, appends to end.
            
        Returns:
            SoundFileHandle for the copy
        """
        if not (0 <= index < len(self._sound.sound_files)):
            return None
            
        source_sf = self._sound.sound_files[index]
        
        # We need the copy logic from manager or local
        from sections.sounds.sound_file import SoundFile
        new_sf = SoundFile(ver=source_sf.ver)
        attrs = ['resource_id', 'probability', 'civilization_id', 'icon_set', 'sound_name', 'filename']
        for attr in attrs:
            try:
                setattr(new_sf, attr, getattr(source_sf, attr))
            except Exception:
                pass
        
        if target_index is None:
            self._sound.sound_files.append(new_sf)
            target_index = len(self._sound.sound_files) - 1
        else:
            # Clamp target_index
            target_index = max(0, min(target_index, len(self._sound.sound_files)))
            self._sound.sound_files.insert(target_index, new_sf)
            
        self._sound.num_sound_files = len(self._sound.sound_files)
        from aoe2_genie_tooling.Sounds.sound_file_handle import SoundFileHandle
        return SoundFileHandle(self, target_index)

    def move_sound(self, source_index: int, target_index: int) -> bool:
        """
        Move a sound entry to a new position within this holder.
        
        Args:
            source_index: Index of sound to move
            target_index: New index position
            
        Returns:
            True if moved, False if out of range
        """
        if not (0 <= source_index < len(self._sound.sound_files)):
            return False
            
        # Clamp target
        target_index = max(0, min(target_index, len(self._sound.sound_files) - 1))
        
        if source_index == target_index:
            return True
            
        obj = self._sound.sound_files.pop(source_index)
        self._sound.sound_files.insert(target_index, obj)
        return True

    def remove_file(self, index: int) -> bool:
        """Remove a sound file by index."""
        if 0 <= index < len(self._sound.sound_files):
            del self._sound.sound_files[index]
            self._sound.num_sound_files = len(self._sound.sound_files)
            return True
        return False

    # Aliases
    remove_sound = remove_file
    add_file = new_sound
    get_sound = get_file

    def clear_files(self) -> None:
        """Remove all sound file entries."""
        self._sound.sound_files = []
        self._sound.num_sound_files = 0

    def exists(self) -> bool:
        """Check if this sound entry exists and is not None."""
        return self._sound is not None

    def __repr__(self) -> str:
        if not self.exists():
            return f"SoundHandle(id={self._id}, status=DELETED)"
        return f"SoundHandle(id={self._id}, name='{getattr(self, 'id', 'Unknown')}')"

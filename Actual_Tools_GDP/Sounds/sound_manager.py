"""
SoundManager - Manages sound operations.

Responsibilities:
- Get sounds by ID
- Create new sounds
- Validate sound references
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any, Union

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
        """Get total number of sounds (including None)."""
        return len(self.workspace.dat.sounds)

    def exists(self, sound_id: int) -> bool:
        """
        Check if sound exists.
        
        Since the sound list in DAT is dense (no None gaps),
        this just checks if the ID is within range.
        """
        return 0 <= sound_id < len(self.workspace.dat.sounds)
        
    def count_active(self) -> int:
        """Get number of sounds."""
        return len(self.workspace.dat.sounds)

    def delete(self, sound_id: int) -> bool:
        """
        Reset a sound to blank values.
        
        Args:
            sound_id: ID to reset
            
        Returns:
            True if reset, False if out of range
        """
        if self.exists(sound_id):
            template = self.workspace.dat.sounds[sound_id]
            self.workspace.dat.sounds[sound_id] = self._create_blank_sound(template.ver, sound_id)
            return True
        return False

    def find_by_name(self, name: Union[str, int]) -> Optional[SoundHandle]:
        """
        Find first sound matching name (the 'id' property inside the sound object).
        """
        name_str = str(name)
        for i, sound in enumerate(self.workspace.dat.sounds):
            if str(sound.id) == name_str:
                return SoundHandle(self.workspace, i)
        return None

    def find_by_file_name(self, file_name: str) -> Optional[SoundHandle]:
        """
        Find first sound that contains a sound file with matching filename.
        """
        fn_lower = file_name.lower()
        for i, sound in enumerate(self.workspace.dat.sounds):
            for sf in sound.sound_files:
                # Version-safe filename check
                current_fn = ""
                try:
                    current_fn = sf.filename
                except Exception:
                    try:
                        current_fn = sf.sound_name
                    except Exception:
                        pass
                
                if current_fn.lower() == fn_lower:
                    return SoundHandle(self.workspace, i)
        return None

    def _create_blank_sound(self, ver: Any, sound_id: int) -> Any:
        """Create a blank Sound object."""
        from sections.sounds.sound import Sound
        s = Sound(ver=ver)
        s.id = sound_id
        s.play_delay = 0
        s.cache_time = 0
        s.total_probability = 0
        s.num_sound_files = 0
        s.sound_files = []
        return s

    def add_new(
        self,
        sound_id: Optional[int] = None,
        play_delay: int = 0,
        cache_time: int = 300000,
        total_probability: int = 100,
    ) -> SoundHandle:
        """
        Add a new sound holder (container) to the mega-list.
        
        Args:
            sound_id: Target ID for list index. If None, appends to end
            play_delay: Delay before playing (default: 0)
            cache_time: Cache time (default: 300000)
            total_probability: Total probability (default: 100)
            
        Returns:
            SoundHandle for the new sound holder
        """
        from sections.sounds.sound import Sound
        
        target_idx = sound_id
        if target_idx is None:
            target_idx = len(self.workspace.dat.sounds)
        
        # Find template for version
        template_ver = None
        for s in self.workspace.dat.sounds:
            template_ver = s.ver
            break
        
        if template_ver is None:
             raise RuntimeError("Cannot add sound: DAT file has no existing sounds")
             
        new_sound = Sound(ver=template_ver)
        new_sound.id = target_idx
        new_sound.play_delay = play_delay
        new_sound.cache_time = cache_time
        new_sound.total_probability = total_probability
        new_sound.num_sound_files = 0
        new_sound.sound_files = []
        
        # Ensure capacity by filling with blank sounds
        while len(self.workspace.dat.sounds) <= target_idx:
            idx = len(self.workspace.dat.sounds)
            self.workspace.dat.sounds.append(self._create_blank_sound(template_ver, idx))
            
        self.workspace.dat.sounds[target_idx] = new_sound
        return SoundHandle(self.workspace, target_idx)

    # Alias for add_new
    add_sound = add_new

    def copy(self, source_id: int, target_id: Optional[int] = None) -> SoundHandle:
        """
        Copy a sound to a new ID.
        
        Args:
            source_id: Sound to copy
            target_id: Destination ID. If None, appends to end
            
        Returns:
            SoundHandle for the copy
        """
        from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError
        if not self.exists(source_id):
            raise InvalidIdError(f"Source sound {source_id} does not exist")
            
        source = self.workspace.dat.sounds[source_id]
        new_obj = self._copy_sound(source)
        
        if target_id is None:
            target_id = len(self.workspace.dat.sounds)
        
        new_obj.id = target_id
        
        while len(self.workspace.dat.sounds) <= target_id:
            idx = len(self.workspace.dat.sounds)
            self.workspace.dat.sounds.append(self._create_blank_sound(source.ver, idx))
            
        self.workspace.dat.sounds[target_id] = new_obj
        return SoundHandle(self.workspace, target_id)

    def _copy_sound(self, source: Any) -> Any:
        """Manual copy of Sound object."""
        from sections.sounds.sound import Sound
        new_sound = Sound(ver=source.ver)
        attrs = ['id', 'play_delay', 'cache_time', 'total_probability']
        for attr in attrs:
            setattr(new_sound, attr, getattr(source, attr))
        
        new_sound.num_sound_files = source.num_sound_files
        new_sound.sound_files = [self._copy_sound_file(sf) for sf in source.sound_files]
        return new_sound

    def _copy_sound_file(self, source: Any) -> Any:
        """Manual copy of SoundFile object."""
        from sections.sounds.sound_file import SoundFile
        new_sf = SoundFile(ver=source.ver)
        attrs = ['resource_id', 'probability', 'civilization_id', 'icon_set', 'sound_name', 'filename']
        for attr in attrs:
            try:
                setattr(new_sf, attr, getattr(source, attr))
            except Exception:
                pass # Not supported in this version
        return new_sf

    # Clipboard Implementation
    _clipboard: Optional[Any] = None

    def copy_to_clipboard(self, sound_id: int) -> bool:
        """Copy sound to internal clipboard."""
        if self.exists(sound_id):
            self.__class__._clipboard = self._copy_sound(self.workspace.dat.sounds[sound_id])
            return True
        return False

    def paste(self, target_id: Optional[int] = None) -> Optional[SoundHandle]:
        """Paste sound from clipboard."""
        if self.__class__._clipboard is None:
            return None
            
        pasted = self._copy_sound(self.__class__._clipboard)
        if target_id is None:
            target_id = len(self.workspace.dat.sounds)
        
        pasted.id = target_id
        
        while len(self.workspace.dat.sounds) <= target_id:
            idx = len(self.workspace.dat.sounds)
            self.workspace.dat.sounds.append(self._create_blank_sound(pasted.ver, idx))
            
        self.workspace.dat.sounds[target_id] = pasted
        return SoundHandle(self.workspace, target_id)

    def clear_clipboard(self) -> None:
        """Clear clipboard."""
        self.__class__._clipboard = None

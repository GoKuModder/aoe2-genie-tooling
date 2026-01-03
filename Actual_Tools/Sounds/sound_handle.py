"""
SoundHandle - High-level wrapper for Sound objects.

Provides attribute access and item management for Sounds.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from genieutils.sound import Sound, SoundItem

if TYPE_CHECKING:
    from genieutils.datfile import DatFile

__all__ = ["SoundHandle", "SoundItemHandle"]


class SoundItemHandle:
    """
    Wrapper for a SoundItem with its index.
    """
    
    __slots__ = ("_item", "_item_id")
    
    def __init__(self, item: SoundItem, item_id: int) -> None:
        object.__setattr__(self, "_item", item)
        object.__setattr__(self, "_item_id", item_id)
    
    def __repr__(self) -> str:
        return f"SoundItemHandle(id={self._item_id}, filename={self._item.filename!r})"
    
    @property
    def item_id(self) -> int:
        """Index in parent's items list."""
        return self._item_id
    
    @property
    def filename(self) -> str:
        """Sound filename."""
        return self._item.filename
    
    @filename.setter
    def filename(self, value: str) -> None:
        self._item.filename = value
    
    @property
    def resource_id(self) -> int:
        """Resource ID."""
        return self._item.resource_id
    
    @resource_id.setter
    def resource_id(self, value: int) -> None:
        self._item.resource_id = value
    
    @property
    def probability(self) -> int:
        """Playback probability (0-100)."""
        return self._item.probability
    
    @probability.setter
    def probability(self, value: int) -> None:
        self._item.probability = value
    
    @property
    def civilization(self) -> int:
        """Civ restriction (-1 = all)."""
        return self._item.civilization
    
    @civilization.setter
    def civilization(self, value: int) -> None:
        self._item.civilization = value
    
    @property
    def icon_set(self) -> int:
        """Icon set."""
        return self._item.icon_set
    
    @icon_set.setter
    def icon_set(self, value: int) -> None:
        self._item.icon_set = value


class SoundHandle:
    """
    High-level wrapper for Sound objects.
    
    Provides attribute access and item management.
    
    Example:
        >>> sound = sm.get(100)
        >>> sound.play_delay = 0.5
        >>> item = sound.add_item("attack.wav", probability=50)
    """
    
    __slots__ = ("_sound_id", "_dat_file")
    
    def __init__(self, sound_id: int, dat_file: DatFile) -> None:
        if sound_id < 0:
            raise ValueError(f"sound_id must be non-negative, got {sound_id}")
        object.__setattr__(self, "_sound_id", sound_id)
        object.__setattr__(self, "_dat_file", dat_file)
    
    def __repr__(self) -> str:
        s = self._sound
        items = len(s.items) if s else 0
        return f"SoundHandle(id={self._sound_id}, items={items})"
    
    # =========================================================================
    # CORE ACCESS
    # =========================================================================
    
    @property
    def _sound(self) -> Optional[Sound]:
        """Get the underlying Sound object."""
        if 0 <= self._sound_id < len(self._dat_file.sounds):
            return self._dat_file.sounds[self._sound_id]
        return None
    
    def exists(self) -> bool:
        """Check if this sound exists."""
        return self._sound is not None
    
    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================
    
    @property
    def id(self) -> int:
        """Sound ID."""
        return self._sound_id
    
    @property
    def play_delay(self) -> int:
        """Play delay."""
        s = self._sound
        return s.play_delay if s else 0
    
    @play_delay.setter
    def play_delay(self, value: int) -> None:
        s = self._sound
        if s:
            s.play_delay = value
    
    @property
    def cache_time(self) -> int:
        """Cache time."""
        s = self._sound
        return s.cache_time if s else 0
    
    @cache_time.setter
    def cache_time(self, value: int) -> None:
        s = self._sound
        if s:
            s.cache_time = value
    
    @property
    def total_probability(self) -> int:
        """Total probability."""
        s = self._sound
        return s.total_probability if s else 0
    
    @total_probability.setter
    def total_probability(self, value: int) -> None:
        s = self._sound
        if s:
            s.total_probability = value
    
    @property
    def items(self) -> List[SoundItem]:
        """Sound items list."""
        s = self._sound
        return s.items if s else []
    
    @items.setter
    def items(self, value: List[SoundItem]) -> None:
        s = self._sound
        if s:
            s.items = value
    
    @property
    def item_count(self) -> int:
        """Number of items."""
        s = self._sound
        return len(s.items) if s else 0
    
    # =========================================================================
    # ITEM MANAGEMENT
    # =========================================================================
    
    def add_item(
        self,
        filename: str,
        resource_id: int = 0,
        probability: int = 100,
        civilization: int = -1,
        icon_set: int = 0,
    ) -> Optional[SoundItemHandle]:
        """Add a sound item."""
        s = self._sound
        if s:
            item = SoundItem(
                filename=filename,
                resource_id=resource_id,
                probability=probability,
                civilization=civilization,
                icon_set=icon_set,
            )
            s.items.append(item)
            item_id = len(s.items) - 1
            return SoundItemHandle(item, item_id)
        return None
    
    def get_item(self, item_id: int) -> Optional[SoundItemHandle]:
        """Get an item by index."""
        s = self._sound
        if s and 0 <= item_id < len(s.items):
            return SoundItemHandle(s.items[item_id], item_id)
        return None
    
    def get_items(self) -> List[SoundItemHandle]:
        """Get all items as handles."""
        result = []
        s = self._sound
        if s:
            for i, item in enumerate(s.items):
                result.append(SoundItemHandle(item, i))
        return result
    
    def remove_item(self, item_id: int) -> bool:
        """Remove an item by index."""
        s = self._sound
        if s and 0 <= item_id < len(s.items):
            s.items.pop(item_id)
            return True
        return False
    
    def clear_items(self) -> None:
        """Remove all items."""
        s = self._sound
        if s:
            s.items.clear()
    
    # =========================================================================
    # DYNAMIC ACCESS
    # =========================================================================
    
    def __getattr__(self, name: str) -> Any:
        s = self._sound
        if s and hasattr(s, name):
            return getattr(s, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__slots__:
            object.__setattr__(self, name, value)
            return
        s = self._sound
        if s and hasattr(s, name):
            setattr(s, name, value)
            return
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

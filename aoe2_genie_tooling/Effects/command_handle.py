"""
CommandHandle - Wrapper for individual EffectCommand objects.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aoe2_genie_tooling.Effects.effect_handle import EffectHandle

__all__ = ["CommandHandle"]


class CommandHandle:
    """
    Handle for a single effect command entry within an effect holder.
    """
    
    def __init__(self, parent_handle: EffectHandle, command_id: int) -> None:
        """
        Initialize CommandHandle.
        
        Args:
            parent_handle: The EffectHandle owning this command
            command_id: Index in the effects list
        """
        object.__setattr__(self, '_parent', parent_handle)
        object.__setattr__(self, '_id', command_id)
        object.__setattr__(self, '_cmd', parent_handle._effect.effects[command_id])
    
    @property
    def index(self) -> int:
        """Get the index of this command in the holder's list."""
        return self._id

    @property
    def type(self) -> int:
        """Effect command type."""
        return self._cmd.type

    @type.setter
    def type(self, value: int) -> None:
        self._cmd.type = value

    @property
    def a(self) -> int:
        """Parameter A (often unit/class/attribute ID)."""
        return self._cmd.a

    @a.setter
    def a(self, value: int) -> None:
        self._cmd.a = value

    @property
    def b(self) -> int:
        """Parameter B (often amount/value)."""
        return self._cmd.b

    @b.setter
    def b(self, value: int) -> None:
        self._cmd.b = value

    @property
    def c(self) -> int:
        """Parameter C (often civ/class)."""
        return self._cmd.c

    @c.setter
    def c(self, value: int) -> None:
        self._cmd.c = value

    @property
    def d(self) -> float:
        """Parameter D (float value)."""
        return self._cmd.d

    @d.setter
    def d(self, value: float) -> None:
        self._cmd.d = value

    def __getattr__(self, name: str) -> Any:
        return getattr(self._cmd, name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._cmd, name, value)

    def __repr__(self) -> str:
        return f"CommandHandle(index={self._id}, type={self.type}, a={self.a}, b={self.b}, c={self.c}, d={self.d})"

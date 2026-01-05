"""
EffectHandle - High-level wrapper for Effect objects.

Provides attribute access and command management for Effects.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional

from ..backend import DatFile, Effect, EffectCommand

__all__ = ["EffectHandle", "EffectCommandHandle"]


class EffectCommandHandle:
    """
    Wrapper for an EffectCommand with its index.

    Attributes:
        command_id: Index in parent's effect_commands list.
        type_: Command type (effect type ID).
        a, b, c, d: Command parameters.
    """

    __slots__ = ("_cmd", "_command_id")

    def __init__(self, cmd: EffectCommand, command_id: int) -> None:
        object.__setattr__(self, "_cmd", cmd)
        object.__setattr__(self, "_command_id", command_id)

    def __repr__(self) -> str:
        return f"EffectCommandHandle(id={self._command_id}, type={self._cmd.type_})"

    @property
    def command_id(self) -> int:
        """Index in parent's command list."""
        return self._command_id

    @property
    def type_(self) -> int:
        """Effect command type."""
        return self._cmd.type_

    @type_.setter
    def type_(self, value: int) -> None:
        self._cmd.type_ = value

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


class EffectHandle:
    """
    High-level wrapper for Effect objects.

    Provides command management and attribute access.

    Example:
        >>> effect = em.get(100)
        >>> effect.name = "Upgrade Archer"
        >>> cmd = effect.add_command(type_=5, a=4, d=2.0)
        >>> print(cmd.command_id)
    """

    __slots__ = ("_effect_id", "_dat_file")

    def __init__(self, effect_id: int, dat_file: DatFile) -> None:
        if effect_id < 0:
            raise ValueError(f"effect_id must be non-negative, got {effect_id}")
        object.__setattr__(self, "_effect_id", effect_id)
        object.__setattr__(self, "_dat_file", dat_file)

    def __repr__(self) -> str:
        effect = self._effect
        name = effect.name if effect else "<not found>"
        cmds = len(effect.effect_commands) if effect else 0
        return f"EffectHandle(id={self._effect_id}, name={name!r}, commands={cmds})"

    # =========================================================================
    # CORE ACCESS
    # =========================================================================

    @property
    def _effect(self) -> Optional[Effect]:
        """Get the underlying Effect object."""
        if 0 <= self._effect_id < len(self._dat_file.effects):
            return self._dat_file.effects[self._effect_id]
        return None

    def exists(self) -> bool:
        """Check if this effect exists."""
        return self._effect is not None

    # =========================================================================
    # BASIC PROPERTIES
    # =========================================================================

    @property
    def id(self) -> int:
        """Effect ID."""
        return self._effect_id

    @property
    def name(self) -> str:
        """Effect name."""
        e = self._effect
        return e.name if e else ""

    @name.setter
    def name(self, value: str) -> None:
        e = self._effect
        if e:
            e.name = value

    @property
    def effect_commands(self) -> List[EffectCommand]:
        """List of effect commands."""
        e = self._effect
        return e.effect_commands if e else []

    @effect_commands.setter
    def effect_commands(self, value: List[EffectCommand]) -> None:
        e = self._effect
        if e:
            e.effect_commands = value

    @property
    def command_count(self) -> int:
        """Number of commands in this effect."""
        e = self._effect
        return len(e.effect_commands) if e else 0

    # =========================================================================
    # COMMAND MANAGEMENT
    # =========================================================================

    def add_command(
        self,
        type_: int,
        a: int = -1,
        b: int = -1,
        c: int = -1,
        d: float = 0.0,
    ) -> Optional[EffectCommandHandle]:
        """
        Add a command to this effect.

        Args:
            type_: Effect command type (see Datasets.effect_types).
            a: Parameter A (unit/class/attribute ID).
            b: Parameter B (amount/value).
            c: Parameter C (civ/class).
            d: Parameter D (float value).

        Returns:
            EffectCommandHandle for the new command.
        """
        e = self._effect
        if e:
            cmd = EffectCommand(type_=type_, a=a, b=b, c=c, d=d)
            e.effect_commands.append(cmd)
            cmd_id = len(e.effect_commands) - 1
            return EffectCommandHandle(cmd, cmd_id)
        return None

    def get_command(self, command_id: int) -> Optional[EffectCommandHandle]:
        """Get a command by index."""
        e = self._effect
        if e and 0 <= command_id < len(e.effect_commands):
            return EffectCommandHandle(e.effect_commands[command_id], command_id)
        return None

    def get_commands(self) -> List[EffectCommandHandle]:
        """Get all commands as handles."""
        result = []
        e = self._effect
        if e:
            for i, cmd in enumerate(e.effect_commands):
                result.append(EffectCommandHandle(cmd, i))
        return result

    def remove_command(self, command_id: int) -> bool:
        """
        Remove a command by index.

        Args:
            command_id: Index of command to remove.

        Returns:
            True if removed, False if not found.
        """
        e = self._effect
        if e and 0 <= command_id < len(e.effect_commands):
            e.effect_commands.pop(command_id)
            return True
        return False

    def clear_commands(self) -> None:
        """Remove all commands."""
        e = self._effect
        if e:
            e.effect_commands.clear()

    # =========================================================================
    # DYNAMIC ACCESS
    # =========================================================================

    def __getattr__(self, name: str) -> Any:
        e = self._effect
        if e and hasattr(e, name):
            return getattr(e, name)
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.__slots__:
            object.__setattr__(self, name, value)
            return
        e = self._effect
        if e and hasattr(e, name):
            setattr(e, name, value)
            return
        raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")

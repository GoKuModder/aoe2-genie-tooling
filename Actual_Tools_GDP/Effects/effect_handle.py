"""
EffectHandle - Wrapper for individual TechEffect (Effect Holder) objects.

Each Effect Holder has a name and contains a list of EffectCommands.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from Actual_Tools_GDP.Base.workspace import GenieWorkspace
    from Actual_Tools_GDP.Effects.command_handle import CommandHandle

__all__ = ["EffectHandle"]


class EffectHandle:
    """
    Handle for a single effect holder.
    
    Provides direct attribute access and command management.
    """
    
    def __init__(self, workspace: GenieWorkspace, effect_id: int) -> None:
        """
        Initialize EffectHandle.
        
        Args:
            workspace: The GenieWorkspace instance
            effect_id: ID of the effect
        """
        object.__setattr__(self, '_workspace', workspace)
        object.__setattr__(self, '_id', effect_id)
        object.__setattr__(self, '_effect', workspace.dat.tech_effects[effect_id])
    
    @property
    def id(self) -> int:
        """Get the effect ID."""
        return self._id
    
    @property
    def workspace(self) -> GenieWorkspace:
        """Get the workspace."""
        return self._workspace

    @property
    def name(self) -> str:
        """Get the effect name."""
        try:
            return self._effect.name
        except Exception:
            return ""

    @name.setter
    def name(self, value: str) -> None:
        """Set the effect name."""
        try:
            self._effect.name = value
        except Exception:
            pass

    @property
    def commands(self) -> list[CommandHandle]:
        """Get all effect commands inside this holder."""
        from Actual_Tools_GDP.Effects.command_handle import CommandHandle
        return [CommandHandle(self, i) for i in range(len(self._effect.effects))]

    # Alias
    effects = commands

    def new_command(
        self,
        type: int = 0,
        a: int = -1,
        b: int = -1,
        c: int = -1,
        d: float = 0.0,
    ) -> CommandHandle:
        """
        Add a new effect command to this holder.
        
        Args:
            type: Command type (effect type ID)
            a: Parameter A (unit/class/attribute)
            b: Parameter B (amount/value)
            c: Parameter C (civ/class)
            d: Parameter D (float value)
            
        Returns:
            CommandHandle for the new command
        """
        from sections.tech_effect.effect_command import EffectCommand
        from Actual_Tools_GDP.Effects.command_handle import CommandHandle
        
        new_cmd = EffectCommand(ver=self._effect.ver)
        new_cmd.type = type
        new_cmd.a = a
        new_cmd.b = b
        new_cmd.c = c
        new_cmd.d = d
        
        self._effect.effects.append(new_cmd)
        return CommandHandle(self, len(self._effect.effects) - 1)

    # Alias
    add_command = new_command

    def get_command(self, index: int) -> Optional[CommandHandle]:
        """Get a command by index."""
        from Actual_Tools_GDP.Effects.command_handle import CommandHandle
        if 0 <= index < len(self._effect.effects):
            return CommandHandle(self, index)
        return None

    def copy_command(self, index: int, target_index: Optional[int] = None) -> Optional[CommandHandle]:
        """
        Copy a command within this holder.
        
        Args:
            index: Source command index
            target_index: Destination index. If None, appends to end.
            
        Returns:
            CommandHandle for the copy
        """
        if not (0 <= index < len(self._effect.effects)):
            return None
            
        source_cmd = self._effect.effects[index]
        
        from sections.tech_effect.effect_command import EffectCommand
        new_cmd = EffectCommand(ver=source_cmd.ver)
        attrs = ['type', 'a', 'b', 'c', 'd']
        for attr in attrs:
            try:
                setattr(new_cmd, attr, getattr(source_cmd, attr))
            except Exception:
                pass
        
        if target_index is None:
            self._effect.effects.append(new_cmd)
            target_index = len(self._effect.effects) - 1
        else:
            target_index = max(0, min(target_index, len(self._effect.effects)))
            self._effect.effects.insert(target_index, new_cmd)
            
        from Actual_Tools_GDP.Effects.command_handle import CommandHandle
        return CommandHandle(self, target_index)

    def move_command(self, source_index: int, target_index: int) -> bool:
        """
        Move a command to a new position within this holder.
        
        Args:
            source_index: Index of command to move
            target_index: New index position
            
        Returns:
            True if moved, False if out of range
        """
        if not (0 <= source_index < len(self._effect.effects)):
            return False
            
        target_index = max(0, min(target_index, len(self._effect.effects) - 1))
        
        if source_index == target_index:
            return True
            
        obj = self._effect.effects.pop(source_index)
        self._effect.effects.insert(target_index, obj)
        return True

    def remove_command(self, index: int) -> bool:
        """Remove a command by index."""
        if 0 <= index < len(self._effect.effects):
            del self._effect.effects[index]
            return True
        return False

    def clear_commands(self) -> None:
        """Remove all commands."""
        self._effect.effects = []

    def exists(self) -> bool:
        """Check if this effect entry exists."""
        return self._effect is not None

    def __getattr__(self, name: str) -> Any:
        """Get attribute from underlying effect."""
        return getattr(self._effect, name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute on underlying effect."""
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(self._effect, name, value)

    def __repr__(self) -> str:
        if not self.exists():
            return f"EffectHandle(id={self._id}, status=DELETED)"
        return f"EffectHandle(id={self._id}, name='{self.name}', commands={len(self.commands)})"

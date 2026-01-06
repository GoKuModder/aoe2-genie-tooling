"""Type stubs for EffectHandle - enables IDE autocomplete"""
from typing import Any, Optional
from Actual_Tools_GDP.Effects.command_handle import CommandHandle

class EffectHandle:
    """Handle for a single effect holder."""
    
    @property
    def id(self) -> int:
        """Get the effect ID."""
        ...
    
    @property
    def name(self) -> str:
        """Get the effect name."""
        ...

    @name.setter
    def name(self, value: str) -> None:
        ...

    @property
    def commands(self) -> list[CommandHandle]:
        """Get all effect commands inside this holder."""
        ...

    @property
    def effects(self) -> list[CommandHandle]:
        """Alias for commands."""
        ...

    def new_command(
        self,
        type: int = 0,
        a: int = -1,
        b: int = -1,
        c: int = -1,
        d: float = 0.0,
    ) -> CommandHandle:
        """Add a new effect command to this holder."""
        ...

    def add_command(
        self,
        type: int = 0,
        a: int = -1,
        b: int = -1,
        c: int = -1,
        d: float = 0.0,
    ) -> CommandHandle:
        """Alias for new_command."""
        ...

    def get_command(self, index: int) -> Optional[CommandHandle]:
        """Get a command by index."""
        ...

    def copy_command(self, index: int, target_index: Optional[int] = None) -> Optional[CommandHandle]:
        """Copy a command within this holder."""
        ...

    def move_command(self, source_index: int, target_index: int) -> bool:
        """Move a command to a new position within this holder."""
        ...

    def remove_command(self, index: int) -> bool:
        """Remove a command by index."""
        ...

    def clear_commands(self) -> None:
        """Remove all commands."""
        ...

    def exists(self) -> bool:
        """Check if this effect entry exists."""
        ...

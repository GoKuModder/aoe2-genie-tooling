"""Type stubs for CommandHandle - enables IDE autocomplete"""
from typing import Any

class CommandHandle:
    """Handle for a single effect command entry."""
    
    @property
    def index(self) -> int:
        """Get the index of this command in the holder's list."""
        ...

    @property
    def type(self) -> int:
        """Effect command type."""
        ...

    @type.setter
    def type(self, value: int) -> None:
        ...

    @property
    def a(self) -> int:
        """Parameter A (often unit/class/attribute ID)."""
        ...

    @a.setter
    def a(self, value: int) -> None:
        ...

    @property
    def b(self) -> int:
        """Parameter B (often amount/value)."""
        ...

    @b.setter
    def b(self, value: int) -> None:
        ...

    @property
    def c(self) -> int:
        """Parameter C (often civ/class)."""
        ...

    @c.setter
    def c(self, value: int) -> None:
        ...

    @property
    def d(self) -> float:
        """Parameter D (float value)."""
        ...

    @d.setter
    def d(self, value: float) -> None:
        ...

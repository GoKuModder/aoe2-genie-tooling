from __future__ import annotations
import sys
from typing import TYPE_CHECKING, Any, Protocol, List, Optional, Union

# Protocol definitions to ensure structural compatibility
class UnitProtocol(Protocol):
    id: int
    name: str
    hit_points: int
    # ... adds stability for type checkers

# =============================================================================
# BACKEND SELECTION
# =============================================================================

# Default to None, will be populated below
DatFile = None
Unit = None
Civ = None
Tech = None
Graphic = None

BACKEND_NAME = "unknown"

try:
    # -------------------------------------------------------------------------
    # OPTION 1: GenieDatParser (High Performance)
    # -------------------------------------------------------------------------
    from sections.datfile_sections import DatFile as _G_DatFile
    from sections.civilization.unit import Unit as _G_Unit
    from sections.civilization.civilization import Civilization as _G_Civ
    from sections.tech.tech import Tech as _G_Tech
    from sections.sprite_data.sprite import Sprite as _G_Sprite

    BACKEND_NAME = "GenieDatParser"

    class UnitWrapper:
        """
        Wraps GenieDatParser.Unit to provide a flat API matching genieutils-py.
        Forward attributes to sub-structs (movement_info, combat_info, etc.)
        """
        __slots__ = ('_wrapped',)

        def __init__(self, wrapped_unit: _G_Unit):
            self._wrapped = wrapped_unit

        def __getattr__(self, name: str) -> Any:
            # 1. Try direct attribute (id, name, hit_points)
            if hasattr(self._wrapped, name):
                return getattr(self._wrapped, name)

            # 2. Try sub-structs (order matters for precedence)
            # Common ones first for performance
            for sub in ('movement_info', 'combat_info', 'creation_info',
                        'building_info', 'projectile_info', 'task_info'):
                sub_obj = getattr(self._wrapped, sub, None)
                if sub_obj and hasattr(sub_obj, name):
                    return getattr(sub_obj, name)

            raise AttributeError(f"'Unit' object has no attribute '{name}'")

        def __setattr__(self, name: str, value: Any) -> None:
            if name == '_wrapped':
                super().__setattr__(name, value)
                return

            # 1. Try direct attribute
            if hasattr(self._wrapped, name):
                setattr(self._wrapped, name, value)
                return

            # 2. Try sub-structs
            for sub in ('movement_info', 'combat_info', 'creation_info',
                        'building_info', 'projectile_info', 'task_info'):
                sub_obj = getattr(self._wrapped, sub, None)
                if sub_obj and hasattr(sub_obj, name):
                    setattr(sub_obj, name, value)
                    return

            # If not found, maybe set it on _wrapped anyway (dynamic attrs?)
            # or raise helper error
            super().__setattr__(name, value)

        # Proxy connection for equality checks
        def __eq__(self, other):
            if isinstance(other, UnitWrapper):
                return self._wrapped == other._wrapped
            return self._wrapped == other

    class DatFileWrapper:
        """Shim for GenieDatParser DatFile to match genieutils-py API."""
        def __init__(self, wrapped: _G_DatFile):
            self._wrapped = wrapped

        @classmethod
        def parse(cls, path: str) -> 'DatFileWrapper':
            return cls(_G_DatFile.from_file(path))

        @classmethod
        def from_file(cls, path: str) -> 'DatFileWrapper':
            return cls(_G_DatFile.from_file(path))

        def save(self, path: str) -> None:
            self._wrapped.to_file(path)

        def write(self, path: str) -> None:
            self._wrapped.to_file(path)

        # Property Aliases
        @property
        def civs(self) -> List[_G_Civ]:
            return self._wrapped.civilizations

        @property
        def techs(self) -> List[_G_Tech]:
            return self._wrapped.techs

        @property
        def graphics(self) -> List[_G_Sprite]:
            return self._wrapped.sprites

        @property
        def terrains(self):
            return self._wrapped.terrain_data.terrains

        # Proxy everything else
        def __getattr__(self, name):
            return getattr(self._wrapped, name)

    # Expose the Wrappers as the standard names
    DatFile = DatFileWrapper
    Unit = UnitWrapper
    Civ = _G_Civ
    Tech = _G_Tech
    Graphic = _G_Sprite

except ImportError:
    # -------------------------------------------------------------------------
    # OPTION 2: genieutils-py (Legacy / Fallback)
    # -------------------------------------------------------------------------
    try:
        from genieutils.datfile import DatFile
        from genieutils.unit import Unit
        from genieutils.civilization import Civilizations as Civ
        from genieutils.tech import Tech
        from genieutils.graphic import Graphic

        BACKEND_NAME = "genieutils-py"

    except ImportError:
        # No backend found
        BACKEND_NAME = "none"

# =============================================================================
# EXPORTS
# =============================================================================
__all__ = ["DatFile", "Unit", "Civ", "Tech", "Graphic", "BACKEND_NAME"]

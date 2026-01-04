from __future__ import annotations
import sys
from typing import TYPE_CHECKING, Any, Protocol, List, Optional, Union

# Protocol definitions to ensure structural compatibility
class UnitProtocol(Protocol):
    id: int
    name: str
    hit_points: int
    # ... adds stability for type checkers

# BACKEND SELECTION

# Default to None, will be populated below
DatFile = None
Unit = None
Civ = None
Tech = None
Graphic = None
Sound = None
SoundItem = None
Effect = None
EffectCommand = None

BACKEND_NAME = "unknown"

try:
    # -------------------------------------------------------------------------
    # OPTION 1: Genie-Rust (High Performance)
    # -------------------------------------------------------------------------
    from sections.datfile_sections import DatFile as _G_DatFile
    from sections.civilization.unit import Unit as _G_Unit
    from sections.civilization.civilization import Civilization as _G_Civ
    from sections.tech.tech import Tech as _G_Tech
    from sections.sprite_data.sprite import Sprite as _G_Sprite
    from sections.tech_effect.tech_effect import TechEffect as _G_Effect
    from sections.tech_effect.effect_command import EffectCommand as _G_EffectCommand

    BACKEND_NAME = "GenieDatParser"

    class UnitWrapper:
        """
        Wraps Genie-Rust.Unit to provide a flat API matching genieutils-py.
        Forward attributes to sub-structs (type_50, creatable, etc.)
        """
        __slots__ = ('_wrapped',)

        def __init__(self, wrapped_unit: _G_Unit):
            self._wrapped = wrapped_unit

        def __getattr__(self, name: str) -> Any:
            # 1. Try direct attribute (id, name, hit_points, speed)
            if hasattr(self._wrapped, name):
                return getattr(self._wrapped, name)

            # 2. Try sub-structs (order matters for precedence)
            # Common ones first for performance
            # Based on genie-rust/sections logic, these are the sub-structs
            for sub in ('type_50', 'creatable', 'building', 'projectile'):
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
            for sub in ('type_50', 'creatable', 'building', 'projectile'):
                sub_obj = getattr(self._wrapped, sub, None)
                if sub_obj and hasattr(sub_obj, name):
                    setattr(sub_obj, name, value)
                    return

            # If not found, set on wrapper (though this might vanish)
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
        
        @civs.setter
        def civs(self, value):
            self._wrapped.civilizations = value

        @property
        def techs(self) -> List[_G_Tech]:
            return self._wrapped.techs

        @techs.setter
        def techs(self, value):
             self._wrapped.techs = value

        @property
        def graphics(self) -> List[_G_Sprite]:
            return self._wrapped.sprites
        
        @graphics.setter
        def graphics(self, value):
             self._wrapped.sprites = value
             
        @property
        def effects(self) -> List[_G_Effect]:
             return self._wrapped.effects
             
        @effects.setter
        def effects(self, value):
             self._wrapped.effects = value

        @property
        def terrains(self):
            return self._wrapped.terrain_data.terrains

        def __getattr__(self, name: str) -> Any:
            # 1. Try direct attribute on the wrapped object
            if hasattr(self._wrapped, name):
                return getattr(self._wrapped, name)

            # 2. Try sub-structs for nested properties
            # Based on genieutils-py structure and likely mappings
            sub_struct_map = {
                'terrain_data': [
                    'float_ptr_terrain_tables', 'terrain_pass_graphic_pointers',
                    'terrain_restrictions', 'terrain_block'
                ],
                'player_data': ['player_colours'],
                'map_data': ['random_maps'],
                'kill_stats': [
                    'razing_kill_rate', 'razing_kill_total',
                    'unit_hit_point_rate', 'unit_hit_point_total',
                    'unit_kill_rate', 'unit_kill_total'
                ]
            }

            for sub_name, properties in sub_struct_map.items():
                if name in properties:
                    sub_obj = getattr(self._wrapped, sub_name, None)
                    if sub_obj and hasattr(sub_obj, name):
                        return getattr(sub_obj, name)

            # 3. If nothing is found, raise an error
            raise AttributeError(f"'DatFile' object has no attribute '{name}'")

    # Expose the Wrappers as the standard names
    DatFile = DatFileWrapper
    Unit = UnitWrapper
    Civ = _G_Civ
    Tech = _G_Tech
    Graphic = _G_Sprite
    Sound = None # Placeholder if Sound not available
    SoundItem = None
    Effect = _G_Effect
    EffectCommand = _G_EffectCommand


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
        # genieutils might not have Effect exposed top-level in same way, 
        # but let's try to grab whatever we can or set None
        try:
             from genieutils.tech import Effect, EffectCommand
        except ImportError:
             Effect = None
             EffectCommand = None

        BACKEND_NAME = "genieutils-py"
        Sound = None
        SoundItem = None
        
    except ImportError:
        # No backend found
        BACKEND_NAME = "none"

# EXPORTS
__all__ = ["DatFile", "Unit", "Civ", "Tech", "Graphic", "Sound", "SoundItem", "Effect", "EffectCommand", "BACKEND_NAME"]

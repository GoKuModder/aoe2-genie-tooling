"""
Adapter module providing genieutils-py compatible interface over genie_rust.

This allows existing code using genieutils-py to work with minimal changes.

Usage:
    from Actual_Tools_GDP.Shared.dat_adapter import DatFile, Unit, Civ
    
    dat = DatFile.parse("path/to/file.dat")
    print(dat.civs[0].name)
    dat.save("path/to/output.dat")
"""
from __future__ import annotations

from typing import List, Optional, Any

# Import directly from genie_rust package
from sections.datfile_sections import DatFile as _GRDatFile
from sections.civilization.unit import Unit
from sections.civilization.civilization import Civilization as Civ
from sections.sprite_data.sprite import Sprite as Graphic
from sections.sounds.sound import Sound
from sections.sounds.sound_file import SoundFile as SoundItem
from sections.tech.tech import Tech
from sections.tech_effect.tech_effect import TechEffect as Effect
from sections.civilization.type_info.combat_info import CombatInfo as Type50
from sections.civilization.type_info.projectile_info import ProjectileInfo as Projectile
from sections.civilization.type_info.creation_info import CreationInfo as Creatable
from sections.civilization.type_info.building_info import BuildingInfo as Building
from sections.civilization.type_info.damage_class import DamageClass as AttackOrArmor
from sections.civilization.type_info.creation_info import TrainLocation
from sections.civilization.type_info.unit_cost import UnitCost as ResourceStorage
from sections.sprite_data.sprite_delta import SpriteDelta as GraphicDelta
from sections.sprite_data.facet_attack_sound import FacetAttackSound as GraphicAngleSound
from sections.unit_data.unit_task import UnitTask as Task

# Missing/Placeholder classes
class Bird: pass
class DeadFish: pass

# Re-export for compatibility
Civilization = Civ
DamageGraphic = ResourceStorage  # Name alias if needed
Sprite = Graphic
SpriteDelta = GraphicDelta
FacetAttackSound = GraphicAngleSound
TechEffect = Effect


class Version:
    """Compatibility shim for genieutils Version enum."""
    
    VER88 = "VER 8.8"
    
    @staticmethod
    def from_bytes(data: bytes) -> str:
        return data.decode("ascii", errors="ignore").strip("\x00")


class DatFile:
    """
    Adapter providing genieutils-py compatible access to genie_rust.DatFile.
    
    Attribute mappings:
    - civs -> civs (native)
    - graphics -> graphics (native)
    - effects -> effects (native)
    """
    
    def __init__(self, inner: _GRDatFile):
        self._inner = inner
    
    @classmethod
    def parse(cls, path: str) -> "DatFile":
        """Load a .dat file (genieutils-py compatible method name)."""
        return cls(_GRDatFile.from_file(path))
    
    @classmethod
    def from_file(cls, path: str) -> "DatFile":
        """Load a .dat file (alternative method name)."""
        return cls.parse(path)
    
    def save(self, path: str) -> None:
        """Save the .dat file to disk."""
        self._inner.to_file(path)
    
    def to_file(self, path: str) -> None:
        """Save the .dat file (GenieDatParser method name)."""
        self.save(path)
    
    # --- Direct Access Properties ---
    
    @property
    def version(self) -> str:
        """File version string."""
        return getattr(self._inner, 'version', "VER 8.8")
    
    @property
    def civs(self) -> List:
        """Civilizations list."""
        return self._inner.civilizations
    
    @civs.setter
    def civs(self, value: List) -> None:
        self._inner.civilizations = value
    
    @property
    def graphics(self) -> List:
        """Graphics/Sprites list."""
        return self._inner.sprites
    
    @graphics.setter
    def graphics(self, value: List) -> None:
        self._inner.sprites = value
    
    @property
    def sounds(self) -> List:
        """Sounds list."""
        return self._inner.sounds
    
    @sounds.setter
    def sounds(self, value: List) -> None:
        self._inner.sounds = value
    
    @property
    def effects(self) -> List:
        """Effects list."""
        return self._inner.tech_effects
    
    @effects.setter
    def effects(self, value: List) -> None:
        self._inner.tech_effects = value
    
    @property
    def techs(self) -> List:
        """Techs list."""
        return self._inner.techs
    
    @techs.setter
    def techs(self, value: List) -> None:
        self._inner.techs = value
    
    @property
    def terrain_restrictions(self):
        """Access terrain_restrictions."""
        # Maps to terrain_tables in sections.terrain_table_data
        return getattr(self._inner.terrain_table_data, 'terrain_tables', [])
    
    @property
    def player_colours(self):
        """Access player_colours."""
        # Try acceptable fields for different versions
        cd = getattr(self._inner, 'color_data', None)
        if not cd:
            return []
        
        try:
             return cd.player_color_data_age1
        except (AttributeError, ValueError, Exception): # Catch version mismatch error
             pass
             
        try:
             return cd.player_color_data_age2
        except (AttributeError, ValueError, Exception):
             return []
    
    @property
    def tech_tree(self):
        """Access tech_tree."""
        return getattr(self._inner, 'tech_tree', None)
    
    # --- Passthrough for any unhandled attributes ---
    
    def __getattr__(self, name: str) -> Any:
        """Fallback to inner object for any unhandled attributes."""
        return getattr(self._inner, name)


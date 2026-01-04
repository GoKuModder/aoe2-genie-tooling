"""
Adapter module providing genieutils-py compatible interface over GenieDatParser.

This allows existing code using genieutils-py to work with minimal changes.

Usage:
    from Actual_Tools_GDP.Shared.dat_adapter import DatFile, Version, Unit, Civ
    
    dat = DatFile.parse("path/to/file.dat")
    print(dat.civs[0].name)
    dat.save("path/to/output.dat")
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional, Any

# Add GenieDatParser to path
GDP_PATH = Path(__file__).parent.parent.parent / "GenieDatParser" / "src"
if str(GDP_PATH) not in sys.path:
    sys.path.insert(0, str(GDP_PATH))

# --- Import from GenieDatParser ---
from sections.datfile_sections import DatFile as _GDPDatFile
from sections.civilization import Civilization as _GDPCivilization
from sections.civilization.unit import Unit as _GDPUnit
from sections.civilization.unit_damage_sprite import UnitDamageSprite
from sections.civilization.unit_resource import UnitResource
from sections.sounds import Sound as _GDPSound
from sections.sounds.sound_file import SoundFile as _GDPSoundFile
from sections.sprite_data import Sprite as _GDPSprite
from sections.sprite_data.sprite_delta import SpriteDelta as _GDPSpriteDelta
from sections.sprite_data.facet_attack_sound import FacetAttackSound as _GDPFacetAttackSound
from sections.tech import Tech as _GDPTech
from sections.tech_effect import TechEffect as _GDPTechEffect

# --- Type Aliases for genieutils-py compatibility ---

# Civilization types
Civ = _GDPCivilization
Civilization = _GDPCivilization

# Unit types
Unit = _GDPUnit
DamageGraphic = UnitDamageSprite  # genieutils calls it DamageGraphic
ResourceStorage = UnitResource    # genieutils calls it ResourceStorage

# Sound types
Sound = _GDPSound
SoundItem = _GDPSoundFile  # genieutils calls it SoundItem, GDP calls it SoundFile
SoundFile = _GDPSoundFile

# Graphics/Sprite types
Graphic = _GDPSprite
Sprite = _GDPSprite
GraphicDelta = _GDPSpriteDelta    # genieutils calls it GraphicDelta, GDP calls it SpriteDelta
SpriteDelta = _GDPSpriteDelta
GraphicAngleSound = _GDPFacetAttackSound  # genieutils name
FacetAttackSound = _GDPFacetAttackSound

# Tech types
Tech = _GDPTech
Effect = _GDPTechEffect
TechEffect = _GDPTechEffect

# Try to import additional types if available
try:
    from sections.civilization.type_info import (
        AnimationInfo, MovementInfo, TaskInfo, CreationInfo, 
        ProjectileInfo, CombatInfo, BuildingInfo
    )
    # Aliases for genieutils names
    Type50 = CombatInfo
    Projectile = ProjectileInfo
    Creatable = CreationInfo
    Building = BuildingInfo
    DeadFish = MovementInfo
    Bird = TaskInfo
except ImportError:
    pass

# Task type
try:
    from sections.civilization.type_info.task_info import Task as _GDPTask
    Task = _GDPTask
except ImportError:
    try:
        from sections.unit_data.task import Task as _GDPTask
        Task = _GDPTask
    except ImportError:
        Task = None

# Attack/Armor types
try:
    from sections.civilization.type_info.combat_info import AttackOrArmour
    AttackOrArmor = AttackOrArmour  # American spelling alias
except ImportError:
    AttackOrArmor = None

# TrainLocation
try:
    from sections.tech.research_location import ResearchLocation
    TrainLocation = ResearchLocation
except ImportError:
    TrainLocation = None


class Version:
    """Compatibility shim for genieutils Version enum."""
    
    VER88 = "VER 8.8"
    
    @staticmethod
    def from_bytes(data: bytes) -> str:
        return data.decode("ascii", errors="ignore").strip("\x00")


class DatFile:
    """
    Adapter providing genieutils-py compatible access to GenieDatParser.
    
    Attribute mappings:
    - civs -> civilizations
    - graphics -> sprites
    - effects -> tech_effects
    """
    
    def __init__(self, inner: _GDPDatFile):
        self._inner = inner
    
    @classmethod
    def parse(cls, path: str) -> "DatFile":
        """Load a .dat file (genieutils-py compatible method name)."""
        return cls(_GDPDatFile.from_file(path))
    
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
    
    # --- Property Aliases ---
    
    @property
    def version(self) -> str:
        """File version string."""
        return Version.from_bytes(self._inner.file_version)
    
    @property
    def civs(self) -> List[_GDPCivilization]:
        """Civilizations list (alias for 'civilizations')."""
        return self._inner.civilizations
    
    @civs.setter
    def civs(self, value: List[_GDPCivilization]) -> None:
        self._inner.civilizations = value
    
    @property
    def graphics(self) -> List[Optional[_GDPSprite]]:
        """Graphics/Sprites list (alias for 'sprites')."""
        return self._inner.sprites
    
    @graphics.setter
    def graphics(self, value: List[Optional[_GDPSprite]]) -> None:
        self._inner.sprites = value
    
    @property
    def sounds(self) -> List[_GDPSound]:
        """Sounds list."""
        return self._inner.sounds
    
    @sounds.setter
    def sounds(self, value: List[_GDPSound]) -> None:
        self._inner.sounds = value
    
    @property
    def effects(self) -> List[_GDPTechEffect]:
        """Effects list (alias for 'tech_effects')."""
        return self._inner.tech_effects
    
    @effects.setter
    def effects(self, value: List[_GDPTechEffect]) -> None:
        self._inner.tech_effects = value
    
    @property
    def techs(self) -> List[_GDPTech]:
        """Techs list."""
        return self._inner.techs
    
    @techs.setter
    def techs(self, value: List[_GDPTech]) -> None:
        self._inner.techs = value
    
    # --- Direct Access to Inner Object ---
    
    @property
    def terrain_restrictions(self):
        """Access terrain_table_data (genieutils-py name)."""
        return self._inner.terrain_table_data
    
    @property
    def player_colours(self):
        """Access color_data (genieutils-py name)."""
        return self._inner.color_data
    
    @property
    def tech_tree(self):
        """Access tech_tree."""
        return self._inner.tech_tree
    
    # --- Passthrough for any unhandled attributes ---
    
    def __getattr__(self, name: str) -> Any:
        """Fallback to inner object for any unhandled attributes."""
        return getattr(self._inner, name)

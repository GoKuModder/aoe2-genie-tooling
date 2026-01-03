"""
Pytest configuration and fixtures for Actual_Tools tests.

Provides lightweight mock objects (FakeDatFile, FakeCiv) for testing
without requiring actual DAT files.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, List, Optional, Tuple
from unittest.mock import MagicMock

import pytest


# -------------------------
# Fake Data Classes
# -------------------------

@dataclass
class FakeResourceCost:
    """Fake ResourceCost for testing."""
    type: int = 0
    amount: int = 0
    flag: int = 1


@dataclass
class FakeTrainLocation:
    """Fake TrainLocation for testing."""
    train_time: int = 30
    unit_id: int = -1
    button_id: int = 0
    hot_key_id: int = 16000


@dataclass
class FakeAttackOrArmor:
    """Fake AttackOrArmor for testing."""
    class_: int = 0
    amount: int = 0


@dataclass
class FakeType50:
    """Fake Type50 combat data for testing."""
    base_armor: int = 0
    attacks: List[FakeAttackOrArmor] = field(default_factory=list)
    armours: List[FakeAttackOrArmor] = field(default_factory=list)
    displayed_attack: int = 0
    displayed_melee_armour: int = 0
    attack_graphic: int = -1
    attack_graphic_2: int = -1


@dataclass
class FakeCreatable:
    """Fake Creatable training data for testing."""
    resource_costs: Tuple[FakeResourceCost, FakeResourceCost, FakeResourceCost] = field(
        default_factory=lambda: (
            FakeResourceCost(type=0, amount=0),  # Food
            FakeResourceCost(type=1, amount=0),  # Wood
            FakeResourceCost(type=3, amount=0),  # Gold
        )
    )
    train_locations: List[FakeTrainLocation] = field(
        default_factory=lambda: [FakeTrainLocation()]
    )
    displayed_pierce_armour: int = 0


@dataclass
class FakeUnit:
    """
    Fake Unit for testing (duck-typed to match genieutils.unit.Unit).
    """
    type: int = 70  # Creatable type
    id: int = 0
    name: str = "Test Unit"
    enabled: int = 1
    hit_points: int = 100
    line_of_sight: float = 4.0
    garrison_capacity: int = 0
    speed: Optional[float] = 1.0
    standing_graphic: Tuple[int, int] = (100, -1)
    dying_graphic: int = 200
    selection_sound: int = 300
    dying_sound: int = 301
    train_sound: int = 302
    damage_sound: int = 303
    type_50: Optional[FakeType50] = field(default_factory=FakeType50)
    creatable: Optional[FakeCreatable] = field(default_factory=FakeCreatable)
    # Additional fields that may be accessed
    language_dll_name: int = 0
    language_dll_creation: int = 0
    class_: int = 0
    undead_graphic: int = -1
    undead_mode: int = 0
    collision_size_x: float = 0.0
    collision_size_y: float = 0.0
    collision_size_z: float = 0.0
    dead_unit_id: int = -1
    blood_unit_id: int = -1
    sort_number: int = 0
    can_be_built_on: int = 0
    icon_id: int = 0
    hide_in_editor: int = 0
    old_portrait_pict: int = -1
    disabled: int = 0
    placement_side_terrain: Tuple[int, int] = (-1, -1)
    placement_terrain: Tuple[int, int] = (-1, -1)
    clearance_size: Tuple[float, float] = (0.0, 0.0)
    hill_mode: int = 0
    fog_visibility: int = 0
    terrain_restriction: int = 0
    fly_mode: int = 0
    resource_capacity: int = 0
    resource_decay: float = 0.0
    blast_defense_level: int = 0
    combat_level: int = 0
    interaction_mode: int = 0
    minimap_mode: int = 0
    interface_kind: int = 0
    multiple_attribute_mode: float = 0.0
    minimap_color: int = 0
    language_dll_help: int = 0
    language_dll_hotkey_text: int = 0
    hot_key: int = 16000
    recyclable: int = 0
    enable_auto_gather: int = 0
    create_doppelganger_on_death: int = 0
    resource_gather_group: int = 0
    occlusion_mode: int = 0
    obstruction_type: int = 0
    obstruction_class: int = 0
    trait: int = 0
    civilization: int = 0
    nothing: int = 0
    selection_effect: int = 0
    editor_selection_colour: int = 0
    outline_size_x: float = 0.0
    outline_size_y: float = 0.0
    outline_size_z: float = 0.0
    scenario_triggers_1: int = 0
    scenario_triggers_2: int = 0
    resource_storages: List[Any] = field(default_factory=list)
    damage_graphics: List[Any] = field(default_factory=list)
    wwise_train_sound_id: int = 0
    wwise_damage_sound_id: int = 0
    wwise_selection_sound_id: int = 0
    wwise_dying_sound_id: int = 0
    old_attack_reaction: int = 0
    convert_terrain: int = 0
    copy_id: int = -1
    base_id: int = -1
    dead_fish: Any = None
    bird: Any = None
    projectile: Any = None
    building: Any = None


@dataclass
class FakeCiv:
    """Fake Civ for testing."""
    name: str = "Test Civ"
    units: List[Optional[FakeUnit]] = field(default_factory=list)
    player_type: int = 0
    tech_tree_id: int = -1
    team_bonus_id: int = -1
    resources: List[float] = field(default_factory=list)
    icon_set: int = 0


@dataclass
class FakeDatFile:
    """Fake DatFile for testing (duck-typed to match genieutils.datfile.DatFile)."""
    civs: List[FakeCiv] = field(default_factory=list)
    graphics: List[Any] = field(default_factory=list)
    sounds: List[Any] = field(default_factory=list)
    techs: List[Any] = field(default_factory=list)
    version: str = "VER 7.4"


# -------------------------
# Fixtures
# -------------------------

@pytest.fixture
def fake_unit() -> FakeUnit:
    """Create a single fake unit."""
    return FakeUnit(id=0, name="Unit 0")


@pytest.fixture
def fake_dat_file() -> FakeDatFile:
    """
    Create a fake DatFile with 2 civs and 10 units each.
    """
    civs = []
    for civ_id in range(2):
        units = []
        for unit_id in range(10):
            unit = FakeUnit(
                id=unit_id,
                name=f"Unit {unit_id}",
                hit_points=100 + unit_id,
            )
            units.append(unit)
        civ = FakeCiv(name=f"Civ {civ_id}", units=units)
        civs.append(civ)
    
    return FakeDatFile(civs=civs)


@pytest.fixture
def empty_dat_file() -> FakeDatFile:
    """Create a fake DatFile with 2 civs but no units."""
    civs = [
        FakeCiv(name="Civ 0", units=[]),
        FakeCiv(name="Civ 1", units=[]),
    ]
    return FakeDatFile(civs=civs)


# -------------------------
# Real DAT File Fixtures
# -------------------------

def get_real_dat_path() -> Optional[str]:
    """Get real DAT path from environment variable."""
    return os.environ.get("AOE2_DAT_PATH")


@pytest.fixture
def real_dat_path() -> Optional[str]:
    """Fixture that returns the real DAT path if set."""
    return get_real_dat_path()


# Marker for tests that require a real DAT file
real_dat = pytest.mark.skipif(
    get_real_dat_path() is None,
    reason="Requires AOE2_DAT_PATH environment variable"
)

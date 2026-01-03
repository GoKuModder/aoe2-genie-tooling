"""
Unit Field Schema - Validation rules for genieutils Unit fields.

This defines the validation rules for all 150+ Unit fields that are NOT
in the Attribute enum but still need validation.

Each field specifies:
- reference_type: What it references (unit, graphic, sound, tech, terrain, etc.)
- validation: How to validate (exists, range, enum, list, etc.)
- allow_negative: Whether -1 means "none"
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class ReferenceType(Enum):
    """Types of references a field can have."""
    NONE = "none"  # No reference, just a value
    UNIT = "unit"
    GRAPHIC = "graphic"
    SOUND = "sound"
    TECH = "tech"
    EFFECT = "effect"
    TERRAIN = "terrain"  # TerrainType ID
    TERRAIN_TABLE = "terrain_table"  # TerrainRestriction
    TASK = "task"
    CIV = "civ"
    WWISE_HASH = "wwise"  # WWise event hash (no validation)
    
    # Lists
    UNIT_LIST = "unit_list"
    GRAPHIC_LIST = "graphic_list"
    SOUND_LIST = "sound_list"
    TASK_LIST = "task_list"
    TRAIN_LOCATION_LIST = "train_location_list"  # Complex list
    ANNEX_LIST = "annex_list"  # Tuple of annexes


class ValidationType(Enum):
    """Type of validation to perform."""
    EXISTS = "exists"  # ID must exist in collection
    RANGE = "range"  # Must be in a numeric range
    ENUM = "enum"  # Must be valid enum value
    BITMASK = "bitmask"  # Must be valid bitmask
    PASSTHROUGH = "passthrough"  # No validation (legacy/internal fields)
    CLASS = "class"  # Must be instance of a specific class


@dataclass
class FieldSchema:
    """Schema definition for a single field."""
    reference_type: ReferenceType = ReferenceType.NONE
    validation: ValidationType = ValidationType.PASSTHROUGH
    allow_negative: bool = True  # -1 often means "none"
    enum_class: Optional[str] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    class_name: Optional[str] = None
    description: str = ""


# =============================================================================
# UNIT BASE CLASS FIELDS
# =============================================================================

UNIT_SCHEMA: Dict[str, FieldSchema] = {
    # Identity fields (no validation needed)
    "id": FieldSchema(description="Unit ID"),
    "type": FieldSchema(description="Unit type class"),
    "name": FieldSchema(description="Internal name"),
    "base_id": FieldSchema(description="Template unit ID"),
    "copy_id": FieldSchema(description="Copy source ID"),
    
    # Unit class (0-100 range typically)
    "class_": FieldSchema(
        validation=ValidationType.RANGE,
        min_value=0, max_value=100,
        description="Unit class ID"
    ),
    
    # Civ must exist
    "civilization": FieldSchema(
        reference_type=ReferenceType.CIV,
        validation=ValidationType.EXISTS,
        description="Civ restriction - must exist in CivManager"
    ),
    
    # Sound references
    "selection_sound": FieldSchema(
        reference_type=ReferenceType.SOUND,
        validation=ValidationType.EXISTS,
        description="Selection sound ID"
    ),
    "dying_sound": FieldSchema(
        reference_type=ReferenceType.SOUND,
        validation=ValidationType.EXISTS,
        description="Dying sound ID"
    ),
    "train_sound": FieldSchema(
        reference_type=ReferenceType.SOUND,
        validation=ValidationType.EXISTS,
        description="Train sound ID"
    ),
    "damage_sound": FieldSchema(
        reference_type=ReferenceType.SOUND,
        validation=ValidationType.EXISTS,
        description="Damage sound ID"
    ),
    
    # Graphic lists/references
    "damage_graphics": FieldSchema(
        reference_type=ReferenceType.GRAPHIC_LIST,
        validation=ValidationType.EXISTS,
        description="Damage graphics list - each must exist"
    ),
    
    # Terrain references
    "placement_terrain": FieldSchema(
        reference_type=ReferenceType.TERRAIN,
        validation=ValidationType.EXISTS,
        description="Placement terrain ID"
    ),
    "placement_side_terrain": FieldSchema(
        reference_type=ReferenceType.TERRAIN,
        validation=ValidationType.EXISTS,
        description="Side terrain ID"
    ),
    
    # WWise hashes (no validation - just copy)
    "wwise_train_sound_id": FieldSchema(
        reference_type=ReferenceType.WWISE_HASH,
        description="WWise hash - no validation"
    ),
    "wwise_damage_sound_id": FieldSchema(
        reference_type=ReferenceType.WWISE_HASH,
        description="WWise hash - no validation"
    ),
    "wwise_selection_sound_id": FieldSchema(
        reference_type=ReferenceType.WWISE_HASH,
        description="WWise hash - no validation"
    ),
    "wwise_dying_sound_id": FieldSchema(
        reference_type=ReferenceType.WWISE_HASH,
        description="WWise hash - no validation"
    ),
    
    # Selection effect enum
    "selection_effect": FieldSchema(
        validation=ValidationType.ENUM,
        enum_class="SelectionEffect",
        description="Selection effect type"
    ),
}


# =============================================================================
# BIRD COMPONENT FIELDS
# =============================================================================

BIRD_SCHEMA: Dict[str, FieldSchema] = {
    # Task must exist
    "default_task_id": FieldSchema(
        reference_type=ReferenceType.TASK,
        validation=ValidationType.EXISTS,
        description="Default task - must exist in unit's tasks"
    ),
    
    # Unit list for drop sites
    "drop_sites": FieldSchema(
        reference_type=ReferenceType.UNIT_LIST,
        validation=ValidationType.EXISTS,
        description="Drop sites - each unit ID must exist"
    ),
    
    # Task list
    "tasks": FieldSchema(
        reference_type=ReferenceType.TASK_LIST,
        validation=ValidationType.CLASS,
        class_name="Task",
        description="Task list - must be Task instances"
    ),
    
    # Sound references
    "attack_sound": FieldSchema(
        reference_type=ReferenceType.SOUND,
        validation=ValidationType.EXISTS,
        description="Attack sound ID"
    ),
    "move_sound": FieldSchema(
        reference_type=ReferenceType.SOUND,
        validation=ValidationType.EXISTS,
        description="Move sound ID"
    ),
    
    # WWise hashes
    "wwise_attack_sound_id": FieldSchema(
        reference_type=ReferenceType.WWISE_HASH,
        description="WWise hash"
    ),
    "wwise_move_sound_id": FieldSchema(
        reference_type=ReferenceType.WWISE_HASH,
        description="WWise hash"
    ),
}


# =============================================================================
# DEAD_FISH COMPONENT FIELDS
# =============================================================================

DEAD_FISH_SCHEMA: Dict[str, FieldSchema] = {
    # Tracking unit (trailing unit)
    "tracking_unit": FieldSchema(
        reference_type=ReferenceType.UNIT,
        validation=ValidationType.EXISTS,
        description="Trailing unit ID - must exist"
    ),
    
    # Tracking mode enum
    "tracking_unit_mode": FieldSchema(
        validation=ValidationType.ENUM,
        enum_class="TrackingUnitMode",
        description="0=unused, 1=while moving and start, 2=while moving based on density"
    ),
    
    # Tracking unit density
    "tracking_unit_density": FieldSchema(
        validation=ValidationType.RANGE,
        min_value=0, max_value=100,
        description="Trailing unit spawn density"
    ),
}


# =============================================================================
# TYPE50 COMPONENT FIELDS
# =============================================================================

TYPE50_SCHEMA: Dict[str, FieldSchema] = {
    # Projectile unit
    "projectile_unit_id": FieldSchema(
        reference_type=ReferenceType.UNIT,
        validation=ValidationType.EXISTS,
        description="Projectile unit ID"
    ),
}


# =============================================================================
# CREATABLE COMPONENT FIELDS
# =============================================================================

CREATABLE_SCHEMA: Dict[str, FieldSchema] = {
    # Graphic references
    "garrison_graphic": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Garrison graphic ID"
    ),
    "hero_glow_graphic": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Hero glow graphic ID"
    ),
    "idle_attack_graphic": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Idle attack graphic ID"
    ),
    "spawning_graphic": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Spawning graphic ID"
    ),
    "upgrade_graphic": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Upgrade graphic ID"
    ),
    
    # Charge projectile unit
    "charge_projectile_unit": FieldSchema(
        reference_type=ReferenceType.UNIT,
        validation=ValidationType.EXISTS,
        description="Charge projectile unit ID"
    ),
    
    # Train locations list (Unit, train_time, button_id, hotkey_id)
    "train_locations": FieldSchema(
        reference_type=ReferenceType.TRAIN_LOCATION_LIST,
        validation=ValidationType.CLASS,
        class_name="TrainLocation",
        description="Training locations - each has unit_id, train_time, button_id, hotkey_id"
    ),
}


# =============================================================================
# BUILDING COMPONENT FIELDS
# =============================================================================

BUILDING_SCHEMA: Dict[str, FieldSchema] = {
    # Graphic references
    "construction_graphic_id": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Construction graphic ID"
    ),
    "snow_graphic_id": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Snow graphic ID"
    ),
    "destruction_graphic_id": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Destruction graphic ID"
    ),
    "destruction_rubble_graphic_id": FieldSchema(
        reference_type=ReferenceType.GRAPHIC,
        validation=ValidationType.EXISTS,
        description="Destruction rubble graphic ID"
    ),
    
    # Sound references
    "construction_sound": FieldSchema(
        reference_type=ReferenceType.SOUND,
        validation=ValidationType.EXISTS,
        description="Construction sound ID"
    ),
    "transform_sound": FieldSchema(
        reference_type=ReferenceType.SOUND,
        validation=ValidationType.EXISTS,
        description="Transform sound ID"
    ),
    
    # WWise hashes
    "wwise_construction_sound_id": FieldSchema(
        reference_type=ReferenceType.WWISE_HASH,
        description="WWise hash"
    ),
    "wwise_transform_sound_id": FieldSchema(
        reference_type=ReferenceType.WWISE_HASH,
        description="WWise hash"
    ),
    
    # Terrain
    "foundation_terrain_id": FieldSchema(
        reference_type=ReferenceType.TERRAIN,
        validation=ValidationType.EXISTS,
        description="Foundation terrain ID"
    ),
    
    # Unit references
    "transform_unit": FieldSchema(
        reference_type=ReferenceType.UNIT,
        validation=ValidationType.EXISTS,
        description="Transform unit ID"
    ),
    "pile_unit": FieldSchema(
        reference_type=ReferenceType.UNIT,
        validation=ValidationType.EXISTS,
        description="Pile unit ID"
    ),
    "stack_unit_id": FieldSchema(
        reference_type=ReferenceType.UNIT,
        validation=ValidationType.EXISTS,
        description="Stack unit ID"
    ),
    
    # Tech reference
    "tech_id": FieldSchema(
        reference_type=ReferenceType.TECH,
        validation=ValidationType.EXISTS,
        description="Tech ID - must exist"
    ),
    
    # Head unit reference
    "head_unit": FieldSchema(
        reference_type=ReferenceType.UNIT,
        validation=ValidationType.EXISTS,
        description="Head unit ID"
    ),
    
    # Annexes (tuple of up to 4 annexes, each with unit_id)
    "annexes": FieldSchema(
        reference_type=ReferenceType.ANNEX_LIST,
        validation=ValidationType.CLASS,
        class_name="Annex",
        description="Building annexes - tuple of 4, each unit_id must exist"
    ),
}


# =============================================================================
# COMBINED SCHEMA
# =============================================================================

def get_field_schema(component: str, field_name: str) -> Optional[FieldSchema]:
    """Get the schema for a field in a component."""
    schemas = {
        "unit": UNIT_SCHEMA,
        "bird": BIRD_SCHEMA,
        "dead_fish": DEAD_FISH_SCHEMA,
        "type_50": TYPE50_SCHEMA,
        "creatable": CREATABLE_SCHEMA,
        "building": BUILDING_SCHEMA,
    }
    schema_dict = schemas.get(component.lower(), {})
    return schema_dict.get(field_name)


def get_all_reference_fields() -> Dict[str, FieldSchema]:
    """Get all fields that have reference validation."""
    result = {}
    for schema in [UNIT_SCHEMA, BIRD_SCHEMA, DEAD_FISH_SCHEMA, 
                   TYPE50_SCHEMA, CREATABLE_SCHEMA, BUILDING_SCHEMA]:
        for name, field in schema.items():
            if field.reference_type != ReferenceType.NONE:
                result[name] = field
    return result

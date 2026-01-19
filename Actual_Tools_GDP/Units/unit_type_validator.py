"""
Unit Type Validator - Synchronizes unit info structures to match type.

Reverse-engineered from GenieDatParser's on_read hook logic.
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sections.civilization.unit import Unit

# Unit type constants (from GenieDatParser)
class UnitType:
    EyeCandy = 10
    Animated = 20  # Tree, Flag
    Moving = 30    # Dead/Fish/Birds
    Acting = 40    # Has tasks
    Combat = 50    # Has combat
    Projectile = 60
    Creatable = 70   # Can be trained
    Building = 80

# Type → Required Info Structures mapping
TYPE_REQUIREMENTS = {
    UnitType.EyeCandy: {
        'animation_info': False,
        'movement_info': False,
        'task_info': False,
        'combat_info': False,
        'projectile_info': False,
        'creation_info': False,
        'building_info': False,
    },
    UnitType.Animated: {
        'animation_info': True,
        'movement_info': False,
        'task_info': False,
        'combat_info': False,
        'projectile_info': False,
        'creation_info': False,
        'building_info': False,
    },
    UnitType.Moving: {
        'animation_info': True,
        'movement_info': True,
        'task_info': False,
        'combat_info': False,
        'projectile_info': False,
        'creation_info': False,
        'building_info': False,
    },
    UnitType.Acting: {
        'animation_info': True,
        'movement_info': True,
        'task_info': True,
        'combat_info': False,
        'projectile_info': False,
        'creation_info': False,
        'building_info': False,
    },
    UnitType.Combat: {
        'animation_info': True,
        'movement_info': True,
        'task_info': True,
        'combat_info': True,
        'projectile_info': False,
        'creation_info': False,
        'building_info': False,
    },
    UnitType.Projectile: {
        'animation_info': True,
        'movement_info': True,
        'task_info': True,
        'combat_info': True,
        'projectile_info': True,
        'creation_info': False,
        'building_info': False,
    },
    UnitType.Creatable: {
        'animation_info': True,
        'movement_info': True,
        'task_info': True,
        'combat_info': True,
        'projectile_info': False,
        'creation_info': True,
        'building_info': False,
    },
    UnitType.Building: {
        'animation_info': True,
        'movement_info': True,
        'task_info': True,
        'combat_info': True,
        'projectile_info': False,
        'creation_info': False,
        'building_info': True,
    },
}


def _get_template_building(civilizations) -> Unit:
    """Find first Building unit to use as template for building_info structure."""
    # Town Center (ID 109) is a reliable Building-type unit
    for civ in civilizations:
        if len(civ.units) > 109:
            unit = civ.units[109]
            if unit and unit.type_ == UnitType.Building and unit.building_info:
                return unit
    return None


def _sanitize_building_info(building_info) -> None:
    """Reset user-facing building_info fields to defaults after copying template."""
    # Graphics/sprites - reset to -1
    building_info.construction_sprite_id = -1
    building_info.snow_sprite_id = -1
    building_info.destruction_sprite_id = -1
    building_info.destruction_rubble_sprite_id = -1
    building_info.researching_sprite = -1
    building_info.research_completed_sprite = -1
    
    # Sounds - reset to -1
    if hasattr(building_info, 'damage_sound_id'):
        building_info.damage_sound_id = -1
    if hasattr(building_info, 'construction_sound_id'):
        building_info.construction_sound_id = -1
    
    # Annexes - clear all 4 slots
    if hasattr(building_info, 'building_annex') and building_info.building_annex:
        for annex in building_info.building_annex:
            annex.unit_id = -1
            annex.displacement_x = 0.0
            annex.displacement_y = 0.0
    
    # Head unit (garrison graphic) - reset
    if hasattr(building_info, 'head_unit_id'):
        building_info.head_unit_id = -1
    
    # Keep structural flags intact (construction_mode, etc.)


def _sanitize_creation_info(creation_info) -> None:
    """Reset user-facing creation_info fields to defaults after copying template."""
    # Costs - reset to empty
    if hasattr(creation_info, 'resource_costs') and creation_info.resource_costs:
        for cost in creation_info.resource_costs:
            cost.type = -1
            cost.amount = 0
            cost.flag = 0
    
    # Train location/button - reset
    if hasattr(creation_info, 'train_location_id'):
        creation_info.train_location_id = -1
    if hasattr(creation_info, 'button_id'):
        creation_info.button_id = 0
    
    # Times - keep as-is (user will likely change them anyway)
    # Train time, etc. - depends on use case


def sync_structures_to_type(unit: Unit, civilizations=None) -> None:
    """
    Synchronize unit info structures to match its type.
    
    Uses template copying for complex structures (BuildingInfo) to ensure
    proper initialization, then sanitizes user-facing fields to defaults.
    
    Args:
        unit: Unit object to synchronize (modified in-place).
        civilizations: List of civilizations (needed for finding template units).
    """
    unit_type = unit.type_
    
    if unit_type not in TYPE_REQUIREMENTS:
        # Unknown type - don't mess with it
        return
    
    requirements = TYPE_REQUIREMENTS[unit_type]
    
    # Import structure classes for initialization
    from sections.civilization.type_info import (
        AnimationInfo, MovementInfo, TaskInfo, CombatInfo,
        ProjectileInfo, CreationInfo, BuildingInfo
    )
    import copy
    
    structure_classes = {
        'animation_info': AnimationInfo,
        'movement_info': MovementInfo,
        'task_info': TaskInfo,
        'combat_info': CombatInfo,
        'projectile_info': ProjectileInfo,
        'creation_info': CreationInfo,
        'building_info': BuildingInfo,
    }
    
    for struct_name, required in requirements.items():
        current_value = getattr(unit, struct_name, None)
        
        if required and current_value is None:
            # Need this structure but it's missing
            
            # Special case: building_info is complex - copy from template
            if struct_name == 'building_info' and civilizations:
                template_building = _get_template_building(civilizations)
                if template_building and template_building.building_info:
                    # Create new building_info with same version (BFP-RS handles nested structures)
                    new_building_info = BuildingInfo(ver=unit.ver)
                    setattr(unit, struct_name, new_building_info)
                    # Sanitize user-facing fields
                    _sanitize_building_info(new_building_info)
                else:
                    # Fallback: basic initialization
                    struct_class = structure_classes[struct_name]
                    setattr(unit, struct_name, struct_class(ver=unit.ver))
            else:
                # Simple initialization for other structures
                struct_class = structure_classes[struct_name]
                setattr(unit, struct_name, struct_class(ver=unit.ver))
        
        # DON'T REMOVE STRUCTURES - causes serialization corruption
        # Just add missing ones; game seems to tolerate having both
        # elif not required and current_value is not None:
        #     setattr(unit, struct_name, None)

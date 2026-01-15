# Field Discovery Test Results

## Summary
✅ **ALL 37 FIELDS PASSING** (100% Success Rate)

Tested with Unit 4 (Archer) from `empires2_x2_p1_Shortened.dat`

## Field Categories

### Graphics Fields (19 total)
- ✅ All wrapper-based graphics working (`type_50`, `creatable`, `building`, `dead_fish`)
- ✅ Base struct fields working (`standing_graphic`, `dying_graphic`, `undead_graphic`)

### Sound Fields (8 total)
- ✅ All wrapper-based sounds working (`bird`, `building`)
- ✅ Base struct fields working (`selection_sound`, `dying_sound`, `train_sound`, `damage_sound`)

### Unit Reference Fields (10 total)
- ✅ All wrapper-based unit refs working (`type_50`, `creatable`, `dead_fish`, `building`)
- ✅ Base struct fields working (`dead_unit`, `blood_unit`)

## Key Findings

1. **Base Struct Fields Work**: Fields like `dead_unit`, `blood_unit`, `standing_graphic` etc. are accessible directly via `UnitHandle.__getattr__` which falls through to the base Unit struct when not found on wrappers.

2. **Wrapper Paths Validated**: All wrapper-based paths (e.g., `creatable.spawning_graphic_id`, `type_50.projectile_unit_id`) work correctly.

3. **Null Handling**: Most fields return `-1` or `None` when not set, which matches the `null_value` defined in `field_discovery.json`.

## Test Script
Run `Testing/test_field_discovery_attributes.py` to verify field accessibility on any unit.

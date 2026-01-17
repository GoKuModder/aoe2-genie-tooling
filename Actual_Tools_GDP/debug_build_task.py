"""
Debug: Replicate EXACT user build task and save/load to check for issues.
"""
import sys
import tempfile
from pathlib import Path

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace

SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")

print("=" * 60)
print("DEBUG: Replicate EXACT User Build Task Config")
print("=" * 60)

# Load
print("\n1. Loading DAT...", flush=True)
ws = GenieWorkspace.load(str(SOURCE_DAT))

# Use King as crusader_hero_unit stand-in
HERO_ID = 434  # King
TARGET_BUILDING_ID = 1234  # Fake ID for sword_of_sanctity

print(f"\n2. Getting hero unit {HERO_ID}...", flush=True)
crusader_hero_unit = ws.unit_manager.get(HERO_ID)
print(f"   Hero: {crusader_hero_unit.name}")
print(f"   Initial tasks: {len(crusader_hero_unit.tasks)}")

# Replicate EXACT user code
print("\n3. Adding BUILD task with EXACT user config...", flush=True)
build_sword_of_sanctity = crusader_hero_unit.add_task.build()

build_sword_of_sanctity.unit_id = TARGET_BUILDING_ID  # sword_of_sanctity_unit.id
build_sword_of_sanctity.work_value_1 = 1
build_sword_of_sanctity.work_range = 5
build_sword_of_sanctity.target_diplomacy = 4
build_sword_of_sanctity.building_pick = True
build_sword_of_sanctity.search_wait_time = 3
build_sword_of_sanctity.auto_search_targets = True

print(f"   Tasks after: {len(crusader_hero_unit.tasks)}")

# Dump ALL task properties for inspection
print("\n4. Dumping ALL properties of the new task...", flush=True)
task_idx = len(crusader_hero_unit.tasks) - 1

# Get raw task from first unit
units = crusader_hero_unit._get_units()
raw_task = units[0].task_info.tasks[task_idx]

# Print all fields
print(f"   task_type: {raw_task.task_type}")
print(f"   id: {raw_task.id}")
print(f"   is_default: {raw_task.is_default}")
print(f"   action_type: {raw_task.action_type}")
print(f"   unit_class_id: {raw_task.unit_class_id}")
print(f"   unit_type: {raw_task.unit_type}")
print(f"   terrain_type: {raw_task.terrain_type}")
print(f"   resource_in: {raw_task.resource_in}")
print(f"   productivity_resource: {raw_task.productivity_resource}")
print(f"   resource_out: {raw_task.resource_out}")
print(f"   unused_resource: {raw_task.unused_resource}")
print(f"   work_value1: {raw_task.work_value1}")
print(f"   work_value2: {raw_task.work_value2}")
print(f"   work_range: {raw_task.work_range}")
print(f"   auto_search_targets: {raw_task.auto_search_targets}")
print(f"   search_wait_time: {raw_task.search_wait_time}")
print(f"   enable_targeting: {raw_task.enable_targeting}")
print(f"   combat_level: {raw_task.combat_level}")
print(f"   gather_type: {raw_task.gather_type}")
print(f"   work_mode: {raw_task.work_mode}")
print(f"   target_diplomacy: {raw_task.target_diplomacy}")
print(f"   target_resource_flag: {raw_task.target_resource_flag}")
print(f"   build_task_flag: {raw_task.build_task_flag}")
print(f"   move_sprite_id: {raw_task.move_sprite_id}")
print(f"   proceed_sprite_id: {raw_task.proceed_sprite_id}")
print(f"   work_sprite_id: {raw_task.work_sprite_id}")
print(f"   carry_sprite_id: {raw_task.carry_sprite_id}")
print(f"   resource_gather_sound_id: {raw_task.resource_gather_sound_id}")
print(f"   resource_deposit_sound_id: {raw_task.resource_deposit_sound_id}")

# Save
print("\n5. Saving DAT...", flush=True)
temp_dir = Path(tempfile.gettempdir())
output_path = temp_dir / "debug_build_task.dat"
ws.save(str(output_path))
print(f"   Saved to: {output_path}")

# Reload
print("\n6. Reloading...", flush=True)
ws2 = GenieWorkspace.load(str(output_path))
hero2 = ws2.unit_manager.get(HERO_ID)
print(f"   Tasks after reload: {len(hero2.tasks)}")

# Check task survived
raw_task2 = ws2.dat.civilizations[0].units[HERO_ID].task_info.tasks[task_idx]
print(f"\n7. Verifying reloaded task...")
print(f"   action_type: {raw_task2.action_type} (expected: 101)")
print(f"   unit_type: {raw_task2.unit_type} (expected: {TARGET_BUILDING_ID})")
print(f"   work_value1: {raw_task2.work_value1} (expected: 1.0)")
print(f"   build_task_flag: {raw_task2.build_task_flag} (expected: True)")

# Look for potential issues
print("\n8. Potential issues check...")

# Check if unit_class_id is -1 (might be needed for BUILD tasks)
if raw_task2.unit_class_id == -1:
    print("   WARNING: unit_class_id is -1. BUILD tasks might need a valid class!")

# Check if target_diplomacy=4 is valid
print(f"   target_diplomacy={raw_task2.target_diplomacy} (4=Self+Ally+Gaia)")

# Check task_type
if raw_task2.task_type == 1:
    print("   INFO: task_type=1 (default)")
elif raw_task2.task_type == 0:
    print("   WARNING: task_type=0 (might need to be 1?)")

print("\nOutput file kept at:", output_path)
print("You can test this DAT in-game to see if it crashes.")

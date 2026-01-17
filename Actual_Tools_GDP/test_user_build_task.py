"""
Test: Replicate user's exact build task code pattern.
Game crashes on loading screen - need to identify which property causes it.
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
print("TEST: Replicate User's Build Task Pattern")
print("=" * 60)

# Step 1: Load DAT
print("\n1. Loading source DAT...", flush=True)
ws = GenieWorkspace.load(str(SOURCE_DAT))

# Use a hero unit (like King) and a building target
HERO_UNIT_ID = 434  # King
TARGET_BUILDING_ID = 12  # Barracks (example target)

print(f"\n2. Getting hero unit {HERO_UNIT_ID}...", flush=True)
crusader_hero_unit = ws.unit_manager.get(HERO_UNIT_ID)
print(f"   Hero: {crusader_hero_unit.name}")
print(f"   Tasks before: {len(crusader_hero_unit.tasks)}")

# Replicate user's EXACT code pattern
print(f"\n3. Adding BUILD task with user's exact properties...", flush=True)

build_sword_of_sanctity = crusader_hero_unit.add_task.build()
print(f"   Task created. Setting properties...")

# These are the exact properties from user's code
build_sword_of_sanctity.unit_id = TARGET_BUILDING_ID
print(f"   - unit_id = {TARGET_BUILDING_ID}")

build_sword_of_sanctity.work_value_1 = 1
print(f"   - work_value_1 = 1")

build_sword_of_sanctity.work_range = 5
print(f"   - work_range = 5")

build_sword_of_sanctity.target_diplomacy = 4
print(f"   - target_diplomacy = 4")

build_sword_of_sanctity.building_pick = True
print(f"   - building_pick = True")

build_sword_of_sanctity.search_wait_time = 3
print(f"   - search_wait_time = 3")

build_sword_of_sanctity.auto_search_targets = True
print(f"   - auto_search_targets = True")

print(f"\n   Tasks after: {len(crusader_hero_unit.tasks)}")

# Step 4: Dump task properties for inspection
print(f"\n4. Inspecting created task properties...", flush=True)
task_count = len(crusader_hero_unit.tasks)
last_task = crusader_hero_unit.tasks[task_count - 1]

# Check what values are actually stored
print(f"   task_type: {last_task.task_type}")
print(f"   action_type: {last_task.action_type}")
print(f"   unit_id (unit_type): {last_task.unit_id}")
print(f"   work_value_1: {last_task.work_value_1}")
print(f"   work_range: {last_task.work_range}")
print(f"   target_diplomacy: {last_task.target_diplomacy}")
print(f"   building_pick: {last_task.building_pick}")
print(f"   search_wait_time: {last_task.search_wait_time}")
print(f"   auto_search_targets: {last_task.auto_search_targets}")

# Step 5: Save to temp file
print(f"\n5. Saving DAT...", flush=True)
temp_dir = Path(tempfile.gettempdir())
output_path = temp_dir / "test_user_build_task.dat"
ws.save(str(output_path))
print(f"   Saved to: {output_path}")
print(f"   File size: {output_path.stat().st_size:,} bytes")

# Step 6: Reload and verify
print(f"\n6. Reloading saved DAT...", flush=True)
try:
    ws2 = GenieWorkspace.load(str(output_path))
    print(f"   Reloaded successfully!")
    
    hero2 = ws2.unit_manager.get(HERO_UNIT_ID)
    print(f"   Hero tasks after reload: {len(hero2.tasks)}")
    
    # Verify task properties survived
    last_task2 = hero2.tasks[len(hero2.tasks) - 1]
    print(f"\n   Verifying task properties after reload:")
    print(f"   task_type: {last_task2.task_type}")
    print(f"   action_type: {last_task2.action_type}")
    print(f"   unit_id: {last_task2.unit_id}")
    print(f"   work_value_1: {last_task2.work_value_1}")
    print(f"   work_range: {last_task2.work_range}")
    print(f"   target_diplomacy: {last_task2.target_diplomacy}")
    print(f"   building_pick: {last_task2.building_pick}")
    print(f"   search_wait_time: {last_task2.search_wait_time}")
    print(f"   auto_search_targets: {last_task2.auto_search_targets}")
    
    print("\n" + "=" * 60)
    print("DAT SAVED AND RELOADED OK - properties saved, check game!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n   ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# Keep file for testing in game
print(f"\nOutput DAT kept at: {output_path}")
print("You can copy this to your mod folder and test in-game.")

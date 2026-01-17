"""
Test: Add a build task to a unit, save DAT, reload, and verify no corruption.
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
print("TEST: Add Build Task -> Save -> Reload")
print("=" * 60)

# Step 1: Load DAT
print("\n1. Loading source DAT...", flush=True)
ws = GenieWorkspace.load(str(SOURCE_DAT))
print(f"   Loaded. Unit count: {ws.unit_manager.count()}")

# Step 2: Get a unit (e.g., Villager ID=83 or Archer ID=4)
UNIT_ID = 83  # Villager - should have tasks already
print(f"\n2. Getting unit {UNIT_ID}...", flush=True)
handle = ws.unit_manager.get(UNIT_ID)
print(f"   Unit: {handle.name}")
print(f"   Tasks before: {len(handle.tasks)}")

# Step 3: Add a BUILD task
print("\n3. Adding BUILD task...", flush=True)
# Build task: task_type=1, action_type=101 (build), class_id=3 (building class)
new_task = handle.add_task.build(class_id=3)
print(f"   Added task. Tasks after: {len(handle.tasks)}")

# Step 4: Save to temp file
print("\n4. Saving DAT to temp file...", flush=True)
temp_dir = Path(tempfile.gettempdir())
output_path = temp_dir / "test_build_task.dat"
ws.save(str(output_path))
print(f"   Saved to: {output_path}")
print(f"   File size: {output_path.stat().st_size:,} bytes")

# Step 5: Reload the saved DAT
print("\n5. Reloading saved DAT...", flush=True)
try:
    ws2 = GenieWorkspace.load(str(output_path))
    print(f"   Reloaded successfully!")
    print(f"   Unit count: {ws2.unit_manager.count()}")
    
    # Verify the unit and task
    handle2 = ws2.unit_manager.get(UNIT_ID)
    print(f"   Unit {UNIT_ID} name: {handle2.name}")
    print(f"   Tasks: {len(handle2.tasks)}")
    
    # Check last task (use positive index since manager doesn't support negative)
    task_count = len(handle2.tasks)
    if task_count > 0:
        last_task = handle2.tasks[task_count - 1]
        print(f"   Last task type: {last_task.task_type}")
        print(f"   Last task action_type: {last_task.action_type}")
    
    print("\n" + "=" * 60)
    print("SUCCESS: No corruption detected!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n   ERROR during reload: {type(e).__name__}: {e}")
    print("\n" + "=" * 60)
    print("FAILURE: DAT CORRUPTION DETECTED!")
    print("=" * 60)
    import traceback
    traceback.print_exc()

# Cleanup
try:
    output_path.unlink()
    print(f"\nCleaned up temp file.")
except:
    pass

"""
Reproduction script for "Task added only to Gaia" issue.
"""
import sys
from pathlib import Path

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace
from Actual_Tools_GDP.Units.unit_handle import UnitHandle

print("1: Load DAT", flush=True)
SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")
ws = GenieWorkspace.load(str(SOURCE_DAT))

# Pick a standard unit - Archer (ID 4)
UNIT_ID = 4
print(f"2: Get Unit {UNIT_ID} (all civs)", flush=True)

# Create handle for all civs
handle = UnitHandle(ws, UNIT_ID, civ_ids=None) # None = all

units = handle._get_units()
print(f"  Got {len(units)} unit instances (one per civ)", flush=True)

# Check Civ 0 (Gaia) and Civ 1 (Britons usually)
gaia_unit = units[0]
civ1_unit = units[1]

print(f"  Civ 0 (Gaia) Has TaskInfo: {hasattr(gaia_unit, 'task_info') and bool(gaia_unit.task_info)}")
if gaia_unit.task_info:
    print(f"    Tasks: {len(gaia_unit.task_info.tasks)}")

print(f"  Civ 1        Has TaskInfo: {hasattr(civ1_unit, 'task_info') and bool(civ1_unit.task_info)}")
if civ1_unit.task_info:
    print(f"    Tasks: {len(civ1_unit.task_info.tasks)}")

# Detect if task lists are SHARED (same pointer)
if gaia_unit.task_info and civ1_unit.task_info:
    is_shared = (gaia_unit.task_info == civ1_unit.task_info) # or tasks list object
    print(f"  TaskInfo shared object? {is_shared}")
    # Check tasks list specifically
    # BfpList usually returns new wrapper, so compare contents or just ID if possible?
    # BFP-RS equality might check content.
    pass

print("\n3: Add Task using Handle", flush=True)
handle.create_task(task_type=1, work_value_1=999)

print("\n4: Check counts again", flush=True)
if gaia_unit.task_info:
    print(f"  Civ 0 Tasks: {len(gaia_unit.task_info.tasks)} (Expected +1)")
else:
    print("  Civ 0: No task info")

if civ1_unit.task_info:
    print(f"  Civ 1 Tasks: {len(civ1_unit.task_info.tasks)} (Expected +1)")
else:
    print("  Civ 1: No task info")

# Check last task
if civ1_unit.task_info and len(civ1_unit.task_info.tasks) > 0:
    last = civ1_unit.task_info.tasks[-1]
    print(f"  Civ 1 Last Task Val: {last.work_value1}")
else:
    print("  Civ 1: Task not added!")

print("\nDone")

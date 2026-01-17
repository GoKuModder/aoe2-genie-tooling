"""
Simulate add_unit and check tasks.
"""
import sys
from pathlib import Path

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace
from Actual_Tools_GDP.Units.unit_handle import UnitHandle

SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")
ws = GenieWorkspace.load(str(SOURCE_DAT))

print("1: Add new unit", flush=True)
# Assuming typical usage
# Create new unit using manager.create
# Base ID 4 (Archer) - has tasks
handle = ws.unit_manager.create(name="TestUnit1", base_unit_id=4)
new_unit_id = handle.id
print(f"  New ID: {new_unit_id}")

# Get handle again (just to be sure)
h = UnitHandle(ws, new_unit_id, civ_ids=None)
units = h._get_units()
print(f"  Got {len(units)} units")

gaia = units[0]
civ1 = units[1]

print(f"  Gaia TaskInfo: {hasattr(gaia, 'task_info') and bool(gaia.task_info)}")
print(f"  Civ1 TaskInfo: {hasattr(civ1, 'task_info') and bool(civ1.task_info)}")

print("2: Add Task", flush=True)
h.create_task(1)

print(f"  Gaia Tasks: {len(gaia.task_info.tasks) if gaia.task_info else 'None'}")
print(f"  Civ1 Tasks: {len(civ1.task_info.tasks) if civ1.task_info else 'None'}")

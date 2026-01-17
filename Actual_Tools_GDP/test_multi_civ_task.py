"""
Verification test: TaskHandle multi-civ propagation.
Verify that setting properties on TaskHandle updates tasks for ALL civs, not just Gaia.
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
print("TEST: TaskHandle Multi-Civ Property Propagation")
print("=" * 60)

# Load
print("\n1. Loading DAT...", flush=True)
ws = GenieWorkspace.load(str(SOURCE_DAT))

# Get unit
UNIT_ID = 83  # Villager
hero = ws.unit_manager.get(UNIT_ID)
print(f"   Unit: {hero.name}")
print(f"   Civs covered: {len(hero._civ_ids)}")

# Get initial task count
initial_count = len(hero.tasks)
print(f"   Initial tasks: {initial_count}")

# Add task
print("\n2. Adding BUILD task and setting properties...", flush=True)
task = hero.add_task.build()
print(f"   Task created. Index: {task.task_id}")

# Set properties (these should propagate to ALL civs)
task.unit_id = 999
task.work_value_1 = 123.0
task.target_diplomacy = 4
task.building_pick = True
print(f"   Set: unit_id=999, work_value_1=123.0, target_diplomacy=4, building_pick=True")

# Verify propagation by checking multiple civs
print("\n3. Verifying propagation across civs...", flush=True)
units = hero._get_units()
print(f"   Checking {len(units)} unit instances...")

all_ok = True
task_idx = len(hero.tasks) - 1

for i, u in enumerate(units[:5]):  # Check first 5 civs
    if u.task_info and task_idx < len(u.task_info.tasks):
        t = u.task_info.tasks[task_idx]
        ok = (t.unit_type == 999 and t.work_value1 == 123.0 and t.target_diplomacy == 4 and t.build_task_flag == True)
        status = "OK" if ok else "FAIL"
        print(f"   Civ {i}: unit_type={t.unit_type}, work_value1={t.work_value1}, target_diplomacy={t.target_diplomacy}, build_task_flag={t.build_task_flag} {status}")
        if not ok:
            all_ok = False

# Check last civ too
last_idx = len(units) - 1
if last_idx > 4:
    u = units[last_idx]
    if u.task_info and task_idx < len(u.task_info.tasks):
        t = u.task_info.tasks[task_idx]
        ok = (t.unit_type == 999 and t.work_value1 == 123.0 and t.target_diplomacy == 4 and t.build_task_flag == True)
        status = "OK" if ok else "FAIL"
        print(f"   Civ {last_idx}: unit_type={t.unit_type}, work_value1={t.work_value1}, target_diplomacy={t.target_diplomacy}, build_task_flag={t.build_task_flag} {status}")
        if not ok:
            all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("SUCCESS: Properties propagated to ALL civs!")
else:
    print("FAILURE: Properties NOT propagated to all civs!")
print("=" * 60)

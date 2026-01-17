"""
DEBUG: Find and compare working SPEED_CHARGE tasks (action_type=137)
"""
import sys
from pathlib import Path

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace

SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")
ws = GenieWorkspace.load(str(SOURCE_DAT))

# Action type 137 = Speed Charge
print("Searching for SPEED_CHARGE tasks (action_type=137)...")
print("=" * 60)

count = 0
for u in ws.dat.civilizations[0].units[:2000]:
    if u and hasattr(u, 'task_info') and u.task_info:
        for i, task in enumerate(u.task_info.tasks):
            if task.action_type == 137:
                count += 1
                print(f"\nUnit {u.id} ({u.name}) Task {i}: action_type=137 (SPEED_CHARGE)")
                print(f"   task_type: {task.task_type}")
                print(f"   id: {task.id}")
                print(f"   unit_class_id: {task.unit_class_id}")
                print(f"   unit_type: {task.unit_type}")
                print(f"   work_value1: {task.work_value1}")
                print(f"   work_value2: {task.work_value2}")
                print(f"   work_range: {task.work_range}")
                print(f"   work_mode: {task.work_mode}")
                print(f"   target_diplomacy: {task.target_diplomacy}")
                print(f"   auto_search_targets: {task.auto_search_targets}")
                if count >= 5:
                    break
    if count >= 5:
        break

if count == 0:
    print("No SPEED_CHARGE tasks found!")
else:
    print(f"\nFound {count} SPEED_CHARGE tasks.")
    
# Now create a new one and compare
print("\n" + "=" * 60)
print("Creating new SPEED_CHARGE task with user's params...")
print("=" * 60)

unit = ws.unit_manager.get(4)  # Archer
task = unit.add_task.speed_charge(
    work_value_1=2,
    work_value_2=6,
    work_range=4,
    work_flag_2=2001
)

raw = unit._get_units()[0].task_info.tasks[len(unit.tasks) - 1]
print(f"\nCreated task properties:")
print(f"   task_type: {raw.task_type}")
print(f"   action_type: {raw.action_type}")
print(f"   work_value1: {raw.work_value1}")
print(f"   work_value2: {raw.work_value2}")
print(f"   work_range: {raw.work_range}")
print(f"   work_mode: {raw.work_mode}")

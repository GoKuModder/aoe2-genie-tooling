"""
Find units with BUILD tasks (action_type=101).
"""
import sys
from pathlib import Path

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace

SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")
ws = GenieWorkspace.load(str(SOURCE_DAT))

print("Searching for units with BUILD tasks (action_type=101)...")
print("=" * 60)

count = 0
for u in ws.dat.civilizations[0].units[:500]:
    if u and hasattr(u, 'task_info') and u.task_info:
        for i, task in enumerate(u.task_info.tasks):
            if task.action_type == 101:
                count += 1
                print(f"Unit {u.id} ({u.name}) Task {i}: action_type=101")
                print(f"   task_type={task.task_type}, unit_class_id={task.unit_class_id}, unit_type={task.unit_type}")
                print(f"   target_diplomacy={task.target_diplomacy}, build_task_flag={task.build_task_flag}")
                if count >= 10:
                    break
    if count >= 10:
        break

if count == 0:
    print("No BUILD tasks found! Searching for any task with build_task_flag=True...")
    for u in ws.dat.civilizations[0].units[:500]:
        if u and hasattr(u, 'task_info') and u.task_info:
            for i, task in enumerate(u.task_info.tasks):
                if task.build_task_flag:
                    count += 1
                    print(f"Unit {u.id} ({u.name}) Task {i}: build_task_flag=True")
                    print(f"   action_type={task.action_type}, task_type={task.task_type}")
                    print(f"   unit_class_id={task.unit_class_id}, unit_type={task.unit_type}")
                    if count >= 10:
                        break
        if count >= 10:
            break

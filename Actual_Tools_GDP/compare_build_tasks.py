"""
Compare: User's build task vs working Villager build task.
"""
import sys
from pathlib import Path

lib_path = Path(r"c:\AoE2DE Modding\Code\1 GenieUtils Python Tools  Library")
sys.path.insert(0, str(lib_path))
sys.path.insert(0, str(lib_path / "GenieDatParser" / "src"))

from Actual_Tools_GDP.Base.workspace import GenieWorkspace

SOURCE_DAT = Path(r"C:\Program Files (x86)\Steam\steamapps\common\AoE2DE\resources\_common\dat\empires2_x2_p1.dat")

ws = GenieWorkspace.load(str(SOURCE_DAT))

# Villager (ID 83) has BUILD tasks
villager = ws.dat.civilizations[0].units[83]

print("=" * 60)
print("COMPARING: Villager's BUILD tasks (action_type=101)")
print("=" * 60)

for i, task in enumerate(villager.task_info.tasks):
    if task.action_type == 101:  # Build
        print(f"\n--- Task {i} (BUILD) ---")
        print(f"   task_type: {task.task_type}")
        print(f"   id: {task.id}")
        print(f"   is_default: {task.is_default}")
        print(f"   action_type: {task.action_type}")
        print(f"   unit_class_id: {task.unit_class_id}")
        print(f"   unit_type: {task.unit_type}")
        print(f"   terrain_type: {task.terrain_type}")
        print(f"   resource_in: {task.resource_in}")
        print(f"   resource_out: {task.resource_out}")
        print(f"   work_value1: {task.work_value1}")
        print(f"   work_value2: {task.work_value2}")
        print(f"   work_range: {task.work_range}")
        print(f"   auto_search_targets: {task.auto_search_targets}")
        print(f"   search_wait_time: {task.search_wait_time}")
        print(f"   enable_targeting: {task.enable_targeting}")
        print(f"   target_diplomacy: {task.target_diplomacy}")
        print(f"   build_task_flag: {task.build_task_flag}")
        print(f"   move_sprite_id: {task.move_sprite_id}")
        print(f"   work_sprite_id: {task.work_sprite_id}")

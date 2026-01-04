from Actual_Tools_GDP.Base.base_manager import GenieWorkspace
import sys

try:
    ws = GenieWorkspace.load("Actual_Tools_GDP/empires2_x2_p1.dat")
    # Unit 4 is Archer (tasks: None). Unit 83 (Villager) should have tasks.
    # Finding a unit with task_info
    unit = None
    for civ in ws.dat.civs:
        for u in civ.units:
            if u and hasattr(u, "task_info") and u.task_info:
                unit = u
                break
        if unit: break

    if not unit:
        print("No unit with task_info found.")
        sys.exit(1)
        
    print(f"Unit: {unit.name} (ID: {unit.id})")
    ti = unit.task_info
    print(f"task_info type: {type(ti)}")
    print(f"task_info dir: {dir(ti)}")
    
    # Check for fields expected by BirdWrapper
    print(f"Has move_sound: {hasattr(ti, 'move_sound')}")
    print(f"Has default_task_id: {hasattr(ti, 'default_task_id')}")
    print(f"Has search_radius: {hasattr(ti, 'search_radius')}")
    print(f"Has drop_sites: {hasattr(ti, 'drop_sites')}")

except Exception as e:
    print(f"Inspection failed: {e}")
    sys.exit(1)

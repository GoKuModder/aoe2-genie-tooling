import copy
from Actual_Tools_GDP.Base.base_manager import GenieWorkspace

try:
    ws = GenieWorkspace.load("Actual_Tools_GDP/empires2_x2_p1.dat")
    # Get first valid unit
    civ = ws.dat.civs[0]
    unit = next(u for u in civ.units if u is not None)
    
    print(f"Unit type: {type(unit)}")
    print(f"Dir: {dir(unit)}")
    
    print("Attempting .clone()...")
    if hasattr(unit, 'clone'):
        cloned = unit.clone()
        print("Clone successful!")
    else:
        print("No .clone() method found.")

    print("Attempting copy.deepcopy()...")
    try:
        copied = copy.deepcopy(unit)
        print("Deepcopy successful!")
    except Exception as e:
        print(f"Deepcopy failed: {e}")

except Exception as e:
    print(f"Script failed: {e}")

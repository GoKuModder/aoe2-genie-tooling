from Actual_Tools_GDP.Base.base_manager import GenieWorkspace
import sys
import json

try:
    ws = GenieWorkspace.load("Actual_Tools_GDP/empires2_x2_p1.dat")
    civ = ws.dat.civs[0]
    unit = next(u for u in civ.units if u is not None)
    
    print("Testing to_json -> from_json cloning...")
    
    # Serialize
    data_str = unit.to_json()
    print(f"Serialized to JSON string (len {len(data_str)})")
    
    # Deserialize
    UnitClass = type(unit)
    cloned = UnitClass.from_json(data_str)
    
    print("Cloned successfully!")
    print(f"Original ID: {unit.id}, Name: {unit.name}")
    print(f"Cloned ID: {cloned.id}, Name: {cloned.name}")
    
    if unit.id == cloned.id and unit.name == cloned.name:
        print("Clone verification PASSED")
    else:
        print("Clone verification FAILED")

except Exception as e:
    print(f"Clone test failed: {e}")
    sys.exit(1)

from Actual_Tools_GDP.Base.base_manager import GenieWorkspace
import sys

try:
    ws = GenieWorkspace.load("Actual_Tools_GDP/empires2_x2_p1.dat")
    civ = ws.dat.civs[0]
    unit = next(u for u in civ.units if u is not None)
    
    print("Testing to_bytes -> from_bytes cloning...")
    
    # Serialize
    data = unit.to_bytes()
    print(f"Serialized to {len(data)} bytes")
    
    # Deserialize (using class method from type(unit))
    UnitClass = type(unit)
    cloned = UnitClass.from_bytes(data)
    
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

from Actual_Tools_GDP.Base.base_manager import GenieWorkspace
import sys

try:
    ws = GenieWorkspace.load("Actual_Tools_GDP/empires2_x2_p1.dat")
    # Unit 4 is Archer, usually creatable
    unit = ws.dat.civs[0].units[4]
    
    print(f"Unit: {unit.name}")
    print(f"Has creation_info: {hasattr(unit, 'creation_info')}")
    
    if hasattr(unit, 'creation_info'):
        ci = unit.creation_info
        print(f"creation_info type: {type(ci)}")
        print(f"creation_info dir: {dir(ci)}")
        
        # specific check for fields used in wrapper
        print(f"Has train_locations: {hasattr(ci, 'train_locations')}")
        print(f"Has resource_costs: {hasattr(ci, 'resource_costs')}")

except Exception as e:
    print(f"Inspection failed: {e}")
    sys.exit(1)

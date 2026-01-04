from Actual_Tools_GDP.Base.base_manager import GenieWorkspace
import sys

try:
    ws = GenieWorkspace.load("Actual_Tools_GDP/empires2_x2_p1.dat")
    template = ws.dat.civs[0].units[4] # Archer
    UnitClass = type(template)
    
    print("\n--- Testing Unit.from_base(template) ---")
    try:
        cloned = UnitClass.from_base(template)
        print("Cloned successfully using from_base!")
        print(f"Original ID: {template.id}, Name: {template.name}")
        print(f"Cloned ID: {cloned.id}, Name: {cloned.name}")
        print(f"Cloned Version: {cloned.ver}")
        
        # Modify clone
        cloned.name = "Cloned Archer"
        print(f"Modified Name: {cloned.name}")
        
    except Exception as e:
        print(f"from_base failed: {e}")

except Exception as e:
    print(f"Test failed: {e}")
    sys.exit(1)

from Actual_Tools_GDP.Base.base_manager import GenieWorkspace
import sys

try:
    ws = GenieWorkspace.load("Actual_Tools_GDP/empires2_x2_p1.dat")
    template = ws.dat.civs[0].units[4]
    
    print(f"Template Name: {template.name}")
    print(f"Template Version: {template.ver} (Get: {template._get_version()})")
    
    print("\n--- Constructing new Unit ---")
    new_unit = type(template)()
    print(f"New Unit type: {type(new_unit)}")
    print(f"New Unit Version (Initial): {getattr(new_unit, 'ver', 'N/A')} (Get: {getattr(new_unit, '_get_version', lambda: 'N/A')()})")
    
    print("\n--- Attempting to set version ---")
    try:
        new_unit.ver = template.ver
        print("Set .ver attribute successfully.")
    except Exception as e:
        print(f"Failed to set .ver: {e}")
        
    print(f"New Unit Version (After Set): {getattr(new_unit, 'ver', 'N/A')} (Get: {getattr(new_unit, '_get_version', lambda: 'N/A')()})")
    
    print("\n--- Attempting to set Name ---")
    try:
        new_unit.name = "Test Name"
        print("Success: Set name")
    except Exception as e:
        print(f"Failed: {e}")

except Exception as e:
    print(f"Test failed: {e}")
    sys.exit(1)

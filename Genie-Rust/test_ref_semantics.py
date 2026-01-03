import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import genie_rust

DAT_FILE = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\empires2_x2_p1_RUST_TEST.dat"

def test_reference_semantics():
    df = genie_rust.DatFile.from_file(DAT_FILE)
    
    # 1. Test List Element Modification persistence
    print(f"Original Civ[0] Name: {df.civs[0].name}")
    
    # Get the list, modify an element
    civs = df.civs
    civs[0].name = "MODIFIED_NAME"
    
    # Check if df sees the change (without re-assignment)
    print(f"Direct Civ[0] access after modification: {df.civs[0].name}")
    
    if df.civs[0].name == "MODIFIED_NAME":
        print("RESULT: Reference semantics (Like Python)")
    else:
        print("RESULT: Copy semantics (Different from Python)")
        
        # Test if re-assignment works
        df.civs = civs
        print(f"Civ[0] access after re-assignment: {df.civs[0].name}")

    # 2. Test Deep Object persistence
    # Re-fetch to be clean
    df = genie_rust.DatFile.from_file(DAT_FILE)
    civ = df.civs[0]
    unit = civ.units[0] # Assumes first unit exists and is not None
    if unit:
        print(f"Original Unit HP: {unit.hit_points}")
        unit.hit_points = 555
        
        # Does df see it?
        print(f"Unit HP from df root: {df.civs[0].units[0].hit_points}")
        
        if df.civs[0].units[0].hit_points == 555:
             print("RESULT: Deep Object Reference semantics")
        else:
             print("RESULT: Deep Object Copy semantics")

if __name__ == "__main__":
    test_reference_semantics()

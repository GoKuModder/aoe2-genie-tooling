import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))
import genie_rust

DAT_FILE = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\empires2_x2_p1_RUST_TEST.dat"

def test_mutability():
    df = genie_rust.DatFile.from_file(DAT_FILE)
    
    print(f"Original Civ Name: {df.civs[0].name}")
    df.civs[0].name = "New Name"
    print(f"Modified Civ Name: {df.civs[0].name}")
    
    # Get a unit
    unit = next((u for u in df.civs[0].units if u is not None), None)
    if unit:
        print(f"Original Unit HP: {unit.hit_points}")
        unit.hit_points = 999
        print(f"Modified Unit HP: {unit.hit_points}")
    
    # Check if list modification works (requires setter on DatFile)
    print(f"Original Sound Count: {len(df.sounds)}")
    # Note: Modifying the list itself might not work if it returns a copy
    # But replacing it should
    new_sounds = []
    df.sounds = new_sounds
    print(f"Modified Sound Count: {len(df.sounds)}")

if __name__ == "__main__":
    test_mutability()

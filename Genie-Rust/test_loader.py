import genie_rust
import sys
import os

DAT_FILE = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\empires2_x2_p1_RUST_TEST.dat"

def test_loading():
    print(f"Loading {DAT_FILE}...")
    if not os.path.exists(DAT_FILE):
        print("Error: Test file not found at", DAT_FILE)
        return

    try:
        df = genie_rust.DatFile.from_file(DAT_FILE)
        print("Successfully loaded DatFile!")
        print(f"Version: {df.version}")
        print(f"Civ Count: {len(df.civs)}")
        print(f"Sound Count: {len(df.sounds)}")
        print(f"Graphic Count: {len(df.graphics)}")
        print(f"Effect Count: {len(df.effects)}")
        
        if len(df.civs) > 0:
            print(f"First Civ Name: {df.civs[0].name}")
            print(f"First Civ Unit Count: {len(df.civs[0].units)}")
            # Find first non-None unit
            first_unit = next((u for u in df.civs[0].units if u is not None), None)
            if first_unit:
                print(f"First Unit Name: {first_unit.name}")
            else:
                print("First Civ has no valid units.")

    except Exception as e:
        print(f"Error loading DatFile: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_loading()

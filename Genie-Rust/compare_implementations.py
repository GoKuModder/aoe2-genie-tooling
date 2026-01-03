import sys
import os

# Add project root to path for genieutils import
sys.path.append(os.path.dirname(os.getcwd()))

try:
    from genieutils.datfile import DatFile as PyDatFile
    import genie_rust
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

DAT_FILE = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\empires2_x2_p1_RUST_TEST.dat"

def compare():
    print("Loading with genieutils-py...")
    py_df = PyDatFile.parse(DAT_FILE)
    
    print("Loading with genie-rust...")
    rust_df = genie_rust.DatFile.from_file(DAT_FILE)
    
    print("\n--- Comparison ---")
    
    # Version
    print(f"Version: Py='{py_df.version}', Rust='{rust_df.version}' match={str(py_df.version) == rust_df.version}")
    
    # Counts
    sections = [
        ("Civs", "civs"),
        ("Sounds", "sounds"),
        ("Graphics", "graphics"),
        ("Effects", "effects"),
    ]
    
    for label, attr in sections:
        py_list = getattr(py_df, attr)
        rust_list = getattr(rust_df, attr)
        match = len(py_list) == len(rust_list)
        print(f"{label} count: Py={len(py_list)}, Rust={len(rust_list)} match={match}")
        
    # Deep comparison: First Civ Unit
    if len(py_df.civs) > 0 and len(rust_df.civs) > 0:
        py_civ = py_df.civs[0]
        rust_civ = rust_df.civs[0]
        
        print(f"Civ Name: Py='{py_civ.name}', Rust='{rust_civ.name}' match={py_civ.name == rust_civ.name}")
        
        # Helper to find first unit
        py_unit = next((u for u in py_civ.units if u is not None), None)
        rust_unit = next((u for u in rust_civ.units if u is not None), None)
        
        if py_unit and rust_unit:
            print(f"First Unit Name: Py='{py_unit.name}', Rust='{rust_unit.name}' match={py_unit.name == rust_unit.name}")
            print(f"First Unit HP: Py={py_unit.hit_points}, Rust={rust_unit.hit_points} match={py_unit.hit_points == rust_unit.hit_points}")
            print(f"First Unit ID: Py={py_unit.id}, Rust={rust_unit.id} match={py_unit.id == rust_unit.id}")
            # Note: Rust impl calls it 'type_' mapped to 'type', Py calls it 'type'
            # Let's check attributes that exist on both
        else:
            print("Could not find matching units to compare.")

    # Graphic Comparison
    if len(py_df.graphics) > 0:
        py_gfx = py_df.graphics[0]
        rust_gfx = rust_df.graphics[0]
        print(f"Graphic 0 Name: Py='{py_gfx.name}', Rust='{rust_gfx.name}' match={py_gfx.name == rust_gfx.name}")

if __name__ == "__main__":
    compare()

import sys
from pathlib import Path

try:
    from Actual_Tools_GDP import GenieWorkspace
except ImportError as e:
    print(f"Error: Could not import Actual_Tools_GDP. Make sure it is installed or in PYTHONPATH.\nDetails: {e}")
    sys.exit(1)

INPUT_DAT = "empires2_x2_p1.dat"
OUTPUT_DAT = "output_units.dat"

def main():
    if not Path(INPUT_DAT).exists():
        print(f"Skipping example: '{INPUT_DAT}' not found.")
        return

    try:
        workspace = GenieWorkspace.load(INPUT_DAT)
        unit_manager = workspace.unit_manager

        # 1. Create a new unit based on ID 4 (Archer)
        # This will find a new slot automatically
        # Note: Requires a valid base_unit_id to exist
        if unit_manager.exists(4):
            new_unit = unit_manager.create("Super Archer", base_unit_id=4)
            print(f"Created new unit '{new_unit.name}' at ID {new_unit.id}")

            # 2. Modify properties
            new_unit.hit_points = 100
            new_unit.line_of_sight = 8
            new_unit.speed = 1.2

            # 3. Clone a unit into a specific ID
            # Useful if you want to replace an existing unit or use a specific slot
            target_id = 100
            try:
                # Use clone_into when you care about the destination ID
                cloned_unit = unit_manager.clone_into(
                    dest_unit_id=target_id,
                    base_unit_id=4,
                    name="Cloned Archer"
                )
                print(f"Cloned unit into ID {target_id}: {cloned_unit.name}")
            except Exception as e:
                print(f"Could not clone to {target_id}: {e}")
        else:
            print("Base unit ID 4 not found, skipping creation.")

        # 4. Save Registry
        # This saves a JSON map of what we created, useful for other tools
        workspace.save_registry("registry.json")

        workspace.save(OUTPUT_DAT)
        print(f"Saved to {OUTPUT_DAT}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

import sys
from pathlib import Path

# Try to import Actual_Tools_GDP
try:
    from Actual_Tools_GDP import GenieWorkspace
except ImportError as e:
    print(f"Error: Could not import Actual_Tools_GDP. Make sure it is installed or in PYTHONPATH.\nDetails: {e}")
    sys.exit(1)

# Paths
INPUT_DAT = "empires2_x2_p1.dat"
OUTPUT_DAT = "output_example.dat"

def main():
    if not Path(INPUT_DAT).exists():
        print(f"Skipping example: '{INPUT_DAT}' not found in current directory.")
        print("Please place a valid DAT file here to run this example.")
        return

    try:
        # 1. Load the workspace
        # validation=VALIDATE_NEW is default, checking only what we change
        workspace = GenieWorkspace.load(INPUT_DAT)
        print(f"Loaded {INPUT_DAT}")

        # 2. Access managers
        unit_manager = workspace.unit_manager

        # 3. Simple modification
        # Get the first unit (usually ARCHER or similar in full DATs, here just ID 4)
        if unit_manager.exists(4):
            archer = unit_manager.get(4)
            old_hp = archer.hit_points
            archer.hit_points = 45
            print(f"Modified Unit 4 HP: {old_hp} -> {archer.hit_points}")
        else:
            print("Unit ID 4 does not exist in this DAT file.")

        # 4. Save
        workspace.save(OUTPUT_DAT)
        print(f"Saved to {OUTPUT_DAT}")

    except Exception as e:
        print(f"An error occurred during execution: {e}")

if __name__ == "__main__":
    main()

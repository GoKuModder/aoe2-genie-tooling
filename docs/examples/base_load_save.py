from pathlib import Path
import sys

# Import from Actual_Tools_GDP as the source of truth
try:
    from Actual_Tools_GDP import GenieWorkspace, ValidationLevel, ValidationError
except ImportError:
    print("Error: Actual_Tools_GDP not installed or not in path.")
    sys.exit(1)

def main():
    # Define paths
    input_dat = Path("empires2_x2_p1.dat")
    output_dat = Path("empires2_x2_p1_edited.dat")

    # Check if input file exists
    if not input_dat.exists():
        print(f"Skipping example: '{input_dat}' not found.")
        print("Please place a valid Age of Empires II DE .dat file in this directory to run this example.")
        return

    try:
        # 1. Load the workspace
        print(f"Loading {input_dat}...")
        workspace = GenieWorkspace.load(input_dat)

        # 2. Access managers (just to show it works)
        print(f"Unit Manager initialized with {workspace.unit_manager.count()} units.")

        # 3. Save the workspace
        print(f"Saving to {output_dat}...")
        workspace.save(output_dat, validate=ValidationLevel.VALIDATE_NEW)

        print("Success!")

    except ValidationError as e:
        print(f"Validation failed during save: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

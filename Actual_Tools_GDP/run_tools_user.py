from pathlib import Path
import sys

# Adjust if GenieDatParser is elsewhere; this assumes it is alongside resolve_conflicts.py
repo_root = Path(__file__).resolve().parent
genie_dat_parser_src = repo_root / "GenieDatParser" / "src"

sys.path.insert(0, str(genie_dat_parser_src))


from Actual_Tools_GDP.Base import GenieWorkspace


import argparse

# Setup argument parser for portable path handling
parser = argparse.ArgumentParser(description="GenieUtils Tool Runner")
parser.add_argument("input_dat", nargs="?", default=None, help="Path to input .dat file")
args = parser.parse_args()

# Determine input path
if args.input_dat:
    input_dat = Path(args.input_dat).resolve()
else:
    # Look for dat file in typical locations
    possible_paths = [
        Path.cwd() / "empires2_x2_p1.dat",
        Path(__file__).parent / "empires2_x2_p1.dat",
    ]
    input_dat = next((p for p in possible_paths if p.exists()), None)

if not input_dat or not input_dat.exists():
    print(f"Error: Input file 'empires2_x2_p1.dat' not found.")
    print(f"Usage: python {Path(__file__).name} [path_to_dat_file]")
    sys.exit(1)

print(f"Using input file: {input_dat}")

workspace = GenieWorkspace.load(str(input_dat))
print(f'Graphics: {len(workspace.dat.graphics)}')

registry_json = "genie_edits.json"




unit_manager = workspace.genie_unit_manager()
graphics_manager = workspace.graphic_manager()
sounds_manager = workspace.sound_manager()
techs_manager = workspace.tech_manager()
effects_manager = workspace.effect_manager()
civs_manager = workspace.civ_manager()



# ============================
# Create units
# ============================
unit1 = unit_manager.create(
    name="Hero1",
    base_unit_id=4,
    unit_id=2900,
    on_conflict="overwrite",
)
unit1.creatable.train_location_id = 1

unit1.bird.move_sound = 1
unit1.move_sound = 20


unit1.add_drop_site(
    unit_id=4,
)
unit1.default_task_id = 100

unit1.add_armour(
    class_=3,
    amount=120
)

unit1.resource_storages.resource_1(type=0, amount=200.0, flag=1)
unit1.resource_storages.resource_2(type=1, amount=150.0, flag=1)
unit1.resource_storages.resource_3(type=2, amount=100.0, flag=0)

unit1.tasks.add_task(
    id=5,
    work_value_1=1
)



# unit1.train_locations = 1 this line is wrong as train_locations is a class (see Genie)
# unit1.annexes = 1 this line is wrong as annex is a class (see Genie)
unit1.attack_graphic = 20000    # This line should throw error. Graphics 20000 doesn't exist at the end of the code.

# unit1.selection_effect Why isn't this supported?
# unit1.vanish_mode = 3 Why isn't this supported?
# unit1.projectile.vanish_mode = 3 VanishMode has values between 0 1 2. 3 should raise error but this doesn't do that.







try:
    workspace.save('test_output.dat')
    workspace.save_registry(registry_json)
except Exception as e:
    print(f'')

'''
from Actual_Tools import GenieWorkspace

# Paths

input_dat = "empires2_x2_p1.dat"
output_dat = "empires2_x2_p1_output.dat"





# ============================
# Load
# ============================
workspace = GenieWorkspace.load(input_dat)


# ============================
# Save DAT
# ============================
workspace.save(output_dat)

# ============================
# Save registry for ASP
# ============================

'''
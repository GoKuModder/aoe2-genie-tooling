from Actual_Tools.Base import GenieWorkspace


input_dat = r"F:\Games\AOE II DE Scirpting Python Projects\1 GenieUtils Python Tools  Library\empires2_x2_p1_RUST_TEST.dat"

ws = GenieWorkspace.load(input_dat)
print(f'Graphics: {len(ws.dat.graphics)}')

um = ws.genie_unit_manager()
unit = um.get(4)
print(f'Unit: {unit}')

#unit.attack_graphic = 20000 Works now and throws error

#unit.projectile_unit_id = 500 # Doesnt work to throw error even tho this unit doesn't exist



try:
    ws.save('test_output.dat')
except Exception as e:
    print(f'')

'''
from Actual_Tools import GenieWorkspace

# Paths

input_dat = "empires2_x2_p1.dat"
output_dat = "empires2_x2_p1_output.dat"

registry_json = "genie_edits.json"



# ============================
# Load
# ============================
workspace = GenieWorkspace.load(input_dat)

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



# ============================
# Save DAT
# ============================
workspace.save(output_dat)

# ============================
# Save registry for ASP
# ============================
workspace.save_registry(registry_json)
'''
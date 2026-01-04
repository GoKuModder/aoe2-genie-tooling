
import os
from genieutils.datfile import DatFile as LegacyDatFile
from genie_rust import DatFile as RustDatFile

def compare_units(legacy_unit, rust_unit):
    """Compares attributes of two unit objects and prints a diff."""
    print(f"--- Comparing Unit ID: {legacy_unit.id} ---")

    print("Inspecting Rust Unit object...")
    print(f"Type: {type(rust_unit)}")
    print("Attributes:", dir(rust_unit))
    print("-" * 10)

    diffs = []
    attributes_to_compare = [
        "name", "hit_points", "line_of_sight", "speed"
    ]

    for attr in attributes_to_compare:
        try:
            legacy_val = getattr(legacy_unit, attr)
            rust_val = getattr(rust_unit, attr)
            if legacy_val != rust_val:
                diffs.append(f"  - {attr}: '{legacy_val}' (legacy) vs '{rust_val}' (rust)")
        except AttributeError:
            diffs.append(f"  - {attr}: NOT FOUND on one of the units.")
        except Exception as e:
            diffs.append(f"  - Error comparing '{attr}': {e}")

    # Specific check for attacks
    try:
        legacy_attacks = legacy_unit.attacks
        rust_attacks = rust_unit.attacks
        if len(legacy_attacks) != len(rust_attacks):
             diffs.append(f"  - Attack count mismatch: {len(legacy_attacks)} (legacy) vs {len(rust_attacks)} (rust)")
        elif len(legacy_attacks) > 0:
            legacy_attack = legacy_attacks[0]
            rust_attack = rust_attacks[0]
            if legacy_attack.amount != rust_attack.amount:
                diffs.append(f"  - Attack[0] Amount: {legacy_attack.amount} (legacy) vs {rust_attack.amount} (rust)")
            if legacy_attack.class_ != rust_attack.class_:
                diffs.append(f"  - Attack[0] Class: {legacy_attack.class_} (legacy) vs {rust_attack.class_} (rust)")
    except AttributeError as e:
        diffs.append(f"  - 'attacks' attribute missing: {e}")

    if diffs:
        for diff in diffs:
            print(diff)
    else:
        print("  No differences found in checked attributes.")
    print("\n")


def main():
    """Loads a DAT file with both backends and compares units."""
    dat_path = os.path.join(os.path.dirname(__file__), '..', 'empires2_x2_p1_RUST_TEST.dat')

    print("Loading with genieutils-py...")
    try:
        legacy_dat = LegacyDatFile.parse(dat_path)
        print("  ...success.")
    except Exception as e:
        print(f"  ...FAILED: {e}")
        return

    print("Loading with Genie-Rust...")
    try:
        rust_dat = RustDatFile.from_file(dat_path)
        print("  ...success.")
    except Exception as e:
        print(f"  ...FAILED: {e}")
        return

    # NOTE on Civ Indexes:
    # The legacy `genieutils-py` library uses a 1-based index for its `civs` list,
    # where civs[0] is a dummy "Gaia" civ that is not present in the DAT file's
    # actual civilization list. The real first civ (e.g., "British") is at index 1.
    # The new `genie-rust` backend, however, uses a 0-based index that directly
    # maps to the civilizations in the DAT file. `civs[0]` is the first real civ.
    # Therefore, we use different indexes to access the same civilization data.
    legacy_civ_index = 1
    rust_civ_index = 0

    unit_ids_to_compare = [4, 21]  # Archer, Villager

    for unit_id in unit_ids_to_compare:
        try:
            legacy_unit = legacy_dat.civs[legacy_civ_index].units[unit_id]
            rust_unit = rust_dat.civs[rust_civ_index].units[unit_id]
            compare_units(legacy_unit, rust_unit)
        except IndexError:
            print(f"Unit ID {unit_id} not found in one of the backends. File may be too short.")
        except Exception as e:
            print(f"An error occurred comparing unit {unit_id}: {e}")

if __name__ == "__main__":
    main()

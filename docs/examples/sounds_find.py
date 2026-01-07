from Actual_Tools_GDP import GenieWorkspace

def main():
    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    sm = workspace.sound_manager

    # 1. Find an existing sound
    # Search for the selection sound of a villager
    existing = sm.find_by_file_name("v_m_select_1.wav")
    if existing:
        print(f"Found existing sound at ID {existing.id}")

    # 2. Create a new multi-sample sound
    new_sound = sm.add_new()

    # Add variations
    new_sound.new_sound("custom_attack_01.wav")
    new_sound.new_sound("custom_attack_02.wav")

    # 3. Assign to a unit
    unit = workspace.unit_manager.get(4) # Archer
    unit.attack_sound = new_sound.id

    print(f"Assigned Sound ID {new_sound.id} to Unit {unit.id}")

if __name__ == "__main__":
    main()

from Actual_Tools_GDP import GenieWorkspace

def main():
    # Load workspace
    try:
        workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    except Exception:
        print("DAT file not found. Skipping example.")
        return

    um = workspace.unit_manager

    # 1. Create a new unit (Standard approach)
    # Automatically finds a free ID at the end of the file
    print("Creating 'Hero Knight'...")
    hero = um.create(name="Hero Knight", base_unit_id=38)  # 38 = Knight

    # Modify the hero - this change is isolated to the hero
    hero.hit_points = 500
    # Add a unique task to the hero
    hero.add_task.combat(class_id=1)

    # Verify isolation: Check the original Knight
    original_knight = um.get(38)
    print(f"Hero HP: {hero.hit_points}")
    print(f"Original Knight HP: {original_knight.hit_points}")

    # 2. Clone into specific ID (Overwrite approach)
    # Let's say we want to replace the Archer (4) with our Hero Knight
    # strictly for demonstration (don't do this in a real mod unless intended!)
    print("Cloning Hero Knight into ID 5000...")

    clone = um.clone_into(
        src_unit_id=hero.id,
        dst_unit_id=5000,
        name="Hero Knight Clone",
        on_conflict="overwrite"
    )

    # 3. Verify deep copy semantics
    # Modifying the clone's attack should NOT affect the original hero
    print("Modifying clone attack...")
    clone.add_attack(class_=3, amount=999)

    # Check attack count
    print(f"Hero Attacks: {len(hero.attacks)}")
    print(f"Clone Attacks: {len(clone.attacks)}")

    if len(clone.attacks) > len(hero.attacks):
        print("SUCCESS: Clone is isolated from original.")
    else:
        print("FAILURE: Clone shares state with original.")

if __name__ == "__main__":
    main()

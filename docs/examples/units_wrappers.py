from Actual_Tools_GDP import GenieWorkspace

def main():
    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    um = workspace.unit_manager

    # Get a unit (Archer)
    archer = um.get(4)

    # 1. Accessing via Wrappers (Explicit)
    # This is "safer" and more self-documenting for complex properties
    print(f"Range: {archer.combat.max_range}")
    print(f"Reload Time: {archer.combat.reload_time}")

    # 2. Accessing via Flattened Properties (Shortcuts)
    # These are convenient for common stats
    # Note: 'speed' is actually on the MovementWrapper (DeadFish) internal struct
    print(f"Speed: {archer.speed}")
    print(f"HP: {archer.hit_points}")

    # 3. Modifying Properties
    # Updates propagate to all civilizations automatically
    archer.combat.base_armor = 1
    archer.combat.accuracy_percent = 100

    # 4. Building specific properties
    # Town Center (109)
    tc = um.get(109)
    if tc.building:
        print(f"Garrison Capacity: {tc.building.garrison_capacity}")

    # 5. Projectile specific properties
    # Arrow (368)
    arrow = um.get(368)
    if arrow.projectile:
        print(f"Arc: {arrow.projectile.arc}")
        print(f"Gravity: {arrow.projectile.gravity}")

if __name__ == "__main__":
    main()

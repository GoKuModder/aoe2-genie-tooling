from Actual_Tools_GDP import GenieWorkspace

def main():
    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    gm = workspace.graphic_manager

    # 1. Create base graphic
    # SLP ID 666 is hypothetical
    base = gm.add_graphic(
        name="Hero Body",
        slp_id=666,
        frame_count=15,
        angle_count=16, # 16 angles for smooth rotation
        duration=0.6    # Seconds per animation cycle
    )

    # 2. Create accessory graphic (e.g., a weapon)
    weapon = gm.add_graphic(
        name="Hero Weapon",
        slp_id=667,
        frame_count=15,
        angle_count=16,
        duration=0.6
    )

    # 3. Stack them using Deltas
    # The weapon will be drawn on top of the body
    base.add_delta(
        graphic_id=weapon.id,
        offset_x=0,
        offset_y=0
    )

    print(f"Created graphic {base.name} (ID {base.id}) with {len(base.deltas)} delta.")

if __name__ == "__main__":
    main()

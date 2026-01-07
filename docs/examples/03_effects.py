import sys
from pathlib import Path

try:
    from Actual_Tools_GDP import GenieWorkspace
except ImportError as e:
    print(f"Error: Could not import Actual_Tools_GDP. Make sure it is installed or in PYTHONPATH.\nDetails: {e}")
    sys.exit(1)

INPUT_DAT = "empires2_x2_p1.dat"
OUTPUT_DAT = "output_effects.dat"

def main():
    if not Path(INPUT_DAT).exists():
        print(f"Skipping example: '{INPUT_DAT}' not found.")
        return

    try:
        workspace = GenieWorkspace.load(INPUT_DAT)
        effect_manager = workspace.effect_manager

        # 1. Create a new effect
        # Effects are containers for commands.
        effect = effect_manager.create("New Civ Bonus")
        print(f"Created effect '{effect.name}' at ID {effect.id}")

        # 2. Add commands fluently using the EffectCommandBuilder
        # The builder provides typed methods for all command types.

        # Example: Multiply HP (Attr 0) of Unit Class 9 (Archers) by 1.1 (10% boost)
        effect.add_command.attribute_modifier_multiply(
            a=9,    # Unit Class
            b=0,    # Attribute (Hit Points)
            c=4,    # Mode (4 = Multiply Class)
            d=1.1   # Amount
        )

        # Example: Add +1 Attack (Attr 9) to Unit ID 4
        effect.add_command.attribute_modifier_add(
            a=4,    # Unit ID
            b=9,    # Attribute (Attack)
            c=0,    # Mode (0 = Add to Unit)
            d=1.0   # Amount
        )

        print(f"Added {len(effect.commands)} commands to effect.")

        workspace.save(OUTPUT_DAT)
        print(f"Saved to {OUTPUT_DAT}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

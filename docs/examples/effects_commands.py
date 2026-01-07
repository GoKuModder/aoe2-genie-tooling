from Actual_Tools_GDP import GenieWorkspace
from Actual_Tools_GDP.Datasets import Attribute, UnitClass, Resource

def main():
    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    effect = workspace.effect_manager.add_new("Complex Bonus")

    # 1. Attribute Modifier (+20% HP for Cavalry)
    # Type 5: Attribute Modifier (Multiply)
    effect.add_command.attribute_modifier_multiply(
        a=UnitClass.CAVALRY,
        b=Attribute.HIT_POINTS,
        d=1.2
    )

    # 2. Resource Drip (Gain 1 Gold per second)
    # Type 101 or specific implementation depending on engine version/mod
    # Standard resource mod
    effect.add_command.resource_modifier(
        a=Resource.GOLD,
        b=1, # Add
        d=100.0 # Instant lump sum
    )

    # 3. Disable a building
    # Type 2: Enable/Disable
    effect.add_command.enable_disable_unit(
        a=82, # Castle
        b=0   # Disable
    )

    # Inspect commands
    for i, cmd in enumerate(effect.commands):
        print(f"Command {i}: Type {cmd.type}")

if __name__ == "__main__":
    main()

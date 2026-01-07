from Actual_Tools_GDP import GenieWorkspace
from Actual_Tools_GDP.Datasets import Attribute, UnitClass

def main():
    workspace = GenieWorkspace.load("empires2_x2_p1.dat")

    # 1. Create a new effect for "Heavy Infantry HP"
    effect = workspace.effect_manager.add_new("Heavy Infantry Upgrade")

    # 2. Add command: +20 HP to Infantry (Class 6)
    # Using the builder for type safety
    effect.add_command.attribute_modifier_add(
        a=UnitClass.INFANTRY,
        b=Attribute.HIT_POINTS,
        d=20.0
    )

    # 3. Add command: +1 Armor to Infantry
    effect.add_command.attribute_modifier_add(
        a=UnitClass.INFANTRY,
        b=Attribute.MELEE_ARMOR,
        d=1.0
    )

    print(f"Created effect '{effect.name}' (ID {effect.id}) with {len(effect.commands)} commands.")

    # 4. Link to a Tech (Optional context)
    # tech = workspace.tech_manager.add_new("Infantry Armor Tech")
    # tech.effect_id = effect.id

if __name__ == "__main__":
    main()

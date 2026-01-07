from Actual_Tools_GDP import GenieWorkspace
from Actual_Tools_GDP.Datasets import UnitClass, Resource

def main():
    workspace = GenieWorkspace.load("empires2_x2_p1.dat")
    um = workspace.unit_manager

    # Create a custom villager
    villager = um.create("Super Villager", base_unit_id=83)

    # Clear existing tasks to start fresh
    villager.tasks.clear()

    # 1. Add Move task (Essential)
    villager.add_task.move(work_range=0.0)

    # 2. Add Combat task (Self-defense)
    villager.add_task.combat(
        class_id=UnitClass.INFANTRY,
        work_range=3.0
    )

    # 3. Add Gather task (Gold)
    # Fluent builder handles the cryptic type codes
    villager.add_task.gather(
        resource_in=Resource.GOLD,
        resource_out=Resource.GOLD,
        work_range=0.5,
        work_value1=2.5 # Super fast gather rate
    )

    # 4. Verify tasks
    print(f"Task count: {len(villager.tasks)}")
    for task in villager.tasks:
        print(f"Task ID {task.id}: Type={task.task_type}")

if __name__ == "__main__":
    main()

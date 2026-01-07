from Actual_Tools_GDP import GenieWorkspace
from Actual_Tools_GDP.Base.core.exceptions import InvalidIdError

def main():
    try:
        # Simulate an invalid ID access
        # In a real scenario, this would happen if you tried to get a unit
        # with an ID larger than the list size.

        # We'll use a mock list here to demonstrate the error formatting
        # since we don't have a loaded workspace in this snippet.
        raise InvalidIdError(
            message="Unit ID 9999 is out of range.",
            context="UnitManager.get(9999)",
            current_items=["Unit 0: Archer", "Unit 1: Militia", "..."],
            hints=["Check the unit ID", "Ensure the unit exists"]
        )

    except InvalidIdError as e:
        print("Caught expected InvalidIdError:")
        print(str(e))

if __name__ == "__main__":
    main()

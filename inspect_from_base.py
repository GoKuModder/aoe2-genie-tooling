try:
    from sections.civilization.unit import Unit
except ImportError:
    pass

try:
    print(f"from_base doc: {Unit.from_base.__doc__}")
except:
    pass

print("Calling Unit.from_base()...")
try:
    Unit.from_base()
except Exception as e:
    print(f"Error: {e}")

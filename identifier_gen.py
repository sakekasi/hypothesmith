import sys
from pathlib import Path

# Add the local hypothesmith package to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from hypothesis import given, settings
import libcst
from hypothesmith import from_node

# Create a strategy for generating Name nodes (identifiers)
name_strategy = from_node(libcst.Name)

@given(name_strategy)
@settings(max_examples=10)
def test_generate_identifiers(name_node):
    # The strategy returns the identifier directly
    print(f"Generated identifier: {name_node}")

if __name__ == "__main__":
    test_generate_identifiers()
import sys
import ast
import keyword
from pathlib import Path

# Add src directory to Python path to use local hypothesmith
sys.path.insert(0, str(Path(__file__).parent / "src"))

from hypothesis import given, settings, strategies as st, HealthCheck
from hypothesmith.syntactic import from_grammar

# Create a strategy for Python expressions that will generate identifiers
expr_strategy = from_grammar("eval_input", auto_target=False)

# Filter expressions to get only simple identifiers
def is_valid_identifier(s: str) -> bool:
    try:
        # Parse the expression and check if it's just a name
        tree = ast.parse(s, mode='eval')
        if not isinstance(tree.body, ast.Name):
            return False
        # Get the actual identifier from the AST
        identifier = tree.body.id
        # Check if it's a valid identifier and not a keyword
        return (identifier.isidentifier() and 
                not keyword.iskeyword(identifier) and
                identifier == s.strip())  # Ensure no extra whitespace
    except SyntaxError:
        return False

identifier_strategy = expr_strategy.filter(is_valid_identifier)

# Sample some identifiers
@settings(max_examples=20, suppress_health_check=[HealthCheck.filter_too_much, HealthCheck.too_slow])
@given(identifier_strategy)
def print_identifier(identifier):
    print(f"Generated identifier: {identifier}")

if __name__ == "__main__":
    print("Sampling 20 Python identifiers...")
    print_identifier()
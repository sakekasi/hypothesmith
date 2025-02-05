from hypothesis import given, settings, Verbosity
from typed_expr_strategy import module_strategy

@given(module_strategy)
@settings(max_examples=10, verbosity=Verbosity.verbose)
def test_typed_assignments(module):
    print("\nGenerated code:")
    print(module.code)
    # Verify it's valid Python code
    compile(module.code, "<string>", "exec")

if __name__ == "__main__":
    test_typed_assignments()
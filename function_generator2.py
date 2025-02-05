from typing import List, Set, Tuple
import libcst
from hypothesis import given, strategies as st, settings, HealthCheck
from hypothesmith.syntactic import from_grammar

@st.composite
def generate_function_body(draw):
    # Generate a valid Python statement using hypothesmith
    statement = draw(from_grammar("file_input"))
    return statement

@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=5)
@given(generate_function_body())
def test_generated_function(code: str):
    # Create a template for our function
    template = """
def process_files(directory: str) -> Tuple[Set[str], Set[str]]:
    set1 = set()
    set2 = set()
    {}
    return set1, set2
"""
    # Insert the generated code into our template
    full_code = template.format(code)
    print(full_code)

if __name__ == "__main__":
    test_generated_function()
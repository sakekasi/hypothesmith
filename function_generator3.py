from typing import List, Set, Tuple
import libcst
from hypothesis import given, strategies as st, settings, HealthCheck
from hypothesmith.syntactic import from_grammar

@st.composite
def generate_function_body(draw):
    # Generate multiple valid Python statements using hypothesmith
    statements = []
    for _ in range(3):  # Generate 3 statements
        stmt = draw(from_grammar("file_input"))
        if stmt.strip():  # Only add non-empty statements
            statements.append(stmt)
    return "\n".join(statements)

@settings(suppress_health_check=[HealthCheck.too_slow], max_examples=3)
@given(generate_function_body())
def test_generated_function(code: str):
    # Create a template for our function with file processing logic
    template = """
def process_files(directory: str) -> Tuple[Set[str], Set[str]]:
    set1 = set()
    set2 = set()
    
    import os
    import re
    
    pattern1 = re.compile(r'pattern1:(\w+)')
    pattern2 = re.compile(r'pattern2:(\w+)')
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                path = os.path.join(root, file)
                with open(path) as f:
                    content = f.read()
                    {}
    
    return set1, set2
"""
    # Insert the generated code into our template
    full_code = template.format(code)
    print(full_code)
    print("-" * 80)

if __name__ == "__main__":
    test_generated_function()
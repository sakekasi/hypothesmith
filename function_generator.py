from typing import List, Set, Tuple
import libcst
from hypothesis import given, strategies as st
from hypothesmith.syntactic import from_grammar
import sys
sys.path.append('/workspace/hypothesmith/src')

# Define basic building blocks for our AST
def make_type_annotation(name: str) -> libcst.Annotation:
    return libcst.Annotation(
        libcst.Name(name)
    )

def make_param_with_annotation(name: str, type_name: str) -> libcst.Param:
    return libcst.Param(
        name=libcst.Name(name),
        annotation=make_type_annotation(type_name)
    )

def make_return_annotation() -> libcst.Annotation:
    return libcst.Annotation(
        libcst.Subscript(
            value=libcst.Name("Tuple"),
            slice=[
                libcst.SubscriptElement(
                    libcst.Subscript(
                        value=libcst.Name("Set"),
                        slice=[
                            libcst.SubscriptElement(
                                libcst.Name("str")
                            )
                        ]
                    )
                ),
                libcst.SubscriptElement(
                    libcst.Subscript(
                        value=libcst.Name("Set"),
                        slice=[
                            libcst.SubscriptElement(
                                libcst.Name("str")
                            )
                        ]
                    )
                )
            ]
        )
    )

# Strategy for generating the function
@st.composite
def file_processor_function(draw):
    # Generate the function using hypothesmith
    # Generate a single statement using the file_input grammar
    module_code = draw(from_grammar("file_input"))
    # Parse it into a LibCST node
    module = libcst.parse_module(module_code)
    # Extract the first statement
    func_body = module.body[0] if module.body else libcst.Pass()
    
    # Create the function definition
    func_def = libcst.FunctionDef(
        name=libcst.Name("process_files"),
        params=libcst.Parameters(
            params=[
                make_param_with_annotation("directory", "str")
            ]
        ),
        returns=make_return_annotation(),
        body=libcst.IndentedBlock([
            # Initialize sets
            libcst.SimpleStatementLine([
                libcst.Assign(
                    targets=[libcst.Name("set1")],
                    value=libcst.Call(func=libcst.Name("set"), args=[])
                )
            ]),
            libcst.SimpleStatementLine([
                libcst.Assign(
                    targets=[libcst.Name("set2")],
                    value=libcst.Call(func=libcst.Name("set"), args=[])
                )
            ]),
            # Add generated statement
            func_body,
            # Return statement
            libcst.SimpleStatementLine([
                libcst.Return(
                    value=libcst.Tuple([
                        libcst.Name("set1"),
                        libcst.Name("set2")
                    ])
                )
            ])
        ])
    )
    
    # Wrap in a module
    module = libcst.Module(body=[func_def])
    return module.code

# Example usage
@given(file_processor_function())
def test_generated_function(code: str):
    print(code)
    # The code can be executed by using:
    # exec(code)
    # But we'll just print it for demonstration

if __name__ == "__main__":
    test_generated_function()
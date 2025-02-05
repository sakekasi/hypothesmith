import sys
import os

# Add src directory to path so we can import hypothesmith
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from hypothesmith import from_node
import hypothesis.strategies as st
from hypothesis import given, settings, HealthCheck
import libcst as cst

# Strategy to generate loop body statements
@st.composite
def loop_body_strategy(draw):
    # Choose between different types of statements
    stmt_type = draw(st.sampled_from([
        "print",
        "assign"
    ]))
    
    if stmt_type == "print":
        return cst.SimpleStatementLine(body=[
            cst.Expr(value=cst.Call(
                func=cst.Name("print"),
                args=[cst.Arg(value=cst.Name("i"))]
            ))
        ])
    else:  # assign
        return cst.SimpleStatementLine(body=[
            cst.Assign(
                targets=[cst.AssignTarget(target=cst.Name("x"))],
                value=cst.Call(
                    func=cst.Name("len"),
                    args=[cst.Arg(value=cst.Name("i"))]
                )
            )
        ])

# Strategy to generate loop variables
@st.composite
def loop_var_strategy(draw):
    # Generate a simple name node for loop variables
    return cst.Name(value=draw(st.sampled_from(["i", "j", "k"])))

# Strategy to generate iterable expressions
@st.composite
def iterable_strategy(draw):
    # Choose between different types of iterables
    iter_type = draw(st.sampled_from([
        "range",
        "list",
        "range_with_step"
    ]))
    
    if iter_type == "range":
        return cst.Call(
            func=cst.Name("range"),
            args=[cst.Arg(value=cst.Integer(str(draw(st.integers(min_value=3, max_value=10)))))]
        )
    elif iter_type == "list":
        nums = draw(st.lists(st.integers(min_value=1, max_value=5), min_size=2, max_size=4))
        return cst.List(
            elements=[
                cst.Element(value=cst.Integer(str(n)))
                for n in nums
            ]
        )
    else:  # range_with_step
        return cst.Call(
            func=cst.Name("range"),
            args=[
                cst.Arg(value=cst.Integer("0")),
                cst.Arg(value=cst.Integer("10")),
                cst.Arg(value=cst.Integer("2"))
            ]
        )

# Strategy to generate for loops
@st.composite
def for_loop_strategy(draw):
    target = draw(loop_var_strategy())
    iter_expr = draw(iterable_strategy())
    body = [draw(loop_body_strategy()) for _ in range(draw(st.integers(min_value=1, max_value=3)))]
    
    return cst.For(
        target=target,
        iter=iter_expr,
        body=cst.IndentedBlock(body=body)
    )

# Function to generate and print sample programs
@settings(max_examples=5, deadline=None)
@given(st.data())
def generate_loop_programs(data):
    loop = data.draw(for_loop_strategy())
    module = cst.Module(body=[loop])
    print("\n=== Generated Program ===")
    print(module.code)
    print("=======================\n")

if __name__ == "__main__":
    generate_loop_programs()
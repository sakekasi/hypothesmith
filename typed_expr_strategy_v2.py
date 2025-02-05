from hypothesis import given, strategies as st
import libcst as cst
from hypothesmith import from_node

# Define strategies for basic types
simple_types = st.sampled_from([
    cst.Name("int"),
    cst.Name("str"),
    cst.Name("bool"),
    cst.Name("float")
])

# Strategy for variable names
var_names = st.from_regex(r"[a-z][a-z0-9_]{0,10}", fullmatch=True)

# Strategy for literal values
def make_literal_for(type_name: str) -> st.SearchStrategy[cst.BaseExpression]:
    """Generate a literal value of the given type."""
    if type_name == "int":
        return st.integers(min_value=0, max_value=1000).map(
            lambda x: cst.Integer(str(x))
        )
    elif type_name == "str":
        return st.text(min_size=0, max_size=10).map(
            lambda x: cst.SimpleString(repr(x))
        )
    elif type_name == "bool":
        return st.booleans().map(lambda x: cst.Name("True" if x else "False"))
    elif type_name == "float":
        return st.floats(
            min_value=0.0,
            max_value=1000.0,
            allow_infinity=False,
            allow_nan=False
        ).map(lambda x: cst.Float(f"{x:.1f}"))
    return st.just(cst.Integer("0"))  # fallback

# Strategy for binary operations
@st.composite
def make_binary_op_for(draw, type_name: str) -> cst.BaseExpression:
    """Generate a binary operation that results in the given type."""
    if type_name == "int":
        ops = [
            cst.Add(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            ),
            cst.Multiply(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            )
        ]
        op = draw(st.sampled_from(ops))
        left = draw(make_typed_expr_for(cst.Name("int"), max_depth=0))
        right = draw(make_typed_expr_for(cst.Name("int"), max_depth=0))
        return cst.BinaryOperation(left=left, operator=op, right=right)
    elif type_name == "str":
        op = cst.Add(
            whitespace_before=cst.SimpleWhitespace(" "),
            whitespace_after=cst.SimpleWhitespace(" ")
        )
        left = draw(make_typed_expr_for(cst.Name("str"), max_depth=0))
        right = draw(make_typed_expr_for(cst.Name("str"), max_depth=0))
        return cst.BinaryOperation(left=left, operator=op, right=right)
    elif type_name == "bool":
        ops = [
            cst.And(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            ),
            cst.Or(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            )
        ]
        op = draw(st.sampled_from(ops))
        left = draw(make_typed_expr_for(cst.Name("bool"), max_depth=0))
        right = draw(make_typed_expr_for(cst.Name("bool"), max_depth=0))
        return cst.BooleanOperation(left=left, operator=op, right=right)
    elif type_name == "float":
        ops = [
            cst.Add(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            ),
            cst.Multiply(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            )
        ]
        op = draw(st.sampled_from(ops))
        left = draw(make_typed_expr_for(cst.Name("float"), max_depth=0))
        right = draw(make_typed_expr_for(cst.Name("float"), max_depth=0))
        return cst.BinaryOperation(left=left, operator=op, right=right)
    return cst.Integer("0")  # fallback

# Strategy for comparison operations
@st.composite
def make_comparison_for(draw, type_name: str) -> cst.BaseExpression:
    """Generate a comparison operation that results in a boolean."""
    if type_name == "bool":
        ops = [
            cst.LessThan(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            ),
            cst.GreaterThan(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            ),
            cst.Equal(
                whitespace_before=cst.SimpleWhitespace(" "),
                whitespace_after=cst.SimpleWhitespace(" ")
            )
        ]
        op = draw(st.sampled_from(ops))
        comparable_types = ["int", "float", "str"]
        comp_type = draw(st.sampled_from(comparable_types))
        left = draw(make_typed_expr_for(cst.Name(comp_type), max_depth=0))
        right = draw(make_typed_expr_for(cst.Name(comp_type), max_depth=0))
        return cst.Comparison(
            left=left,
            comparisons=[cst.ComparisonTarget(operator=op, comparator=right)]
        )
    return cst.Name("True")  # fallback

def make_typed_expr_for(type_node: cst.Name, max_depth: int = 2) -> st.SearchStrategy[cst.BaseExpression]:
    """Generate an expression of the given type with bounded depth."""
    if not isinstance(type_node, cst.Name):
        return st.just(cst.Integer("0"))  # fallback
    
    type_name = type_node.value
    if max_depth <= 0:
        return make_literal_for(type_name)
    
    # Mix of literals, binary operations, and comparisons
    strategies = [make_literal_for(type_name)]
    if max_depth > 0:
        strategies.append(make_binary_op_for(type_name))
        if type_name == "bool":
            strategies.append(make_comparison_for(type_name))
    
    return st.one_of(*strategies)

# Strategy for typed assignments
@st.composite
def typed_assignments(draw):
    name = draw(var_names)
    type_node = draw(simple_types)
    value = draw(make_typed_expr_for(type_node))
    
    return cst.AnnAssign(
        target=cst.Name(name),
        annotation=cst.Annotation(type_node),
        value=value,
        equal=cst.AssignEqual(cst.SimpleWhitespace(" "), cst.SimpleWhitespace(" "))
    )

# Strategy for a module containing a typed assignment
@st.composite
def module_with_assignment(draw):
    assignment = draw(typed_assignments())
    return cst.Module(body=[assignment])

module_strategy = module_with_assignment()
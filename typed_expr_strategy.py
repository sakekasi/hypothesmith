from hypothesis import given, strategies as st
import libcst as cst
from hypothesmith import from_node

# Define strategies for basic types and their corresponding expressions
simple_types = st.sampled_from([
    cst.Name("int"),
    cst.Name("str"),
    cst.Name("bool"),
    cst.Name("float")
])

def make_typed_expr_for(type_node):
    if isinstance(type_node, cst.Name):
        type_name = type_node.value
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

# Strategy for variable names
var_names = st.from_regex(r"[a-z][a-z0-9_]{0,10}", fullmatch=True)

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
from typing import List, Set, Tuple
import libcst
from hypothesis import given, strategies as st
from hypothesmith import from_node
import string

def make_type_annotation():
    return st.one_of(
        st.just(libcst.Annotation(
            annotation=libcst.Name("str")
        )),
        st.just(libcst.Annotation(
            annotation=libcst.Subscript(
                value=libcst.Name("Tuple"),
                slice=[
                    libcst.SubscriptElement(
                        libcst.Index(
                            libcst.Subscript(
                                value=libcst.Name("Set"),
                                slice=[
                                    libcst.SubscriptElement(
                                        libcst.Index(libcst.Name("str"))
                                    )
                                ]
                            )
                        )
                    ),
                    libcst.SubscriptElement(
                        libcst.Index(
                            libcst.Subscript(
                                value=libcst.Name("Set"),
                                slice=[
                                    libcst.SubscriptElement(
                                        libcst.Index(libcst.Name("str"))
                                    )
                                ]
                            )
                        )
                    )
                ]
            )
        ))
    )

def make_for_loop_body():
    return st.lists(
        st.one_of(
            st.builds(
                libcst.Assign,
                targets=st.lists(
                    st.builds(
                        libcst.AssignTarget,
                        target=st.builds(libcst.Name, value=st.sampled_from(["result", "temp"]))
                    ),
                    min_size=1,
                    max_size=1
                ),
                value=st.builds(
                    libcst.Call,
                    func=st.builds(libcst.Name, value=st.just("set")),
                    args=st.just([])
                )
            ),
            st.builds(
                libcst.Expr,
                value=st.builds(
                    libcst.Call,
                    func=st.builds(
                        libcst.Attribute,
                        value=st.builds(libcst.Name, value=st.sampled_from(["result", "temp"])),
                        attr=st.builds(libcst.Name, value=st.just("add"))
                    ),
                    args=st.lists(
                        st.builds(
                            libcst.Arg,
                            value=st.builds(libcst.SimpleString, value=st.just('"item"'))
                        ),
                        min_size=1,
                        max_size=1
                    )
                )
            )
        ),
        min_size=1,
        max_size=3
    )

def make_for_loop():
    return st.builds(
        libcst.For,
        target=st.builds(
            libcst.Name,
            value=st.just("item")
        ),
        iter=st.builds(
            libcst.Call,
            func=st.builds(libcst.Name, value=st.sampled_from(["range", "enumerate"])),
            args=st.lists(
                st.builds(
                    libcst.Arg,
                    value=st.builds(libcst.Integer, value=st.just("10"))
                ),
                min_size=1,
                max_size=1
            )
        ),
        body=st.builds(
            libcst.IndentedBlock,
            body=make_for_loop_body()
        )
    )

def make_function_body():
    return st.lists(
        st.one_of(
            st.builds(
                libcst.Assign,
                targets=st.lists(
                    st.builds(
                        libcst.AssignTarget,
                        target=st.builds(libcst.Name, value=st.just("result"))
                    ),
                    min_size=1,
                    max_size=1
                ),
                value=st.builds(
                    libcst.Call,
                    func=st.builds(libcst.Name, value=st.just("set")),
                    args=st.just([])
                )
            ),
            make_for_loop(),
            st.builds(
                libcst.Return,
                value=st.builds(libcst.Name, value=st.just("result"))
            )
        ),
        min_size=2,
        max_size=4
    )

def make_function():
    return st.builds(
        libcst.FunctionDef,
        name=st.builds(
            libcst.Name,
            value=st.just("process_data")
        ),
        params=st.builds(
            libcst.Parameters,
            params=st.lists(
                st.builds(
                    libcst.Param,
                    name=st.builds(libcst.Name, value=st.just("input_data")),
                    annotation=make_type_annotation()
                ),
                min_size=1,
                max_size=1
            )
        ),
        returns=make_type_annotation(),
        body=st.builds(
            libcst.IndentedBlock,
            body=make_function_body()
        )
    )

def make_module():
    return st.builds(
        libcst.Module,
        body=st.lists(make_function(), min_size=1, max_size=1)
    )

@given(make_module())
def test_generated_code(module):
    print(module.code)

if __name__ == "__main__":
    test_generated_code()
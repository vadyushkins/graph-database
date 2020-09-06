from pygraphblas import Matrix, INT64
from pyformlang.finite_automaton import *

def test_matrix_product():
    a = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [1, 1, 1, 1],
        typ=INT64,
    )
    b = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [2, 2, 2, 2],
        typ=INT64,
    )

    actual = a @ b
    expected = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [4, 4, 4, 4],
        typ=INT64
    )

    assert expected.iseq(actual)


def test_dfa_intersection():
    s0 = State(0)
    s1 = State(1)

    a = Symbol("a")

    dfa1 = DeterministicFiniteAutomaton(
        states={s0},
        input_symbols={a},
        start_state=s0,
        final_states={s0}
    )
    dfa1.add_transition(s0, a, s1)
    dfa1.add_transition(s1, a, s0)

    dfa2 = DeterministicFiniteAutomaton(
        states={s0},
        input_symbols={a},
        start_state=s0,
        final_states={s0}
    )
    dfa2.add_transition(s0, a, s0)

    actual = dfa1 and dfa2

    expected = DeterministicFiniteAutomaton(
        states={s0},
        input_symbols={a},
        start_state=s0,
        final_states={s0}
    )
    expected.add_transition(s0, a, s0)

    assert expected.is_equivalent_to(actual)


from pyformlang.finite_automaton import *


def test_simple():
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


def test_by_regex(automatic_suite):
    a = automatic_suite['left']
    b = automatic_suite['right']

    actual = a.get_intersection(b)

    expected = automatic_suite['expected']

    def equal(fa1, fa2):
        for s in automatic_suite['accepts']:
            if fa1.accepts(s) != fa2.accepts(s):
                return False
        for s in automatic_suite['not accepts']:
            if fa1.accepts(s) != fa2.accepts(s):
                return False
        return True

    assert equal(expected, actual)

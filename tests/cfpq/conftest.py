from itertools import product

import pytest

from src.CFPQ import Hellings, Azimov, TensorWithCNF, TensorWithRSM

grammars = {
    0: ['S a S b S', 'S ']
    , 1: ['S a S b', 'S ']
    , 2: ['S S S', 'S a', 'S ']
    , 3: ['S A B', 'A A A', 'B B B', 'A a', 'B b']
    , 4: ['S b S b b', 'S A', 'A a A', 'A ']
    , 5: ['S A A', 'A a', 'A b']
    , 6: ['S b S b b', 'S ']
    , 7: ['S A B', 'A A A', 'B B B', 'A a', 'B b', 'A ', 'B ']
}

algorithms = [
    Hellings
    , Azimov
    , TensorWithCNF
    , TensorWithRSM
]


@pytest.fixture(scope='session', params=[
    {
        'graph': ['0 a 1', '1 a 2', '2 a 0']
        , 'grammar': grammars[2]
        , 'expected': set(product({0, 1, 2}, {0, 1, 2}))
    }
    , {
        'graph': ['0 a 1', '1 a 2', '2 a 3', '3 a 0', '3 b 4', '4 b 3']
        , 'grammar': grammars[0]
        , 'expected': {(3, 3), (0, 4), (1, 3), (2, 4)} \
                      | {(i, i) for i in range(5)}
    }
    , {
        'graph': ['0 a 1', '1 b 2']
        , 'grammar': grammars[3]
        , 'expected': {(0, 2)}
    }
    , {
        'graph': ['0 a 0', '0 b 0']
        , 'grammar': grammars[1]
        , 'expected': {(0, 0)}
    }
    , {
        'graph': ['0 b 1', '1 b 1', '1 a 2', '2 a 3', '2 b 3', '3 b 4', '4 b 3']
        , 'grammar': grammars[4]
        , 'expected': {(0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (4, 3), (0, 3), (1, 4), (2, 3), (1, 3)} \
                      | {(i, i) for i in range(5)}
    }
    , {
        'graph': ['0 a 1', '1 b 2', '2 a 3']
        , 'grammar': grammars[5]
        , 'expected': {(0, 2), (1, 3)}
    }
    , {
        'graph': ['0 b 1', '1 b 2', '2 b 3', '3 b 2']
        , 'grammar': grammars[6]
        , 'expected': {(0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (3, 2)} \
                      | {(i, i) for i in range(4)}
    }
    , {
        'graph': ['0 a 1', '1 b 2', '0 a 0', '1 a 1', '1 b 1', '2 b 2', '2 b 0', '2 a 0']
        , 'grammar': grammars[7]
        , 'expected': {(i, j) for i, j in product(*[range(3)] * 2)}
    }
])
def manual_suite(request):
    return request.param


@pytest.fixture(scope='session', params=algorithms)
def algo(request):
    return request.param

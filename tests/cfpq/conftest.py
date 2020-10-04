from itertools import product

import pytest

from src.CFPQ import Hellings, Azimov, Tensor

grammars = [
    '\n'.join(['S -> a S b S', 'S -> '])
    , '\n'.join(['S -> a S b', 'S -> '])
    , '\n'.join(['S -> S S', 'S -> a', 'S -> '])
    , '\n'.join(['S -> A B', 'A -> A A', 'B -> B B', 'A -> a', 'B -> b'])
    , '\n'.join(['S -> b S b b', 'S -> A', 'A -> a A', 'A -> '])
    , '\n'.join(['S -> A A', 'A -> a', 'A -> b'])
]

algorithms = [
    Hellings.cfpq
    , Azimov.cfpq
    , Tensor.cfpq
]


@pytest.fixture(scope='session', params=[
    {
        'edges': ['0 a 1', '1 a 2', '2 a 0']
        , 'cnf': grammars[2]
        , 'expected': set(product({0, 1, 2}, {0, 1, 2}))
    }
    , {
        'edges': ['0 a 1', '1 a 2', '2 a 3', '3 a 0', '3 b 4', '4 b 3']
        , 'cnf': grammars[0]
        , 'expected': {(3, 3), (0, 4), (1, 3), (2, 4)} | {(i, i) for i in range(5)}
    }
    , {
        'edges': ['0 a 1', '1 b 2']
        , 'cnf': grammars[3]
        , 'expected': {(0, 2)}
    }
    , {
        'edges': ['0 a 0', '0 b 0']
        , 'cnf': grammars[1]
        , 'expected': {(0, 0)}
    }
    , {
        'edges': ['0 b 1', '1 b 1', '1 a 2', '2 a 3', '2 b 3', '3 b 4', '4 b 3']
        , 'cnf': grammars[4]
        , 'expected': {(0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (4, 3), (0, 3), (1, 4), (2, 3), (1, 3)} \
                      | {(i, i) for i in range(5)}
    }
    , {
        'edges': ['0 a 1', '1 b 2', '2 a 3']
        , 'cnf': grammars[5]
        , 'expected': {(0, 2), (1, 3)}
    }
])
def manual_suite(request):
    return request.param


@pytest.fixture(scope='session', params=algorithms)
def algo(request):
    return request.param

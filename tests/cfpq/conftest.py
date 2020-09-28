import pytest

from itertools import product

grammars = [
    'S -> a S b S\nS -> '
    , 'S -> a S b\nS -> '
    , 'S -> S S\nS -> a'
    , 'S -> A B\nA -> A A\nB -> B B\nA -> a\nB -> b'
]


@pytest.fixture(scope='session', params=[
    {
        'edges': ['0 a 1', '1 a 2', '2 a 0']
        , 'cnf': grammars[2]
        , 'expected': set(product({0, 1, 2}, {0, 1, 2}))
    }
    ,{
        'edges': ['0 a 1', '1 a 2', '2 a 3', '3 a 0', '3 b 4', '4 b 3']
        , 'cnf': grammars[0]
        , 'expected': {(3, 3), (0, 4), (1, 3), (2, 4)} | {(i, i) for i in range(5)}
    }
    ,{
        'edges': ['0 a 1', '1 b 2']
        , 'cnf': grammars[3]
        , 'expected': {(0, 2)}
    }
])
def manual_suite(request):
    return request.param

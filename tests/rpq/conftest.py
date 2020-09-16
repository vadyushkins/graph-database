import random
from itertools import product

import networkx
import pytest

random.seed(42)

graphs = [
    ['0 a 0']
    , ['0 a 1', '1 b 2', '1 c 2']
    , ['0 a 1', '1 a 0', '1 b 2', '2 b 3', '3 b 1']
    , ['0 a 1', '1 a 2']
]

regexes = [
    '(a*)'
    , '(a)(b*)(c*)'
    , '(a|b)*'
    , '(a)(a)'
]


@pytest.fixture(scope='session', params=[
    {
        'edges': edges
        , 'regex': regex
    }
    for edges, regex in product(graphs, regexes)
])
def manual_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {'n': n, 'm': random.randint(1, n * (n - 1) // 2 // 2), 'r': r}
    for n in range(4, 10)
    for r in ['(a)(a)', '(a|b)*', '(a)(a|b)(c)']
])
def automatic_suite(request):
    n, m, r = request.param.values()

    random_graph = networkx.gnm_random_graph(n, m, seed=42, directed=True)

    return {
        'edges': [
            f'{i} {"abc"[random.randint(0, 2)]} {j}'
            for i, j in random_graph.edges
        ]
        , 'regex': r
    }

import os
import random

import networkx
import pytest
from pyformlang.regular_expression import Regex

from src.graph.LabeledGraph import LabeledGraph
from src.graph.RegexGraph import RegexGraph

cwd = os.path.join(os.getcwd(), 'tests/rpq/suites')
suites = filter(lambda path: path.startswith('test'), os.listdir(cwd))


@pytest.fixture(scope='function', params=suites)
def suite(request):
    suite = request.param
    suite_dir = f'{cwd}/{suite}/'

    graph = suite_dir + 'graph.txt'
    regex = suite_dir + 'regex.txt'
    intersection = suite_dir + 'intersection.txt'
    closure = suite_dir + 'closure.txt'
    rpq = suite_dir + 'rpq.txt'

    return {
        'graph': graph
        , 'regex': regex
        , 'intersection': intersection
        , 'closure': closure
        , 'rpq': rpq
    }


@pytest.fixture(scope='function', params=[
    {
        'graph': n
        , 'edges': m
        , 'regex': r
    }
    for r in ['(a*)', '(a|b)*', '(a|b|c)*']
    for n in range(1, 10)
    for m in [n * (n - 1) // 2 // 100 * p for p in [25, 50, 75, 100]]
])
def automatic_suite(request):
    n = request.param['graph']
    m = request.param['edges']

    graph = networkx.gnm_random_graph(n, m, seed=42, directed=True)

    g = LabeledGraph(n)
    r = RegexGraph(Regex(request.param['regex']))

    random.seed(42)

    for i, j in graph.edges:
        g[chr(ord('a') + random.randint(0, 2))][i, j] = True

    return {
        'graph': g
        , 'regex': r
    }

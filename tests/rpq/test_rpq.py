from pygraphblas import *

from src.algo.rpq import get_intersection, transitive_closure, rpq
from src.graph.Graph import Graph
from src.graph.LabeledGraph import LabeledGraph
from src.graph.RegexGraph import RegexGraph


def test_graph_reading(suite):
    lg = LabeledGraph.from_txt(suite['graph'])
    g = Graph.from_txt(suite['graph'])

    def check():
        for v, to in g:
            for label in g[v, to]:
                if lg[label][v, to] is not True:
                    return False
        return True

    assert check()


def test_intersection(suite):
    g = LabeledGraph.from_txt(suite['graph'])
    r = RegexGraph.from_regex_in_txt(suite['regex'])

    def get_checksums(graph: LabeledGraph):
        res = dict()
        for label in graph:
            res[label] = graph[label].nvals
        return res

    actual = get_checksums(get_intersection(g, r))

    expected = get_checksums(LabeledGraph.from_txt(suite['intersection']))

    assert expected == actual


def test_transitive_closure(suite):
    g = LabeledGraph.from_txt(suite['graph'])

    actual = Matrix.sparse(BOOL, g.matrices_size, g.matrices_size)

    for label in g:
        actual += g[label]

    tmp = transitive_closure(actual)
    actual = tmp

    expected = LabeledGraph.from_txt(suite['closure'])['test_transitive_closure']

    assert expected.iseq(actual)


def test_rpq(suite):
    g = LabeledGraph.from_txt(suite['graph'])
    r = RegexGraph.from_regex_in_txt(suite['regex'])

    actual = rpq(g, r)

    def read_reachabilities(path):
        res = Matrix.sparse(BOOL, g.matrices_size, g.matrices_size)
        with open(path, 'r') as f:
            for line in f:
                v, to, reachability = line.split()
                res[int(v), int(to)] = bool(reachability)
        return res

    expected = read_reachabilities(suite['rpq'])

    assert expected.iseq(actual)


def test_execute_rpq(automatic_suite):
    g = automatic_suite['graph']
    r = automatic_suite['regex']

    actual = rpq(g, r)

    paths = dict()

    for label in g:
        for i, j, _ in zip(*g[label].to_lists()):
            if (i, j) not in paths:
                paths[i, j] = set()
            paths[i, j].add(label)

    for k in range(g.matrices_size):
        for i in range(g.matrices_size):
            for j in range(g.matrices_size):
                if ((i, k) in paths) and ((k, j) in paths):
                    if (i, j) not in paths:
                        paths[i, j] = set()
                    cur = set()
                    for left in paths[i, k]:
                        for right in paths[k, j]:
                            cur.add(left + right)
                    paths[i, j] |= cur

    def check():
        for i, j, _ in zip(*actual.to_lists()):
            accepts = False
            for path in paths[i, j]:
                if r.accepts(path):
                    accepts = True
            if accepts is False:
                return False
        return True

    assert check()

from itertools import product

from pygraphblas import *

from src.LabeledGraph import LabeledGraph
from src.RegularPathQuering import rpq


def test_manual(manual_suite, tmp_path):
    assert check(manual_suite['edges'], manual_suite['regex'], tmp_path)


def test_automatic(automatic_suite, tmp_path):
    assert check(automatic_suite['edges'], automatic_suite['regex'], tmp_path)


def check(edges, regex, tmp_path):
    graph_file = tmp_path / 'graph.txt'
    graph_file.write_text('\n'.join(edges))

    regex_file = tmp_path / 'regex.txt'
    regex_file.write_text(regex)

    g = LabeledGraph.from_txt(graph_file)
    r = LabeledGraph.from_regex(regex_file)

    paths = dict()

    actual = rpq(g, r)

    for label in g.labels:
        for i, j, _ in zip(*g[label].select(lib.GxB_NONZERO).to_lists()):
            if (i, j) not in paths:
                paths[i, j] = set()
            paths[i, j].add(label)

    for k in range(g.size):
        for i in range(g.size):
            for j in range(g.size):
                if ((i, k) in paths) and ((k, j) in paths):
                    if (i, j) not in paths:
                        paths[i, j] = set()
                    paths[i, j] |= set(map(lambda s: s[0] + s[1], product(paths[i, k], paths[k, j])))

    expected = Matrix.sparse(BOOL, g.size, g.size)
    for i in range(g.size):
        for j in range(g.size):
            if (i, j) in paths:
                for path in paths[i, j]:
                    if r.accepts(path):
                        expected[i, j] = True
                        break

    return expected.iseq(actual)

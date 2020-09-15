from pygraphblas import *

from src.graph.LabeledGraph import LabeledGraph
from src.graph.RegexGraph import RegexGraph


def get_intersection(g: LabeledGraph, r: LabeledGraph) -> LabeledGraph:
    res = LabeledGraph(g.matrices_size * r.matrices_size)

    tmp = Matrix.sparse(BOOL, res.matrices_size, res.matrices_size)
    for label in g:
        g[label].kronecker(r[label], out=tmp)
        res[label] += tmp

    return res


def transitive_closure(m: Matrix) -> Matrix:
    res = m.dup()

    changed = True
    while changed:
        changed = False

        old_nnz = res.nvals
        res += res @ res
        new_nnz = res.nvals

        if new_nnz != old_nnz:
            changed = True

    return res


def rpq(g: LabeledGraph, r: LabeledGraph):
    k = get_intersection(g, r)

    m = Matrix.sparse(BOOL, k.matrices_size, k.matrices_size)
    for label in k:
        m += k.matrices[label]

    tc = transitive_closure(m)
    tc.select(lib.GxB_NONZERO)

    def get_coordinates(i, n):
        return i // n, i % n

    ans = Matrix.sparse(BOOL, g.matrices_size, g.matrices_size)

    for i, j, _ in zip(*tc.to_lists()):
        v = get_coordinates(i, r.matrices_size)[0]
        to = get_coordinates(j, r.matrices_size)[0]
        ans[v, to] = True

    return ans


def execute_rpq(args, verbose=False):
    g = LabeledGraph.from_txt(args.graph)
    r = RegexGraph.from_regex_in_txt(args.query)

    res = rpq(g, r)

    def read_vertices(path):
        res = set()
        with open(path, 'r') as f:
            for line in f:
                vertices = line.split()
                for v in vertices:
                    res.add(int(v))
        return res

    src = range(g.matrices_size) if args.sources is None else read_vertices(args.sources)
    dst = range(g.matrices_size) if args.destinations is None else read_vertices(args.destinations)

    ans = list()

    for i, j, _ in zip(*res.to_lists()):
        if (i in src) and (j in dst):
            ans.append((i, j))

    ans.sort()

    if verbose:
        for i, j in ans:
            print(f'{j} reachable from {i}')

    return ans

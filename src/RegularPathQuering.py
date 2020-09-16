from pygraphblas import *

from src.LabeledGraph import LabeledGraph


def rpq(g: LabeledGraph, r: LabeledGraph) -> Matrix:
    kron = g.get_intersection(r)

    tc = Matrix.sparse(BOOL, kron.size, kron.size)
    for label in kron.labels:
        tc += kron[label]

    while True:
        prev = tc.nvals
        tc += tc @ tc
        if prev == tc.nvals:
            break

    ans = Matrix.sparse(BOOL, g.size, g.size)
    for i, j, _ in zip(*tc.select(lib.GxB_NONZERO).to_lists()):
        i_g, i_r = i // r.size, i % r.size
        j_g, j_r = j // r.size, j % r.size
        if (i_g in g.start_states) and (i_r in r.start_states):
            if (j_g in g.final_states) and (j_r in r.final_states):
                ans[i_g, j_g] = True

    return ans


def execute_rpq(args, verbose=False):
    g = LabeledGraph.from_txt(args.graph)
    r = LabeledGraph.from_regex(args.query)

    res = rpq(g, r)

    srcs = None
    if args.sources is not None:
        with open(args.sources, 'r') as f:
            srcs = list(map(int, f.readline().split()))

    dsts = None
    if args.destinations is not None:
        with open(args.destinations, 'r') as f:
            dsts = list(map(int, f.readline().split()))

    ans = list()

    for i, j, _ in zip(*res.select(lib.GxB_NONZERO).to_lists()):
        if (srcs is None) or (i in srcs):
            if (dsts is None) or (j in dsts):
                ans.append((i, j))

    ans.sort()

    if verbose:
        for i, j in ans:
            print(f'{j} reachable from {i}')

    return ans

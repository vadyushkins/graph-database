from pyformlang.cfg import *
from pygraphblas import *

from src.LabeledGraph import LabeledGraph
from src.MyCNF import MyCNF


def cfpq(g: LabeledGraph, gr: MyCNF) -> Matrix:
    cur = LabeledGraph(g.size)

    variables_for_edge = dict()
    edges_for_variable = dict()

    for variable in gr.variables:
        cur[variable] = Matrix.sparse(BOOL, g.size, g.size)

    for label in g.labels:
        cur[Terminal(label)] = g[label].dup()

        for i, j, k in zip(*cur[Terminal(label)].select(lib.GxB_NONZERO).to_lists()):
            variables_for_edge[(i, j)] = variables_for_edge.get((i, j), set()) | {Terminal(label)}
            edges_for_variable[Terminal(label)] = edges_for_variable.get(Terminal(label), set()) | {(i, j)}

    if gr.generate_epsilon() is True:
        for i in range(g.size):
            cur[gr.start_symbol][i, i] = True
            variables_for_edge[(i, i)] = variables_for_edge.get((i, i), set()) | {gr.start_symbol}
            edges_for_variable[gr.start_symbol] = edges_for_variable.get(gr.start_symbol, set()) | {(i, i)}

    for p in gr.productions:
        if len(p.body) == 1:
            for i, j in edges_for_variable.get(p.body[0], set()):
                if (i, j) not in edges_for_variable.get(p.head, set()):
                    edges_for_variable[p.head] = edges_for_variable.get(p.head, set()) | {(i, j)}
                    variables_for_edge[(i, j)] = variables_for_edge.get((i, j), set()) | {p.head}
                    cur[p.head][i, j] = True

    changing = True
    while changing:
        changing = False
        for p in gr.productions:
            if len(p.body) == 2:
                for i, k in edges_for_variable.get(p.body[0], set()):
                    for l, j in edges_for_variable.get(p.body[1], set()):
                        if k == l:
                            if (i, j) not in edges_for_variable.get(p.head, set()):
                                changing = True
                                edges_for_variable[p.head] = edges_for_variable.get(p.head, set()) | {(i, j)}
                                variables_for_edge[(i, j)] = variables_for_edge.get((i, j), set()) | {p.head}
                                cur[p.head][i, j] = True

    return cur[gr.start_symbol]

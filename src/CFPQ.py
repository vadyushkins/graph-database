from abc import ABC, abstractmethod
from typing import AbstractSet

from pyformlang.cfg import *
from pygraphblas import *

from src.LabeledGraph import LabeledGraph
from src.MyCNF import MyCNF


class CFPQ(ABC):
    @classmethod
    @abstractmethod
    def cfpq(cls, g: LabeledGraph, gr: MyCNF) -> AbstractSet:
        pass


class Hellings(CFPQ):
    @classmethod
    def cfpq(cls, g: LabeledGraph, gr: MyCNF) -> AbstractSet:
        edges_for_variable = dict()

        for v in gr.variables:
            edges_for_variable[v] = set()

        for t in gr.terminals | set(map(Terminal, g.labels)):
            edges_for_variable[t] = set()

        for label in g.labels:
            for i, j in zip(*g[label].to_lists()[:2]):
                edges_for_variable[Terminal(label)].add((i, j))

        if gr.generate_epsilon() is True:
            for i in range(g.size):
                edges_for_variable[gr.start_symbol].add((i, i))

        for p in gr.unit_productions:
            for e in edges_for_variable[p.body[0]]:
                edges_for_variable[p.head].add(e)

        changing = True
        while changing:
            changing = False
            for p in gr.pair_productions:
                new = set()
                for i, k in edges_for_variable[p.body[0]]:
                    for _, j in filter(lambda x: x[0] == k, edges_for_variable[p.body[1]]):
                        if (changing is not True) and ((i, j) not in edges_for_variable[p.head]):
                            changing = True
                        new.add((i, j))
                edges_for_variable[p.head] |= new

        return edges_for_variable[gr.start_symbol]


class Azimov(CFPQ):
    @classmethod
    def cfpq(cls, g: LabeledGraph, gr: MyCNF) -> AbstractSet:
        m = LabeledGraph(g.size)
        for p in gr.unit_productions:
            m[p.head] += g[p.body[0].value]

        if gr.generate_epsilon():
            for i in range(g.size):
                m[gr.start_symbol][i, i] = True

        changing = True
        while changing:
            changing = False
            for p in gr.pair_productions:
                prev = m[p.head].nvals
                m[p.head] += m[p.body[0]] @ m[p.body[1]]
                if (changing is False) and (prev != m[p.head].nvals):
                    changing = True

        return set(zip(*m[gr.start_symbol].to_lists()[:2]))


class Tensor(CFPQ):
    @classmethod
    def cfpq(cls, g: LabeledGraph, gr: MyCNF) -> AbstractSet:
        rsm = LabeledGraph(2 * len(gr.unit_productions) + 3 * len(gr.pair_productions))

        cur = 0
        production_for_reachability = dict()
        for p in gr.unit_productions:
            rsm.start_states.add(cur)
            rsm.final_states.add(cur + 1)
            production_for_reachability[(cur, cur + 1)] = p
            rsm[p.body[0].value][cur, cur + 1] = True
            cur += 2
        for p in gr.pair_productions:
            rsm.start_states.add(cur)
            rsm.final_states.add(cur + 2)
            production_for_reachability[(cur, cur + 2)] = p
            rsm[p.body[0]][cur, cur + 1] = True
            rsm[p.body[1]][cur + 1, cur + 2] = True
            cur += 3

        m = g.dup()

        tc = m.get_intersection(rsm).get_transitive_closure()

        while True:
            prev = tc.nvals
            for i, j, _ in zip(*tc.select(lib.GxB_NONZERO).to_lists()):
                i_m, i_rsm = i // rsm.size, i % rsm.size
                j_m, j_rsm = j // rsm.size, j % rsm.size
                if (i_m in m.start_states) and (i_rsm in rsm.start_states):
                    if (j_m in m.final_states) and (j_rsm in rsm.final_states):
                        m[production_for_reachability[(i_rsm, j_rsm)].head][i_m, j_m] = True

            tc = m.get_intersection(rsm).get_transitive_closure()
            if prev == tc.nvals:
                break

        ans = set(zip(*m[gr.start_symbol].to_lists()[:2]))

        if gr.generate_epsilon():
            ans |= {(i, i) for i in range(g.size)}

        return ans

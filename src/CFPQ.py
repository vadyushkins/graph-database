from abc import ABC, abstractmethod
from typing import AbstractSet

from pyformlang.cfg import *

from src.LabeledGraph import LabeledGraph
from src.MyCNF import MyCNF


class CFPQ(ABC):
    @classmethod
    @abstractmethod
    def cfpq(cls, graph: LabeledGraph, grammar: MyCNF) -> AbstractSet:
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

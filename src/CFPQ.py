from abc import ABC, abstractmethod
from typing import AbstractSet

from pyformlang.cfg import *

from src.LabeledGraph import LabeledGraph
from src.MyCNF import MyCNF
from src.RecursiveStateMachine import RecursiveStateMachine
from src.Utils import *


class CFPQ(ABC):
    def __init__(self, path_to_graph: str, path_to_grammar: str):
        self.path_to_graph: str = path_to_graph
        self.path_to_grammar: str = path_to_grammar
        self.graph: LabeledGraph = LabeledGraph.from_txt(self.path_to_graph)
        self.rsm: RecursiveStateMachine = RecursiveStateMachine.from_txt(self.path_to_grammar)
        self.cfg: CFG = self.rsm.to_cfg()
        self.cnf: MyCNF = self.rsm.to_mycnf()

    @abstractmethod
    def cfpq(self) -> AbstractSet:
        pass


class Hellings(CFPQ):
    def cfpq(self) -> AbstractSet:
        edges_for_variable = dict()

        for v in self.cnf.variables:
            edges_for_variable[v] = set()

        for t in self.cnf.terminals | set(map(Terminal, self.graph.labels)):
            edges_for_variable[t] = set()

        for label in self.graph.labels:
            for i, j in zip(*self.graph[label].to_lists()[:2]):
                edges_for_variable[Terminal(label)].add((i, j))

        if self.cnf.generate_epsilon() is True:
            for i in range(self.graph.size):
                edges_for_variable[self.cnf.start_symbol].add((i, i))

        for p in self.cnf.unit_productions:
            for e in edges_for_variable[p.body[0]]:
                edges_for_variable[p.head].add(e)

        changing = True
        while changing:
            changing = False
            for p in self.cnf.pair_productions:
                new = set()
                for i, k in edges_for_variable[p.body[0]]:
                    for _, j in filter(lambda x: x[0] == k, edges_for_variable[p.body[1]]):
                        if (changing is not True) and ((i, j) not in edges_for_variable[p.head]):
                            changing = True
                        new.add((i, j))
                edges_for_variable[p.head] |= new

        return edges_for_variable[self.cnf.start_symbol]


class Azimov(CFPQ):
    def cfpq(self) -> AbstractSet:
        m = LabeledGraph(self.graph.size)
        for p in self.cnf.unit_productions:
            m[p.head] += self.graph[p.body[0].value]

        if self.cnf.generate_epsilon():
            for i in range(self.graph.size):
                m[self.cnf.start_symbol][i, i] = True

        changing = True
        while changing:
            changing = False
            for p in self.cnf.pair_productions:
                prev = m[p.head].nvals
                m[p.head] += m[p.body[0]] @ m[p.body[1]]
                if (changing is False) and (prev != m[p.head].nvals):
                    changing = True

        return set(zip(*m[self.cnf.start_symbol].to_lists()[:2]))


class TensorWithCNF(CFPQ):
    def cfpq(self) -> AbstractSet:
        m = self.graph.dup()
        rsm = LabeledGraph(
            sum(
                len(p.body) + 1
                for p in self.cnf.productions
            )
        )

        cur = 0
        production_for_reachability = dict()
        for p in self.cnf.productions:
            rsm.start_states.add(cur)
            production_for_reachability[(cur, cur + len(p.body))] = p.head
            if len(p.body) == 0:
                for i in m.vertices:
                    m[p.head][i, i] = True
            for b in p.body:
                if isinstance(b, Terminal):
                    rsm[b.value][cur, cur + 1] = True
                else:
                    rsm[b][cur, cur + 1] = True
                cur += 1
            rsm.final_states.add(cur)
            cur += 1

        tc = m.get_intersection(rsm).get_transitive_closure()

        while True:
            prev = tc.nvals
            for i, j, _ in zip(*tc.select(lib.GxB_NONZERO).to_lists()):
                i_m, i_rsm = i // rsm.size, i % rsm.size
                j_m, j_rsm = j // rsm.size, j % rsm.size
                if (i_m in m.start_states) and (i_rsm in rsm.start_states):
                    if (j_m in m.final_states) and (j_rsm in rsm.final_states):
                        m[production_for_reachability[(i_rsm, j_rsm)]][i_m, j_m] = True

            tmp = m.get_intersection(rsm)
            for label in tmp.labels:
                tc += tmp[label]
            tc = transitive_closure(tc)

            if prev == tc.nvals:
                break

        ans = set(zip(*m[self.cnf.start_symbol].to_lists()[:2]))

        return ans


class TensorWithRSM(CFPQ):
    def cfpq(self) -> AbstractSet:
        m = self.graph.dup()
        rsm = LabeledGraph(
            sum(
                len(box.states)
                for x in self.rsm.boxes
                for box in self.rsm.boxes[x]
            )
        )

        cnt = 0
        production_for_reachability = dict()
        for x in self.rsm.boxes:
            for box in self.rsm.boxes[x]:
                name = dict()
                for s in box.states:
                    if s not in name:
                        name[s] = cnt
                        cnt += 1
                    if s in box.final_states:
                        rsm.final_states.add(name[s])
                rsm.start_states.add(name[box.start_state])
                if box.start_state in box.final_states:
                    for i in m.vertices:
                        m[Variable(x)][i, i] = True
                for s in box.final_states:
                    production_for_reachability[(name[box.start_state], name[s])] = Variable(x)
                for v in box._transition_function._transitions:
                    for label in box._transition_function._transitions[v]:
                        to = box._transition_function._transitions[v][label]

                        if label.value == label.value.lower():
                            rsm[label.value][name[v], name[to]] = True
                        else:
                            rsm[Variable(label.value)][name[v], name[to]] = True

        tc = m.get_intersection(rsm).get_transitive_closure()

        while True:
            prev = tc.nvals
            for i, j, _ in zip(*tc.select(lib.GxB_NONZERO).to_lists()):
                i_m, i_rsm = i // rsm.size, i % rsm.size
                j_m, j_rsm = j // rsm.size, j % rsm.size
                if (i_m in m.start_states) and (i_rsm in rsm.start_states):
                    if (j_m in m.final_states) and (j_rsm in rsm.final_states):
                        m[production_for_reachability[(i_rsm, j_rsm)]][i_m, j_m] = True

            tmp = m.get_intersection(rsm)
            for label in tmp.labels:
                tc += tmp[label]
            tc = transitive_closure(tc)

            if prev == tc.nvals:
                break

        ans = set(zip(*m[self.rsm.start_symbol].to_lists()[:2]))

        return ans

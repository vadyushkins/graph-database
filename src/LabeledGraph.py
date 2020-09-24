from itertools import product

from pyformlang import *
from pygraphblas import *


class LabeledGraph:
    def __init__(self, size: int):
        self.size = size
        self.vertices = set(range(size))
        self.labels = set()
        self.matrices = dict()
        self.start_states = set()
        self.final_states = set()

    def __getitem__(self, item: str) -> Matrix:
        if item not in self.matrices:
            self.matrices[item] = Matrix.sparse(BOOL, self.size, self.size)
            self.labels.add(item)
        return self.matrices[item]

    def __setitem__(self, key: str, value: Matrix):
        self.labels.add(key)
        self.matrices[key] = value

    def accepts(self, word: str):
        nfa = finite_automaton.EpsilonNFA(
            states=self.vertices,
            input_symbols=self.labels,
            start_state=self.start_states,
            final_states=self.final_states
        )

        for label in self.labels:
            for i, j, _ in zip(*self[label].select(lib.GxB_NONZERO).to_lists()):
                nfa.add_transition(i, label, j)

        return nfa.accepts(word)

    def get_transitive_closure(self) -> Matrix:
        res = Matrix.sparse(BOOL, self.size, self.size)

        for label in self.labels:
            res += self[label]

        while True:
            prev = res.nvals
            res += res @ res
            if prev == res.nvals:
                break

        return res

    def get_intersection(self, other):
        kron = LabeledGraph(self.size * other.size)

        tmp = Matrix.sparse(BOOL, kron.size, kron.size)
        for label in self.labels:
            self[label].kronecker(other[label], out=tmp)
            kron[label] += tmp

        kron.start_states = set(map(lambda x: x[0] * other.size + x[1], product(self.start_states, other.start_states)))
        kron.final_states = set(map(lambda x: x[0] * other.size + x[1], product(self.final_states, other.final_states)))

        return kron

    def __and__(self, other):
        if not isinstance(other, LabeledGraph):
            raise NotImplementedError
        return self.get_intersection(LabeledGraph)

    def print(self, prefix=None):
        print()
        for label in self:
            print(f'{prefix}: Label {label}, matrix[label]: {self.matrices[label].to_lists()}')
        print(f'{prefix}: start_states: {self.start_states}')
        print(f'{prefix}: final_states: {self.final_states}')

    @classmethod
    def from_txt(cls, path):
        vertices = set()
        edges = set()

        with open(path, 'r') as f:
            for line in f:
                v, label, to = line.split()
                v, to = int(v), int(to)
                vertices |= {v, to}
                edges.add((v, label, to))

        g = LabeledGraph(max(vertices) + 1)

        for v, label, to in edges:
            g[label][v, to] = True
        g.vertices = g.start_states = g.final_states = vertices

        return g

    @classmethod
    def from_regex(cls, path):
        with open(path, 'r') as f:
            regex = f.readline().replace('\n', '')

        r = regular_expression.Regex(regex).to_epsilon_nfa().to_deterministic().minimize()

        num = dict()
        for s in r.states:
            if s not in num:
                num[s] = len(num)

        edges = sorted(
            [
                (num[v], str(label), num[to])
                for v, label, to in r._transition_function.get_edges()
            ]
            , key=lambda t: (t[1], t[0], t[2])
        )

        g = LabeledGraph(len(r.states))
        for v, label, to in edges:
            g[label][v, to] = True
        g.vertices = set(num.values())
        g.start_states = set(map(num.get, r.start_states))
        g.final_states = set(map(num.get, r.final_states))

        return g

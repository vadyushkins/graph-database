from pygraphblas.matrix import Matrix
from pygraphblas.types import BOOL

from src.config import MAX_MATRICES_SIZE
from src.graph.Graph import Graph


class LabeledGraph(Graph):
    def __init__(self, matrices_size=MAX_MATRICES_SIZE):
        super().__init__()
        self.matrices = dict()
        self.matrices_size = matrices_size

    def __getitem__(self, item: str) -> Matrix:
        if item not in self.matrices:
            self.matrices[item] = Matrix.sparse(BOOL, self.matrices_size, self.matrices_size)
        return self.matrices[item]

    def __setitem__(self, key, value):
        self.matrices[key] = value

    def __iter__(self):
        return self.matrices.__iter__()

    def iseq(self, other):
        if not isinstance(other, LabeledGraph):
            return False
        for label in self.matrices:
            if self.matrices[label].to_lists() != other.matrices[label].to_lists():
                return False
        return True

    def print(self, prefix=None):
        print()
        for label in self.matrices:
            print(f'{prefix}: Label {label}, matrix[label]: {self.matrices[label].to_lists()}')

    @classmethod
    def from_txt(cls, path):
        g = LabeledGraph(_get_graph_size(path))
        with open(path, 'r') as f:
            for line in f:
                v, label, to = g.append(line)
                g[label][int(v), int(to)] = True
        return g


def _get_graph_size(path):
    res = -1
    with open(path, 'r') as f:
        for line in f:
            v, _, to = line.split()
            res = max(res, int(v), int(to))
    return res + 1

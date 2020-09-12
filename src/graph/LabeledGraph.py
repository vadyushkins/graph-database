from pygraphblas.matrix import Matrix
from pygraphblas.types import BOOL


class LabeledGraph:
    def __init__(self, matrices_size=int(1e6)):
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

    @classmethod
    def from_txt(cls, path):
        g = LabeledGraph(_get_graph_size(path))
        with open(path, 'r') as f:
            for line in f:
                v, l, u = line.split()
                g[l][int(v), int(u)] = True
        return g


def _get_graph_size(path):
    res = -1
    with open(path, 'r') as f:
        for line in f:
            v, _, u = line.split()
            res = max(res, int(v), int(u))
    return res + 1
class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = list()

    def __getitem__(self, item: str) -> bool:
        return item in self.edges

    def append(self, other: str):
        v, l, u = other.split()
        v = int(v)
        u = int(u)

        self.vertices.add(v)
        self.vertices.add(u)
        self.edges.append((v, l, u))

    def __iter__(self):
        return self.edges.__iter__()

    @classmethod
    def from_txt(cls, path):
        g = Graph()
        with open(path, 'r') as f:
            for line in f:
                g.append(line)
        return g


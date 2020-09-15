class Graph:
    def __init__(self):
        self.vertices = dict()
        self.labels = dict()
        self.edges = dict()

    def __getitem__(self, item):
        return self.edges[item]

    def append(self, other: str, compress=False):
        v, label, to = other.split()

        def get_num(x, d):
            if x not in d:
                d[x] = len(d)
            return d[x]

        get_num(v, self.vertices)
        get_num(label, self.labels)
        get_num(to, self.vertices)

        if compress:
            v = get_num(v, self.vertices)
            to = get_num(to, self.vertices)
        else:
            v = int(v)
            to = int(to)

        if (v, to) not in self.edges:
            self.edges[v, to] = []

        self.edges[v, to].append(label)

        return v, label, to

    def __iter__(self):
        return self.edges.__iter__()

    @classmethod
    def from_txt(cls, path):
        g = Graph()
        with open(path, 'r') as f:
            for line in f:
                g.append(line)
        return g

from src.graph.LabeledGraph import LabeledGraph
from src.graph.Graph import Graph


def test_graph_reading(graph):
    lg = LabeledGraph.from_txt(graph)
    g = Graph.from_txt(graph)

    def check():
        for v, l, u in g:
            if lg[l][v, u] is not True:
                return False
            if max(g.vertices) + 1 != lg.matrices_size:
                return False
        return True

    assert check()
import pytest
import os


@pytest.fixture(scope='session')
def graph():
    cwd = os.getcwd()
    graphs_dir = os.path.join(cwd, 'graphs')
    graphs = os.listdir(graphs_dir)
    for graph in graphs:
        yield os.path.join(graphs_dir, graph)
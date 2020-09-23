import os
import shutil
from glob import glob
from pathlib import Path

import pytest
from pygraphblas import *

from src.LabeledGraph import LabeledGraph

cwd = './benchmarks/benchmark_rpq'
data_for_rpq_dir = cwd + '/myDataForRPQ'


class LabeledGraphWithLinearTransitiveClosure(LabeledGraph):
    def get_transitive_closure(self) -> Matrix:
        res = Matrix.sparse(BOOL, self.size, self.size)

        for label in self.labels:
            res += self[label]

        tmp = res.dup()
        for i in range(self.size):
            res += res @ tmp

        return res


class LabeledGraphWithSelectTransitiveClosure(LabeledGraph):
    def get_transitive_closure(self) -> Matrix:
        res = Matrix.sparse(BOOL, self.size, self.size)

        for label in self.labels:
            res += self[label]

        while True:
            prev = res.nvals
            res += res @ res
            res.select(lib.GxB_NONZERO)
            if prev == res.nvals:
                break

        return res


if not os.path.exists(data_for_rpq_dir):
    os.mkdir(data_for_rpq_dir)
    shutil.unpack_archive(data_for_rpq_dir + '.zip', cwd)

suites = [
    {
        'id': f'(impl={impl.__name__})(graph={Path(graph).stem})(regex={Path(regex).stem})'
        , 'impl': impl
        , 'impl_name': impl.__name__
        , 'graph': graph
        , 'graph_name': Path(graph).stem
        , 'regex': regex
        , 'regex_name': Path(regex).stem
    }
    for impl in [
        LabeledGraph
        , LabeledGraphWithLinearTransitiveClosure
        , LabeledGraphWithSelectTransitiveClosure
    ]
    for graph in glob(f'{data_for_rpq_dir}/*/*.txt')
    for regex in glob(f'{data_for_rpq_dir}/{Path(graph).stem}/regexes/*')
]

params = [
    pytest.param(
        {'impl': x['impl'], 'name': x['impl_name']}
        , {'graph': x['graph'], 'name': x['graph_name']}
        , {'regex': x['regex'], 'name': x['regex_name']}
        , marks=[
            getattr(pytest.mark, x['impl_name'])
            , getattr(pytest.mark, x['graph_name'])
            , getattr(pytest.mark, x['regex_name'])
        ]
        , id=x['id']
    )
    for x in suites
]


def pytest_configure(config):
    for param in params:
        for mark in param.marks:
            config.addinivalue_line('markers', f'{mark}: generated marker')

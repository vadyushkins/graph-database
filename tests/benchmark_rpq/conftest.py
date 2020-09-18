import os
import shutil
from glob import glob

from pygraphblas import *

import pytest

from src.LabeledGraph import LabeledGraph

cwd = './tests/benchmark_rpq'
data_for_rpq_dir = cwd + '/dataForRPQ'


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

    for suite in os.listdir(data_for_rpq_dir):
        suite_path = data_for_rpq_dir + f'/{suite}'
        if not suite.startswith('LUBM'):
            shutil.unpack_archive(suite_path, data_for_rpq_dir)

suite_paths = list(map(
    lambda path: data_for_rpq_dir + f'/{path}',
    filter(
        lambda path: not path.endswith('.tar.gz'),
        os.listdir(data_for_rpq_dir)
    )
))

suites = [
    {
        'id': f'impl={impl.__name__}-graph={os.path.basename(suite_path)}-regex={"/".join(regex.split("/")[-2:])}'
        , 'impl': impl
        , 'impl_name': impl.__name__
        , 'graph': suite_path + f'/{os.path.basename(suite_path)}.txt'
        , 'graph_name': os.path.basename(suite_path)
        , 'regex': regex
        , 'regex_name': "_in_".join(regex.split("/")[-2:])
    }
    for impl in [
        LabeledGraph
        , LabeledGraphWithLinearTransitiveClosure
        , LabeledGraphWithSelectTransitiveClosure
    ]
    for suite_path in suite_paths
    for regex in glob(f'{suite_path}/queries/*/*')
]

params = [
    pytest.param(
        x['impl']
        , x['graph']
        , x['regex']
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

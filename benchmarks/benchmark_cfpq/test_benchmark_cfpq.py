import csv
import os
import time
from pathlib import Path

import pytest
from conftest import params


@pytest.mark.parametrize('algo,graph,grammar', params)
def test_benchmark_rpq(algo, graph, grammar):
    algo_name = algo['name']
    g_name = graph['name']
    g_filename = Path(graph['graph']).stem
    r_name = grammar['name']

    result_file = f'{g_name}.csv'
    result_file_path = f'./benchmarks/benchmark_cfpq/results/{result_file}'

    headers = [
        'Algorithm'
        , 'Graph'
        , 'Graph filename'
        , 'Grammar'
        , 'Time (in microseconds)'
        , 'Control sum'
    ]

    if not os.path.exists(result_file_path):
        with open(result_file_path, mode='w+', newline='\n') as f:
            csv_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')
            csv_writer.writerow(headers)

    with open(result_file_path, mode='a+', newline='\n', buffering=1) as f:
        csv_writer = csv.writer(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')

        start_time = time.time_ns()
        res = algo['algo'](graph['graph'], grammar['grammar']).cfpq()
        end_time = time.time_ns()

        result_time = (end_time - start_time) // (10 ** 3)

        results = [algo_name, g_name, g_filename, r_name, result_time, len(res)]

        csv_writer.writerow(results)

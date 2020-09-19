from pathlib import Path

import pytest
import os
import csv
import time

from src.RegularPathQuering import rpq
from conftest import params


@pytest.mark.parametrize('impl,graph,regex', params)
def test_benchmark_rpq(impl, graph, regex):
    impl_name = impl['name']

    g = impl['impl'].from_txt(graph['graph'])
    g_name = graph['name']

    r = impl['impl'].from_regex(regex['regex'])
    r_name = regex['name']

    result_file = f'{g_name}.csv'
    result_file_path = f'./benchmarks/benchmark_rpq/results/{result_file}'

    append_headers = False
    if not os.path.exists(result_file_path):
        append_headers = True

    with open(result_file_path, mode='a+', newline='\n') as csv_f:
        csv_writer = csv.writer(csv_f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC, escapechar=' ')
        headers = [
            'Implementation'
            , 'Graph'
            , 'Regex'
            , 'Min time (in microseconds)'
            , 'Max time (in microseconds)'
            , 'Average time (in microseconds)'
        ]

        if append_headers:
            csv_writer.writerow(headers)

        times = []
        for i in range(5):
            start_time = time.time_ns()
            rpq(g, r)
            end_time = time.time_ns()

            times.append((end_time - start_time) // (10 ** 3))

        results = [impl_name, g_name, r_name, min(times), max(times), sum(times) / len(times)]

        csv_writer.writerow(results)
        print(results)

import pytest

from src.RegularPathQuering import rpq

from conftest import params


@pytest.mark.parametrize('impl,graph,regex', params)
def test_benchmark_rpq(impl, graph, regex, benchmark):
    g = impl.from_txt(graph)
    r = impl.from_regex(regex)

    benchmark.pedantic(rpq, (g, r), rounds=3, iterations=3, warmup_rounds=3)

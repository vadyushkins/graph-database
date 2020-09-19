import pytest

from src.RegularPathQuering import rpq

from .conftest import params


@pytest.mark.parametrize('impl,graph,regex', params)
def test_benchmark_rpq(impl, graph, regex, benchmark):
    g = impl.from_txt(graph)
    r = impl.from_regex(regex)

    benchmark.pedantic(rpq, (g, r), rounds=1, iterations=1, warmup_rounds=0)

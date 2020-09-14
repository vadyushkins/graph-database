import numpy as np
import pygraphblas as pg
import pytest


@pytest.fixture(scope='session', params=[i for i in range(42)])
def matrix_multiplication_suite(request):
    n = request.param

    a = np.random.randint(low=42, high=4242, size=(n, n), dtype=np.int64)
    b = np.random.randint(low=42, high=4242, size=(n, n), dtype=np.int64)
    exp = a.dot(b)

    def fill(dst, src):
        for i in range(n):
            for j in range(n):
                dst[i, j] = int(src[i][j])

    a_pg = pg.Matrix.sparse(pg.INT64, n, n)
    fill(dst=a_pg, src=a)

    b_pg = pg.Matrix.sparse(pg.INT64, n, n)
    fill(dst=b_pg, src=b)

    exp_pg = pg.Matrix.sparse(pg.INT64, n, n)
    fill(dst=exp_pg, src=exp)

    return {'left': a_pg, 'right': b_pg, 'expected': exp_pg}

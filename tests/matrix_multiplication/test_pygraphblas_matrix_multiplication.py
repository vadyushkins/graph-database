import pygraphblas as pg

def test_simple():
    a = pg.Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [1, 2, 3, 4],
        typ=pg.INT64,
    )
    b = pg.Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [5, 6, 7, 8],
        typ=pg.INT64,
    )

    actual = a @ b
    expected = pg.Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [19, 22, 43, 50],
        typ=pg.INT64
    )

    assert expected.iseq(actual)


def test_by_numpy(matrix_multiplication_suite):
    a = matrix_multiplication_suite['left']
    b = matrix_multiplication_suite['right']

    actual = a @ b

    expected = matrix_multiplication_suite['expected']

    assert expected.iseq(actual)
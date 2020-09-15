from pygraphblas import *


def test_simple():
    a = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [1, 2, 3, 4],
        typ=INT64,
    )
    b = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [5, 6, 7, 8],
        typ=INT64,
    )

    actual = a @ b

    expected = Matrix.from_lists(
        [0, 0, 1, 1],
        [0, 1, 0, 1],
        [19, 22, 43, 50],
        typ=INT64
    )

    assert expected.iseq(actual)


def test_by_numpy(matrix_multiplication_suite):
    a = matrix_multiplication_suite['left']
    b = matrix_multiplication_suite['right']

    actual = a @ b

    expected = matrix_multiplication_suite['expected']

    assert expected.iseq(actual)

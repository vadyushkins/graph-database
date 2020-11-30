from checker import check


def test_syntax(suite):
    assert check(suite) is True

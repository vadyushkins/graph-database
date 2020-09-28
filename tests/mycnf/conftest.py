import pytest

grammars = [
    'S -> a S b S\nS -> '
    , 'S -> a S b\nS -> '
    , 'S -> S S\nS -> a'
    , 'S -> A B\nA -> A A\nB -> B B\nA -> a\nB -> b'
]


@pytest.fixture(scope='session', params=grammars)
def automatic_suite(request):
    return request.param

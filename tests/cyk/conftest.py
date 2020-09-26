import pytest

from src.MyCNF import MyCNF

grammars = [
    'S -> a S b S\nS -> '
    , 'S -> a S b\nS -> '
    , 'S -> S S\nS -> a'
    , 'S -> A B\nA -> A a\nB -> b B\nA -> a\nB -> b'
]


@pytest.fixture(scope='session', params=[
    {
        'cnf': MyCNF.from_text(grammars[0])
        , 'accepted': 'aabbab'
    }
    ,{
        'cnf': MyCNF.from_text(grammars[1])
        , 'accepted': 'aabb'
    }
])
def accepted_manual_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cnf': MyCNF.from_text(grammars[0])
        , 'not accepted': 'aabcbab'
    }
    ,{
        'cnf': MyCNF.from_text(grammars[1])
        , 'not accepted': 'aacbb'
    }
])
def not_accepted_manual_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cnf': MyCNF.from_text(gr)
        , 'accepted': ''.join(map(lambda x: x.value, accepted))
    }
    for gr in grammars
    for accepted in MyCNF.from_text(gr).cfg.get_words(10)
])
def accepted_automatic_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cnf': MyCNF.from_text(gr)
        , 'not accepted': ''.join(map(lambda x: x.value, not_accepted)) + 'c'
    }
    for gr in grammars
    for not_accepted in MyCNF.from_text(gr).cfg.get_words(10)
])
def not_accepted_automatic_suite(request):
    return request.param

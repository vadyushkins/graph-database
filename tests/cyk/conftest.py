import pytest

from src.MyCNF import MyCNF

from pyformlang.cfg import *

grammars = [
    'S -> a S b S\nS -> '
    , 'S -> a S b\nS -> '
    , 'S -> S S\nS -> a'
    , 'S -> A B\nA -> A A\nB -> B B\nA -> a\nB -> b'
]


@pytest.fixture(scope='session', params=[
    {
        'cnf': MyCNF.from_text(grammars[0])
        , 'accepted': [Terminal(x) for x in 'aabbab']
    }
    ,{
        'cnf': MyCNF.from_text(grammars[1])
        , 'accepted': [Terminal(x) for x in 'aabb']
    }
])
def accepted_manual_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cnf': MyCNF.from_text(grammars[0])
        , 'not accepted': [Terminal(x) for x in 'aabcbab']
    }
    ,{
        'cnf': MyCNF.from_text(grammars[1])
        , 'not accepted': [Terminal(x) for x in 'aacbb']
    }
])
def not_accepted_manual_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cnf': MyCNF.from_text(gr)
        , 'accepted': accepted
    }
    for gr in grammars
    for accepted in CFG.from_text(gr).get_words(10)
])
def accepted_automatic_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cnf': MyCNF.from_text(gr)
        , 'not accepted': not_accepted + [Terminal('c')]
    }
    for gr in grammars
    for not_accepted in CFG.from_text(gr).get_words(10)
])
def not_accepted_automatic_suite(request):
    return request.param

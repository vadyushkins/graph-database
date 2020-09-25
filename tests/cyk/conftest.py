import pytest

from pyformlang.cfg import *

cfgs = [
    'S -> a S b S\nS -> '
    , 'S -> a S b\nS -> '
    , 'S -> S S\nS -> a'
    , 'S -> A B\nA -> A a\nB -> b B\nA -> a\nB -> b'
]


@pytest.fixture(scope='session', params=[
    {
        'cfg': CFG.from_text(cfgs[0]).to_normal_form()
        , 'accepted': list(map(lambda x: Terminal(x), 'aabbab'))
    }
    ,{
        'cfg': CFG.from_text(cfgs[1]).to_normal_form()
        , 'accepted': list(map(lambda x: Terminal(x), 'aabb'))
    }
])
def manual_suite_accepted(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cfg': CFG.from_text(cfgs[0]).to_normal_form()
        , 'not accepted': list(map(lambda x: Terminal(x), 'aba'))
    }
    ,{
        'cfg': CFG.from_text(cfgs[1]).to_normal_form()
        , 'not accepted': list(map(lambda x: Terminal(x), 'aaab'))
    }
])
def manual_suite_not_accepted(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cfg': CFG.from_text(cfg).to_normal_form()
        , 'accepted': accepted
    }
    for cfg in cfgs
    for accepted in CFG.from_text(cfg).get_words(4)
])
def automatic_suite_accepted(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cfg': CFG.from_text(cfg).to_normal_form()
        , 'not accepted': not_accepted + [Terminal('c')]
    }
    for cfg in cfgs
    for not_accepted in CFG.from_text(cfg).get_words(4)
])
def automatic_suite_not_accepted(request):
    return request.param

import pytest
from pyformlang.regular_expression import *


@pytest.fixture(scope='session', params=[
    {
        'r1': 'ab(b|c)'
        , 'r2': 'a(b|c)*'
        , 'exp': '(abb)|(abc)'
        , 'accepts': ['abb', 'abc']
        , 'not accepts': ['abc', 'abbc']
    }
    , {
        'r1': 'ab*'
        , 'r2': 'a*b'
        , 'exp': 'ab'
        , 'accepts': ['ab']
        , 'not accepts': ['abb', 'aab']
    }
])
def automatic_suite(request):
    regex1 = Regex(request.param['r1'])
    regex2 = Regex(request.param['r2'])
    exp = Regex(request.param['exp'])

    a_pfl = regex1.to_epsilon_nfa()
    b_pfl = regex2.to_epsilon_nfa()
    exp_pfl = exp.to_epsilon_nfa()

    return {
        'left': a_pfl
        , 'right': b_pfl
        , 'expected': exp_pfl
        , 'accepts': request.param['accepts']
        , 'not accepts': request.param['not accepts']
    }

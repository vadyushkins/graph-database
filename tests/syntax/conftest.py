import pytest

examples = [
    "connect to database db_1;"
    , "select pairs from g1;"
    , "select count from g2 where (((a|b)|(c*))*);"
    , "select pairs from intersection of g1 and g2 where ((a*)|(b*));"
    , "\
    connect to database resources/database_1;\
    select pairs from g1;\
    select count from g2 where (((a|b)|(c*))*);\
    "
    , "\
    connect to database resources_database_42;\
    select pairs from intersection of g1 and g2 where ((a*)|(b*));\
    "
    , "\
    connect to database resources/database_1;\
    select pairs from g1;\
    select count from g2 where (((a|b)|(c*))*);\
    connect to database resources_database_42;\
    select pairs from intersection of g1 and g2 where ((a*)|(b*));\
    "
]


@pytest.fixture(scope='session', params=examples)
def suite(request):
    return request.param

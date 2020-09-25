from src.CYK import cyk


def test_manual_accepted(manual_suite_accepted):
    cfg = manual_suite_accepted['cfg']
    accepted = manual_suite_accepted['accepted']

    assert cyk(accepted, cfg) is True


def test_manual_not_accepted(manual_suite_not_accepted):
    cfg = manual_suite_not_accepted['cfg']
    not_accepted = manual_suite_not_accepted['not accepted']

    assert cyk(not_accepted, cfg) is False


def test_automatic_accepted(automatic_suite_accepted):
    cfg = automatic_suite_accepted['cfg']
    accepted = automatic_suite_accepted['accepted']

    assert cyk(accepted, cfg) is True


def test_automatic_not_accepted(automatic_suite_not_accepted):
    cfg = automatic_suite_not_accepted['cfg']
    not_accepted = automatic_suite_not_accepted['not accepted']

    assert cyk(not_accepted, cfg) is False

from src.CYK import cyk


def test_manual_accepted(accepted_manual_suite):
    cnf = accepted_manual_suite['cnf']
    accepted = accepted_manual_suite['accepted']

    assert cyk(accepted, cnf) is True


def test_manual_not_accepted(not_accepted_manual_suite):
    cnf = not_accepted_manual_suite['cnf']
    not_accepted = not_accepted_manual_suite['not accepted']

    assert cyk(not_accepted, cnf) is False


def test_automatic_accepted(accepted_automatic_suite):
    cnf = accepted_automatic_suite['cnf']
    accepted = accepted_automatic_suite['accepted']

    assert cyk(accepted, cnf) is True


def test_automatic_not_accepted(not_accepted_automatic_suite):
    cnf = not_accepted_automatic_suite['cnf']
    not_accepted = not_accepted_automatic_suite['not accepted']

    assert cyk(not_accepted, cnf) is False

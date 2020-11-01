def test_manual(manual_suite, algo, tmp_path):
    graph_file = tmp_path / 'graph.txt'
    graph_file.write_text('\n'.join(manual_suite['graph']))

    grammar_file = tmp_path / 'grammar.txt'
    grammar_file.write_text('\n'.join(manual_suite['grammar']))

    actual = algo(graph_file, grammar_file).cfpq()

    expected = manual_suite['expected']

    assert actual == expected

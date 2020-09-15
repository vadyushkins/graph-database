from pyformlang.regular_expression import Regex

from src.graph.LabeledGraph import LabeledGraph


class RegexGraph(LabeledGraph):
    def __init__(self, regex: Regex):
        self.regex = regex
        self.dfa = regex.to_epsilon_nfa().to_deterministic().minimize()
        super().__init__(len(self.dfa.states))

        transitions = list()
        for v, label, to in self.dfa._transition_function.get_edges():
            transitions.append((str(v), str(label), str(to)))
        transitions.sort(key=lambda x: (x[1], x[0], x[2]))

        for v, label, to in transitions:
            self.append(f'{v} {label} {to}', compress=True)
            self[f'{label}'][self.vertices[v], self.vertices[to]] = True

    def accepts(self, word):
        return self.dfa.accepts(word)

    @classmethod
    def from_regex_in_txt(cls, path):
        with open(path, 'r') as f:
            regex = f.readline().replace('\n', '')
            return RegexGraph(Regex(regex))

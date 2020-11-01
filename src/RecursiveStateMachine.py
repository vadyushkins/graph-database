from pyformlang.cfg import *
from pyformlang.regular_expression import Regex

from src.MyCNF import MyCNF


class RecursiveStateMachine:
    def __init__(self):
        self.start_symbol = None
        self.boxes = dict()

    def to_cfg(self):
        variables = set()
        terminals = set()
        start_symbol = self.start_symbol
        productions = set()

        cnt = 1
        for x in self.boxes:
            head = Variable(x)
            variables.add(head)
            for box in self.boxes[x]:
                name = {box.start_state: head}
                for s in box.states:
                    if s not in name:
                        name[s] = Variable(f'S{cnt}')
                        cnt += 1
                        variables.add(name[s])
                    if s in box.final_states:
                        productions.add(Production(name[s], []))
                for v in box._transition_function._transitions:
                    for label in box._transition_function._transitions[v]:
                        to = box._transition_function._transitions[v][label]

                        if label.value == label.value.lower():
                            terminals.add(Terminal(label.value))
                            productions.add(Production(name[v], [Terminal(label.value), name[to]]))
                        else:
                            productions.add(Production(name[v], [Variable(label.value), name[to]]))

        return CFG(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions
        )

    def to_mycnf(self):
        cfg = self.to_cfg()

        return MyCNF(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions
        )

    @classmethod
    def from_text(cls, text, start_symbol='S'):
        rsm = RecursiveStateMachine()

        rsm.start_symbol = start_symbol

        changing = True
        while changing:
            changing = False
            productions = text.split('\n')
            eps_head, eps_body = None, None
            for p in productions:
                head, body = p.split(' -> ')
                if body == '':
                    eps_head = head
                    eps_body = body
            new_productions = list()
            for p in productions:
                head, body = p.split(' -> ')
                if head == eps_head and body == eps_body:
                    continue
                new_body = list()
                for b in body.split():
                    if b == eps_head:
                        new_body.append(f'({eps_head}|$)')
                        changing = True
                    else:
                        new_body.append(b)
                new_body = " ".join(new_body)
                if head == eps_head:
                    new_body = f'({new_body})|$'
                new_productions.append(f'{head} -> {new_body}')
            text = '\n'.join(new_productions)

        changing = True
        while changing:
            changing = False
            productions = text.split('\n')
            tmp = dict()
            for p in productions:
                head, body = p.split(' -> ')
                tmp[head] = tmp.get(head, list()) + [body]
            new_productions = list()
            for head in tmp:
                if len(tmp[head]) > 1:
                    new_body = '|'.join(
                        map(
                            lambda x: f'({x})',
                            tmp[head]
                        )
                    )
                    new_productions.append(f'{head} -> {new_body}')
                    changing = True
                else:
                    new_productions.append(f'{head} -> {tmp[head][0]}')
            text = '\n'.join(new_productions)

        productions = text.split('\n')

        for p in productions:
            head, body = p.split(' -> ')
            body = body.replace('epsilon', '$').replace('eps', '$')
            if body == '':
                body = '$'
            rsm.boxes[head] = rsm.boxes.get(head, list()) + [
                Regex(body) \
                    .to_epsilon_nfa() \
                    .to_deterministic() \
                    .minimize()
            ]

        return rsm

    @classmethod
    def from_txt(cls, path):
        productions = []
        with open(path, 'r') as f:
            for line in f:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        text = '\n'.join(productions)

        return RecursiveStateMachine.from_text(text)

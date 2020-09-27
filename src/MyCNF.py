from typing import AbstractSet, Iterable

from pyformlang.cfg import *


class MyCNF(CFG):
    def __init__(self,
                 variables: AbstractSet[Variable] = None,
                 terminals: AbstractSet[Terminal] = None,
                 start_symbol: Variable = None,
                 productions: Iterable[Production] = None):
        cfg = CFG(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions
        )
        eps = cfg.generate_epsilon()
        cfg = cfg.to_normal_form()

        if eps is True:
            cfg._productions |= {Production(cfg._start_symbol, [])}

        super(MyCNF, self).__init__(
            variables=cfg._variables,
            terminals=cfg._terminals,
            start_symbol=cfg._start_symbol,
            productions=cfg._productions
        )

        self.heads_for_body = dict()
        self.bodies_for_head = dict()

        for p in self._productions:
            if len(p.body) == 1:
                body = p.body[0]
            else:
                body = tuple(p.body)
            self.heads_for_body[body] = self.heads_for_body.get(body, set()) | {p.head}
            self.bodies_for_head[p.head] = self.bodies_for_head.get(p.head, set()) | {body}

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")):
        cfg = CFG.from_text(text, start_symbol=start_symbol)

        return MyCNF(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions
        )

    @classmethod
    def from_txt(cls, path):
        productions = []
        with open(path, 'r') as f:
            for line in f:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        cfg = CFG.from_text('\n'.join(productions))

        return MyCNF(
            variables=cfg.variables,
            terminals=cfg.terminals,
            start_symbol=cfg.start_symbol,
            productions=cfg.productions
        )

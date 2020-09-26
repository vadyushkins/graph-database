from pyformlang.cfg import Variable

from src.MyCFG import MyCFG


class MyCNF:
    def __init__(self, cfg: MyCFG, weak: bool = False):
        self.cfg = cfg
        self.variables = set()
        self.terminals = set()
        self.start_symbol = 'S'
        self.unit_productions = set()
        self.pair_productions = set()
        self.heads_for_body = dict()
        self.bodies_for_head = dict()

        if weak is True:
            cfg = cfg.to_weak_normal_form()
        else:
            cfg = cfg.to_normal_form()

        for variable in cfg.variables:
            self.variables.add(variable.value)

        for terminal in cfg.terminals:
            self.terminals.add(terminal.value)

        self.start_symbol = cfg.start_symbol.value

        for production in cfg.productions:
            head = production.head.value
            body = None
            if len(production.body) == 1:
                body = production.body[0].value
                self.unit_productions.add((head, body))
            else:
                body = (production.body[0].value, production.body[1].value)
                self.pair_productions.add((head, body))

            if body not in self.heads_for_body:
                self.heads_for_body[body] = set()
            self.heads_for_body[body].add(head)

            if head not in self.bodies_for_head:
                self.bodies_for_head[head] = set()
            self.bodies_for_head[head].add(body)

    @classmethod
    def from_text(cls, text, start_symbol='S'):
        cfg = MyCFG.from_text(text, start_symbol=Variable(start_symbol))

        return MyCNF(cfg)

    @classmethod
    def from_txt(cls, path, weak=False):
        cfg = MyCFG.from_txt(path, weak)

        return MyCNF(cfg, weak)

from pyformlang.cfg import *


class MyCFG(CFG):
    def to_weak_normal_form(self) -> "MyCFG":
        if self._normal_form is not None:
            return self._normal_form

        nullables = self.get_nullable_symbols()
        unit_pairs = self.get_unit_pairs()
        generating = self.get_generating_symbols()
        reachables = self.get_reachable_symbols()

        if (len(nullables) != 0 or
                len(unit_pairs) != len(self._variables) or
                len(generating) != len(self._variables) + len(self._terminals) or
                len(reachables) != len(self._variables) + len(self._terminals)):

            if len(self._productions) == 0:
                self._normal_form = self
                return self

            new_cfg = self.remove_useless_symbols().eliminate_unit_productions().remove_useless_symbols()

            cfg = new_cfg.to_weak_normal_form()
            self._normal_form = cfg

            return cfg

        new_productions = self._get_productions_with_only_single_terminals()

        cfg = MyCFG(start_symbol=self._start_symbol, productions=set(new_productions))
        self._normal_form = cfg

        return cfg

    @classmethod
    def from_txt(cls, path, weak=False):
        productions = []
        with open(path, 'r') as f:
            for line in f:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        gr = MyCFG.from_text('\n'.join(productions))

        if weak is True:
            gr = gr.to_weak_normal_form()
        else:
            gr = gr.to_normal_form()

        return gr

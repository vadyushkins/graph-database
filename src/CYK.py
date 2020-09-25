from itertools import product
from typing import List

from pyformlang.cfg import *

from src.MyCFG import MyCFG


def cyk(s: List[Terminal], gr: MyCFG):
    n = len(s)

    if n == 0:
        return True  # Temporary patch because https://github.com/Aunsiels/pyformlang/issues/2
        return gr.generate_epsilon()

    dp = [[set() for _ in range(n)] for _ in range(n)]

    ups = dict()
    pps = dict()

    for p in gr.productions:
        if len(p.body) == 1:
            u = p.body[0]
            if u not in ups:
                ups[u] = set()
            ups[u].add(p.head)
        else:
            t = tuple(p.body)
            if t not in pps:
                pps[t] = set()
            pps[t].add(p.head)

    for i in range(n):
        dp[i][0] |= ups.get(s[i], set())

    for d in range(1, n):
        for i in range(n - d):
            for p in range(i, i + d):
                for l, r in product(dp[i][p - i], dp[p + 1][i + d - p - 1]):
                    dp[i][d] |= pps.get((l, r), set())

    return gr.start_symbol in dp[0][n - 1]

from itertools import product
from typing import List

from pyformlang.cfg import *

from src.MyCNF import MyCNF


def cyk(s: List[Terminal], cnf: MyCNF):
    n = len(s)

    if n == 0:
        return cnf.generate_epsilon()

    dp = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        dp[i][0] |= cnf.heads_for_body.get(s[i], set())

    for d in range(1, n):
        for i in range(n - d):
            for p in range(i, i + d):
                for l, r in product(dp[i][p - i], dp[p + 1][i + d - p - 1]):
                    dp[i][d] |= cnf.heads_for_body.get((l, r), set())

    return cnf.start_symbol in dp[0][n - 1]

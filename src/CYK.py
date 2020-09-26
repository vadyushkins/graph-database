from itertools import product

from src.MyCNF import MyCNF


def cyk(s: str, gr: MyCNF):
    n = len(s)

    if n == 0:
        return gr.cfg.generate_epsilon()

    dp = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        dp[i][0] |= gr.heads_for_body.get(s[i], set())

    for d in range(1, n):
        for i in range(n - d):
            for p in range(i, i + d):
                for l, r in product(dp[i][p - i], dp[p + 1][i + d - p - 1]):
                    dp[i][d] |= gr.heads_for_body.get((l, r), set())

    return gr.start_symbol in dp[0][n - 1]

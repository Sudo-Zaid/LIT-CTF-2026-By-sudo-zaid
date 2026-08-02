#!/usr/bin/env python3
"""
LIT CTF 2026 — rev — "pathfinder" (check)

The binary wants LITCTF{ <inner> } where <inner> is a string of '(' and ')' that is a
valid balanced sequence of 35 '(' and 35 ')' (a Dyck path). While scanning it keeps two
counters A (opens) and C (closes) and a 64-bit SUM:

    '(' : require A < 35 ;                         A += 1
    ')' : require A > C  ; SUM += f[A+1][C] ;      C += 1     (f[A+1][C]=0 when A==35)
    end : require A == 35 and C == 35 and SUM == 0x128e740722b291ad

`f[a][c]` (built at runtime in .bss) is the number of ways to complete a valid path from
state (a opens, c closes) to (35,35):  f[a][c] = f[a+1][c]·(a<35) + f[a][c+1]·(a>c),
f[35][35]=1  — i.e. the Catalan/ballot DP.

Because ')' adds f[A+1][C] = "number of completions that would have gone '(' here",
SUM is exactly the LEXICOGRAPHIC RANK of the path ('(' < ')'). The target
MAGIC = 0x128e740722b291ad = 1337133713371337133, so we just UNRANK it.
"""
N = 35
MAGIC = 0x128e740722b291ad          # == 1337133713371337133

def main():
    f = [[0]*(N+2) for _ in range(N+2)]
    f[N][N] = 1
    for a in range(N, -1, -1):
        for c in range(N, -1, -1):
            if a == N and c == N:
                continue
            f[a][c] = (f[a+1][c] if a < N else 0) + (f[a][c+1] if a > c else 0)

    R, a, c, path = MAGIC, 0, 0, []
    for _ in range(2*N):
        open_paths = f[a+1][c] if a < N else 0
        if a < N and R < open_paths:
            path.append('('); a += 1
        else:
            R -= open_paths                 # skip all '(' completions -> take ')'
            path.append(')'); c += 1
    assert R == 0 and a == N == c
    print("[+] LITCTF{" + "".join(path) + "}")

if __name__ == "__main__":
    main()

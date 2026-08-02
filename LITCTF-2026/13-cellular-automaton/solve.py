#!/usr/bin/env python3
"""
LIT CTF 2026 — rev — "cellular automaton"

The binary (from main disasm):
  1. fread 26 bytes (the flag) -> 208 bits, MSB-first per byte.
  2. 32 generations of Rule 90 on a CYCLIC array of 208 cells:
         new[j] = cells[(j-1) % 208] XOR cells[(j+1) % 208]
  3. Pack 208 bits back to 26 bytes, print as hex.

Rule 90 is LINEAR over GF(2), so 32 generations is a fixed 208x208 GF(2) matrix M
with  out = M * in. We invert it by Gaussian elimination. M has rank 192 (nullspace
dim 16 -> 2^16 preimages), so we pin the unique flag by adding the known "LITCTF{"
prefix bits as extra equations. ("going back in time" = undoing the generations.)
"""
OUT = "652b481a7c203a240b244f045b365f090016050e58227d270b37"
N, GEN = 208, 32

def forward(cell):
    cell = cell[:]
    for _ in range(GEN):
        cell = [cell[(j-1) % N] ^ cell[(j+1) % N] for j in range(N)]
    return cell

def main():
    out = bytes.fromhex(OUT)
    y = [(out[i//8] >> (7-(i%8))) & 1 for i in range(N)]

    cols = [forward([1 if k == p else 0 for k in range(N)]) for p in range(N)]
    eqs = []
    for j in range(N):
        mask = 0
        for p in range(N):
            if cols[p][j]:
                mask |= (1 << p)
        eqs.append(mask | (y[j] << 208))

    # known-plaintext: flag begins with "LITCTF{"
    for i, ch in enumerate(b"LITCTF{"):
        for k in range(8):
            eqs.append((1 << (i*8+k)) | (((ch >> (7-k)) & 1) << 208))

    rows = eqs[:]; piv = {}; r = 0
    for col in range(N):
        sel = next((i for i in range(r, len(rows)) if (rows[i] >> col) & 1), None)
        if sel is None:
            continue
        rows[r], rows[sel] = rows[sel], rows[r]
        for i in range(len(rows)):
            if i != r and ((rows[i] >> col) & 1):
                rows[i] ^= rows[r]
        piv[col] = r; r += 1

    x = [0]*N
    for col, rr in piv.items():
        x[col] = (rows[rr] >> 208) & 1
    assert forward(x) == y, "not a valid preimage"
    flag = bytes(sum(x[i*8+k] << (7-k) for k in range(8)) for i in range(26))
    print("[+]", flag.decode())

if __name__ == "__main__":
    main()

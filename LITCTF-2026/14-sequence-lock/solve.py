#!/usr/bin/env python3
"""
LIT CTF 2026 — rev — "sequence lock" (seqlock)

Flag format check: strncmp prefix "LITCTF{" + last char '}', and the INNER content
(between braces) must be exactly 20 bytes. Then main runs a Fibonacci "chain":

    state = 0xAA
    for i in range(20):
        state ^= (fib[i] + inner[i]) & 0xff        # fib = 1,1,2,3,5,8,...
        assert (state & 0xff) == target[i]         # target = 20 bytes @ vaddr 0x2140

All operations are invertible:
    (fib[i] + inner[i]) & 0xff = target[i] ^ prev_state
    inner[i] = ((target[i] ^ prev_state) - fib[i]) & 0xff     (prev_state[-1] = 0xAA)
"""
import struct, os

BIN = os.path.join(os.path.dirname(__file__), "seqlock")

def main():
    d = open(BIN, "rb").read()
    # locate the 20-byte target at vaddr 0x2140
    e_shoff = struct.unpack("<Q", d[0x28:0x30])[0]
    ent = struct.unpack("<H", d[0x3a:0x3c])[0]; n = struct.unpack("<H", d[0x3c:0x3e])[0]
    off = None
    for i in range(n):
        o = e_shoff + i*ent
        _, _, _, addr, offset, size, *_ = struct.unpack("<IIQQQQIIQQ", d[o:o+64])
        if size and addr <= 0x2140 < addr + size:
            off = offset + (0x2140 - addr); break
    target = d[off:off+20]

    fib = [1, 1]
    for _ in range(18):
        fib.append(fib[-1] + fib[-2])
    fib = [x & 0xff for x in fib]

    prev, inner = 0xAA, []
    for i in range(20):
        inner.append(((target[i] ^ prev) - fib[i]) & 0xff)
        prev = target[i]

    flag = b"LITCTF{" + bytes(inner) + b"}"
    print("[+]", flag.decode())

if __name__ == "__main__":
    main()

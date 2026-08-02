#!/usr/bin/env python3
"""
LIT CTF 2026 - "extremely original" (crypto)

Only the challenge text is given:

    It seems that I have accidentally leaked my flag: oyO+UrMXccyqeo2W+WA5jZPVXNSAyYVwGt
    Good thing that my computer generated keys before releasing the flag to the public.
    The flag will be "LITCTF" followed by a string of characters. Insert curly braces.

Model:
  * 34 chars, all inside the base64 alphabet, but NOT a valid stripped base64 of a byte
    string (the trailing pad bits of the last char are non-zero) -> it is not
    b64(bytes), it is 34 *symbols*: one cipher symbol per plaintext character.
  * "insert curly braces" == braces are not representable -> plaintext alphabet is the
    64-char base64 alphabet, which has no '{' '}' '_'.
  * "eXtremely ORiginal" -> XOR, applied to the 6-bit alphabet *indices*.
  * "my computer generated keys" -> keystream from a (weak) PRNG.

The PRNG turns out to be a textbook LCG mod 64:  k_{i+1} = (21*k_i + 27) mod 64, k_0 = 35.
Its whole parameter space is only 64^3 = 262144 triples, so the known "LITCTF"
prefix recovers it instantly.
"""
import string

ALPH = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'
CT = 'oyO+UrMXccyqeo2W+WA5jZPVXNSAyYVwGt'
C = [ALPH.index(ch) for ch in CT]
KNOWN = 'LITCTF'

COMBINERS = {                       # decrypt(cipher_symbol, key_symbol)
    'xor': lambda c, k: c ^ k,
    'add': lambda c, k: (c - k) % 64,   # c = p + k
    'sub': lambda c, k: (c + k) % 64,   # c = p - k
}


def lcg(a, c, s0, n=34):
    """k_0 = s0, k_{i+1} = (a*k_i + c) mod 64"""
    ks, s = [], s0
    for _ in range(n):
        ks.append(s)
        s = (a * s + c) % 64
    return ks


def solve():
    for a in range(64):
        for c in range(64):
            for s0 in range(64):
                ks = lcg(a, c, s0)
                for name, dec in COMBINERS.items():
                    pt = ''.join(ALPH[dec(x, k)] for x, k in zip(C, ks))
                    if pt.startswith(KNOWN):
                        yield a, c, s0, name, pt


if __name__ == '__main__':
    for a, c, s0, comb, pt in solve():
        ks = lcg(a, c, s0)
        enc = ''.join(ALPH[ALPH.index(p) ^ k] for p, k in zip(pt, ks))
        print(f'[+] LCG k_(i+1) = ({a}*k_i + {c}) mod 64, k_0 = {s0}, combiner = {comb}')
        print(f'    keystream : {ks}')
        print(f'    plaintext : {pt}')
        print(f'    re-encrypt matches ciphertext: {enc == CT}')
        print(f'    FLAG      : LITCTF{{{pt[len(KNOWN):]}}}')

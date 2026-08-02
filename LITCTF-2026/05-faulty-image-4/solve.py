#!/usr/bin/env python3
"""
LIT CTF 2026 — crypto/stego — "faulty image 4" (corrupt4.png)

Prompt: the flag you see is a decoy; the hacker corrupted some pixels, "separating them
from encoding information together as a whole".
Hint: some pixels have unusually small blue values, "almost like they've been clipped to
4 bits. Which pixels exactly?"

Findings:
  * The clipped pixels (blue < 16) all live in row 0.
  * Their x-coordinates are exactly the PRIME numbers (2,3,5,7,11,13,...,251) -> that's
    "which pixels exactly".
  * Each clipped blue value is a 4-bit nibble. Concatenate the nibbles in x order,
    high-nibble-first, two per byte -> the real flag.
"""
from PIL import Image
import numpy as np, os

SRC = os.path.join(os.path.dirname(__file__), "corrupt4.png")

def main():
    a = np.array(Image.open(SRC).convert("RGB"))
    B = a[:, :, 2]
    ys, xs = np.where(B < 16)                 # 4-bit-clipped blue channel
    order = np.argsort(xs)                     # left-to-right (prime order)
    nib = [int(B[ys[i], xs[i]]) for i in order]
    flag = bytes((nib[i] << 4) | nib[i+1] for i in range(0, len(nib) - 1, 2))
    print("[+] clipped pixels:", len(nib), "at x =", sorted(int(x) for x in xs))
    print("[+] flag:", flag.decode())

if __name__ == "__main__":
    main()
